#!/usr/bin/env python3
"""Genera la biblioteca completa delle fonti e il vault delle fonti su J: (PA-027, ADR-038).

Legge il registro completo locale _notes/biblioteca/fonti-completo.json, l'indice del materiale di studio
research-vault/fonti-locali/lotto-*-origine.json, il manifesto della conversione
_notes/.tmp-doc-cache/fonti/manifest.json e le regole research-vault/biblioteca-regole.yml,
la cui specifica e' research-vault/09-Biblioteca-tassonomia.md. Assegna ogni fonte ai
gruppi di quattro alberi, cioe' disciplina, progetto, provenienza e stato, con regole
deterministiche, poi applica ai soli residui la classificazione di un agente in
_notes/biblioteca/classificazione-agente.json, e scrive:

  _notes/biblioteca/assegnazioni.json           chiave, titolo, gruppi e regole che li hanno
                                                assegnati: e' lo stato intermedio da rileggere,
                                                locale perche' i titoli del materiale su J:
                                                comprendono documenti personali
  <dest>/Biblioteca.bib                         biblioteca JabRef con i quattro alberi nel
                                                blocco jabref-meta, il campo groups e il
                                                campo file verso la posizione su J:
  <dest>/00-INDICE.md                           punto d'ingresso del vault Obsidian
  <dest>/Gruppi/<gruppo>.md                     una nota per gruppo, con le sue fonti
  <dest>/Fonti/<chiave>.md                      una nota per fonte

La destinazione predefinita e' J:/MAIN/LOUDSPEAKERS & ELECTROACOUSTIC/_VAULT FONTI, scelta
dall'utente il 2026-10-05. Lo strumento scrive soltanto dentro la destinazione e non
cancella nulla. Quando riscrive la nota di una fonte conserva per intero tutto cio' che
segue l'intestazione "## Note di lettura", che e' testo autorato. I campi owner della
libreria JabRef non vengono riportati.

Uso:
    python tools/biblioteca.py --prova      assegna e stampa i conteggi, non scrive su J:
    python tools/biblioteca.py              assegna e scrive biblioteca e vault
    python tools/biblioteca.py --dest DIR   destinazione diversa
"""
import argparse
import collections
import json
import re
import sys
import unicodedata
from pathlib import Path

import yaml

RADICE = Path(__file__).resolve().parent.parent
VAULT = RADICE / "research-vault"
LOCALI = VAULT / "fonti-locali"
CACHE = RADICE / "_notes" / ".tmp-doc-cache" / "fonti"
NOTE = RADICE / "_notes" / "biblioteca"
DEST = Path("J:/MAIN/LOUDSPEAKERS & ELECTROACOUSTIC/_VAULT FONTI")
SEGNO_LETTURA = "## Note di lettura"
SOGLIA_PAROLE = 50
LETTURA = 200_000      # caratteri del testo convertito letti per documento
SOGLIA_DISC = 8        # occorrenze minime perche' il contenuto assegni una disciplina
SOGLIA_PROG = 8        # e un capitolo o un filone del progetto


def albero(nodo, padre=(), uscita=None):
    """Appiattisce l'albero delle regole in una lista di percorsi, nell'ordine dichiarato."""
    uscita = [] if uscita is None else uscita
    for nome, figli in (nodo or {}).items():
        percorso = padre + (str(nome),)
        uscita.append(percorso)
        albero(figli, percorso, uscita)
    return uscita


def slug(testo, n=60):
    t = unicodedata.normalize("NFKD", testo).encode("ascii", "ignore").decode()
    t = re.sub(r"[^A-Za-z0-9]+", "-", t).strip("-").lower()
    return t[:n].strip("-") or "senza-titolo"


def nome_file(testo):
    """Nome di file sicuro su Windows e in Obsidian, leggibile."""
    t = re.sub(r'[<>:"/\\|?*#^\[\]]', " ", testo)
    return re.sub(r"\s+", " ", t).strip()[:120] or "senza-nome"


def bib_escape(v):
    return str(v).replace("{", "(").replace("}", ")").replace("\n", " ").strip()


