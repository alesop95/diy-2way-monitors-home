"""Converte i capitoli tecnici 62, 63 e 64 in documenti LaTeX autonomi."""

import argparse
from pathlib import Path
import re
import subprocess


CHAPTERS = {
    "62": (
        "62-confronto-crossover-e-verifica-matematica.md",
        "crossover-pc-pi-analogico.tex",
    ),
    "63": (
        "63-sistema-autonomo-driver-e-collaudo.md",
        "sistema-autonomo-driver-e-collaudo.tex",
    ),
    "64": (
        "64-reflex-direttivita-e-cabinet-nominale.md",
        "reflex-direttivita-cabinet.tex",
    ),
}

FIGURES = ("lr4-modulo-fase", "cammino-e-somma")
COMPANION_PDFS = {
    source: Path(tex).with_suffix(".pdf").name for source, tex in CHAPTERS.values()
}

INLINE_MATH = {
    "omega_c=2*pi*fc": r"\omega_c=2\pi f_c",
    "Q=1/sqrt(2)": r"Q=1/\sqrt{2}",
    "s=j*omega_c": r"s=j\omega_c",
    "s=j*omega": r"s=j\omega",
    "w0=2*pi*fc/fs": r"\omega_0=2\pi f_c/f_s",
    "alpha=sin(w0)/(2Q)": r"\alpha=\sin(\omega_0)/(2Q)",
    "b0, b1, b2": r"b_0, b_1, b_2",
    "a0, a1, a2": r"a_0, a_1, a_2",
    "per a0": r"per $a_0$",
    "K=1": "K=1",
    "Q=0,5": "Q=0{,}5",
    "K=3-sqrt(2)=1,5857864": r"K=3-\sqrt{2}=1{,}5857864",
    "K^2=2,5147186": "K^2=2{,}5147186",
    "fc=2 kHz": r"f_c=2\,\mathrm{kHz}",
    "C=10 nF": r"C=10\,\mathrm{nF}",
    "R=7957,747 ohm": r"R=7957{,}747\,\Omega",
    "Gw=Gt": "G_w=G_t",
    "Gw e Gt": "$G_w$ e $G_t$",
    "delta_d=20 mm": r"\Delta d=20\,\mathrm{mm}",
    "delta_d=85,75 mm": r"\Delta d=85{,}75\,\mathrm{mm}",
    "delta_d introduce": r"$\Delta d$ introduce",
    "c=343 m/s": r"c=343\,\mathrm{m/s}",
    "il profilo Ep": "il profilo $E_p$",
    "10^(6/20)=1,99526": "10^{6/20}=1{,}99526",
    "||y||infinito <= ||h||1 ||x||infinito": (
        r"\lVert y\rVert_\infty \le \lVert h\rVert_1\lVert x\rVert_\infty"
    ),
    "1/f^2": "1/f^2",
    "Vn=Vref*10^(-DR/20)": r"V_n=V_\mathrm{ref}\,10^{-DR/20}",
    "N=1025": "N=1025",
    "(N-1)/(2fs)=10,667 ms": r"(N-1)/(2f_s)=10{,}667\,\mathrm{ms}",
    "incluso fc esatto": "incluso $f_c$ esatto",
    "DeltaP*t/1000 kWh": r"\Delta P\,t/1000\,\mathrm{kWh}",
    "ipotetico DeltaP": r"ipotetico $\Delta P$",
}


