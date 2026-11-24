"""Il banco non deve consentire un link estraneo al sottografo posseduto."""
import unittest
import importlib.util
from pathlib import Path
from unittest import mock
from types import SimpleNamespace
import dsp_pipewire

spec=importlib.util.spec_from_file_location('collaudo_pw',Path(__file__).with_name('collauda-dsp-pipewire.py'))
bench=importlib.util.module_from_spec(spec)
spec.loader.exec_module(bench)


def graph(pairs):
    return [{'id':i+100,'type':'PipeWire:Interface:Link',
             'info':{'output-node-id':a,'input-node-id':b,
                     'output-port-id':c,'input-port-id':d}}
            for i,(a,b,c,d) in enumerate(pairs)]


class GraphGuardTest(unittest.TestCase):
    def test_exact_lab_graph_and_unrelated_hardware_are_allowed(self):
        dsp_pipewire.guard_links(graph([(1,2,10,20),(3,4,30,40),(8,9,80,90)]),
                                {1,2,3,4},{(10,20),(30,40)},complete=True)

    def test_one_lab_port_connected_to_hardware_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError,'Link'):
            dsp_pipewire.guard_links(graph([(1,2,10,20),(3,9,30,90)]),
                                    {1,2,3,4},{(10,20),(30,40)},complete=True)

    def test_incorrect_channel_link_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError,'Link'):
            dsp_pipewire.guard_links(graph([(1,2,11,20),(3,4,30,40)]),
                                    {1,2,3,4},{(10,20),(30,40)},complete=True)

    def test_missing_link_is_not_a_complete_bench(self):
        with self.assertRaisesRegex(RuntimeError,'mancanti'):
            dsp_pipewire.guard_links(graph([(1,2,10,20)]),
                                    {1,2,3,4},{(10,20),(30,40)},complete=True)

    def test_partial_construction_may_have_no_links(self):
        dsp_pipewire.guard_links([], {1,2,3,4}, {(10,20),(30,40)},complete=False)

    def test_sample_limit_exit_1_has_a_narrow_verified_exception(self):
        info='pw-cat\nCompiled with libpipewire 1.6.2\nLinked with libpipewire 1.6.2\n'
        self.assertTrue(dsp_pipewire.validate_exit('record',1,info,160,160,b'')['sample_limit_exit_1'])
        for role,code,version,size,log in [('play',1,info,160,b''),('record',2,info,160,b''),
                                          ('record',1,info,144,b''),('record',1,info,160,b'error'),
                                          ('record',1,info.replace('1.6.2','1.6.3'),160,b'')]:
            with self.subTest(role=role,code=code,version=version,size=size,log=log):
                with self.assertRaises(RuntimeError):
                    dsp_pipewire.validate_exit(role,code,version,size,160,log)

    def test_mute_reports_small_startup_ramp_and_requires_silent_steady_state(self):
        frames=[(5e-7,0,0,0)]*19200+[(0,0,0,0)]*(288000-19200)
        result=bench.measure(frames,0,True)
        self.assertEqual(result['mute_peak_steady'],0)
        self.assertEqual(result['mute_peak_startup'],5e-7)

    def test_mute_rejects_late_leak_or_large_initial_signal(self):
        for frames in ([(0,0,0,0)]*96000+[(1e-6,0,0,0)]*192000,
                       [(0.01,0,0,0)]*19200+[(0,0,0,0)]*(288000-19200)):
            with self.assertRaises(AssertionError): bench.measure(frames,0,True)

    def test_success_exit_does_not_excuse_a_short_recording(self):
        with self.assertRaises(RuntimeError):
            dsp_pipewire.validate_exit('record',0,'1.6.2',144,160,b'')
        with self.assertRaises(AssertionError): bench.measure([(0,0,0,0)]*192000,0,True)

    def test_refusing_active_pipeline_does_not_mute_or_stop_it(self):
        peer=mock.Mock()
        with mock.patch.object(bench,'read_status',return_value={'state':'Running','mute':False}), \
             mock.patch.object(bench,'stop_lab') as stop, \
             mock.patch.object(bench.subprocess,'run',return_value=SimpleNamespace(stdout='version')), \
             mock.patch.object(Path,'mkdir'),mock.patch.object(Path,'write_text'):
            with self.assertRaises(RuntimeError): bench.run_case(peer,{},Path('unused'),Path('input'))
            peer.call.assert_not_called()
            stop.assert_not_called()

    def test_acquisition_error_is_not_a_detected_routing_mutation(self):
        config={'mixers':{'stereo_quattro_vie':{'mapping':[{'sources':[{'channel':0}]}]}}}
        with mock.patch.object(bench,'run_case',side_effect=AssertionError('Cattura corta: 0 frame')):
            with self.assertRaisesRegex(AssertionError,'Cattura corta'):
                bench.detect_swapped_channels(None,config,Path('unused'),Path('input'))


if __name__=='__main__': unittest.main()