def carica():
    regole = yaml.safe_load((VAULT / "biblioteca-regole.yml").read_text(encoding="utf-8"))
    # Le regole che descrivono l'SSD privato, cioe' cartelle, provenienze dal percorso e
    # documenti non pertinenti, vivono in un file locale e si uniscono qui (MS-202).
    locali_p = NOTE / "regole-locali.yml"
    if locali_p.exists():
        regole.update(yaml.safe_load(locali_p.read_text(encoding="utf-8")) or {})
    for k in ("cartelle", "provenienza_percorso", "non_pertinente"):
        regole.setdefault(k, {} if k != "non_pertinente" else [])
    fonti = json.loads((NOTE / "fonti-completo.json").read_text(encoding="utf-8"))
    posizioni = {}
    for r in sorted(LOCALI.glob("lotto-*-origine.json")):
        for v in json.loads(r.read_text(encoding="utf-8")):
            if v.get("esito") == "indicizzato" and v.get("sha256"):
                posizioni.setdefault(v["sha256"], v["posizione"])
    conv_p = CACHE / "manifest.json"
    conv = json.loads(conv_p.read_text(encoding="utf-8")) if conv_p.exists() else {}
    return regole, fonti, posizioni, conv


def relativo(posizione):
    p = posizione.replace("\\", "/")
    for radice in ("J:/MAIN/", "J:/"):
        if p.upper().startswith(radice.upper()):
            return p[len(radice):]
    return p


