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

Cinque incoerenze del sorgente sono state rilevate e trattate esplicitamente invece di essere ricopiate. Lo schema finale delle partizioni indicava due filesystem sullo stesso punto di montaggio, corretto e segnalato nella pagina di installazione. Akabak era descritto in un punto come software a 16 bit e in un altro correttamente come 3.x a 64 bit, chiarito nella pagina dei programmi. Un prefix Wine era proposto annidato dentro un altro prefix, segnalato come da evitare nella pagina di troubleshooting. Il tweeter era indicato da quattro pollici come il woofer, misura fuori scala, segnalata come errore di trascrizione nella pagina di progettazione. La scelta fra le catene di simulazione Pachyderm e Octave era lasciata aperta, risolta nella pagina della fase 2 con la ragione dell'esclusione. Tutte e cinque sono spiegate nel dettaglio, con il testo originale e il metodo per riconoscere quella classe di errore, in MS-017 e in `docs/90-riferimenti/incoerenze-sorgente.md`.

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

Nota aggiunta a posteriori: la conclusione era incompleta. I fatti osservati erano corretti, ma la causa era la sospensione automatica della macchina e non lo spegnimento né un altro segmento di rete. La correzione è in MS-015, che spiega perché una macchina sospesa scompare anche dalla tabella ARP e produce esattamente questo quadro. La seconda parte della conclusione, cioè che non fosse un problema di configurazione SSH, si è rivelata a sua volta errata una volta risvegliata la macchina: si veda MS-016.

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

### MS-015 - La macchina non era spenta: era sospesa

Perimetro: diagnostica di rete dalla postazione Windows, nessuna modifica.

MS-008 aveva concluso che la macchina fosse spenta oppure su un altro segmento di rete. La conclusione era prudente ma incompleta, e l'ipotesi corretta l'ha fornita l'utente: la macchina si sospende da sola dopo un periodo di inattività, e questo è coerente con le osservazioni invece di contraddirle.

Il punto tecnico da capire è che una macchina sospesa non è una macchina che risponde male: è una macchina che non risponde affatto, nemmeno al livello più basso. L'interfaccia di rete in sospensione non risponde alle richieste ARP, quindi la postazione non riesce nemmeno a tradurre l'indirizzo IP in un indirizzo hardware, e il suo stesso stack di rete genera il messaggio di host non raggiungibile senza che un solo pacchetto lasci la scheda. È esattamente il quadro registrato in MS-008, con gli indirizzi vicini presenti nella tabella ARP e il suo assente: non era il sintomo di una macchina altrove, era il sintomo di una macchina addormentata.

Alla ripresa dell'attività la situazione si è invertita in modo netto. Una scansione della sottorete ha popolato la tabella ARP e la voce è comparsa, con indirizzo hardware `2c:4d:54:53:a4:fb`, prefisso che appartiene ad ASUSTek. Il ping ha risposto in meno di un millisecondo con TTL 64, valore che conferma un sistema Linux e non un intermediario.

Verificato con: `arp -a` filtrato sull'intorno dell'indirizzo, prima e dopo la scansione; `ping` con esito positivo e TTL 64.

Esito: fatto. MS-008 non era sbagliato nei fatti osservati ma incompleto nella conclusione, e questa voce la corregge.

### MS-016 - Il servizio SSH risponde, l'autenticazione no

Perimetro: diagnostica SSH dalla postazione, nessuna modifica su nessuna delle due macchine.

Con la macchina sveglia, la connessione alla porta 22 non va più in timeout: il servizio risponde e rifiuta con `Permission denied (publickey,password)`. Va letto con precisione, perché è un messaggio informativo e non un guasto: il servizio è attivo e raggiungibile, l'utente `alesop95` esiste, e i metodi di autenticazione accettati sono chiave pubblica e password. Ciò che è fallito è soltanto l'autenticazione.

La causa è stata isolata con la diagnostica verbosa di `ssh`, che elenca quali identità il client offre. Il client legge `~/.ssh/config` e non trova alcuna voce per questo host, quindi ripiega sui nomi di chiave predefiniti, cioè `id_rsa`, `id_ecdsa`, `id_ed25519` e le varianti con token hardware. Tutti risultano assenti, riportati con tipo `-1`. Le chiavi effettivamente presenti sulla postazione si chiamano `id_ed25519_personal` e `id_ed25519_corp`, e `ssh` non le prova perché nessuna configurazione gli dice di farlo per questo host.

Provate poi entrambe esplicitamente con `-i` e `IdentitiesOnly=yes`: nessuna delle due è autorizzata sulla macchina, quindi non è solo un problema di configurazione del client ma anche di chiave mai installata sul server.

Il contenuto delle chiavi non è stato letto in nessun momento: la regola `deny` del progetto vieta la lettura di `~/.ssh/**`, e la diagnosi è stata condotta interamente attraverso l'output di `ssh`, che dichiara i percorsi tentati senza esporre il materiale crittografico.

La soluzione, che richiede un passaggio interattivo con la password e quindi è dell'utente, è documentata come fase 10.3 della procedura di installazione pulita: una chiave dedicata a questo host, separata da quelle di GitHub, con una voce di configurazione che le dia un alias.

Esito: fatto per la diagnosi. L'accesso resta bloccato in attesa dell'installazione della chiave, ed è ora un blocco su un'azione dell'utente e non su uno stato ignoto.

### MS-017 - Le cinque incoerenze del sorgente, documentate una per una

Perimetro: `docs/90-riferimenti/incoerenze-sorgente.md`, e collegamenti dalle pagine di destinazione.

MS-006 aveva rilevato e corretto cinque incoerenze del documento sorgente, elencandole in una riga ciascuna. Questa voce le porta al livello didattico richiesto: per ognuna, che cosa diceva il sorgente con il testo originale, perché è tecnicamente sbagliato, come si riconosce l'errore, che cosa è vero e dove è finito nella documentazione.

Le cinque sono le due partizioni dichiarate sullo stesso punto di montaggio, con l'osservazione aggiuntiva che le due fonti interne al documento divergevano anche sulla dimensione della swap; Akabak descritto come software a 16 bit in un punto e correttamente come 3.x a 64 bit in un altro; un prefix Wine proposto annidato dentro un altro prefix, con le tre conseguenze che ne derivano e nessuna delle quali si manifesta subito; il tweeter da quattro pollici, che è un errore di ordine di grandezza e non di trascrizione; e la scelta fra le catene Pachyderm e Octave lasciata aperta quando il documento stesso conteneva, poche righe più in là, il requisito che rendeva la prima non eseguibile.

La pagina si chiude con una generalizzazione che è la parte utile: le cinque ricadono in tre tipi, cioè errore di trascrizione, errore di ordine di grandezza e decisione non presa travestita da elenco di alternative, e per ciascun tipo indica il metodo con cui si trova.

Esito: fatto.

### MS-018 - Approfondimento della pagina su Wine

Perimetro: `docs/10-ambiente/wine-vs-emulatore.md`, riscritta e ampliata.

La versione precedente enunciava correttamente le conclusioni ma non mostrava il meccanismo, e su una pagina da cui dipendono quattro decisioni architetturali questo non basta. L'ampliamento aggiunge il percorso concreto di avvio di un programma: il formato PE che Linux non saprebbe avviare da sé, Wine come caricatore, il codice macchina x86-64 che gira direttamente sul silicio perché è lo stesso del processore, e la traduzione che avviene sulle chiamate di libreria e non sulle istruzioni. Da lì spiega il rapporto numerico fra i due livelli, che è ciò che davvero spiega le prestazioni: il calcolo non paga nulla, le chiamate di sistema pagano un piccolo sovrapprezzo e sono relativamente poche.

Le tre conseguenze hanno ora una sezione ciascuna. Perché il profilo Windows 10 è una stringa in un registro finto letta con una chiamata di funzione, e perché è la scelta corretta e non un compromesso. Perché un prefix è una cartella ispezionabile con `ls` mentre una macchina virtuale è un file immagine opaco. E il meccanismo con cui Akabak calcola l'identificativo di macchina, seguito su questo caso reale invece che in astratto, perché è il punto da cui dipende la sopravvivenza della licenza.

La tabella di confronto è passata da nove a tredici righe, con l'aggiunta del livello a cui ciascun approccio traduce, del formato eseguibile, della forma tipica dei guasti e della comunicazione fra processi via COM, che è la riga che collega la pagina al limite scoperto in MS-019.

Verificato con: `python tools/md-unwrap.py --check docs/` e `python tools/lint-md-commands.py docs/`, zero errori.

Esito: fatto.

### MS-019 - Storico di Akabak e VACS dalla corrispondenza, e il limite delle pipeline COM

Perimetro: `docs/90-riferimenti/timeline-akabak-vacs.md`, `_notes/licenze-akabak-riservato.md`, e aggiornamenti a `wine-programmi-windows.md`, `60-simulazione-finale-akabak.md` e `licenze-e-registrazioni.md`.

Letti dodici screenshot della corrispondenza con l'autore del software, forniti dall'utente, e ricostruita la cronologia completa dal 13 agosto al 3 settembre 2025. Il valore di questa ricostruzione è che colma un punto preciso: il documento sorgente riportava la domanda iniziale e la prima risposta, e al paragrafo immediatamente successivo aveva un segnaposto. Tutto il seguito, cioè la parte in cui l'installazione fallisce, l'autore rivela un limite del suo software, l'installazione riesce e il codice viene verificato, non era da nessuna parte.

Sette fatti emersi, con la conseguenza operativa di ciascuno. Akabak e VACS sono già installati, licenziati e funzionanti dal 3 settembre 2025, quindi l'installazione pulita non è un primo impianto ma la ricostruzione di un percorso già percorso. La licenza è machine-based con codice permanente, e questa è la conferma dall'autore stesso dell'affermazione su cui poggia ADR-006. Un solo Release Code copre entrambi i programmi. L'inserimento richiede privilegi di amministratore, istruzione pensata per Windows che sotto Wine si traduce nella necessità di attivare con lo stesso utente e nello stesso prefix. Le versioni corrette sono AKABAK 3.2.4 b126 e VACS 2.1.3 b33, e questa è la conferma esterna che chiude l'incoerenza 2 del sorgente. VACS inizialmente non partiva e il modo in cui il problema fu risolto non è registrato, quindi resta una lacuna dichiarata e non riempita per ipotesi.

Il settimo fatto è il più importante e non era nel sorgente affatto: l'autore ha dichiarato che poiché Linux non supporta le pipeline COM, il trasferimento dei dati fra AKABAK e VACS avviene soltanto attraverso gli appunti di sistema. È una proprietà dell'ambiente e non un difetto di configurazione, ha una conseguenza diretta sul ciclo di ottimizzazione della fase 5, ed è registrata come ADR-007. Vale notare che non riapre ADR-003: il confronto corretto è fra un passo manuale nella simulazione e la somma di licenza Windows, latenza permanente sulla misura e licenza Akabak da rifare.

Sul trattamento dei dati riservati. Il Machine Identifier e il Release Code non sono in alcun file tracciato, perché il repository è ospitato su GitHub e un codice di attivazione non va pubblicato. Vivono in `_notes/licenze-akabak-riservato.md`, ignorato da git, insieme alla procedura di inserimento e al controllo da fare prima di azzerare la macchina.

Verificato con: `git check-ignore -v` sul file riservato, che lo dichiara ignorato; una ricerca del codice e dell'identificativo su tutti i file tracciati, con zero risultati; e i due controlli di convenzione sui documenti nuovi.

Esito: fatto.

### MS-020 - Procedura operativa di installazione pulita

Perimetro: `docs/10-ambiente/installazione-pulita-26-04.md`.

Scritta la procedura completa in undici fasi, su decisione confermata dall'utente. Il criterio di redazione è che ogni passo dichiara che cosa si fa, perché si fa, il comando esatto e il controllo con cui si verifica: una procedura senza controlli di uscita è un elenco di speranze.

Tre scelte di struttura meritano di essere spiegate. La fase 0 raccoglie una fotografia completa della macchina attuale in quattordici file, e viene prima di tutto perché dopo la fase 4 quelle informazioni non sarebbero più recuperabili: la mappa del disco con gli identificativi univoci, la catena audio, i prefix Wine esistenti, l'elenco dei pacchetti installati deliberatamente, e la verifica che il Machine Identifier di Akabak sia ancora quello a cui il codice è legato. La fase 1 mette in salvo e trasferisce i materiali prima di toccare il disco, e non dopo, perché la destinazione è sotto `/home`. E ogni fase ha un controllo di uscita esplicito, con l'indicazione di fermarsi se l'esito non è quello atteso.

Le tre regole non negoziabili sono in testa al documento: non si formatta `/home`, non si parte senza aver completato la fase 1, non si dà per verificato ciò che non si è letto.

La fase 10 raccoglie l'igiene post-installazione, e le sue quattro voci nascono da problemi realmente incontrati: la direttiva `Prompt=lts`, che su una LTS è quella corretta ed è la singola riga che impedisce alla situazione di ripetersi; la sospensione automatica e il Wake-on-LAN, dalla diagnosi di MS-015; la chiave SSH dedicata, da MS-016, con l'avvertenza di verificare la configurazione con `sshd -t` prima di riavviare il servizio; e la prenotazione dell'indirizzo sul router.

Il documento si chiude con il confronto atteso fra la fotografia della fase 0 e quella della fase 11, voce per voce, e con tre scenari di rientro se qualcosa va storto.

Verificato con: i due controlli di convenzione sull'intero albero `docs/`, zero errori e zero avvisi. La procedura in sé non è stata eseguita: è scritta e in attesa dell'accesso alla macchina.

Esito: fatto per la redazione. L'esecuzione è il prossimo blocco di lavoro.

### MS-021 - Ispezione diretta del corredo "Progetto stanza"

