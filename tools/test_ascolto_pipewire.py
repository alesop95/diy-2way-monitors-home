"""Il grafo PC deve essere esatto, attestato e legato alla card osservata."""
import copy
import json
import unittest
from ascolto_alsa import AlsaObserver,digest
from ascolto_pipewire import LabObserver,PipeWirePolicy,PipeWireObserver,make_candidate
from test_ascolto_alsa import fixture,ROOT


def fixture_pw():
    _,m,raw=fixture()
    m['pcm']['verify_capture']=False
    m['pipewire']={'capture_node':'diy-in','playback_node':'diy-out','group':'diy-audio',
        'inputs':[['daw','out_L','input_0'],['daw','out_R','input_1']],
        'outputs':[[f'output_{i}','sink',f'playback_{i+4}'] for i in range(4)]}
    source=json.loads((ROOT/'config/camilladsp/offline-lr4.json').read_text(encoding='utf-8'))
    cfg=make_candidate(source,m)
    m['profiles_sha256']={'mix':digest(cfg)}
    proof=json.loads(raw)
    for key in ('pcm','pipewire','profiles_sha256'): proof[key]=m[key]
    raw=json.dumps(proof).encode(); m['proof_sha256']=digest(raw)
    graph=[]
    for ident,name in ((1,'diy-in'),(2,'diy-out'),(3,'daw'),(4,'sink')):
        props={'node.name':name}
        if ident==4: props['device.id']=5
        graph.append({'id':ident,'type':'PipeWire:Interface:Node','info':{'props':props}})
    graph.append({'id':5,'type':'PipeWire:Interface:Device','info':{'props':{'api.alsa.card':7}}})
    for ident,node,direction,name in [(10+i,1,'in',f'input_{i}') for i in range(2)]+[(20+i,2,'out',f'output_{i}') for i in range(4)]+[(30+i,3,'out',f'out_{c}') for i,c in enumerate(('L','R'))]+[(40+i,4,'in',f'playback_{i+4}') for i in range(4)]:
        graph.append({'id':ident,'type':'PipeWire:Interface:Port','info':{'props':{'node.id':node,'port.direction':direction,'port.name':name}}})
    for a,b,c,d in [(3,1,30,10),(3,1,31,11)]+[(2,4,20+i,40+i) for i in range(4)]:
        graph.append({'type':'PipeWire:Interface:Link','info':{'output-node-id':a,'input-node-id':b,'output-port-id':c,'input-port-id':d}})
    state={'card':7,'card_id':m['card_id'],'usb':m['usb'],
           'playback':{'format':'S32_LE','channels':20,'rate':48000}}
    alsa=AlsaObserver(m,lambda:state,lambda card,numid:{3:'1',4:'on',5:'1'}[numid])
    return cfg,m,raw,graph,alsa,state


