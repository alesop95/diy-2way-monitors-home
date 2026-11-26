# Pacchetto opzionale: ambiente LaTeX

> Scheletro riusabile dell'ambiente di build LaTeX descritto nella sezione 13 di `PROJECT-SYSTEM.md`. Si istanzia solo nei progetti che producono un documento LaTeX. Modello manifesto + ambiente-esterno: si versiona la fonte riproducibile (manifesto e script), si ignora la distribuzione TeX materializzata (TinyTeX), installata user-local e condivisa fra i progetti.

## Mappa di istanziazione

```
templates/latex/scripts/setup-tex.ps1   ->  <radice>/scripts/setup-tex.ps1   (tracciato)
templates/latex/scripts/setup-tex.sh    ->  <radice>/scripts/setup-tex.sh    (tracciato)
templates/latex/scripts/build.ps1       ->  <radice>/scripts/build.ps1       (tracciato)
templates/latex/scripts/build.sh        ->  <radice>/scripts/build.sh        (tracciato)
templates/latex/tex-packages.txt        ->  <radice>/tex-packages.txt        (tracciato, da adattare)
templates/latex/latexmkrc               ->  <radice>/.latexmkrc              (tracciato)
templates/latex/skills/latex-build/     ->  <radice>/.claude/skills/latex-build/   (tracciato)
```

Aggiungere inoltre al `.gitignore` del progetto le esclusioni degli artefatti LaTeX (PDF e ausiliari): vedi il blocco LaTeX in `templates/gitignore.snippet`.

## Dopo l'istanziazione

Adattare `tex-packages.txt` al preambolo reale del proprio `.tex` (aggiungere i pacchetti delle `\usepackage` non coperti dalla base). Poi eseguire `scripts/setup-tex.{ps1,sh}` per installare TinyTeX e i pacchetti, e `scripts/build.{ps1,sh}` per compilare. La procedura è incapsulata nella skill `latex-build`. L'engine è pdflatex, fissato in `.latexmkrc`: per documenti che richiedono fontspec/unicode-math passare a lualatex/xelatex modificando `.latexmkrc` e il manifesto.

L'auto-rilevamento del file principale (`build.ps1`/`.sh` senza argomenti) cerca un solo `.tex` nella radice del progetto: se il documento vive altrove, per esempio `docs/relazione.tex`, va passato esplicitamente con `-Main docs\relazione.tex` (Windows) o `--main docs/relazione.tex` (Linux/macOS), path relativo alla radice. Verificato dal vivo (pilota 2026-07-02): la build passa senza altre modifiche.

Un secondo difetto, trovato eseguendo davvero lo script invece di limitarsi a `pdflatex` a mano (pilota 2026-07-03): quando `-Main`/`--main` punta a un file in una sottocartella, `latexmk` invocato senza `-cd` esegue `pdflatex` restando nella radice del progetto, e `pdflatex` scrive per default il PDF e tutti gli ausiliari (`.aux`, `.log`, `.fls`, `.synctex.gz`, `.fdb_latexmk`) nella directory corrente, non accanto al sorgente: la build riusciva, ma sporcava la radice del progetto invece di `docs/`, e il messaggio finale dello script dichiarava una posizione (`docs/diploma.pdf`) diversa da quella reale. Corretto aggiungendo `-cd` a ogni invocazione di `latexmk` in `build.ps1` e `build.sh`, che gli fa cambiare directory di lavoro in quella del file principale prima di compilare: verificato dal vivo, ora il PDF e gli ausiliari finiscono correttamente accanto al `.tex` sorgente.

## Non versionato

La distribuzione TinyTeX (default `%APPDATA%\TinyTeX` su Windows, `~/.TinyTeX` su Unix) e il PDF e gli ausiliari di compilazione sono derivati: restano fuori da git.

## Attriti osservati dal vivo (pilota 2026-07-02)

Su un TinyTeX già installato ma non aggiornato di recente, `tlmgr install <pacchetto>` può rifiutarsi con "tlmgr itself needs to be updated": va lanciato prima `tlmgr update --self`, che può restare silenzioso per una manciata di secondi prima di completare, poi si ripete il comando di installazione. Inoltre, un documento che unisce `psnfss`/`times` a `\texttt` su un preambolo `fontenc` T1 fallisce con "Font T1/pcr/.../not loadable: Metric (TFM) file not found" se manca il pacchetto `courier`: TinyTeX, a differenza di una TeX Live completa, non lo installa di default insieme a `psnfss`. Il manifesto base in `tex-packages.txt` documenta ora questa coppia.

## Capitoli tecnici del progetto

Le fonti editoriali sono il [confronto fra crossover](../62-confronto-crossover-e-verifica-matematica.md) il [progetto delle modalità PC e autonoma](../63-sistema-autonomo-driver-e-collaudo.md) e il [completamento reflex e CAD](../64-reflex-direttivita-e-cabinet-nominale.md). Modificare il Markdown e rigenerare i rispettivi file TeX con [converti.py](converti.py). La rigenerazione sostituisce eventuali modifiche fatte direttamente ai TeX.

