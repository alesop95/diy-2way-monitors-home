#!/usr/bin/env python3
"""Estrae gli archivi del materiale di studio accanto al materiale stesso, e li indicizza.

Legge la sezione "da_aprire" di research-vault/fonti-locali/lotti-manifest*.json, estrae
ogni archivio (zip, rar, 7z) con 7-Zip in una cartella temporanea dentro il progetto,
_notes/.tmp-estrazione/, e scrive nella destinazione indicata con --dest soltanto i file
la cui impronta non e' gia' indicizzata. Poi registra ogni file in
research-vault/fonti-locali/lotto-archivi-origine.json con origine
"<archivio> :: <percorso interno>", posizione, impronta e dimensione, e cancella la
cartella temporanea.

La destinazione sta di norma su J:, accanto al materiale, perche' il materiale di studio
non vive nel progetto (ADR-036). Scrivere su J: richiede il permesso esplicito
dell'utente (vincolo di CLAUDE.md, MS-177): per questo --dest non ha un valore
predefinito, e lo strumento non cancella e non sovrascrive mai nulla nella destinazione.
Il 2026-10-02 l'utente ha scelto J:\\MAIN\\_ESTRATTI ARCHIVI TESI.

Uso:
    python tools/estrai-archivi.py --dest "J:/MAIN/_ESTRATTI ARCHIVI TESI"
    python tools/estrai-archivi.py --dest "..." --prova     elenca soltanto
"""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path, PureWindowsPath

RADICE = Path(__file__).resolve().parent.parent
LOCALI = RADICE / "research-vault" / "fonti-locali"
TEMPORANEA = RADICE / "_notes" / ".tmp-estrazione"
SETTEZIP = Path("C:/Program Files/7-Zip/7z.exe")


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for blocco in iter(lambda: fh.read(1 << 20), b""):
            h.update(blocco)
    return h.hexdigest()


def impronte_note():
    noto = {}
    for r in LOCALI.glob("lotto-*-origine.json"):
        for v in json.loads(r.read_text(encoding="utf-8")):
            if v.get("esito") == "indicizzato":
                noto.setdefault(v["sha256"], v["posizione"])
    return noto


def main():
    ap = argparse.ArgumentParser(description="Estrae e indicizza gli archivi del materiale di studio")
    ap.add_argument("--dest", required=True, help="cartella di destinazione, scelta dall'utente")
    ap.add_argument("--prova", action="store_true")
    a = ap.parse_args()
    dest = Path(a.dest)
    archivi = []
    for m in sorted(LOCALI.glob("lotti-manifest*.json")):
        archivi += [v["origine"] for v in json.loads(m.read_text(encoding="utf-8")).get("da_aprire", [])]
    registro_p = LOCALI / "lotto-archivi-origine.json"
    registro = json.loads(registro_p.read_text(encoding="utf-8")) if registro_p.exists() else []
    fatti = {v["origine"].split(" :: ")[0] for v in registro}
    noto = impronte_note()
    for archivio in archivi:
        if archivio in fatti:
            print(f"gia indicizzato: {archivio}")
            continue
        sorgente = Path(archivio)
        if not sorgente.is_file():
            print(f"mancante: {archivio}")
            continue
        nome = re.sub(r"[^\w\- .()+]", "_", sorgente.stem)
        if a.prova:
            print(f"estrarrei {archivio} in {dest / nome}")
            continue
        tmp = TEMPORANEA / nome
        shutil.rmtree(tmp, ignore_errors=True)
        tmp.mkdir(parents=True)
        r = subprocess.run([str(SETTEZIP), "x", "-y", "-bd", f"-o{tmp}", str(sorgente)],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode != 0:
            print(f"errore di 7-Zip su {archivio}: {r.stderr.strip()[:300]}")
            continue
        conta = {"indicizzato": 0, "doppione": 0}
        for f in sorted(p for p in tmp.rglob("*") if p.is_file()):
            impronta = sha256(f)
            interno = f.relative_to(tmp).as_posix()
            voce = {"origine": f"{archivio} :: {interno}", "sha256": impronta, "byte": f.stat().st_size}
            if impronta in noto:
                voce.update(esito="doppione", rappresentato_da=noto[impronta])
                conta["doppione"] += 1
            else:
                d = dest / nome / interno
                if d.exists():
                    raise SystemExit(f"esiste gia' nella destinazione, non sovrascrivo: {d}")
                d.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, d)
                if sha256(d) != impronta:
                    raise SystemExit(f"impronta diversa dopo la copia: {d}")
                posizione = str(PureWindowsPath(d))
                voce.update(esito="indicizzato", posizione=posizione, nome=f"{nome}/{interno}")
                noto[impronta] = posizione
                conta["indicizzato"] += 1
            registro.append(voce)
        shutil.rmtree(tmp, ignore_errors=True)
        registro_p.write_text(json.dumps(registro, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"{sorgente.name}: nuovi {conta['indicizzato']}, doppioni {conta['doppione']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