class PipeWireQualification(unittest.TestCase):
    def test_qualified_pc_can_use_playback_without_claiming_capture_open(self):
        cfg,m,raw,graph,alsa,_=fixture_pw()
        policy=PipeWirePolicy(m,{'mix':cfg},raw)
        self.assertEqual(policy.validate(cfg),digest(cfg))
        self.assertTrue(PipeWireObserver(m,alsa,lambda:graph).observe(cfg).routing_verified)
        self.assertTrue(alsa.observe(cfg).clock_locked)

    def test_extra_missing_swapped_and_other_card_links_block_signal(self):
        cfg,m,_,graph,alsa,_=fixture_pw()
        variants=[]
        missing=copy.deepcopy(graph); missing.pop(); variants.append(missing)
        extra=copy.deepcopy(graph); edge=copy.deepcopy(extra[-1]); edge['info']['input-node-id']=999; extra.append(edge); variants.append(extra)
        swapped=copy.deepcopy(graph); swapped[-1]['info']['input-port-id']=40; variants.append(swapped)
        card=copy.deepcopy(graph); card[4]['info']['props']['api.alsa.card']=8; variants.append(card)
        duplicated=copy.deepcopy(graph); duplicated.append(copy.deepcopy(duplicated[0])); variants.append(duplicated)
        for bad in variants:
            with self.subTest(graph=bad[-1]):
                self.assertFalse(PipeWireObserver(m,alsa,lambda:bad).observe(cfg).routing_verified)

    def test_unrelated_headphone_links_are_untouched(self):
        cfg,m,_,graph,alsa,_=fixture_pw()
        graph.append({'type':'PipeWire:Interface:Link','info':{'output-node-id':91,'input-node-id':92,'output-port-id':93,'input-port-id':94}})
        self.assertTrue(PipeWireObserver(m,alsa,lambda:graph).observe(cfg).routing_verified)

    def test_another_application_cannot_bypass_dsp_into_a_reserved_driver_port(self):
        cfg,m,_,graph,alsa,_=fixture_pw()
        graph.extend([{'id':91,'type':'PipeWire:Interface:Node','info':{'props':{'node.name':'other-player'}}},
            {'id':93,'type':'PipeWire:Interface:Port','info':{'props':{'node.id':91,'port.direction':'out','port.name':'output_L'}}},
            {'id':44,'type':'PipeWire:Interface:Port','info':{'props':{'node.id':4,'port.direction':'in','port.name':'playback_2'}}}])
        graph.append({'type':'PipeWire:Interface:Link','info':{'output-node-id':91,'input-node-id':4,'output-port-id':93,'input-port-id':40}})
        observer=PipeWireObserver(m,alsa,lambda:graph)
        self.assertFalse(observer.observe(cfg).routing_verified)
        # La medesima applicazione sul cue cuffie, fuori dalle quattro vie,
        # non appartiene al percorso che il controller deve bloccare.
        graph[-1]['info']['input-port-id']=44
        self.assertTrue(observer.observe(cfg).routing_verified)

    def test_manifest_graph_change_even_with_new_profile_hash_needs_new_proof(self):
        cfg,m,raw,_,_,_=fixture_pw(); m['pipewire']['outputs'][0][2]='headphones'
        with self.assertRaises(ValueError): PipeWirePolicy(m,{'mix':cfg},raw)

    def test_binder_only_adds_missing_expected_links_and_rejects_foreign_links(self):
        cfg,m,_,graph,alsa,_=fixture_pw(); complete=copy.deepcopy(graph)
        graph.pop(); calls=[]
        def link(a,b):
            calls.append((a,b)); graph.append(copy.deepcopy(complete[-1]))
        observer=PipeWireObserver(m,alsa,lambda:graph,link=link)
        observer.bind(cfg)
        self.assertEqual(calls,[(23,43)])
        graph[-1]['info']['input-port-id']=40
        with self.assertRaises(RuntimeError): observer.bind(cfg)
        self.assertEqual(calls,[(23,43)])

    def test_binder_refuses_identity_loss_before_writing_any_link(self):
        cfg,m,_,graph,alsa,state=fixture_pw(); graph.pop(); state['usb']={}; calls=[]
        with self.assertRaises(RuntimeError): PipeWireObserver(m,alsa,lambda:graph,link=lambda *a:calls.append(a)).bind(cfg)
        self.assertEqual(calls,[])

    def test_lab_rejects_hardware_connection_even_when_engine_is_running(self):
        cfg=json.loads((ROOT/'config/controllo-ascolto/mix-pipewire.json').read_text(encoding='utf-8'))
        graph=[{'id':1,'type':'PipeWire:Interface:Node','info':{'props':{'node.name':'diy-monitor-lab-capture'}}},
               {'id':2,'type':'PipeWire:Interface:Node','info':{'props':{'node.name':'diy-monitor-lab-playback'}}},
               {'type':'PipeWire:Interface:Link','info':{'output-node-id':2,'input-node-id':99,'output-port-id':20,'input-port-id':90}}]
        self.assertFalse(LabObserver(lambda:graph).observe(cfg).routing_verified)

    def test_lab_exact_bench_is_valid_and_missing_link_is_not(self):
        cfg=json.loads((ROOT/'config/controllo-ascolto/mix-pipewire.json').read_text(encoding='utf-8'))
        names=['diy-monitor-lab-capture','diy-monitor-lab-playback','diy-monitor-lab-generator','diy-monitor-lab-recorder']
        graph=[{'id':i+1,'type':'PipeWire:Interface:Node','info':{'props':{'node.name':name}}} for i,name in enumerate(names)]
        for node,direction,count,base in ((1,'in',2,10),(2,'out',4,20),(3,'out',2,30),(4,'in',4,40)):
            for i in range(count):
                graph.append({'id':base+i,'type':'PipeWire:Interface:Port','info':{'props':{'node.id':node,'port.direction':direction,'port.id':i}}})
        for a,b,c,d in [(3,1,30,10),(3,1,31,11)]+[(2,4,20+i,40+i) for i in range(4)]:
            graph.append({'type':'PipeWire:Interface:Link','info':{'output-node-id':a,'input-node-id':b,'output-port-id':c,'input-port-id':d}})
        observer=LabObserver(lambda:graph)
        self.assertTrue(observer.observe(cfg).routing_verified)
        graph.pop(); self.assertFalse(observer.observe(cfg).routing_verified)


if __name__=='__main__': unittest.main()