Perimetro: sola lettura su `C:\Users\Utente\Desktop\Progetto stanza (software)`, 2,3 GB.

Fino a questo punto l'inventario del corredo software proveniva da un file di testo nella radice del progetto, che descrive l'albero della copia su SSD esterno. Un inventario derivato da un elenco di nomi è però un inventario di seconda mano, e l'ispezione diretta ha mostrato quanto la differenza conti: ha corretto tre affermazioni, ne ha aggiunta una che nessun documento riportava, e ha rivelato un passo di installazione mancante.

Il metodo è stato leggere il formato reale di ogni installer con `file`, invece di dedurlo dal nome o dall'età del programma. Il risultato è che tutti gli installer del corredo sono PE32 a 32 bit, con una eccezione: `SETUP.EXE` di LSPCad 5.25 è in formato NE per Windows 3.1, cioè genuinamente a 16 bit. Ne discende la distinzione che è il contenuto tecnico più utile ricavato da questa ispezione: l'architettura dell'installer non è quella dell'applicazione, e un installer a 32 bit gira senza problemi in un prefix a 64 bit attraverso lo strato di compatibilità, mentre un eseguibile a 16 bit in un prefix a 64 bit non gira affatto. È il motivo per cui `VituixCAD_setup.exe`, che è a 32 bit, va comunque nel prefix a 64 bit dell'applicazione .NET che installa.

Tre correzioni a quanto era stato scritto in precedenza. Grenander Loudspeaker Lab era descritto come privo di cartella di modifica: accanto al suo installer c'è invece il file descrittivo di un gruppo di distribuzione illecita, quindi la voce cambia gruppo. Ramsete 27b era annotato come non valutato: la struttura del suo `SETUP.LST`, che dichiara un archivio, l'avvio di un `Setup1.exe` e fra le dipendenze `MSVCRT40.DLL` e `OLEPRO32.DLL`, lo identifica come applicazione Visual Basic 6, quindi a 32 bit e con bisogno del runtime `vb6run`. E le versioni di Akabak e VACS erano rese come 3.24 e 2.13, mentre l'autore dichiara 3.2.4 build 126 e 2.1.3 build 33.

Un fatto nuovo che nessun documento riportava: della versione 3.1.10 di EASE Focus la copia sul Desktop ha soltanto un collegamento e non la cartella. Da qui era stata tratta l'inferenza che quel contenuto vivesse sul solo SSD esterno, e quindi che le due copie non fossero identiche. **Quella inferenza è stata smentita il 2026-09-07 e va letta come ritirata**: il collegamento è presente e identico su entrambe le copie, che risultano identiche file per file, e punta invece a un quarto disco. Si vedano MS-024 e MS-025.

Verificato con: `file` su otto installer; `du -sb` per le dimensioni reali; `find` per la struttura a due e tre livelli; conteggio dei file del database GLL, che sono 221 di cui 174 con estensione `.gll`, dove la differenza fra i due numeri misura i file di accompagnamento `.dll` e `.bin` e spiega perché la copia deve essere dell'intera cartella.

Esito: fatto.

### MS-022 - Piano Wine del corredo, e emendamento a due decisioni

Perimetro: `docs/10-ambiente/wine-corredo-progetto-stanza.md`, aggiornamento di `docs/90-riferimenti/inventario-software.md` e delle fasi 7 e 8 della procedura di installazione pulita, e due voci nuove nel registro delle decisioni.

Scritto il piano di messa in opera voce per voce, con prefix di destinazione, dipendenze `winetricks` e stato di licenza accertato per ciascuna. Il gruppo da installare conta quattro programmi più i dati: VituixCAD, ARTA, EASE Focus 3.1.260 con il servizio di database AFMG, il database dei GLL, e Ramsete subordinato a una verifica. Il gruppo escluso conta otto voci per circa 1,7 GB.

ARTA è la promozione: non era nel piano e vi entra perché è la via più diretta per produrre un file GLL da un diffusore misurato, quindi serve alla fase 8 del progetto. Con una avvertenza sull'uso che vale registrare, perché è il tipo di dettaglio che si scopre nel momento sbagliato: ARTA è un programma di misura e vuole la scheda audio, e sotto Wine quell'accesso passa dal driver audio di Wine verso PipeWire con latenza e stabilità che non sono quelle di un programma nativo. Per lavorare su file già acquisiti il problema non si pone; per una misura dal vivo si usa REW, che è nativo.

Le due decisioni emendate. ADR-004 aveva vietato ogni prefix a 32 bit, ma il divieto era motivato da un solo candidato escluso, WinISD, e non da un principio: con Ramsete che è Visual Basic 6, il divieto decade e diventa ADR-009, con la parte condizionata che il prefix si crea soltanto se la verifica di licenza dà esito positivo. Il costo del prefix a 32 bit non è nullo e va pagato solo quando serve, perché richiede di dichiarare l'architettura `i386`, che è uno dei fattori di attrito degli aggiornamenti di rilascio, cioè uno dei motivi per cui la macchina si trova nella situazione da cui questa documentazione parte. La conseguenza operativa è di non dichiararla durante l'installazione pulita: rimandare costa un comando, anticipare costa attrito permanente.

La seconda è ADR-010, che registra il trasferimento per sottoinsieme selezionato con la motivazione voce per voce.

L'ispezione ha inoltre portato alla luce la sesta incoerenza del documento sorgente, di un tipo diverso dalle altre cinque: il sorgente indicava un installer di EASE Focus chiamato `EASE_Focus_Setup_v3.1.260.exe`, che non esiste, e ometteva l'installazione del servizio di database AFMG che pure valutava di impatto alto in una propria tabella. Non è una contraddizione interna e non si trova rileggendo: si trova solo confrontando la procedura con i file su cui dovrebbe operare. La fase 8 della procedura è stata corretta di conseguenza, e la pagina delle incoerenze ora ne conta sei divise in quattro tipi.

Verificato con: `python tools/md-unwrap.py --check docs/` e `python tools/lint-md-commands.py docs/`, zero errori su ventotto file.

Esito: fatto per il piano. L'esecuzione dipende dall'accesso alla macchina.

### MS-023 - Trasferimento esteso al corredo, e registro delle azioni differite

Perimetro: `docs/TRANSFER-MANIFEST.md`, `tools/transfer-to-studio.sh`, `tools/transfer-to-studio.ps1`, `docs/PENDING-ACTIONS.md`, `tools/check-pending-actions.py`.

Il manifest di trasferimento aveva una sola forma, cioè otto file piatti con le impronte trascritte nel documento. Il corredo ha forma diversa, perché è fatto di alberi di cartelle, e questo ha richiesto due estensioni distinte.

La prima è la copia: lo strumento bash ha ora una mappa separata per gli alberi e una funzione di copia ricorsiva, con la stessa degradazione da `rsync` a `scp` già prevista. La seconda è la verifica, che è la parte che si sarebbe rotta in silenzio: il confronto delle impronte era scritto per un elenco piatto e con percorsi a due livelli avrebbe smesso di corrispondere. È stato riscritto in due parti, un confronto per nome di file per il manifest piatto e un confronto voce per voce degli elenchi completi di impronte relative alla radice di ciascun albero, con il numero di file riportato per entrambi i lati.

La versione PowerShell non è stata estesa, e la scelta è dichiarata nella sua intestazione: copre i soli otto file piatti, mentre il corredo si trasferisce con la versione bash. Duplicare in PowerShell la logica di confronto ricorsivo raddoppierebbe la superficie da mantenere per un caso che Git Bash copre già ed è installato su questa postazione.

La seconda parte del microstep riguarda una richiesta esplicita dell'utente: ricordare di cancellare la copia ridondante del corredo su `J:\Progetto stanza (software)` una volta che il trasferimento è compiuto. Un promemoria che vive in una conversazione è perduto, quindi è stato creato un registro delle azioni differite, con una voce che dichiara le tre condizioni di sblocco, il criterio di verifica e il criterio di completamento, più uno strumento che legge le condizioni verificabili in automatico.

Le tre condizioni di sblocco di quella voce meritano una riga, perché la terza non era stata chiesta e va aggiunta. Il disco deve essere collegato, e al momento non lo era. Il trasferimento verso la macchina deve essere completato e verificato, perché non si cancella una copia prima che la copia buona sia al suo posto. E la corrispondenza fra le due copie va verificata per impronte e non a occhio, perché cancellare sulla base di una affermazione è il modo classico di perdere dati. Lo strumento offre `--confronta` proprio per quello. La motivazione data qui includeva anche la presunta divergenza sul collegamento della versione 3.1.10, che il 2026-09-07 si è rivelata inesistente: la condizione resta giusta ma il suo esempio era sbagliato, e la verifica ha poi confermato copie identiche. Si veda MS-024.

Verificato con: `bash -n` sullo strumento esteso; la sua prova a secco, che ora riporta 682 MiB in otto file più cinque voci del corredo, contro i 158 MiB precedenti; l'esecuzione dello strumento delle azioni differite, che riconosce correttamente il disco `J:` come non collegato e blocca la voce; e il suo rifiuto pulito con codice di uscita 2 quando gli si chiede il confronto senza il disco.

Esito: fatto per la preparazione. L'esecuzione del trasferimento dipende dall'accesso alla macchina, e la cancellazione su SSD dipende da quella più dal collegamento del disco.

## 2026-09-07, sessione di verifica delle copie e apertura dell'accesso

### MS-024 - Le due copie del corredo sono identiche: una inferenza sbagliata ritirata

Perimetro: sola lettura su `C:\Users\Utente\Desktop\Progetto stanza (software)` e su `J:\Progetto stanza (software)`, più `tools/check-pending-actions.py` e le pagine che riportavano l'inferenza sbagliata.

Il disco `J:` è stato collegato dall'utente, il che ha sbloccato le prime due condizioni di PA-001. Il confronto ha dato un esito netto: 650 file su ciascuna copia, gli stessi nomi relativi, le stesse dimensioni file per file, 2.380.021.546 byte in totale su entrambe, e le impronte SHA-256 di tutti e 650 i file coincidenti, senza alcun file presente su una sola delle due. La dichiarazione dell'utente che si trattasse di una copia uno a uno è quindi confermata come fatto e non più come affermazione.

Va registrato il tranello nel metodo, perché avrebbe portato alla conclusione opposta. La prima misura fatta è stata `du -sh` sulle sottocartelle, e le due copie sembravano diverse in modo sostanziale: 14 MB contro 5,9 MB su LSPCad 5.25, 36 MB contro 15 MB su LSPCad 6.32, 71 MB contro 66 MB su FineCone, e differenze minori su quasi tutte le altre voci, con `J:` sempre più grande. Nessuna di quelle differenze era reale. Il comando `du` misura lo spazio occupato sul supporto, che dipende dalla dimensione dei cluster del filesystem e arrotonda per eccesso ogni file: i due dischi hanno cluster di dimensione diversa, e su un corredo di 650 file l'arrotondamento si accumula in modo vistoso. La misura corretta è la somma dei byte reali, che è identica, e la prova definitiva è l'impronta del contenuto.

Da questo discende una inferenza sbagliata che va ritirata invece di essere cancellata in silenzio, perché era stata scritta come probabile in tre documenti. Si era osservato che nella copia sul Desktop la versione 3.1.10 di EASE Focus era un collegamento e non una cartella, e si era concluso che quel contenuto vivesse presumibilmente sul solo SSD, quindi che la cancellazione andasse limitata a ciò che era effettivamente duplicato. È falso: il collegamento è presente e identico su entrambe le copie, e non è una divergenza fra loro. L'inferenza era stata marcata come probabile e non come certa, che è il minimo, ma restava una ipotesi presentata dove bastava leggere un file.

Verificato con: confronto degli elenchi di file per nome e dimensione, che dà zero differenze in entrambe le direzioni; confronto completo delle impronte SHA-256 con `python tools/check-pending-actions.py --confronta`, che riporta 650 identici, zero solo su una parte e zero diversi, ed esce con codice 0.

Esito: fatto. Corretti `docs/10-ambiente/wine-corredo-progetto-stanza.md`, `docs/PENDING-ACTIONS.md` e le voci MS-021 e MS-023 di questo registro, oltre alla conseguenza di ADR-010.

### MS-025 - Il collegamento puntava a un quarto disco: scoperta di G:

Perimetro: lettura del file `EASE_Focus_v3.1.10 (k-array) - collegamento.lnk`, e apertura di PA-004.

Chiarito che il collegamento non era una divergenza fra le copie, restava la domanda su dove punti. La risposta si ottiene leggendo il file, perché un collegamento di Windows contiene il percorso di destinazione come stringa, sia in forma ASCII sia in UTF-16, e si estrae senza strumenti speciali.

Il percorso è `G:\LIBRARY\LOUDSPEAKERS & ELECTROACOUSTIC\K-ARRAY WORKSHOP\EASE Focus (k-array)`, su un disco `G:` mai menzionato prima in nessun documento di questo progetto. Il disco non risulta fra le unità montate, che al momento della verifica sono `C:`, `D:`, `E:`, `J:`, `T:`, `V:` e `X:`, quindi il contenuto non è stato ispezionato.

Che cosa si sa e che cosa non si sa, distinto con cura. Si sa dove punta il collegamento. Si sa dal documento sorgente che il pacchetto della 3.1.10 comprendeva l'installer InstallShield, i due servizi di database AFMG, una cartella di dati, una di configurazione predefinita e una di esempi ed esercitazioni con un progetto di workshop e due file GLL. Non si sa se il contenuto su `G:` corrisponda a quella descrizione né se contenga altro.

La priorità è bassa e va detto perché, per non trasformare una curiosità in un compito. La versione da installare è la 3.1.260: la 3.1.10 e la 3.0.18 sono superate, i GLL sono retrocompatibili, e tre versioni dello stesso programma in tre prefix sono manutenzione senza ritorno. Il valore residuo del materiale del workshop è didattico, cioè i progetti di esempio e i due GLL, non di installazione.

