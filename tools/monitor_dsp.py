#!/usr/bin/env python3
"""Controllo locale del DSP di progetto: stato, mute e laboratorio senza autoconnect."""
import argparse
import json
from pathlib import Path
import sys
import time

DEFAULT_PROFILE = Path.home() / '.config/diy-2way-monitors/camilladsp/laboratorio-pipewire.json'


class RpcPeer:
    def __init__(self, connection, timeout=3.0):
        self.connection = connection
        self.timeout = timeout

    def call(self, command):
        name = command if isinstance(command, str) else next(iter(command))
        self.connection.send(json.dumps(command))
        deadline = time.monotonic() + self.timeout
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError(f'Nessuna risposta per {name}')
            response = json.loads(self.connection.recv(timeout=remaining))
            if not isinstance(response, dict):
                raise RuntimeError('Risposta API non riconosciuta')
            if name not in response:
                continue
            result = response[name]
            if not isinstance(result, dict) or result.get('result') != 'Ok':
                raise RuntimeError(f'{name}: {result}')
            return result.get('value')


def validate_lab_config(config):
    if not isinstance(config, dict) or not str(config.get('title', '')).startswith('LABORATORIO'):
        raise ValueError('Il profilo non e marcato come laboratorio')
    devices = config.get('devices', {})
    if devices.get('samplerate') != 48000 or devices.get('chunksize') != 256:
        raise ValueError('Il banco richiede 48000 Hz e blocchi di 256 campioni')
    for direction, channels, name in (
        ('capture', 2, 'diy-monitor-lab-capture'),
        ('playback', 4, 'diy-monitor-lab-playback'),
    ):
        device = devices.get(direction, {})
        if (device.get('type') != 'PipeWire' or device.get('channels') != channels
                or device.get('node_name') != name
                or device.get('node_group_name') != 'diy-monitor-lab'
                or device.get('autoconnect_to') is not None):
            raise ValueError(f'{direction}: consentito solo il nodo di laboratorio senza autoconnect')


def read_status(peer):
    return {'version': peer.call('GetVersion'), 'state': peer.call('GetState'),
            'mute': peer.call('GetMute'), 'volume_db': peer.call('GetVolume'),
            'stop_reason': peer.call('GetStopReason')}


def wait_state(peer, accepted, timeout=5.0):
    deadline = time.monotonic() + timeout
    while True:
        state = peer.call('GetState')
        if state in accepted:
            return state
        if time.monotonic() >= deadline:
            raise TimeoutError(f'Stato DSP {state}, atteso uno di {sorted(accepted)}')
        time.sleep(0.05)


def load_lab(peer, config):
    validate_lab_config(config)
    if peer.call('GetVersion') != '4.1.3':
        raise ValueError('Motore diverso dalla versione 4.1.3 collaudata')
    peer.call({'SetMute': True})
    peer.call({'SetVolume': -60.0})
    peer.call({'SetConfigJson': json.dumps(config)})
    peer.call({'SetMute': True})
    # Senza link PipeWire il motore attende il primo buffer in Starting.
    # L'accettazione del profilo non dimostra che stia elaborando audio.
    wait_state(peer, {'Starting', 'Running', 'Paused', 'Stalled'})
    active = peer.call('GetConfigJson')
    active = json.loads(active) if isinstance(active, str) else active
    if not isinstance(active, dict):
        raise RuntimeError('La configurazione non risulta caricata')
    validate_lab_config(active)
    if active.get('title') != config['title']:
        raise RuntimeError('La configurazione caricata non coincide con quella richiesta')
    status = read_status(peer)
    if status['mute'] is not True or status['volume_db'] != -60:
        raise RuntimeError('Mute o guadagno iniziale del banco non confermati')
    return dict(status, audio_running=status['state'] == 'Running')


def stop_lab(peer):
    peer.call({'SetMute': True})
    peer.call({'SetVolume': -60.0})
    peer.call('Stop')
    wait_state(peer, {'Inactive'})
    return read_status(peer)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['stato', 'silenzio', 'laboratorio', 'attesa'])
    parser.add_argument('--port', type=int, default=12341)
    parser.add_argument('--profile', type=Path, default=DEFAULT_PROFILE)
    args = parser.parse_args()
    from websockets.sync.client import connect
    with connect(f'ws://127.0.0.1:{args.port}', proxy=None, open_timeout=3, close_timeout=2) as connection:
        peer = RpcPeer(connection)
        if args.command == 'laboratorio':
            result = load_lab(peer, json.loads(args.profile.read_text(encoding='utf-8')))
        elif args.command == 'attesa':
            result = stop_lab(peer)
        else:
            if args.command == 'silenzio':
                peer.call({'SetMute': True})
            result = read_status(peer)
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (OSError, RuntimeError, ValueError, ImportError, TimeoutError) as error:
        print(json.dumps({'error': str(error)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
