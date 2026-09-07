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

## Microstep bloccati, e da che cosa dipendono ora

Il blocco è cambiato natura nel corso della sessione, e vale registrarlo perché è un progresso e non uno stallo. All'inizio la macchina era di stato ignoto, poi si è rivelata sospesa e non spenta, poi sveglia e raggiungibile ma senza autenticazione configurata. Il blocco attuale è quindi su una singola azione dell'utente, cioè l'installazione della chiave SSH descritta nella fase 10.3 della procedura, che richiede la password una volta sola e non è delegabile.

Sbloccata quella, i microstep seguenti diventano eseguibili nell'ordine in cui sono elencati, e ciascuno corrisponde a una fase numerata della procedura di installazione pulita.

La fotografia completa della macchina attuale, in quattordici file, secondo la fase 0. Include la conferma o la smentita della diagnosi del blocco di aggiornamento, la lettura dello stato di salute dell'SSD, l'inventario dei prefix Wine esistenti che chiude la lacuna su come fu risolto il fallimento iniziale di VACS, e la verifica che il Machine Identifier di Akabak sia ancora quello a cui il Release Code è legato.

L'esecuzione del trasferimento dei materiali, con verifica delle impronte sulla destinazione, secondo la fase 1 e `docs/TRANSFER-MANIFEST.md`.

La copia di sicurezza di `/home` fuori dalla macchina, secondo la fase 1.3. Non è opzionale: copre l'unico rischio irreversibile della procedura, cioè l'errore umano nella selezione delle partizioni.

L'installazione pulita di Ubuntu Studio 26.04 LTS conservando `/home`, secondo le fasi da 2 a 5.

La verifica della catena audio e la ricostruzione dell'ambiente Wine con un prefix per programma e senza architettura a 32 bit, secondo le fasi 6 e 7.

La reinstallazione dei quattro programmi e la riattivazione della licenza con il codice esistente, secondo la fase 8. È la prova pratica dell'affermazione registrata in ADR-003 sulla licenza legata alla macchina, e il suo esito va registrato come tale: se il codice viene accettato, l'affermazione è confermata; se il Machine Identifier fosse cambiato, ADR-003 va corretta con una voce nuova nel registro delle decisioni.

L'installazione del corredo Progetto stanza secondo le fasi da 8.5 a 8.9, cioè VituixCAD, EASE Focus 3.1.260 con il servizio di database AFMG e il database dei GLL, e ARTA. Ramsete resta fuori finché PA-002 non è risolta.

L'igiene post-installazione secondo la fase 10, cioè la direttiva di aggiornamento su `Prompt=lts`, la disattivazione della sospensione automatica con il Wake-on-LAN come rete di sicurezza, la chiave SSH dedicata con la disattivazione dell'autenticazione per password, e la prenotazione dell'indirizzo sul router.

La fotografia finale e il confronto con quella iniziale, secondo la fase 11.

E infine, con un blocco proprio e indipendente dai precedenti, la cancellazione della copia ridondante del corredo sull'SSD esterno, tracciata come PA-001 in `docs/PENDING-ACTIONS.md`. Dipende dal collegamento del disco `J:`, che in questa sessione non era presente, dal completamento verificato del trasferimento, e dal confronto per impronte fra le due copie. Lo strumento `python tools/check-pending-actions.py` dice quali di queste condizioni sono soddisfatte, così che il controllo sia un comando invece di un ricordo.
