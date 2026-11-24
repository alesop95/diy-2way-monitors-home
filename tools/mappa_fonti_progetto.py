"""Mappa di provenienza e usi delle fonti pubbliche del progetto audio.

Riusa il normalizzatore del template e le citekey del registro bibliografico.
Non apre rete, materiale personale, altri repository o dischi esterni.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import ipaddress
import json
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('url_template',ROOT/'.claude/templates/verifica-link/tools/verifica-link-progetto.py')
url_tools = importlib.util.module_from_spec(spec)
spec.loader.exec_module(url_tools)


def identity(url):
    key = url_tools.chiave(url)
    if not key:
        raise ValueError(f'Indirizzo senza identità pubblica: {url}')
    return 'SRC-'+hashlib.sha256(key.encode()).hexdigest()[:16].upper()


def alias_index(records):
    result = {}
    for source in records:
        for url in [source.get('url'),*source.get('aliases',[])]:
            if not url:
                continue
            key = url_tools.chiave(url)
            if key in result and result[key]['id'] != source['id']:
                raise ValueError(f'Alias assegnato a due fonti: {url}')
            result[key] = source
    return result


def seed_index(records):
    result = {}
    for source in records:
        if source['id'] in result:
            raise ValueError(f"Identità duplicata: {source['id']}")
        result[source['id']] = dict(source,usi=list(source.get('usi_dichiarati',[])))
    return result


def default_source(url, label):
    return {'id':identity(url),'url':url,'aliases':[], 'usi':[], 'titolo':label or urlsplit(url).netloc,
            'tipo':'riferimento_storico_da_classificare',
            'spiegazione':'Riferimento rilevato nei documenti sotto elencati; titolo e funzione derivano dal contesto locale, non da una nuova lettura web.',
            'verifica':{'stato':'da_verificare','nota':'La ricognizione non promuove i riscontri storici a verifiche correnti.'},
            'lettura':{'stato':'da_riconciliare','copertura':'Consultare i microstep e la scheda della fonte per le eventuali letture precedenti.'}}


def public_url(url):
    host = urlsplit(url).hostname or ''
    try:
        return not (ipaddress.ip_address(host).is_private or ipaddress.ip_address(host).is_loopback)
    except ValueError:
        return bool(host and host != 'localhost')


def project_files(root):
    excluded = {'docs/90-riferimenti/fonti-progetto.md','research-vault/usi-fonti-progetto.json',
                'research-vault/anagrafiche-fonti-web.json'}
    paths = []
    for directory in ('docs','.claude/context','config','data'):
        for path in (root/directory).rglob('*'):
            rel = path.relative_to(root).as_posix()
            if path.is_file() and path.suffix.lower() in {'.md','.tex','.json','.html'} and rel not in excluded:
                if not rel.startswith(('docs/anti-slop/','docs/separazione-ambienti/','docs/latex/')):
                    paths.append(path)
    paths.append(root/'.claude/memory/decisions.md')
    # Topic autorati del progetto: non corpus, testi di terzi o biblioteca personale.
    for directory in ('research-vault/crossover-pc-pi-analogico','research-vault/sistema-autonomo-20261120','research-vault/web'):
        paths.extend((root/directory).glob('*.md'))
    return sorted(set(p for p in paths if p.exists()))


def build(root=ROOT):
    seeds = json.loads((root/'research-vault/anagrafiche-fonti-web.json').read_text(encoding='utf-8'))['fonti']
    aliases = alias_index(seeds)
    by_id = seed_index(seeds)
    bibliography = json.loads((root/'research-vault/fonti-proposte.json').read_text(encoding='utf-8'))
    bib_by_url = {url_tools.chiave(u):b['citekey'] for b in bibliography for u in b.get('url',[])}
    files = project_files(root)
    ignored = set()
    for path in files:
        rel = path.relative_to(root).as_posix()
        section = 'Documento'
        for number,line in enumerate(path.read_text(encoding='utf-8').splitlines(),1):
            if re.match(r'^#{1,6} ',line):
                section = re.sub(r'^#+ ','',line)
            for url in url_tools.estrai(line):
                if not public_url(url):
                    ignored.add('endpoint locale o privato')
                    continue
                key = url_tools.chiave(url)
                if not key:
                    continue
                source = aliases.get(key)
                if source:
                    record = by_id[source['id']]
                else:
                    ident = identity(url)
                    if ident not in by_id:
                        label_match = re.search(r'\[([^\]]+)\]\('+re.escape(url),line)
                        record = default_source(url,label_match.group(1) if label_match else urlsplit(url).netloc)
                        if key in bib_by_url:
                            record['citekey_esistente'] = bib_by_url[key]
                        by_id[ident] = record
                    record = by_id[ident]
                usage = {'file':rel,'riga':number,'sezione':section,'contesto':line.strip()[:320]}
                if usage not in record['usi']:
                    record['usi'].append(usage)
    records = sorted(by_id.values(),key=lambda s:(not s.get('prioritaria',False),s['id']))
    if len({s['id'] for s in records}) != len(records):
        raise ValueError('Identità duplicate')
    return {'schema':'fonti-usi-audio-1','data':'2026-11-20',
            'perimetro':{'file':len(files),'radici':['docs','.claude/context','decisioni','config','data','topic di ricerca autorati'],
                         'esclusi':['template e guide ereditate','corpus/biblioteca privata','_notes','altri repository','rete'],
                         'non_fonti_locali':sorted(ignored)},
            'bibliografia_canonica':'research-vault/fonti.json','fonti':records}


def context_text(text):
    # Il contesto viene da un altro documento: i suoi link relativi non
    # possono mantenere la stessa destinazione nel percorso della mappa.
    return re.sub(r'!?\[([^\]]*)\]\([^)]*\)',r'\1',text).replace('|','/')


def render(report):
    records = report['fonti']
    lines = ['# Fonti del progetto: identità, pedigree e punti di uso','',
             '<!-- Generato da tools/mappa_fonti_progetto.py; dati autorati in research-vault/anagrafiche-fonti-web.json. -->','',
             f"Ricognizione del {report['data']}: {len(records)} identità nei {report['perimetro']['file']} file del perimetro. Il [JSON completo](../../research-vault/usi-fonti-progetto.json) conserva tutti i punti d'uso con riga e sezione.",'',
             'Le chiavi bibliografiche preesistenti restano nel registro canonico del vault. Questa mappa descrive gli usi, non sostituisce la biblioteca. Registrata, letta e verificata sono proprietà distinte: le fonti storiche da riconciliare non diventano lette perché censite. Le letture parziali restano parziali.','',
             'Il perimetro esclude template, guide ereditate, testi privati, appunti, altri repository e nuove letture web. Il contenuto aziendale non è una fonte importata. Gli endpoint locali sono esclusi; pagine di prezzo e scaricamento rimangono distinte dalle evidenze tecniche.','',
             '| ID permanente | Fonte/etichetta locale | Tipo | Stato verifica | Usi rilevati |','|---|---|---|---|---|']
    for source in records:
        title = source['titolo'].replace('|','/').replace('\n',' ')
        lines.append(f"| [{source['id']}](#{source['id'].lower()}) | {title} | {source['tipo']} | {source['verifica']['stato']} | {len(source['usi'])} |")
    for source in records:
        lines += ['',f"## {source['id']}",'',source['titolo'],'',source['spiegazione'],'']
        if source.get('url'):
            lines += [f"Fonte canonica: [{source['url']}]({source['url']}).",'']
        if source.get('sha256'):
            lines += [f"Impronta SHA-256: `{source['sha256']}`.",'']
        if source.get('aliases'):
            lines += ['Alias dichiarati: '+', '.join(f'[{u}]({u})' for u in source['aliases'])+'.','']
        for key,label in [('ente','Responsabile'),('versione','Versione'),('citekey_esistente','Chiave bibliografica esistente')]:
            if source.get(key):
                lines += [f'{label}: {source[key]}.','']
        lines += [f"Verifica: {source['verifica']['stato']}, data {source['verifica'].get('data','non riconciliata')}. {source['verifica'].get('nota','')}",'',
                  f"Lettura: {source['lettura']['stato']}. {source['lettura']['copertura']}",'']
        if source.get('usi_progettuali'):
            lines += ['Usi progettuali dichiarati: '+source['usi_progettuali'],'']
        for use in source['usi'][:8]:
            lines += [f"Uso in [{use['file']}](../../{use['file']}), sezione «{use['sezione']}», riga {use['riga']}.",'']
            if use.get('contesto'):
                lines += ['Contesto locale: '+context_text(use['contesto']),'']
        if len(source['usi']) > 8:
            lines += ['Altri punti d’uso sono nel JSON completo indicato in apertura.','']
        if not source['usi']:
            lines += ['Registrata come fonte locale o riferimento esplicito; uso documentato nella scheda collegata ai metadati.','']
    return '\n'.join(lines).rstrip()+'\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args = parser.parse_args()
    report = build()
    outputs = {ROOT/'research-vault/usi-fonti-progetto.json':json.dumps(report,ensure_ascii=False,indent=2)+'\n',
               ROOT/'docs/90-riferimenti/fonti-progetto.md':render(report)}
    stale = []
    for path, content in outputs.items():
        old = path.read_text(encoding='utf-8') if path.exists() else ''
        if old == content:
            continue
        stale.append(path.relative_to(ROOT).as_posix())
        if not args.check:
            # Riusa il motore di rigenerazione protetta del template.
            import sys
            sys.path.insert(0,str(ROOT/'.claude/templates/tools'))
            import rigenera_sicuro
            result = rigenera_sicuro.scrivi(str(path),content,schema=r'^#{1,6} ')
            if result != 0:
                raise RuntimeError(f'Rigenerazione rifiutata: {path}')
    print(json.dumps({'fonti':len(report['fonti']),'file_perimetro':report['perimetro']['file'],
                      'usi':sum(len(s['usi']) for s in report['fonti']),'da_rigenerare':stale},ensure_ascii=False))
    return int(bool(stale) and args.check)


if __name__ == '__main__':
    raise SystemExit(main())