def assegna(regole, fonti, posizioni, conv):
    percorsi = albero(regole["alberi"])
    nomi = [p[-1] for p in percorsi]
    doppi = [n for n, c in collections.Counter(nomi).items() if c > 1]
    if doppi:
        sys.exit(f"nomi di gruppo ripetuti nell'albero: {doppi}")
    per_nome = {p[-1]: p for p in percorsi}
    compila = lambda sez: {g: [re.compile(x) for x in pp] for g, pp in regole[sez].items()}
    r_disc, r_prog, r_prov = compila("disciplina"), compila("progetto"), compila("provenienza_percorso")
    r_nonpert = [re.compile(x) for x in regole["non_pertinente"]]
    solo_titolo = set(regole.get("solo_titolo", []))
    citati = list(r_disc) + list(r_prog) + list(r_prov) + list(regole["appendici"])
    citati += [g for gg in regole["cartelle"].values() for g in gg]
    citati += [g for gg in regole["filoni_proposte"].values() for g in gg]
    citati += [g for g in regole["mappa_libreria"].values() if g]
    for g in citati:
        if g not in per_nome:
            sys.exit(f"le regole nominano un gruppo che non e' nell'albero: {g}")
    disciplina = set(n for p in percorsi if p[0] == "Disciplina" for n in p[1:]) - {"Da classificare"}
    # Classificazione dei residui fatta da un agente sul solo titolo: stato intermedio
    # versionato e correggibile a mano, applicato solo dove nessuna regola ha assegnato.
    ag_p = NOTE / "classificazione-agente.json"
    agente = json.loads(ag_p.read_text(encoding="utf-8")) if ag_p.exists() else {}

    voci, chiavi = [], set()
    for v in fonti:
        gruppi, motivi = set(), collections.defaultdict(list)

        def metti(g, motivo):
            if g in per_nome:
                gruppi.add(g)
                motivi[g].append(motivo)

        loc = v.get("locale") or {}
        chiave = v.get("citekey") or f"loc-{slug(v.get('titolo') or loc.get('file', ''), 40)}-{loc.get('sha256', '')[:6]}"
        base, i = chiave, 2
        while chiave.lower() in chiavi:
            chiave, i = f"{base}-{i}", i + 1
        chiavi.add(chiave.lower())
        posizione = posizioni.get(loc.get("sha256", ""))
        rel = relativo(posizione).lower() if posizione else ""
        titolo = " ".join([v.get("titolo") or "", v.get("sede") or ""]).lower()
        # Il percorso entra nelle parole chiave solo all'universita', dove le cartelle portano
        # i nomi dei corsi; altrove i nomi delle cartelle ombrello farebbero corrispondere tutto.
        testo = titolo + (" " + rel if rel.startswith("z_____universita") else "")

        for g in v.get("gruppi_libreria") or []:
            dest = regole["mappa_libreria"].get(g, g)
            if dest:
                metti(dest, f"libreria:{g}")
        for prefisso, gg in regole["cartelle"].items():
            if rel.startswith(prefisso):
                for g in gg:
                    metti(g, f"cartella:{prefisso}")
        for g, pp in r_disc.items():
            if any(x.search(testo) for x in pp):
                metti(g, "parole")
        for g, pp in r_prog.items():
            if any(x.search(testo) for x in pp):
                metti(g, "parole")
        # Il contenuto: le stesse parole chiave contate sul testo convertito. Un gruppo entra
        # solo se ricorre spesso, in assoluto e rispetto al gruppo piu' frequente del documento,
        # cosi' che una citazione di passaggio non basti.
        cv = conv.get(loc.get("sha256", ""))
        if cv and (CACHE / cv["cache"]).exists():
            corpo = (CACHE / cv["cache"]).read_text(encoding="utf-8", errors="replace")[:LETTURA].lower()
            for regole_g, soglia, quanti in ((r_disc, SOGLIA_DISC, 4), (r_prog, SOGLIA_PROG, 3)):
                punti = {g: sum(len(x.findall(corpo)) for x in pp) for g, pp in regole_g.items() if g not in solo_titolo}
                massimo = max(punti.values(), default=0)
                scelti = sorted((g for g, n in punti.items() if n >= soglia and n >= massimo * 0.25),
                                key=lambda g: -punti[g])[:quanti]
                for g in scelti:
                    metti(g, f"testo:{punti[g]}")
        for g in regole["filoni_proposte"].get(v.get("filone") or "", []):
            metti(g, f"filone:{v.get('filone')}")
        for app, radici in regole["appendici"].items():
            if any(r in per_nome[g] for g in list(gruppi) for r in radici):
                metti(app, "appendice dalla disciplina")
        if not gruppi & disciplina and chiave in agente:
            for g in agente[chiave].get("disciplina", []) + agente[chiave].get("progetto", []):
                metti(g, "agente")
        if not gruppi & disciplina and "Non pertinente" not in gruppi:
            metti("Da classificare", "nessuna regola")

        prov = v.get("provenienze", [])
        if "libreria" in prov:
            metti("Libreria JabRef ELE", "provenienza")
        if "tesi2020" in prov:
            metti("Bibliografia della tesi 2020", "provenienza")
        if "proposta" in prov:
            metti("Proposte dell'agente", "provenienza")
        if "scaricata" in prov:
            metti("Scaricati per la tesi", "provenienza")
        if "locale" in prov:
            metti("Materiale di studio su J:", "provenienza")
            for g, pp in r_prov.items():
                if any(x.search(rel.lower()) for x in pp):
                    metti(g, "percorso")

        c = conv.get(loc.get("sha256", ""))
        if v.get("stato_pdf") == "scaricato":
            metti("PDF scaricato", "stato")
        elif posizione:
            metti("PDF su J:", "stato")
        else:
            metti("Senza PDF", "stato")
        if c:
            metti("Scansione da OCR" if c.get("parole", 0) < SOGLIA_PAROLE else "Testo convertito", "conversione")
        if v.get("stato_verifica") == "verificato":
            metti("Verificato", "registro")
        elif "proposta" in prov or "scaricata" in prov:
            metti("Da verificare", "registro")
        if any(x.search(titolo + " " + rel) for x in r_nonpert):
            metti("Non pertinente", "parole")

        voci.append({"chiave": chiave, "voce": v, "posizione": posizione, "conv": c,
                     "gruppi": [p[-1] for p in percorsi if p[-1] in gruppi],
                     "motivi": {g: sorted(set(m)) for g, m in motivi.items()}})
    return percorsi, voci


