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

# Copia di sicurezza di /home, condizione di sblocco di PA-007. Si cercano piu' posizioni
# invece di una sola perche' l'archivio e' un file che l'utente puo' spostare: la prima
# versione di questo controllo inchiodava il percorso su E: e lo spostamento sul Desktop
# lo avrebbe fatto dichiarare assente, riportando PA-007 a bloccata per un motivo falso.
# Il nome del file e' l'invariante, non la cartella che lo contiene.
BACKUP_HOME_NOME = "home-alesop95-2026-09-07.tar"
BACKUP_HOME_CANDIDATI = [
    Path(r"C:\Users\Utente\Desktop\_backup-ubuntu-studio") / BACKUP_HOME_NOME,
    Path(r"E:\_backup-ubuntu-studio") / BACKUP_HOME_NOME,
]
BACKUP_HOME_BYTE = 4_662_927_360


def trova_backup_home() -> Path | None:
    """Prima posizione in cui l'archivio di /home risulta presente, o None."""
    for p in BACKUP_HOME_CANDIDATI:
        if p.is_file():
            return p
    return None

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

    # Tre stati distinti, e confonderne due e' stato un difetto reale di questo
    # strumento: il disco assente e la cartella gia' cancellata producono entrambi
    # "cartella non trovata", ma il primo e' un ostacolo e il secondo e' l'obiettivo
    # raggiunto. Si guarda quindi la radice del disco separatamente dalla cartella.
    disco_presente = COPIA_SSD.parent.is_dir()
    cartella_presente = COPIA_SSD.is_dir()
    lavoro_presente = COPIA_LAVORO.is_dir()

    if disco_presente and not cartella_presente:
        riga("ok", "COMPIUTA: la cartella non e' piu' su J:, con il disco collegato")
        riga("ok" if lavoro_presente else "!!",
             f"copia sul Desktop, intatta: {COPIA_LAVORO}")
        riga("ok", "copia sulla macchina, verificata: ~/electroacoustics, 281 file")
        print("\n  L'obiettivo della voce e' raggiunto: quella copia non c'e' piu' e le")
        print("  altre due ci sono. Nessun dato perduto. Il momento esatto e il modo della")
        print("  cancellazione non sono accertati, e la voce in PA-001 lo dichiara.")
        return

    riga("ok" if lavoro_presente else "!!", f"condizione 1a, copia di lavoro: {COPIA_LAVORO}")
    riga("ok" if disco_presente else "  ", f"condizione 1b, disco J: collegato: {COPIA_SSD.parent}")
    ssd_presente = cartella_presente

    # La condizione sul disco collegato e' transitoria: si soddisfa e si perde a ogni
    # scollegamento. Le altre due sono fatti accertati una volta per sempre. Una prima
    # versione usciva subito quando il disco era assente, e questo nascondeva le due
    # condizioni permanenti facendo sembrare la voce piu' lontana dallo sblocco di
    # quanto sia: le si mostra sempre, e l'assenza del disco resta l'unico ostacolo.
    riga("ok", "condizione 2, corrispondenza fra le copie: verificata il 2026-09-07")
    print("       650 file per copia, stesse dimensioni, impronte SHA-256 tutte coincidenti.")
    print("       Rieseguibile in qualsiasi momento con: --confronta")
    riga("ok", "condizione 3, trasferimento verso la macchina: eseguito il 2026-09-07")
    print("       8 file del manifest e 273 file del corredo, tutte le impronte coincidenti.")
    print("       Rieseguibile con: bash tools/transfer-to-studio.sh --impronte")
    if ssd_presente:
        print("\n  SBLOCCATA: le tre condizioni sono soddisfatte, la cancellazione e' autorizzata.")
        print("  Resta un'azione dell'utente: cancellare 2,3 GB da un disco esterno e' una")
        print("  operazione distruttiva su materiale personale. Il comando e' in PA-001.")
    else:
        print("\n  IN ATTESA DEL DISCO. Le due condizioni di merito sono soddisfatte in modo")
        print("  permanente: il materiale e' sulla macchina e verificato. Manca solo che")
        print("  J: sia collegato, che e' una condizione transitoria. Ricollegarlo e rilanciare.")


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
    # La lettera non identifica il disco: Windows assegna la prima libera, quindi la
    # stessa lettera indica dispositivi diversi in momenti diversi. Il 2026-09-08 G:
    # era una chiavetta di installazione. Il criterio di riconoscimento e' il percorso
    # completo qui sopra, non la lettera: se la lettera esiste ma il percorso no, non
    # si e' trovato il disco sbagliato, semplicemente non c'e'. Vedi PA-004.
    if not presente and COPIA_G.drive and Path(COPIA_G.drive + "\\").is_dir():
        riga("  ", f"attenzione: la lettera {COPIA_G.drive} e' occupata da un altro volume")
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
    riga("ok", "Machine Identifier: letto in interfaccia il 2026-09-07, coincide con _notes")
    riga("? ", "esito reale di sudo apt update")
    print("  APERTA su una voce su tre, e quella voce e' resa irrilevante da ADR-013:")
    print("  su un sistema che verra' azzerato l'esito di apt update non decide nulla.")
    print("  Le due voci che contavano sono chiuse: disco sano, licenza confermata valida.")

    print("\nPA-007  Cancellare la copia del corredo sul Desktop della postazione")
    if COPIA_LAVORO.is_dir():
        n = sum(1 for x in COPIA_LAVORO.rglob("*") if x.is_file())
        riga("  ", f"presente: {n} file")
        backup = trova_backup_home()
        if backup is not None:
            riga("ok", f"backup di /home presente: {backup.stat().st_size >> 30} GiB, verificato")
            riga("  ", f"posizione: {backup.parent}")
            if backup.stat().st_size != BACKUP_HOME_BYTE:
                riga("!!", f"dimensione diversa da quella registrata ({BACKUP_HOME_BYTE} byte):")
                print("  l'archivio e' stato rigenerato o e' incompleto, la verifica di MS-049")
                print("  non vale piu' per questo file e va rifatta prima di cancellare.")
            print("  SBLOCCATA: il backup di /home su supporto diverso esiste ed e' verificato,")
            print("  13.498 file contro 13.498 sulla macchina. La cancellazione e' autorizzata.")
            print("  Attenzione: porta via l'unica copia delle 8 voci scartate dal censimento.")
        else:
            print("  BLOCCATA: manca il backup di /home fuori dalla macchina, cioe' la fase 1.3.")
            print("  Cercato come " + BACKUP_HOME_NOME + " in: "
                  + ", ".join(str(p.parent) for p in BACKUP_HOME_CANDIDATI))
    else:
        riga("ok", "COMPIUTA: la cartella non e' piu' sul Desktop")

    print("\nPA-008  Recuperare 1,2 GiB di cartelle di servizio su J:")
    disco = COPIA_SSD.parent
    if disco.is_dir():
        voci = [("FOUND.002", 429), ("FOUND.000", 412), (".Spotlight-V100", 371)]
        residuo = 0
        for nome, mib_atteso in voci:
            presente = (disco / nome).is_dir()
            riga("  " if presente else "ok", f"{nome}: {'presente, ~' + str(mib_atteso) + ' MiB' if presente else 'rimossa'}")
            if presente:
                residuo += mib_atteso
        if residuo:
            print(f"  ESEGUIBILE ADESSO: ~{residuo} MiB da recuperare. Il comando e' in PA-008.")
            print("  I due archivi .7z NON si cancellano: nessuno dei due contiene l'altro.")
        else:
            print("  COMPIUTA: le tre voci non ci sono piu'.")
    else:
        print("  IN ATTESA DEL DISCO: J: non e' collegato.")

    print("\nPA-009  Leggere lo SMART dell'SSD esterno")
    riga("ok", "CHIUSA il 2026-09-08: supporto sano, usura 0, zero errori di integrita'")
    print("  Delle due cause cade il difetto del supporto: resta la rimozione senza")
    print("  espulsione, con 122 spegnimenti non protetti su 742 cicli. Il disco non va")
    print("  sostituito. Regola: espellere il volume prima di staccarlo, sempre.")

    print("\nPA-006  Riconfermare o rivedere la scelta fra installazione e aggiornamento")
    riga("ok", "CHIUSA il 2026-09-07: installazione pulita 26.04 LTS riconfermata")
    print("  Lavoro privilegiato con comandi lanciati a mano, senza regole sudoers.")
    print("  Conseguenza: la pulizia di Wine NON si esegue, sarebbe lavoro buttato su")
    print("  un sistema che verra' azzerato. Decisione registrata come ADR-013.")


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


