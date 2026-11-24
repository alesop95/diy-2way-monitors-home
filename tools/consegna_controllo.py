"""Kit locale riproducibile; nessun trasferimento o installazione automatica."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/'build/controllo-ascolto/controllo-ascolto.zip'
RUNTIME=('controllo_ascolto.py','monitor_dsp.py','ascolto_alsa.py','ascolto_pipewire.py',
         'dsp_pipewire.py','pannello_ascolto.py','consegna_controllo.py')


def bundle():
    files={f'tools/{n}':(ROOT/'tools'/n).read_bytes() for n in RUNTIME}
    files.update({p.relative_to(ROOT).as_posix():p.read_bytes() for p in sorted((ROOT/'config/controllo-ascolto').iterdir()) if p.is_file()})
    service='config/systemd/user/diy-listening-control.service'; files[service]=(ROOT/service).read_bytes()
    manual='docs/61-camilladsp-manuale-tecnico.md'; files[manual]=(ROOT/manual).read_bytes()
    for name in ('Altro-Grotesk-Book.ttf','Altro-Serif-Light.ttf'):
        files['assets/'+name]=(ROOT/'build/consegna-cabinet-20261119/assets'/name).read_bytes()
    manifest={'schema':'kit-ascolto-1','hardware_qualified':False,'auto_deploy':False,
              'files':{p:hashlib.sha256(raw).hexdigest() for p,raw in sorted(files.items())}}
    files['manifest.json']=(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
    output=io.BytesIO()
    with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for name,raw in sorted(files.items()):
            info=zipfile.ZipInfo(name,(2026,11,23,0,0,0)); info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o644<<16; archive.writestr(info,raw)
    return output.getvalue()


def verify_installed(folder):
    manifest=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
    for name,expected in manifest['files'].items():
        path=(folder/name).resolve()
        if not path.is_relative_to(folder.resolve()) or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
            raise ValueError('File diverso o fuori kit: '+name)
    return len(manifest['files'])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true'); parser.add_argument('--verify-installed',type=Path)
    args=parser.parse_args()
    if args.verify_installed:
        print(json.dumps({'verified_files':verify_installed(args.verify_installed),'hardware_qualified':False})); return
    raw=bundle()
    if args.check:
        valid=TARGET.exists() and TARGET.read_bytes()==raw
        print('Kit controllo: '+('coerente' if valid else 'da rigenerare')); raise SystemExit(0 if valid else 1)
    TARGET.parent.mkdir(parents=True,exist_ok=True); TARGET.write_bytes(raw)
    print(json.dumps({'zip':TARGET.relative_to(ROOT).as_posix(),'bytes':len(raw),
                      'sha256':hashlib.sha256(raw).hexdigest(),'auto_deploy':False}))


if __name__=='__main__': main()