def scrivi_bib(dest, percorsi, voci):
    righe = ["% Biblioteca completa delle fonti, generata da tools/biblioteca.py (ADR-038).",
             "% Non si modifica a mano: si cambiano le regole e si rigenera.", ""]
    tipi_ok = {"article", "book", "inproceedings", "incollection", "phdthesis", "mastersthesis",
               "techreport", "manual", "misc", "standard", "online", "inbook", "proceedings", "unpublished"}
    for x in voci:
        v = x["voce"]
        tipo = (v.get("tipo") or "misc").lower()
        tipo = tipo if tipo in tipi_ok else "misc"
        campi = [("title", v.get("titolo")), ("author", v.get("autori")), ("year", v.get("anno")),
                 ("journal" if tipo == "article" else "howpublished" if tipo == "misc" else "booktitle", v.get("sede")),
                 ("doi", v.get("doi")), ("note", v.get("riferimento")),
                 ("url", (v.get("url") or [None])[0] if isinstance(v.get("url"), list) else v.get("url"))]
        if x["posizione"]:
            p = x["posizione"].replace("\\", "/").replace(":", "\\:", 1)
            campi.append(("file", f":{p}:{Path(x['posizione']).suffix.lstrip('.').upper() or 'PDF'}"))
        campi.append(("groups", ", ".join(x["gruppi"])))
        righe.append(f"@{tipo}{{{x['chiave']},")
        righe += [f"  {k} = {{{bib_escape(val)}}}," for k, val in campi if val not in (None, "", [])]
        righe += ["}", ""]
    righe.append("@Comment{jabref-meta: databaseType:bibtex;}")
    righe.append("")
    righe.append("@Comment{jabref-meta: grouping:")
    righe.append("0 AllEntriesGroup:;")
    for p in percorsi:
        nome = p[-1].replace("\\", "\\\\").replace(";", "\\;")
        righe.append(f"{len(p)} StaticGroup:{nome}\\;0\\;1\\;\\;\\;\\;;")
    righe.append("}")
    (dest / "Biblioteca.bib").write_text("\n".join(righe) + "\n", encoding="utf-8")


