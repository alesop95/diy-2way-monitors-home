"""Contratto del controllo DSP: rifiuto dei percorsi fisici e caricamento muto."""
import copy
import json
from pathlib import Path
import unittest

import monitor_dsp

ROOT = Path(__file__).resolve().parents[1]


class FakePeer:
    def __init__(self, reject=False, loaded_state='Stalled'):
        self.calls = []
        self.muted = False
        self.volume = 0
        self.state = 'Inactive'
        self.reject = reject
        self.loaded_state = loaded_state
        self.config = None

    def call(self, command):
        self.calls.append(command)
        if isinstance(command, dict):
            if 'ValidateConfigJson' in command:
                return command['ValidateConfigJson']
            elif 'SetMute' in command:
                self.muted = command['SetMute']
            elif 'SetVolume' in command:
                self.volume = command['SetVolume']
            elif 'SetConfigJson' in command:
                if not self.muted:
                    raise AssertionError('Configurazione inviata prima del mute')
                if self.reject:
                    raise RuntimeError('Configurazione rifiutata dal motore')
                self.state = self.loaded_state
                self.config = command['SetConfigJson']
        else:
            return {'GetMute': self.muted, 'GetVolume': self.volume,
                    'GetState': self.state, 'GetVersion': '4.1.3',
                    'GetStopReason': 'None', 'GetConfigJson': self.config}.get(command)


class DspControlTest(unittest.TestCase):
    def setUp(self):
        self.config = json.loads((ROOT / 'config/camilladsp/laboratorio-pipewire.json').read_text(encoding='utf-8'))

    def test_lab_load_is_muted_before_configuration(self):
        peer = FakePeer()
        monitor_dsp.load_lab(peer, self.config)
        self.assertTrue(peer.muted)
        self.assertEqual(peer.volume, -60)
        sent = [command for command in peer.calls if isinstance(command, dict) and 'SetConfigJson' in command]
        self.assertEqual(len(sent), 1)
        self.assertEqual(json.loads(sent[0]['SetConfigJson']), self.config)

    def test_hardware_backend_is_rejected_before_any_request(self):
        bad = copy.deepcopy(self.config)
        bad['devices']['playback'] = {'type': 'Alsa', 'channels': 4, 'device': 'hw:0,0', 'format': 'F32_LE'}
        peer = FakePeer()
        with self.assertRaises(ValueError):
            monitor_dsp.load_lab(peer, bad)
        self.assertEqual(peer.calls, [])

    def test_autoconnect_is_rejected_before_any_request(self):
        bad = copy.deepcopy(self.config)
        bad['devices']['playback']['autoconnect_to'] = 'alsa_output.un_dispositivo_fisico'
        peer = FakePeer()
        with self.assertRaises(ValueError):
            monitor_dsp.load_lab(peer, bad)
        self.assertEqual(peer.calls, [])

    def test_rejected_config_propagates_error_and_leaves_mute(self):
        peer = FakePeer(reject=True)
        with self.assertRaisesRegex(RuntimeError, 'rifiutata'):
            monitor_dsp.load_lab(peer, self.config)
        self.assertTrue(peer.muted)

    def test_wrong_channel_count_is_rejected(self):
        bad = copy.deepcopy(self.config)
        bad['devices']['playback']['channels'] = 2
        peer = FakePeer()
        with self.assertRaises(ValueError):
            monitor_dsp.load_lab(peer, bad)
        self.assertEqual(peer.calls, [])

    def test_unlinked_lab_can_wait_in_starting_without_claiming_audio_running(self):
        peer = FakePeer(loaded_state='Starting')
        status = monitor_dsp.load_lab(peer, self.config)
        self.assertEqual(status['state'], 'Starting')
        self.assertFalse(status['audio_running'])
        self.assertTrue(status['mute'])

    def test_acknowledged_but_absent_profile_is_not_success(self):
        class MissingProfilePeer(FakePeer):
            def call(self, command):
                if command == 'GetConfigJson':
                    return 'null'
                return super().call(command)
        with self.assertRaisesRegex(RuntimeError, 'configurazione'):
            monitor_dsp.load_lab(MissingProfilePeer(), self.config)


if __name__ == '__main__':
    unittest.main()
