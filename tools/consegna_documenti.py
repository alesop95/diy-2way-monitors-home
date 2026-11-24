"""Rigenera le tre consegne con Craft/LaTeX, conserva input e QA dichiarato."""
import argparse
from datetime import date
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import unicodedata
from craft_apps_comune import sistema,versione_installata
from verifica_documenti import inspect_document

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'docs/pdf/manifest.json'
BUILD=ROOT/'build/relazione-audio-20261120'


def run(command,cwd=ROOT,env=None):
    result=subprocess.run([str(x) for x in command],cwd=cwd,env=env,capture_output=True,
                          encoding='utf-8',errors='replace',timeout=180)
    if result.returncode: raise RuntimeError(result.stdout[-7000:]+result.stderr[-7000:])
    return result.stdout


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized(text): return ' '.join(unicodedata.normalize('NFKC',text).replace('\u2212','-').split())


def rebuild(record,cli,version):
    final=ROOT/record['pdf']; name=final.name
    BUILD.mkdir(parents=True,exist_ok=True)
    staged=BUILD/name
    if name=='recap-progetto.pdf':
        run([sys.executable,ROOT/'.claude/templates/craft-apps/tools/craft-documento.py','documento',
             ROOT/'docs/STATO-PROGETTO.md','--out',staged,'--stile',ROOT/'config/documenti/intrawelt-tecnico.json'])
    else:
        chapter='62' if name.startswith('crossover') else '63'
        run([sys.executable,ROOT/'docs/latex/converti.py',chapter])
        env=dict(os.environ,TEXMFCACHE=str(BUILD))
        run(['latexmk','-lualatex','-interaction=nonstopmode','-halt-on-error','-file-line-error',
             '-outdir='+str(BUILD),Path(name).with_suffix('.tex').name],cwd=ROOT/'docs/latex',env=env)
    info=json.loads(run([cli,'info',staged]))
    text=normalized(run([cli,'text',staged]))
    terms=list(record['controllo_testo']['termini_ritrovati'])
    if name.startswith('sistema'): terms+=['WebSocket','SIGTERM']
    missing=[term for term in terms if normalized(term) not in text]
    if missing or info.get('warnings'): raise RuntimeError(f'PDF da verificare: termini {missing}, warning {info.get("warnings")}')
    # Prima verifica il risultato; soltanto dopo sostituisce la consegna.
    shutil.copyfile(staged,final)
    if sha(staged)!=sha(final): raise RuntimeError('Copia PDF diversa')
    staged.unlink()
    sources=list(record['sorgenti'])
    sources.append('tools/consegna_documenti.py')
    if name.startswith('sistema'): sources.append('research-vault/sistema-autonomo-20261120/risultati-controllo.json')
    record.update(sha256=sha(final),bytes=final.stat().st_size,pagine=info['pages'],
                  sorgenti={p:sha(ROOT/p) for p in dict.fromkeys(sources)},collegamenti_pdf=info['links'])
    record['controllo_testo']={'strumento':'PdfCraft '+version,'termini_ritrovati':terms}
    record['ispezione_visiva']={'pagine_correnti':[],'esito':'Da ispezionare sulla nuova consegna.','png_conservate':False}
    record['rigenerazione']=str(date.today())
    return record


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--conferma-qa',choices=['recap-progetto.pdf','crossover-pc-pi-analogico.pdf','sistema-autonomo-driver-e-collaudo.pdf'])
    parser.add_argument('--pagine',help='Numeri delle sole pagine effettivamente ispezionate, separati da virgole')
    args=parser.parse_args(); manifest=json.loads(MANIFEST.read_text(encoding='utf-8'))
    if args.conferma_qa:
        record=next(r for r in manifest['documenti'] if Path(r['pdf']).name==args.conferma_qa)
        if inspect_document(record,lambda p:(ROOT/p).read_bytes()): raise ValueError('Consegna o input non correnti')
        pages=sorted(set(int(s) for s in (args.pagine or '').split(',') if s))
        if not pages or not all(1<=n<=record['pagine'] for n in pages): raise ValueError('Pagine QA non valide')
        record['ispezione_visiva']={'pagine_correnti':pages,'esito':'Testo, formule e tabelle leggibili nelle pagine ispezionate; nessun taglio rilevato.',
                                   'png_conservate':False,'data':str(date.today())}
    elif args.check:
        errors=[e for r in manifest['documenti'] for e in inspect_document(r,lambda p:(ROOT/p).read_bytes())]
        errors+=['QA assente: '+r['pdf'] for r in manifest['documenti'] if not r['ispezione_visiva']['pagine_correnti']]
        print(json.dumps({'errori':errors},ensure_ascii=False)); raise SystemExit(bool(errors))
    else:
        version,cli=versione_installata('pdfcraft',sistema())
        if cli is None: raise RuntimeError('PdfCraft non disponibile; nessuna installazione automatica')
        changed=[]
        for r in manifest['documenti']:
            if inspect_document(r,lambda p:(ROOT/p).read_bytes()):
                rebuild(r,cli,version); changed.append(r['pdf'])
        if not changed: print('PDF correnti, nessuna rigenerazione'); return
        manifest['data']=str(date.today())
        print(json.dumps({'rigenerati':changed,'qa':'Ispezionare le pagine cambiate e confermare; nessun PNG generato automaticamente.'},ensure_ascii=False))
    MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__': main()