def scrivi_vault(dest, percorsi, voci):
    (dest / "Fonti").mkdir(parents=True, exist_ok=True)
    (dest / "Gruppi").mkdir(parents=True, exist_ok=True)
    ob = dest / ".obsidian"
    if not ob.exists():
        ob.mkdir()
        (ob / "app.json").write_text('{\n  "useMarkdownLinks": false,\n  "newLinkFormat": "shortest"\n}\n', encoding="utf-8")
    per_gruppo = collections.defaultdict(list)
    nota = {}
    for x in voci:
        nota[x["chiave"]] = nome_file(x["chiave"])
        for g in x["gruppi"]:
            per_gruppo[g].append(x)
    for x in voci:
        v = x["voce"]
        p = dest / "Fonti" / f"{nota[x['chiave']]}.md"
        lettura = ""
        if p.exists():
            vecchio = p.read_text(encoding="utf-8")
            i = vecchio.find(SEGNO_LETTURA)
            if i >= 0:
                lettura = vecchio[i:]
        if not lettura:
            lettura = SEGNO_LETTURA + "\n\nDa scrivere alla lettura. Questa sezione non viene mai riscritta dallo strumento.\n"
        righe = ["---", f"chiave: \"{x['chiave']}\"", f"titolo: \"{(v.get('titolo') or '').replace(chr(34), chr(39))}\"",
                 f"anno: \"{v.get('anno') or ''}\"", "gruppi:"] + [f"  - \"{g}\"" for g in x["gruppi"]] + ["---",
                 f"# {v.get('titolo') or x['chiave']}", ""]
        if v.get("autori"):
            righe.append(f"Autori: {v['autori']}  ")
        if v.get("sede"):
            righe.append(f"Sede: {v['sede']}  ")
        if v.get("riferimento"):
            righe.append(f"Riferimento: {v['riferimento']}  ")
        if v.get("doi"):
            righe.append(f"DOI: [{v['doi']}](https://doi.org/{v['doi']})  ")
        if x["posizione"]:
            righe.append(f"File: [{Path(x['posizione']).name}](<file:///{x['posizione'].replace(chr(92), '/')}>)  ")
        if x["conv"]:
            testo = (CACHE / x["conv"]["cache"]).as_posix()
            righe.append(f"Testo convertito: [{x['conv'].get('parole', 0)} parole](<file:///{testo}>)  ")
        righe += ["", "Gruppi: " + " · ".join(f"[[{nome_file(g)}]]" for g in x["gruppi"]), "",
                  "<!-- Sopra: generato da tools/biblioteca.py, riscritto a ogni corsa. -->", "", lettura.rstrip() + "\n"]
        p.write_text("\n".join(righe), encoding="utf-8")
    figli = collections.defaultdict(list)
    for q in percorsi:
        if len(q) > 1:
            figli[q[-2]].append(q[-1])
    for q in percorsi:
        g = q[-1]
        elenco = sorted(per_gruppo.get(g, []), key=lambda x: (x["voce"].get("titolo") or x["chiave"]).lower())
        righe = ["---", f"gruppo: \"{g}\"", f"fonti: {len(elenco)}", "---", f"# {g}", "",
                 "Percorso: " + " / ".join(f"[[{nome_file(n)}]]" for n in q), ""]
        if figli.get(g):
            righe += ["Sottogruppi: " + " · ".join(f"[[{nome_file(n)}]] ({len(per_gruppo.get(n, []))})" for n in figli[g]), ""]
        righe += [f"## Fonti ({len(elenco)})", ""]
        righe += [f"- [[{nota[x['chiave']]}|{(x['voce'].get('titolo') or x['chiave']).replace('|', '-')}]]"
                  + (f" ({x['voce']['anno']})" if x['voce'].get('anno') else "") for x in elenco]
        (dest / "Gruppi" / f"{nome_file(g)}.md").write_text("\n".join(righe) + "\n", encoding="utf-8")
    righe = ["# Vault delle fonti", "",
             "Generato da `tools/biblioteca.py` del progetto diy-2way-monitors-home (ADR-038). "
             "La biblioteca JabRef e' `Biblioteca.bib` in questa cartella. Ogni nota di fonte ha una "
             "sezione di note di lettura che lo strumento non riscrive.", "",
             f"Fonti: {len(voci)}.", ""]
    for q in percorsi:
        righe.append("  " * (len(q) - 1) + f"- [[{nome_file(q[-1])}]] ({len(per_gruppo.get(q[-1], []))})")
    (dest / "00-INDICE.md").write_text("\n".join(righe) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="Genera biblioteca e vault delle fonti")
    ap.add_argument("--prova", action="store_true", help="assegna e stampa i conteggi, senza scrivere su J:")
    ap.add_argument("--dest", default=str(DEST), help="cartella del vault")
    a = ap.parse_args()
    regole, fonti, posizioni, conv = carica()
    percorsi, voci = assegna(regole, fonti, posizioni, conv)
    # Le voci non pertinenti, cioe' documenti personali, amministrativi o estranei allo studio,
    # non entrano ne' nella biblioteca ne' nel vault, per scelta dell'utente (MS-202).
    esclusi = [x for x in voci if "Non pertinente" in x["gruppi"]]
    voci = [x for x in voci if "Non pertinente" not in x["gruppi"]]
    conta = collections.Counter(g for x in voci for g in x["gruppi"])
    assegn = [{"chiave": x["chiave"], "titolo": x["voce"].get("titolo"), "gruppi": x["gruppi"], "motivi": x["motivi"]} for x in voci]
    (NOTE / "assegnazioni.json").write_text(json.dumps(assegn, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"escluse come non pertinenti {len(esclusi)}")
    print(f"fonti {len(voci)}; gruppi {len(percorsi)}; da classificare {conta['Da classificare']}; vuoti {sum(1 for p in percorsi if not conta[p[-1]])}")
    for p in percorsi:
        print(f"{conta[p[-1]]:6d} {'  ' * (len(p) - 1)}{p[-1]}")
    if a.prova:
        return 0
    dest = Path(a.dest)
    dest.mkdir(parents=True, exist_ok=True)
    scrivi_bib(dest, percorsi, voci)
    scrivi_vault(dest, percorsi, voci)
    print(f"scritti {dest / 'Biblioteca.bib'}, {len(voci)} note di fonte e {len(percorsi)} note di gruppo")
    return 0


if __name__ == "__main__":
    sys.exit(main())
