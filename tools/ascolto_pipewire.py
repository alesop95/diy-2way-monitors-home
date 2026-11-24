"""Grafo osservato del laboratorio e collegamenti PC esplicitamente qualificati."""
import copy
import argparse
import json
from pathlib import Path
import subprocess
import time
from ascolto_alsa import AlsaPolicy,digest
from controllo_ascolto import Observation,validate_profile
from dsp_pipewire import CAPTURE,PLAYBACK,GENERATOR,RECORDER,dump_graph,guard_links,lab_objects,ports_for


def make_candidate(profile,manifest):
    """Solo dati: quattro porte logiche, destinazioni fisiche nel grafo attestato."""
    validate_profile(profile)
    cfg=copy.deepcopy(profile); pw=manifest['pipewire']
    cfg['title']='DIY-2WAY '+profile['title']
    cfg['devices'].update(stop_on_rate_change=True,enable_rate_adjust=False,volume_limit=-6,resampler=None)
    for direction,channels,node in (('capture',2,'capture_node'),('playback',4,'playback_node')):
        cfg['devices'][direction]={'type':'PipeWire','channels':channels,'node_name':pw[node],
            'node_group_name':pw['group'],'autoconnect_to':None}
    return cfg


class PipeWirePolicy(AlsaPolicy):
    def validate(self,cfg):
        if digest(cfg) not in self.allowed or not cfg.get('title','').startswith(self.owner_prefix):
            raise ValueError('Profilo PipeWire non attestato')
        d=cfg['devices']; pw=self.manifest['pipewire']
        if (d['samplerate'] not in (44100,48000) or d.get('resampler') is not None
                or d.get('enable_rate_adjust') not in (None,False)
                or d.get('stop_on_rate_change') is not True or d.get('volume_limit')!=-6):
            raise ValueError('Clock o volume PipeWire non conforme')
        for direction,channels,node in (('capture',2,'capture_node'),('playback',4,'playback_node')):
            expected={'type':'PipeWire','channels':channels,'node_name':pw[node],
                      'node_group_name':pw['group'],'autoconnect_to':None}
            if any(d[direction].get(k)!=v for k,v in expected.items()): raise ValueError('Nodo PipeWire diverso')
        names=[pw['capture_node'],pw['playback_node']]
        if len(set(names))!=2 or any(not isinstance(n,str) or not n or ':' in n for n in names):
            raise ValueError('Nomi dei nodi non validi')
        if (len(pw['inputs'])!=2 or len(pw['outputs'])!=4
                or len({row[2] for row in pw['inputs']})!=2 or len({row[0] for row in pw['outputs']})!=4):
            raise ValueError('Porte delle quattro vie non valide')
        for row in pw['inputs']+pw['outputs']:
            if len(row)!=3 or any(not isinstance(s,str) or not s for s in row): raise ValueError('Porta non attestata')
        if any(row[0] in names for row in pw['inputs']) or any(row[1] in names for row in pw['outputs']):
            raise ValueError('Feedback fra nodi DSP non ammesso')
        return digest(cfg)


class LabObserver:
    def __init__(self,graph=dump_graph): self.graph=graph

    def observe(self,cfg):
        try:
            graph=self.graph(); nodes=lab_objects(graph,(CAPTURE,PLAYBACK,GENERATOR,RECORDER))
            capture=ports_for(graph,nodes[CAPTURE],'in',2)
            playback=ports_for(graph,nodes[PLAYBACK],'out',4)
            gen=ports_for(graph,nodes[GENERATOR],'out',2)
            rec=ports_for(graph,nodes[RECORDER],'in',4)
            pairs={(a['id'],b['id']) for a,b in zip(gen,capture)}|{(a['id'],b['id']) for a,b in zip(playback,rec)}
            guard_links(graph,{n['id'] for n in nodes.values()},pairs,complete=True)
            return Observation(cfg['devices']['samplerate'],True,True,True)
        except (ValueError,KeyError,RuntimeError,OSError,subprocess.SubprocessError):
            return Observation(0,False,False,False)


def link_ports(output,input_):
    subprocess.run(['pw-link',str(output),str(input_)],check=True,capture_output=True,timeout=1)


