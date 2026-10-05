#!/usr/bin/env python3
"""Censisce cartelle intere di J: e scrive il manifesto di un lotto nuovo del materiale di studio.

Percorre in sola lettura ogni cartella indicata, in tutte le sottocartelle, e scrive
research-vault/fonti-locali/lotti-manifest-NN.json con ogni documento convertibile che non
ha ancora una posizione in un registro d'origine ne' una voce in un altro manifesto, piu'
gli archivi da aprire. Il manifesto poi si indicizza con tools/indicizza-lotti.py --lotto NN,
che calcola le impronte e scarta i doppioni. Nato il 2026-10-05 con MS-196 e MS-201, dove i
lotti 10 e 11 erano stati generati con script temporanei: il censimento completo di J:
chiesto dall'utente (ADR-038) va rifatto quando il materiale cresce, quindi e' uno strumento.

Non scrive, non sposta e non cancella nulla fuori dal repository (vincolo di CLAUDE.md).

Uso:
    python tools/censisci-cartelle.py --lotto 12 "J:/MAIN/CARTELLA" ["J:/altra" ...]
    python tools/censisci-cartelle.py --lotto 12 --prova "J:/MAIN/CARTELLA"    solo conteggi
"""
import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
LOCALI = RADICE / "research-vault" / "fonti-locali"
DOC = {".pdf", ".docx", ".pptx", ".xlsx", ".html", ".htm"}
ARCHIVI = {".zip", ".rar", ".7z"}


def chiave(p):
    return os.path.normcase(os.path.normpath(p))


def gia_noti(escludi):
    noti = set()
    for r in LOCALI.glob("lotto-*-origine.json"):
        for v in json.loads(r.read_text(encoding="utf-8")):
            for k in ("posizione", "origine"):
                if v.get(k):
                    noti.add(chiave(v[k]))
    for m in LOCALI.glob("lotti-manifest*.json"):
        if m.name == escludi:
            continue
        d = json.loads(m.read_text(encoding="utf-8"))
        for v in d["voci"] + d.get("da_aprire", []):
            noti.add(chiave(v["origine"]))
    return noti


def main():
    ap = argparse.ArgumentParser(description="Censisce cartelle di J: in un lotto nuovo")
    ap.add_argument("--lotto", required=True, help="numero del lotto, per esempio 12")
    ap.add_argument("--prova", action="store_true", help="stampa i conteggi senza scrivere il manifesto")
    ap.add_argument("cartelle", nargs="+", help="cartelle o file da censire")
    a = ap.parse_args()
    nome = f"lotti-manifest-{a.lotto}.json"
    noti = gia_noti(nome)
    voci, da_aprire = [], []
    for radice in a.cartelle:
        if os.path.isfile(radice):
            elenco = [(os.path.dirname(radice), [os.path.basename(radice)])]
        elif os.path.isdir(radice):
            elenco = ((d, fs) for d, _, fs in os.walk(radice))
        else:
            print(f"non trovato: {radice}", file=sys.stderr)
            continue
        for d, fs in elenco:
            for f in sorted(fs):
                p = os.path.join(d, f)
                ext = os.path.splitext(f)[1].lower()
                if f.startswith("~$") or chiave(p) in noti or ext not in DOC | ARCHIVI:
                    continue
                motivo = f"censimento di {radice}: {os.path.relpath(d, radice)}"
                voce = {"lotto": a.lotto, "origine": p, "byte": os.path.getsize(p), "proprio": False, "motivo": motivo}
                (voci if ext in DOC else da_aprire).append(voce)
                noti.add(chiave(p))
    print(f"lotto {a.lotto}: documenti {len(voci)}, archivi da aprire {len(da_aprire)}, "
          f"{sum(v['byte'] for v in voci) / 2**30:.1f} GiB")
    if a.prova:
        return 0
    out = LOCALI / nome
    if out.exists():
        sys.exit(f"{out} esiste gia': scegliere un numero di lotto nuovo")
    out.write_text(json.dumps({"generato": date.today().isoformat(), "voci": voci, "da_aprire": da_aprire},
                              ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"scritto {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
