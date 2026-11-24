"""Prova il controllo sul motore reale in istanza separata, soltanto FIFO/file.

Da Windows usare --ssh con un alias autorizzato. Il bundle temporaneo è rimosso.
"""
import argparse
from array import array
import base64
from datetime import datetime,timezone
import hashlib
import json
import math
import os
import platform
from pathlib import Path
import socket
import select
import struct
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
SOURCES=('tools/collauda-controllo-ascolto.py','tools/controllo_ascolto.py','tools/monitor_dsp.py',
         'tools/pannello_ascolto.py','tools/ascolto_alsa.py','tools/ascolto_pipewire.py','tools/dsp_pipewire.py',
         'config/controllo-ascolto/index.html',
         'config/controllo-ascolto/mix-file.json','config/controllo-ascolto/ascolto-file.json',
         'build/consegna-cabinet-20261119/assets/Altro-Grotesk-Book.ttf',
         'build/consegna-cabinet-20261119/assets/Altro-Serif-Light.ttf')


def valid_report(report,hashes):
    try:
        if (report['source_sha256']!=hashes or report['passed'] is not True or report['hardware_test'] is not False
                or report['main_service_state_unchanged'] is not True or report['temporary_files_retained'] is not False
                or len(report['cases'])!=2 or {c['rate_hz'] for c in report['cases']}!={44100,48000}): return False
        for case in report['cases']:
            for key in ('http_actions_verified','alsa_candidate_canonical_checked_without_loading',
                        'pipewire_candidate_canonical_checked_without_loading',
                        'cli_sigterm_mute_verified','automatic_restore_rejected'):
                if case[key] is not True: return False
            for key in ('rms_initial_mute_max','rms_after_injected_clock_loss_max','rms_manual_mute_max','rms_after_cli_shutdown_max'):
                if not math.isfinite(case[key]) or not 0<=case[key]<1e-8: return False
            if len(case['volume_step_measured_db'])!=4 or any(not math.isfinite(v) or abs(v-6)>=.1 for v in case['volume_step_measured_db']): return False
            if len(case['rms_minus24_per_channel'])!=4 or any(not math.isfinite(v) or v<=1e-6 for v in case['rms_minus24_per_channel']): return False
            if not .2<case['listening_profile_change_100hz_db']<2.1: return False
            if not math.isfinite(case['output_peak']) or not 0<case['output_peak']<1: return False
        if report['main_service_snapshot_before'] is None or report['main_service_snapshot_before']!=report['main_service_snapshot_after']: return False
        if report['linux_pipewire_read_only_probe']['read_only'] is not True: return False
        return True
    except (KeyError,TypeError,ValueError): return False


