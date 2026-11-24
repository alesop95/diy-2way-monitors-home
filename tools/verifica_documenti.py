"""Controlla i tre PDF correnti, la provenienza e l'assenza di copie QA sparse."""
from pathlib import Path, PurePosixPath
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]


def inspect_document(record,reader):
    for path in [record['pdf'],*record['sorgenti']]:
        relative=PurePosixPath(path)
        if relative.is_absolute() or '..' in relative.parts or ':' in path or '\\' in path:
            raise ValueError('Percorso non relativo al progetto')
    errors=[]
    for path,expected in [(record['pdf'],record['sha256']),*record['sorgenti'].items()]:
        try: actual=hashlib.sha256(reader(path)).hexdigest()
        except (OSError,KeyError): errors.append('File assente: '+path); continue
        if actual!=expected:
            errors.append(('PDF cambiato: ' if path==record['pdf'] else 'Sorgente cambiata: ')+path)
    return errors


def main():
    manifest=json.loads((ROOT/'docs/pdf/manifest.json').read_text(encoding='utf-8'))
    errors=[]
    expected={'recap-progetto.pdf','crossover-pc-pi-analogico.pdf','sistema-autonomo-driver-e-collaudo.pdf'}
    if {Path(r['pdf']).name for r in manifest['documenti']}!=expected:
        errors.append('Elenco PDF diverso dai tre documenti correnti')
    for record in manifest['documenti']:
        errors.extend(inspect_document(record,lambda p:(ROOT/p).read_bytes()))
    for folder in ('build/relazione-audio-20261120','build/recap-progetto-20261120'):
        errors.extend('PNG QA rimasto: '+str(p.relative_to(ROOT)) for p in (ROOT/folder).rglob('*.png'))
        errors.extend('PDF intermedio rimasto: '+str(p.relative_to(ROOT)) for p in (ROOT/folder).glob('*.pdf'))
    errors.extend('Temporaneo rimasto: '+str(p.relative_to(ROOT)) for p in (ROOT/'build').glob('*')
                  if p.is_dir() and p.name.startswith(('tmp','basso-')))
    print(json.dumps({'pdf':len(manifest['documenti']),'errori':errors},ensure_ascii=False))
    return int(bool(errors))


if __name__=='__main__': raise SystemExit(main())
