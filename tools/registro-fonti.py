#!/usr/bin/env python3
"""Registro unico delle fonti del vault di ricerca.

Rigenera research-vault/fonti.json, il registro completo locale _notes/biblioteca/fonti-completo.json,
research-vault/papers/manifest.json e la nota
research-vault/06-Registro-fonti.md fondendo cinque provenienze, ciascuna dichiarata
nella voce invece di essere dedotta:

  proposta    research-vault/fonti-proposte.json, candidati dell'agente gia' riscontrati
  libreria    research-vault/basi/ELE_Technical_Library.bib, libreria JabRef di terzi,
              filtrata sui gruppi pertinenti (solo metadati: i suoi PDF non esistono)
  tesi2020    research-vault/basi/tesi-2020-bibliografia.txt, bibliografia della tesi
              magistrale dell'utente estratta con pdftotext
  locale      research-vault/fonti-locali/lotto-*-origine.json, indice del materiale di
              studio che resta su J:, con posizione e impronta (ADR-036)
  scaricata   research-vault/papers/*.pdf, PDF scaricati dall'utente, con nome uguale
              alla chiave bibliografica

Le voci si uniscono per DOI e poi per titolo normalizzato. Crea in research-vault/paper/
la scheda delle sole fonti proposte o scaricate, e non sovrascrive mai una scheda gia'
esistente, che dopo la creazione e' testo autorato. I percorsi su J: e il contenuto dei
libri non entrano nel registro tracciato (ADR-028): delle copie locali restano titolo,
lotto, impronta e dimensione.

Uso:
    python tools/registro-fonti.py           rigenera
    python tools/registro-fonti.py --check   esce 1 se il registro su disco e' vecchio
"""
import argparse
import difflib
import hashlib
import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
VAULT = RADICE / "research-vault"
COMPLETO = RADICE / "_notes" / "biblioteca" / "fonti-completo.json"
GRUPPI_PERTINENTI = {
    "Loudspeakers", "Loudspeaker motor", "Acoustics", "Signal processing",
    "Digital Signal Processing", "Audio electronics", "Electronics and circuit theory",
    "Analog electronics", "Analog", "Circuit theory", "Amplifiers 2.0", "Electromagnetism",
    "Mathematics", "Analysis", "Algebra", "Numerical mathematics", "Mechanics",
    "Spatial perception", "Sound field analysis", "Nonlinear Signal Processing",
    "Statistical Signal Processing", "Plane wave tube", "Acustica classica",
    "Audio and acoustics signal processing", "Probability and statistics",
}


def norm_titolo(t):
    t = unicodedata.normalize("NFKD", t or "").encode("ascii", "ignore").decode()
    t = re.sub(r"[{}\\]", "", t.lower())
    t = re.sub(r"[^a-z0-9]+", " ", t).strip()
    # "Part I" e "Part 1" sono lo stesso titolo: la numerazione romana si porta in cifre
    return re.sub(r"\bpart (iv|iii|ii|i)\b",
                  lambda m: "part " + str(["i", "ii", "iii", "iv"].index(m.group(1)) + 1), t)


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for blocco in iter(lambda: fh.read(1 << 20), b""):
            h.update(blocco)
    return h.hexdigest()


def leggi_campi(corpo):
    """Legge i campi di una voce BibTeX contando le parentesi, cosi' che un valore
    su piu' righe o con graffe annidate non venga troncato."""
    campi, i, n = {}, 0, len(corpo)
    while i < n:
        m = re.compile(r"\s*,?\s*(\w+)\s*=\s*").match(corpo, i)
        if not m:
            break
        nome, i = m.group(1).lower(), m.end()
        if i < n and corpo[i] == "{":
            livello, j = 0, i
            while j < n:
                if corpo[j] == "{":
                    livello += 1
                elif corpo[j] == "}":
                    livello -= 1
                    if livello == 0:
                        break
                j += 1
            valore, i = corpo[i + 1:j], j + 1
        else:
            m2 = re.compile(r"[^,\n]*").match(corpo, i)
            valore, i = m2.group(0), m2.end()
        campi[nome] = re.sub(r"\s+", " ", valore).strip()
    return campi


