"""Collaudo 2 -> 4 senza hardware: pw-cat --target 0 e soli link espliciti.

Il servizio deve essere Inactive e silenziato. I file e le prove restano in una
cartella nuova; il motore ritorna in attesa anche quando una verifica fallisce.
"""
import argparse
import copy
import json
import math
from pathlib import Path
import struct
import subprocess
import tempfile
import time

import dsp_pipewire as pw
from monitor_dsp import RpcPeer, load_lab, read_status, stop_lab, wait_state, DEFAULT_PROFILE

RATE=48000
DURATION=6
AMPLITUDE=0.035
FREQUENCIES=((100,2000,8000),(200,2500,9000))


class RoutingMismatch(AssertionError):
    """Segnale presente sul lato estraneo; distingue routing da cattura guasta."""


def generate_signal(path):
    raw=bytearray()
    for i in range(RATE*DURATION):
        frame=[round(32767*AMPLITUDE*sum(math.sin(2*math.pi*f*i/RATE) for f in freqs)) for freqs in FREQUENCIES]
        raw.extend(struct.pack('<hh',*frame))
    path.write_bytes(raw)


def level(values,frequency):
    omega=2*math.pi*frequency/RATE
    real=sum(v*math.cos(omega*i) for i,v in enumerate(values))
    imag=sum(v*math.sin(omega*i) for i,v in enumerate(values))
    return 2*math.hypot(real,imag)/len(values)


def db(value):
    return 20*math.log10(max(value,1e-15))


def measure(frames,gain,mute):
    if len(frames)!=RATE*DURATION: raise AssertionError(f'Cattura di lunghezza errata: {len(frames)} frame')
    if not all(math.isfinite(x) for frame in frames for x in frame): raise AssertionError('PCM non finito')
    peak=max(abs(x) for frame in frames for x in frame)
    if mute:
        # Il fader Main ha una rampa predefinita di 400 ms. Il banco parte
        # a -60 dB: si misura e si limita il transitorio, poi lo zero a regime.
        startup=max(abs(x) for frame in frames[:RATE] for x in frame)
        steady=max(abs(x) for frame in frames[RATE:] for x in frame)
        bound=3*AMPLITUDE*10**(-60/20)*10**(1/20)
        if startup>bound: raise AssertionError(f'Mute: transitorio oltre il limite iniziale -60 dB: {startup}')
        if steady>1e-8: raise AssertionError(f'Mute a regime non nullo: {steady}')
        return {'frames':len(frames),'mute_peak_startup':startup,
                'mute_startup_bound':bound,'mute_peak_steady':steady,'steady_from_frame':RATE}
    start=len(frames)//2-RATE//2
    window=frames[start:start+RATE]
    measurements=[]
    for side,freqs in enumerate(FREQUENCIES):
        lo,hi=2*side,2*side+1
        other=2*(1-side)
        for freq in freqs:
            levels=[level([frame[c] for frame in window],freq)/AMPLITUDE for c in range(4)]
            summed=level([frame[lo]+frame[hi] for frame in window],freq)/AMPLITUDE
            if max(db(levels[other]),db(levels[other+1]))>-65+gain:
                raise RoutingMismatch(f'Segnale sul lato estraneo: lato {side}, {freq} Hz, livelli {levels}')
            if abs(db(summed)-gain)>0.2: raise AssertionError(f'Somma/volume: lato {side}, {freq} Hz, {db(summed):.3f} dB, attesi {gain}')
            if freq==2000:
                if max(abs(db(levels[c])-gain+6.0206) for c in (lo,hi))>0.2: raise AssertionError('Incrocio diverso da -6.0206 dB')
            elif freq<500:
                if db(levels[hi])-gain>-40: raise AssertionError('Bassi nella via alta')
            elif freq>=8000:
                if db(levels[lo])-gain>-40: raise AssertionError('Alti nella via bassa')
            measurements.append({'side':side,'frequency_hz':freq,'levels_db':[round(db(v),5) for v in levels],'sum_db':round(db(summed),5)})
    return {'frames':len(frames),'gain_db':gain,'peak':peak,'measurements':measurements}


