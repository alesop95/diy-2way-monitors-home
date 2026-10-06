"""Prepara gli estratti per le schede di fonte del livello 2 (ADR-041), senza modello.

Sceglie in modo deterministico i documenti di una cartella di J:/MAIN gia' convertiti in
_notes/.tmp-doc-cache/fonti/, esclude i documenti personali (ADR-042) e quelli sotto la soglia
di parole, e per ciascuno scrive un estratto con lo scheletro delle intestazioni e le prime
parole del testo. Il modello economico legge soltanto gli estratti: il lavoro meccanico resta
nel codice, per token-economy.md.

Uso: python tools/estratti-lotto.py --cartella "LOUDSPEAKERS & ELECTROACOUSTIC" --quanti 50 --dest _notes/lotti/prova-L2
"""
import argparse
import glob
import json
import re
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RADICE / "tools"))
from privato_esclusi import carica_schemi, e_personale  # noqa: E402

CACHE = RADICE / "_notes" / ".tmp-doc-cache" / "fonti"
LOCALI = RADICE / "research-vault" / "fonti-locali"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cartella", required=True)
    ap.add_argument("--quanti", type=int, default=50)
    ap.add_argument("--parole", type=int, default=1500, help="parole iniziali dell'estratto")
    ap.add_argument("--minimo", type=int, default=300, help="parole minime del documento")
    ap.add_argument("--salta", type=int, default=0, help="documenti da saltare, per i lotti successivi")
    ap.add_argument("--dest", required=True)
    ap.add_argument("--pacchetti", type=int, default=0,
                    help="se maggiore di zero, riunisce gli estratti in file pacchetto-NN.md da tanti estratti ciascuno, "
                         "con l'elenco delle pagine di concetto esistenti, cosi' che un agente legga un solo file (MS-214)")
    a = ap.parse_args()
    schemi = carica_schemi()
    posizioni = {}
    for f in sorted(LOCALI.glob("lotto-*-origine.json")):
        for v in json.loads(f.read_text(encoding="utf-8")):
            if v.get("esito") == "indicizzato" and v.get("sha256"):
                posizioni.setdefault(v["sha256"], v["posizione"])
    manifest = json.loads((CACHE / "manifest.json").read_text(encoding="utf-8"))
    marcatore = "\\MAIN\\" + a.cartella + "\\"
    scelti = []
    for h, m in manifest.items():
        pos = posizioni.get(h, "")
        if marcatore.lower() not in pos.lower() or e_personale(pos, schemi):
            continue
        if m.get("parole", 0) < a.minimo or not (CACHE / m["cache"]).exists():
            continue
        scelti.append((pos.lower(), h, m))
    scelti.sort()
    scelti = scelti[a.salta:a.salta + a.quanti]
    dest = Path(a.dest)
    dest.mkdir(parents=True, exist_ok=True)
    elenco = []
    for i, (_, h, m) in enumerate(scelti, 1):
        testo = (CACHE / m["cache"]).read_text(encoding="utf-8", errors="replace")
        titoli = [r for r in testo.splitlines() if re.match(r"#{1,3} ", r)][:60]
        parole = testo.split()
        corpo = " ".join(parole[:a.parole])
        nome = f"{i:03d}.md"
        (dest / nome).write_text(
            f"# Estratto {i:03d}\n\nnome: {m['nome']}\nparole totali: {m['parole']}\nimpronta: {h[:12]}\n\n"
            f"## Scheletro\n\n" + ("\n".join(titoli) or "(nessuna intestazione)") +
            f"\n\n## Prime {min(a.parole, len(parole))} parole\n\n{corpo}\n", encoding="utf-8")
        elenco.append({"estratto": nome, "nome": m["nome"], "cache": m["cache"], "parole": m["parole"], "impronta": h})
    (dest / "elenco.json").write_text(json.dumps(elenco, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if a.pacchetti:
        concetti = sorted(p.stem for p in (RADICE / "knowledge" / "wiki" / "concepts").glob("*.md"))
        for k in range(0, len(elenco), a.pacchetti):
            parti = [(dest / e["estratto"]).read_text(encoding="utf-8") for e in elenco[k:k + a.pacchetti]]
            testa = ("# Pacchetto di estratti\n\nPagine di concetto esistenti in knowledge/wiki/concepts/, "
                     "le sole da usare nei collegamenti:\n\n" + ", ".join(concetti) + "\n\n")
            (dest / f"pacchetto-{k // a.pacchetti + 1:02d}.md").write_text(testa + "\n\n".join(parti), encoding="utf-8")
    print(f"estratti {len(elenco)} in {dest}; parole negli estratti circa {sum(min(a.parole, e['parole']) for e in elenco)}")


if __name__ == "__main__":
    main()
