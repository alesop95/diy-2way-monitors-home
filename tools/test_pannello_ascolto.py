import copy
import http.client
import json
from pathlib import Path
import threading
import unittest
from controllo_ascolto import Observation
from test_monitor_dsp import FakePeer
from pannello_ascolto import Session, make_server,load_session

ROOT=Path(__file__).resolve().parents[1]


def profiles():
    cfg=json.loads((ROOT/'config/camilladsp/offline-lr4.json').read_text(encoding='utf-8'))
    other=copy.deepcopy(cfg); other['title']+=' Ascolto'
    return {'mix':cfg,'ascolto':other}


class ListeningSession(unittest.TestCase):
    def setUp(self):
        self.peer=FakePeer(loaded_state='Running')
        self.good=True
        self.session=Session(self.peer,profiles(),observer=lambda cfg:Observation(48000,self.good,True,True))

    def test_prepare_enable_volume_and_mute_are_separate_actions(self):
        self.session.action('prepare',{'profile':'mix'})
        self.assertTrue(self.peer.muted)
        self.session.action('enable',{'volume':-24})
        self.session.action('volume',{'volume':-18})
        self.assertEqual(self.peer.volume,-18)
        self.session.action('mute',{})
        self.assertTrue(self.peer.muted); self.assertEqual(self.peer.volume,-60)
        self.session.action('enable',{'volume':-24})
        self.assertFalse(self.peer.muted)

    def test_watchdog_loss_and_recovery_do_not_restore_audio(self):
        self.session.action('prepare',{'profile':'mix'}); self.session.action('enable',{'volume':-24})
        self.good=False; state=self.session.poll()
        self.assertFalse(state['ready']); self.assertTrue(state['mute'])
        self.good=True; self.session.poll()
        self.assertTrue(self.peer.muted)
        self.session.action('prepare',{'profile':'ascolto'})
        self.assertTrue(self.peer.muted)

    def test_foreign_profile_is_not_modified_and_invalid_actions_do_not_reach_rpc(self):
        for name,body in (('prepare',{'profile':'../../altro'}),('enable',{'volume':float('nan')}),('unknown',{})):
            before=len(self.peer.calls)
            with self.assertRaises(ValueError): self.session.action(name,body)
            self.assertEqual(len(self.peer.calls),before)
        self.peer.config={'title':'ESTRANEO'}
        with self.assertRaises(RuntimeError): self.session.action('prepare',{'profile':'mix'})
        self.assertFalse(any(isinstance(x,dict) and 'SetConfigJson' in x for x in self.peer.calls))

    def test_preflight_missing_identity_blocks_before_rpc(self):
        session=Session(self.peer,profiles(),identity=lambda:False)
        with self.assertRaises(RuntimeError): session.action('prepare',{'profile':'mix'})
        self.assertEqual(self.peer.calls,[])

    def test_identity_loss_on_reprepare_immediately_mutes_owned_audio(self):
        self.session.action('prepare',{'profile':'mix'}); self.session.action('enable',{'volume':-24})
        self.session.identity=lambda:False
        with self.assertRaises(RuntimeError): self.session.action('prepare',{'profile':'ascolto'})
        self.assertTrue(self.peer.muted); self.assertFalse(self.session.controller.ready)

    def test_link_preparation_failure_stays_muted_and_revokes_readiness(self):
        def fail(cfg): raise RuntimeError('Link non qualificato')
        session=Session(self.peer,profiles(),after_prepare=fail)
        with self.assertRaises(RuntimeError): session.action('prepare',{'profile':'mix'})
        self.assertTrue(self.peer.muted); self.assertEqual(self.peer.volume,-60)
        self.assertFalse(session.controller.ready)

    def test_unqualified_example_stops_before_missing_hardware_profiles(self):
        with self.assertRaisesRegex(ValueError,'non qualificata'):
            load_session(ROOT/'config/controllo-ascolto/pannello-alsa.example.json')

    def test_pipewire_catalogue_is_read_without_connecting_or_autoconnect(self):
        session=load_session(ROOT/'config/controllo-ascolto/pannello-pipewire.example.json')
        self.assertEqual(set(session.profiles),{'mix','ascolto'})
        self.assertTrue(all(p['devices']['playback']['autoconnect_to'] is None for p in session.profiles.values()))

    def test_closing_owned_session_mutes_and_closing_foreign_session_does_not_modify_it(self):
        self.session.action('prepare',{'profile':'mix'}); self.session.action('enable',{'volume':-24})
        self.session.close()
        self.assertTrue(self.peer.muted); self.assertEqual(self.peer.volume,-60)
        self.session.action('prepare',{'profile':'mix'}); self.session.action('enable',{'volume':-24})
        self.peer.config={'title':'ESTRANEO'}
        before=len(self.peer.calls); self.session.close()
        self.assertFalse(any(isinstance(x,dict) for x in self.peer.calls[before:]))

    def test_reconnected_transport_retries_unconfirmed_mute_without_restoring_audio(self):
        class DroppingPeer(FakePeer):
            online=True
            def call(self,command):
                if not self.online: raise OSError('Connessione interrotta')
                return super().call(command)
        peer=DroppingPeer(loaded_state='Running'); session=Session(peer,profiles())
        session.action('prepare',{'profile':'mix'}); session.action('enable',{'volume':-24})
        peer.online=False; state=session.poll()
        self.assertIsNone(state['mute']); self.assertFalse(state['ready'])
        peer.online=True; recovered=session.poll()
        self.assertTrue(peer.muted); self.assertEqual(peer.volume,-60)
        self.assertFalse(recovered['ready'])


