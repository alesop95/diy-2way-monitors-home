"""Pannello locale PC/Pi: sessione esplicita, sorveglianza e API limitata."""
import argparse
import copy
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import json
import math
from pathlib import Path
import secrets
import signal
import threading
import time

from controllo_ascolto import Controller,Observation,decoded,validate_profile
from monitor_dsp import RpcPeer,validate_lab_config

ROOT=Path(__file__).resolve().parents[1]


class WebSocketPeer:
    def __init__(self,port=12341):
        if type(port) is not int or not 0<port<65536: raise ValueError('Porta DSP non valida')
        self.port=port

    def call(self,command):
        from websockets.sync.client import connect
        with connect(f'ws://127.0.0.1:{self.port}',proxy=None,open_timeout=1,close_timeout=.5) as connection:
            return RpcPeer(connection,timeout=1).call(command)


class Session:
    def __init__(self,peer,profiles,observer=None,identity=lambda:True,validator=validate_profile,
                 owner_prefix='LABORATORIO',hardware=False,after_prepare=lambda cfg:None):
        self.peer=peer
        self.profiles=copy.deepcopy(profiles)
        for cfg in self.profiles.values(): validator(cfg)
        self.observer=observer or (lambda cfg:Observation(cfg['devices']['samplerate'],True,True,True))
        self.identity=identity
        self.after_prepare=after_prepare
        self.controller=Controller(peer,validator=validator,owner_prefix=owner_prefix)
        self.hardware=hardware
        self.lock=threading.RLock(); self.selected=None; self.error=None; self.startup_until=0
        self.snapshot={'state':'Attesa','ready':False,'mute':None,'volume':None,'error':None,
                       'profile':None,'profiles':list(self.profiles),'hardware':hardware}

    def status(self):
        with self.lock: return copy.deepcopy(self.snapshot)

    def poll(self):
        with self.lock:
            try:
                state=self.peer.call('GetState')
                if self.controller.needs_silence_retry:
                    self.controller.hold()
                    self.error='Collegamento ripristinato e mute confermato; prepara nuovamente il profilo.'
                if self.controller.ready:
                    starting=state=='Starting' and time.monotonic()<self.startup_until
                    if not starting and not self.controller.observe(self.observer(self.controller.profile)):
                        self.error='Sorgente, clock o configurazione da verificare; prepara nuovamente il profilo.'
                mute=self.peer.call('GetMute'); volume=self.peer.call('GetVolume')
                if type(mute) is not bool or type(volume) not in (int,float) or not math.isfinite(volume):
                    raise RuntimeError('Stato mute/volume non valido')
                self.snapshot.update(state=state,ready=self.controller.ready,mute=mute,volume=volume,
                                     error=self.error,profile=self.selected)
            except Exception as error:
                self.error='DSP non disponibile: '+str(error)
                if self.controller.ready:
                    try: self.controller.hold()
                    except Exception: self.error+='; mute non confermato'
                self.snapshot.update(state='Non disponibile',ready=False,mute=None,volume=None,error=self.error)
            return self.status()

    def action(self,name,body):
        if not isinstance(body,dict): raise ValueError('Richiesta JSON non valida')
        allowed={'prepare':{'profile'},'enable':{'volume'},'volume':{'volume'},'mute':set()}
        if name not in allowed or set(body)!=allowed[name]: raise ValueError('Operazione o campi non ammessi')
        if name=='prepare' and body['profile'] not in self.profiles: raise ValueError('Profilo non dichiarato')
        volume=None
        if name in ('enable','volume'):
            if type(body['volume']) not in (int,float) or not math.isfinite(body['volume']) or not -60<=body['volume']<=-6:
                raise ValueError('Livello ammesso da -60 a -6 dB')
            volume=float(body['volume'])
        with self.lock:
            try:
                if name=='prepare':
                    if not self.identity():
                        if self.controller.ready: self.controller.hold()
                        raise RuntimeError('Periferica qualificata non disponibile')
                    self.controller.prepare(self.profiles[body['profile']])
                    try: self.after_prepare(self.controller.profile)
                    except Exception:
                        self.controller.hold()
                        raise
                    self.selected=body['profile']; self.startup_until=time.monotonic()+3
                elif name in ('enable','volume'):
                    if name=='volume' and self.peer.call('GetMute') is not False:
                        raise RuntimeError('Abilita esplicitamente l’ascolto prima del volume')
                    profile=self.controller.profile
                    if profile is None: raise RuntimeError('Prepara prima un profilo')
                    self.controller.enable(self.observer(profile),volume)
                else:
                    previous=decoded(self.peer.call('GetConfigJson'))
                    if previous is not None:
                        if not previous.get('title','').startswith(self.controller.owner_prefix):
                            raise RuntimeError('Istanza occupata da una configurazione estranea')
                        self.controller.validator(previous)
                    self.controller.manual_mute()
                self.error=None
            except Exception as error:
                self.error=str(error)
                self.snapshot.update(error=self.error,ready=self.controller.ready)
                raise
            return self.poll()

    def supervise(self,stop,interval=.25):
        while not stop.is_set():
            self.poll()
            stop.wait(interval)

    def close(self):
        with self.lock:
            if self.controller.profile is not None:
                active=decoded(self.peer.call('GetConfigJson'))
                if active==self.controller.profile: self.controller.hold()


