#!/usr/bin/env python3
"""Converte il grassetto usato nella prosa in corsivo, come prescrive lo stile del template.

Perche' serve. La sezione 8 di .claude/PROJECT-SYSTEM.md, che discende dal template
template-claude-developing, prescrive che nella prosa non si usino elenchi puntati, emoji
ne' grassetto, e che i termini chiave densi si marchino in corsivo. La convenzione era
dichiarata e non verificata, ed e' esattamente la condizione in cui una convenzione
deriva: al 2026-09-09 la documentazione propria del progetto conteneva quasi trecento
marcature in grassetto nella prosa. Come per gli accenti e per i trattini, l'attuazione
meccanica e' l'unico modo per cui la regola vale invece di essere ricordata.

Che cosa NON tocca, e sono tre esclusioni sostanziali e non prudenziali.

Il contenuto dei blocchi recintati e dei blocchi indentati resta intatto, per lo stesso
contratto di md-unwrap: dentro un blocco di codice il grassetto non e' formattazione ma
testo, e riscriverlo cambierebbe un comando.

Le righe di tabella restano intatte, perche' una cella non e' prosa. Il divieto della
sezione 8 riguarda il discorso, mentre in una tabella il grassetto e' segnaletica: nella
scheda di reinstallazione la parola che dice di non formattare una partizione e' in
grassetto di proposito, e togliere quel risalto peggiorerebbe un documento di sicurezza.

Le keyword di codice dentro i blocchi sintattici vanno in grassetto per prescrizione
della stessa sezione 8, e stando dentro blocchi sono gia' coperte dalla prima esclusione.

Cosa NON garantisce. Non riconosce il grassetto annidato in strutture esotiche, e in
generale non sostituisce la lettura: e' uno strumento di normalizzazione, e il suo esito
va guardato in diff prima di committare, come per la catena tipografica.

Uso:
    python tools/fix-emphasis.py --check <percorso>   segnala senza scrivere
    python tools/fix-emphasis.py <percorso>           converte
    python tools/fix-emphasis.py --dettaglio <perc>   elenca ogni occorrenza convertita

Esce con codice 1 se in modalita' --check trova almeno una occorrenza, 0 altrimenti.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# I modelli sotto .claude/templates/ sono copie del template di origine: riscriverli qui
# allargherebbe la divergenza che PA-003 esiste per chiudere. Le fixture di md-unwrap
# sono materiale di prova e vanno lasciate come sono.
CARTELLE_ESCLUSE = {".git", "_notes", "__pycache__", "node_modules", "fixtures", "templates"}

APERTURA_RECINTO = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
# Una riga di tabella comincia con una barra verticale, oppure e' la riga dei separatori.
RIGA_TABELLA = re.compile(r"^\s{0,3}\|")
SEPARATORE_TABELLA = re.compile(r"^\s{0,3}\|?[\s:|-]+\|[\s:|-]*$")
# Blocco indentato: quattro spazi o un tab, fuori da un elenco. Approssimazione
# volutamente prudente, che preferisce non toccare a toccare per errore.
BLOCCO_INDENTATO = re.compile(r"^(?: {4,}|\t)\S")

# Grassetto con doppio asterisco. Si richiede contenuto non vuoto e senza asterischi,
# cosi' da non catturare marcature annidate o triple, che vanno guardate a mano.
GRASSETTO = re.compile(r"\*\*(?=\S)([^*\n]+?)(?<=\S)\*\*")


def converti_riga(riga: str) -> tuple[str, int]:
    """Converte il grassetto in corsivo su una riga di prosa. Ritorna riga e conteggio."""
    nuova, n = GRASSETTO.subn(r"*\1*", riga)
    return nuova, n


def elabora(testo: str) -> tuple[str, list[tuple[int, str, str]]]:
    """Percorre il file riga per riga rispettando le esclusioni.

    Ritorna il testo nuovo e l'elenco delle conversioni come (numero riga, prima, dopo).
    """
    righe = testo.split("\n")
    dentro_recinto = False
    recinto_marcatore = ""
    conversioni: list[tuple[int, str, str]] = []

    for i, riga in enumerate(righe):
        apertura = APERTURA_RECINTO.match(riga)
        if dentro_recinto:
            # Si esce dal recinto solo con lo stesso tipo di marcatore che lo ha aperto.
            if apertura and apertura.group(1)[0] == recinto_marcatore[0]:
                dentro_recinto = False
                recinto_marcatore = ""
            continue
        if apertura:
            dentro_recinto = True
            recinto_marcatore = apertura.group(1)
            continue
        if RIGA_TABELLA.match(riga) or SEPARATORE_TABELLA.match(riga):
            continue
        if BLOCCO_INDENTATO.match(riga):
            continue
        nuova, n = converti_riga(riga)
        if n:
            conversioni.append((i + 1, riga, nuova))
            righe[i] = nuova

    return "\n".join(righe), conversioni


def candidati(radice: Path):
    if radice.is_file():
        yield radice
        return
    for p in sorted(radice.rglob("*.md")):
        if any(parte in CARTELLE_ESCLUSE for parte in p.parts):
            continue
        yield p


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("percorsi", nargs="*", default=["."], type=Path)
    ap.add_argument("--check", action="store_true", help="segnala senza scrivere")
    ap.add_argument("--dettaglio", action="store_true", help="elenca ogni conversione")
    args = ap.parse_args()

    esaminati = 0
    modificati = 0
    totale = 0

    for percorso in args.percorsi:
        for f in candidati(Path(percorso)):
            esaminati += 1
            # newline="" conserva CRLF, LF e BOM esattamente come stanno sul disco,
            # perche' la convenzione prescrive di non toccare la fine riga di un file.
            grezzo = f.read_text(encoding="utf-8", newline="")
            crlf = "\r\n" in grezzo
            testo = grezzo.replace("\r\n", "\n") if crlf else grezzo

            nuovo, conversioni = elabora(testo)
            if not conversioni:
                continue

            modificati += 1
            totale += len(conversioni)
            print(f"  {len(conversioni):3d}  {f}")
            if args.dettaglio:
                for numero, prima, dopo in conversioni:
                    print(f"       riga {numero}")
                    print(f"         - {prima.strip()[:150]}")
                    print(f"         + {dopo.strip()[:150]}")

            if not args.check:
                if crlf:
                    nuovo = nuovo.replace("\n", "\r\n")
                f.write_text(nuovo, encoding="utf-8", newline="")

    verbo = "da convertire" if args.check else "convertite"
    print(f"{esaminati} file esaminati, {modificati} con grassetto in prosa, {totale} occorrenze {verbo}")
    if totale and args.check:
        print("Lo stile del template vieta il grassetto nella prosa: sezione 8 di")
        print(".claude/PROJECT-SYSTEM.md. Tabelle e blocchi di codice non sono toccati.")
    return 1 if (totale and args.check) else 0


if __name__ == "__main__":
    sys.exit(main())