class PipeWireObserver:
    def __init__(self,manifest,alsa,graph=dump_graph,link=link_ports):
        self.manifest=manifest; self.alsa=alsa; self.graph=graph; self.link=link

    def identity(self): return self.alsa.identity()

    def resolve(self,graph):
        pw=self.manifest['pipewire']; managed=(pw['capture_node'],pw['playback_node'])
        names=set(managed)|{r[0] for r in pw['inputs']}|{r[1] for r in pw['outputs']}
        nodes=lab_objects(graph,names); owners={}
        def port(node,name,direction):
            matches=[p for p in graph if p['type']=='PipeWire:Interface:Port'
                     and str(p['info']['props'].get('node.id'))==str(nodes[node]['id'])
                     and p['info']['props'].get('port.name')==name
                     and p['info']['props'].get('port.direction')==direction]
            if len(matches)!=1: raise RuntimeError('Porta assente o ambigua: '+node+':'+name)
            owners[matches[0]['id']]=nodes[node]['id']
            return matches[0]['id']
        expected={(port(n,p,'out'),port(managed[0],d,'in')) for n,p,d in pw['inputs']}
        expected|={(port(managed[1],p,'out'),port(n,d,'in')) for p,n,d in pw['outputs']}
        if len(expected)!=6: raise RuntimeError('Collegamenti non univoci')
        snapshot=self.alsa.snapshot()
        for sink in {r[1] for r in pw['outputs']}:
            props=nodes[sink]['info']['props']; card=props.get('api.alsa.pcm.card')
            if card is None:
                devices=[o for o in graph if o['type']=='PipeWire:Interface:Device' and str(o['id'])==str(props.get('device.id'))]
                if len(devices)==1: card=devices[0]['info']['props'].get('api.alsa.card')
            if card is None or str(card)!=str(snapshot.get('card')): raise RuntimeError('Sink non legato alla card qualificata')
        owned={nodes[n]['id'] for n in managed}; actual=set()
        destinations={target for _,target in expected}
        for o in graph:
            if o['type']!='PipeWire:Interface:Link': continue
            info=o['info']
            if {info['output-node-id'],info['input-node-id']}&owned or info['input-port-id'] in destinations:
                pair=(info['output-port-id'],info['input-port-id'])
                if pair not in expected: raise RuntimeError('Collegamento DSP estraneo alla qualifica')
                if (owners[pair[0]],owners[pair[1]])!=(info['output-node-id'],info['input-node-id']):
                    raise RuntimeError('Estremi del collegamento incoerenti')
                actual.add(pair)
        return expected,actual

    def observe(self,cfg):
        try:
            base=self.alsa.observe(cfg); expected,actual=self.resolve(self.graph())
            return Observation(base.rate_hz,base.clock_locked,base.routing_verified and expected==actual,base.identity_matches)
        except (ValueError,KeyError,RuntimeError,OSError,subprocess.SubprocessError):
            return Observation(0,False,False,False)

    def bind(self,cfg):
        # Invocato solo dopo prepare: motore mutato a -60 dB. Nessun unlink.
        deadline=time.monotonic()+3
        while True:
            if not self.identity(): raise RuntimeError('Identità persa prima dei collegamenti')
            try: expected,actual=self.resolve(self.graph()); break
            except RuntimeError as error:
                # Si attende solo la creazione dei nodi; un grafo presente ma
                # sbagliato non viene riparato eliminando collegamenti altrui.
                if not str(error).startswith('Atteso un solo nodo') or time.monotonic()>=deadline: raise
                time.sleep(.05)
        for a,b in sorted(expected-actual):
            if not self.identity(): raise RuntimeError('Identità persa durante i collegamenti')
            self.link(a,b)
        expected,actual=self.resolve(self.graph())
        if expected!=actual: raise RuntimeError('Collegamenti non confermati')


def main():
    parser=argparse.ArgumentParser(description='Normalizza un candidato PC senza caricarlo o attestarlo.')
    parser.add_argument('profile',type=Path); parser.add_argument('manifest',type=Path)
    parser.add_argument('--out',type=Path,required=True); parser.add_argument('--port',type=int,default=12341)
    args=parser.parse_args()
    from pannello_ascolto import WebSocketPeer
    peer=WebSocketPeer(args.port)
    if peer.call('GetVersion')!='4.1.3': raise ValueError('Versione DSP diversa')
    candidate=make_candidate(json.loads(args.profile.read_text(encoding='utf-8')),
                             json.loads(args.manifest.read_text(encoding='utf-8')))
    canonical=json.loads(peer.call({'ReadConfigJson':json.dumps(candidate,allow_nan=False)}))
    with args.out.open('x',encoding='utf-8') as output: output.write(json.dumps(canonical,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'candidate':str(args.out),'sha256':digest(canonical),'qualified':False,'hardware_opened':False}))


if __name__=='__main__': main()