La lezione operativa vale più della scoperta: un collegamento va letto, non interpretato dal nome. Due minuti di lettura del file hanno sostituito una supposizione sbagliata con un percorso esatto.

Verificato con: estrazione delle stringhe del file `.lnk`, che restituisce il percorso completo; `ls` sul percorso, che non lo trova; elenco delle unità montate, che non comprende `G:`.

Esito: fatto per la scoperta. L'ispezione è tracciata come PA-004 e resta bloccata dal disco non collegato.

### MS-026 - Il perimetro di installazione include ora anche J:, senza conseguenze pratiche

Perimetro: risposta a una domanda dell'utente, e nota aggiunta a `docs/PENDING-ACTIONS.md` sotto PA-001.

L'utente ha chiesto di verificare se il percorso indicato in precedenza includesse anche `J:\Progetto stanza (software)`, precisando che anche quel contenuto va fatto funzionare sulla macchina.

La risposta è no, e conviene essere precisi sul perché non era un'omissione. Il percorso indicato per la messa in opera sotto Wine era la sola copia sul Desktop; `J:` era stato nominato in quel messaggio con un ruolo diverso e opposto, cioè come la copia da cancellare a lavoro finito. Le due indicazioni erano coerenti fra loro e il piano le ha seguite entrambe.

La richiesta nuova, però, non cambia nulla in pratica, ed è la verifica di MS-024 a renderlo certo. Essendo le due copie identiche file per file, il piano di installazione già scritto copre entrambe: non esiste sul disco `J:` un solo programma che non sia già nell'inventario verificato, e nessuna voce va aggiunta al gruppo da installare. Il perimetro resta quello di ADR-010.

Vale però registrare una conseguenza sull'ordine delle operazioni, perché è l'unico effetto reale della richiesta. Se il contenuto di `J:` deve funzionare sulla macchina, allora `J:` non è soltanto una copia da cancellare ma anche una possibile origine del trasferimento, alternativa al Desktop. Questo non cambia il manifest, perché le impronte sono identiche e quindi la sorgente è indifferente, ma cambia una precauzione: la cancellazione di PA-001 non va eseguita finché il trasferimento non è compiuto, altrimenti si perde la sorgente alternativa nel momento in cui potrebbe servire. È esattamente la condizione 3 di PA-001, che resta l'unica a bloccare.

Esito: fatto.

### MS-027 - ssh-copy-id non esiste in PowerShell: errore mio, e la forma corretta

Perimetro: correzione della fase 10.3 di `docs/10-ambiente/installazione-pulita-26-04.md`.

L'utente ha eseguito i comandi che gli erano stati forniti per aprire l'accesso SSH alla macchina. Il primo è riuscito: la chiave `id_ed25519_studio` è stata generata, con la sua coppia di file sotto `~/.ssh` e l'impronta mostrata a schermo. Il secondo è fallito con `Termine 'ssh-copy-id' non riconosciuto come nome di cmdlet, funzione, programma eseguibile o file script`.

L'impronta della chiave non è trascritta qui deliberatamente. Non è un segreto, perché una impronta di chiave pubblica è nata per essere confrontata alla luce del sole, ma su un repository ospitato pubblicamente rivelerebbe quale chiave è autorizzata su quell'host senza aggiungere nulla alla lezione tecnica. Il criterio adottato in questo progetto è di non pubblicare più di quanto serva a capire.

L'errore è nella documentazione fornita, non nell'esecuzione. Il comando `ssh-copy-id` non è un eseguibile: è uno script di shell POSIX, distribuito con OpenSSH nei sistemi Unix e presente su Windows dentro Git Bash, ma non fra i comandi che il client OpenSSH di Windows installa. Metterlo in un blocco PowerShell era sbagliato, e la causa dell'errore è la mia assunzione che i due blocchi di comandi differissero soltanto nella sintassi dei percorsi, come accade per `git`, mentre qui differiva la disponibilità del comando stesso.

Ne discende una regola che vale oltre questo caso, e che è la ragione per cui il microstep esiste invece di essere una correzione silenziosa: quando si forniscono due blocchi equivalenti per due shell, l'equivalenza va verificata sulla disponibilità dei comandi e non solo sulla loro sintassi. Il linter dei comandi del progetto controlla la forma delle righe, non l'esistenza dei binari, quindi questo controllo resta umano.

La forma corretta per PowerShell fa a mano ciò che `ssh-copy-id` automatizza, cioè legge la chiave pubblica e la accoda al file delle chiavi autorizzate sulla macchina remota, creando la cartella con i permessi giusti. Sta su una riga sola, come prescrive la regola sul formato dei comandi.

Va inoltre segnalato all'utente un punto che l'errore rende attuale: `ssh-keygen` non va rilanciato, perché la chiave è già stata generata e un secondo lancio chiederebbe di sovrascriverla.

Esito: fatto. La fase 10.3 della procedura riporta ora tre forme, cioè PowerShell senza `ssh-copy-id`, Git Bash con `ssh-copy-id`, e la verifica successiva.

### MS-028 - Accesso SSH aperto e verificato

Perimetro: nessuna modifica al progetto; installazione della chiave sulla macchina eseguita dall'utente.

L'utente ha eseguito il comando corretto per PowerShell, quello che accoda la chiave pubblica al file delle chiavi autorizzate impostando i permessi, e ha inserito la password una volta. La verifica immediata ha risposto `CONNESSO` e ha rivelato il nome della macchina, `i7-6700-16GBDDR4-500GBSSD`, che descrive l'hardware e conferma quanto documentato.

Da parte dell'agente la connessione con chiave funziona in modalità non interattiva, cioè con `BatchMode=yes`, che è la condizione necessaria per eseguire diagnostica senza intervento umano. L'utente risulta `alesop95` con identificativo numerico 1000, e appartiene ai gruppi `sudo`, `audio` e `plugdev` fra gli altri. L'appartenenza al gruppo `audio` è uno dei controlli della fase 6 della procedura, quindi risulta soddisfatto in anticipo.

Un limite dell'accesso da registrare, perché determina che cosa l'agente può e non può fare: `sudo` chiede la password, quindi ogni comando privilegiato resta dell'utente. La verifica è `sudo -n true`, che risponde `sudo: a password is required`. Ne segue che la fase 0 è stata eseguita nella sua parte non privilegiata, e che le due voci che richiedono privilegi restano da fare.

Esito: fatto. Il blocco che durava da due sessioni è rimosso.

### MS-029 - Fase 0 eseguita: la fotografia della macchina, e tre ipotesi smentite

Perimetro: `docs/10-ambiente/fotografia-macchina-2026-09-07.md` nuovo, `_notes/fotografia-2026-09-07/` con ventitré file di output grezzo, correzioni a `docs/10-ambiente/ubuntu-lts-upgrade.md`.

Eseguita la fase 0 nella sua parte non privilegiata e raccolti ventitré file sulla macchina sotto `~/fotografia-pre-reinstall/`, poi recuperati sulla postazione sotto `_notes/`, che è ignorata da git. Il documento tracciato è l'analisi; i file grezzi restano locali perché sono output di comandi e non documentazione.

Il risultato principale è una smentita, e va messo per primo perché è la ragione per cui la fase 0 esiste. Delle quattro cause che avevo attribuito al blocco di aggiornamento, tre sono false.

La prima, secondo cui dalla 25.04 non esisterebbe un salto diretto alla LTS e servirebbe passare dalla 25.10, è smentita da `do-release-upgrade -c`, che risponde *New release '26.04.1 LTS' available*.

La seconda, secondo cui `Prompt=lts` impedirebbe di trovare il rilascio successivo, è smentita due volte. Il file contiene `Prompt=normal`, quindi quel valore non c'è. E il commento dello stesso file dichiara che con `lts` su un rilascio non-LTS l'aggiornatore assume `normal`, quindi la causa non avrebbe potuto agire nemmeno se il valore fosse stato quello. Questa è la smentita più istruttiva: l'errore non era di osservazione ma di lettura della documentazione, perché la risposta era scritta nei commenti del file che stavo ipotizzando.

La terza, secondo cui gli archivi della 25.04 sarebbero stati spostati su `old-releases` producendo errori 404, è smentita da sei richieste HTTP: archivio, mirror italiano e security rispondono 200 sulle suite `plucky`, mentre `old-releases` risponde 404 sulla stessa risorsa, cioè il rilascio non è ancora stato spostato lì. Il ragionamento sulla politica di Ubuntu era corretto in generale ma applicato a un momento sbagliato.

L'unica parte confermata è la quarta, i fattori di attrito, e in forma più grave del previsto: sotto `/etc/apt/sources.list.d/` convivono due repository WineHQ attivi, `winehq-noble.sources` e `winehq-plucky.sources`, per due rilasci diversi di Ubuntu, che forniscono pacchetti con gli stessi nomi in versioni diverse per amd64 e i386. Restano anche l'architettura `i386` dichiarata, una sorgente `file:/cdrom/` residua e due file di backup delle sorgenti.

Il fatto che riorganizza tutto il quadro è però un altro, ed è di quelli che si trovano soltanto guardando: la cartella `/var/log/dist-upgrade/` è vuota. L'aggiornamento di rilascio non è mai stato eseguito su questa macchina, quindi non esisteva un tentativo fallito da diagnosticare. La cronologia di apt lo conferma dall'altro lato: l'ultima operazione registrata è del 13 agosto 2025 e riguarda l'installazione di `winetricks`, e la simulazione `apt-get -s dist-upgrade` elenca 134 pacchetti pendenti da `plucky-updates` senza segnalare conflitti. Il sistema chiede anche un riavvio, perché il kernel `6.14.0-37` è installato mentre in esecuzione c'è il `6.14.0-35`.

La conclusione onesta è che la macchina non fa fatica ad aggiornarsi: non è mai stata aggiornata. Che cosa significasse concretamente la difficoltà riferita resta una domanda per l'utente, e questa è la lezione metodologica del microstep: avevo costruito una diagnosi elaborata su una premessa che non avevo verificato, cioè che un tentativo fosse stato fatto e fosse fallito. La premessa era implicita nella domanda e l'ho accettata senza chiederla.

La pagina della diagnosi non è stata riscritta per far finta di aver avuto ragione. Porta in apertura l'avvertenza che è smentita, ciascuna delle tre cause è marcata come tale nel corpo, e la sezione delle due strade è stata corretta perché la strada dell'aggiornamento in posto si è rivelata molto meno onerosa di come era stata descritta.

Verificato con: i ventitré file di output, tutti non vuoti; il confronto riga per riga fra esito atteso ed esito reale, riportato in tabella nel documento nuovo.

Esito: fatto per la parte non privilegiata. Restano lo stato di salute dell'SSD, l'esito reale di `apt update` e la verifica del Machine Identifier di Akabak.

### MS-030 - La catena audio a bassa latenza è attiva, e la fase 6 chiedeva la cosa sbagliata

Perimetro: correzione della fase 6 di `docs/10-ambiente/installazione-pulita-26-04.md`.

Il documento sull'aggiornamento elencava fra i punti da verificare il modo in cui Ubuntu Studio fornisce il kernel a bassa latenza, e la fase 6 prescriveva di controllare che il kernel in esecuzione fosse un kernel a bassa latenza. La fotografia mostra che quella prescrizione avrebbe dato un falso negativo.

Sulla macchina non è installato alcun `linux-image-lowlatency`. I kernel presenti sono `linux-image-6.14.0-35-generic`, `linux-image-6.14.0-37-generic` e il metapacchetto `linux-image-generic`. È installato invece `ubuntustudio-lowlatency-settings` alla versione `25.04.21`, che non è un kernel ma un pacchetto di impostazioni.

I due fatti convivono perché la configurazione a bassa latenza è ottenuta sul kernel generico tramite parametri di avvio, e la riga di comando del kernel in esecuzione li mostra: `preempt=full`, che abilita la prelazione completa, e `threadirqs`, che sposta la gestione degli interrupt in thread schedulabili. Sono le proprietà per cui esisteva un kernel separato. Il pacchetto configura anche i limiti di priorità in tempo reale, con `rtprio 95` e `memlock unlimited` per i gruppi `audio` e `pipewire`, e i tre servizi `pipewire`, `pipewire-pulse` e `wireplumber` risultano attivi.

Ne segue la correzione: il controllo corretto non è il nome del kernel ma la presenza di `preempt=full` e `threadirqs` in `/proc/cmdline`, insieme ai limiti `rtprio` per il gruppo `audio` e allo stato dei tre servizi. Un controllo sul nome avrebbe concluso che la configurazione mancasse mentre è attiva, e avrebbe portato a installare un kernel che non serve.

Va registrato inoltre che **la Scarlett 2i2 non è collegata**: l'elenco USB non riporta alcun dispositivo Focusrite, e le sole schede viste sono l'audio integrato `ALC887-VD` con le sue uscite HDMI. Il controllo di uscita della fase 6, che chiede di vedere la Scarlett in ingresso e in uscita, non è eseguibile finché l'interfaccia non viene collegata.

Esito: fatto.

### MS-031 - L'ambiente Wine reale, e due lacune di cui una si chiude

Perimetro: aggiornamento della fotografia e dello storico di Akabak e VACS.

Esiste **un solo prefix** Wine sulla macchina, ed è quello di default, `/home/alesop95/.wine`. Non ci sono prefix separati per programma.

Questo chiude la prima delle due lacune dichiarate in `docs/90-riferimenti/timeline-akabak-vacs.md`, cioè in quale prefix Akabak e VACS siano installati: sono nel prefix condiviso, secondo l'approccio che il documento sorgente chiamava fare come per Akabak e di cui riconosceva il rischio. La seconda lacuna, cioè quale variante di VACS sia installata e come fu risolto il suo fallimento iniziale, richiede di guardare dentro il prefix e resta aperta.

