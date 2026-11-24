"""Policy attestata e osservazione ALSA senza scrivere controlli o aprire PCM."""
import copy
import argparse
import hashlib
import json
from pathlib import Path,PurePosixPath
import re
import subprocess
from controllo_ascolto import Observation, validate_profile

ALSA_FORMATS={'S16_LE':'S16_LE','S24_3_LE':'S24_3LE','S32_LE':'S32_LE','F32_LE':'FLOAT_LE','F64_LE':'FLOAT64_LE'}


def digest(value):
    raw=value if isinstance(value,bytes) else json.dumps(value,sort_keys=True,allow_nan=False,separators=(',',':')).encode()
    return hashlib.sha256(raw).hexdigest()


def parse_hw_params(text):
    if text.strip()=='closed': return {}
    result={}
    for key in ('format','channels','rate'):
        found=re.search(r'^'+key+r':\s*(\S+)',text,re.M)
        if not found: return {}
        value=found.group(1)
        result[key]=value if key=='format' else int(re.match(r'\d+',value).group())
    return result


def parse_control(text):
    found=re.search(r'^\s*:\s*values=([^\r\n]+)',text,re.M)
    if not found: raise ValueError('Valore ALSA non leggibile')
    return found.group(1).strip()


def make_candidate(profile,manifest):
    """Genera soltanto dati; non attesta il candidato e non lo installa."""
    validate_profile(profile)
    cfg=copy.deepcopy(profile); p=manifest['pcm']; routing=manifest['routing']
    cfg['title']='DIY-2WAY '+profile['title']
    for direction in ('capture','playback'):
        cfg['devices'][direction]={'type':'Alsa','channels':p[direction+'_channels'],
            'device':f"hw:CARD={manifest['card_id']},DEV={p[direction+'_device']}",'format':p['format']}
    cfg['devices'].update(stop_on_rate_change=True,enable_rate_adjust=False,volume_limit=-6,resampler=None)
    first=cfg['mixers'][cfg['pipeline'][0]['name']]
    first['channels']['in']=p['capture_channels']
    for row in first['mapping']:
        for source in row['sources']: source['channel']=routing['sources'][source['channel']]
    cfg['mixers']['uscite_fisiche']={'channels':{'in':4,'out':p['playback_channels']},
        'mapping':[{'dest':channel,'sources':[{'channel':i,'gain':0,'inverted':False}]} for i,channel in enumerate(routing['outputs'])]}
    cfg['pipeline'].append({'type':'Mixer','name':'uscite_fisiche'})
    return cfg


def canonical_candidate(peer,profile,manifest):
    candidate=make_candidate(profile,manifest)
    if peer.call('GetVersion')!='4.1.3': raise ValueError('Versione DSP diversa da 4.1.3')
    return json.loads(peer.call({'ReadConfigJson':json.dumps(candidate,allow_nan=False)}))