def run_case(peer,config,folder,input_path,gain=0,mute=False):
    status=read_status(peer)
    if status['state']!='Inactive' or status['mute'] is not True:
        raise RuntimeError('Il servizio deve essere inattivo e silenziato prima del banco')
    folder.mkdir()
    processes=[]
    logs=[]
    result=None
    error=None
    owns_pipeline=False
    try:
        version=subprocess.run(['pw-cat','--version'],capture_output=True,text=True,check=True,timeout=3).stdout
        (folder/'pw-cat-version.txt').write_text(version)
        owns_pipeline=True
        load_lab(peer,config)
        graph=pw.dump_graph()
        nodes=pw.lab_objects(graph,[pw.CAPTURE,pw.PLAYBACK])
        pw.guard_links(graph,{x['id'] for x in nodes.values()},set(),complete=True)
        for name,mode,channels,fmt,chmap,filename in (
            (pw.RECORDER,'--record',4,'f32','AUX0,AUX1,AUX2,AUX3',str(folder/'output.pcm')),
            (pw.GENERATOR,'--playback',2,'s16','FL,FR',str(input_path)),
        ):
            props=f'node.name={name} node.group=diy-monitor-lab node.autoconnect=false node.dont-reconnect=true'
            command=['pw-cat',mode,'--raw','--target','0','--rate',str(RATE),'--channels',str(channels),
                     '--format',fmt,'--channel-map',chmap,'--latency','1024','--properties',props]
            if mode=='--record': command+=['--sample-count',str(RATE*DURATION)]
            command.append(filename)
            log=(folder/(name+'.log')).open('xb'); logs.append(log)
            process=subprocess.Popen(command,stdout=log,stderr=log)
            processes.append((name,process))
        deadline=time.monotonic()+5
        while True:
            graph=pw.dump_graph()
            try:
                nodes=pw.lab_objects(graph,[pw.CAPTURE,pw.PLAYBACK,pw.GENERATOR,pw.RECORDER])
                cap=pw.ports_for(graph,nodes[pw.CAPTURE],'in',2)
                play=pw.ports_for(graph,nodes[pw.PLAYBACK],'out',4)
                gen=pw.ports_for(graph,nodes[pw.GENERATOR],'out',2)
                rec=pw.ports_for(graph,nodes[pw.RECORDER],'in',4)
                break
            except RuntimeError:
                if time.monotonic()>=deadline: raise
                time.sleep(0.1)
        clients={x['id']:x['info']['props'] for x in graph if x['type']=='PipeWire:Interface:Client'}
        for name,process in processes:
            props=nodes[name]['info']['props']
            owner=clients[int(props['client.id'])]
            if int(owner.get('pipewire.sec.pid',-1))!=process.pid:
                raise RuntimeError('Il nodo non appartiene al client appena creato')
        owned={obj['id'] for obj in nodes.values()}
        pairs=[(out['id'],inp['id']) for out,inp in list(zip(play,rec))+list(zip(gen,cap))]
        allowed=set(pairs)
        pw.guard_links(graph,owned,allowed,complete=False)
        for out,inp in pairs:
            pw.guard_links(pw.dump_graph(),owned,allowed,complete=False)
            subprocess.run(['pw-link',str(out),str(inp)],capture_output=True,text=True,check=True,timeout=4)
        graph=pw.dump_graph()
        pw.guard_links(graph,owned,allowed,complete=True)
        (folder/'graph-connected.json').write_text(json.dumps(graph,indent=2))
        peer.call({'SetVolume':gain})
        peer.call({'SetMute':mute})
        wait_state(peer,{'Running'},timeout=5)
        (folder/'status-running.json').write_text(json.dumps(read_status(peer),indent=2))
        exits={}
        for name,process in processes:
            code=process.wait(timeout=DURATION+6)
            role='record' if name==pw.RECORDER else 'play'
            size=(folder/'output.pcm').stat().st_size
            log=(folder/(name+'.log')).read_bytes()
            exit_info=pw.validate_exit(role,code,version,size,RATE*DURATION*16,log)
            exits[name]=dict(exit_info,pid=process.pid)
            (folder/f'process-{process.pid}-exit.json').write_text(json.dumps(exits[name]))
        raw=(folder/'output.pcm').read_bytes()
        if len(raw)%16: raise AssertionError('Cattura non allineata su quattro float32')
        frames=list(struct.iter_unpack('<ffff',raw))
        result=measure(frames,gain,mute)
        result['process_exits']=exits
    except BaseException as exc:
        error=exc
    finally:
        cleanup_errors=[]
        try:
            if owns_pipeline: peer.call({'SetMute':True})
        except Exception as exc: cleanup_errors.append(str(exc))
        for _,process in processes:
            if process.poll() is None:
                process.terminate()
                try: process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    process.kill(); process.wait(timeout=2)
        for log in logs: log.close()
        try:
            if owns_pipeline:
                stopped=stop_lab(peer)
                (folder/'status-final.json').write_text(json.dumps(stopped,indent=2))
        except Exception as exc: cleanup_errors.append(str(exc))
        if cleanup_errors:
            (folder/'cleanup-errors.json').write_text(json.dumps(cleanup_errors,indent=2))
            error=RuntimeError(f'{error or "Errore di ripristino"}; cleanup: {cleanup_errors}')
    if error:
        (folder/'failure.json').write_text(json.dumps({'error':str(error),'type':type(error).__name__},indent=2))
        raise error
    (folder/'measurement.json').write_text(json.dumps(result,indent=2))
    return result