Lo stato dei pacchetti è la fotografia del pasticcio già raccontato dal documento sorgente. La versione attiva è `wine-9.0 (Ubuntu 9.0~repack-4build3)`, cioè quella dei repository Ubuntu e non di WineHQ, nonostante entrambi i repository WineHQ siano configurati. Accanto a essa è installato `wine-stable 3.0.1ubuntu1`, che è una versione del 2018 e di fatto un residuo, dato che `wine --version` riporta 9.0. Sono presenti anche `wine32:i386`, `libwine`, `libwine:i386`, `fonts-wine` e `winetricks`. Non esistono `wine64` né `wine32` come comandi separati, quindi la verifica prevista dalla pagina di configurazione che li usa entrambi darebbe esito negativo su questa macchina pur essendo l'ambiente funzionante.

La cronologia di apt fornisce il riscontro indipendente che finora mancava alla sezione di troubleshooting del documento sorgente. La sequenza di installazioni, purghe e reinstallazioni che il documento descriveva è registrata con data e ora del 13 agosto 2025: installazione di `wine64` e `winetricks` alle 12:06, aggiunta di `wine32` alle 12:17, purga di tutto alle 13:18, `autoremove` alle 13:19, reinstallazione con `--install-recommends wine-stable` alle 13:31, e `winetricks` alle 16:37. È la prima volta in questo progetto che una affermazione del documento sorgente viene confermata da una fonte sulla macchina stessa.

Esito: fatto.

### MS-032 - Perché SMART richiede privilegi, e i tre dati che si leggono comunque

Perimetro: diagnostica in sola lettura sulla macchina, aggiornamento della fotografia, della fase 0.3 della procedura e della pagina delle incoerenze.

L'utente ha chiesto se il comando `sudo smartctl -a /dev/nvme0n1` non si possa lanciare via SSH da Windows. La risposta è in due parti e la distinzione conta: via SSH si può e funziona, ma non dallo strumento di shell dell'agente, perché quella shell non ha input interattivo e la connessione usa `BatchMode=yes`, che disabilita di proposito ogni richiesta interattiva. Non è un limite della rete né della chiave: è un limite di canale.

Prima di rimandare la palla all'utente ho verificato se esistesse una via non privilegiata, invece di darlo per scontato. Non esiste, e la ragione è precisa: i dati SMART di un disco NVMe si leggono interrogando il controller, che è il dispositivo a caratteri `/dev/nvme0`, con permessi `crw------- root root`, cioè nessun gruppo a cui delegare. Il dispositivo a blocchi `/dev/nvme0n1` è `brw-rw---- root disk`, ma l'utente non appartiene al gruppo `disk`. E `udisksctl`, che tramite polkit avrebbe potuto essere una terza via, non è installato.

Tre dati si ricavano comunque senza privilegi, e due di essi correggono quanto era documentato.

Il modello reale del disco è `CT500P2SSD8` con firmware `P2CR033`, letti da `/sys/class/nvme/nvme0/`. Il documento sorgente lo riportava come `CT500P25SD8`, con un carattere trasposto: `P2` è la sigla della serie Crucial, `P25` non esiste. È la settima incoerenza del documento sorgente, e appartiene a un tipo nuovo rispetto alle sei precedenti, perché non si trova né rileggendo il documento né guardando i file, ma solo leggendo l'hardware. Non ha sintomi e non cambia nulla di operativo; cambia tutto nel momento in cui quel numero serve a cercare un firmware, una scheda tecnica o un ricambio.

La temperatura del controller si legge da `hwmon` ed è di 33,85 gradi, sotto l'etichetta `Composite`. È un indicatore parziale ma esclude la sofferenza termica, che è una delle cause di degrado di un SSD.

Il pacchetto `smartmontools` è già installato, alla versione `smartctl 7.4`. Questo rende superflua l'avvertenza della fase 0.3, che prevedeva di installarlo e ipotizzava che l'installazione da rete potesse non funzionare su un rilascio fuori supporto: era una precauzione ragionevole e non serviva.

Le tre strade per il comando privilegiato sono documentate con il costo di ciascuna. L'esecuzione da parte dell'utente con l'opzione `-t`, che alloca un terminale sulla connessione e senza la quale `sudo` non ha dove chiedere la password. Una regola `sudoers` limitata al singolo comando in sola lettura, che renderebbe autonoma la diagnostica privilegiata anche in futuro ma amplia ciò che un accesso compromesso alla chiave permette, quindi resta una decisione dell'utente perché modifica la postura di sicurezza della macchina. E l'aggiunta al gruppo `disk`, nominata solo per escluderla, perché darebbe accesso in lettura e scrittura a tutti i dispositivi a blocchi per leggere una tabella.

Verificato con: `sudo -n smartctl`, che risponde `sudo: a password is required`; `ls -l` sui due dispositivi; `groups`; lettura dei tre attributi da `/sys`; assenza di `udisksctl`.

Un secondo controllo della stessa passata, riportato perché il suo esito è un falso allarme rientrato e questo è un tipo di voce che merita comunque di stare a verbale. Una scansione dei caratteri non attesi nei file Markdown ha trovato 166 trattini lunghi in otto file del pacchetto `academic-researcher`, che la regola di stile vieta e che `fix-dashes.py` non converte. Il sospetto era un difetto dello strumento.

Non lo è. Uno dei due file è dichiarato in `tools/dashes-exclude.txt` con la sua motivazione, cioè un documento copiato verbatim da fonte esterna, che per la regola di stile mantiene la formattazione originale. Negli altri sette, la mappatura delle posizioni ha mostrato che ogni trattino cade dentro un blocco recintato: le recinzioni stanno alle righe 44, 54, 58, 67, 71, 83 e così via, e le occorrenze alle righe 51, 61, 80 e seguenti sono tutte comprese fra una apertura e la sua chiusura. Sono modelli di prompt in inglese dentro blocchi preformattati, che lo strumento non tocca di proposito e che la regola di stile esclude esplicitamente insieme al codice e alle tabelle.

La lezione è la stessa del resto della sessione, applicata questa volta in tempo: verificare prima di riportare. Un difetto annunciato e poi rientrato costa credibilità alla documentazione più di quanto valga la segnalazione.

Esito: fatto per la diagnosi del vincolo. La lettura di SMART resta in PA-005 e resta dell'utente.

### MS-033 - SMART letto: il disco è sano e la decisione non cambia

Perimetro: aggiornamento di `docs/10-ambiente/fotografia-macchina-2026-09-07.md` e di PA-005.

L'utente ha eseguito `sudo smartctl -a /dev/nvme0n1` con l'opzione `-t`, e l'esito chiude la voce più importante della fase 0, cioè la sola che poteva spostare la decisione da installazione a sostituzione del disco. Non la sposta.

Il giudizio complessivo è `PASSED`. I due indicatori che contano su un SSD stanno bene: `Percentage Used` al 9 per cento, quindi 91 per cento di vita residua, e `Available Spare` al 100 per cento contro una soglia di allarme del 5. Gli errori di integrità dei dati e dei supporti sono zero. La temperatura è 34 gradi contro soglie di 70 e 85.

Un riscontro che vale segnalare. Il documento sorgente riportava il disco al 91 per cento, misurato con CrystalDiskInfo da Windows nel 2025; SMART oggi dice 9 per cento usato, cioè lo stesso valore. Fra le due misure passano tredici mesi e l'usura non si è mossa di un punto, coerentemente con i 3,7 GB occupati su `/home`.

Due numeri richiedono una lettura e non vanno presi per allarmi, ed è la parte tecnicamente utile di questo microstep.

Le 584 voci nel registro degli errori hanno tutte lo stesso stato, `0x4004`, con messaggio `Invalid Field in Command`. Non sono errori del supporto: sono risposte del controller a comandi che non implementa. La riga finale dell'output lo dimostra da sola, perché `smartctl` stesso ne genera una mentre gira, con `Read Self-test Log failed: Invalid Field in Command`. Il registro dell'autotest è una funzione opzionale della specifica NVMe che questo controller non espone, quindi ogni interrogazione incrementa il contatore. Quel numero misura quante volte qualcosa ha chiesto al disco una funzione che non ha, non quante volte il disco ha sbagliato, e la prova è la coesistenza con gli errori di integrità a zero.

I 24 spegnimenti non puliti su 135 cicli di accensione sono invece un dato reale, circa uno su sei, e vale sapere che non è normale: indica mancanze di alimentazione, blocchi risolti col pulsante o spegnimenti forzati. Non ha prodotto danni, ma è un fattore di rischio da tenere in conto proprio in vista di una reinstallazione, perché una interruzione durante la scrittura del sistema è il momento peggiore.

Un terzo dato racconta qualcosa che il documento sorgente non conteneva: le ore di accensione sono 12.787, cioè circa un anno e cinque mesi di funzionamento continuo, mentre il sistema attuale è installato dal 5 agosto 2025. Ne segue che il disco ha una vita precedente a questa installazione, presumibilmente nel PC Windows da cui la macchina è stata riconvertita, e lo confermano i 24,6 TB scritti che su tredici mesi di uso leggero non si spiegherebbero.

Il modello letto da SMART, `CT500P2SSD8` con firmware `P2CR033`, conferma la correzione della settima incoerenza del documento sorgente, che lo riportava come `CT500P25SD8`.

Esito: fatto. La prima delle tre voci di PA-005 è chiusa con esito positivo, e la scelta resta fra installazione pulita e aggiornamento in posto, cioè dove ADR-011 l'ha lasciata.

### MS-034 - Censimento dell'inventario testuale contro l'SSD: completo e accurato

Perimetro: `docs/90-riferimenti/censimento-corredo.md` nuovo, sola lettura su `J:` e sul Desktop della postazione.

L'utente ha chiesto di controllare l'inventario testuale `(SSD S7) DIY Loudspeaker Pack Softwares.txt` contro il contenuto reale di `J:\Progetto stanza (software)`, con il disco collegato.

L'esito è netto: l'inventario dichiara 36 cartelle e tutte e 36 esistono su `J:`, e su `J:` non c'è alcuna cartella non dichiarata. L'inventario è quindi completo e accurato.

Va spiegato un dettaglio che a prima lettura sembra una lacuna e non lo è. L'inventario non nomina né `VituixCAD_setup.exe` né il collegamento della versione 3.1.10 di EASE Focus, benché entrambi esistano, perché quel file è l'uscita di un comando che elenca soltanto le cartelle. È un inventario completo di ciò che si era proposto di elencare, e la sua incompletezza sui file è una proprietà del comando e non un errore dell'autore. Questo chiude in modo definitivo il sospetto, avanzato in MS-021 e ritirato in MS-024, secondo cui l'assenza della 3.1.10 dall'inventario indicasse una differenza fra le copie: non la indicava, e la spiegazione era più banale di quanto avessi ipotizzato.

Il censimento vero e proprio assegna a ciascuna delle quattordici voci un verdetto fra portare, archiviare e scartare, con la ragione. Si portano cinque voci per circa 524 mebibyte, si archiviano due, si scartano otto per circa 1,7 GB, cioè quasi tre quarti del peso.

La parte che vale più dell'elenco è il criterio, perché è quello che rende il censimento ripetibile su materiale nuovo. Il criterio primario è la posizione nel workflow: questo progetto parte da driver finiti e usa i loro parametri Thiele/Small, quindi tutto ciò che opera a monte, cioè la simulazione del cono e del motore magnetico, sta fuori per costruzione e non per giudizio di qualità. Il criterio secondario è la sostituibilità con qualcosa di migliore già disponibile: LSPCad e Grenander fanno ciò che fa VituixCAD, che è gratuito e di quindici anni più recente. Lo stato di licenza è un criterio terziario, e va detto con precisione perché è controintuitivo: nessuna delle otto voci scartate è esclusa perché porta una protezione rimossa, ma perché non serve, e la dimostrazione è che ciascuna ha una ragione funzionale che regge da sola.

Sulla destinazione fisica, la richiesta era di portare il materiale sulla scrivania della macchina levandolo dall'SSD. La soluzione adottata concilia le due esigenze: l'albero organizzato resta sotto `~/electroacoustics/`, perché è la struttura che gli strumenti di trasferimento e il manifest conoscono e su cui calcolano le impronte, e sulla scrivania si mette un collegamento simbolico a quella cartella. Così è raggiungibile con un doppio clic senza duplicare 524 mebibyte né spezzare la corrispondenza fra manifest e disco.

Verificato con: confronto insiemistico fra le cartelle dichiarate nel `.txt` e quelle reali su `J:`, che dà zero differenze in entrambe le direzioni.

Esito: fatto.

### MS-035 - La catena di riproduzione, e la conseguenza che anticipa una decisione di progetto

Perimetro: `docs/75-catena-di-riproduzione.md` nuovo, ADR-012.

L'utente ha indicato come uscita per i due monitor l'unità Rod Rain audio, oggetto di studio del progetto `rodrainaudio-reverse-eng`, precisando che il dispositivo è condiviso con un altro computer. La catena di ascolto non era mai stata definita: il documento sorgente si occupava della catena di misura e lasciava il resto implicito.

Letta la catena interna dal progetto dedicato, che ne è la fonte canonica: USB, ricevitore SA9023, collegamento I2S, convertitore ES9023 con driver integrato a 2 Vrms, filtro RC, uscita a livello di linea, e da lì lo stadio cuffie discreto. Il pannello posteriore espone AUDIO IN, AUDIO OUT su RCA, USB-B e rete.

Ciò che conta per il progetto è un solo dato, ed è anche ciò che genera la conseguenza: esiste una uscita a livello di linea su RCA a circa 2 Vrms. Due Vrms sono un segnale, non una potenza, e lo stadio cuffie che segue è dimensionato per carichi da decine o centinaia di ohm, non per un altoparlante da 4 o 8 ohm che chiede decine di watt.