def worker(binary):
    from websockets.sync.client import connect
    from monitor_dsp import RpcPeer
    from controllo_ascolto import Controller,Observation
    from pannello_ascolto import Session,WebSocketPeer,make_server
    from ascolto_alsa import make_candidate,AlsaPolicy,digest,parse_hw_params
    from ascolto_pipewire import make_candidate as make_pw_candidate,PipeWirePolicy
    from dsp_pipewire import dump_graph
    if os.name!='posix': raise RuntimeError('Il banco FIFO richiede Linux; da Windows usare --ssh')
    if '4.1.3' not in subprocess.run([str(binary),'--version'],capture_output=True,text=True,check=True).stdout:
        raise ValueError('Motore diverso da 4.1.3')
    def main_status():
        try:
            with connect('ws://127.0.0.1:12341',proxy=None,open_timeout=.5,close_timeout=.5) as c:
                p=RpcPeer(c)
                return {k:p.call(k) for k in ('GetVersion','GetState','GetMute','GetVolume')}
        except (OSError,TimeoutError): return None
    before=main_status(); cases=[]
    if before is None: raise RuntimeError('Impossibile rileggere il servizio principale prima della prova')
    graph=dump_graph()
    pw_probe={'nodes_read':sum(o['type']=='PipeWire:Interface:Node' for o in graph),
              'links_read':sum(o['type']=='PipeWire:Interface:Link' for o in graph),'read_only':True}
    proc_files=list(Path('/proc/asound').glob('card*/pcm*/sub*/hw_params'))
    parsed=[parse_hw_params(p.read_text()) for p in proc_files]
    proc_probe={'files_read':len(parsed),'active_streams_parsed':sum(bool(p) for p in parsed),'read_only':True}
    for rate in (44100,48000):
        cfg=json.loads((ROOT/'config/controllo-ascolto/mix-file.json').read_text())
        cfg['devices']['samplerate']=rate
        cfg['devices']['volume_limit']=-6
        listening=json.loads((ROOT/'config/controllo-ascolto/ascolto-file.json').read_text())
        listening['devices']['samplerate']=rate; listening['devices']['volume_limit']=-6
        with tempfile.TemporaryDirectory(prefix='diy-control-') as tmp:
            folder=Path(tmp); os.mkfifo(folder/'input.pcm')
            keeper=os.open(folder/'input.pcm',os.O_RDWR|os.O_NONBLOCK)
            with socket.socket() as reserve:
                reserve.bind(('127.0.0.1',0)); port=reserve.getsockname()[1]
            stop=threading.Event(); sent=[0]; failures=[]
            def feed():
                try:
                    while not stop.is_set():
                        try: fd=os.open(folder/'input.pcm',os.O_WRONLY|os.O_NONBLOCK); break
                        except OSError: time.sleep(.01)
                    else: return
                    os.set_blocking(fd,True)
                    with os.fdopen(fd,'wb',buffering=0) as stream:
                        block=rate//100; deadline=time.monotonic()
                        while not stop.is_set():
                            start=sent[0]
                            data=b''.join(struct.pack('<hh',round(3200*math.sin(2*math.pi*100*n/rate)+800*math.sin(2*math.pi*7000*n/rate)),
                                                     round(800*math.sin(2*math.pi*500*n/rate)+1600*math.sin(2*math.pi*7000*n/rate))) for n in range(start,start+block))
                            stream.write(data); sent[0]+=block
                            deadline+=block/rate; stop.wait(max(0,deadline-time.monotonic()))
                except (BrokenPipeError,OSError) as error:
                    if not stop.is_set(): failures.append(type(error).__name__)
            thread=threading.Thread(target=feed,daemon=True); thread.start()
            with (folder/'engine.log').open('wb') as log:
                process=subprocess.Popen([str(binary),'-w','-m','-g=-60','-a','127.0.0.1','-p',str(port)],
                                         cwd=folder,stdout=log,stderr=subprocess.STDOUT)
                connection=None
                http=None; watcher_stop=threading.Event(); http_thread=None; watcher=None; cli=None
                try:
                    deadline=time.monotonic()+4
                    while connection is None:
                        try: connection=connect(f'ws://127.0.0.1:{port}',proxy=None,open_timeout=.2,close_timeout=.5)
                        except OSError:
                            if time.monotonic()>deadline: raise TimeoutError('Istanza di test non disponibile')
                            time.sleep(.03)
                    peer=WebSocketPeer(port)
                    # ReadConfigJson esegue soltanto parsing/serializzazione.
                    # Il candidato ALSA sintetico non viene mai caricato.
                    m={'schema':'ascolto-alsa-1','verified':True,'card_id':'Test',
                       'usb':{'vendor':'1234','product':'5678','serial_sha256':'a'*64},
                       'pcm':{'capture_device':0,'playback_device':0,'capture_channels':18,'playback_channels':20,'format':'S32_LE'},
                       'routing':{'sources':[8,9],'outputs':[4,5,6,7]},
                       'clock':{'mode':'external','source_numid':3,'source_expected':'1','lock_numid':4,'lock_expected':'on',
                                'rate_numid':5,'rate_values_hz':{'0':44100,'1':48000}}}
                    candidate=make_candidate(cfg,m)
                    canonical_alsa=json.loads(peer.call({'ReadConfigJson':json.dumps(candidate)}))
                    m['profiles_sha256']={'mix':digest(canonical_alsa)}
                    proof=dict(m,schema='qualifica-ascolto-1',physical_routing_verified=True,volume_path_verified=True)
                    raw=json.dumps(proof).encode(); m['proof_sha256']=digest(raw)
                    try: AlsaPolicy(m,{'mix':canonical_alsa},raw)
                    except ValueError:
                        print(json.dumps(canonical_alsa['mixers']['uscite_fisiche']),file=sys.stderr)
                        raise
                    # Anche il candidato PC passa dal parser reale, senza
                    # SetConfigJson: nessun nodo o link hardware è creato.
                    m['pcm']['verify_capture']=False
                    m['pipewire']={'capture_node':'diy-in','playback_node':'diy-out','group':'diy-audio',
                        'inputs':[['daw','out_L','input_0'],['daw','out_R','input_1']],
                        'outputs':[[f'output_{i}','sink',f'playback_{i+4}'] for i in range(4)]}
                    canonical_pw=json.loads(peer.call({'ReadConfigJson':json.dumps(make_pw_candidate(cfg,m))}))
                    m['profiles_sha256']={'mix':digest(canonical_pw)}
                    proof=dict(m,schema='qualifica-ascolto-1',physical_routing_verified=True,volume_path_verified=True)
                    raw=json.dumps(proof).encode(); m['proof_sha256']=digest(raw)
                    PipeWirePolicy(m,{'mix':canonical_pw},raw)
                    good=[True]
                    session=Session(peer,{'mix':cfg,'ascolto':listening},
                        observer=lambda profile:Observation(rate,good[0],True,True))
                    http=make_server(session,port=0)
                    http_thread=threading.Thread(target=http.serve_forever,daemon=True); http_thread.start()
                    watcher=threading.Thread(target=session.supervise,args=(watcher_stop,),daemon=True); watcher.start()
                    url=f'http://127.0.0.1:{http.server_address[1]}'
                    def action(name,body):
                        request=urllib.request.Request(url+'/api/'+name,data=json.dumps(body).encode(),
                            headers={'Content-Type':'application/json','X-Session-Token':http.token},method='POST')
                        with urllib.request.urlopen(request,timeout=4) as response: return json.load(response)
                    with urllib.request.urlopen(url,timeout=2) as response:
                        page=response.read()
                        assert http.token.encode() in page and b'__TOKEN__' not in page
                    action('prepare',{'profile':'mix'}); controller=session.controller
                    deadline=time.monotonic()+3
                    while peer.call('GetState')!='Running':
                        if time.monotonic()>deadline: raise TimeoutError('Nessun audio Running')
                        time.sleep(.02)
                    normalized=controller.profile
                    windows={}
                    def window(name):
                        # Il contatore del produttore FIFO precede il segnale
                        # effettivamente scritto dal DSP. Le finestre devono
                        # appartenere al file di uscita, non all'orologio host.
                        output=folder/'output.pcm'
                        start=output.stat().st_size//16; deadline=time.monotonic()+4
                        while output.stat().st_size//16<start+round(.95*rate):
                            if time.monotonic()>deadline: raise TimeoutError('Uscita PCM non avanza')
                            time.sleep(.01)
                        windows[name]=(start+round(.6*rate),start+round(.85*rate))
                    window('initial_mute')
                    action('enable',{'volume':-24}); window('minus24')
                    action('volume',{'volume':-18}); window('minus18')
                    action('mute',{}); window('manual_mute')
                    action('prepare',{'profile':'ascolto'})
                    assert peer.call('GetMute') is True
                    action('enable',{'volume':-24}); window('listening_profile')
                    fault_at=time.monotonic(); good[0]=False
                    deadline=fault_at+2
                    while session.status()['ready']:
                        if time.monotonic()>deadline: raise AssertionError('Sorveglianza non intervenuta')
                        time.sleep(.01)
                    watchdog_delay=time.monotonic()-fault_at
                    window('lost_clock')
                    assert peer.call('GetMute') is True and peer.call('GetVolume')==-60
                    good[0]=True; time.sleep(.3)
                    assert not session.status()['ready'] and peer.call('GetMute') is True
                    try: action('enable',{'volume':-24})
                    except urllib.error.HTTPError as error: assert error.code==409
                    else: raise AssertionError('Ripristino senza nuova preparazione')
                    watcher_stop.set(); watcher.join(timeout=3)
                    http.shutdown(); http.server_close(); http_thread.join(timeout=2); http=None
                    for name,data in (('mix',cfg),('ascolto',listening)):
                        (folder/(name+'.json')).write_text(json.dumps(data))
                    panel={'mode':'file','dsp_port':port,'profiles':{'mix':'mix.json','ascolto':'ascolto.json'}}
                    (folder/'panel.json').write_text(json.dumps(panel))
                    cli=subprocess.Popen([sys.executable,str(ROOT/'tools/pannello_ascolto.py'),'--config',str(folder/'panel.json'),'--port','0'],
                                         cwd=folder,stdout=subprocess.PIPE,stderr=log,text=True)
                    if not select.select([cli.stdout],[],[],4)[0]: raise TimeoutError('CLI del pannello non pronta')
                    address=cli.stdout.readline().strip().split('Pannello: ',1)[-1]
                    with urllib.request.urlopen(address,timeout=2) as response:
                        import re
                        cli_token=re.search(r'name="session-token" content="([^"]+)"',response.read().decode()).group(1)
                    def cli_action(name,body):
                        req=urllib.request.Request(address+'/api/'+name,data=json.dumps(body).encode(),
                            headers={'Content-Type':'application/json','X-Session-Token':cli_token},method='POST')
                        with urllib.request.urlopen(req,timeout=4) as response: return json.load(response)
                    cli_action('prepare',{'profile':'mix'}); cli_action('enable',{'volume':-24})
                    time.sleep(.6); cli.terminate(); assert cli.wait(timeout=8)==0
                    assert peer.call('GetMute') is True and peer.call('GetVolume')==-60
                    window('cli_shutdown')
                    stop.set()
                    peer.call('Stop')
                    time.sleep(.1)
                except Exception:
                    print(json.dumps({'fifo_writer_errors':failures,'frames_sent':sent[0]}),file=sys.stderr)
                    print((folder/'engine.log').read_text(errors='replace')[-5000:],file=sys.stderr)
                    raise
                finally:
                    stop.set()
                    watcher_stop.set()
                    if watcher is not None: watcher.join(timeout=3)
                    if cli is not None and cli.poll() is None: cli.terminate(); cli.wait(timeout=8)
                    if http is not None: http.shutdown(); http.server_close()
                    if http_thread is not None: http_thread.join(timeout=2)
                    if connection is not None: connection.close()
                    if process.poll() is None: process.terminate()
                    process.wait(timeout=4); os.close(keeper); thread.join(timeout=1)
                if failures: raise AssertionError(failures)
            values=array('f'); values.frombytes((folder/'output.pcm').read_bytes())
            if sys.byteorder!='little': values.byteswap()
            assert len(values)%4==0 and all(math.isfinite(x) for x in values)
            peak=max(abs(x) for x in values)
            assert peak<1,('Picco fuori scala',peak)
            assert len(values)//4>=max(b for a,b in windows.values())
            def rms(name,channel):
                a,b=windows[name]
                return math.sqrt(sum(values[n*4+channel]**2 for n in range(a,b))/(b-a))
            initial=max(rms('initial_mute',c) for c in range(4))
            lost=max(rms('lost_clock',c) for c in range(4))
            manual=max(rms('manual_mute',c) for c in range(4))
            shutdown=max(rms('cli_shutdown',c) for c in range(4))
            levels=[rms('minus24',c) for c in range(4)]
            assert min(levels)>1e-6,('Stimolo insufficiente in una banda',levels)
            differences=[20*math.log10(rms('minus18',c)/levels[c]) for c in range(4)]
            shelf_change=20*math.log10(rms('listening_profile',0)/rms('minus24',0))
            assert initial<1e-8 and lost<1e-8 and manual<1e-8 and shutdown<1e-8,(initial,lost,manual,shutdown)
            assert all(abs(x-6)<.1 for x in differences),(differences,levels)
            assert .2<shelf_change<2.1,shelf_change
            cases.append({'rate_hz':rate,'rms_initial_mute_max':initial,'rms_after_injected_clock_loss_max':lost,
                          'rms_manual_mute_max':manual,'listening_profile_change_100hz_db':shelf_change,
                          'rms_minus24_per_channel':levels,
                          'http_actions_verified':True,'watchdog_reaction_seconds':watchdog_delay,
                          'alsa_candidate_canonical_checked_without_loading':True,
                          'pipewire_candidate_canonical_checked_without_loading':True,
                          'cli_sigterm_mute_verified':True,'rms_after_cli_shutdown_max':shutdown,
                          'volume_step_measured_db':differences,'expected_step_db':6,
                          'measurement_windows':'Output PCM frame positions; 600-850 ms after action',
                          'normalized_config_has_defaults':normalized!=cfg,'pcm_frames':len(values)//4,'output_peak':peak,
                          'automatic_restore_rejected':True})
    after=main_status()
    assert after==before,'Stato del servizio principale cambiato'
    return {'passed':True,'hardware_test':False,'transport':'websockets 15.0.1',
            'tested_at_utc':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),'kernel':platform.release(),
            'binary_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'cases':cases,
            'linux_procfs_read_only_probe':proc_probe,
            'linux_pipewire_read_only_probe':pw_probe,
            'main_service_state_unchanged':True,'temporary_files_retained':False,
            'main_service_snapshot_before':before,'main_service_snapshot_after':after,
            'limits':['Clock mancante iniettato come condizione software sul banco file; non guasto fisico ALSA.',
                      'Nessuna misura di jack, DAC, latenza DAW o diffusori.']}