def detect_swapped_channels(peer,config,folder,input_path):
    mutated=copy.deepcopy(config)
    for mapping in mutated['mixers']['stereo_quattro_vie']['mapping']:
        mapping['sources'][0]['channel']=1-mapping['sources'][0]['channel']
    try: run_case(peer,mutated,folder,input_path)
    except RoutingMismatch as exc: return {'mutation_detected':str(exc)}
    raise AssertionError('Prova vacua: scambio dei lati non rilevato')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile',type=Path,default=DEFAULT_PROFILE)
    parser.add_argument('--dest',type=Path,required=True)
    parser.add_argument('--mutazioni',action='store_true')
    parser.add_argument('--solo-normale',action='store_true')
    args=parser.parse_args()
    args.dest.mkdir(parents=True,exist_ok=True)
    folder=Path(tempfile.mkdtemp(prefix='pipewire-',dir=args.dest)).resolve()
    config=json.loads(args.profile.read_text())
    generate_signal(folder/'input.pcm')
    report={'folder':str(folder),'passed':False,'cases':{}}
    from websockets.sync.client import connect
    try:
        with connect('ws://127.0.0.1:12341',proxy=None,open_timeout=3,close_timeout=2) as connection:
            peer=RpcPeer(connection)
            cases=[('normale',0,False)] if args.solo_normale else [('normale',0,False),('volume',-6,False),('mute',0,True)]
            for name,gain,mute in cases:
                report['cases'][name]=run_case(peer,config,folder/name,folder/'input.pcm',gain,mute)
            if args.mutazioni:
                report['cases']['lati-scambiati']=detect_swapped_channels(peer,config,folder/'lati-scambiati',folder/'input.pcm')
            report['passed']=True
    except BaseException as exc:
        report['error']=str(exc)
        raise
    finally:
        (folder/'esito.json').write_text(json.dumps(report,indent=2))
        print(folder/'esito.json',flush=True)


if __name__=='__main__': main()