Il preambolo comune usa i font Altro Serif Light e Altro Grotesk Book e Medium dal kit locale Intrawelt, Consolas installato nel sistema e Latin Modern Math per la matematica. `intrawelt-header.tex` indica la radice dei font Altro e accetta `\AltroFontPath` come sostituzione. Per compilare si usano TinyTeX e latexmk del pacchetto LaTeX già adottato dal progetto, con LuaLaTeX per questi capitoli. L'ambiente verificato comprende Pandoc 3.12, latexmk 4.88, LuaHBTeX 1.24.0 della distribuzione TeX Live 2026 e i pacchetti `amsmath`, `amsfonts`, `babel` con italiano, `bookmark`, `booktabs`, `caption`, `etoolbox`, `fontspec`, `geometry`, `graphics`, `hyperref`, `listings`, `lm`, `titlesec`, `tools`, `unicode-math` e `xcolor`.

Il capitolo 62 incorpora `lr4-modulo-fase.pdf` e `cammino-e-somma.pdf` da `build/studio-crossover-20261120-v2/`. Il capitolo 63 incorpora `confronto-driver.pdf` da `build/sistema-autonomo-20261120-v5/`. Il capitolo 64 incorpora quattro grafici da build/completamento-20261125-figure. I comandi di riproduzione nei capitoli sorgente generano i grafici vettoriali con i dati dei modelli, quando le rispettive directory non sono ancora presenti.

Eseguire dalla radice del repository con PowerShell.

```powershell
python docs/latex/converti.py 62 63 64
if ($LASTEXITCODE -ne 0) { throw 'Conversione Pandoc fallita' }
New-Item -ItemType Directory -Force -Path build/relazione-audio-20261120
$cacheTexPrecedente = $env:TEXMFCACHE
Push-Location docs/latex
try {
    $env:TEXMFCACHE = (Resolve-Path '../../build/relazione-audio-20261120').Path
    latexmk -lualatex -interaction=nonstopmode -halt-on-error -file-line-error '-outdir=../../build/relazione-audio-20261120' crossover-pc-pi-analogico.tex sistema-autonomo-driver-e-collaudo.tex reflex-direttivita-cabinet.tex
    if ($LASTEXITCODE -ne 0) { throw 'Compilazione LuaLaTeX fallita' }
} finally {
    $env:TEXMFCACHE = $cacheTexPrecedente
    Pop-Location
}
```

Il compilatore usa `build/relazione-audio-20261120/` soltanto per intermedi, log e cache font. I PDF correnti consegnati sono `docs/pdf/crossover-pc-pi-analogico.pdf` e `docs/pdf/sistema-autonomo-driver-e-collaudo.pdf`; dopo compilazione si copiano, si confrontano le impronte e si rimuovono i PDF intermedi. Il quarto PDF, `docs/pdf/recap-progetto.pdf`, deriva da STATO-PROGETTO.md con WordCraft. Il manifesto in docs/pdf registra i sorgenti e le impronte. I collegamenti sono relativi alla collocazione finale. Le immagini renderizzate per il controllo sono temporanee e vengono eliminate dopo l'ispezione.

### Problemi osservati su Windows

Il comando corrente che orchestra anche la copia verificata e il manifesto è `python tools/consegna_documenti.py`. Riusa WordCraft per il recap, Pandoc/LuaLaTeX per le relazioni e PdfCraft per metadati/testo; rigenera soltanto le consegne con input cambiati. I comandi sopra restano la compilazione LaTeX elementare. `python tools/consegna_documenti.py --check` richiede impronte correnti e QA visivo registrato. Dopo avere realmente ispezionato le pagine cambiate si usa `--conferma-qa nome.pdf --pagine 1,3`; il comando registra il gesto, non lo esegue. Non vengono prodotte immagini di ogni pagina: le singole immagini eventualmente renderizzate si eliminano dopo l'ispezione. La nuova compilazione può cambiare il numero di pagine; il manifesto conserva quello effettivo.

- `no writeable cache path` indica che LuaLaTeX richiede una cache font scrivibile. Il comando imposta `TEXMFCACHE` nella directory di build per la durata della compilazione.
- Se latexmk tenta di aprire `../../build/` come directory di lavoro, controllare che l'intero argomento `'-outdir=…'` sia racchiuso tra apici. Windows PowerShell 5.1 altrimenti lo può dividere in due argomenti.

La selezione dei font dei grafici e delle tavole usa tools/font_intrawelt.py, con risorsa esplicita, INTRAWELT_FONT_DIR oppure installazione di account/sistema; non richiede una copia nel vecchio kit build. tools/test_ricostruzione_sorgenti.py esercita il caso da sorgenti isolati. Il compilatore LuaLaTeX conserva il preambolo di account e la possibilità di sostituire AltroFontPath. Le prove autonome del manifesto usano byte costruiti; la produzione del kit richiede i file CAD e PDF realmente verificati.
