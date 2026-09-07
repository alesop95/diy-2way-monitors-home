#!/usr/bin/env python3
"""Misura lo spazio recuperabile sull'SSD esterno e segnala gli indizi di guasto.

Nasce da una domanda pratica, cioe' che cosa si puo' cancellare dall'SSD per liberare
spazio, e da una osservazione fatta guardando la radice del disco: la presenza di piu'
cartelle `FOUND.00x`, che sono il deposito dei frammenti orfani prodotti da `chkdsk`
quando ripara il filesystem. Piu' di una significa piu' di una riparazione, e su un
disco esterno quello e' un segnale da leggere, non solo spazio da liberare.

Lo strumento non cancella nulla e non modifica nulla: misura, classifica e riporta.
La cancellazione resta una decisione dell'utente su materiale personale.

Uso:
    python tools/analisi-ssd-esterno.py
    python tools/analisi-ssd-esterno.py --disco J:
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Cartelle di sistema e di servizio, classificate. Il valore e' la ragione, che viene
# stampata: una classificazione senza motivazione non e' verificabile da chi legge.
SERVIZIO = {
    "$RECYCLE.BIN": "cestino di Windows su questo volume: si svuota dal cestino, non a mano",
    ".Spotlight-V100": "indice di ricerca di macOS, inutile su Windows e su Linux",
    ".TemporaryItems": "file temporanei di macOS",
    ".Trashes": "cestino di macOS",
    ".fseventsd": "registro degli eventi del filesystem di macOS",
    "System Volume Information": "punti di ripristino e indici di Windows, gestiti dal sistema",
    "found.000": "frammenti orfani recuperati da chkdsk",
}

TRASFERITA = "Progetto stanza (software)"


def dimensione(p: Path) -> tuple[int, int]:
    """Byte occupati e numero di file sotto p, senza seguire i collegamenti."""
    byte = 0
    n = 0
    try:
        for x in p.rglob("*"):
            try:
                if x.is_file() and not x.is_symlink():
                    byte += x.stat().st_size
                    n += 1
            except OSError:
                pass
    except OSError:
        pass
    return byte, n


def mib(byte: int) -> str:
    if byte >= 1 << 30:
        return f"{byte / (1 << 30):.1f} GiB"
    return f"{byte / (1 << 20):.0f} MiB"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--disco", default="J:", help="lettera del disco esterno, per esempio J:")
    args = ap.parse_args()

    radice = Path(args.disco + "\\")
    if not radice.is_dir():
        print(f"ERRORE: {radice} non raggiungibile: il disco non e' collegato.", file=sys.stderr)
        print("Ricollegarlo e rilanciare. Nessuna misura e' possibile senza il disco.", file=sys.stderr)
        return 2

    # Cartelle e file sciolti insieme. Una prima versione iterava le sole cartelle, e su
    # questo volume quel difetto nascondeva 45 GiB in quattro file di radice, fra cui due
    # archivi di backup da 20 e 26 GiB: un totale sbagliato per difetto e' peggio di un
    # totale assente, perche' non si vede che manca qualcosa.
    voci = sorted([p for p in radice.iterdir() if p.is_dir() or p.is_file()],
                  key=lambda p: (p.is_file(), p.name.lower()))
    found = [p for p in voci if p.is_dir() and p.name.lower().startswith("found.")]

    recuperabile = 0
    da_guardare = 0

    print(f"Analisi di {radice}\n")
    print(f"{'Voce ([f] = file sciolto)':<48} {'Peso':>10} {'File':>8}  Classificazione")
    print("-" * 108)

    for p in voci:
        if p.is_file():
            byte, n = p.stat().st_size, 1
        else:
            byte, n = dimensione(p)
        nome = ("" if p.is_dir() else "[f] ") + p.name
        chiave = p.name if p.name in SERVIZIO else ("found.000" if p.is_dir() and p.name.lower().startswith("found.") else None)
        if chiave:
            classe = f"servizio: {SERVIZIO[chiave]}"
            recuperabile += byte
        elif p.name == TRASFERITA:
            classe = "TRASFERITA e verificata sulla macchina: cancellabile, si veda PA-001"
            recuperabile += byte
        else:
            classe = "materiale personale: fuori dal perimetro di questo progetto"
            da_guardare += byte
        print(f"{nome[:47]:<48} {mib(byte):>10} {n:>8}  {classe}")

    print("-" * 108)
    print(f"\nRecuperabile senza perdere nulla di utile: {mib(recuperabile)}")
    print(f"Materiale personale, non toccato:          {mib(da_guardare)}")

    if len(found) >= 2:
        print(f"\n{'=' * 76}")
        print(f"SEGNALE DA LEGGERE: {len(found)} cartelle FOUND sul volume")
        print(f"{'=' * 76}")
        print("Ogni cartella FOUND.00x e' il deposito dei frammenti orfani che `chkdsk`")
        print("produce quando ripara il filesystem. Averne piu' di una significa che il")
        print("filesystem e' stato riparato piu' volte, e le date delle cartelle dicono")
        print("quando. Su un disco esterno le cause tipiche sono due, e vanno distinte:")
        print("la rimozione senza espulsione sicura, che e' un problema di abitudine, e")
        print("un difetto del supporto o del suo controllore, che e' un problema di")
        print("hardware. Lo spazio si libera cancellandole, ma la causa resta.")
        print("\nDate delle cartelle, dalla piu' vecchia:")
        for p in sorted(found, key=lambda x: x.stat().st_mtime):
            import datetime
            d = datetime.datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d")
            b, n = dimensione(p)
            print(f"  {d}  {p.name:<12} {mib(b):>10} {n:>6} file")
        print("\nIl controllo che chiude la questione e' la lettura SMART del disco esterno,")
        print("con `smartctl` da Linux oppure CrystalDiskInfo da Windows. Se il supporto e'")
        print("sano, la causa e' l'espulsione; se non lo e', quel disco non e' il posto")
        print("dove tenere l'unica copia di qualcosa.")

    print("\nQuesto strumento non cancella nulla. Le cancellazioni restano dell'utente.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
