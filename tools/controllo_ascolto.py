"""Nucleo del controllo comune: volume, mute e perdita di qualificazione.

Il default accetta soltanto profili su file. La policy ALSA richiede una mappa
e una prova attestata; il codice non sostituisce la qualifica fisica sospesa.
"""
import argparse
from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path
import time


@dataclass(frozen=True)
class Observation:
    rate_hz: int
    clock_locked: bool
    routing_verified: bool
    identity_matches: bool


def validate_profile(profile):
    if not isinstance(profile,dict) or not profile.get('title','').startswith('LABORATORIO'):
        raise ValueError('Consentito soltanto un profilo di laboratorio')
    devices=profile.get('devices',{})
    for key,kind,channels,filename in (('capture','RawFile',2,'input.pcm'),('playback','File',4,'output.pcm')):
        device=devices.get(key,{})
        if (device.get('type')!=kind or device.get('channels')!=channels or device.get('filename')!=filename):
            raise ValueError('Questa versione accetta soltanto i file fissi di laboratorio 2/4')
    if devices.get('samplerate') not in (44100,48000):
        raise ValueError('Frequenza non qualificata nel laboratorio')
    if any(f.get('type') not in ('Biquad','BiquadCombo','Gain') for f in profile.get('filters',{}).values()):
        raise ValueError('Filtro esterno al perimetro')
    if any('filename' in json.dumps(f) for f in profile.get('filters',{}).values()):
        raise ValueError('File accessorio non ammesso')
    return hashlib.sha256(json.dumps(profile,sort_keys=True,allow_nan=False).encode()).hexdigest()


def decoded(value):
    return json.loads(value) if isinstance(value,str) else value


class Controller:
    def __init__(self,peer,validator=validate_profile,settle_timeout=2.0,owner_prefix='LABORATORIO'):
        self.peer=peer
        self.validator=validator
        self.settle_timeout=settle_timeout
        self.owner_prefix=owner_prefix
        self.profile=None
        self.ready=False
        self.needs_silence_retry=False

    def hold(self):
        # Non dichiarare il mute riuscito se la RPC fallisce. Prova comunque
        # anche la seconda azione, conservando l'errore per il chiamante.
        self.needs_silence_retry=True
        errors=[]
        for command in ({'SetMute':True},{'SetVolume':-60.0}):
            try: self.peer.call(command)
            except Exception as error: errors.append(str(error))
        self.ready=False
        if not errors:
            try:
                if self.peer.call('GetMute') is not True or self.peer.call('GetVolume')!=-60:
                    errors.append('Attesa silenziata non confermata dalla rilettura')
            except Exception as error: errors.append(str(error))
        if errors: raise RuntimeError('; '.join(errors))
        self.needs_silence_retry=False

    def manual_mute(self):
        qualified_before=self.ready
        self.hold()
        self.ready=qualified_before

    def prepare(self,profile):
        self.validator(profile)  # prima di qualsiasi richiesta al peer
        if self.peer.call('GetVersion')!='4.1.3': raise RuntimeError('Versione diversa dalla qualificata')
        previous=decoded(self.peer.call('GetConfigJson'))
        if previous is not None and not str(previous.get('title','')).startswith(self.owner_prefix):
            raise RuntimeError('Istanza occupata da una configurazione estranea')
        if previous is not None: self.validator(previous)
        canonical=decoded(self.peer.call({'ValidateConfigJson':json.dumps(profile,allow_nan=False)}))
        self.validator(canonical)
        self.hold()
        self.profile=None
        try:
            self.peer.call({'SetConfigJson':json.dumps(canonical,allow_nan=False)})
            deadline=time.monotonic()+self.settle_timeout
            while decoded(self.peer.call('GetConfigJson'))!=canonical:
                if time.monotonic()>=deadline:
                    raise RuntimeError('Rilettura della configurazione diversa dopo la scadenza')
                time.sleep(.01)
            if self.peer.call('GetMute') is not True or self.peer.call('GetVolume')!=-60:
                raise RuntimeError('Attesa silenziata non confermata')
            self.profile=json.loads(json.dumps(canonical))
            self.ready=True
        except Exception:
            self.hold()
            raise

    def qualified(self,observation):
        return (self.ready and self.profile is not None
                and observation.rate_hz==self.profile['devices']['samplerate']
                and observation.clock_locked is True and observation.routing_verified is True
                and observation.identity_matches is True and self.peer.call('GetState')=='Running'
                and decoded(self.peer.call('GetConfigJson'))==self.profile)

    def enable(self,observation,volume_db):
        if not math.isfinite(volume_db) or not -60 <= volume_db <= -6:
            raise ValueError('Volume fuori dal limite di sviluppo [-60,-6] dB')
        try:
            if not self.qualified(observation): raise RuntimeError('Condizioni di ascolto non qualificate')
            self.peer.call({'SetVolume':float(volume_db)})
            if self.peer.call('GetVolume')!=volume_db: raise RuntimeError('Volume non confermato')
            self.peer.call({'SetMute':False})
            if self.peer.call('GetMute') is not False: raise RuntimeError('Unmute non confermato')
        except Exception:
            self.hold()
            raise

    def observe(self,observation):
        try: valid=self.qualified(observation)
        except Exception:
            self.hold()
            raise
        if not valid: self.hold()
        return valid


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('profile',type=Path)
    args=parser.parse_args()
    profile=json.loads(args.profile.read_text(encoding='utf-8'))
    print(json.dumps({'valid':True,'sha256':validate_profile(profile),'hardware_enabled':False,
                      'note':'Nessuna connessione RPC aperta dalla CLI; nucleo da integrare con adapter qualificato.'}))


if __name__=='__main__': main()
