#!/usr/bin/env python3
"""Indicizza i lotti del materiale di studio dove stanno, senza copiarli nel progetto.

Il materiale di studio resta sul disco esterno, in J:\\MAIN: il progetto ne conserva
soltanto l'indice, perche' il progetto e' oggetto di copia di sicurezza due volte al giorno
e 5,6 GiB di doppioni la appesantirebbero senza aggiungere nulla (ADR-036, 2026-10-02).

Legge research-vault/fonti-locali/lotti-manifest*.json, che elencano file per file che
cosa appartiene a quale lotto, apre ogni file soltanto in lettura, ne calcola l'impronta
SHA-256 e registra in research-vault/fonti-locali/lotto-NN-origine.json la voce con
origine, posizione, impronta, dimensione, nome ed esito: indicizzato, doppione (con il
file che lo rappresenta) o mancante. I doppioni si riconoscono per impronta anche fra
lotti diversi e fra gli archivi estratti. Non scrive, non sposta e non cancella nulla
fuori dal repository (vincolo di CLAUDE.md, MS-177).

E' rientrante: una voce gia' indicizzata non si rilegge, quindi una corsa interrotta si
riprende rilanciando lo stesso comando. Con --verifica rilegge invece tutte le posizioni
e controlla che l'impronta registrata coincida ancora, che e' il controllo da fare prima
di fidarsi di un indice vecchio.

Uso:
    python tools/indicizza-lotti.py                indicizza le voci nuove dei manifesti
    python tools/indicizza-lotti.py --lotto 02     un solo lotto
    python tools/indicizza-lotti.py --verifica     rilegge e confronta tutte le impronte
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path, PureWindowsPath

RADICE = Path(__file__).resolve().parent.parent
LOCALI = RADICE / "research-vault" / "fonti-locali"
ESITI_VALIDI = ("indicizzato", "doppione")


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for blocco in iter(lambda: fh.read(1 << 20), b""):
            h.update(blocco)
    return h.hexdigest()


def registri():
    return sorted(LOCALI.glob("lotto-*-origine.json"))


def impronte_note():
    noto = {}
    for r in registri():
        lotto = r.name.split("-origine")[0]
        for v in json.loads(r.read_text(encoding="utf-8")):
            if v.get("esito") == "indicizzato":
                noto.setdefault(v["sha256"], f"{lotto}/{v.get('nome', '')}")
    return noto


def indicizza(lotto, voci, noto):
    registro_p = LOCALI / f"lotto-{lotto}-origine.json"
    registro = json.loads(registro_p.read_text(encoding="utf-8")) if registro_p.exists() else []
    gia = {v["origine"]: v for v in registro}
    conta = {"indicizzato": 0, "doppione": 0, "mancante": 0, "gia indicizzato": 0}
    for voce in voci:
        origine = voce["origine"]
        precedente = gia.get(origine)
        if precedente and precedente.get("esito") in ESITI_VALIDI:
            conta["gia indicizzato"] += 1
            continue
        p = Path(origine)
        if not p.is_file():
            esito = {"origine": origine, "esito": "mancante"}
        else:
            impronta = sha256(p)
            esito = {"origine": origine, "posizione": origine, "sha256": impronta,
                     "byte": p.stat().st_size, "nome": PureWindowsPath(origine).name,
                     "proprio": bool(voce.get("proprio")), "motivo": voce.get("motivo", "")}
            if impronta in noto:
                esito.update(esito="doppione", rappresentato_da=noto[impronta])
            else:
                esito["esito"] = "indicizzato"
                noto[impronta] = f"lotto-{lotto}/{esito['nome']}"
        conta[esito["esito"]] += 1
        if precedente:
            registro[registro.index(precedente)] = esito
        else:
            registro.append(esito)
    registro_p.write_text(json.dumps(registro, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return conta


def verifica():
    buoni, problemi = 0, []
    for r in registri():
        for v in json.loads(r.read_text(encoding="utf-8")):
            if v.get("esito") != "indicizzato":
                continue
            p = Path(v["posizione"])
            if not p.is_file():
                problemi.append(f"{r.name}: mancante {v['posizione']}")
            elif sha256(p) != v["sha256"]:
                problemi.append(f"{r.name}: impronta cambiata {v['posizione']}")
            else:
                buoni += 1
    print(f"posizioni verificate: {buoni}; problemi: {len(problemi)}")
    for x in problemi:
        print("  " + x)
    return 1 if problemi else 0


def main():
    ap = argparse.ArgumentParser(description="Indicizza i lotti del materiale di studio dove stanno")
    ap.add_argument("--lotto", help="solo questo lotto, per esempio 02")
    ap.add_argument("--verifica", action="store_true", help="rilegge tutte le posizioni e confronta le impronte")
    a = ap.parse_args()
    if a.verifica:
        return verifica()
    per_lotto = {}
    for m in sorted(LOCALI.glob("lotti-manifest*.json")):
        for v in json.loads(m.read_text(encoding="utf-8"))["voci"]:
            per_lotto.setdefault(v["lotto"], []).append(v)
    noto = impronte_note()
    for lotto in sorted(per_lotto):
        if a.lotto and lotto != a.lotto:
            continue
        c = indicizza(lotto, per_lotto[lotto], noto)
        print(f"lotto {lotto}: " + ", ".join(f"{k} {n}" for k, n in c.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
