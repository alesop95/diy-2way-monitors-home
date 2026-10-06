"""Riconosce i documenti personali dell'utente dal solo percorso, prima di aprirli.

Regola .claude/rules/documenti-personali.md, ADR-042: i documenti personali non si leggono,
non si convertono e non si sintetizzano a nessun livello senza richiesta espressa. Gli schemi
vivono nel file locale _notes/privacy/esclusi-personali.txt, ignorato da git perche' gli schemi
stessi possono rivelare dati personali: un'espressione regolare per riga, confrontata senza
distinzione di maiuscole con il percorso completo; le righe vuote e quelle che iniziano con #
si ignorano. Se il file manca, lo strumento che chiama si ferma invece di procedere senza filtro.
"""
import re
from pathlib import Path

ELENCO = Path(__file__).resolve().parent.parent / "_notes" / "privacy" / "esclusi-personali.txt"


def carica_schemi(percorso=ELENCO):
    if not percorso.exists():
        raise SystemExit(f"manca {percorso}: senza schemi di esclusione dei documenti personali non si procede (ADR-042)")
    righe = percorso.read_text(encoding="utf-8").splitlines()
    return [re.compile(r, re.IGNORECASE) for r in (x.strip() for x in righe) if r and not r.startswith("#")]


def e_personale(posizione, schemi):
    return bool(posizione) and any(s.search(posizione) for s in schemi)
