#!/usr/bin/env python3
"""Sincronizza il blocco documentale dell'ambiente fra i due progetti che lo condividono.

Il blocco `docs/10-ambiente/` descrive la macchina Ubuntu Studio e lo strato Wine che
ci gira sopra. La stessa macchina serve alla progettazione elettroacustica e all'home
recording, quindi il blocco vive in due repository. La copia canonica sta in
`diy-2way-monitors-home`; questo strumento la replica nel gemello senza toccare nulla
d'altro, e in modalità `--check` si limita a segnalare la deriva senza scrivere.

La direzione e' deliberatamente unidirezionale. Una sincronizzazione bidirezionale
richiederebbe una risoluzione dei conflitti che a due copie non vale il costo: si
modifica la canonica e si propaga, mai il contrario.

Uso:
    python tools/sync-ambiente.py --check      segnala la deriva, esce 1 se la trova
    python tools/sync-ambiente.py              propaga la canonica sul gemello
    python tools/sync-ambiente.py --gemello <percorso>
"""

from __future__ import annotations

import argparse
import filecmp
import hashlib
import shutil
import sys
from pathlib import Path

BLOCCO = Path("docs") / "10-ambiente"
GEMELLO_DEFAULT = Path("E:/home-recording-training-mixing-setup")

INTESTAZIONE_COPIA = """<!-- COPIA SINCRONIZZATA. Non modificare qui.
     La copia canonica di questo blocco vive in diy-2way-monitors-home/docs/10-ambiente/
     e si propaga con `python tools/sync-ambiente.py` da quel progetto. -->

"""


def impronta(percorso: Path) -> str:
    return hashlib.sha256(percorso.read_bytes()).hexdigest()


def file_del_blocco(radice: Path) -> list[Path]:
    sorgente = radice / BLOCCO
    if not sorgente.is_dir():
        return []
    return sorted(p for p in sorgente.rglob("*.md") if p.is_file())


def contenuto_atteso(percorso: Path) -> bytes:
    """Il gemello riceve il file con l'intestazione che ne dichiara la provenienza."""
    grezzo = percorso.read_bytes()
    bom = b"\xef\xbb\xbf"
    if grezzo.startswith(bom):
        return bom + INTESTAZIONE_COPIA.encode("utf-8") + grezzo[len(bom):]
    return INTESTAZIONE_COPIA.encode("utf-8") + grezzo


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="segnala la deriva senza scrivere")
    ap.add_argument("--gemello", type=Path, default=GEMELLO_DEFAULT, help="radice del progetto gemello")
    args = ap.parse_args()

    canonica = Path(__file__).resolve().parent.parent
    gemello = args.gemello.resolve() if args.gemello.exists() else args.gemello

    if not (canonica / BLOCCO).is_dir():
        print(f"ERRORE: blocco canonico non trovato: {canonica / BLOCCO}", file=sys.stderr)
        return 2
    if not gemello.is_dir():
        print(f"ERRORE: progetto gemello non trovato: {gemello}", file=sys.stderr)
        return 2

    sorgenti = file_del_blocco(canonica)
    if not sorgenti:
        print(f"ERRORE: nessun file .md nel blocco canonico", file=sys.stderr)
        return 2

    destinazione_blocco = gemello / BLOCCO
    da_aggiornare: list[tuple[Path, Path]] = []
    invariati = 0

    for sorgente in sorgenti:
        relativo = sorgente.relative_to(canonica / BLOCCO)
        destinazione = destinazione_blocco / relativo
        atteso = contenuto_atteso(sorgente)
        if destinazione.is_file() and destinazione.read_bytes() == atteso:
            invariati += 1
        else:
            da_aggiornare.append((sorgente, destinazione))

    # File presenti solo nel gemello: sono residui di una versione precedente del blocco.
    orfani: list[Path] = []
    if destinazione_blocco.is_dir():
        attesi = {(destinazione_blocco / s.relative_to(canonica / BLOCCO)).resolve()
                  for s in sorgenti}
        for esistente in sorted(destinazione_blocco.rglob("*.md")):
            if esistente.resolve() not in attesi:
                orfani.append(esistente)

    print(f"blocco canonico: {canonica / BLOCCO}")
    print(f"gemello:         {destinazione_blocco}")
    print(f"{len(sorgenti)} file nel blocco, {invariati} allineati, {len(da_aggiornare)} da propagare, {len(orfani)} orfani nel gemello")

    for _, destinazione in da_aggiornare:
        print(f"  da propagare: {destinazione.relative_to(gemello)}")
    for orfano in orfani:
        print(f"  orfano (non rimosso automaticamente): {orfano.relative_to(gemello)}")

    if args.check:
        if da_aggiornare or orfani:
            print("deriva rilevata: rilanciare senza --check per propagare")
            return 1
        print("nessuna deriva")
        return 0

    for sorgente, destinazione in da_aggiornare:
        destinazione.parent.mkdir(parents=True, exist_ok=True)
        destinazione.write_bytes(contenuto_atteso(sorgente))
        print(f"  scritto: {destinazione.relative_to(gemello)}")

    if orfani:
        print("gli orfani non vengono rimossi: se sono residui, cancellarli a mano dopo averli guardati")

    print(f"propagati {len(da_aggiornare)} file")
    return 0


if __name__ == "__main__":
    sys.exit(main())
