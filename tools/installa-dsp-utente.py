"""Installa solo su percorsi nuovi, o verifica la preparazione DSP esistente.

Non avvia servizi. Riceve l'archivio ufficiale già scaricato e la radice delle
sorgenti del progetto (tools e config). Non richiede sudo ne dipendenze Python.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import tarfile

ARCHIVE_SHA='04388dfbf0999732c51a972fa7c3dc7fa17437333124af7918022445c459851a'
BINARY_SHA='933502e484f4696a218a0a935d8fa240ba0045e2a4af929fc920d54195180081'
RELEASE='.local/share/diy-2way-monitors/releases/dsp-control-1.0.0'
BENCH_RELEASE='.local/share/diy-2way-monitors/releases/pipewire-bench-1.0.1'
BINARY='.local/opt/camilladsp-4.1.3-pipewire/camilladsp'


def digest(raw): return hashlib.sha256(raw).hexdigest()


def write_new_files(files):
    # Controllare l'intero insieme prima di creare il primo file.
    for target,_,_ in files:
        if target.exists() or target.is_symlink(): raise FileExistsError(target)
    for target,raw,mode in files:
        target.parent.mkdir(parents=True,exist_ok=True)
        with target.open('xb') as out: out.write(raw)
        target.chmod(mode)
        if target.read_bytes()!=raw: raise OSError(f'Copia non coincidente: {target}')


def source_files(root,home):
    mapping=[('tools/monitor_dsp.py',f'{RELEASE}/monitor_dsp.py',0o644)]
    mapping += [(f'tools/{name}',f'{BENCH_RELEASE}/{name}',0o644) for name in
             ['monitor_dsp.py','dsp_pipewire.py','collauda-dsp-pipewire.py']]
    mapping += [('config/systemd/user/diy-monitor-dsp.service','.config/systemd/user/diy-monitor-dsp.service',0o644),
                ('config/camilladsp/laboratorio-pipewire.json','.config/diy-2way-monitors/camilladsp/laboratorio-pipewire.json',0o644),
                ('config/camilladsp/monitor-dsp.sh','.local/bin/diy-monitor-dsp',0o755)]
    return [(home/dst,(root/src).read_bytes().replace(b'\r\n',b'\n'),mode) for src,dst,mode in mapping]


def binary_from_archive(path):
    raw=path.read_bytes()
    if digest(raw)!=ARCHIVE_SHA: raise ValueError('SHA-256 archivio diverso dal rilascio scelto')
    with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
        members=archive.getmembers()
        if len(members)!=1 or members[0].name!='camilladsp' or not members[0].isfile():
            raise ValueError('Contenuto archivio inatteso')
        content=archive.extractfile(members[0]).read()
    if digest(content)!=BINARY_SHA: raise ValueError('SHA-256 binario inatteso')
    return content


def verify(files,home):
    results=[]
    for target,raw,mode in files:
        actual=target.read_bytes()
        if actual.replace(b'\r\n',b'\n')!=raw: raise ValueError(f'File diverso dalle sorgenti: {target}')
        if mode&0o111 and not target.stat().st_mode&0o111: raise ValueError(f'Permesso eseguibile assente: {target}')
        results.append({'path':str(target),'sha256':digest(actual)})
    binary=home/BINARY
    if digest(binary.read_bytes())!=BINARY_SHA: raise ValueError('Binario installato diverso')
    if not binary.stat().st_mode&0o111: raise ValueError('Binario non eseguibile')
    return results+[{'path':str(binary),'sha256':BINARY_SHA}]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sorgenti',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--home',type=Path,default=Path.home(),help='Radice di prova alternativa, senza attivazione servizi')
    parser.add_argument('--archivio',type=Path)
    parser.add_argument('--verifica',action='store_true')
    args=parser.parse_args()
    home=args.home.resolve()
    files=source_files(args.sorgenti.resolve(),home)
    if not args.verifica:
        if args.archivio is None: parser.error('--archivio richiesto per una installazione nuova')
        binary=binary_from_archive(args.archivio)
        write_new_files(files+[(home/BINARY,binary,0o755)])
    print(json.dumps({'verified':True,'files':verify(files,home)},indent=2))


if __name__=='__main__': main()