Ne segue che la scelta della sorgente vincola l'architettura del diffusore, e questa è la conseguenza non ovvia. Con monitor attivi la catena è completa così com'è, perché l'uscita RCA va direttamente ai loro ingressi. Con monitor passivi serve un amplificatore di potenza stereo interposto, che non è fra le cose disponibili e diventerebbe un acquisto.

Il documento sorgente lasciava aperta la scelta fra crossover passivo e attivo, ed era legittimo quando la sorgente non era decisa. Ora va anticipata alla fase 4a, prima dell'acquisto dei driver, perché determina se occorre un amplificatore in più, perché cambia il modo in cui il crossover si progetta, e perché influisce su quali driver convengono. Non l'ho decisa io: è registrata come decisione aperta con i suoi termini in ADR-012.

Una seconda conseguenza riguarda la validità delle misure, ed è il tipo di dettaglio che si scopre nel momento sbagliato. La catena di misura usa la Scarlett, perché serve un ingresso microfonico con phantom; la catena di ascolto userà il Rod Rain. Per la fase 1 la differenza è irrilevante, perché si misura la stanza e la sorgente è provvisoria. Per la fase 8 non lo è: se si vuole misurare ciò che si ascolterà, il segnale di prova deve uscire dalla catena di ascolto reale, quindi microfono sulla Scarlett e generazione sul Rod Rain, che REW permette configurando dispositivi diversi in ingresso e in uscita.

Resta da verificare, e non da assumere, se l'uscita AUDIO OUT sia a livello fisso o segua il controllo di volume: con uscita fissa e monitor attivi il volume deve stare altrove.

Esito: fatto.

### MS-036 - Scheda audio per l'home recording, registrata nel progetto che la riguarda

Perimetro: nel progetto `home-recording-training-mixing-setup`, `docs/PENDING-ACTIONS.md` nuovo, più i due indici.

L'utente ha chiesto di annotare in quel progetto la valutazione di acquisto di una interfaccia audio, con ricerca di mercato, da fare più avanti.

La voce è stata scritta lì e non qui, e la ragione va detta perché è la stessa logica del blocco condiviso sull'ambiente: la macchina serve a due progetti, ma l'esigenza è di uno solo. La Scarlett 2i2 ha due ingressi, che bastano al progetto dei monitor dove serve un solo ingresso microfonico per il microfono di misura, e sono invece il vincolo principale per la registrazione multitraccia, che è lo scopo dell'altro progetto.

La voce fissa i criteri prima dei modelli, perché è l'ordine che evita di innamorarsi di una scheda e poi giustificarla. Il primo criterio, quello che ordina tutti gli altri, è quanti ingressi contemporanei servano davvero e di che tipo. Fra gli altri c'è il supporto su Linux, che a questo scopo non è un dettaglio: le interfacce conformi alla classe audio USB funzionano senza driver proprietari, mentre alcune richiedono software di configurazione che esiste solo per Windows e macOS, e in quel caso funzioni come il mixer interno o il routing restano inaccessibili.

Esito: fatto. La valutazione resta aperta e non blocca nulla del progetto dei monitor.

### MS-037 - Pulizia: rimossa la pagina smentita e corrette le affermazioni obsolete

Perimetro: rimozione di `docs/10-ambiente/ubuntu-lts-upgrade.md` da questo progetto e dalla sua copia nel gemello, più correzioni in sei file.

L'utente ha chiesto di far sparire dal progetto le informazioni obsolete o sbagliate. La richiesta convive con quella di tracciare tutto, e la conciliazione adottata è questa: le affermazioni sbagliate non restano dove qualcuno le leggerebbe come vere, cioè nella documentazione di riferimento, mentre il record di che cosa era sbagliato e perché resta dove il tracciamento vive, cioè in questo registro e nella pagina delle incoerenze.

La pagina della diagnosi è stata quindi rimossa invece di essere tenuta con l'avvertenza in apertura. Tre delle sue quattro cause erano false, e una pagina così è un rischio anche con l'avvertenza, perché chi la apre a metà legge il ragionamento e non la premessa. Il quadro reale sta nella fotografia della macchina, e il record dell'errore con la ragione di ciascuna smentita sta in MS-029. Tutti i rimandi sono stati ridiretti.

Corrette inoltre quattro affermazioni obsolete che sopravvivevano come dichiarazioni al presente. La partizione EFI è 1,1 GB e non i circa 100 MB del documento sorgente, e la correzione era urgente nella tabella della fase 4.2 perché chi la seguisse cercherebbe una partizione che non corrisponde. Il modello del disco è `CT500P2SSD8`. Lo stato dell'SSD non è più una scansione Windows del 2025 ma una lettura SMART del 2026-09-07. E la configurazione a bassa latenza non arriva da un kernel dedicato ma dal kernel generico con `preempt=full` e `threadirqs`.

Un residuo dichiarato: i rimandi alla pagina rimossa che restano nel registro dei microstep, nel work-log e nel contesto di ADR-006 non sono stati toccati, perché lì sono storia e riferirsi a un file che esisteva è corretto. Un lettore che li segue non trova il file, e questo microstep è la spiegazione.

Verificato con: ricerca dei rimandi residui, che nella documentazione di riferimento è vuota; i due controlli di convenzione su tutto l'albero; e la propagazione al gemello, che ha richiesto la rimozione manuale della copia perché lo strumento di sincronizzazione segnala gli orfani ma per scelta non li cancella.

Esito: fatto.

### MS-038 - Decisioni chiuse: installazione pulita riconfermata, e la pulizia di Wine non si fa

Perimetro: ADR-013, chiusura di PA-006, aggiornamento dello strumento delle azioni differite.

L'utente ha riconfermato l'installazione pulita di Ubuntu Studio 26.04 LTS sulla base corretta, cioè su tre motivi invece di quattro con l'ambiente pulito come dominante invece della fragilità dell'alternativa, e ha scelto di eseguire il lavoro privilegiato con comandi preparati e lanciati a mano, senza regole `sudoers`. La motivazione della seconda scelta è che una regola senza password amplierebbe ciò che può fare chi ottenesse la chiave SSH, e per una macchina raggiungibile in rete quel prezzo non è giustificato da una comodità di esecuzione.

La conseguenza operativa merita di stare in evidenza perché non è ovvia e perché ha risparmiato lavoro: **la pulizia dell'ambiente Wine non si esegue**. Pulire un sistema che verrà azzerato è lavoro che si butta, perché la riformattazione di root porta via l'installazione dei pacchetti, i due repository WineHQ, l'architettura `i386` e la sorgente `file:/cdrom/` residua. L'ambiente pulito si ottiene per costruzione dalla reinstallazione, non da una purga preventiva. Per la stessa ragione non si applicano i 134 pacchetti pendenti e non si esegue il riavvio richiesto.

Cambia anche il peso delle due voci ancora aperte di PA-005: l'esito reale di `apt update` diventa irrilevante, perché quel sistema non verrà aggiornato, mentre la verifica del Machine Identifier di Akabak resta necessaria e va fatta prima di azzerare, perché dopo non sarebbe più confrontabile.

Esito: fatto. PA-006 chiusa, ADR-013 registrata, ADR-011 superata nel suo stato di attesa.

### MS-039 - Trasferimento eseguito e verificato, e due difetti dello strumento trovati sul campo

Perimetro: esecuzione della fase 1.1 sulla macchina, correzioni a `tools/transfer-to-studio.sh`, chiusura della terza condizione di PA-001.

Il trasferimento è stato eseguito e verificato: 8 file del manifest e 6 voci del corredo per 273 file, 728 MB sotto `~/electroacoustics`, con tutte le impronte SHA-256 coincidenti fra origine e destinazione. Sulla scrivania della macchina è stato creato un collegamento simbolico all'albero, così che sia raggiungibile con un doppio clic senza duplicare i file. Lo spazio su `/home` passa da 3,7 a 4,4 GB su 369 disponibili.

Prima di questo, lo strumento ha richiesto una aggiunta e ha rivelato due difetti, tutti e tre istruttivi.

L'aggiunta è il supporto alla chiave dedicata. Lo strumento invocava `ssh` e `scp` senza indicare una identità, e su questa postazione non esiste una voce in `~/.ssh/config` per la macchina, quindi il client provava solo i nomi di chiave predefiniti, che non esistono. Aggiunta la variabile `STUDIO_KEY`, con valore predefinito la chiave dedicata e possibilità di svuotarla se in futuro si aggiungerà un alias di configurazione.

Il primo difetto è il più interessante e si è manifestato al primo tentativo, con `scp: dest open "$HOME/electroacoustics/installers/": No such file or directory`. La causa è che da OpenSSH 9 in avanti `scp` trasferisce via SFTP invece del vecchio protocollo, e SFTP non esegue una shell sul lato remoto: la variabile `$HOME` arrivava letterale, come stringa, e non veniva espansa. Il dettaglio che rende il difetto insidioso è che nello stesso script la creazione dell'albero di destinazione, fatta con `ssh` seguito da un comando, funzionava perfettamente, perché lì una shell remota c'è e la variabile si espande. Convivevano quindi due invocazioni all'apparenza simmetriche con comportamenti diversi. La correzione è usare percorsi relativi, che SFTP risolve dalla home dell'utente perché è la directory iniziale della sessione.

Il secondo difetto era nel confronto delle impronte e ha prodotto un falso negativo su `VituixCAD_setup.exe`. Lo strumento dichiarava impronte diverse mostrando due righe con la **stessa** impronta: `95a1aea4...` da un lato e `95a1aea4...` dall'altro. La differenza era il separatore. Il comando `sha256sum` di Git Bash per Windows scrive `impronta *nome`, con l'asterisco che marca la lettura in modo binario, mentre quello di Linux scrive `impronta  nome` con due spazi. Confrontare le due forme grezze segnala una differenza che non esiste. La correzione è normalizzare il separatore su entrambi i lati prima del confronto.

Vale notare che questo secondo difetto era il più pericoloso dei due, e non per la sua gravità tecnica ma per l'effetto che avrebbe avuto sull'uso: un falso negativo su una verifica di integrità insegna a non fidarsi della verifica, e una verifica di cui non si ha fiducia non viene più guardata. Un difetto che blocca è meno dannoso di uno che mente.

Aggiunta infine una modalità `--impronte`, che esegue la sola verifica saltando la copia. È nata da una necessità pratica, cioè non ricopiare 726 MB per riprovare un confronto corretto, ma resta utile in generale, perché la verifica di integrità è precisamente il tipo di controllo che si vuole poter ripetere.

Verificato con: `bash -n` sulla sintassi; l'esecuzione completa con esito positivo su tutte e quattordici le voci; la modalità di sola verifica rilanciata dopo la correzione, che riporta impronte identiche su tutte le voci; e l'ispezione dell'albero sulla macchina, con 281 file e il collegamento sulla scrivania.

Esito: fatto. La terza e ultima condizione di PA-001 è soddisfatta, quindi la cancellazione della copia sull'SSD è autorizzata. L'esecuzione resta dell'utente, perché cancellare 2,3 GB da un disco esterno è una operazione distruttiva su materiale personale e non la compie l'agente.

### MS-040 - PA-001 compiuta, e due difetti dello strumento delle azioni differite

Perimetro: `tools/check-pending-actions.py`, chiusura di PA-001 e di PA-006 nello strumento.

L'output incollato dall'utente ha rivelato due difetti, di cui uno era mio e non era stato notato.

Il primo: la chiusura di PA-006 nello strumento **non era stata applicata**. Lo script che la scriveva conteneva un `assert` sul testo da sostituire, l'assert è fallito perché gli accenti erano stati normalizzati fra la scrittura e la modifica, e lo script si è interrotto prima di scrivere il file. La modifica al documento era andata a buon fine, quella allo strumento no, e i due si contraddicevano: il documento dava PA-006 per chiusa, lo strumento la dava per aperta. Non me ne sono accorto perché ho letto l'output della parte riuscita senza controllare quella fallita. La regola che ne discende è semplice e vale oltre questo caso: quando uno script fa più modifiche e una fallisce, l'esito da guardare non è la riga di successo ma il codice di uscita.

Il secondo era un difetto di progetto più che di codice. Su PA-001 lo strumento usciva subito quando il disco non era collegato, mostrando le sole prime due condizioni. L'effetto era di nascondere le due condizioni permanenti, cioè il materiale verificato sulla macchina e la corrispondenza fra le copie, facendo sembrare la voce molto più lontana dallo sblocco di quanto fosse: chi leggeva vedeva `BLOCCATA` e due righe, non `manca solo che il disco sia collegato`. Corretto mostrando sempre tutte le condizioni e distinguendo quella transitoria dalle due permanenti.

Nel frattempo la voce si è chiusa. La cartella `Progetto stanza (software)` non esiste più su `J:`, verificato con il disco collegato, mentre le due copie restanti sono intatte: 650 file per 2,3 GB sul Desktop e 281 file per 728 MB sulla macchina con le impronte verificate. Nessun dato perduto.

Il momento e il modo della cancellazione non sono accertati, e va detto invece di ricostruirlo. Il comando dell'utente ha risposto che il percorso non esisteva mentre lo strumento riportava il disco come non collegato, e le due cose sono compatibili sia con una cartella già rimossa sia con un disco assente in quell'istante. Alle 14 dello stesso giorno la cartella c'era, perché il confronto delle impronte ne aveva letto tutti e 650 i file. Poiché l'obiettivo era che quella copia non ci fosse più e le altre due sì, la voce è compiuta a prescindere da quale spiegazione sia quella giusta.

Esito: fatto.

### MS-041 - Analisi dello spazio sull'SSD esterno, e un difetto che sbagliava di 45 GiB

Perimetro: `tools/analisi-ssd-esterno.py` nuovo, `docs/90-riferimenti/pulizia-ssd-esterno.md` nuovo.

