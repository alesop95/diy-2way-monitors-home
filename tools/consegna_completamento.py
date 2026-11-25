"""Kit nominale locale: firma soltanto gli artefatti ancora coincidenti col collaudo."""
import argparse
from datetime import datetime
import hashlib
import io
import json
from pathlib import Path
import shutil
import zipfile
from consegna_controllo import verify_installed
from studio_completamento import ROOT,build_report
from verifica_documenti import inspect_document

FREECAD=ROOT/'build/completamento-20261125-freecad-verificato'
CADCRAFT=ROOT/'build/completamento-20261125-cadcraft-verificato'
TARGET=ROOT/'build/consegna-completamento-20261125'
ZIP=ROOT/'build/consegna-completamento-20261125.zip'
RECORD=ROOT/'research-vault/completamento-20261125/consegna.json'
DOC_MANIFEST=ROOT/'docs/pdf/manifest.json'
SOURCES=('tools/acustica_cabinet.py','tools/progetto_cabinet.py','tools/studio_completamento.py',
    'tools/figure_completamento.py','tools/cabinet-dettagli-cadcraft.py','tools/cabinet-dettagli-freecad.py',
    'tools/cabinet-dettagli-vista.FCMacro','tools/collauda-cabinet-dettagli.py','tools/consegna_completamento.py',
    'tools/studia_ingombri.py','tools/studio_sistema_audio.py','tools/fattibilita_basso.py',
    'tools/test_acustica_cabinet.py','tools/test_progetto_cabinet.py','tools/test_studio_completamento.py',
    'tools/test_consegna_cabinet.py','tools/test_consegna_completamento.py','tools/test_figure_completamento.py',
    'data/driver-candidati.json','data/driver-geometria.json','config/cabinet/studio-st120.json',
    'config/cabinet/progetto-candidato.json','docs/64-reflex-direttivita-e-cabinet-nominale.md')


def sha(raw):return hashlib.sha256(raw).hexdigest()


def checked(path,expected,label):
    raw=path.read_bytes()
    if sha(raw)!=expected:raise ValueError(label+' diverso dal file verificato: '+path.name)
    return raw


