# Schema della LLM Wiki

> Costituzione di questa wiki. Definisce i tipi di pagina, come si collegano, quando si aggiornano e come si gestiscono le contraddizioni. La skill `wiki-digest` segue questo schema a ogni ingestione. Questo file è la fonte di verità del comportamento della wiki.

## In questo progetto: che cosa resta locale

Sezione di progetto aggiunta il 2026-10-01 con ADR-028. Il repository è pubblico, e le fonti di questa wiki sono i libri e gli appunti dell'utente, alcuni dei quali di provenienza che non consente di ridistribuirli. Per questo `sources/` e `wiki/` sono nel `.gitignore` e non entrano mai nella storia di git: diversamente dal default del pacchetto, qui la wiki compilata resta locale come le fonti, perché le sue pagine sono sintesi di quei libri. Restano tracciati soltanto questo schema e `log.md`, che registra che cosa è stato ingerito e quando, senza riprodurre contenuto. Le skill generate da `book-digest` prendono uno slug con il prefisso `libro-`, per esempio `libro-self-small-signal`, così che il `.gitignore` le escluda insieme ai loro wrapper per Codex. Le conversioni in Markdown fatte da `tools/doc-ingest.py` stanno nella cache `_notes/.tmp-doc-cache/`, e le copie dei file originali in `_notes/fonti-studio/`, entrambe sotto `_notes/`, già ignorata. Il report LaTeX cita queste fonti in bibliografia e non ne riproduce il testo.

## Principio

La wiki non è un archivio di documenti da cercare, ma una knowledge base già sintetizzata e collegata. Le fonti grezze stanno in `sources/`, immutabili; le pagine in `wiki/` sono il prodotto compilato. La manutenzione, cioè sintetizzare, collegare e rilevare contraddizioni, è delegata all'LLM tramite `wiki-digest`, non fatta a mano.

## Tipi di pagina

`wiki/concepts/<concetto>.md` per i concetti e i modelli mentali. `wiki/entities/<entita>.md` per persone, prodotti, aziende, tecnologie. `wiki/sources/<fonte>.md` per il riassunto di una singola fonte ingerita. Ogni pagina ha un titolo, un sommario denso, i collegamenti alle pagine correlate e i riferimenti alle fonti da cui deriva.

## Collegamenti

Le pagine si collegano tra loro con link markdown relativi, per esempio `[replication](../concepts/replication.md)`. Ogni concetto cita le fonti che lo trattano e le altre pagine con cui è in relazione. Il valore della wiki sta nella densità dei collegamenti: una pagina isolata vale poco.

## Quando aggiornare

A ogni ingestione di una nuova fonte, `wiki-digest` aggiorna le pagine esistenti toccate dal nuovo contenuto, crea le pagine nuove per i concetti o le entità non ancora presenti, e aggiorna i collegamenti reciproci. Non si rigenera la wiki da zero: si fanno modifiche mirate.

## Contraddizioni

Quando una nuova fonte contraddice una pagina esistente, non si sovrascrive in silenzio: si registra la divergenza nella pagina, citando entrambe le fonti e la data, e si marca il punto come da risolvere. Una conoscenza superata si aggiorna dichiarando cosa la supera, non cancellandola senza traccia.

## Stile

Sommari densi, voce da praticante ("usa X quando Y", non "la fonte dice X"), mai testo grezzo copiato: sempre sintesi ed estrazione di segnale. Le pagine si scrivono per essere lette sia da un LLM sia da un umano, dense e senza ridondanza, coerentemente con la regola di stile del sistema.

## Regola sulle fonti

`sources/` è append-only: una fonte ingerita non si modifica e non si cancella. Se una fonte va corretta, si aggiunge una nuova versione e lo si annota nel `log.md`. Questo tiene la wiki ricostruibile dalle fonti.
