"""L'installazione deve rifiutare qualsiasi destinazione preesistente."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('installer',Path(__file__).with_name('installa-dsp-utente.py'))
installer=importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class ExclusiveInstallTest(unittest.TestCase):
    def test_late_existing_target_preserves_all_previous_targets(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp); new=base/'first.txt'; old=base/'second.txt'
            old.write_bytes(b'contenuto precedente')
            with self.assertRaises(FileExistsError):
                installer.write_new_files([(new,b'primo',0o644),(old,b'secondo',0o644)])
            self.assertFalse(new.exists())
            self.assertEqual(old.read_bytes(),b'contenuto precedente')

    def test_new_targets_have_the_exact_requested_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'subdir'/'new.py'
            installer.write_new_files([(path,b'print(1)\n',0o755)])
            self.assertEqual(path.read_bytes(),b'print(1)\n')


if __name__=='__main__': unittest.main()
