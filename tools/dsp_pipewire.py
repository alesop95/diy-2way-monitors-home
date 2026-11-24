"""Funzioni del banco locale PipeWire, con link verificati prima del segnale."""
import json
import subprocess

CAPTURE = 'diy-monitor-lab-capture'
PLAYBACK = 'diy-monitor-lab-playback'
GENERATOR = 'diy-monitor-lab-generator'
RECORDER = 'diy-monitor-lab-recorder'


def validate_exit(role,code,version,size,expected,log):
    if role=='record' and size!=expected:
        raise RuntimeError(f'Cattura di lunghezza errata: {size}/{expected} byte')
    if code==0: return {'exit_code':0,'sample_limit_exit_1':False}
    # pw-cat 1.6.2 esce al limite campioni senza impostare data.drained.
    # src/tools/pw-cat.c, on_process e fine main: non mascherare altri errori.
    known=('Compiled with libpipewire 1.6.2\n' in version
           and 'Linked with libpipewire 1.6.2\n' in version)
    if role=='record' and code==1 and known and size==expected and not log:
        return {'exit_code':1,'sample_limit_exit_1':True,'reason':'pw-cat 1.6.2 sample limit without drained flag'}
    raise RuntimeError(f'pw-cat {role} termina con codice {code}, bytes {size}/{expected}, log {log!r}')


def dump_graph():
    result = subprocess.run(['pw-dump','-N'],capture_output=True,text=True,timeout=5,check=True)
    return json.loads(result.stdout)


def guard_links(graph, owned_nodes, allowed_ports, complete=False):
    actual=set()
    for obj in graph:
        if obj['type']!='PipeWire:Interface:Link': continue
        info=obj['info']
        if {info['output-node-id'],info['input-node-id']}&owned_nodes:
            pair=(info['output-port-id'],info['input-port-id'])
            if not {info['output-node-id'],info['input-node-id']} <= owned_nodes or pair not in allowed_ports:
                raise RuntimeError(f'Link estraneo al banco: {info}')
            actual.add(pair)
    if complete and actual!=allowed_ports:
        raise RuntimeError(f'Link mancanti: {allowed_ports-actual}')


def lab_objects(graph, names):
    nodes={}
    for name in names:
        matches=[obj for obj in graph if obj['type']=='PipeWire:Interface:Node' and obj['info']['props'].get('node.name')==name]
        if len(matches)!=1: raise RuntimeError(f'Atteso un solo nodo {name}, trovati {len(matches)}')
        nodes[name]=matches[0]
    return nodes


def ports_for(graph,node,direction,count):
    ports=[obj for obj in graph if obj['type']=='PipeWire:Interface:Port'
           and obj['info']['props'].get('node.id')==node['id']
           and obj['info']['props'].get('port.direction')==direction
           and not obj['info']['props'].get('port.monitor',False)]
    ports.sort(key=lambda obj:int(obj['info']['props']['port.id']))
    if len(ports)!=count or [int(obj['info']['props']['port.id']) for obj in ports]!=list(range(count)):
        raise RuntimeError(f'Porte inattese per {node["info"]["props"]["node.name"]}')
    return ports
