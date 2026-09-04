# Registro dei microstep

> Tracciamento cronologico degli interventi, un microstep per voce. Ogni voce dichiara che cosa è stato fatto, come è stato verificato e con quale esito. La verifica è la parte che conta: un microstep senza esito verificato resta aperto, e la colonna dell'esito non contiene mai una previsione.

## Convenzione

Ogni microstep ha un identificativo progressivo nella forma `MS-NNN`, una data, un titolo, il perimetro dei file toccati, il comando o l'osservazione con cui è stato verificato, e l'esito. Gli stati possibili sono `fatto` quando la verifica è passata, `bloccato` quando la verifica non è eseguibile per una dipendenza esterna, e `aperto` quando il lavoro è iniziato e non concluso. Un microstep bloccato dichiara sempre da che cosa dipende.

Le voci si aggiungono in ordine cronologico crescente, così che il registro si legga come una storia. Non si riscrive una voce passata: se un intervento successivo la corregge, si aggiunge una voce nuova che dichiara di superarla.

## 2026-09-04, sessione di allineamento e conversione

### MS-001 - Ricognizione dello stato reale

Perimetro: sola lettura su questo progetto, sul template `template-claude-developing`, sul progetto gemello `home-recording-training-mixing-setup` e sulla rete locale.

Rilevato: il progetto era in pari con il proprio remoto ma indietro di sette commit rispetto al template; i materiali pesanti ammontavano a 159 MiB in una cartella ignorata da git; il documento sorgente `.docx` non era ancora stato convertito e non esisteva alcuna cartella `docs/`; la macchina Ubuntu Studio non era raggiungibile in rete.

Verificato con: `git rev-list --left-right --count origin/main...HEAD` che ha restituito zero e zero, `du -sh` sulle cartelle di radice, `diff -rq` fra gli alberi `.claude` dei due progetti, e la diagnostica di rete riportata in MS-008.

Esito: fatto.

### MS-002 - Allineamento al template

Perimetro: `.claude/rules/` con tutte e sette le regole, `.claude/PROJECT-SYSTEM.md`, i due prompt di sistema, `.claude/skills/` e l'intero catalogo `.claude/templates/`.

I sette commit del template da propagare portavano tre pacchetti nuovi, cioè `md-unwrap`, `fix-typography` e `community-sources`, la regola nuova `web-sources-not-fetchable.md`, e la conversione degli accenti posticci in accenti veri su tutto il corpus normativo. Verificato prima della copia che il template non avesse rimozioni né rinomine dopo la base comune, con `git diff --name-status`, così che la copia in sovrascrittura fosse equivalente a una sostituzione.

Deliberatamente non toccati: `.claude/settings.json`, che è già istanziato correttamente con il nome di questo progetto, `.claude/settings.local.json`, `.claude/agents/`, `CLAUDE.md` e `README.md`, che sono specifici del progetto.

Esito: fatto.

### MS-003 - Re-istanziazione dei valori di macchina nella regola di identità git

Perimetro: `.claude/rules/git-identity-and-repo.md`.

La versione del template è genericizzata con segnaposto, quindi la copia aveva sostituito i valori reali con `<user-personale>` e simili. Ripristinati i valori concreti leggendoli dalla configurazione effettiva invece di ricordarli: identità personale `alesop95` con la sua email, identità di lavoro `asopranzi` con la sua, alias SSH e organizzazione. Aggiunta la terza directory di account presente sulla macchina, che il template non contemplava.

Corretta inoltre una affermazione errata che la copia aveva introdotto: il testo attribuiva questo repository al profilo di lavoro, mentre la configurazione locale mostra l'identità personale.

L'email associata alla seconda directory di account non è stata verificata in questa sessione, quindi il testo la dichiara come da leggere con `/status` invece di indicarne una.

Verificato con: `git config --local --list`, e conteggio dei segnaposto residui, che è zero.

Esito: fatto.

### MS-004 - Istanziazione degli strumenti di verifica

Perimetro: `tools/md-unwrap.py`, `tools/lint-md-commands.py`, e i quattro strumenti tipografici nuovi.

Trovata una deriva interna al template: il commit `219473f` ha migliorato le copie in `tools/` alla radice del template, aggiungendo il riconoscimento degli identificatori LaTeX e del front matter YAML, ma non le ha ripropagate nel pacchetto `templates/fix-typography/tools/`, che è la sorgente canonica di istanziazione. Le due copie differiscono di circa tre kilobyte per file. Istanziate le versioni più recenti, cioè quelle di `tools/` del template.