class AlsaPolicy:
    owner_prefix='DIY-2WAY '
    hardware=True

    def __init__(self,manifest,profiles,proof_bytes):
        m=copy.deepcopy(manifest)
        if m.get('schema')!='ascolto-alsa-1' or m.get('verified') is not True:
            raise ValueError('Mappa hardware non qualificata')
        if digest(proof_bytes)!=m.get('proof_sha256'): raise ValueError('Prova di qualifica diversa')
        proof=json.loads(proof_bytes)
        if (proof.get('schema')!='qualifica-ascolto-1' or proof.get('verified') is not True
                or proof.get('physical_routing_verified') is not True or proof.get('volume_path_verified') is not True):
            raise ValueError('Qualifica fisica e volume non attestati')
        for key in ('card_id','usb','pcm','routing','clock','profiles_sha256','pipewire'):
            if proof.get(key)!=m.get(key): raise ValueError('Prova e mappa non coincidono: '+key)
        if not re.fullmatch(r'[A-Za-z0-9_]+',m['card_id']): raise ValueError('Card ID non valido')
        for key in ('vendor','product'):
            if not re.fullmatch(r'[0-9a-fA-F]{4}',m['usb'][key]): raise ValueError('Identità USB incompleta')
        identity_keys=set(m['usb'])-{'vendor','product'}
        if identity_keys=={'serial_sha256'}:
            serial=m['usb']['serial_sha256']
            if not re.fullmatch(r'[0-9a-f]{64}',serial) or serial==digest(b''):
                raise ValueError('Identità seriale assente')
        elif identity_keys=={'port_path'}:
            port=m['usb']['port_path']; relative=PurePosixPath(port)
            if relative.is_absolute() or '..' in relative.parts or not re.fullmatch(r'[A-Za-z0-9_:/.-]+',port):
                raise ValueError('Porta USB non attestata')
        else: raise ValueError('Specificare seriale oppure porta USB attestata')
        p=m['pcm']; r=m['routing']
        if type(p.get('verify_capture',True)) is not bool: raise ValueError('Cattura non qualificata')
        if (len(r['sources'])!=2 or len(set(r['sources']))!=2 or len(r['outputs'])!=4 or len(set(r['outputs']))!=4
                or any(type(n) is not int or n<0 or n>=p['capture_channels'] for n in r['sources'])
                or any(type(n) is not int or n<0 or n>=p['playback_channels'] for n in r['outputs'])):
            raise ValueError('Mappa canali non valida')
        if p['format'] not in ALSA_FORMATS: raise ValueError('Formato non supportato')
        for key in ('capture_device','playback_device'):
            if type(p[key]) is not int or not 0<=p[key]<=127: raise ValueError('PCM non valido')
        clock=m['clock']
        if clock['mode'] not in ('internal','external'): raise ValueError('Modo clock non valido')
        needed=('source_numid',) if clock['mode']=='internal' else ('source_numid','lock_numid','rate_numid')
        if any(type(clock.get(k)) is not int or not 0<clock[k]<65536 for k in needed):
            raise ValueError('Controlli clock non censiti')
        self.manifest=m
        self.allowed=set(m['profiles_sha256'].values())
        if {name:digest(cfg) for name,cfg in profiles.items()}!=m['profiles_sha256']:
            raise ValueError('Profili diversi dalla qualifica')
        for cfg in profiles.values(): self.validate(cfg)

    def validate(self,cfg):
        if self.manifest['pcm'].get('verify_capture',True) is not True:
            raise ValueError('ALSA diretto richiede anche la cattura verificata')
        signature=digest(cfg)
        if signature not in self.allowed: raise ValueError('Profilo non attestato; normalizzarlo prima della qualifica')
        if not cfg.get('title','').startswith(self.owner_prefix): raise ValueError('Profilo estraneo')
        m=self.manifest; p=m['pcm']; d=cfg['devices']
        if d['samplerate'] not in (44100,48000) or d.get('resampler') is not None or d.get('stop_on_rate_change') is not True:
            raise ValueError('Clock o rate non conformi')
        if d.get('volume_limit')!=-6: raise ValueError('Limite del volume non conforme')
        for direction in ('capture','playback'):
            expected={'type':'Alsa','channels':p[direction+'_channels'],
                      'device':f"hw:CARD={m['card_id']},DEV={p[direction+'_device']}",'format':p['format']}
            if any(d[direction].get(k)!=v for k,v in expected.items()): raise ValueError('PCM diverso dalla qualifica')
        last=cfg['mixers'][cfg['pipeline'][-1]['name']]
        if last['channels']!={'in':4,'out':p['playback_channels']}:
            raise ValueError('Numero di uscite diverso')
        if [r['dest'] for r in last['mapping']]!=m['routing']['outputs']:
            raise ValueError('Destinazioni fisiche diverse')
        def unity(row,channel):
            if row.get('mute') not in (None,False) or len(row['sources'])!=1: return False
            source=row['sources'][0]
            return (source.get('channel')==channel and source.get('gain')==0 and source.get('inverted') is False
                    and source.get('mute') in (None,False) and source.get('scale') in (None,'dB'))
        if not all(unity(row,i) for i,row in enumerate(last['mapping'])):
            raise ValueError('Assegnazione delle quattro vie diversa')
        first=cfg['mixers'][cfg['pipeline'][0]['name']]
        expected_sources=[m['routing']['sources'][i//2] for i in range(4)]
        if (first['channels']!={'in':p['capture_channels'],'out':4}
                or [r['dest'] for r in first['mapping']]!=list(range(4))
                or not all(unity(row,c) for row,c in zip(first['mapping'],expected_sources))):
            raise ValueError('Sorgenti delle quattro vie diverse')
        return signature


def linux_snapshot(manifest):
    """Legge ID stabile e identità USB; nessun valore seriale viene restituito in chiaro."""
    for folder in Path('/proc/asound').glob('card[0-9]*'):
        if (folder/'id').read_text().strip()!=manifest['card_id']: continue
        number=int(folder.name[4:]); device=(Path('/sys/class/sound')/folder.name/'device').resolve(strict=True)
        usb={}
        for parent in (device,*device.parents):
            if (parent/'idVendor').exists() and (parent/'idProduct').exists():
                usb={'vendor':(parent/'idVendor').read_text().strip(),'product':(parent/'idProduct').read_text().strip()}
                if 'serial_sha256' in manifest['usb']:
                    serial=(parent/'serial').read_text().strip()
                    if serial: usb['serial_sha256']=digest(serial.encode())
                else: usb['port_path']=str(parent.relative_to('/sys/devices'))
                break
        result={'card':number,'card_id':manifest['card_id'],'usb':usb}
        for direction,suffix in (('capture','c'),('playback','p')):
            if direction=='capture' and manifest['pcm'].get('verify_capture',True) is False: continue
            path=folder/f"pcm{manifest['pcm'][direction+'_device']}{suffix}"/'sub0/hw_params'
            result[direction]=parse_hw_params(path.read_text())
        return result
    return {}


def read_control(card,numid):
    result=subprocess.run(['amixer','-c',str(card),'cget',f'numid={numid}'],capture_output=True,text=True,check=True,timeout=1)
    return parse_control(result.stdout)


class AlsaObserver:
    def __init__(self,manifest,snapshot=None,control=read_control):
        self.manifest=manifest
        self.snapshot=snapshot or (lambda:linux_snapshot(manifest))
        self.control=control

    def identity(self):
        try:
            s=self.snapshot()
            return s.get('card_id')==self.manifest['card_id'] and s.get('usb')==self.manifest['usb']
        except (OSError,ValueError,KeyError): return False

    def observe(self,cfg):
        m=self.manifest; target=cfg['devices']['samplerate']
        try:
            s=self.snapshot(); ident=s.get('card_id')==m['card_id'] and s.get('usb')==m['usb']
            streams=('capture','playback') if m['pcm'].get('verify_capture',True) else ('playback',)
            params=all(s.get(direction)=={'format':ALSA_FORMATS[m['pcm']['format']],'channels':m['pcm'][direction+'_channels'],'rate':target}
                       for direction in streams)
            clock=m['clock']; card=s['card']
            locked=self.control(card,clock['source_numid'])==clock['source_expected']
            if clock['mode']=='external':
                locked=(locked and self.control(card,clock['lock_numid'])==clock['lock_expected']
                        and clock['rate_values_hz'].get(self.control(card,clock['rate_numid']))==target)
            rate=target if params else 0
            return Observation(rate,bool(locked and params),bool(ident and params),bool(ident))
        except (OSError,ValueError,KeyError,subprocess.SubprocessError):
            return Observation(0,False,False,False)


def main():
    parser=argparse.ArgumentParser(description='Genera e normalizza un candidato ALSA senza caricarlo o qualificarlo.')
    parser.add_argument('profile',type=Path)
    parser.add_argument('manifest',type=Path)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--port',type=int,default=12341)
    args=parser.parse_args()
    from pannello_ascolto import WebSocketPeer
    cfg=canonical_candidate(WebSocketPeer(args.port),json.loads(args.profile.read_text(encoding='utf-8')),
                            json.loads(args.manifest.read_text(encoding='utf-8')))
    with args.out.open('x',encoding='utf-8') as output:
        output.write(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'candidate':str(args.out),'sha256':digest(cfg),'qualified':False,'hardware_opened':False}))


if __name__=='__main__': main()
