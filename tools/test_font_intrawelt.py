"""La risorsa esplicita prevale e un percorso errato non cambia il marchio."""
from pathlib import Path
import tempfile
import unittest

from font_intrawelt import resolve_fonts, FONT_FILES

ROOT=Path(__file__).resolve().parents[1]


class FontResources(unittest.TestCase):
    def setUp(self):
        (ROOT/'build').mkdir(exist_ok=True)
        temporary=tempfile.TemporaryDirectory(dir=ROOT/'build')
        self.addCleanup(temporary.cleanup)
        self.home=Path(temporary.name)

    def fontdir(self,name):
        folder=self.home/name
        folder.mkdir(parents=True,exist_ok=True)
        for filename in FONT_FILES:(folder/filename).write_bytes(b'fixture di sola selezione del percorso')
        return folder

    def test_explicit_directory_precedes_environment(self):
        explicit=self.fontdir('explicit');other=self.fontdir('other')
        self.assertEqual(resolve_fonts(explicit,environment={'INTRAWELT_FONT_DIR':str(other)},home=self.home),explicit)

    def test_invalid_explicit_resource_is_not_replaced(self):
        existing=self.fontdir('existing')
        with self.assertRaisesRegex(FileNotFoundError,'Altro-Serif-Light.ttf'):
            broken=self.home/'broken';broken.mkdir()
            (broken/FONT_FILES[0]).write_bytes(b'body')
            resolve_fonts(broken,environment={'INTRAWELT_FONT_DIR':str(existing)},home=self.home)

    def test_environment_is_an_explicit_resource(self):
        folder=self.fontdir('configured')
        self.assertEqual(resolve_fonts(environment={'INTRAWELT_FONT_DIR':str(folder)},home=self.home),folder)
        with self.assertRaises(FileNotFoundError):
            resolve_fonts(environment={'INTRAWELT_FONT_DIR':str(self.home/'absent')},home=self.home)

    def test_active_account_skill_is_discovered(self):
        account=self.home/'account'
        folder=self.fontdir('account/skills/intrawelt-design/assets/fonts')
        self.assertEqual(resolve_fonts(environment={'CODEX_HOME':str(account)},home=self.home),folder)

    def test_installed_windows_font_directory_is_discovered(self):
        folder=self.fontdir('windows/Fonts')
        self.assertEqual(resolve_fonts(environment={'WINDIR':str(folder.parent)},home=self.home),folder)

    def test_absent_design_system_has_actionable_error(self):
        with self.assertRaisesRegex(FileNotFoundError,'INTRAWELT_FONT_DIR'):
            resolve_fonts(environment={},home=self.home)


if __name__=='__main__':unittest.main()