Verificato con: `python tools/test-tipografia.py`, che riporta zero controlli falliti, e `python .claude/templates/md-unwrap/tests/run-tests.py`, che riporta 106 test passati e zero falliti con l'oracolo di rendering attivo.

Esito: fatto.

### MS-005 - Estrazione integrale del documento sorgente

Perimetro: sola lettura su `full_electroacoustics.docx`, con estrazione in un file di lavoro temporaneo fuori dal progetto.

Il documento contiene 507 paragrafi, 4 tabelle, 1 immagine e circa 10.100 parole. Estratti e letti tutti i 507 paragrafi con il loro stile, tutte e quattro le tabelle integralmente riga per riga, e la struttura completa dei titoli su nove livelli di profondità.

Verificato con: conteggio dei paragrafi confrontato fra estrazione e sorgente, e lettura di ogni intervallo di paragrafi fino a copertura totale. La copertura per sezione è documentata in MS-006.

Esito: fatto.

### MS-006 - Conversione in albero di documentazione

Perimetro: `docs/` con venti file Markdown.

Il contenuto è stato riorganizzato secondo la struttura del progetto e non secondo quella del documento, separando tre piani che nel sorgente erano un unico flusso: la teoria del workflow, la cronaca dell'ambiente e le schede dei singoli strumenti. Le sequenze che nel sorgente erano elenchi puntati sono state promosse a prosa, secondo la regola di stile del progetto; le tabelle sono state conservate come tabelle perché lì l'a capo è strutturale.

Scartati soltanto i paragrafi segnaposto privi di contenuto, cioè le sequenze di lettere ripetute che l'autore aveva lasciato come promemoria. Le sezioni marcate come da verificare nel sorgente restano marcate come tali, e nessuna è stata promossa a fatto.

Cinque incoerenze del sorgente sono state rilevate e trattate esplicitamente invece di essere ricopiate. Lo schema finale delle partizioni indicava due filesystem sullo stesso punto di montaggio, corretto e segnalato nella pagina di installazione. Akabak era descritto in un punto come software a 16 bit e in un altro correttamente come 3.x a 64 bit, chiarito nella pagina dei programmi. Un prefix Wine era proposto annidato dentro un altro prefix, segnalato come da evitare nella pagina di troubleshooting. Il tweeter era indicato da quattro pollici come il woofer, misura fuori scala, segnalata come errore di trascrizione nella pagina di progettazione. La scelta fra le catene di simulazione Pachyderm e Octave era lasciata aperta, risolta nella pagina della fase 2 con la ragione dell'esclusione.

Verificato con: `python tools/md-unwrap.py --check docs/`, venti file esaminati e zero da modificare; `python tools/lint-md-commands.py docs/`, zero errori e zero avvisi; la catena tipografica sui tre strumenti, zero modifiche necessarie.

Esito: fatto.

### MS-007 - Blocco ambiente condiviso e sua propagazione

Perimetro: `docs/10-ambiente/` con otto file, `tools/sync-ambiente.py`, e la copia nel progetto gemello.

Il materiale sull'ambiente serve a due progetti, perché la stessa macchina è usata per la progettazione elettroacustica e per l'home recording. Invece di duplicarlo a mano è stato isolato in un blocco con una copia canonica e uno strumento di propagazione unidirezionale, che marca ogni copia con una intestazione che ne dichiara la provenienza e rileva i file orfani senza rimuoverli.

La direzione unidirezionale è una scelta: una sincronizzazione bidirezionale richiederebbe risoluzione dei conflitti, che a due copie non vale il costo.

Verificato con: `python tools/sync-ambiente.py --check` eseguito prima della propagazione, che ha riportato otto file da propagare ed è uscito con codice 1; poi la propagazione; poi lo stesso comando di controllo, che riporta otto file allineati, zero da propagare, zero orfani, ed esce con codice 0.

Esito: fatto.

### MS-008 - Diagnosi della rete verso la macchina Ubuntu Studio

Perimetro: sola diagnostica di rete dalla postazione Windows.

L'host `192.168.10.204` non risponde. Quattro osservazioni indipendenti concordano: l'indirizzo non compare nella tabella ARP mentre i vicini `.203` e `.205` ci sono; il ping restituisce host di destinazione non raggiungibile generato dall'interfaccia locale stessa; la connessione alla porta 22 va in timeout; la traccia dell'instradamento si ferma sull'interfaccia locale.