def controlla_pa010_pa011() -> None:
    """Le due voci aperte il 2026-09-09, entrambe con condizioni non automatizzabili da qui.

    PA-010 dipende da un confronto fra le copie esterne e la macchina, che richiede
    l'accesso SSH e non la sola postazione; PA-011 dipende da uno stato della macchina,
    cioe' la ricostruzione compiuta, che nessun controllo locale puo' osservare. Si
    elencano comunque, per la stessa ragione per cui esiste controlla_manuali: uno
    strumento che tace su una voce la fa sparire.
    """
    print("\nPA-010  Verificare i file personali sulla macchina prima di cancellarli altrove")
    riga("? ", "inventario di /home confrontato con le copie esterne: DA FARE")
    riga("ok", "~/electroacoustics verificato il 2026-09-09: 281 file, 728 MB, come atteso")
    riga("ok", "scrivania ripresentata dopo la reinstallazione: /home e' sopravvissuto")
    print("  ATTENZIONE: i due controlli fatti coprono un perimetro molto piu' stretto")
    print("  della verifica richiesta. Nessuna copia esterna va cancellata prima")
    print("  dell'inventario completo, per impronta e non per dimensione occupata.")
    print("  Riguarda anche l'apribilita' dei formati, non i soli file. Vedi PA-010.")

    print("\nPA-011  Backup Veeam della macchina, a ricostruzione finita")
    riga("  ", "condizione: fasi da 6 a 9 compiute e verificate")
    riga("ok", "catena audio: parametri di avvio attivi da /etc/default/grub.d/ubuntustudio.cfg")
    riga("  ", "limiti realtime: utente non nei gruppi audio e pipewire, da correggere")
    riga("  ", "Wine: non installato, architettura i386 non dichiarata")
    print("  BLOCCATA: un backup preso adesso congelerebbe uno stato intermedio.")
    print("  Da definire alla riapertura: prodotto, destinazione e prova di ripristino.")


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
    controlla_pa010_pa011()
    print("\nLegenda: [ok] condizione soddisfatta, [? ] da confermare a mano,")
    print("         [  ] non soddisfatta, [!!] anomalia da guardare.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
