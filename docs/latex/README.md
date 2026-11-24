# Capitoli tecnici in LaTeX

Le fonti editoriali sono il [confronto fra crossover](../62-confronto-crossover-e-verifica-matematica.md) e il [progetto delle modalità PC e autonoma](../63-sistema-autonomo-driver-e-collaudo.md). Modificare il Markdown e rigenerare i rispettivi file TeX con [converti.py](converti.py). La rigenerazione sostituisce eventuali modifiche fatte direttamente ai TeX.

Il preambolo comune usa i font Altro Serif Light e Altro Grotesk Book e Medium dal kit locale Intrawelt, Consolas installato nel sistema e Latin Modern Math per la matematica. `intrawelt-header.tex` indica la radice dei font Altro e accetta `\AltroFontPath` come sostituzione. Per compilare si usano TinyTeX e latexmk del pacchetto LaTeX già adottato dal progetto, con LuaLaTeX per questi capitoli. L'ambiente verificato comprende Pandoc 3.12, latexmk 4.88, LuaHBTeX 1.24.0 della distribuzione TeX Live 2026 e i pacchetti `amsmath`, `amsfonts`, `babel` con italiano, `bookmark`, `booktabs`, `caption`, `etoolbox`, `fontspec`, `geometry`, `graphics`, `hyperref`, `listings`, `lm`, `titlesec`, `tools`, `unicode-math` e `xcolor`.

Il capitolo 62 incorpora `lr4-modulo-fase.pdf` e `cammino-e-somma.pdf` da `build/studio-crossover-20261120-v2/`. Il capitolo 63 incorpora `confronto-driver.pdf` da `build/sistema-autonomo-20261120-v5/`. I comandi di riproduzione nei capitoli sorgente generano i tre grafici vettoriali con i dati dei modelli, quando le rispettive directory non sono ancora presenti.

Eseguire dalla radice del repository con PowerShell.

```powershell
python docs/latex/converti.py 62 63
if ($LASTEXITCODE -ne 0) { throw 'Conversione Pandoc fallita' }
New-Item -ItemType Directory -Force -Path build/relazione-audio-20261120
$cacheTexPrecedente = $env:TEXMFCACHE
Push-Location docs/latex
try {
    $env:TEXMFCACHE = (Resolve-Path '../../build/relazione-audio-20261120').Path
    latexmk -lualatex -interaction=nonstopmode -halt-on-error -file-line-error '-outdir=../../build/relazione-audio-20261120' crossover-pc-pi-analogico.tex sistema-autonomo-driver-e-collaudo.tex
    if ($LASTEXITCODE -ne 0) { throw 'Compilazione LuaLaTeX fallita' }
} finally {
    $env:TEXMFCACHE = $cacheTexPrecedente
    Pop-Location
}
```

Il compilatore usa `build/relazione-audio-20261120/` soltanto per intermedi, log e cache font. I PDF correnti consegnati sono `docs/pdf/crossover-pc-pi-analogico.pdf` e `docs/pdf/sistema-autonomo-driver-e-collaudo.pdf`; dopo compilazione si copiano, si confrontano le impronte e si rimuovono i PDF intermedi. Il terzo PDF, `docs/pdf/recap-progetto.pdf`, deriva da STATO-PROGETTO.md con WordCraft. Il manifesto in docs/pdf registra i sorgenti e le impronte. I collegamenti sono relativi alla collocazione finale. Le immagini renderizzate per il controllo sono temporanee e vengono eliminate dopo l'ispezione.

## Problemi osservati su Windows

Il comando corrente che orchestra anche la copia verificata e il manifesto è `python tools/consegna_documenti.py`. Riusa WordCraft per il recap, Pandoc/LuaLaTeX per le relazioni e PdfCraft per metadati/testo; rigenera soltanto le consegne con input cambiati. I comandi sopra restano la compilazione LaTeX elementare. `python tools/consegna_documenti.py --check` richiede impronte correnti e QA visivo registrato. Dopo avere realmente ispezionato le pagine cambiate si usa `--conferma-qa nome.pdf --pagine 1,3`; il comando registra il gesto, non lo esegue. Non vengono prodotte immagini di ogni pagina: le singole immagini eventualmente renderizzate si eliminano dopo l'ispezione. La nuova compilazione può cambiare il numero di pagine; il manifesto conserva quello effettivo.

- `no writeable cache path` indica che LuaLaTeX richiede una cache font scrivibile. Il comando imposta `TEXMFCACHE` nella directory di build per la durata della compilazione.
- Se latexmk tenta di aprire `../../build/` come directory di lavoro, controllare che l'intero argomento `'-outdir=…'` sia racchiuso tra apici. Windows PowerShell 5.1 altrimenti lo può dividere in due argomenti.