La sottorete è compatibile, perché la postazione ha indirizzo `192.168.10.73` con maschera `255.255.224.0`, quindi il bersaglio cade nell'intervallo diretto. La rete presenta più segmenti e un numero di host tipico di un ufficio.

Conclusione: la macchina non è accesa oppure non è collegata a questo segmento. Non è un problema di chiave né di configurazione SSH.

Esito: fatto, con l'esito negativo. Tutti i microstep che dipendono dall'accesso alla macchina restano bloccati da questo.

### MS-009 - Preparazione del trasferimento dei materiali pesanti

Perimetro: `docs/TRANSFER-MANIFEST.md`, `tools/transfer-to-studio.sh`, `tools/transfer-to-studio.ps1`.

Redatto il manifest di otto file per circa 166 MiB, con destinazione sotto `/home` sulla macchina, scelta perché quella partizione è separata e sopravvive alla reinstallazione pulita del sistema. Calcolate e registrate le impronte SHA-256 di tutti i file di origine. Escluse dal manifest, con la motivazione, le copie con protezione rimossa presenti nel pacchetto software ereditato.

Gli strumenti verificano la raggiungibilità dell'host, la corrispondenza fra manifest e disco e lo spazio disponibile sulla destinazione prima di copiare, e ricalcolano le impronte dopo. Non cancellano nulla sull'origine.

Durante la prova è emerso che `rsync` non è disponibile in Git Bash su Windows: lo strumento è stato modificato per degradare su `scp`, dichiarando la perdita della ripresa di un trasferimento interrotto. Nella versione PowerShell è emerso che `$ErrorActionPreference` impostato a `Stop` promuove la diagnostica di `ssh` su stderr a errore terminante, abortendo lo script prima dei suoi percorsi d'errore puliti: corretto impostando `Continue` e verificando esplicitamente il codice di uscita di ogni comando nativo.

Verificato con: `bash -n` sulla sintassi, poi entrambi gli strumenti in modalità di sola verifica. Entrambi riportano otto file presenti per 158 MiB e si fermano sull'host irraggiungibile con codice di uscita 2, che è il comportamento progettato.

Esito: fatto per la preparazione. L'esecuzione resta bloccata da MS-008.

### MS-010 - Correzione del gitignore

Perimetro: `.gitignore`.

I pattern per tipo di file erano globali invece che ancorati alla radice, e nascondevano per errore file che devono essere versionati: `tools/dashes-exclude.txt` appena istanziato, `.claude/templates/fix-typography/tools/dashes-exclude.txt`, `.claude/templates/latex/tex-packages.txt`, `.claude/templates/automation-starter/workflows/automation-routine-prompt.txt` e il modello `.claude/templates/CLAUDE.local.md`. Gli ultimi due erano già assenti dalla storia del repository per questo motivo.

I pattern sono stati ancorati alla radice, dove sta il materiale scritto a mano che l'intenzione originaria voleva escludere; la cartella dei materiali pesanti è stata esclusa in modo esplicito con il proprio nome; gli eseguibili e gli archivi restano esclusi globalmente perché non vanno versionati in nessuna cartella.

Aggiunta una negazione per i `_notes` sotto `.claude/templates/`, che non sono appunti reali ma i modelli da cui si istanziano, e che senza negazione un clone perderebbe. È una divergenza voluta dal template di origine, che ha lo stesso difetto, ed è annotata come tale nel file perché va propagata all'indietro.

Verificato con: `git check-ignore` su ciascun file interessato, che ora li dichiara tracciabili, e sui materiali pesanti e sugli appunti di radice, che restano correttamente ignorati. Verificato inoltre che un file dentro il `_notes` reale del progetto resti ignorato, così che la negazione non abbia allargato troppo.

Esito: fatto.

### MS-011 - Verifica di copertura e archiviazione del documento sorgente

Perimetro: `docs/90-riferimenti/copertura-sorgente.md`, e spostamento del `.docx` dalla radice a `_notes/`.

Prima di togliere il sorgente dalla radice è stata prodotta la prova di copertura, perché rimuoverlo senza quella prova significherebbe fidarsi della memoria. Classificati tutti i 507 paragrafi: 71 titoli, 387 paragrafi di contenuto, 29 vuoti e 22 segnaposto, questi ultimi elencati uno per uno con la loro posizione. Mappata ciascuna delle 71 sezioni al file di destinazione, distinguendo le sezioni contenitore da quelle che nel sorgente erano genuinamente vuote e dichiarando per queste come sono state trattate. Distinto inoltre il materiale che nell'albero `docs/` non proviene dal `.docx`, cioè gli appunti della conversazione del 2024, l'inventario del pacchetto software e la pagina sull'aggiornamento alla LTS.

