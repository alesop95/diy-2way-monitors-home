"""Contratti del supervisore: richieste RPC osservabili, non hardware simulato."""
import copy
import json
from pathlib import Path
import unittest
from test_monitor_dsp import FakePeer
from controllo_ascolto import Controller, Observation, validate_profile

ROOT = Path(__file__).resolve().parents[1]


class ListeningControl(unittest.TestCase):
    def setUp(self):
        self.cfg = json.loads((ROOT/'config/camilladsp/offline-lr4.json').read_text(encoding='utf-8'))
        self.good = Observation(48000,True,True,True)

    def test_hardware_rejected_before_any_rpc(self):
        self.cfg['devices']['capture']['type']='Alsa'
        peer = FakePeer(loaded_state='Running')
        with self.assertRaises(ValueError):
            Controller(peer).prepare(self.cfg)
        self.assertEqual(peer.calls,[])

    def test_normalized_config_and_delayed_commit_are_supported(self):
        class CanonicalPeer(FakePeer):
            pending=None
            delay=0
            def call(self,command):
                if isinstance(command,dict) and 'ValidateConfigJson' in command:
                    self.calls.append(command)
                    cfg=json.loads(command['ValidateConfigJson'])
                    cfg['devices']['enable_rate_adjust']=False
                    cfg['devices']['capture']['skip_bytes']=0
                    return json.dumps(cfg)
                if isinstance(command,dict) and 'SetConfigJson' in command:
                    super().call(command)
                    self.pending=json.loads(command['SetConfigJson'])
                    self.pending['devices']['enable_rate_adjust']=False
                    self.pending['devices']['capture']['skip_bytes']=0
                    self.config=None; self.delay=2
                    return None
                if command=='GetConfigJson' and self.pending:
                    if self.delay:
                        self.calls.append(command); self.delay-=1; return None
                    self.config=json.dumps(self.pending)
                    self.pending=None
                return super().call(command)
        peer=CanonicalPeer(loaded_state='Running')
        control=Controller(peer)
        control.prepare(self.cfg)
        self.assertTrue(control.ready)
        self.assertIs(control.profile['devices']['enable_rate_adjust'],False)
        control.enable(self.good,-24)
        self.assertFalse(peer.muted)
        peer.config=json.dumps(dict(control.profile,description='alterata dopo il caricamento'))
        with self.assertRaises(RuntimeError): control.enable(self.good,-24)
        self.assertTrue(peer.muted)

    def test_prepare_always_returns_muted_minus60_and_requires_explicit_enable(self):
        peer = FakePeer(loaded_state='Running')
        control = Controller(peer)
        control.prepare(self.cfg)
        self.assertTrue(peer.muted)
        self.assertEqual(peer.volume,-60)
        control.enable(self.good,-20)
        self.assertFalse(peer.muted)
        self.assertEqual(peer.volume,-20)

    def test_each_missing_condition_prevents_unmute(self):
        for bad in (Observation(44100,True,True,True),Observation(48000,False,True,True),
                    Observation(48000,True,False,True),Observation(48000,True,True,False)):
            with self.subTest(bad=bad):
                peer = FakePeer(loaded_state='Running'); control=Controller(peer)
                control.prepare(self.cfg)
                with self.assertRaises(RuntimeError): control.enable(bad,-20)
                self.assertTrue(peer.muted)

    def test_starting_is_not_running(self):
        peer=FakePeer(loaded_state='Starting'); control=Controller(peer); control.prepare(self.cfg)
        with self.assertRaises(RuntimeError): control.enable(self.good,-20)
        self.assertTrue(peer.muted)

    def test_lost_clock_mutes_and_never_restores_old_level(self):
        peer=FakePeer(loaded_state='Running'); control=Controller(peer); control.prepare(self.cfg)
        control.enable(self.good,-20)
        control.observe(Observation(48000,False,True,True))
        self.assertTrue(peer.muted); self.assertEqual(peer.volume,-60)
        control.observe(self.good)
        self.assertTrue(peer.muted)
        with self.assertRaises(RuntimeError): control.enable(self.good,-20)

    def test_manual_mute_preserves_only_an_existing_qualification(self):
        peer=FakePeer(loaded_state='Running'); control=Controller(peer); control.prepare(self.cfg)
        control.enable(self.good,-24); control.manual_mute()
        self.assertTrue(peer.muted); self.assertEqual(peer.volume,-60); self.assertTrue(control.ready)
        control.enable(self.good,-24); self.assertFalse(peer.muted)
        control.observe(Observation(48000,False,True,True)); control.manual_mute()
        self.assertFalse(control.ready)

    def test_foreign_configuration_is_not_stopped_or_replaced(self):
        peer=FakePeer(loaded_state='Running'); peer.config={'title':'ALTRA APPLICAZIONE'}
        with self.assertRaises(RuntimeError): Controller(peer).prepare(self.cfg)
        self.assertFalse(any(isinstance(c,dict) and 'SetConfigJson' in c for c in peer.calls))
        self.assertNotIn('Stop',peer.calls)

    def test_changed_profile_and_nan_volume_cannot_be_enabled(self):
        peer=FakePeer(loaded_state='Running'); control=Controller(peer); control.prepare(self.cfg)
        with self.assertRaises(ValueError): control.enable(self.good,float('nan'))
        peer.config=json.dumps(dict(self.cfg,title='ALTERATA'))
        with self.assertRaises(RuntimeError): control.enable(self.good,-20)
        self.assertTrue(peer.muted)

    def test_external_files_and_extra_filter_filenames_are_rejected(self):
        for change in ('output','filter'):
            cfg=copy.deepcopy(self.cfg)
            if change=='output': cfg['devices']['playback']['filename']='../altro.pcm'
            else: cfg['filters']['esterno']={'type':'Conv','parameters':{'filename':'altro.wav'}}
            with self.assertRaises(ValueError): validate_profile(cfg)

    def test_existing_lab_title_does_not_authorize_touching_hardware(self):
        peer=FakePeer(loaded_state='Running')
        previous=copy.deepcopy(self.cfg); previous['devices']['capture']['type']='Alsa'
        peer.config=previous
        with self.assertRaises(ValueError): Controller(peer).prepare(self.cfg)
        self.assertFalse(any(isinstance(c,dict) for c in peer.calls))

    def test_successful_ack_without_applied_mute_is_detected(self):
        class LyingPeer(FakePeer):
            def call(self,command):
                if isinstance(command,dict) and 'SetMute' in command:
                    self.calls.append(command); return None
                return super().call(command)
        with self.assertRaises(RuntimeError): Controller(LyingPeer()).prepare(self.cfg)


if __name__ == '__main__': unittest.main()