Alla domanda su che cosa si possa cancellare da `J:` la risposta richiedeva una misura e non una stima, quindi è stato scritto uno strumento che classifica ogni voce della radice in materiale personale, cartelle di servizio e materiale trasferito, e riporta peso e numero di file senza cancellare nulla.

L'esito: circa 372 GiB di materiale personale e **1,2 GiB recuperabile**. Quasi tutto il recuperabile sta in tre voci, cioè `FOUND.002` con 429 MiB, `FOUND.000` con 412 MiB e `.Spotlight-V100` con 371 MiB; le altre sette sommate non arrivano a un megabyte, quindi cancellarle non cambia nulla.

Il difetto dello strumento merita di stare a verbale perché era del tipo peggiore. La prima versione iterava le sole cartelle della radice e ignorava i file sciolti. Su questo volume ce ne sono quattro per 45,2 GiB, di cui due archivi di backup da 25,8 e 19,4 GiB, e lo strumento riportava quindi 326 GiB di materiale personale invece di 371, sbagliando per difetto di 45 GiB senza che nulla lo segnalasse. Un totale sbagliato per difetto è peggio di un totale assente, perché non si vede che manca qualcosa: chi legge 326 non ha modo di sospettare che ne manchino 45. Corretto iterando anche i file, e con un marcatore in testa al nome invece che in coda, perché in coda veniva tagliato dal troncamento della colonna e un archivio da 26 GiB compariva indistinguibile da una cartella.

Sui due archivi di backup la conclusione è di non cancellarli, e la ragione è che la conclusione opposta non è sostenibile con i dati disponibili. La tentazione è considerare il più vecchio superato dal più recente, recuperando 25,8 GiB. Ma i nomi dichiarano perimetri diversi: il più recente esclude una cartella in più, cioè quella dei modelli 3DS, che sul volume pesa 11,4 GiB. Non sono due versioni della stessa cosa, e il più vecchio potrebbe essere l'unico a contenere qualcosa. Si aggiunge un elemento che complica e che va dichiarato invece di risolvere per ipotesi: quella cartella porta nel nome una data successiva al backup del 28 agosto, quindi non poteva esserne parte con quel nome, e non lo si stabilisce dal nome. La decisione richiede di elencare il contenuto dei due archivi, che è una lettura e non una operazione distruttiva.

Il segnale che vale più dello spazio è un altro, ed è emerso guardando la radice senza cercarlo: sul volume ci sono **cinque cartelle FOUND**, dal 30 giugno al 3 settembre, cioè cinque riparazioni del filesystem in poco più di due mesi. Le cause tipiche sono due e portano a rimedi opposti: la rimozione senza espulsione sicura, che è una abitudine da correggere, oppure un difetto del supporto, che è un hardware da sostituire. C'è un elemento di contesto che rende la prima ipotesi meno rassicurante di quanto sembri, e vale metterlo in relazione: la lettura SMART del disco interno della macchina ha riportato 24 spegnimenti non puliti su 135 accensioni. Due dischi diversi con sintomi diversi che puntano nella stessa direzione sono un indizio più forte di due sintomi isolati. Resta un indizio e non una conclusione, e il controllo che la chiude è la lettura SMART del disco esterno.

La conseguenza pratica non aspetta la diagnosi: quel disco non è il posto dove tenere l'unica copia di qualcosa. Che è esattamente il motivo per cui la cancellazione era stata subordinata alla verifica che il materiale fosse altrove, invece di essere eseguita sulla fiducia.

Verificato con: esecuzione dello strumento sul volume collegato, prima e dopo la correzione, con il totale che passa da 326 a 371 GiB; misura indipendente dei file sciolti, che conferma 45,2 GiB in quattro file; e una scansione dei caratteri di controllo su tutti i Markdown del progetto, che ha trovato e rimosso due caratteri di backspace introdotti per errore da un escape di uno script di modifica, e che ora non ne trova più nessuno.

Esito: fatto.

### MS-042 - Emendamento sul budget della catena di ascolto

Perimetro: ADR-014.

L'utente ha precisato che l'acquisto di un buon amplificatore non è un problema quando servirà, e che in alternativa si può valutare la sostituzione del convertitore, ragionando sul miglior compromesso fra qualità e costo.

ADR-012 aveva presentato l'amplificatore necessario alla strada passiva come un costo da evitare, scrivendo che diventerebbe un acquisto. Era una inquadratura sbagliata, e correggerla conta perché un vincolo di budget che non esiste distorce una decisione tecnica: avrebbe spinto verso la strada attiva per la ragione sbagliata, cioè per non comprare un componente, invece che per le sue ragioni proprie, che sono il controllo indipendente per via, l'assenza di componenti passivi in serie all'altoparlante e la possibilità di realizzare il filtro in digitale.

L'emendamento aggiunge anche un terzo termine di confronto che ADR-012 non contemplava, cioè la sostituzione del convertitore. E rileva un legame da non trascurare: la valutazione dell'interfaccia audio per l'home recording, tracciata nel progetto gemello, riguarda un dispositivo che potrebbe coprire anche il ruolo di sorgente per l'ascolto. Valutare le due cose insieme evita di comprare due dispositivi dove ne basterebbe uno, oppure di scoprire dopo che quello comprato per la registrazione non è adatto all'ascolto.

Esito: fatto. La decisione resta aperta e si prende nella fase 4a, informata dalle simulazioni invece che dal listino.

### MS-043 - I due archivi di backup confrontati: nessuno contiene l'altro

Perimetro: sola lettura sui due archivi su `J:`, indici salvati sotto `_notes/`, riscrittura della sezione corrispondente di `docs/90-riferimenti/pulizia-ssd-esterno.md`.

MS-041 aveva lasciato la questione aperta dichiarando che la conclusione "il vecchio è superato dal nuovo" non era sostenibile con i dati disponibili. I dati sono stati raccolti.

Estratti gli indici dei due archivi con `7z l`, per 159.217 e 94.221 righe, e confrontati per percorso. L'esito è che **nessuno dei due contiene l'altro**: 145.483 voci esistono solo nel più vecchio e 80.487 solo nel più recente.

La causa è `backup-sviluppo`, che spiega 145.478 delle prime e 80.377 delle seconde: fra il 28 agosto e il 4 settembre quella cartella è cambiata quasi per intero, quindi i due archivi sono due istantanee diverse della stessa cosa e non due versioni incrementali. Il più recente ha in aggiunta 81 voci sotto `_info_PW`, 26 sotto `DOCUMENTATION` e 2 sotto `SONGWRITING`.

Cade anche l'ipotesi che MS-041 aveva avanzato sulla differenza di peso. Si era supposto che i 6 GiB di scarto dipendessero dalla cartella dei modelli 3DS, esclusa dal più recente per dichiarazione del suo stesso nome. Quella cartella non compare fra le differenze, quindi non era nemmeno nel più vecchio, coerentemente con il fatto che porti nel nome una data successiva a quel backup. Lo scarto si spiega interamente con il rimescolamento di `backup-sviluppo`.

Conseguenza: cancellare il più vecchio costa 145.478 versioni di file che non esistono altrove in forma archiviata. La domanda "posso cancellarlo perché c'è il nuovo" ha quindi risposta negativa e documentata. Se quelle versioni servano è una decisione dell'utente e non una questione tecnica, dato che la cartella `backup-sviluppo` esiste ancora sul disco con il suo contenuto corrente.

Nota operativa: `7z` non è sul PATH di PowerShell su questa postazione, e il comando che lo invocava per nome era quindi ineseguibile. L'eseguibile sta in `C:\Program Files\7-Zip\7z.exe`, e va invocato per percorso completo oppure aggiunto al PATH. È lo stesso genere di errore di MS-027 su `ssh-copy-id`, cioè un comando fornito assumendo che sia disponibile invece di verificarlo.

Esito: fatto.

### MS-044 - La copia sul Desktop non si cancella adesso, e la ragione è il conteggio delle copie

Perimetro: PA-007 nuova, aggiornamento dello strumento delle azioni differite.

L'utente ha proposto di cancellare anche `C:\Users\Utente\Desktop\Progetto stanza (software)`, dato che tutto il necessario è sulla macchina. Il ragionamento è corretto sul contenuto e sbagliato sul momento, e vale spiegare la differenza perché è il tipo di errore che costa dati.

Oggi le voci utili del corredo esistono in due copie, una sul Desktop e una sulla macchina. Cancellare il Desktop le porta a **una copia sola**, e quella copia vive su una macchina che sta per subire una reinstallazione con riformattazione di una partizione, per ADR-013. Ridurre a una copia proprio prima di una operazione che tocca le partizioni è il momento peggiore possibile: non perché la procedura sia rischiosa, ma perché l'unico rischio irreversibile che ha, cioè l'errore umano nella selezione della partizione da formattare, è esattamente quello contro cui una seconda copia protegge.

La condizione di sblocco è quindi una sola, ed è un passo che era già in programma: la copia di sicurezza di `/home` fuori dalla macchina, cioè la fase 1.3. Fatta quella, le copie tornano due e il Desktop diventa la terza, quindi ridondante.

Va dichiarato con precisione che cosa si perderà quando si cancellerà. Delle sei voci trasferite nulla, perché sono sulla macchina con le impronte verificate. Delle otto voci scartate dal censimento si perde l'unica copia esistente, perché non sono state trasferite di proposito: la perdita è voluta e documentata, dato che il censimento stabilisce che nessuna serve e che per ciascuna esiste una sostituzione già disponibile, ma resta irreversibile e va detta.

Aggiunto al comando di cancellazione un passo che lo precede e che non è decorativo: la riverifica delle impronte sulla macchina, da lanciare subito prima e non ore prima.

Esito: fatto per la decisione. L'esecuzione è subordinata alla fase 1.3.

### MS-045 - Chiarito un equivoco: l'agente non ha cancellato nulla su J:

Perimetro: PA-008 nuova, con la verifica dello stato attuale del disco.

L'utente ha chiesto che cosa dovesse cancellare "se l'ho cancellato io". L'equivoco va chiarito perché riguarda la fiducia su un disco con materiale personale: **l'agente non ha cancellato nulla su quel volume, e non ha eseguito alcuna cancellazione in tutta la sessione.** La cartella `Progetto stanza (software)` risultava già assente quando è stata verificata, come MS-040 registra dichiarando di non sapere quando e come sia sparita.

Verificato lo stato attuale: le nove voci di servizio sono tutte ancora presenti, comprese le tre che contengono lo spazio recuperabile. Quindi c'è ancora tutto da fare, e PA-008 lo elenca con i pesi misurati.

Il recuperabile è concentrato in tre voci per circa 1.212 MiB: `FOUND.002` con 429 MiB e 77 file, `FOUND.000` con 412 MiB e 90 file, e `.Spotlight-V100` con 371 MiB e 76 file. Le altre sei, cioè `FOUND.001`, `FOUND.003`, `FOUND.004`, `.Trashes`, `.fseventsd` e `.TemporaryItems`, esistono ma sommate non arrivano a un megabyte: cancellarle non cambia niente.

Aggiunta una precauzione prima della cancellazione delle due `FOUND` grandi, che insieme contengono 167 file recuperati da `chkdsk` senza il loro nome originale. Nella grande maggioranza dei casi sono inservibili, ma la maggioranza non è la totalità, e guardare i venti più grandi costa un minuto.

Lo strumento delle azioni differite ora misura la presenza delle tre voci e riporta quanto resta da recuperare, così che il controllo sia un comando invece di un ricordo, e ricorda in quella stessa schermata che i due archivi `.7z` non si cancellano, perché è il punto dove la tentazione è più forte.

Esito: fatto.

### MS-046 - PA-008 compiuta: 1,2 GiB recuperati su J:

Perimetro: verifica dello stato del disco esterno dopo l'intervento dell'utente.

L'utente ha guardato i venti file più grandi delle due cartelle `FOUND` e le ha cancellate insieme alle altre quattro e a `.Spotlight-V100`. Verificato: tutte e sei le voci sono rimosse.

Vale registrare cosa contenevano, perché la precauzione di guardare prima si è rivelata sensata anche se l'esito è stato di cancellare. I due frammenti maggiori erano di 247 MB in `FOUND.000` e 206 MB in `FOUND.002`, e da soli valevano 453 dei 841 MB complessivi. Frammenti di quelle dimensioni non sono documenti: sono immagini disco, archivi o file multimediali di cui `chkdsk` ha trovato i dati senza il nome. Restano inservibili senza sapere che cosa fossero, ma la loro dimensione dice che il filesystem ha perso qualcosa di sostanzioso, non solo metadati sparsi. È un elemento in più a favore di PA-009, cioè della lettura SMART di quel disco.

Esito: fatto.

### MS-047 - La destinazione del backup di /home, e perché non può stare sulla stessa macchina

Perimetro: ADR-015, aggiornamento della fase 1.3 della procedura.

L'utente ha chiesto se la copia di sicurezza di `/home` possa stare su una partizione della stessa macchina, oppure temporaneamente su questa postazione Windows. La prima risposta è no e la seconda è sì, e le ragioni sono diverse fra loro.

Sulla stessa macchina non è possibile né sensato, e la verifica lo mostra: il sistema ha **un solo disco**, `nvme0n1` da 465,8 GB, con quattro partizioni e nient'altro, cioè EFI da 1 GB, root da 74,5 GB, swap da 14,9 GB e `/home` da 375,3 GB. Non ci sono altri dischi e non c'è alcun disco USB collegato.

Le tre varianti pensabili fallirebbero tutte, e per ragioni diverse che vale distinguere. Copiare `/home` su root è inutile, perché root è la partizione che viene formattata. Copiare `/home` su se stessa non protegge da nulla, perché il rischio contro cui il backup esiste è precisamente la formattazione per errore di quella partizione: la copia morirebbe con l'originale. Creare una partizione nuova richiederebbe di ridurre `/home`, che è una operazione rischiosa in sé, e non proteggerebbe comunque dal rischio principale, perché un errore nella selezione della partizione da formattare può colpire anche quella nuova, e un guasto del disco porta via tutto.