Le sole informazioni non trasferite sono i paragrafi vuoti, i segnaposto e una delle due formule della sezione su Octave, che nel file esisteva solo come immagine. La pagina della fase 3 dichiara questa perdita invece di ricostruire la formula a memoria.

Il documento è stato quindi spostato sotto `_notes/`, che è ignorato da git, e non distrutto: resta la fonte di rigenerazione e resta nel manifest di trasferimento verso la macchina.

Verificato con: l'impronta SHA-256 ricalcolata dopo lo spostamento, identica a quella registrata nel manifest, e il controllo che la radice non contenga più il file.

Esito: fatto. La rimozione definitiva del file, se e quando la si volesse, è ora una decisione senza rischio di perdita di contenuto.

### MS-012 - Impianto del contesto versionato e della roadmap

Perimetro: `.claude/context/` con tre schede, `.claude/memory/` con tre file, `CLAUDE.md` e `README.md`.

Create le schede `STACK.md`, `roadmap.md` e `current-work.md` con il frontmatter di riconciliazione ancorato al commit corrente. Deliberatamente non create le schede `design-and-security.md`, `deployment.md` e `dev-testing.md`: il progetto non ha codice applicativo né superficie di attacco, non ha deploy, e i suoi test sono le suite degli strumenti. La scelta è dichiarata nello snapshot invece di lasciare tre file vuoti.

La roadmap non ordina le fasi del workflow, che hanno un ordine proprio, ma le priorità reali del progetto, e la prima non è di progetto: rimettere in servizio la macchina, perché una macchina su un rilascio fuori supporto accumula attrito a ogni intervento successivo. La seconda è il trasferimento dei materiali, da eseguire prima della reinstallazione e non dopo, perché la destinazione è sotto `/home`.

Nel registro delle decisioni sono state formalizzate sei voci. Tre riguardano scelte già implicite nel documento sorgente e mai scritte come decisioni: progettare a partire dalla stanza, Wine invece di una macchina virtuale, un prefix per programma senza prefix a 32 bit. Due riguardano scelte di questa sessione: il blocco documentale condiviso con propagazione unidirezionale, e l'adozione del sistema di progetto. La sesta, l'installazione pulita della LTS, è registrata come proposta e non come accettata, perché la diagnosi su cui si fonda non è verificata sulla macchina.

Riscritti `README.md`, che era descritto come contenitore in fase di ricerca e ora descrive un progetto con documentazione, e `CLAUDE.md`, che ora indicizza i satelliti tracciati, riporta la sequenza di verifica prima di un commit, e avverte della trappola del `.gitignore` corretta in MS-010.

Esito: fatto.

### MS-013 - Innesto nel progetto gemello

Perimetro: nel progetto `home-recording-training-mixing-setup`, la cartella `docs/` con il suo indice, `CLAUDE.md` e `README.md`.

Il blocco sull'ambiente era stato propagato in MS-007 ma il progetto gemello non lo indicizzava, quindi nessuno lo avrebbe trovato. Aggiunto un indice che spiega da dove arriva il blocco, perché non va modificato lì, e quali sue tre parti riguardano direttamente l'home recording e non soltanto il progetto dei monitor, cioè la catena audio, lo schema di partizionamento e la decisione sull'aggiornamento del sistema. Dichiarato anche che la parte su Wine è meno pertinente in quel contesto, invece di lasciarla passare come se lo fosse.

Aggiornati `CLAUDE.md` con l'avvertenza di non modificare la copia, e `README.md`, che dichiarava il repository sostanzialmente vuoto e ora dichiara il primo contenuto tecnico reale.

Applicata la catena tipografica anche su quei file, e verificato subito dopo che la normalizzazione non avesse introdotto deriva nel blocco sincronizzato, cosa che sarebbe accaduta se avesse toccato le copie invece dei soli file nuovi.

Verificato con: `python tools/md-unwrap.py --check` sugli undici file del gemello, zero da modificare, e `python tools/sync-ambiente.py --check`, che riporta otto file allineati e nessuna deriva.

Esito: fatto.

### MS-014 - Due difetti degli strumenti tipografici, isolati con casi minimi

