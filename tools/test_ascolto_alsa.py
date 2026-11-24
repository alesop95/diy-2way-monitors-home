import copy
import json
from pathlib import Path
import unittest
from ascolto_alsa import AlsaPolicy, AlsaObserver, digest, parse_hw_params, parse_control, make_candidate,canonical_candidate
from controllo_ascolto import Controller
from test_monitor_dsp import FakePeer

ROOT=Path(__file__).resolve().parents[1]


def fixture():
    cfg=json.loads((ROOT/'config/camilladsp/offline-lr4.json').read_text(encoding='utf-8'))
    m={'schema':'ascolto-alsa-1','verified':True,'card_id':'Test',
       'usb':{'vendor':'1234','product':'5678','serial_sha256':'a'*64},
       'pcm':{'capture_device':0,'playback_device':0,'capture_channels':18,'playback_channels':20,'format':'S32_LE'},
       'routing':{'sources':[8,9],'outputs':[4,5,6,7]},
       'clock':{'mode':'external','source_numid':3,'source_expected':'1','lock_numid':4,'lock_expected':'on',
                'rate_numid':5,'rate_values_hz':{'0':44100,'1':48000}},
       'profiles_sha256':{}}
    cfg=make_candidate(cfg,m)
    m['profiles_sha256']={'mix':digest(cfg)}
    proof={'schema':'qualifica-ascolto-1','verified':True,'card_id':m['card_id'],'usb':m['usb'],
           'pcm':m['pcm'],'routing':m['routing'],'clock':m['clock'],'profiles_sha256':m['profiles_sha256'],
           'physical_routing_verified':True,'volume_path_verified':True}
    raw=json.dumps(proof).encode()
    m['proof_sha256']=digest(raw)
    return cfg,m,raw


