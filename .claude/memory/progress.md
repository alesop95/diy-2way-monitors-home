# Work-log

> Append-only, in ordine cronologico inverso: la voce più recente in alto. Ogni passo significativo lascia una voce con data, file toccati, motivo e commit di riferimento. Il dettaglio tecnico degli interventi, con l'esito verificato di ciascuno, sta in `docs/OPERATIONS-LOG.md`; qui sta il meta-stato.

## 2026-09-04 - Impianto del progetto: allineamento, conversione, ambiente

Commit di partenza: 0df04bb. Commit di arrivo: da assegnare, il lavoro non è ancora committato.

File toccati: `.claude/rules/` tutte e sette le regole, `.claude/PROJECT-SYSTEM.md`, i due prompt di sistema, `.claude/skills/`, l'intero `.claude/templates/`, le tre schede nuove sotto `.claude/context/`, i tre file di `.claude/memory/`, l'albero `docs/` con ventitré file, sei script sotto `tools/`, `.gitignore`, `CLAUDE.md`, `README.md`. Spostato `full_electroacoustics.docx` dalla radice a `_notes/`.

Motivo: il progetto era indietro di sette commit rispetto al template, il documento sorgente non era stato convertito, i materiali pesanti stavano sul disco di sviluppo invece che sulla macchina di lavoro, e il `.gitignore` nascondeva per errore file che devono essere versionati.

Esito in sintesi. Quattordici microstep chiusi con verifica, tracciati come MS-001 a MS-014 in `docs/OPERATIONS-LOG.md`. Cinque microstep progettati ma bloccati dall'irraggiungibilità della macchina Ubuntu Studio, elencati nello stesso registro.

Tre difetti trovati e corretti in questo progetto. Il `.gitignore` con pattern globali invece che ancorati alla radice, che escludeva strumenti e modelli da versionare. La regola di identità git tornata genericizzata dopo la copia dal template, con in più una attribuzione errata del profilo di questo repository. Cinque incoerenze interne al documento sorgente, corrette e segnalate nelle pagine di destinazione invece di essere ricopiate.

Quattro difetti trovati nel template di origine e non ancora propagati all'indietro. Il pacchetto `fix-typography` contiene versioni degli strumenti più vecchie delle copie in `tools/` alla radice del template, quindi istanziare dal pacchetto darebbe strumenti peggiori. I modelli `_notes` sotto `.claude/templates/` non sono versionati perché il `.gitignore` del template li esclude con un pattern globale, quindi un clone del template li perde. Le regole di prudenza di `fix-accents.py` e `fix-missing-accents.py` sono incoerenti fra loro sui file di codice, e la catena dei due lascia un apostrofo orfano su forme come `c'e'`: il danno è già presente in quindici punti dei sorgenti del template. I tre strumenti tipografici terminano con un errore su percorsi cross-disco, difetto che `md-unwrap.py` ha già corretto. Tutti e quattro sono annotati come domanda aperta in `.claude/context/current-work.md`, e gli ultimi due sono diagnosticati con casi minimi in MS-014.

Riconciliazione del documento sorgente: `full_electroacoustics.docx`, 507 paragrafi, 4 tabelle, 1 immagine, circa 10.100 parole. Copertura integrale verificata e documentata in `docs/90-riferimenti/copertura-sorgente.md`. Non trasferiti soltanto 29 paragrafi vuoti, 22 segnaposto e una formula presente solo come immagine, tutti dichiarati uno per uno. Il sorgente è stato archiviato sotto `_notes/`, non distrutto, con impronta SHA-256 verificata identica dopo lo spostamento.

## Precedente al 2026-09-04

Il progetto esisteva come impalcatura standard con `CLAUDE.md`, `README.md` e il sistema `.claude/` istanziato, senza documentazione tecnica propria. Il remoto GitHub era già collegato tramite l'alias SSH personale e il repository era in pari. Il materiale di progetto viveva alla radice come file di testo e un documento `.docx`, tutto ignorato da git.