Perimetro: diagnosi sugli strumenti sotto `tools/`, più la correzione di due occorrenze in `tools/sync-ambiente.py`.

Eseguendo la catena tipografica sull'intero progetto, cioè su `.` e non sui soli file Markdown, sono comparse in alcuni file forme con l'accento seguito da un apostrofo orfano, del tipo `c'è'` e `perché'`. La prima ipotesi, che fosse un danno introdotto dalla catena, è stata verificata e in gran parte smentita: confrontando con il template di origine, quindici delle diciassette occorrenze erano già lì, quindi ereditate e prodotte da una versione precedente degli strumenti. Le sole due nuove erano in `tools/sync-ambiente.py`, scritto in questa sessione, e sono state corrette.

Isolata la causa con un caso minimo invece di dedurla. Su un file `.py` che contiene sette forme, `fix-accents.py` converte correttamente `perche'`, `e'`, `piu'`, `puo'` e `la'`, consumando l'apostrofo, ma salta di proposito `c'e'` e `com'e'`, perché la sua regola di prudenza per i file di codice esclude una parola preceduta da apostrofo, dato che in un file Python quell'apostrofo può essere un delimitatore di stringa. Subito dopo `fix-missing-accents.py` incontra la `e` nuda che segue l'elisione, la converte in `è` perché senza accento non sarebbe una parola, e lascia l'apostrofo finale orfano, producendo `c'è'` e `com'è'`.

Il difetto non è quindi in uno dei due strumenti ma nell'incoerenza fra le loro regole di prudenza: il primo si astiene, il secondo no, e la catena dei due corrompe ciò che nessuno dei due corromperebbe da solo. Sui file `.md` il problema non si presenta, perché lì `fix-accents.py` gestisce anche le forme elise.

Il secondo difetto è indipendente e più semplice: entrambi gli strumenti terminano con `ValueError: path is on mount 'C:', start on mount 'E:'` quando ricevono un percorso su un'altra lettera di unità, perché calcolano un percorso relativo alla radice del progetto senza gestire il caso cross-disco. È lo stesso difetto che `md-unwrap.py` aveva e che nel template è stato corretto per quello strumento e non per questi.

Le quindici occorrenze ereditate non sono state corrette qui. La correzione è deterministica, ma quei file arrivano dal template e ripararli in questo progetto creerebbe una divergenza da inseguire: il posto giusto è il template, e la voce è registrata fra le domande aperte in `.claude/context/current-work.md`. Va notato che gli strumenti attuali non le riconoscono più, perché cercano la forma con apostrofo e non quella già accentata: il danno non si autoripara rilanciando la catena.

Conseguenza operativa adottata subito: la sequenza di verifica documentata in `CLAUDE.md` e in `.claude/context/STACK.md` non include l'esecuzione della catena tipografica su `.`, e la catena si esegue sui soli file Markdown.

Verificato con: i casi minimi eseguiti su file temporanei sotto `_notes/`, poi rimossi; il confronto delle occorrenze fra questo progetto e il template; e il conteggio a zero delle occorrenze nei file scritti in questa sessione.

Esito: fatto per la diagnosi e per la correzione dei file propri. La correzione del template resta una domanda aperta per l'utente.

## Microstep bloccati, in attesa di accesso alla macchina

Questi microstep sono progettati e documentati ma non eseguibili finché MS-008 non si risolve. Sono elencati qui, senza numero definitivo, così da non essere confusi con lavoro fatto.

L'esecuzione del trasferimento dei materiali, con verifica delle impronte sulla destinazione, secondo `docs/TRANSFER-MANIFEST.md`.

La conferma della diagnosi di blocco dell'aggiornamento di rilascio, eseguendo sulla macchina la sequenza di comandi in sola lettura di `docs/10-ambiente/ubuntu-lts-upgrade.md` e confrontando gli esiti reali con quelli attesi.

L'installazione pulita di Ubuntu Studio 26.04 LTS conservando `/home`, oppure la strada dell'aggiornamento in posto in due salti, secondo la decisione presa dopo la conferma della diagnosi.

La ricostruzione dell'ambiente Wine secondo `docs/10-ambiente/wine-configurazione.md`, con un prefix per programma e la reinstallazione di Akabak e VACS con il release code esistente.

La verifica che il release code di Akabak sia ancora valido dopo la reinstallazione, che è la prova pratica dell'affermazione sulla licenza legata alla macchina.
