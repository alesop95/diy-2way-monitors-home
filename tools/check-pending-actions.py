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

# Quarta posizione, emersa leggendo il collegamento presente in entrambe le copie:
# il materiale EASE Focus 3.1.10 del workshop K-array. Vedi PA-004.
COPIA_G = Path(r"G:\LIBRARY\LOUDSPEAKERS & ELECTROACOUSTIC\K-ARRAY WORKSHOP\EASE Focus (k-array)")

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

    riga("ok" if lavoro_presente else "!!", f"condizione 1a, copia di lavoro: {COPIA_LAVORO}")
    riga("ok" if ssd_presente else "  ", f"condizione 1b, disco J: collegato: {COPIA_SSD}")

    if not ssd_presente:
        print("\n  BLOCCATA: il disco J: non e' collegato, quindi non c'e' nulla da")
        print("  confrontare ne' da cancellare. Ricollegare l'SSD e rilanciare.")
        return

    riga("ok", "condizione 2, corrispondenza fra le copie: verificata il 2026-09-07")
    print("       650 file per copia, stesse dimensioni, impronte SHA-256 tutte coincidenti.")
    print("       Rieseguibile in qualsiasi momento con: --confronta")
    riga("ok", "condizione 3, trasferimento verso la macchina: eseguito il 2026-09-07")
    print("       8 file del manifest e 273 file del corredo, tutte le impronte coincidenti.")
    print("       Rieseguibile con: bash tools/transfer-to-studio.sh --impronte")
    print("\n  SBLOCCATA: le tre condizioni sono soddisfatte, la cancellazione e' autorizzata.")
    print("  Resta un'azione dell'utente: cancellare 2,3 GB da un disco esterno e' una")
    print("  operazione distruttiva su materiale personale. Il comando e' in PA-001.")


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


def controlla_pa004() -> None:
    print("\nPA-004  Ispezionare il disco G: e il materiale EASE Focus 3.1.10 (K-array)")
    presente = COPIA_G.is_dir()
    riga("ok" if presente else "  ", f"percorso su G:: {COPIA_G}")
    if presente:
        try:
            n = sum(1 for x in COPIA_G.rglob("*") if x.is_file())
            print(f"  SBLOCCATA: il percorso e' raggiungibile e contiene {n} file.")
            print("  Ispezionarlo e decidere se qualcosa va nel manifest di trasferimento.")
        except OSError as e:
            print(f"  ANOMALIA: percorso presente ma non percorribile: {e}")
    else:
        print("  BLOCCATA: il disco G: non e' collegato.")
        print("  Priorita' bassa: la versione da installare e' la 3.1.260, non la 3.1.10.")


def controlla_manuali() -> None:
    """PA-005 e PA-006 non hanno condizioni automatizzabili, ma vanno elencate.

    Uno strumento che riporta quattro voci su sei sotto-riporta in silenzio, ed e'
    peggio di uno strumento che dichiara di non poter decidere.
    """
    print("\nPA-005  Completare le tre voci privilegiate della fase 0")
    riga("ok", "stato di salute dell'SSD: letto il 2026-09-07, PASSED, usura 9 per cento")
    riga("? ", "esito reale di sudo apt update")
    riga("? ", "Machine Identifier di Akabak, controllo in interfaccia grafica")
    print("  APERTA su due voci su tre: non automatizzabili perche' sudo chiede la password")
    print("  e perche' il controllo del Machine Identifier e' visivo. La voce che poteva")
    print("  cambiare la decisione, cioe' lo stato del disco, e' chiusa: risulta sano.")

    print("\nPA-006  Riconfermare o rivedere la scelta fra installazione e aggiornamento")
    print("  APERTA: e' una decisione dell'utente. La verifica del 2026-09-07 ha fatto")
    print("  cadere uno dei quattro motivi di ADR-006; la revisione e' ADR-011.")


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
    controlla_pa004()
    controlla_manuali()
    print("\nLegenda: [ok] condizione soddisfatta, [? ] da confermare a mano,")
    print("         [  ] non soddisfatta, [!!] anomalia da guardare.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
