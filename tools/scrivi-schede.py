"""Scrive le schede di fonte di livello 2 (ADR-041) dalle risposte JSON degli agenti, senza modello.

Nato con MS-214 per ridurre i turni degli agenti economici: l'agente legge un solo pacchetto
di estratti preparato da tools/estratti-lotto.py --pacchetti e scrive un solo file JSON con i
soli campi di giudizio. Questo strumento ricava da elenco.json i campi meccanici, cioe' nome,
parole, impronta e cache, calcola lo slug, tiene nei collegamenti le sole pagine di concetto
che esistono davvero, e scrive le schede nel formato di knowledge/WIKI-SCHEMA.md con fini
riga LF in modalita' binaria.

Ogni file pacchetto-NN.json e' una lista di oggetti con i campi:
    estratto (es. "003.md"), titolo, tipo, autori_anno, contenuto, il campo
    "utile" con il giudizio di utilità (alta, media, bassa o nessuna; accettata anche la chiave dei
    lotti di MS-214), motivo, sezioni, collegamenti (lista di nomi di
    pagine di concetto), personale (vero se il documento sembra personale).

Uso: python tools/scrivi-schede.py _notes/lotti/lotto-L2-03
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
SCHEDE = RADICE / "knowledge" / "wiki" / "schede"
CONCETTI = RADICE / "knowledge" / "wiki" / "concepts"
AVVISO = ("> Scheda di livello 2 (ADR-041): scritta dal modello economico sullo scheletro e sulle prime pagine, "
          "non è una lettura completa e i conti non sono verificati. Non fonda affermazioni della tesi: indica dove leggere.")
UTILITA = {"alta", "media", "bassa", "nessuna"}


def slug(nome):
    s = unicodedata.normalize("NFKD", Path(nome).stem).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:60] or "documento"


def main():
    lotto = Path(sys.argv[1])
    elenco = {e["estratto"]: e for e in json.loads((lotto / "elenco.json").read_text(encoding="utf-8"))}
    esistenti = {p.stem for p in CONCETTI.glob("*.md")}
    SCHEDE.mkdir(parents=True, exist_ok=True)
    scritte, personali, problemi = 0, [], []
    for f in sorted(lotto.glob("pacchetto-*.json")):
        for r in json.loads(f.read_text(encoding="utf-8")):
            e = elenco.get(r.get("estratto", ""))
            if not e:
                problemi.append(f"{f.name}: estratto sconosciuto {r.get('estratto')}")
                continue
            if r.get("personale"):
                personali.append(e["estratto"])
                continue
            u = str(r.get("utile", r.get("utilita", ""))).strip().lower()
            if u not in UTILITA:
                problemi.append(f"{e['estratto']}: utilita' fuori formato '{u}'")
            link = [c for c in r.get("collegamenti") or [] if c in esistenti]
            collegamenti = ", ".join(f"[{c}](../concepts/{c}.md)" for c in link) or "nessuno"
            base = s = slug(e["nome"])
            k = 2
            while (SCHEDE / f"{s}.md").exists() and f"Impronta: {e['impronta'][:12]}" not in (SCHEDE / f"{s}.md").read_text(encoding="utf-8"):
                s, k = f"{base}-{k}", k + 1
            testo = (f"# {r.get('titolo') or Path(e['nome']).stem}\n\n{AVVISO}\n\n"
                     f"Documento: {e['nome']}. Parole: {e['parole']}. Impronta: {e['impronta'][:12]}. Cache: {e['cache']}.\n\n"
                     f"Tipo: {r.get('tipo', 'altro')}. Autori e anno: {r.get('autori_anno') or 'non ricavabili dall estratto'}.\n\n"
                     f"Contenuto: {r.get('contenuto', '').strip()}\n\n"
                     f"Utilità per la tesi: {u}, {r.get('motivo', '').strip()}\n\n"
                     f"Sezioni da leggere: {r.get('sezioni') or 'nessuna in particolare'}.\n\n"
                     f"Collegamenti: {collegamenti}.\n")
            (SCHEDE / f"{s}.md").write_bytes(testo.replace("\r\n", "\n").encode("utf-8"))
            scritte += 1
    # Gli agenti economici scrivono a volte trattini lunghi o accenti mancanti: la catena
    # tipografica del progetto li sistema sulle sole schede, che sono Markdown (MS-216).
    import subprocess
    for strumento in ("fix-dashes.py", "fix-accents.py", "fix-missing-accents.py"):
        subprocess.run([sys.executable, str(RADICE / "tools" / strumento), str(SCHEDE)], capture_output=True)
    print(f"schede scritte {scritte}; personali saltati {len(personali)} {personali}; problemi {len(problemi)}")
    for p in problemi:
        print("  " + p)


if __name__ == "__main__":
    main()