La regola generale che ne discende, e che vale oltre questo caso: una copia di sicurezza sullo stesso supporto della cosa che protegge non è una copia di sicurezza, è una copia.

Sulla postazione Windows invece funziona, ed è la scelta adottata. `/home` pesa 4,4 GB e il disco di destinazione ne ha 198 liberi, quindi il costo è trascurabile. E soprattutto è una **macchina fisicamente diversa**, che è l'unica proprietà che rende un backup un backup.

Il metodo richiede una precisazione che non è pedanteria. La copia si fa con `tar` in streaming attraverso `ssh` e non con `scp` dei file, perché la destinazione è un filesystem NTFS che non sa rappresentare proprietario, gruppo e permessi POSIX: copiando i file singoli quelle informazioni andrebbero perdute e il ripristino produrrebbe una `/home` con i permessi sbagliati. Dentro un archivio `tar` quei metadati sopravvivono anche su NTFS, perché sono contenuto dell'archivio e non attributi del filesystem. Si usa `--numeric-owner` per registrare gli identificativi numerici invece dei nomi, così che il ripristino non dipenda dall'esistenza dell'utente al momento in cui si ripristina.

L'archivio non viene compresso, ed è una scelta e non una dimenticanza: dei 4,4 GB la maggior parte sono installer, archivi e pacchetti già compressi, quindi la compressione costerebbe tempo di processore per un guadagno prossimo a zero.

La destinazione è fuori dalla cartella del progetto, allora in `E:\_backup-ubuntu-studio\` e oggi sul Desktop della postazione, perché un archivio di 4,4 GB non ha ragione di stare dentro un repository, nemmeno in una cartella ignorata.

Esito: si veda la voce successiva per l'esecuzione.

### MS-048 - Il corredo era già sulla macchina: il trasferimento ha prodotto una copia in più

Perimetro: constatazione sullo stato della macchina, con conseguenza su PA-007.

Ispezionando la scrivania della macchina per capire da cosa venissero 2,3 GB di `/home`, è emerso che il corredo software **era già lì**, nelle sue tre cartelle originali: `DIY Loudspeaker Pack Softwares` per 117 MB, `Room acoustics` per 563 MB e `Simulators` per 1,6 GB. Ci sono anche gli installer di Akabak e di VACS a 32 bit, sciolti sulla scrivania.

Il trasferimento di MS-039 ha quindi prodotto una seconda copia sulla macchina, sotto `~/electroacoustics`, invece della prima. Non è lavoro inutile e vale spiegare perché: la copia nuova è il sottoinsieme selezionato dal censimento, organizzato in un albero con le impronte verificate e coperto dal manifest, mentre quella sulla scrivania è il materiale grezzo con tutte e quattordici le voci, comprese le otto scartate. Sono due cose diverse con due scopi diversi. Resta il fatto che il peso su `/home` è oggi maggiore del necessario.

La conseguenza importante riguarda PA-007, cioè la cancellazione della copia sul Desktop di Windows, e **corregge in meglio** il ragionamento di MS-044. Lì avevo detto che cancellare il Desktop di Windows avrebbe portato le voci utili a una copia sola: non è vero, perché sulla macchina esistono due copie indipendenti, quella organizzata e quella grezza sulla scrivania. Il conteggio corretto è quindi di tre copie oggi e due dopo la cancellazione.

Questo non cambia la decisione ma ne cambia la ragione, e la differenza conta perché una decisione giusta per il motivo sbagliato non regge alla prima verifica. La ragione valida che resta è che entrambe le copie sulla macchina vivono sulla stessa partizione dello stesso disco, quindi non sono due copie indipendenti rispetto al rischio che il backup deve coprire: un errore sulla partizione le porta via entrambe. La condizione di sblocco resta la copia di sicurezza di `/home` fuori dalla macchina, ma ora perché è l'unica copia su un supporto diverso, non perché sia la seconda.

Emerge anche una cosa da sistemare più avanti, quando l'ambiente verrà ricostruito: sulla macchina il materiale sarà in tre posti, cioè la scrivania, `~/electroacoustics` e il collegamento simbolico. Vale consolidare, ma dopo la reinstallazione e non prima, perché toccare adesso l'unica installazione funzionante non porta nulla.

Esito: fatto per la constatazione. La correzione al ragionamento di MS-044 è riportata in PA-007.

### MS-049 - Backup di /home eseguito e verificato: fase 1.3 chiusa

Perimetro: la cartella `_backup-ubuntu-studio` fuori dal repository, aggiornamento di PA-007.

Eseguita la copia di sicurezza di `/home` con `tar` in streaming attraverso `ssh`, secondo ADR-015. L'archivio pesa 4,4 GB e non è compresso.

La verifica è la parte che conta, perché un backup non verificato non è un backup. Tre controlli. L'archivio si legge per intero senza errori. Il conteggio dei file coincide esattamente: **13.498 nell'archivio contro 13.498 sulla macchina**. E i metadati sono conservati, come mostra l'elenco esteso, che riporta permessi e proprietario numerico `1000/1000`: è la ragione per cui si è usato `tar` e non `scp`, dato che NTFS non sa rappresentarli.

Registrata anche l'impronta SHA-256 dell'archivio, così che una eventuale copia successiva sia confrontabile.

Conseguenza: PA-007 è sbloccata, cioè la copia del corredo sul Desktop di Windows può andare. E la fase 1.2 della procedura, che prevedeva un archivio separato dei soli prefix Wine, diventa ridondante: i prefix stanno sotto `/home` e questo archivio li contiene.

Esito: fatto.

### MS-050 - Akabak è a 32 bit: la scoperta che corregge tre decisioni e sei documenti

Perimetro: ADR-016, correzioni alle fasi 7 e 8 della procedura e a quattro pagine del blocco ambiente.

Ispezionando la scrivania della macchina per capire da dove venissero 2,3 GB di `/home` sono comparsi i lanciatori `.desktop` di Akabak e di VACS, e leggerli ha aperto una catena di verifiche il cui esito ribalta una parte del piano.

I fatti, tutti misurati. Il prefix in uso è `~/.wine` e il suo registro dichiara `#arch=win32`, cioè è **a 32 bit**; `syswow64` è assente, come deve essere in un prefix a 32 bit. L'eseguibile installato `AKABAK.exe` è `PE32 executable, Intel 80386`, cioè **a 32 bit**, e lo stesso vale per `VACS_32.exe`; la libreria che entrambi portano si chiama `Matrix32.dll`. Nel prefix non esiste alcun `winetricks.log`, non esiste `Microsoft.NET/Framework/v4` e non è installato alcun font Microsoft di base. I lanciatori invocano `wine-stable`, che su questa macchina esiste come comando e riporta la versione 9.0.

Ne segue che tre affermazioni del documento sorgente sono false. Akabak 3 non è a 64 bit. Non è vero che non esista una build a 32 bit, dato che quella installata lo è. E non richiede .NET Framework 4.8, né i font di base, né i runtime Visual C++, perché la configurazione che funziona non ne ha nessuno. La lista di dipendenze del sorgente descriveva **ciò che era stato tentato durante il troubleshooting, non ciò che serviva**, e questa è la lettura che riconcilia tutto: la cronologia di apt del 13 agosto 2025 mostra installazioni, purghe e reinstallazioni, cioè la traccia di una ricerca per tentativi, non di una procedura.

Chiude anche una lacuna che due documenti dichiaravano aperta, cioè quale variante di VACS fosse installata e come fosse stato risolto il fallimento iniziale. La risposta è la build a 32 bit, ed era **esattamente l'ipotesi formulata nella corrispondenza del 13 agosto 2025**, dove si chiedeva all'autore se il problema potesse dipendere dall'aver usato la versione a 64 bit invece della 32. Quell'ipotesi era corretta.

Le conseguenze sono sostanziali e vanno dichiarate una per una. La fase 7 della procedura prescriveva quattro prefix a 64 bit con `dotnet48` per tutti: sbagliata per Akabak e VACS, corretta. Il consiglio di non dichiarare l'architettura `i386`, dato in ADR-009 e ripetuto in ADR-013, è **rovesciato**: senza `i386` il solo software del progetto che oggi funziona non funzionerebbe. La mappa dei prefix passa da quattro a 64 bit a uno a 32 bit più tre a 64. E le pagine sui prefix, sulla configurazione e sui programmi sono state corrette nei punti che riportavano l'architettura e le dipendenze sbagliate.

Resta valida la parte di ADR-004 che non riguarda l'architettura, cioè un prefix per programma, con l'eccezione dichiarata di Akabak e VACS che condividono il proprio perché si usano in sequenza e perché così è la configurazione funzionante.

La lezione di metodo è la più costosa della sessione, e va scritta per intero. Tre decisioni consecutive, ADR-004, ADR-009 e ADR-013, hanno propagato una affermazione non verificata presa da un appunto, e ciascuna l'ha usata come premessa della successiva senza tornare alla fonte. Il risultato è stata una prescrizione operativa sbagliata su sei documenti, che se eseguita avrebbe prodotto un ambiente in cui il programma centrale del progetto non parte. Il controllo che l'avrebbe evitato costava un comando: `file` sull'eseguibile installato. È la stessa lezione di MS-029, dove tre cause su quattro di una diagnosi erano false: la differenza fra un appunto e una misura non è di grado.

Esito: fatto.

### MS-051 - Il release code in chiaro sulla scrivania della macchina

Perimetro: constatazione, senza modifiche.

Sulla scrivania della macchina esiste un file vuoto il cui **nome** è il release code di Akabak, e nella cartella di installazione di VACS esiste un `ReleaseCode.rtf`. Sono due copie in chiaro di un codice di attivazione, su una macchina che questo progetto documenta e che verrà sottoposta a backup.

Non è una falla e non va drammatizzata: è la macchina personale dell'utente, il codice vale solo per quell'hardware, e tenerlo a portata di mano su una scrivania è una scelta comprensibile di comodità. Vale registrarlo per due ragioni pratiche.

La prima è che il backup di `/home` eseguito in MS-049 contiene quel nome di file, quindi l'archivio di `/home` contiene il codice. Non è un problema perché resta su una macchina personale, ma va saputo, perché se quell'archivio venisse spostato su un servizio condiviso il codice ci andrebbe con lui.

La seconda è che spiega perché la scheda riservata di questo progetto vive sotto `_notes/` e non fra i file tracciati: non per proteggere un segreto che l'utente tiene su una scrivania, ma perché il repository è pubblico su GitHub e lì il codice avrebbe una diffusione di natura diversa.

Esito: fatto, come constatazione. Nessuna azione proposta.

### MS-052 - Machine Identifier confermato in interfaccia: PA-005 chiusa nella sostanza

Perimetro: chiusura della seconda delle tre voci privilegiate della fase 0, quattro documenti aggiornati.

L'utente ha aperto sulla macchina la finestra delle informazioni di AKABAK e quella del release code, e ha fornito le due immagini. Il confronto che serviva è quello fra il Machine Identifier mostrato dal programma e il valore conservato nella scheda riservata sotto `_notes/`: **coincidono**. Coincide anche il release code inserito, e il programma dichiara `Release Code valid` con l'indicatore verde. Nessuno dei due valori entra in un file tracciato, perché il repository è pubblico.

Il valore del controllo non è la spunta ma ciò che stabilisce. L'identificativo hardware che AKABAK calcola sotto Wine è lo stesso di agosto 2025, dopo un anno di uso, aggiornamenti e la sedimentazione dell'ambiente Wine che la fotografia della macchina documenta. È la prova sperimentale di ciò che la pagina sui prefix afferma per costruzione, cioè che una licenza machine-based non dipende dal prefix né dall'installazione di Wine, e quindi la conferma che l'installazione pulita non mette a rischio la licenza. Era il solo controllo che dopo la formattazione non sarebbe più stato ripetibile, e per questo era in elenco.

Le finestre hanno portato in dote tre fatti che nessun documento aveva registrato, e due di essi correggono un'aspettativa. Il programma si dichiara **Standard Edition** e non professionale, malgrado l'installer conservato si chiami `AKABAK_Pro_v324b126.exe` e malgrado l'autore avesse scritto di scaricare la versione professionale: l'installer è uno, e l'edizione la determina il release code, coerentemente con la *student license* per cui l'utente era stato registrato. Quali funzioni distinguano le due edizioni non è accertato e non va supposto dal nome del file. Il profilo di Windows dichiarato dal prefix è `NT 10.0 (Build 19043)`, cioè Windows 10, il che trasforma in fatto misurato una prescrizione che la pagina di configurazione dava per uniformità. E sotto il release code compare `Security key not connected to the USB port`, cioè esiste una chiave hardware come portatore alternativo del diritto d'uso, non in uso qui: non è un errore da correggere ma l'alternativa tecnica da valutare nel solo caso che invaliderebbe il codice, cioè un cambio significativo di hardware.

Con questa voce PA-005 resta aperta su una sola delle tre, l'esito reale di `sudo apt update`, che ADR-013 ha reso irrilevante perché su un sistema che verrà azzerato non informa nessuna decisione. La fase 0 è quindi chiusa nella sostanza: tutte le verifiche che potevano spostare una decisione sono state fatte, e nessuna l'ha spostata.

Aggiornati di conseguenza `docs/90-riferimenti/licenze-e-registrazioni.md` con la sezione sullo stato verificato, `docs/90-riferimenti/timeline-akabak-vacs.md` con la voce di cronologia del 2026-09-07 e con la riscrittura della sezione finale, che elencava come da verificare tre cose oggi tutte verificate, `docs/10-ambiente/fotografia-macchina-2026-09-07.md` nella sezione delle voci pendenti, che ne dichiarava pendenti due già chiuse, e `docs/10-ambiente/wine-configurazione.md` sul profilo di Windows.