class AlsaQualification(unittest.TestCase):
    def test_kernel_format_aliases_are_compared_to_camilla_formats(self):
        cfg,m,_=fixture()
        for camilla,kernel in (('S24_3_LE','S24_3LE'),('F32_LE','FLOAT_LE'),('F64_LE','FLOAT64_LE')):
            with self.subTest(format=camilla):
                m['pcm']['format']=camilla
                state={'card':7,'card_id':'Test','usb':m['usb'],
                       'capture':{'format':kernel,'channels':18,'rate':48000},
                       'playback':{'format':kernel,'channels':20,'rate':48000}}
                calls=[]
                def control(card,numid):
                    calls.append(card); return {3:'1',4:'on',5:'1'}[numid]
                result=AlsaObserver(m,lambda:state,control).observe(cfg)
                self.assertTrue(result.clock_locked); self.assertEqual(set(calls),{7})

    def test_device_without_serial_requires_an_attested_usb_port(self):
        cfg,m,raw=fixture()
        m['usb']={'vendor':'1234','product':'5678','port_path':'pci0000:00/0000:00:14.0/usb1/1-2'}
        proof=json.loads(raw); proof['usb']=m['usb']; raw=json.dumps(proof).encode(); m['proof_sha256']=digest(raw)
        AlsaPolicy(m,{'mix':cfg},raw)
        self.assertTrue(m['usb']['port_path'])

    def test_candidate_normalization_never_loads_or_opens_the_device(self):
        cfg,m,_=fixture()
        source=json.loads((ROOT/'config/camilladsp/offline-lr4.json').read_text(encoding='utf-8'))
        class Reader:
            calls=[]
            def call(self,command):
                self.calls.append(command)
                if command=='GetVersion': return '4.1.3'
                if isinstance(command,dict) and 'ReadConfigJson' in command: return command['ReadConfigJson']
                raise AssertionError('Comando con effetti non ammesso')
        peer=Reader(); normalized=canonical_candidate(peer,source,m)
        self.assertEqual(normalized['devices']['capture']['type'],'Alsa')
        self.assertEqual(len(peer.calls),2)
        self.assertNotIn('SetConfigJson',str(peer.calls))

    def test_engine_defaults_are_accepted_but_active_mute_in_attested_route_is_rejected(self):
        cfg,m,raw=fixture()
        last=cfg['mixers']['uscite_fisiche']
        for row in last['mapping']:
            row['mute']=None
            row['sources'][0].update(mute=None,scale=None)
        def attest():
            m['profiles_sha256']={'mix':digest(cfg)}
            proof=json.loads(raw); proof['profiles_sha256']=m['profiles_sha256']
            data=json.dumps(proof).encode(); m['proof_sha256']=digest(data)
            return AlsaPolicy(m,{'mix':cfg},data)
        attest()
        last['mapping'][0]['sources'][0]['mute']=True
        with self.assertRaises(ValueError): attest()

    def test_core_accepts_hardware_only_through_the_explicit_attested_policy(self):
        cfg,m,raw=fixture(); policy=AlsaPolicy(m,{'mix':cfg},raw)
        peer=FakePeer(loaded_state='Running')
        with self.assertRaises(ValueError): Controller(peer).prepare(cfg)
        self.assertEqual(peer.calls,[])
        control=Controller(peer,validator=policy.validate,owner_prefix=policy.owner_prefix)
        control.prepare(cfg)
        control.prepare(cfg)
        self.assertTrue(control.ready); self.assertTrue(peer.muted)

    def test_candidate_has_exact_four_physical_destinations_and_no_other_routes(self):
        cfg,m,_=fixture()
        first=cfg['mixers'][cfg['pipeline'][0]['name']]
        self.assertEqual([r['sources'][0]['channel'] for r in first['mapping']],[8,8,9,9])
        last=cfg['mixers'][cfg['pipeline'][-1]['name']]
        self.assertEqual([r['dest'] for r in last['mapping']],[4,5,6,7])
        self.assertEqual(last['channels'],{'in':4,'out':20})
        self.assertEqual(cfg['devices']['volume_limit'],-6)
        self.assertTrue(cfg['devices']['stop_on_rate_change'])

    def test_realistic_kernel_and_enum_control_parsers(self):
        params=parse_hw_params('access: RW_INTERLEAVED\nformat: S32_LE\nchannels: 20\nrate: 48000 (48000/1)\n')
        self.assertEqual(params,{'format':'S32_LE','channels':20,'rate':48000})
        self.assertEqual(parse_hw_params('closed\n'),{})
        self.assertEqual(parse_control("numid=5\n; Item #1 '48000'\n: values=1\n"),'1')
        with self.assertRaises(ValueError): parse_control('missing values')

    def test_attestation_must_match_manifest_and_actual_profile(self):
        cfg,m,raw=fixture(); policy=AlsaPolicy(m,{'mix':cfg},raw)
        self.assertEqual(policy.validate(cfg),digest(cfg))
        changed=copy.deepcopy(cfg); changed['devices']['samplerate']=44100
        with self.assertRaises(ValueError): policy.validate(changed)
        for key in ('routing','clock','pcm'):
            bad=copy.deepcopy(m); bad[key]={}
            with self.subTest(key=key),self.assertRaises(ValueError): AlsaPolicy(bad,{'mix':cfg},raw)

    def test_example_cannot_enable_hardware_and_proof_cannot_be_forged_by_a_flag(self):
        cfg,m,raw=fixture(); m['verified']=False
        with self.assertRaises(ValueError): AlsaPolicy(m,{'mix':cfg},raw)
        m['verified']=True
        with self.assertRaises(ValueError): AlsaPolicy(m,{'mix':cfg},b'{}')

    def test_identity_pcm_and_clock_are_each_required(self):
        cfg,m,raw=fixture(); AlsaPolicy(m,{'mix':cfg},raw)
        state={'card':2,'card_id':'Test','usb':m['usb'],
               'capture':{'format':'S32_LE','channels':18,'rate':48000},
               'playback':{'format':'S32_LE','channels':20,'rate':48000}}
        controls={3:'1',4:'on',5:'1'}
        observer=AlsaObserver(m,lambda:state,lambda card,numid:controls[numid])
        self.assertTrue(observer.observe(cfg).clock_locked)
        for fault in ('identity','channels','rate','lock','source','clock_rate','hotplug'):
            with self.subTest(fault=fault):
                changed=copy.deepcopy(state); values=dict(controls)
                if fault=='identity': changed['usb']['serial_sha256']='b'*64
                elif fault=='channels': changed['playback']['channels']=4
                elif fault=='rate': changed['capture']['rate']=44100
                elif fault=='lock': values[4]='off'
                elif fault=='source': values[3]='0'
                elif fault=='clock_rate': values[5]='0'
                else: changed={}
                bad=AlsaObserver(m,lambda:changed,lambda c,n:values[n]).observe(cfg)
                self.assertFalse(all((bad.clock_locked,bad.routing_verified,bad.identity_matches,bad.rate_hz==48000)))

    def test_closed_pcm_and_failed_control_read_remain_unqualified(self):
        cfg,m,_=fixture()
        state={'card':2,'card_id':'Test','usb':m['usb'],'capture':{},'playback':{}}
        observer=AlsaObserver(m,lambda:state,lambda *_:(_ for _ in ()).throw(OSError('disconnected')))
        result=observer.observe(cfg)
        self.assertFalse(result.clock_locked)
        self.assertEqual(result.rate_hz,0)


if __name__=='__main__': unittest.main()
