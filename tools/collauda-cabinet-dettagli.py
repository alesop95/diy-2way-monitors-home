"""Collaudo FreeCAD in una cartella remota nuova; nessun deploy o rimozione remota.

Sviluppo e risultati restano nel repository locale. Il programma FreeCAD
già installato e' usato soltanto per il banco CAD temporaneo.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shlex
import subprocess
import tarfile

ROOT=Path(__file__).resolve().parents[1]
FILES=('tools/cabinet-dettagli-freecad.py','tools/progetto_cabinet.py','tools/studia_ingombri.py',
       'data/driver-geometria.json','config/cabinet/progetto-candidato.json','config/cabinet/studio-st120.json',
       'tools/cabinet-dettagli-vista.FCMacro')


def run(command,timeout=180):
    result=subprocess.run(command,capture_output=True,text=True,encoding='utf-8',timeout=timeout)
    if result.returncode: raise RuntimeError(result.stderr+result.stdout)
    return result.stdout.strip()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host',required=True)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--gui',action='store_true')
    args=parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*',args.host):
        raise ValueError('Alias SSH non valido')
    args.out.mkdir(parents=True,exist_ok=False)
    ssh=['ssh','-o','BatchMode=yes','-o','ConnectTimeout=8',args.host]
    work=run(ssh+['mktemp -d /tmp/diy-cabinet-details-XXXXXXXX'])
    if not re.fullmatch(r'/tmp/diy-cabinet-details-[A-Za-z0-9]{8}',work):
        raise RuntimeError('Cartella temporanea remota inattesa')
    payload=args.out/'input.tar'
    with tarfile.open(payload,'w') as archive:
        for name in FILES: archive.add(ROOT/name,arcname=name,recursive=False)
    run(['scp',str(payload),args.host+':'+work+'/input.tar'])
    q=shlex.quote(work)
    remote_hash=run(ssh+['sha256sum '+q+'/input.tar']).split()[0]
    if remote_hash!=hashlib.sha256(payload.read_bytes()).hexdigest():
        raise RuntimeError('Payload remoto non integro')
    run(ssh+['tar -xf '+q+'/input.tar -C '+q])
    app='"$HOME/.local/opt/freecad-1.1.4/FreeCAD_1.1.4-Linux-x86_64-py311.AppImage"'
    for label in ('normal','negative'):
        prefix='DIY_DETAIL_NEGATIVE_RADIUS=1 ' if label=='negative' else ''
        command=(prefix+'DIY_DETAIL_OUT='+q+'/'+label+' '+app+' freecadcmd -u '+q+'/'+label+'-user.cfg -s '+q+'/'+label+
                 '-system.cfg '+q+'/tools/cabinet-dettagli-freecad.py > '+q+'/'+label+'.log 2>&1')
        result=subprocess.run(ssh+[command],capture_output=True,text=True,encoding='utf-8',timeout=180)
        (args.out/(label+'-launcher.json')).write_text(json.dumps({'returncode':result.returncode,
            'stdout':result.stdout,'stderr':result.stderr},indent=2),encoding='utf-8')
    extra=''
    if args.gui:
        command=('DIY_DETAIL_GUI_BASE='+q+'/normal DIY_DETAIL_GUI_OUT='+q+'/views LIBGL_ALWAYS_SOFTWARE=1 '
                 'xvfb-run -a '+app+' -u '+q+'/gui-user.cfg -s '+q+'/gui-system.cfg '+q+
                 '/tools/cabinet-dettagli-vista.FCMacro > '+q+'/gui.log 2>&1')
        run(ssh+[command])
        extra=' views gui.log'
    run(ssh+['tar -czf '+q+'/outputs.tar.gz -C '+q+' normal negative normal.log negative.log'+extra])
    packed=args.out/'outputs.tar.gz'
    run(['scp',args.host+':'+work+'/outputs.tar.gz',str(packed)])
    with tarfile.open(packed,'r:gz') as archive:
        archive.extractall(args.out,filter='data')
    normal=json.loads((args.out/'normal/esito.json').read_text(encoding='utf-8'))
    negative=json.loads((args.out/'negative/esito.json').read_text(encoding='utf-8'))
    expected={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in FILES
              if name!='tools/cabinet-dettagli-freecad.py' and not name.endswith('.FCMacro')}
    if normal['status']!='success' or normal['input_sha256']!=expected:
        raise RuntimeError('CAD normale fallito o input differenti: leggere normal.log')
    source=hashlib.sha256((ROOT/FILES[0]).read_bytes()).hexdigest()
    if normal['source_sha256']!=source or len(normal['variants'])!=3:
        raise RuntimeError('Sorgente o varianti del CAD inattesi')
    if negative['status']!='failed' or 'Volume' not in negative.get('error',''):
        raise RuntimeError('Mutazione del foro non rilevata dalla misura del solido')
    summary={'passed':True,'normal':normal,'negative_error':negative['error'],
             'remote_work_directory':work,'remote_deleted':False,
             'note':'Banco temporaneo; nessun servizio o installazione ordinaria modificati'}
    if args.gui:
        gui=json.loads((args.out/'views/esito.json').read_text(encoding='utf-8'))
        if gui['status']!='captured' or len(gui['variants'])!=3:
            raise RuntimeError('Vista GUI non riuscita: leggere gui.log')
        summary['gui']=gui
    (args.out/'collaudo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'passed':True,'variants':len(normal['variants']),'version':normal['version'],
                      'negative_error':negative['error']}))


if __name__=='__main__':
    main()