def leggi_bib(percorso):
    testo = percorso.read_text(encoding="utf-8", errors="replace")
    voci = []
    for blocco in re.split(r"\n@", testo)[1:]:
        m = re.match(r"(\w+)\{([^,]+),", blocco)
        if not m:
            continue
        voci.append((m.group(1).lower(), m.group(2).strip(), leggi_campi(blocco[m.end():])))
    return voci


def da_libreria(registro):
    p = VAULT / "basi" / "ELE_Technical_Library.bib"
    if not p.exists():
        return 0
    n = 0
    for tipo, chiave, c in leggi_bib(p):
        gruppi = {g.strip() for g in c.get("groups", "").split(",") if g.strip()}
        # si escludono soltanto le voci con gruppi tutti estranei: una voce senza gruppo
        # non e' stata classificata, e fra queste ci sono lavori centrali come Rife 1989
        if gruppi and not gruppi & GRUPPI_PERTINENTI:
            continue
        if not gruppi:
            gruppi = {"(senza gruppo)"}
        n += 1
        aggiungi(registro, {
            "citekey": chiave, "titolo": re.sub(r"[{}]", "", c.get("title", "")),
            "autori": re.sub(r"[{}]", "", c.get("author", "")), "anno": c.get("year", ""),
            "sede": re.sub(r"[{}]", "", c.get("journal") or c.get("booktitle", "")),
            "doi": c.get("doi", ""), "tipo": tipo, "gruppi_libreria": sorted(gruppi),
        }, "libreria")
    return n


def da_tesi(registro):
    p = VAULT / "basi" / "tesi-2020-bibliografia.txt"
    if not p.exists():
        return 0
    testo = re.sub(r"\s+", " ", p.read_text(encoding="utf-8", errors="replace"))
    pezzi = re.split(r"\[(\d+)\]\s", testo)
    n = 0
    for i in range(1, len(pezzi) - 1, 2):
        rif = pezzi[i + 1].strip()
        m = re.search(r'"([^"]+?),?"', rif)
        anno = re.findall(r"\b(19\d\d|20\d\d)\b", rif)
        n += 1
        aggiungi(registro, {"citekey": f"tesi2020-{int(pezzi[i]):03d}",
                            "titolo": m.group(1) if m else rif[:120],
                            "riferimento": rif[:400], "anno": anno[-1] if anno else ""}, "tesi2020")
    return n


def titolo_da_file(nome):
    t = Path(nome).stem
    t = re.sub(r"\s*-\s*libgen\.\w+$|libgen\.\w+|_-libgen\.lc", "", t, flags=re.I)
    return re.sub(r"[_]+", " ", t).strip()


DOCUMENTI = {".pdf", ".djvu", ".docx", ".doc", ".pptx", ".ppt", ".epub", ".tex"}


def da_locali(registro):
    """Conta come fonte soltanto un documento: i dati, gli audio e il codice estratti dagli
    archivi restano copie locali ma non sono voci bibliografiche. Un file il cui nome e'
    una chiave della libreria (cosi' la tesi del 2020 nominava i PDF dello studio
    bibliografico) si unisce a quella voce invece di diventarne una nuova."""
    chiavi = {k.lower(): v for k, v in registro["per_chiave"].items()}
    n = 0
    for origine in sorted((VAULT / "fonti-locali").glob("lotto-*-origine.json")):
        lotto = origine.name.split("-origine")[0]
        for v in json.loads(origine.read_text(encoding="utf-8")):
            if v.get("esito") != "indicizzato":
                continue
            nome = Path(v["origine"].replace("\\", "/").split(" :: ")[-1]).name
            if Path(nome).suffix.lower() not in DOCUMENTI:
                continue
            n += 1
            locale = {"lotto": lotto, "file": nome, "sha256": v["sha256"], "byte": v.get("byte")}
            gemella = chiavi.get(Path(nome).stem.lower())
            if gemella is not None:
                gemella["provenienze"] = sorted(set(gemella["provenienze"]) | {"locale"})
                gemella.setdefault("locale", locale)
                continue
            aggiungi(registro, {"citekey": "", "titolo": titolo_da_file(nome), "locale": locale}, "locale")
    return n