def bundle():
    report_path=ROOT/'research-vault/completamento-20261125/risultati.json'
    report=json.loads(report_path.read_text(encoding='utf-8'));report.pop('generated_at',None)
    if report!=build_report():raise ValueError('Rapporto nominale non corrente')
    documents=json.loads(DOC_MANIFEST.read_text(encoding='utf-8'))
    document=next(d for d in documents['documenti'] if d['pdf']=='docs/pdf/reflex-direttivita-cabinet.pdf')
    if inspect_document(document,lambda name:(ROOT/name).read_bytes()):
        raise ValueError('PDF non corrente: rigenerare prima della consegna')
    normal=json.loads((FREECAD/'normal/esito.json').read_text(encoding='utf-8'))
    gui=json.loads((FREECAD/'views/esito.json').read_text(encoding='utf-8'))
    cad=json.loads((CADCRAFT/'esito.json').read_text(encoding='utf-8'))
    if normal['status']!='success' or gui['status']!='captured' or cad['status']!='success':
        raise ValueError('Collaudo CAD non riuscito')
    checked(ROOT/'tools/cabinet-dettagli-freecad.py',normal['source_sha256'],'Sorgente FreeCAD')
    checked(ROOT/'tools/cabinet-dettagli-vista.FCMacro',gui['source_sha256'],'Sorgente vista')
    checked(ROOT/'tools/cabinet-dettagli-cadcraft.py',cad['source_sha256'],'Sorgente CADCraft')
    for name,expected in normal['input_sha256'].items():checked(ROOT/name,expected,'Input CAD')
    files={}
    for row in normal['variants']:
        name=row['id'];folder=FREECAD/'normal'/name
        checked(folder/'cabinet-nominale.FCStd',row['native_sha256'],'Nativo FreeCAD')
        files[f'cad/{name}/cabinet-nominale.step']=checked(folder/'cabinet-nominale.step',row['step_sha256'],'STEP')
        view=next(v for v in gui['variants'] if v['id']==name)
        files[f'cad/{name}/cabinet-nominale.FCStd']=checked(FREECAD/'views'/name/'cabinet-con-vista.FCStd',view['native_sha256'],'Nativo con vista')
        files[f'cad/{name}/assieme.png']=checked(FREECAD/'views'/name/'assieme.png',view['preview_sha256'],'Vista')
        drawing=next(v for v in cad['variants'] if v['id']==name)
        for filename,expected in drawing['files'].items():
            files[f'cad/{name}/{filename}']=checked(CADCRAFT/name/filename,expected,'Tavola CADCraft')
    files.update({'sources/'+p:(ROOT/p).read_bytes() for p in SOURCES})
    for name in ('chiusa-reflex','condotto-ingombro-velocita','direttivita-ideale','condensatore-e-livelli'):
        files['figure/'+name+'.svg']=(ROOT/'docs/figure/completamento-20261125'/(name+'.svg')).read_bytes()
    files['reflex-direttivita-cabinet.pdf']=(ROOT/'docs/pdf/reflex-direttivita-cabinet.pdf').read_bytes()
    files['reports/risultati.json']=report_path.read_bytes()
    files['reports/cad-verificato.json']=(json.dumps({'freecad':normal,'gui':gui,'cadcraft':cad},ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    readme='''# Cabinet e progetto nominale: consegna del 25 novembre 2026

Aprire [la relazione PDF](reflex-direttivita-cabinet.pdf) per metodo, risultati e limiti. La base di studio resta A24 chiusa; il reflex e le altre varianti sono confronti nominali. Nessun ordine di taglio o qualifica hardware è implicito.

| Variante | Modello modificabile | Scambio 3D | Tavola | Distinta coppia |
|---|---|---|---|---|
| A24 | [FreeCAD](cad/A24/cabinet-nominale.FCStd) | [STEP](cad/A24/cabinet-nominale.step) | [PDF](cad/A24/pannelli-e-frontale.pdf) | [CSV](cad/A24/distinta-coppia.csv) |
| B27 | [FreeCAD](cad/B27/cabinet-nominale.FCStd) | [STEP](cad/B27/cabinet-nominale.step) | [PDF](cad/B27/pannelli-e-frontale.pdf) | [CSV](cad/B27/distinta-coppia.csv) |
| C24 | [FreeCAD](cad/C24/cabinet-nominale.FCStd) | [STEP](cad/C24/cabinet-nominale.step) | [PDF](cad/C24/pannelli-e-frontale.pdf) | [CSV](cad/C24/distinta-coppia.csv) |

Ogni cartella contiene anche DXF, SVG e vista dell'assieme. Nel nativo, il foglio Quote controlla dimensioni, tagli, incassi e rinforzo. I centri di fissaggio della tavola non sono fori pilota: diametri e lavorazioni finali dipendono da fissaggi ed esemplari.

I file nascono dai generatori del repository canonico, copiati in sources per ispezione insieme agli input. La rigenerazione si esegue nel repository, dove sono presenti programmi, font e strumenti di controllo. Il kit si consulta con FreeCAD o un lettore PDF/SVG; non installa applicazioni.

Il manifesto conserva le impronte dei file. Se modifichi un modello, conservarne una copia di lavoro: il generatore rifiuta di sovrascrivere una consegna modificata. Fonti e stato durevole restano nella documentazione versionata; questo kit è una vista generata e non un nuovo registro delle decisioni.
'''
    files['README.md']=readme.encode('utf-8')
    manifest={'schema':'kit-cabinet-nominale-1','hardware_qualified':False,'manufacturing_release':False,
              'files':{p:sha(raw) for p,raw in sorted(files.items())}}
    files['manifest.json']=(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode('utf-8')
    stream=io.BytesIO()
    with zipfile.ZipFile(stream,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for name,raw in sorted(files.items()):
            info=zipfile.ZipInfo(name,(2026,11,25,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
            archive.writestr(info,raw)
    return stream.getvalue()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--verify-installed',type=Path)
    args=parser.parse_args()
    if args.verify_installed:
        print(json.dumps({'verified_files':verify_installed(args.verify_installed)}));return 0
    raw=bundle()
    if args.check:
        valid=ZIP.is_file() and ZIP.read_bytes()==raw
        if valid:verify_installed(TARGET)
        record=json.loads(RECORD.read_text(encoding='utf-8')) if RECORD.is_file() else {}
        valid=valid and record.get('zip_sha256')==sha(raw)
        print('Consegna nominale: '+('coerente' if valid else 'da rigenerare'));return 0 if valid else 1
    if TARGET.exists():
        verify_installed(TARGET)
        if ZIP.is_file() and ZIP.read_bytes()!=raw:
            backup=ROOT/'_notes/archivio-prove/completamento-20261125'/('kit-'+datetime.now().strftime('%Y%m%d-%H%M%S-%f')+'.zip')
            backup.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ZIP,backup)
            if backup.read_bytes()!=ZIP.read_bytes():raise RuntimeError('Backup del kit non integro')
    TARGET.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        for name in archive.namelist():
            path=TARGET/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(archive.read(name))
    ZIP.write_bytes(raw)
    count=verify_installed(TARGET)
    record={'schema':1,'generated_at':datetime.now().astimezone().isoformat(timespec='seconds'),
            'directory':TARGET.relative_to(ROOT).as_posix(),'zip':ZIP.relative_to(ROOT).as_posix(),
            'zip_sha256':sha(raw),'verified_files':count,'hardware_qualified':False,'manufacturing_release':False,
            'source_sha256':{p:sha((ROOT/p).read_bytes()) for p in SOURCES}}
    RECORD.parent.mkdir(parents=True,exist_ok=True)
    RECORD.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'verified_files':count,'bytes':len(raw),'zip':record['zip']}))
    return 0


if __name__=='__main__':raise SystemExit(main())
