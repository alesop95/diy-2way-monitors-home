#!/usr/bin/env python3
"""Cerca nei file destinati a GitHub cio' che viene dall'SSD privato dell'utente.

Il repository e' pubblico, e il materiale di studio sta su un disco privato (ADR-036): un
titolo, un nome di file o un nome di persona copiato da li' in un file tracciato diventa
pubblico al primo push. Lo strumento esamina i file tracciati e quelli nuovi non ignorati,
cioe' tutto cio' che un `git add -A` porterebbe nel commit, e segnala:

  - i termini dell'elenco locale _notes/privacy/termini.txt, una espressione regolare per
    riga: nomi di persone, documenti personali, qualunque cosa l'utente non voglia
    pubblicare. L'elenco e' locale di proposito, perche' scriverlo in un file tracciato
    pubblicherebbe proprio cio' che protegge;
  - le tracce di provenienza non ufficiale dei libri, come i suffissi di libgen o epdf;
  - i percorsi di singoli file sul disco esterno, cioe' J: seguito da un nome con
    estensione di documento o di archivio, perche' rivelano il contenuto del disco.

Le eccezioni dichiarate stanno in _notes/privacy/eccezioni.txt, una per riga nella forma
<file>:<testo esatto>, e vengono contate a parte. Esce con 1 se trova qualcosa.
Nato il 2026-10-05 con MS-202, dopo che il registro delle fonti aveva pubblicato i titoli
di 3300 file dell'SSD, compresi documenti personali.

Uso:
    python tools/check-privato.py
    python tools/check-privato.py --tutti      elenca ogni occorrenza invece delle prime
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
LOCALE = RADICE / "_notes" / "privacy"
FISSI = [
    (r"(?i)libgen\.(lc|is|rs|li|st)|\blibgen\b|library\s+genesis", "provenienza non ufficiale di un libro"),
    (r"(?i)sci-?hub|anna.?s archive", "provenienza non ufficiale di un libro"),
    (r"(?i)epdf\.pub|\bz-lib|\b1lib\b|pdfdrive|b-ok\.(cc|org)", "provenienza non ufficiale di un libro"),
    (r"(?i)(canale|libri) telegram", "provenienza non ufficiale di un libro"),
    (r"(?i)J:[\\/]+[^`\"\n|]*?\.(pdf|docx?|pptx?|xlsx|djvu|epub|zip|rar|7z)\b", "percorso di un singolo file su J:"),
]
TESTO = {".md", ".txt", ".json", ".yml", ".yaml", ".py", ".ps1", ".sh", ".html", ".bib", ".tex", ".csv", ""}
ESCLUSI = (".claude/templates/", ".agents/", "tools/check-privato.py")


def candidati():
    git = lambda *a: subprocess.run(["git", *a], cwd=RADICE, capture_output=True, text=True,
                                    encoding="utf-8").stdout.splitlines()
    nomi = set(git("ls-files")) | set(git("ls-files", "--others", "--exclude-standard"))
    return sorted(n for n in nomi if Path(n).suffix.lower() in TESTO and not n.startswith(ESCLUSI))


def leggi_righe(p):
    if not p.exists():
        return []
    return [r.strip() for r in p.read_text(encoding="utf-8").splitlines() if r.strip() and not r.startswith("#")]


def main():
    ap = argparse.ArgumentParser(description="Cerca nei file destinati a GitHub cio' che viene dall'SSD privato")
    ap.add_argument("--tutti", action="store_true", help="elenca ogni occorrenza")
    a = ap.parse_args()
    regole = [(re.compile(x), m) for x, m in FISSI]
    termini = leggi_righe(LOCALE / "termini.txt")
    regole += [(re.compile(t, re.I), "termine dell'elenco locale") for t in termini]
    eccezioni = set(leggi_righe(LOCALE / "eccezioni.txt"))
    trovati, dichiarati = [], 0
    for nome in candidati():
        p = RADICE / nome
        try:
            testo = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for n, riga in enumerate(testo.splitlines(), 1):
            for rx, motivo in regole:
                for m in rx.finditer(riga):
                    if f"{nome}:{m.group(0)}" in eccezioni:
                        dichiarati += 1
                        continue
                    trovati.append((nome, n, motivo, m.group(0)))
    if not termini:
        print("attenzione: _notes/privacy/termini.txt assente o vuoto, controllati solo i segni fissi")
    limite = None if a.tutti else 40
    for nome, n, motivo, testo in trovati[:limite]:
        print(f"  {nome}:{n}  {motivo}: {testo[:80]}")
    if limite and len(trovati) > limite:
        print(f"  ... e altri {len(trovati) - limite}: rilanciare con --tutti")
    file_ = len({t[0] for t in trovati})
    print(f"check-privato: {len(trovati)} occorrenze in {file_} file, {dichiarati} eccezioni dichiarate, "
          f"{len(termini)} termini locali")
    return 1 if trovati else 0


if __name__ == "__main__":
    sys.exit(main())
