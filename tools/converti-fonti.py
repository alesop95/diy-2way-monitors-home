#!/usr/bin/env python3
"""Converte in Markdown il materiale di studio indicizzato, leggendolo dove sta su J:.

Il materiale resta sul disco esterno (ADR-036) e il progetto ne tiene l'indice in
research-vault/fonti-locali/lotto-*-origine.json. Questo strumento percorre l'indice,
apre ogni documento indicizzato nella sua posizione soltanto in lettura e ne scrive il
testo in _notes/.tmp-doc-cache/fonti/<lotto>/<nome>.md, che resta nel progetto perche'
e' leggero e serve alla wiki e alle ricerche anche con il disco scollegato.

La conversione e' quella di tools/doc-ingest.py, importata e non duplicata: doc-ingest
e' la copia di un modello del template e lavora su una cartella, mentre qui i documenti
sono sparsi su J: e si leggono dall'indice. Il manifesto
_notes/.tmp-doc-cache/fonti/manifest.json e' indicizzato per impronta, quindi un documento
gia' convertito non si riconverte, e registra per ciascuno il numero di parole: sotto le
50 parole un PDF e' quasi sempre una scansione, da rifare con --ocr o --engine docling.
L'indice di Livello 1 del corpus e' _notes/.tmp-doc-cache/fonti/_INDEX.md.

Riusa le conversioni fatte prima di ADR-036 sulle copie, identiche per impronta agli
originali, che stanno in _notes/.tmp-doc-cache/ e in _notes/.tmp-doc-cache/lotto-NN/.

Uso:
    python tools/converti-fonti.py                     converte cio' che manca
    python tools/converti-fonti.py --lotto 05          un solo lotto
    python tools/converti-fonti.py --ocr               OCR sui PDF con poco testo
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from privato_esclusi import carica_schemi, e_personale  # noqa: E402

RADICE = Path(__file__).resolve().parent.parent
LOCALI = RADICE / "research-vault" / "fonti-locali"
CACHE = RADICE / "_notes" / ".tmp-doc-cache"
USCITA = CACHE / "fonti"
SOGLIA_PAROLE = 50


def carica_doc_ingest():
    spec = importlib.util.spec_from_file_location("doc_ingest", RADICE / "tools" / "doc-ingest.py")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def conversione_vecchia(lotto, nome):
    """Il testo convertito dalla copia prima di ADR-036, se esiste."""
    for p in (CACHE / lotto / f"{nome}.md", CACHE / f"{nome}.md"):
        if p.is_file() and p.stat().st_size > 0:
            return p.read_text(encoding="utf-8")
    return None


TESSDATA = RADICE / "_notes" / "tessdata"
PANDOC = Path.home() / "AppData" / "Local" / "Pandoc" / "pandoc.exe"


def docx_con_pandoc(percorso):
    """Converte un .docx con pandoc. markitdown scarta le equazioni di Word, e gli appunti
    dell'utente, cioe' le lezioni del Politecnico sbobinate con le formule, sono fatti di
    equazioni: in EEASE I.docx ce n'erano 2491 e nel testo di markitdown quasi nessuna.
    pandoc le porta in LaTeX fra dollari, che e' la forma in cui la tesi le riusa."""
    import subprocess
    r = subprocess.run([str(PANDOC), "-f", "docx", "-t", "markdown", "--wrap=none", str(percorso)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError(f"pandoc: {r.stderr.strip()[:300]}")
    return r.stdout


def ocr_pdf(percorso, lingue):
    """OCR pagina per pagina con Tesseract. Non usa l'OCR di doc-ingest perche' quello
    chiama Tesseract senza lingua, cioe' in solo inglese, e gli appunti dell'utente sono
    in italiano; i modelli di lingua stanno in _notes/tessdata, fuori dall'installazione
    di sistema."""
    import os
    import pytesseract
    from pdf2image import convert_from_path, pdfinfo_from_path
    import shutil
    os.environ["TESSDATA_PREFIX"] = str(TESSDATA)
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    # Poppler non apre un percorso oltre i 260 caratteri di Windows e risponde "Unable to get
    # page count" (Izadian, MS-206): il PDF si legge da una copia a percorso corto nella
    # cartella locale _notes/ocr/, che si toglie a lavoro finito.
    copia = None
    if len(str(percorso)) > 240:
        copia = RADICE / "_notes" / "ocr" / "percorso-lungo.pdf"
        copia.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(percorso, copia)
        percorso = copia
    try:
        pagine = pdfinfo_from_path(str(percorso))["Pages"]
        parti = []
        for i in range(1, pagine + 1):
            immagine = convert_from_path(str(percorso), dpi=200, first_page=i, last_page=i)[0]
            parti.append(f"<!-- pagina {i} -->\n" + pytesseract.image_to_string(immagine, lang=lingue))
    finally:
        if copia is not None:
            copia.unlink(missing_ok=True)
    return "\n\n".join(parti), f"estratto via OCR Tesseract ({lingue}, {pagine} pagine, 200 dpi)"


def main():
    ap = argparse.ArgumentParser(description="Converte in Markdown il materiale indicizzato su J:")
    ap.add_argument("--lotto", help="solo questo lotto, per esempio 05")
    ap.add_argument("--ocr", action="store_true", help="OCR sui PDF con testo nativo insufficiente")
    ap.add_argument("--lingue", default="ita+eng", help="lingue di Tesseract per l'OCR (default ita+eng)")
    ap.add_argument("--nomi", nargs="*", help="solo i documenti il cui nome contiene uno di questi testi")
    ap.add_argument("--engine", choices=["markitdown", "docling"], default="markitdown")
    a = ap.parse_args()
    di = carica_doc_ingest()
    USCITA.mkdir(parents=True, exist_ok=True)
    manifest_p = USCITA / "manifest.json"
    manifest = json.loads(manifest_p.read_text(encoding="utf-8")) if manifest_p.exists() else {}
    schemi = carica_schemi()
    conta = {"nuovo": 0, "riusato": 0, "invariato": 0, "errore": 0, "assente": 0, "personale escluso": 0}
    for r in sorted(LOCALI.glob("lotto-*-origine.json")):
        lotto = r.name.split("-origine")[0]
        if a.lotto and lotto != f"lotto-{a.lotto}":
            continue
        for v in json.loads(r.read_text(encoding="utf-8")):
            if v.get("esito") != "indicizzato":
                continue
            nome = v.get("nome", "")
            if Path(nome).suffix.lower() not in di.SUPPORTED_EXTENSIONS:
                continue
            if a.nomi and not any(t.lower() in nome.lower() for t in a.nomi):
                continue
            # I documenti personali non si convertono ne' si passano all'OCR (ADR-042).
            if e_personale(v.get("posizione", ""), schemi):
                conta["personale escluso"] += 1
                continue
            impronta = v["sha256"]
            cache_rel = f"{lotto}/{nome}.md"
            destinazione = USCITA / cache_rel
            precedente = manifest.get(impronta)
            e_docx = Path(nome).suffix.lower() == ".docx"
            docx_da_rifare = e_docx and PANDOC.exists() and (precedente or {}).get("motore") != "pandoc"
            if (precedente and (USCITA / precedente["cache"]).exists() and not docx_da_rifare
                    and not (a.ocr and precedente["parole"] < SOGLIA_PAROLE)):
                conta["invariato"] += 1
                continue
            testo, nota, stato = (None if docx_da_rifare else conversione_vecchia(lotto, nome)), None, "riusato"
            motore = (precedente or {}).get("motore", "markitdown")
            if testo is None or (a.ocr and len(testo.split()) < SOGLIA_PAROLE):
                sorgente = Path(v["posizione"])
                if not sorgente.is_file():
                    conta["assente"] += 1
                    print(f"[assente] {v['posizione']}", file=sys.stderr)
                    continue
                try:
                    if testo is None and e_docx and PANDOC.exists():
                        testo, nota, motore = docx_con_pandoc(sorgente), "convertito con pandoc, equazioni in LaTeX", "pandoc"
                    elif testo is None:
                        testo, nota = di.convert_file(sorgente, a.engine, False)
                        motore = a.engine
                    if a.ocr and sorgente.suffix.lower() == ".pdf" and len(testo.split()) < SOGLIA_PAROLE:
                        testo_ocr, nota_ocr = ocr_pdf(sorgente, a.lingue)
                        if len(testo_ocr.split()) > len(testo.split()):
                            testo, nota = testo_ocr, nota_ocr
                    stato = "nuovo"
                except Exception as exc:  # qualunque libreria di conversione puo' fallire
                    conta["errore"] += 1
                    manifest[impronta] = {"lotto": lotto, "nome": nome, "cache": cache_rel, "parole": 0,
                                          "errore": str(exc)[:300]}
                    print(f"[errore] {lotto}/{nome}: {exc}", file=sys.stderr)
                    continue
            destinazione.parent.mkdir(parents=True, exist_ok=True)
            destinazione.write_text(testo, encoding="utf-8")
            analisi = di.analyze_markdown(testo)
            manifest[impronta] = {"lotto": lotto, "nome": nome, "cache": cache_rel,
                                  "parole": analisi["words"], "titolo": analisi["title"], "nota": nota,
                                  "motore": motore, "formule": testo.count("$") // 2}
            conta[stato] += 1
            if (conta["nuovo"] + conta["riusato"]) % 25 == 0:
                manifest_p.write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    manifest_p.write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    voci = []
    for m in manifest.values():
        p = USCITA / m["cache"]
        if not p.exists():
            continue
        analisi = di.analyze_markdown(p.read_text(encoding="utf-8"))
        voci.append({"source_rel": f"{m['lotto']}/{m['nome']}", "cache_rel": m["cache"],
                     "status": "scansione da OCR" if m["parole"] < SOGLIA_PAROLE else "convertito",
                     "note": m.get("nota"), **analisi})
    (USCITA / "_INDEX.md").write_text(di.render_index(voci), encoding="utf-8")
    pochi = sum(1 for m in manifest.values() if m.get("parole", 0) < SOGLIA_PAROLE)
    print("converti-fonti: " + ", ".join(f"{k} {n}" for k, n in conta.items())
          + f"; nel manifesto {len(manifest)}, di cui {pochi} sotto {SOGLIA_PAROLE} parole")
    return 0


if __name__ == "__main__":
    sys.exit(main())