Esito: fatto.

### MS-053 - I 2047 MByte erano già in uno screenshot: la conferma che sarebbe potuta arrivare prima

Perimetro: constatazione di metodo, nessuna decisione cambiata.

La finestra delle informazioni di AKABAK riporta la memoria come `1897 / 2047 MBytes` su una macchina che ha 16 GB di RAM installata. Non è un difetto: è la firma inconfondibile di un processo a **32 bit**, che dispone di 2 GB di spazio di indirizzamento in modo utente indipendentemente dalla memoria fisica presente. È quindi una conferma indipendente di ADR-016, ottenuta per una via completamente diversa da quella che ha prodotto quella decisione, cioè il formato dell'eseguibile e l'architettura dichiarata dal registro del prefix.

Il fatto scomodo, e va scritto perché è la parte utile, è che questa conferma era disponibile **prima** dell'indagine che ha stabilito il fatto. L'immagine appartiene alla stessa serie di screenshot da cui era stata ricostruita la corrispondenza con l'autore, ed è stata letta soltanto oggi, quando è stata fornita per un'altra ragione. Se fosse stata letta allora, ADR-004, ADR-009 e ADR-013 non avrebbero propagato per tre decisioni consecutive un'affermazione sbagliata presa da un appunto, e sei documenti non avrebbero portato una prescrizione che, eseguita, avrebbe prodotto un ambiente in cui il programma centrale del progetto non parte.

La lezione non è leggere tutti gli screenshot, che è irrealizzabile e non è un metodo. È più precisa: quando una premessa regge una decisione, il materiale già in mano va interrogato **su quella premessa** invece di essere letto per il tema per cui era stato raccolto. Gli screenshot erano stati letti per ricostruire lo scambio di posta elettronica, e la domanda sull'architettura non era stata posta a un materiale che conteneva la risposta. È la stessa lezione di MS-029 e MS-050, vista dal lato dell'archivio invece che da quello della misura.

Esito: fatto, come constatazione.

### MS-054 - L'archivio di /home spostato, e un controllo che inchiodava un percorso

Perimetro: `tools/check-pending-actions.py`, ADR-015, quattro documenti, sblocco dichiarato di PA-007.

L'utente ha spostato l'archivio di backup da `E:\_backup-ubuntu-studio\` a `C:\Users\Utente\Desktop\_backup-ubuntu-studio\`. La dimensione è identica al byte, 4.662.927.360, quindi la verifica di MS-049 vale ancora per quel file: è stato spostato e non rigenerato.

Lo spostamento ha però rotto un controllo, e il modo in cui l'ha rotto è più interessante dello spostamento. Lo strumento delle azioni differite verificava la condizione di sblocco di PA-007 cercando l'archivio a un percorso fisso, quindi dallo spostamento in avanti dichiarava mancante un backup che esiste, e con esso riportava PA-007 a bloccata per un motivo falso. È il difetto peggiore che uno strumento di verifica possa avere: non sbagliare l'esito in senso permissivo, che si nota subito perché qualcosa va storto, ma in senso restrittivo, che si crede e blocca un lavoro legittimo.

Corretto rendendo il nome del file l'invariante e la cartella una fra più posizioni plausibili, con una funzione che restituisce la prima in cui l'archivio risulta presente. Aggiunto anche un confronto della dimensione con quella registrata, che segnala un'anomalia se l'archivio è stato rigenerato o è incompleto, perché in quel caso la verifica di MS-049 non varrebbe più e va rifatta prima di cancellare qualcosa. Il controllo eseguito dopo la correzione trova l'archivio sul Desktop, dimensione coincidente, e dichiara PA-007 sbloccata. ADR-015 aggiornata per dire che la destinazione fa parte della decisione solo per la proprietà che conta, cioè essere una macchina diversa da quella protetta, e non per la lettera di unità.

Resta da dire la cosa che l'utente ha chiesto due volte, e che era rimasta implicita fra un aggiornamento di stato e l'altro: **la copia del corredo sul Desktop si può cancellare adesso.** La condizione era una sola, il backup di `/home` fuori dalla macchina, ed è soddisfatta e verificata. L'unica perdita è quella voluta, cioè le otto voci che il censimento ha scartato con una sostituzione nativa o gratuita già disponibile per ciascuna; le sei voci utili restano sulla macchina con le impronte verificate e nell'archivio. La voce PA-007 è stata riscritta perché lo dicesse in apertura invece di farlo dedurre, e il testo con cui era stata aperta è conservato ma marcato come superato.

Esito: fatto per la parte documentale e strumentale; la cancellazione è dell'utente.

### MS-055 - La copia del template nel progetto gemello è rimasta indietro

Perimetro: `docs/PENDING-ACTIONS.md` del progetto gemello, nuova voce PA-002.

La verifica `md-unwrap --check` eseguita sul progetto gemello dopo la propagazione segnala cinque file non conformi alla convenzione della riga sorgente unica, per quattordici righe da unire: `CLAUDE.local.md` e quattro modelli sotto `.claude/templates/_notes/`. La stessa verifica su questo progetto non segnala nulla.

La spiegazione non è che gli strumenti si comportino diversamente. Il confronto dei file mostra che sono **diversi**: la copia del template nel gemello è anteriore alla propagazione della convenzione Markdown fatta qui, quindi non è un difetto nuovo ma un ritardo di allineamento. Vale registrarlo perché l'ipotesi immediata sarebbe stata un marcatore di esclusione presente qui e assente là, e quella ipotesi è falsa: nessuno dei due progetti ha marcatori su quei file.

Non corretto di proposito. Sono modelli in un altro repository, fuori dal blocco che lo strumento di propagazione dichiara di gestire, cioè `docs/10-ambiente/`, e correggerli qui significherebbe allargare in silenzio il perimetro di una sincronizzazione unidirezionale dichiarata. Aperto invece come PA-002 nel gemello, con l'osservazione che conviene trattarla insieme a PA-003 di questo progetto, perché la sorgente comune è `template-claude-developing` e correggere lì risolve entrambe le copie invece di rincorrerle.

Esito: fatto come registrazione; la correzione è una decisione dell'utente.

### MS-056 - Due danni tipografici autoinflitti in dieci minuti, e come sono stati trovati

Perimetro: `docs/OPERATIONS-LOG.md`, riparazione di danni introdotti in questa stessa sessione.

Va scritto perché è il tipo di episodio che si tende a non registrare, essendo un errore proprio e rimediato subito, ed è invece quello da cui si impara di più. Due danni consecutivi, il secondo prodotto dalla riparazione del primo.

Il primo. Scritta la voce MS-055 con le forme non accentate del tipo `e'` e `perche'`, ho lanciato `fix-missing-accents.py` sul file per normalizzarle, e lo strumento ha prodotto esattamente il difetto che MS-014 documenta in questo stesso registro: `perche'` è diventato `perché'` e `cioe'` è diventato `cioè'`, cioè accento corretto più apostrofo orfano. Non è un difetto nuovo dello strumento, è quello già diagnosticato, e la lezione è che averlo documentato non basta a non incapparci: MS-014 aveva escluso la catena tipografica dalla sequenza di verifica su `.` proprio per questo, e io l'ho invocata a mano su un singolo file aggirando la propria mitigazione.

Il secondo, ed è il più istruttivo. Per rimuovere gli apostrofi orfani ho applicato una sostituzione con espressione regolare su tutto il file, nella forma vocale accentata seguita da apostrofo. Ha funzionato, e ha anche cancellato gli apostrofi delle **citazioni deliberate** di MS-014, dove le stringhe `c'è'` e `com'è'` non sono errori del testo ma gli esempi del difetto che quella voce spiega. Il risultato era un paragrafo che dichiarava che il difetto produce `c'è` e `perché`, cioè le forme corrette, rendendo incomprensibile l'intera spiegazione.

La regola che ne discende, e che vale oltre la tipografia. Una sostituzione automatica su un file di documentazione tecnica non distingue il testo dagli esempi, e in un documento che parla di errori gli esempi **sono** errori: applicare una correzione globale a un file che contiene citazioni di forme sbagliate ne distrugge il contenuto. La sostituzione va quindi limitata alla porzione appena scritta, non estesa al file, oppure va verificata leggendo il diff riga per riga.

Ed è così che il danno è stato trovato, che è la parte da conservare. Non da un controllo tipografico, che dopo la riparazione risultava pulito su entrambe le versioni, quella giusta e quella rovinata, perché `c'è` è una forma perfettamente corretta. È stato trovato leggendo il `git diff` di ciò che avevo modificato e chiedendosi perché comparissero righe rimosse in un microstep che non stavo toccando. Il controllo automatico non poteva vederlo: il difetto era semantico, non ortografico. La verifica che ha funzionato è quella che si fa sempre e comunque, cioè guardare l'elenco completo delle righe cambiate e giustificarne ciascuna, e in questo caso l'esito finale è zero rimozioni non attese.

Un terzo difetto minore, trovato nello stesso passaggio e con lo stesso metodo: scrivendo MS-055 avevo introdotto una sequenza `l` più `i` senza punto più accento grave combinante, al posto di una semplice `lì`. Un controllo dei punti di codice fuori dal latino ha isolato il carattere combinante U+0300 e la riparazione è stata immediata. Il progetto era stato ripulito dai caratteri di controllo in una sessione precedente, quindi il controllo esiste già come abitudine ed è ciò che lo ha intercettato prima del commit.

Esito: fatto, con i tre difetti riparati e verificati.

## Che cosa resta da fare, e da che cosa dipende

Questa sezione ha cambiato natura tre volte nel corso della sessione, ed è utile dirlo perché la successione è un progresso e non uno stallo. All'inizio elencava microstep bloccati da una macchina di stato ignoto; poi il blocco si è ristretto all'installazione della chiave SSH, che è una azione dell'utente non delegabile; oggi quella chiave è installata, la fase 0 è chiusa nella sostanza e la fase 1 è compiuta, quindi **non esiste più alcun microstep bloccato da una condizione esterna**. Ciò che resta è lavoro da eseguire, in ordine, e il suo unico prerequisito è la disponibilità dell'utente davanti alla macchina.

Le fasi 0 e 1 sono chiuse. La fotografia della macchina attuale è prodotta e sta in `docs/10-ambiente/fotografia-macchina-2026-09-07.md`; ha smentito tre delle quattro cause che avevo attribuito al blocco di aggiornamento, ha chiuso con esito positivo lo stato di salute del disco, ha chiuso la lacuna su come fu risolto il fallimento iniziale di VACS, e ha portato alla scoperta dei 32 bit registrata in ADR-016. Il trasferimento dei materiali è compiuto e verificato per impronte, si veda MS-039. La copia di sicurezza di `/home` è fatta e verificata, si veda MS-049. Il Machine Identifier è confermato identico a quello a cui il Release Code è legato, si veda MS-052. Della fase 0 resta non eseguito soltanto l'esito reale di `sudo apt update`, che ADR-013 ha reso irrilevante.

Quello che segue è il lavoro rimanente, nell'ordine delle fasi della procedura di installazione pulita descritta in `docs/10-ambiente/installazione-pulita-26-04.md`.

L'installazione pulita di Ubuntu Studio 26.04 LTS conservando `/home`, secondo le fasi da 2 a 5. È il passo che contiene l'unico rischio irreversibile della procedura, cioè l'errore umano nella selezione delle partizioni, e il presidio contro quel rischio è già in posizione.

La verifica della catena audio a bassa latenza e la ricostruzione dell'ambiente Wine, secondo le fasi 6 e 7. Da eseguire **dopo** la reinstallazione e non prima: per ADR-013 l'ambiente attuale non si pulisce, perché sarebbe lavoro buttato su un sistema che verrà azzerato. La forma di questa ricostruzione è cambiata per ADR-016 e va letta lì e non nella versione che questa sezione portava fino al 2026-09-07: i prefix sono quattro ma non tutti a 64 bit, e l'architettura `i386` va **dichiarata** e non evitata, perché senza di essa il solo software del progetto che oggi funziona non funzionerebbe.

La reinstallazione dei programmi e la riattivazione della licenza con il codice esistente, secondo la fase 8. Resta la prova pratica dell'affermazione sulla licenza legata alla macchina, ma il suo esito è oggi molto più prevedibile di quando questa voce fu scritta, perché MS-052 ha verificato che l'identificativo hardware non è cambiato in un anno: se il codice venisse rifiutato, la spiegazione andrebbe cercata in un errore di inserimento o di prefix, non in un cambio di identificativo.

L'installazione del corredo Progetto stanza secondo le fasi da 8.5 a 8.9, cioè VituixCAD, EASE Focus 3.1.260 con il servizio di database AFMG e il database dei GLL, e ARTA. Ramsete resta fuori finché PA-002 non è risolta.

L'igiene post-installazione secondo la fase 10, cioè la direttiva di aggiornamento su `Prompt=lts`, la disattivazione della sospensione automatica con il Wake-on-LAN come rete di sicurezza, la chiave SSH dedicata con la disattivazione dell'autenticazione per password, e la prenotazione dell'indirizzo sul router.

La fotografia finale e il confronto con quella iniziale, secondo la fase 11.

Fuori da questa sequenza restano le azioni differite di `docs/PENDING-ACTIONS.md`, che non dipendono dalla reinstallazione. Di quelle, due sono eseguibili adesso e sono entrambe dell'utente: la cancellazione della copia del corredo sul Desktop, cioè PA-007, sbloccata dal backup di `/home`, e la lettura dello SMART dell'SSD esterno, cioè PA-009, che ha una ragione concreta dietro, cinque riparazioni del filesystem in due mesi. Lo strumento `python tools/check-pending-actions.py` dice quali condizioni sono soddisfatte, così che il controllo sia un comando invece di un ricordo.
