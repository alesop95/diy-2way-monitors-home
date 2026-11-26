"""Trova i font di account senza dipendere dagli artefatti di un vecchio build."""
import hashlib
import os
from pathlib import Path

FONT_FILES=('Altro-Grotesk-Book.ttf','Altro-Serif-Light.ttf')


def resolve_fonts(directory=None,required=FONT_FILES,*,environment=None,home=None):
    environment=os.environ if environment is None else environment
    home=Path.home() if home is None else Path(home)
    configured=directory if directory is not None else environment.get('INTRAWELT_FONT_DIR')
    if configured is not None:
        folder=Path(configured).expanduser().resolve()
        missing=[name for name in required if not (folder/name).is_file()]
        if missing:
            raise FileNotFoundError('Font Intrawelt mancanti: '+', '.join(missing)+
                                    '. Correggere --font-dir o INTRAWELT_FONT_DIR.')
        return folder
    candidates=[]
    for variable in ('CODEX_HOME','CLAUDE_CONFIG_DIR'):
        if environment.get(variable):
            candidates.append(Path(environment[variable])/'skills/intrawelt-design/assets/fonts')
    candidates.extend(home/name/'skills/intrawelt-design/assets/fonts' for name in ('.codex','.claude'))
    if environment.get('LOCALAPPDATA'):
        candidates.append(Path(environment['LOCALAPPDATA'])/'Microsoft/Windows/Fonts')
    if environment.get('WINDIR'):
        candidates.append(Path(environment['WINDIR'])/'Fonts')
    candidates.append(home/'.local/share/fonts')
    for folder in candidates:
        if all((folder/name).is_file() for name in required):return folder.resolve()
    raise FileNotFoundError('Font Intrawelt non trovati. Indicare --font-dir o INTRAWELT_FONT_DIR; '
                            'nessuna installazione automatica.')


def font_hashes(directory,required=FONT_FILES):
    return {name:hashlib.sha256((directory/name).read_bytes()).hexdigest() for name in required}