class HttpContracts(unittest.TestCase):
    def setUp(self):
        self.peer=FakePeer(loaded_state='Running'); self.session=Session(self.peer,profiles())
        self.server=make_server(self.session,port=0)
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True); self.thread.start()

    def tearDown(self):
        self.server.shutdown(); self.server.server_close(); self.thread.join()

    def request(self,method,path,body=None,headers=None):
        c=http.client.HTTPConnection('127.0.0.1',self.server.server_address[1],timeout=2)
        c.request(method,path,body=body,headers=headers or {})
        response=c.getresponse(); raw=response.read(); status=response.status; c.close()
        return status,raw

    def test_page_status_and_authenticated_action(self):
        status,page=self.request('GET','/')
        self.assertEqual(status,200); self.assertIn(self.server.token.encode(),page)
        self.assertNotIn(b'__TOKEN__',page)
        status,raw=self.request('GET','/api/status')
        self.assertEqual(status,200); self.assertEqual(set(json.loads(raw)['profiles']),{'mix','ascolto'})
        code,_=self.request('POST','/api/prepare',json.dumps({'profile':'mix'}),
                            {'Content-Type':'application/json','X-Session-Token':self.server.token})
        self.assertEqual(code,200); self.assertTrue(self.peer.muted)

    def test_cross_site_and_rebinding_requests_cannot_change_state(self):
        for headers in ({'Content-Type':'application/json'},
                        {'Content-Type':'application/json','X-Session-Token':self.server.token,'Origin':'https://esterno.invalid'},
                        {'Content-Type':'application/json','X-Session-Token':self.server.token,'Host':'esterno.invalid'}):
            with self.subTest(headers=headers):
                status,_=self.request('POST','/api/mute','{}',headers)
                self.assertEqual(status,403)
        self.assertEqual(self.peer.calls,[])

    def test_bad_json_unknown_action_and_static_paths_are_rejected(self):
        headers={'Content-Type':'application/json','X-Session-Token':self.server.token}
        self.assertEqual(self.request('POST','/api/mute','[]',headers)[0],400)
        self.assertEqual(self.request('POST','/api/SetConfigJson','{}',headers)[0],400)
        self.assertEqual(self.request('GET','/../../CLAUDE.md')[0],404)
        self.assertEqual(self.peer.calls,[])


if __name__=='__main__': unittest.main()