def da_proposte(registro):
    p = VAULT / "fonti-proposte.json"
    if not p.exists():
        return 0
    voci = json.loads(p.read_text(encoding="utf-8"))
    for v in voci:
        aggiungi(registro, dict(v), "proposta")
    return len(voci)


def da_scaricate(registro):
    cartella = VAULT / "papers"
    cartella.mkdir(exist_ok=True)
    manifest = []
    for pdf in sorted(cartella.glob("*.pdf")):
        manifest.append({"file": pdf.name, "citekey": pdf.stem, "sha256": sha256(pdf),
                         "byte": pdf.stat().st_size})
        trovata = registro["per_chiave"].get(pdf.stem)
        if trovata is not None:
            trovata["provenienze"] = sorted(set(trovata["provenienze"]) | {"scaricata"})
            trovata["pdf"] = pdf.name
        else:
            aggiungi(registro, {"citekey": pdf.stem, "titolo": pdf.stem, "pdf": pdf.name},
                     "scaricata")
    return manifest


def aggiungi(registro, voce, provenienza):
    chiave_doi = (voce.get("doi") or "").lower()
    chiave_tit = norm_titolo(voce.get("titolo"))
    esistente = None
    if chiave_doi and chiave_doi in registro["per_doi"]:
        esistente = registro["per_doi"][chiave_doi]
    elif len(chiave_tit) > 12 and chiave_tit in registro["per_titolo"]:
        esistente = registro["per_titolo"][chiave_tit]
    elif len(chiave_tit) > 25:
        # confronto approssimato, solo verso le proposte: assorbe i refusi di una libreria
        # di terzi senza rischiare di fondere fra loro voci diverse della libreria stessa
        for t, v in registro["per_titolo"].items():
            if ("proposta" in v["provenienze"] and re.findall(r"\d+", t) == re.findall(r"\d+", chiave_tit)
                    and difflib.SequenceMatcher(None, t, chiave_tit).ratio() > 0.95):
                esistente = v
                break
    if esistente is None:
        voce = dict(voce)
        voce["provenienze"] = [provenienza]
        registro["voci"].append(voce)
        esistente = voce
    else:
        esistente["provenienze"] = sorted(set(esistente["provenienze"]) | {provenienza})
        for k, v in voce.items():
            if k == "citekey":
                continue
            if v and not esistente.get(k):
                esistente[k] = v
        # le chiavi diverse della stessa fonte si conservano tutte: la chiave della
        # proposta resta quella principale, le altre servono a riconoscere un PDF locale
        # nominato con la chiave della libreria o della tesi
        nuova = voce.get("citekey")
        if nuova and nuova != esistente.get("citekey"):
            if not esistente.get("citekey"):
                esistente["citekey"] = nuova
            else:
                alt = esistente.setdefault("chiavi_alternative", [])
                principale, altra = (nuova, esistente["citekey"]) if provenienza == "proposta" else (esistente["citekey"], nuova)
                esistente["citekey"] = principale
                if altra not in alt:
                    alt.append(altra)
                registro["per_chiave"][altra] = esistente
    if chiave_doi:
        registro["per_doi"][chiave_doi] = esistente
    if len(chiave_tit) > 12:
        registro["per_titolo"][chiave_tit] = esistente
    if esistente.get("citekey"):
        registro["per_chiave"][esistente["citekey"]] = esistente