def normalize_prose(prose, chapter):
    # I riferimenti del PDF partono da build/relazione-audio-20261120.
    def relative_link(match):
        target = match[1]
        if target in COMPANION_PDFS:
            return f"]({COMPANION_PDFS[target]})"
        if target.startswith(("#", "/")) or ":" in target or target.startswith("figure/"):
            return match[0]
        if target.startswith("../"):
            return f"](../../{target[3:]})"
        return f"](../../docs/{target})"

    prose = re.sub(r"\]\(([^()\s]+)\)", relative_link, prose)
    if chapter == "64":
        for name in ("chiusa-reflex", "condotto-ingombro-velocita", "direttivita-ideale", "condensatore-e-livelli"):
            prose = prose.replace("figure/completamento-20261125/" + name + ".svg",
                                  "../../build/completamento-20261125-figure/" + name + ".pdf")
    if chapter == "62":
        for figure in FIGURES:
            prose = prose.replace(
                f"figure/crossover-20261120/{figure}.svg",
                f"../../build/studio-crossover-20261120-v2/{figure}.pdf",
            )
        for source, math in INLINE_MATH.items():
            pattern = rf"(?<![\w$]){re.escape(source)}(?![\w$])"
            prose = re.sub(
                pattern, lambda _: math if "$" in math else f"${math}$", prose
            )
        prose = re.sub(
            r"\b(\d+,\d+)e-(\d+)\b",
            lambda match: f"${match[1].replace(',', '{,}')}\\times10^{{-{match[2]}}}$",
            prose,
        )
        prose = prose.replace("DAW → Pi", r"DAW $\to$ Pi")
        prose = prose.replace(" --font-dir ", r" \mbox{\texttt{-\/-font-dir}} ")
    return prose


def convert(chapter, docs):
    source_name, tex_name = CHAPTERS[chapter]
    source = docs / source_name
    markdown = source.read_text(encoding="utf-8")
    # Conserva il codice e le formule già delimitate nel Markdown.
    blocks = re.split(r"(^```[^\n]*\n.*?^```[^\n]*$|\$\$.*?\$\$)", markdown, flags=re.M | re.S)
    markdown = "".join(
        normalize_prose(block, chapter) if index % 2 == 0 else block
        for index, block in enumerate(blocks)
    )
    command = [
        "pandoc", "-f", "markdown", "-t", "latex", "--standalone", "--columns=92",
        "--syntax-highlighting=none", "--shift-heading-level-by=-1",
        "-V", r"header-includes=\input{intrawelt-header.tex}", "-V", "documentclass=article",
        "-V", "papersize=a4", "-V", "geometry:margin=22mm", "-V", "fontsize=11pt",
        "-V", "colorlinks=true", "-V", "linkcolor=intraweltViolet",
        "-V", "urlcolor=intraweltViolet", "-V", "citecolor=intraweltViolet",
        "-V", "filecolor=intraweltViolet",
        "-M", "lang=it-IT",
    ]
    output = subprocess.run(
        command, input=markdown, encoding="utf-8", stdout=subprocess.PIPE, check=True
    ).stdout
    # Il testo italiano non richiede la modalità bidirezionale di Babel.
    output = re.sub(r"bidi=(basic|default),", "", output)
    # Questa installazione LuaLaTeX è priva di selnolig.
    output = re.sub(
        r"^\\ifLuaTeX\n  \\usepackage\{selnolig\}[^\n]*\n\\fi\n", "", output, flags=re.M
    )
    # Le tabelle senza didascalia non utilizzano la spaziatura di caption.
    if not re.search(r"\\begin\{longtable\}(?:(?!\\end\{longtable\}).)*\\caption", output, re.S):
        output = output.replace(r"\captionsetup[table]{skip=6pt}" + "\n", "")
    output = output.replace(
        r"\includegraphics[keepaspectratio,alt=",
        r"\includegraphics[width=.92\linewidth,keepaspectratio,alt=",
    )
    output = output.replace(r"\begin{verbatim}", r"\begin{lstlisting}")
    output = output.replace(r"\end{verbatim}", r"\end{lstlisting}")
    output = (
        f"% Generato da docs/{source_name} con Pandoc.\n"
        "% Modificare il Markdown sorgente e rigenerare il file TeX.\n"
        + output
    )
    (docs / "latex" / tex_name).write_text(output, encoding="utf-8", newline="\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("chapters", choices=CHAPTERS, nargs="+")
    args = parser.parse_args()
    docs = Path(__file__).resolve().parents[1]
    for chapter in args.chapters:
        convert(chapter, docs)


if __name__ == "__main__":
    main()