def make_server(session,port=12342,assets=None,fonts=None):
    assets=Path(assets or ROOT/'config/controllo-ascolto')
    fonts=Path(fonts or ROOT/'build/consegna-cabinet-20261119/assets')
    token=secrets.token_urlsafe(32)
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args): pass

        def trusted(self):
            port=self.server.server_address[1]
            hosts={f'127.0.0.1:{port}',f'localhost:{port}'}
            origin=self.headers.get('Origin')
            return self.headers.get('Host') in hosts and (origin is None or origin in {'http://'+h for h in hosts})

        def send(self,status,raw,kind='application/json; charset=utf-8'):
            self.send_response(status); self.send_header('Content-Type',kind)
            self.send_header('Content-Length',str(len(raw))); self.send_header('Cache-Control','no-store')
            self.send_header('X-Content-Type-Options','nosniff')
            self.send_header('Content-Security-Policy',"default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; frame-ancestors 'none'")
            self.end_headers(); self.wfile.write(raw)

        def respond(self,status,value):
            self.send(status,json.dumps(value,ensure_ascii=False,allow_nan=False).encode())

        def do_GET(self):
            if not self.trusted(): self.respond(403,{'error':'Origine non ammessa'}); return
            if self.path=='/':
                page=(assets/'index.html').read_text(encoding='utf-8').replace('__TOKEN__',token)
                self.send(200,page.encode(),'text/html; charset=utf-8')
            elif self.path=='/api/status': self.respond(200,session.status())
            elif fonts and self.path in ('/fonts/Altro-Grotesk-Book.ttf','/fonts/Altro-Serif-Light.ttf'):
                path=Path(fonts)/self.path.rsplit('/',1)[-1]
                if path.is_file(): self.send(200,path.read_bytes(),'font/ttf')
                else: self.respond(404,{'error':'Font non disponibile'})
            else: self.respond(404,{'error':'Risorsa non disponibile'})

        def do_POST(self):
            # Consumare il corpo limitato prima di chiudere una richiesta
            # respinta: altrimenti il TCP può resettare prima del 403.
            try:
                length=int(self.headers.get('Content-Length','0'))
                if not 0<length<=4096: raise ValueError('Dimensione non ammessa')
                self.connection.settimeout(2)
                raw=self.rfile.read(length)
                if len(raw)!=length: raise ValueError('Corpo della richiesta incompleto')
            except (ValueError,OSError) as error:
                self.respond(400,{'error':str(error)}); return
            if not self.trusted() or not secrets.compare_digest(self.headers.get('X-Session-Token',''),token):
                self.respond(403,{'error':'Sessione non autorizzata'}); return
            try:
                if self.headers.get('Content-Type')!='application/json': raise ValueError('Richiesta JSON richiesta')
                if not self.path.startswith('/api/'): raise ValueError('Operazione non ammessa')
                body=json.loads(raw)
                state=session.action(self.path[5:],body)
                self.respond(200,state)
            except (ValueError,KeyError,TypeError) as error: self.respond(400,{'error':str(error)})
            except Exception as error: self.respond(409,{'error':str(error)})
    server=ThreadingHTTPServer(('127.0.0.1',port),Handler)
    server.daemon_threads=True; server.token=token
    return server


def load_session(path):
    from ascolto_alsa import AlsaObserver,AlsaPolicy
    from ascolto_pipewire import LabObserver,PipeWireObserver,PipeWirePolicy
    cfg=json.loads(path.read_text(encoding='utf-8'))
    options={}
    mode=cfg.get('mode','file')
    manifest=None
    if mode in ('alsa','pipewire-qualified'):
        manifest_path=path.parent/cfg['manifest']
        manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
        if manifest.get('verified') is not True: raise ValueError('Mappa hardware non qualificata')
    profiles={name:json.loads((path.parent/value).read_text(encoding='utf-8')) for name,value in cfg['profiles'].items()}
    if mode in ('alsa','pipewire-qualified'):
        raw=(manifest_path.parent/manifest['proof_file']).read_bytes()
        policy_type=AlsaPolicy if mode=='alsa' else PipeWirePolicy
        policy=policy_type(manifest,profiles,raw); observer=AlsaObserver(manifest)
        if mode=='pipewire-qualified': observer=PipeWireObserver(manifest,observer)
        options=dict(observer=observer.observe,identity=observer.identity,validator=policy.validate,
                     owner_prefix=policy.owner_prefix,hardware=True)
        if mode=='pipewire-qualified': options['after_prepare']=observer.bind
    elif mode=='pipewire': options=dict(validator=validate_lab_config,observer=LabObserver().observe)
    elif mode!='file': raise ValueError('Modo non supportato')
    return Session(WebSocketPeer(cfg.get('dsp_port',12341)),profiles,**options)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',type=Path,required=True)
    parser.add_argument('--port',type=int,default=12342)
    parser.add_argument('--fonts',type=Path)
    args=parser.parse_args()
    session=load_session(args.config.resolve())
    def terminate(*_): raise KeyboardInterrupt
    signal.signal(signal.SIGTERM,terminate)
    stop=threading.Event(); thread=threading.Thread(target=session.supervise,args=(stop,),daemon=True)
    server=make_server(session,port=args.port,fonts=args.fonts); thread.start()
    print(f'Pannello: http://127.0.0.1:{server.server_address[1]}',flush=True)
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally:
        stop.set(); thread.join(timeout=4); server.server_close(); session.close()


if __name__=='__main__': main()