def stato_pdf(v):
    if "scaricata" in v["provenienze"]:
        return "scaricato"
    if "locale" in v["provenienze"]:
        return "su J:"
    return "assente"


def scheda(v):
    url = "\n".join(f"- {u}" for u in v.get("url", [])) or "- nessun collegamento riscontrato"
    return (f"---\ntipo: fonte\ncitekey: {v['citekey']}\nfilone: {v.get('filone', '')}\n"
            f"provenienze: [{', '.join(v['provenienze'])}]\nstato: {v.get('stato_verifica', 'da_verificare')}\n---\n"
            f"# {v.get('titolo', v['citekey'])}\n\n**Riferimento.** {v.get('riferimento', '')}\n\n"
            f"**Collegamenti.**\n{url}\n\n**Perché serve alla tesi.** Da scrivere alla lettura.\n\n"
            f"**Che cosa è stato letto.** Nulla: metadati riscontrati in MS-186, PDF non ancora letto.\n\n"
            f"Torna a [[00-START]] · [[06-Registro-fonti]]\n")


def nota_registro(voci, conteggi, manifest):
    per_prov = {p: sum(1 for v in voci if p in v["provenienze"]) for p in
                ("proposta", "libreria", "tesi2020", "locale", "scaricata")}
    da_scaricare = [v for v in voci if "proposta" in v["provenienze"] and stato_pdf(v) == "assente"]
    righe = "\n".join(f"| [[{v['citekey']}]] | {v.get('filone', '')} | {', '.join(v['provenienze'])} | {stato_pdf(v)} |"
                      for v in sorted((v for v in voci if "proposta" in v["provenienze"] or "scaricata" in v["provenienze"]),
                                      key=lambda x: x["citekey"]))
    return (f"---\ntipo: registro\naggiornato: {date.today().isoformat()}\ngenerato-da: tools/registro-fonti.py\n---\n"
            f"# Registro delle fonti\n\n> Nota generata: non si scrive a mano, si rigenera con `python tools/registro-fonti.py`. "
            f"Il registro pubblico, voce per voce, è `fonti.json`, senza le copie locali dell'SSD privato, "
            f"che stanno nel registro completo locale `_notes/biblioteca/fonti-completo.json`.\n\n"
            f"## Conteggi\n\n| Provenienza | Voci |\n|---|---|\n"
            + "".join(f"| {k} | {n} |\n" for k, n in per_prov.items())
            + f"| totale dopo l'unione | {len(voci)} |\n\n"
            f"Voci lette per provenienza prima dell'unione: proposte {conteggi['proposta']}, libreria nei gruppi pertinenti "
            f"{conteggi['libreria']}, bibliografia della tesi {conteggi['tesi2020']}, copie locali {conteggi['locale']}, "
            f"PDF scaricati {len(manifest)}.\n\n"
            f"## Fonti selezionate per la tesi\n\nSono le proposte dell'agente e i PDF scaricati. Da scaricare: {len(da_scaricare)}.\n\n"
            f"| Scheda | Filone | Provenienze | PDF |\n|---|---|---|---|\n{righe}\n\nTorna a [[00-START]]\n")


def nota_da_scaricare(voci):
    mancanti = sorted((v for v in voci if "proposta" in v["provenienze"] and stato_pdf(v) == "assente"),
                      key=lambda x: (x.get("filone", ""), x["citekey"]))
    righe = []
    for v in mancanti:
        url = " · ".join(v.get("url", [])) or "nessun collegamento riscontrato: cercare il titolo nella E-Library"
        righe.append(f"- `{v['citekey']}.pdf` ({v.get('filone', '')}): {url}")
    return (f"---\ntipo: elenco\naggiornato: {date.today().isoformat()}\ngenerato-da: tools/registro-fonti.py\n---\n"
            f"# Paper da scaricare\n\n> Nota generata. Ogni PDF va salvato in `papers/` con il nome indicato, uguale alla "
            f"chiave; alla corsa successiva di `python tools/registro-fonti.py` la riga sparisce da qui e la fonte "
            f"passa a scaricata. I collegamenti AES vengono da risultati di ricerca: controllare che il titolo "
            f"corrisponda prima di scaricare.\n\nDa scaricare: {len(mancanti)}.\n\n" + "\n".join(righe)
            + "\n\nTorna a [[00-START]]\n")


