#!/usr/bin/env python3
"""Verifica quali azioni differite di docs/PENDING-ACTIONS.md sono diventate eseguibili.

Un promemoria che vive solo in una conversazione e' perduto. Questo strumento legge le
condizioni verificabili in automatico e dice quali azioni sono sbloccate, cosi' che il
controllo sia un comando invece di un ricordo. Le condizioni non verificabili da qui,
per esempio l'esito di un trasferimento su una macchina remota, restano dichiarate come
da confermare a mano.

Non cancella e non modifica nulla: e' uno strumento di sola lettura e di segnalazione.

Uso:
    python tools/check-pending-actions.py              stato delle azioni differite
    python tools/check-pending-actions.py --confronta  confronta le due copie del corredo
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

# I due luoghi in cui vive il corredo software del progetto stanza.
COPIA_LAVORO = Path(r"C:\Users\Utente\Desktop\Progetto stanza (software)")
COPIA_SSD = Path(r"J:\Progetto stanza (software)")

# Sottoinsieme legittimo, quello che va sulla macchina Ubuntu Studio. I percorsi sono
# relativi alla radice del corredo. Vedi docs/10-ambiente/wine-corredo-progetto-stanza.md
SOTTOINSIEME_UTILE = [
    Path("DIY Loudspeaker Pack Softwares/VituixCAD_setup.exe"),
    Path("DIY Loudspeaker Pack Softwares/Arta"),
    Path("Room acoustics/EEASE Focus/EASE_Focus_v3.1.260"),
    Path("Room acoustics/EEASE Focus/EASE_Focus_3_GLL_Database_2016_10_11"),
    Path("Room acoustics/Ramsete27b - room acoustics"),
]


def impronta(percorso: Path, blocco: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with percorso.open("rb") as f:
        for pezzo in iter(lambda: f.read(blocco), b""):
            h.update(pezzo)
    return h.hexdigest()


def mappa_impronte(radice: Path) -> dict[str, str]:
    """Impronta di ogni file sotto radice, indicizzata dal percorso relativo."""
    esito: dict[str, str] = {}
    for p in sorted(radice.rglob("*")):
        if p.is_file() and not p.is_symlink():
            try:
                esito[str(p.relative_to(radice)).replace("\\", "/")] = impronta(p)
            except OSError as e:
                esito[str(p.relative_to(radice)).replace("\\", "/")] = f"ERRORE: {e}"
    return esito


def riga(stato: str, testo: str) -> None:
    print(f"  [{stato}] {testo}")


def controlla_pa001() -> None:
    print("\nPA-001  Cancellare la copia del corredo su SSD esterno")

    ssd_presente = COPIA_SSD.is_dir()
    lavoro_presente = COPIA_LAVORO.is_dir()

    riga("ok" if lavoro_presente else "!!", f"copia di lavoro: {COPIA_LAVORO}")
    riga("ok" if ssd_presente else "  ", f"copia su SSD:    {COPIA_SSD}")

    if not ssd_presente:
        print("\n  BLOCCATA: il disco J: non e' collegato, quindi non c'e' nulla da")
        print("  confrontare ne' da cancellare. Ricollegare l'SSD e rilanciare.")
        return

    print("\n  Il disco e' collegato. Restano due condizioni da confermare a mano,")
    print("  perche' questo strumento non puo' verificarle:")
    riga("? ", "il trasferimento verso la macchina Ubuntu Studio e' completato")
    riga("? ", "le impronte sulla destinazione coincidono (docs/TRANSFER-MANIFEST.md)")
    print("\n  Poi il confronto fra le due copie, con: --confronta")
    print("  Non cancellare prima che il confronto sia andato a buon fine.")


def controlla_pa002() -> None:
    print("\nPA-002  Verificare lo stato di licenza di Ramsete 27b")
    ramsete = COPIA_LAVORO / "Room acoustics" / "Ramsete27b - room acoustics"
    riga("ok" if ramsete.is_dir() else "  ", f"materiale presente: {ramsete.name}")
    print("  APERTA: verifica da fare sul sito del produttore, non automatizzabile.")
    print("  Priorita' bassa: il ruolo di Ramsete e' coperto da Akabak.")


def controlla_pa003() -> None:
    print("\nPA-003  Propagare al template le quattro correzioni trovate")
    template = Path(r"E:\template-claude-developing")
    riga("ok" if template.is_dir() else "  ", f"template raggiungibile: {template}")
    print("  APERTA: e' una decisione dell'utente su un altro repository.")


def confronta() -> int:
    if not COPIA_SSD.is_dir():
        print(f"ERRORE: {COPIA_SSD} non trovata: il disco J: non e' collegato.", file=sys.stderr)
        return 2
    if not COPIA_LAVORO.is_dir():
        print(f"ERRORE: {COPIA_LAVORO} non trovata.", file=sys.stderr)
        return 2

    print("Confronto per impronta SHA-256 fra le due copie del corredo.")
    print("Puo' richiedere qualche minuto: sono alcuni gigabyte.\n")

    a = mappa_impronte(COPIA_LAVORO)
    b = mappa_impronte(COPIA_SSD)

    solo_lavoro = sorted(set(a) - set(b))
    solo_ssd = sorted(set(b) - set(a))
    diversi = sorted(k for k in set(a) & set(b) if a[k] != b[k])
    uguali = len(set(a) & set(b)) - len(diversi)

    print(f"copia di lavoro: {len(a)} file")
    print(f"copia su SSD:    {len(b)} file")
    print(f"identici:        {uguali}")
    print(f"solo su Desktop: {len(solo_lavoro)}")
    print(f"solo su SSD:     {len(solo_ssd)}")
    print(f"diversi:         {len(diversi)}")

    for etichetta, elenco in (("solo su Desktop", solo_lavoro),
                              ("solo su SSD", solo_ssd),
                              ("contenuto diverso", diversi)):
        if elenco:
            print(f"\n{etichetta}:")
            for k in elenco[:40]:
                print(f"  {k}")
            if len(elenco) > 40:
                print(f"  ... e altri {len(elenco) - 40}")

    if solo_ssd or diversi:
        print("\nESITO: le due copie NON sono identiche.")
        print("I file presenti solo su SSD, o diversi, non sono duplicati: portarli via")
        print("prima di cancellare, oppure limitare la cancellazione a cio' che e'")
        print("effettivamente duplicato. Non cancellare l'intera cartella.")
        return 1

    print("\nESITO: ogni file dell'SSD ha un gemello identico sul Desktop.")
    print("La cancellazione su SSD e' sicura dal punto di vista della ridondanza,")
    print("purche' le altre due condizioni di PA-001 siano confermate.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--confronta", action="store_true",
                    help="confronta per impronta le due copie del corredo software")
    args = ap.parse_args()

    if args.confronta:
        return confronta()

    print("Azioni differite: stato delle condizioni di sblocco")
    print("Dettaglio e criteri di completamento in docs/PENDING-ACTIONS.md")
    controlla_pa001()
    controlla_pa002()
    controlla_pa003()
    print("\nLegenda: [ok] condizione soddisfatta, [? ] da confermare a mano,")
    print("         [  ] non soddisfatta, [!!] anomalia da guardare.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