def main():
    if not __debug__: raise RuntimeError('Eseguire senza -O')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ssh')
    parser.add_argument('--binary',type=Path,default=Path.home()/'.local/opt/camilladsp-4.1.3-pipewire/camilladsp')
    parser.add_argument('--worker',action='store_true')
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    path=ROOT/'research-vault/sistema-autonomo-20261120/risultati-controllo.json'
    hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in SOURCES}
    if args.check:
        saved=json.loads(path.read_text(encoding='utf-8'))
        valid=valid_report(saved,hashes)
        print('Controllo ascolto: '+('rapporto coerente' if valid else 'rapporto da rigenerare'))
        raise SystemExit(0 if valid else 1)
    if args.ssh:
        files={p:base64.b64encode((ROOT/p).read_bytes()).decode() for p in SOURCES}
        payload=base64.b64encode(json.dumps(files).encode()).decode()
        script="""import base64,json,pathlib,tempfile,subprocess,sys
files=json.loads(base64.b64decode(PAYLOAD))
with tempfile.TemporaryDirectory(prefix='diy-control-bundle-') as tmp:
 root=pathlib.Path(tmp)
 for name,data in files.items():
  path=root/name; path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(base64.b64decode(data))
 result=subprocess.run([sys.executable,str(root/'tools/collauda-controllo-ascolto.py'),'--worker'],capture_output=True)
 sys.stdout.buffer.write(result.stdout); sys.stderr.buffer.write(result.stderr)
 sys.exit(result.returncode)
""".replace('PAYLOAD',repr(payload))
        ssh=str(Path(os.environ.get('SystemRoot','C:/Windows'))/'System32/OpenSSH/ssh.exe') if os.name=='nt' else 'ssh'
        result=subprocess.run([ssh,'-o','BatchMode=yes','-o','ConnectTimeout=8',args.ssh,'python3','-'],
                              input=script.encode(),capture_output=True,timeout=60)
        if result.returncode:
            sys.stderr.buffer.write(result.stderr); raise SystemExit(result.returncode)
        report=json.loads(result.stdout)
    else: report=worker(args.binary.resolve())
    if args.worker: print(json.dumps(report,allow_nan=False)); return
    report['source_sha256']=hashes
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=='__main__': main()