def scrivi_se_cambia(percorso, testo):
    vecchio = percorso.read_text(encoding="utf-8") if percorso.exists() else ""
    if re.sub(r"aggiornato: \S+", "", vecchio) != re.sub(r"aggiornato: \S+", "", testo):
        percorso.write_text(testo, encoding="utf-8", newline="\n")


def costruisci():
    registro = {"voci": [], "per_doi": {}, "per_titolo": {}, "per_chiave": {}}
    conteggi = {"proposta": da_proposte(registro), "libreria": da_libreria(registro),
                "tesi2020": da_tesi(registro), "locale": da_locali(registro)}
    manifest = da_scaricate(registro)
    voci = sorted(registro["voci"], key=lambda v: (v.get("citekey") or "~" + norm_titolo(v.get("titolo"))))
    for v in voci:
        v["stato_pdf"] = stato_pdf(v)
    return voci, conteggi, manifest


def main():
    ap = argparse.ArgumentParser(description="Registro unico delle fonti del vault di ricerca")
    ap.add_argument("--check", action="store_true", help="esce 1 se il registro su disco non corrisponde")
    a = ap.parse_args()
    voci, conteggi, manifest = costruisci()
    # Il registro tracciato e' pubblico, e le copie locali vengono dall'SSD privato
    # dell'utente: i loro titoli e nomi di file restano nel registro completo locale
    # (PA-028, MS-202). Nel tracciato restano libreria, tesi 2020, proposte e scaricati.
    pubbliche = []
    for v in voci:
        prov = [p for p in v["provenienze"] if p != "locale"]
        if not prov:
            continue
        w = {k: x for k, x in v.items() if k != "locale"}
        w["provenienze"] = prov
        pubbliche.append(w)
    COMPLETO.parent.mkdir(parents=True, exist_ok=True)
    uscite = {
        VAULT / "fonti.json": json.dumps(pubbliche, ensure_ascii=False, indent=1) + "\n",
        COMPLETO: json.dumps(voci, ensure_ascii=False, indent=1) + "\n",
        VAULT / "papers" / "manifest.json": json.dumps(manifest, ensure_ascii=False, indent=1) + "\n",
    }
    nota = VAULT / "06-Registro-fonti.md"
    testo_nota = nota_registro(voci, conteggi, manifest)
    if a.check:
        vecchi = [p.name for p, t in uscite.items() if not p.exists() or p.read_text(encoding="utf-8") != t]
        if vecchi:
            print("registro da rigenerare:", ", ".join(vecchi))
            return 1
        print(f"registro allineato: {len(voci)} voci")
        return 0
    for p, t in uscite.items():
        p.write_text(t, encoding="utf-8", newline="\n")
    scrivi_se_cambia(nota, testo_nota)
    scrivi_se_cambia(VAULT / "04-Paper-da-scaricare.md", nota_da_scaricare(voci))
    (VAULT / "paper").mkdir(exist_ok=True)
    nuove = 0
    for v in voci:
        if ("proposta" in v["provenienze"] or "scaricata" in v["provenienze"]) and v.get("citekey"):
            s = VAULT / "paper" / f"{v['citekey']}.md"
            if not s.exists():
                s.write_text(scheda(v), encoding="utf-8", newline="\n")
                nuove += 1
    print(f"{len(voci)} voci; proposte {conteggi['proposta']}, libreria {conteggi['libreria']}, "
          f"tesi {conteggi['tesi2020']}, locali {conteggi['locale']}, scaricati {len(manifest)}; schede nuove {nuove}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
