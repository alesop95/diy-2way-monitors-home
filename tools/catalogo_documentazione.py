"""Elenco dei percorsi documentali pubblici del progetto, senza copiarne il contenuto."""
from pathlib import Path
import argparse
import csv
import io
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PAGE = 'docs/90-riferimenti/catalogo-documentazione.md'
CSV = 'data/catalogo-documentazione.csv'
GROUPS = [('docs/','Documentazione tecnica e procedure'),
          ('.claude/context/','Contesto e didattica'),('.claude/memory/','Memoria e lezioni'),
          ('research-vault/','Fonti, bibliografia e ricerca'),('config/','Configurazioni documentate'),
          ('knowledge/','Wiki e conoscenza')]


def records():
    paths = subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=ROOT).decode('utf-8').split('\0')
    result = []
    for path in sorted(set(paths)):
        suffix = Path(path).suffix.lower()
        for prefix, group in GROUPS:
            if path.startswith(prefix) and (suffix == '.md' or
                (path.startswith('docs/latex/') and suffix == '.tex') or
                (path.startswith('research-vault/') and suffix in {'.json','.bib'})):
                result.append((group,path))
                break
    return result


def outputs():
    entries = records()
    lines = ['# Catalogo completo dei percorsi documentali','',
             '<!-- Generato da tools/catalogo_documentazione.py; non è una seconda copia dei documenti. -->','',
             'Radice di questa postazione: `E:\\diy-2way-monitors-home`. Ogni percorso relativo delle tabelle va aggiunto a questa radice. Il [CSV completo](../../data/catalogo-documentazione.csv) include anche il percorso assoluto Windows. L’elenco censisce i file pubblicabili presenti, compresi quelli ancora da aggiungere manualmente a git; esclude template, binari, appunti privati e fonti della biblioteca esterna.','',
             f'{len(entries)} file documentali, bibliografici e di ricerca. Il [percorso di lettura](../STATO-PROGETTO.md) spiega cosa leggere; questo catalogo risponde a dove si trova ogni file. Lo stato operativo resta nella memoria canonica.','',
             'Per le prove binarie correnti, i manuali privati, i modelli CAD e gli archivi dei tentativi precedenti consultare la [mappa degli artefatti](artefatti-e-prove.md). Per fonti e punti d’uso consultare la [mappa del pedigree](fonti-progetto.md).','',
             'Rigenerazione eseguita con `python tools/catalogo_documentazione.py`; verifica con `python tools/catalogo_documentazione.py --check`. Non viene letto il contenuto degli altri repository o dei documenti privati.']
    for prefix,group in GROUPS:
        subset = [p for g,p in entries if g == group]
        if not subset:
            continue
        lines += ['',f'## {group}','', '| Percorso relativo esatto |','|---|']
        lines += [f'| [{p}](../../{p}) |' for p in subset]
    stream = io.StringIO(newline='')
    writer = csv.writer(stream,lineterminator='\n')
    writer.writerow(['categoria','percorso_relativo','percorso_assoluto_postazione'])
    for group,path in entries:
        writer.writerow([group,path,'E:\\diy-2way-monitors-home\\'+path.replace('/','\\')])
    return {PAGE:'\n'.join(lines)+'\n', CSV:stream.getvalue()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args = parser.parse_args()
    stale = []
    for rel,content in outputs().items():
        path = ROOT/rel
        if path.exists() and path.read_text(encoding='utf-8') == content:
            continue
        stale.append(rel)
        if not args.check:
            path.parent.mkdir(parents=True,exist_ok=True)
            if path.suffix == '.md':
                import sys
                sys.path.insert(0,str(ROOT/'.claude/templates/tools'))
                import rigenera_sicuro
                if rigenera_sicuro.scrivi(str(path),content,schema=r'^#{1,6} ') != 0:
                    raise RuntimeError(f'Rigenerazione rifiutata: {path}')
            else:
                path.write_text(content,encoding='utf-8',newline='\n')
    print(f'Catalogo: {len(records())} file; da rigenerare: {stale}')
    return int(args.check and bool(stale))


if __name__ == '__main__':
    raise SystemExit(main())
