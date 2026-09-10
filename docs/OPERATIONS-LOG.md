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

Un fatto nuovo che nessun documento riportava: della versione 3.1.10 di EASE Focus la copia sul Desktop ha soltanto un collegamento e non la cartella. Da qui era stata tratta l'inferenza che quel contenuto vivesse sul solo SSD esterno, e quindi che le due copie non fossero identiche. *Quella inferenza è stata smentita il 2026-09-07 e va letta come ritirata*: il collegamento è presente e identico su entrambe le copie, che risultano identiche file per file, e punta invece a un quarto disco. Si vedano MS-024 e MS-025.

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

Va registrato inoltre che *la Scarlett 2i2 non è collegata*: l'elenco USB non riporta alcun dispositivo Focusrite, e le sole schede viste sono l'audio integrato `ALC887-VD` con le sue uscite HDMI. Il controllo di uscita della fase 6, che chiede di vedere la Scarlett in ingresso e in uscita, non è eseguibile finché l'interfaccia non viene collegata.

Esito: fatto.

### MS-031 - L'ambiente Wine reale, e due lacune di cui una si chiude

Perimetro: aggiornamento della fotografia e dello storico di Akabak e VACS.

Esiste *un solo prefix* Wine sulla macchina, ed è quello di default, `/home/alesop95/.wine`. Non ci sono prefix separati per programma.

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

La conseguenza operativa merita di stare in evidenza perché non è ovvia e perché ha risparmiato lavoro: *la pulizia dell'ambiente Wine non si esegue*. Pulire un sistema che verrà azzerato è lavoro che si butta, perché la riformattazione di root porta via l'installazione dei pacchetti, i due repository WineHQ, l'architettura `i386` e la sorgente `file:/cdrom/` residua. L'ambiente pulito si ottiene per costruzione dalla reinstallazione, non da una purga preventiva. Per la stessa ragione non si applicano i 134 pacchetti pendenti e non si esegue il riavvio richiesto.

Cambia anche il peso delle due voci ancora aperte di PA-005: l'esito reale di `apt update` diventa irrilevante, perché quel sistema non verrà aggiornato, mentre la verifica del Machine Identifier di Akabak resta necessaria e va fatta prima di azzerare, perché dopo non sarebbe più confrontabile.

Esito: fatto. PA-006 chiusa, ADR-013 registrata, ADR-011 superata nel suo stato di attesa.

### MS-039 - Trasferimento eseguito e verificato, e due difetti dello strumento trovati sul campo

Perimetro: esecuzione della fase 1.1 sulla macchina, correzioni a `tools/transfer-to-studio.sh`, chiusura della terza condizione di PA-001.

Il trasferimento è stato eseguito e verificato: 8 file del manifest e 6 voci del corredo per 273 file, 728 MB sotto `~/electroacoustics`, con tutte le impronte SHA-256 coincidenti fra origine e destinazione. Sulla scrivania della macchina è stato creato un collegamento simbolico all'albero, così che sia raggiungibile con un doppio clic senza duplicare i file. Lo spazio su `/home` passa da 3,7 a 4,4 GB su 369 disponibili.

Prima di questo, lo strumento ha richiesto una aggiunta e ha rivelato due difetti, tutti e tre istruttivi.

L'aggiunta è il supporto alla chiave dedicata. Lo strumento invocava `ssh` e `scp` senza indicare una identità, e su questa postazione non esiste una voce in `~/.ssh/config` per la macchina, quindi il client provava solo i nomi di chiave predefiniti, che non esistono. Aggiunta la variabile `STUDIO_KEY`, con valore predefinito la chiave dedicata e possibilità di svuotarla se in futuro si aggiungerà un alias di configurazione.

Il primo difetto è il più interessante e si è manifestato al primo tentativo, con `scp: dest open "$HOME/electroacoustics/installers/": No such file or directory`. La causa è che da OpenSSH 9 in avanti `scp` trasferisce via SFTP invece del vecchio protocollo, e SFTP non esegue una shell sul lato remoto: la variabile `$HOME` arrivava letterale, come stringa, e non veniva espansa. Il dettaglio che rende il difetto insidioso è che nello stesso script la creazione dell'albero di destinazione, fatta con `ssh` seguito da un comando, funzionava perfettamente, perché lì una shell remota c'è e la variabile si espande. Convivevano quindi due invocazioni all'apparenza simmetriche con comportamenti diversi. La correzione è usare percorsi relativi, che SFTP risolve dalla home dell'utente perché è la directory iniziale della sessione.

Il secondo difetto era nel confronto delle impronte e ha prodotto un falso negativo su `VituixCAD_setup.exe`. Lo strumento dichiarava impronte diverse mostrando due righe con la *stessa* impronta: `95a1aea4...` da un lato e `95a1aea4...` dall'altro. La differenza era il separatore. Il comando `sha256sum` di Git Bash per Windows scrive `impronta *nome`, con l'asterisco che marca la lettura in modo binario, mentre quello di Linux scrive `impronta  nome` con due spazi. Confrontare le due forme grezze segnala una differenza che non esiste. La correzione è normalizzare il separatore su entrambi i lati prima del confronto.

Vale notare che questo secondo difetto era il più pericoloso dei due, e non per la sua gravità tecnica ma per l'effetto che avrebbe avuto sull'uso: un falso negativo su una verifica di integrità insegna a non fidarsi della verifica, e una verifica di cui non si ha fiducia non viene più guardata. Un difetto che blocca è meno dannoso di uno che mente.

Aggiunta infine una modalità `--impronte`, che esegue la sola verifica saltando la copia. È nata da una necessità pratica, cioè non ricopiare 726 MB per riprovare un confronto corretto, ma resta utile in generale, perché la verifica di integrità è precisamente il tipo di controllo che si vuole poter ripetere.

Verificato con: `bash -n` sulla sintassi; l'esecuzione completa con esito positivo su tutte e quattordici le voci; la modalità di sola verifica rilanciata dopo la correzione, che riporta impronte identiche su tutte le voci; e l'ispezione dell'albero sulla macchina, con 281 file e il collegamento sulla scrivania.

Esito: fatto. La terza e ultima condizione di PA-001 è soddisfatta, quindi la cancellazione della copia sull'SSD è autorizzata. L'esecuzione resta dell'utente, perché cancellare 2,3 GB da un disco esterno è una operazione distruttiva su materiale personale e non la compie l'agente.

### MS-040 - PA-001 compiuta, e due difetti dello strumento delle azioni differite

Perimetro: `tools/check-pending-actions.py`, chiusura di PA-001 e di PA-006 nello strumento.

L'output incollato dall'utente ha rivelato due difetti, di cui uno era mio e non era stato notato.

Il primo: la chiusura di PA-006 nello strumento *non era stata applicata*. Lo script che la scriveva conteneva un `assert` sul testo da sostituire, l'assert è fallito perché gli accenti erano stati normalizzati fra la scrittura e la modifica, e lo script si è interrotto prima di scrivere il file. La modifica al documento era andata a buon fine, quella allo strumento no, e i due si contraddicevano: il documento dava PA-006 per chiusa, lo strumento la dava per aperta. Non me ne sono accorto perché ho letto l'output della parte riuscita senza controllare quella fallita. La regola che ne discende è semplice e vale oltre questo caso: quando uno script fa più modifiche e una fallisce, l'esito da guardare non è la riga di successo ma il codice di uscita.

Il secondo era un difetto di progetto più che di codice. Su PA-001 lo strumento usciva subito quando il disco non era collegato, mostrando le sole prime due condizioni. L'effetto era di nascondere le due condizioni permanenti, cioè il materiale verificato sulla macchina e la corrispondenza fra le copie, facendo sembrare la voce molto più lontana dallo sblocco di quanto fosse: chi leggeva vedeva `BLOCCATA` e due righe, non `manca solo che il disco sia collegato`. Corretto mostrando sempre tutte le condizioni e distinguendo quella transitoria dalle due permanenti.

Nel frattempo la voce si è chiusa. La cartella `Progetto stanza (software)` non esiste più su `J:`, verificato con il disco collegato, mentre le due copie restanti sono intatte: 650 file per 2,3 GB sul Desktop e 281 file per 728 MB sulla macchina con le impronte verificate. Nessun dato perduto.

Il momento e il modo della cancellazione non sono accertati, e va detto invece di ricostruirlo. Il comando dell'utente ha risposto che il percorso non esisteva mentre lo strumento riportava il disco come non collegato, e le due cose sono compatibili sia con una cartella già rimossa sia con un disco assente in quell'istante. Alle 14 dello stesso giorno la cartella c'era, perché il confronto delle impronte ne aveva letto tutti e 650 i file. Poiché l'obiettivo era che quella copia non ci fosse più e le altre due sì, la voce è compiuta a prescindere da quale spiegazione sia quella giusta.

Esito: fatto.

### MS-041 - Analisi dello spazio sull'SSD esterno, e un difetto che sbagliava di 45 GiB

Perimetro: `tools/analisi-ssd-esterno.py` nuovo, `docs/90-riferimenti/pulizia-ssd-esterno.md` nuovo.

Alla domanda su che cosa si possa cancellare da `J:` la risposta richiedeva una misura e non una stima, quindi è stato scritto uno strumento che classifica ogni voce della radice in materiale personale, cartelle di servizio e materiale trasferito, e riporta peso e numero di file senza cancellare nulla.

L'esito: circa 372 GiB di materiale personale e *1,2 GiB recuperabile*. Quasi tutto il recuperabile sta in tre voci, cioè `FOUND.002` con 429 MiB, `FOUND.000` con 412 MiB e `.Spotlight-V100` con 371 MiB; le altre sette sommate non arrivano a un megabyte, quindi cancellarle non cambia nulla.

Il difetto dello strumento merita di stare a verbale perché era del tipo peggiore. La prima versione iterava le sole cartelle della radice e ignorava i file sciolti. Su questo volume ce ne sono quattro per 45,2 GiB, di cui due archivi di backup da 25,8 e 19,4 GiB, e lo strumento riportava quindi 326 GiB di materiale personale invece di 371, sbagliando per difetto di 45 GiB senza che nulla lo segnalasse. Un totale sbagliato per difetto è peggio di un totale assente, perché non si vede che manca qualcosa: chi legge 326 non ha modo di sospettare che ne manchino 45. Corretto iterando anche i file, e con un marcatore in testa al nome invece che in coda, perché in coda veniva tagliato dal troncamento della colonna e un archivio da 26 GiB compariva indistinguibile da una cartella.

Sui due archivi di backup la conclusione è di non cancellarli, e la ragione è che la conclusione opposta non è sostenibile con i dati disponibili. La tentazione è considerare il più vecchio superato dal più recente, recuperando 25,8 GiB. Ma i nomi dichiarano perimetri diversi: il più recente esclude una cartella in più, cioè quella dei modelli 3DS, che sul volume pesa 11,4 GiB. Non sono due versioni della stessa cosa, e il più vecchio potrebbe essere l'unico a contenere qualcosa. Si aggiunge un elemento che complica e che va dichiarato invece di risolvere per ipotesi: quella cartella porta nel nome una data successiva al backup del 28 agosto, quindi non poteva esserne parte con quel nome, e non lo si stabilisce dal nome. La decisione richiede di elencare il contenuto dei due archivi, che è una lettura e non una operazione distruttiva.

Il segnale che vale più dello spazio è un altro, ed è emerso guardando la radice senza cercarlo: sul volume ci sono *cinque cartelle FOUND*, dal 30 giugno al 3 settembre, cioè cinque riparazioni del filesystem in poco più di due mesi. Le cause tipiche sono due e portano a rimedi opposti: la rimozione senza espulsione sicura, che è una abitudine da correggere, oppure un difetto del supporto, che è un hardware da sostituire. C'è un elemento di contesto che rende la prima ipotesi meno rassicurante di quanto sembri, e vale metterlo in relazione: la lettura SMART del disco interno della macchina ha riportato 24 spegnimenti non puliti su 135 accensioni. Due dischi diversi con sintomi diversi che puntano nella stessa direzione sono un indizio più forte di due sintomi isolati. Resta un indizio e non una conclusione, e il controllo che la chiude è la lettura SMART del disco esterno.

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

Estratti gli indici dei due archivi con `7z l`, per 159.217 e 94.221 righe, e confrontati per percorso. L'esito è che *nessuno dei due contiene l'altro*: 145.483 voci esistono solo nel più vecchio e 80.487 solo nel più recente.

La causa è `backup-sviluppo`, che spiega 145.478 delle prime e 80.377 delle seconde: fra il 28 agosto e il 4 settembre quella cartella è cambiata quasi per intero, quindi i due archivi sono due istantanee diverse della stessa cosa e non due versioni incrementali. Il più recente ha in aggiunta 81 voci sotto `_info_PW`, 26 sotto `DOCUMENTATION` e 2 sotto `SONGWRITING`.

Cade anche l'ipotesi che MS-041 aveva avanzato sulla differenza di peso. Si era supposto che i 6 GiB di scarto dipendessero dalla cartella dei modelli 3DS, esclusa dal più recente per dichiarazione del suo stesso nome. Quella cartella non compare fra le differenze, quindi non era nemmeno nel più vecchio, coerentemente con il fatto che porti nel nome una data successiva a quel backup. Lo scarto si spiega interamente con il rimescolamento di `backup-sviluppo`.

Conseguenza: cancellare il più vecchio costa 145.478 versioni di file che non esistono altrove in forma archiviata. La domanda "posso cancellarlo perché c'è il nuovo" ha quindi risposta negativa e documentata. Se quelle versioni servano è una decisione dell'utente e non una questione tecnica, dato che la cartella `backup-sviluppo` esiste ancora sul disco con il suo contenuto corrente.

Nota operativa: `7z` non è sul PATH di PowerShell su questa postazione, e il comando che lo invocava per nome era quindi ineseguibile. L'eseguibile sta in `C:\Program Files\7-Zip\7z.exe`, e va invocato per percorso completo oppure aggiunto al PATH. È lo stesso genere di errore di MS-027 su `ssh-copy-id`, cioè un comando fornito assumendo che sia disponibile invece di verificarlo.

Esito: fatto.

### MS-044 - La copia sul Desktop non si cancella adesso, e la ragione è il conteggio delle copie

Perimetro: PA-007 nuova, aggiornamento dello strumento delle azioni differite.

L'utente ha proposto di cancellare anche `C:\Users\Utente\Desktop\Progetto stanza (software)`, dato che tutto il necessario è sulla macchina. Il ragionamento è corretto sul contenuto e sbagliato sul momento, e vale spiegare la differenza perché è il tipo di errore che costa dati.

Oggi le voci utili del corredo esistono in due copie, una sul Desktop e una sulla macchina. Cancellare il Desktop le porta a *una copia sola*, e quella copia vive su una macchina che sta per subire una reinstallazione con riformattazione di una partizione, per ADR-013. Ridurre a una copia proprio prima di una operazione che tocca le partizioni è il momento peggiore possibile: non perché la procedura sia rischiosa, ma perché l'unico rischio irreversibile che ha, cioè l'errore umano nella selezione della partizione da formattare, è esattamente quello contro cui una seconda copia protegge.

La condizione di sblocco è quindi una sola, ed è un passo che era già in programma: la copia di sicurezza di `/home` fuori dalla macchina, cioè la fase 1.3. Fatta quella, le copie tornano due e il Desktop diventa la terza, quindi ridondante.

Va dichiarato con precisione che cosa si perderà quando si cancellerà. Delle sei voci trasferite nulla, perché sono sulla macchina con le impronte verificate. Delle otto voci scartate dal censimento si perde l'unica copia esistente, perché non sono state trasferite di proposito: la perdita è voluta e documentata, dato che il censimento stabilisce che nessuna serve e che per ciascuna esiste una sostituzione già disponibile, ma resta irreversibile e va detta.

Aggiunto al comando di cancellazione un passo che lo precede e che non è decorativo: la riverifica delle impronte sulla macchina, da lanciare subito prima e non ore prima.

Esito: fatto per la decisione. L'esecuzione è subordinata alla fase 1.3.

### MS-045 - Chiarito un equivoco: l'agente non ha cancellato nulla su J:

Perimetro: PA-008 nuova, con la verifica dello stato attuale del disco.

L'utente ha chiesto che cosa dovesse cancellare "se l'ho cancellato io". L'equivoco va chiarito perché riguarda la fiducia su un disco con materiale personale: *l'agente non ha cancellato nulla su quel volume, e non ha eseguito alcuna cancellazione in tutta la sessione.* La cartella `Progetto stanza (software)` risultava già assente quando è stata verificata, come MS-040 registra dichiarando di non sapere quando e come sia sparita.

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

Sulla stessa macchina non è possibile né sensato, e la verifica lo mostra: il sistema ha *un solo disco*, `nvme0n1` da 465,8 GB, con quattro partizioni e nient'altro, cioè EFI da 1 GB, root da 74,5 GB, swap da 14,9 GB e `/home` da 375,3 GB. Non ci sono altri dischi e non c'è alcun disco USB collegato.

Le tre varianti pensabili fallirebbero tutte, e per ragioni diverse che vale distinguere. Copiare `/home` su root è inutile, perché root è la partizione che viene formattata. Copiare `/home` su se stessa non protegge da nulla, perché il rischio contro cui il backup esiste è precisamente la formattazione per errore di quella partizione: la copia morirebbe con l'originale. Creare una partizione nuova richiederebbe di ridurre `/home`, che è una operazione rischiosa in sé, e non proteggerebbe comunque dal rischio principale, perché un errore nella selezione della partizione da formattare può colpire anche quella nuova, e un guasto del disco porta via tutto.

La regola generale che ne discende, e che vale oltre questo caso: una copia di sicurezza sullo stesso supporto della cosa che protegge non è una copia di sicurezza, è una copia.

Sulla postazione Windows invece funziona, ed è la scelta adottata. `/home` pesa 4,4 GB e il disco di destinazione ne ha 198 liberi, quindi il costo è trascurabile. E soprattutto è una *macchina fisicamente diversa*, che è l'unica proprietà che rende un backup un backup.

Il metodo richiede una precisazione che non è pedanteria. La copia si fa con `tar` in streaming attraverso `ssh` e non con `scp` dei file, perché la destinazione è un filesystem NTFS che non sa rappresentare proprietario, gruppo e permessi POSIX: copiando i file singoli quelle informazioni andrebbero perdute e il ripristino produrrebbe una `/home` con i permessi sbagliati. Dentro un archivio `tar` quei metadati sopravvivono anche su NTFS, perché sono contenuto dell'archivio e non attributi del filesystem. Si usa `--numeric-owner` per registrare gli identificativi numerici invece dei nomi, così che il ripristino non dipenda dall'esistenza dell'utente al momento in cui si ripristina.

L'archivio non viene compresso, ed è una scelta e non una dimenticanza: dei 4,4 GB la maggior parte sono installer, archivi e pacchetti già compressi, quindi la compressione costerebbe tempo di processore per un guadagno prossimo a zero.

La destinazione è fuori dalla cartella del progetto, allora in `E:\_backup-ubuntu-studio\` e oggi sul Desktop della postazione, perché un archivio di 4,4 GB non ha ragione di stare dentro un repository, nemmeno in una cartella ignorata.

Esito: si veda la voce successiva per l'esecuzione.

### MS-048 - Il corredo era già sulla macchina: il trasferimento ha prodotto una copia in più

Perimetro: constatazione sullo stato della macchina, con conseguenza su PA-007.

Ispezionando la scrivania della macchina per capire da cosa venissero 2,3 GB di `/home`, è emerso che il corredo software *era già lì*, nelle sue tre cartelle originali: `DIY Loudspeaker Pack Softwares` per 117 MB, `Room acoustics` per 563 MB e `Simulators` per 1,6 GB. Ci sono anche gli installer di Akabak e di VACS a 32 bit, sciolti sulla scrivania.

Il trasferimento di MS-039 ha quindi prodotto una seconda copia sulla macchina, sotto `~/electroacoustics`, invece della prima. Non è lavoro inutile e vale spiegare perché: la copia nuova è il sottoinsieme selezionato dal censimento, organizzato in un albero con le impronte verificate e coperto dal manifest, mentre quella sulla scrivania è il materiale grezzo con tutte e quattordici le voci, comprese le otto scartate. Sono due cose diverse con due scopi diversi. Resta il fatto che il peso su `/home` è oggi maggiore del necessario.

La conseguenza importante riguarda PA-007, cioè la cancellazione della copia sul Desktop di Windows, e *corregge in meglio* il ragionamento di MS-044. Lì avevo detto che cancellare il Desktop di Windows avrebbe portato le voci utili a una copia sola: non è vero, perché sulla macchina esistono due copie indipendenti, quella organizzata e quella grezza sulla scrivania. Il conteggio corretto è quindi di tre copie oggi e due dopo la cancellazione.

Questo non cambia la decisione ma ne cambia la ragione, e la differenza conta perché una decisione giusta per il motivo sbagliato non regge alla prima verifica. La ragione valida che resta è che entrambe le copie sulla macchina vivono sulla stessa partizione dello stesso disco, quindi non sono due copie indipendenti rispetto al rischio che il backup deve coprire: un errore sulla partizione le porta via entrambe. La condizione di sblocco resta la copia di sicurezza di `/home` fuori dalla macchina, ma ora perché è l'unica copia su un supporto diverso, non perché sia la seconda.

Emerge anche una cosa da sistemare più avanti, quando l'ambiente verrà ricostruito: sulla macchina il materiale sarà in tre posti, cioè la scrivania, `~/electroacoustics` e il collegamento simbolico. Vale consolidare, ma dopo la reinstallazione e non prima, perché toccare adesso l'unica installazione funzionante non porta nulla.

Esito: fatto per la constatazione. La correzione al ragionamento di MS-044 è riportata in PA-007.

### MS-049 - Backup di /home eseguito e verificato: fase 1.3 chiusa

Perimetro: la cartella `_backup-ubuntu-studio` fuori dal repository, aggiornamento di PA-007.

Eseguita la copia di sicurezza di `/home` con `tar` in streaming attraverso `ssh`, secondo ADR-015. L'archivio pesa 4,4 GB e non è compresso.

La verifica è la parte che conta, perché un backup non verificato non è un backup. Tre controlli. L'archivio si legge per intero senza errori. Il conteggio dei file coincide esattamente: *13.498 nell'archivio contro 13.498 sulla macchina*. E i metadati sono conservati, come mostra l'elenco esteso, che riporta permessi e proprietario numerico `1000/1000`: è la ragione per cui si è usato `tar` e non `scp`, dato che NTFS non sa rappresentarli.

Registrata anche l'impronta SHA-256 dell'archivio, così che una eventuale copia successiva sia confrontabile.

Conseguenza: PA-007 è sbloccata, cioè la copia del corredo sul Desktop di Windows può andare. E la fase 1.2 della procedura, che prevedeva un archivio separato dei soli prefix Wine, diventa ridondante: i prefix stanno sotto `/home` e questo archivio li contiene.

Esito: fatto.

### MS-050 - Akabak è a 32 bit: la scoperta che corregge tre decisioni e sei documenti

Perimetro: ADR-016, correzioni alle fasi 7 e 8 della procedura e a quattro pagine del blocco ambiente.

Ispezionando la scrivania della macchina per capire da dove venissero 2,3 GB di `/home` sono comparsi i lanciatori `.desktop` di Akabak e di VACS, e leggerli ha aperto una catena di verifiche il cui esito ribalta una parte del piano.

I fatti, tutti misurati. Il prefix in uso è `~/.wine` e il suo registro dichiara `#arch=win32`, cioè è *a 32 bit*; `syswow64` è assente, come deve essere in un prefix a 32 bit. L'eseguibile installato `AKABAK.exe` è `PE32 executable, Intel 80386`, cioè *a 32 bit*, e lo stesso vale per `VACS_32.exe`; la libreria che entrambi portano si chiama `Matrix32.dll`. Nel prefix non esiste alcun `winetricks.log`, non esiste `Microsoft.NET/Framework/v4` e non è installato alcun font Microsoft di base. I lanciatori invocano `wine-stable`, che su questa macchina esiste come comando e riporta la versione 9.0.

Ne segue che tre affermazioni del documento sorgente sono false. Akabak 3 non è a 64 bit. Non è vero che non esista una build a 32 bit, dato che quella installata lo è. E non richiede .NET Framework 4.8, né i font di base, né i runtime Visual C++, perché la configurazione che funziona non ne ha nessuno. La lista di dipendenze del sorgente descriveva *ciò che era stato tentato durante il troubleshooting, non ciò che serviva*, e questa è la lettura che riconcilia tutto: la cronologia di apt del 13 agosto 2025 mostra installazioni, purghe e reinstallazioni, cioè la traccia di una ricerca per tentativi, non di una procedura.

Chiude anche una lacuna che due documenti dichiaravano aperta, cioè quale variante di VACS fosse installata e come fosse stato risolto il fallimento iniziale. La risposta è la build a 32 bit, ed era *esattamente l'ipotesi formulata nella corrispondenza del 13 agosto 2025*, dove si chiedeva all'autore se il problema potesse dipendere dall'aver usato la versione a 64 bit invece della 32. Quell'ipotesi era corretta.

Le conseguenze sono sostanziali e vanno dichiarate una per una. La fase 7 della procedura prescriveva quattro prefix a 64 bit con `dotnet48` per tutti: sbagliata per Akabak e VACS, corretta. Il consiglio di non dichiarare l'architettura `i386`, dato in ADR-009 e ripetuto in ADR-013, è *rovesciato*: senza `i386` il solo software del progetto che oggi funziona non funzionerebbe. La mappa dei prefix passa da quattro a 64 bit a uno a 32 bit più tre a 64. E le pagine sui prefix, sulla configurazione e sui programmi sono state corrette nei punti che riportavano l'architettura e le dipendenze sbagliate.

Resta valida la parte di ADR-004 che non riguarda l'architettura, cioè un prefix per programma, con l'eccezione dichiarata di Akabak e VACS che condividono il proprio perché si usano in sequenza e perché così è la configurazione funzionante.

La lezione di metodo è la più costosa della sessione, e va scritta per intero. Tre decisioni consecutive, ADR-004, ADR-009 e ADR-013, hanno propagato una affermazione non verificata presa da un appunto, e ciascuna l'ha usata come premessa della successiva senza tornare alla fonte. Il risultato è stata una prescrizione operativa sbagliata su sei documenti, che se eseguita avrebbe prodotto un ambiente in cui il programma centrale del progetto non parte. Il controllo che l'avrebbe evitato costava un comando: `file` sull'eseguibile installato. È la stessa lezione di MS-029, dove tre cause su quattro di una diagnosi erano false: la differenza fra un appunto e una misura non è di grado.

Esito: fatto.

### MS-051 - Il release code in chiaro sulla scrivania della macchina

Perimetro: constatazione, senza modifiche.

Sulla scrivania della macchina esiste un file vuoto il cui *nome* è il release code di Akabak, e nella cartella di installazione di VACS esiste un `ReleaseCode.rtf`. Sono due copie in chiaro di un codice di attivazione, su una macchina che questo progetto documenta e che verrà sottoposta a backup.

Non è una falla e non va drammatizzata: è la macchina personale dell'utente, il codice vale solo per quell'hardware, e tenerlo a portata di mano su una scrivania è una scelta comprensibile di comodità. Vale registrarlo per due ragioni pratiche.

La prima è che il backup di `/home` eseguito in MS-049 contiene quel nome di file, quindi l'archivio di `/home` contiene il codice. Non è un problema perché resta su una macchina personale, ma va saputo, perché se quell'archivio venisse spostato su un servizio condiviso il codice ci andrebbe con lui.

La seconda è che spiega perché la scheda riservata di questo progetto vive sotto `_notes/` e non fra i file tracciati: non per proteggere un segreto che l'utente tiene su una scrivania, ma perché il repository è pubblico su GitHub e lì il codice avrebbe una diffusione di natura diversa.

Esito: fatto, come constatazione. Nessuna azione proposta.

### MS-052 - Machine Identifier confermato in interfaccia: PA-005 chiusa nella sostanza

Perimetro: chiusura della seconda delle tre voci privilegiate della fase 0, quattro documenti aggiornati.

L'utente ha aperto sulla macchina la finestra delle informazioni di AKABAK e quella del release code, e ha fornito le due immagini. Il confronto che serviva è quello fra il Machine Identifier mostrato dal programma e il valore conservato nella scheda riservata sotto `_notes/`: *coincidono*. Coincide anche il release code inserito, e il programma dichiara `Release Code valid` con l'indicatore verde. Nessuno dei due valori entra in un file tracciato, perché il repository è pubblico.

Il valore del controllo non è la spunta ma ciò che stabilisce. L'identificativo hardware che AKABAK calcola sotto Wine è lo stesso di agosto 2025, dopo un anno di uso, aggiornamenti e la sedimentazione dell'ambiente Wine che la fotografia della macchina documenta. È la prova sperimentale di ciò che la pagina sui prefix afferma per costruzione, cioè che una licenza machine-based non dipende dal prefix né dall'installazione di Wine, e quindi la conferma che l'installazione pulita non mette a rischio la licenza. Era il solo controllo che dopo la formattazione non sarebbe più stato ripetibile, e per questo era in elenco.

Le finestre hanno portato in dote tre fatti che nessun documento aveva registrato, e due di essi correggono un'aspettativa. Il programma si dichiara *Standard Edition* e non professionale, malgrado l'installer conservato si chiami `AKABAK_Pro_v324b126.exe` e malgrado l'autore avesse scritto di scaricare la versione professionale: l'installer è uno, e l'edizione la determina il release code, coerentemente con la *student license* per cui l'utente era stato registrato. Quali funzioni distinguano le due edizioni non è accertato e non va supposto dal nome del file. Il profilo di Windows dichiarato dal prefix è `NT 10.0 (Build 19043)`, cioè Windows 10, il che trasforma in fatto misurato una prescrizione che la pagina di configurazione dava per uniformità. E sotto il release code compare `Security key not connected to the USB port`, cioè esiste una chiave hardware come portatore alternativo del diritto d'uso, non in uso qui: non è un errore da correggere ma l'alternativa tecnica da valutare nel solo caso che invaliderebbe il codice, cioè un cambio significativo di hardware.

Con questa voce PA-005 resta aperta su una sola delle tre, l'esito reale di `sudo apt update`, che ADR-013 ha reso irrilevante perché su un sistema che verrà azzerato non informa nessuna decisione. La fase 0 è quindi chiusa nella sostanza: tutte le verifiche che potevano spostare una decisione sono state fatte, e nessuna l'ha spostata.

Aggiornati di conseguenza `docs/90-riferimenti/licenze-e-registrazioni.md` con la sezione sullo stato verificato, `docs/90-riferimenti/timeline-akabak-vacs.md` con la voce di cronologia del 2026-09-07 e con la riscrittura della sezione finale, che elencava come da verificare tre cose oggi tutte verificate, `docs/10-ambiente/fotografia-macchina-2026-09-07.md` nella sezione delle voci pendenti, che ne dichiarava pendenti due già chiuse, e `docs/10-ambiente/wine-configurazione.md` sul profilo di Windows.

Esito: fatto.

### MS-053 - I 2047 MByte erano già in uno screenshot: la conferma che sarebbe potuta arrivare prima

Perimetro: constatazione di metodo, nessuna decisione cambiata.

La finestra delle informazioni di AKABAK riporta la memoria come `1897 / 2047 MBytes` su una macchina che ha 16 GB di RAM installata. Non è un difetto: è la firma inconfondibile di un processo a *32 bit*, che dispone di 2 GB di spazio di indirizzamento in modo utente indipendentemente dalla memoria fisica presente. È quindi una conferma indipendente di ADR-016, ottenuta per una via completamente diversa da quella che ha prodotto quella decisione, cioè il formato dell'eseguibile e l'architettura dichiarata dal registro del prefix.

Il fatto scomodo, e va scritto perché è la parte utile, è che questa conferma era disponibile *prima* dell'indagine che ha stabilito il fatto. L'immagine appartiene alla stessa serie di screenshot da cui era stata ricostruita la corrispondenza con l'autore, ed è stata letta soltanto oggi, quando è stata fornita per un'altra ragione. Se fosse stata letta allora, ADR-004, ADR-009 e ADR-013 non avrebbero propagato per tre decisioni consecutive un'affermazione sbagliata presa da un appunto, e sei documenti non avrebbero portato una prescrizione che, eseguita, avrebbe prodotto un ambiente in cui il programma centrale del progetto non parte.

La lezione non è leggere tutti gli screenshot, che è irrealizzabile e non è un metodo. È più precisa: quando una premessa regge una decisione, il materiale già in mano va interrogato *su quella premessa* invece di essere letto per il tema per cui era stato raccolto. Gli screenshot erano stati letti per ricostruire lo scambio di posta elettronica, e la domanda sull'architettura non era stata posta a un materiale che conteneva la risposta. È la stessa lezione di MS-029 e MS-050, vista dal lato dell'archivio invece che da quello della misura.

Esito: fatto, come constatazione.

### MS-054 - L'archivio di /home spostato, e un controllo che inchiodava un percorso

Perimetro: `tools/check-pending-actions.py`, ADR-015, quattro documenti, sblocco dichiarato di PA-007.

L'utente ha spostato l'archivio di backup da `E:\_backup-ubuntu-studio\` a `C:\Users\Utente\Desktop\_backup-ubuntu-studio\`. La dimensione è identica al byte, 4.662.927.360, quindi la verifica di MS-049 vale ancora per quel file: è stato spostato e non rigenerato.

Lo spostamento ha però rotto un controllo, e il modo in cui l'ha rotto è più interessante dello spostamento. Lo strumento delle azioni differite verificava la condizione di sblocco di PA-007 cercando l'archivio a un percorso fisso, quindi dallo spostamento in avanti dichiarava mancante un backup che esiste, e con esso riportava PA-007 a bloccata per un motivo falso. È il difetto peggiore che uno strumento di verifica possa avere: non sbagliare l'esito in senso permissivo, che si nota subito perché qualcosa va storto, ma in senso restrittivo, che si crede e blocca un lavoro legittimo.

Corretto rendendo il nome del file l'invariante e la cartella una fra più posizioni plausibili, con una funzione che restituisce la prima in cui l'archivio risulta presente. Aggiunto anche un confronto della dimensione con quella registrata, che segnala un'anomalia se l'archivio è stato rigenerato o è incompleto, perché in quel caso la verifica di MS-049 non varrebbe più e va rifatta prima di cancellare qualcosa. Il controllo eseguito dopo la correzione trova l'archivio sul Desktop, dimensione coincidente, e dichiara PA-007 sbloccata. ADR-015 aggiornata per dire che la destinazione fa parte della decisione solo per la proprietà che conta, cioè essere una macchina diversa da quella protetta, e non per la lettera di unità.

Resta da dire la cosa che l'utente ha chiesto due volte, e che era rimasta implicita fra un aggiornamento di stato e l'altro: *la copia del corredo sul Desktop si può cancellare adesso.* La condizione era una sola, il backup di `/home` fuori dalla macchina, ed è soddisfatta e verificata. L'unica perdita è quella voluta, cioè le otto voci che il censimento ha scartato con una sostituzione nativa o gratuita già disponibile per ciascuna; le sei voci utili restano sulla macchina con le impronte verificate e nell'archivio. La voce PA-007 è stata riscritta perché lo dicesse in apertura invece di farlo dedurre, e il testo con cui era stata aperta è conservato ma marcato come superato.

Esito: fatto per la parte documentale e strumentale; la cancellazione è dell'utente.

### MS-055 - La copia del template nel progetto gemello è rimasta indietro

Perimetro: `docs/PENDING-ACTIONS.md` del progetto gemello, nuova voce PA-002.

La verifica `md-unwrap --check` eseguita sul progetto gemello dopo la propagazione segnala cinque file non conformi alla convenzione della riga sorgente unica, per quattordici righe da unire: `CLAUDE.local.md` e quattro modelli sotto `.claude/templates/_notes/`. La stessa verifica su questo progetto non segnala nulla.

La spiegazione non è che gli strumenti si comportino diversamente. Il confronto dei file mostra che sono *diversi*: la copia del template nel gemello è anteriore alla propagazione della convenzione Markdown fatta qui, quindi non è un difetto nuovo ma un ritardo di allineamento. Vale registrarlo perché l'ipotesi immediata sarebbe stata un marcatore di esclusione presente qui e assente là, e quella ipotesi è falsa: nessuno dei due progetti ha marcatori su quei file.

Non corretto di proposito. Sono modelli in un altro repository, fuori dal blocco che lo strumento di propagazione dichiara di gestire, cioè `docs/10-ambiente/`, e correggerli qui significherebbe allargare in silenzio il perimetro di una sincronizzazione unidirezionale dichiarata. Aperto invece come PA-002 nel gemello, con l'osservazione che conviene trattarla insieme a PA-003 di questo progetto, perché la sorgente comune è `template-claude-developing` e correggere lì risolve entrambe le copie invece di rincorrerle.

Esito: fatto come registrazione; la correzione è una decisione dell'utente.

### MS-056 - Due danni tipografici autoinflitti in dieci minuti, e come sono stati trovati

Perimetro: `docs/OPERATIONS-LOG.md`, riparazione di danni introdotti in questa stessa sessione.

Va scritto perché è il tipo di episodio che si tende a non registrare, essendo un errore proprio e rimediato subito, ed è invece quello da cui si impara di più. Due danni consecutivi, il secondo prodotto dalla riparazione del primo.

Il primo. Scritta la voce MS-055 con le forme non accentate del tipo `e'` e `perche'`, ho lanciato `fix-missing-accents.py` sul file per normalizzarle, e lo strumento ha prodotto esattamente il difetto che MS-014 documenta in questo stesso registro: `perche'` è diventato `perché'` e `cioe'` è diventato `cioè'`, cioè accento corretto più apostrofo orfano. Non è un difetto nuovo dello strumento, è quello già diagnosticato, e la lezione è che averlo documentato non basta a non incapparci: MS-014 aveva escluso la catena tipografica dalla sequenza di verifica su `.` proprio per questo, e io l'ho invocata a mano su un singolo file aggirando la propria mitigazione.

Il secondo, ed è il più istruttivo. Per rimuovere gli apostrofi orfani ho applicato una sostituzione con espressione regolare su tutto il file, nella forma vocale accentata seguita da apostrofo. Ha funzionato, e ha anche cancellato gli apostrofi delle *citazioni deliberate* di MS-014, dove le stringhe `c'è'` e `com'è'` non sono errori del testo ma gli esempi del difetto che quella voce spiega. Il risultato era un paragrafo che dichiarava che il difetto produce `c'è` e `perché`, cioè le forme corrette, rendendo incomprensibile l'intera spiegazione.

La regola che ne discende, e che vale oltre la tipografia. Una sostituzione automatica su un file di documentazione tecnica non distingue il testo dagli esempi, e in un documento che parla di errori gli esempi *sono* errori: applicare una correzione globale a un file che contiene citazioni di forme sbagliate ne distrugge il contenuto. La sostituzione va quindi limitata alla porzione appena scritta, non estesa al file, oppure va verificata leggendo il diff riga per riga.

Ed è così che il danno è stato trovato, che è la parte da conservare. Non da un controllo tipografico, che dopo la riparazione risultava pulito su entrambe le versioni, quella giusta e quella rovinata, perché `c'è` è una forma perfettamente corretta. È stato trovato leggendo il `git diff` di ciò che avevo modificato e chiedendosi perché comparissero righe rimosse in un microstep che non stavo toccando. Il controllo automatico non poteva vederlo: il difetto era semantico, non ortografico. La verifica che ha funzionato è quella che si fa sempre e comunque, cioè guardare l'elenco completo delle righe cambiate e giustificarne ciascuna, e in questo caso l'esito finale è zero rimozioni non attese.

Un terzo difetto minore, trovato nello stesso passaggio e con lo stesso metodo: scrivendo MS-055 avevo introdotto una sequenza `l` più `i` senza punto più accento grave combinante, al posto di una semplice `lì`. Un controllo dei punti di codice fuori dal latino ha isolato il carattere combinante U+0300 e la riparazione è stata immediata. Il progetto era stato ripulito dai caratteri di controllo in una sessione precedente, quindi il controllo esiste già come abitudine ed è ciò che lo ha intercettato prima del commit.

Esito: fatto, con i tre difetti riparati e verificati.

### MS-057 - Una sequenza operativa, perché il registro per voce risponde alla domanda sbagliata

Perimetro: `docs/PENDING-ACTIONS.md`, nuova sezione in testa al registro.

Alla domanda su quali microstep tocchino all'utente non esisteva un documento che rispondesse. Il registro delle azioni differite dice per ciascuna voce se è eseguibile e da che cosa dipende, la procedura di installazione dice quali fasi restano, ma nessuno dei due dice in che ordine affrontare le due cose insieme, nè quali voci appartengono al registro e quali alla procedura. La risposta esisteva soltanto come ricostruzione fatta a mano leggendo tre documenti, che è esattamente ciò che questo progetto tiene fuori dalla conversazione.

Aggiunta quindi una sequenza numerata di otto passi in testa al registro, con tre proprietà dichiarate per ciascuno: che cosa è, dove sta il dettaglio, e se dipende dal precedente o è indipendente e quindi saltabile. Le tre voci a bassa priorità che non appartengono alla sequenza sono elencate a parte come tali, invece di essere lasciate a galleggiare in un elenco dove sembrerebbero un passo mancato.

Il criterio con cui la sequenza è ordinata vale registrarlo perché non è l'ordine dei numeri delle voci. Prima ciò che una sessione perduta porterebbe via, cioè il commit. Poi le azioni indipendenti e reversibili nei loro effetti utili, cioè recuperare spazio e misurare un disco. Poi la preparazione, che è l'unico posto dove un errore silenzioso, una immagine corrotta, si paga settimane dopo. Poi il passo irreversibile. Poi la ricostruzione e l'igiene.

Esito: fatto.

### MS-058 - SMART dell'SSD esterno: il supporto è sano, la causa è la rimozione

Perimetro: chiusura di PA-009, nuova sezione in `docs/90-riferimenti/pulizia-ssd-esterno.md`, correzione della coda superata della stessa pagina.

L'ostacolo, prima dell'esito, perché è la parte trasferibile. La lettura SMART richiede privilegi anche su Windows, cosa che si tende ad associare al solo Linux. La via nativa, `Get-StorageReliabilityCounter` da PowerShell, risponde `PermissionDenied` sulla classe CIM di storage se la sessione non è elevata, ed è la stessa ragione per cui su Linux serve `sudo` su `/dev/nvme0`: leggere quella tabella significa mandare un comando diretto al dispositivo e non leggere un file. La via che non richiede una sessione interattiva elevata è avviare CrystalDiskInfo con elevazione e l'opzione `/CopyExit`, che scrive il rapporto completo di tutti i dischi in `DiskInfo.txt` nella cartella del programma e chiude subito: nessuna finestra da leggere, nessuno screenshot da catturare, un file di testo che si analizza come qualsiasi altro. È l'alternativa migliore alla regola sugli screenshot ogni volta che lo strumento grafico sa scrivere un rapporto.

L'esito sul Samsung Portable SSD T7 da 500 GB, firmware `FXG42P2Q`, esposto come NVMe 1.3 attraverso un ponte UASP: usura *zero* per cento, riserva disponibile 100 su soglia 10, errori di integrità supporto e dati *zero*, voci nel registro errori *zero*, temperatura 32 gradi, giudizio 100 per cento, 2795 ore di accensione, 742 cicli di alimentazione, 7526 GB letti e 1863 scritti.

Il supporto è quindi sano e delle due cause che PA-009 metteva in alternativa cade la seconda: non c'è difetto del medium né del controllore, e la sostituzione del disco non serve. Resta la prima, la rimozione senza espulsione sicura, coerente con i *122 spegnimenti non protetti*, cioè uno ogni sei cicli.

Su quel numero va però applicato un correttivo, e va scritto perché senza di esso si conclude più di quanto il dato dica. Su un disco USB il contatore degli spegnimenti non protetti si incrementa ogni volta che l'alimentazione cade senza che il ponte inoltri al controller NVMe la notifica di spegnimento, e molti ponti non la inoltrano mai, nemmeno quando il sistema espelle il volume correttamente. Una parte dei 122 è quindi fisiologica dell'involucro esterno e non prova di uno strappo. Ciò che non ha spiegazioni fisiologiche sono le cinque cartelle `FOUND`, perché `chkdsk` non ripara un filesystem coerente: quelle restano la prova che il volume è stato staccato con scritture in sospeso.

Per dare una scala al numero, dallo stesso rapporto, il disco di sistema di questa postazione, un Crucial P3 da 1 TB con firmware `P9CR413`: 23 spegnimenti non protetti su 253 cicli, usura al 13 per cento, salute all'87 per cento, zero errori di integrità dopo 11881 ore. Su un disco interno, dove il contatore non passa da un ponte USB, il rapporto fra spegnimenti non protetti e cicli è circa la metà.

L'ipotesi aperta in MS-042, cioè due dischi con sintomi diversi che puntavano verso una gestione poco pulita dell'alimentazione e delle rimozioni, si risolve così: era corretta come direzione e va precisata nel merito. Non è una gestione dell'alimentazione difettosa su due supporti, è una abitudine di rimozione su uno e un contatore che su USB conta anche gli spegnimenti regolari. La regola operativa che ne discende è una sola, e non è la sostituzione del disco: espellere il volume prima di staccarlo, sempre.

Corretta nella stessa pagina una coda superata. Diceva che la decisione sulla copia del corredo sul Desktop andava presa dopo la reinstallazione compiuta e verificata; la condizione reale che scioglie il nodo non è quella ma una copia di sicurezza su un supporto diverso, che esiste dal 2026-09-07. Si veda PA-007 e ADR-015.

Esito: fatto, PA-009 chiusa.

### MS-059 - Fase 2: la fonte dice 26.04.1, non 26.04, e la firma si verifica davvero

Perimetro: riscrittura delle sottofasi 2.1 e 2.2 e correzione del nome nel comando della 2.3 in `docs/10-ambiente/installazione-pulita-26-04.md`, propagata al progetto gemello.

La procedura prescriveva di non dedurre il nome dell'immagine dal calendario dei rilasci ma di prenderlo dalla fonte, e la prescrizione si è ripagata al primo uso. Nella cartella del rilascio ufficiale convivono *due* immagini, `ubuntustudio-26.04-desktop-amd64.iso` da 6,7 GB e `ubuntustudio-26.04.1-desktop-amd64.iso` da 6,6 GB, cioè il primo point release. Da prendere è la seconda, perché incorpora le correzioni accumulate dopo il rilascio, fra cui quelle dell'installatore e del kernel, ed è anche la versione che `do-release-upgrade` offriva sulla macchina secondo la fase 0. La procedura nominava la prima in due punti, cioè nel testo della 2.1 e nel comando `dd` della 2.3, ed è stata corretta in entrambi: il secondo era il più insidioso, perché un nome sbagliato dentro un comando da copiare non produce un errore di comprensione ma un comando che non trova il file.

Scaricati il file delle somme e la sua firma, 208 e 833 byte, e registrata nella procedura la somma attesa del point release, `2b25d06203c8a2f60da23e20e3afd1fa400f8ff8104fd074c1b7e49fc3768084`, perché un valore verificato vale più di una istruzione da seguire.

La sottofase 2.2 chiedeva una sola verifica, la somma di controllo, e ne chiede ora *due*, perché rispondono a domande diverse e la prima da sola ha un limite che va enunciato: una somma confrontata con un file scaricato dallo stesso posto dell'immagine non protegge da chi controlli quel posto. La seconda verifica è la firma del file delle somme, ed è stata eseguita per davvero invece di essere prescritta.

L'esecuzione ha prodotto tre esiti utili in sequenza. Al primo tentativo `gpg` risponde `Can't check signature: No public key`, che non è un fallimento della verifica ma la sua impossibilità, e nello stesso messaggio dichiara l'identificativo della chiave usata per firmare: `843938DF228D22F7B3742BC0D94AA3F0EFE21092`. Vale notare il metodo, perché è quello che questo progetto impone e che qui si è potuto seguire alla lettera: l'impronta della chiave da importare è stata letta dalla firma stessa e non ricordata, quindi il comando di importazione scritto nella procedura non contiene un valore assunto. Importata la chiave dal server di chiavi, la verifica dà `Good signature from "Ubuntu CD Image Automatic Signing Key (2012) <cdimage@ubuntu.com>"`.

Il terzo esito è l'avviso che segue la firma buona, ed è la ragione per cui l'output è stato riportato per intero nella procedura: `WARNING: This key is not certified with a trusted signature`. Si prende per un fallimento e non lo è. Le due domande sono separate, l'autenticità della firma e la fiducia nella chiave, e `gpg` risponde alla prima con un sì e alla seconda con un non lo so, perché nell'anello di chiavi locale quella chiave non è firmata da nessuno di cui si sia dichiarata la fiducia. L'avviso sparisce solo dichiarando manualmente quella fiducia, che è una scelta di chi usa lo strumento e non un requisito della verifica.

Aggiunta infine la precisazione su che cosa la verifica della firma dimostra e che cosa no, perché è facile attribuirle un valore che non ha. Dimostra che il file delle somme è stato firmato da quella chiave; non dimostra che quella chiave sia di Canonical, se la si è appena presa da un server di chiavi senza confronto indipendente. La fiducia si ancora al fatto che l'impronta è pubblicata dalla distribuzione e che la stessa chiave firma i rilasci da anni. Resta una difesa concreta, perché costringe un attacco a compromettere anche la chiave e non soltanto il sito.

Registrato anche un dettaglio che altrimenti fa sospettare un file diverso: il file delle somme di Ubuntu scrive il nome nella forma `hash *nome`, con l'asterisco della modalità binaria, e la stessa forma la produce `sha256sum` nella shell POSIX che accompagna git su Windows, mentre su Linux la forma abituale è con due spazi. È la stessa trappola di MS-039, dove un confronto fra impronte identiche risultava negativo per il solo separatore.

L'immagine è in scaricamento in `C:\Users\Utente\Desktop\_iso-ubuntu-studio\`, fuori dal repository, con `curl -C -` per poterlo riprendere invece di ricominciare. La verifica della sua integrità è un microstep a parte, perché è un esito che non esiste finché il file non è completo.

Esito: fatto per la fase 2.1 e 2.2 e per la correzione della 2.3; la scrittura della chiavetta resta da fare.

### MS-060 - L'immagine 26.04.1 scaricata e verificata integra

Perimetro: `C:\Users\Utente\Desktop\_iso-ubuntu-studio\` fuori dal repository, chiusura della sottofase 2.2.

Scaricata `ubuntustudio-26.04.1-desktop-amd64.iso`, 7.127.195.648 byte, con `curl -L -C - --retry 5` così che una interruzione di rete si riprendesse invece di richiedere di ricominciare. La destinazione è fuori dalla cartella del progetto, per la stessa ragione dell'archivio di backup: un file da 6,6 GB non ha motivo di stare dentro un repository, nemmeno in una cartella ignorata.

Verifica dell'integrità eseguita con `sha256sum -c SHA256SUMS`, contro il file delle somme la cui firma era già stata verificata in MS-059. Esito: `ubuntustudio-26.04.1-desktop-amd64.iso: OK`. L'ordine delle due verifiche non è indifferente e vale enunciarlo: si verifica prima la firma del file delle somme e poi la somma dell'immagine, perché confrontare un'immagine con un elenco di somme non autenticato dimostra soltanto che il download non si è corrotto, non che l'immagine sia quella pubblicata.

Nello stesso output compare una riga `FAILED open or read` relativa a `ubuntustudio-26.04-desktop-amd64.iso`, cioè l'immagine iniziale del rilascio che non è stata scaricata. Non è un errore ed era previsto nella procedura: il file delle somme elenca tutte le immagini del rilascio, e `sha256sum -c` segnala come mancante ogni voce dell'elenco che non trova su disco. Va detto perché in un output di due righe una delle due dice `FAILED`, e la lettura affrettata conclude il contrario di quello che è successo.

Stato della fase 2 dopo questo passo: 2.1 e 2.2 chiuse, resta la 2.3, cioè la scrittura della chiavetta. Sulla postazione Windows non è presente alcuno strumento di scrittura, dato che Rufus non risulta installato, e nessun supporto rimovibile diverso dall'SSD esterno risulta collegato: entrambe le condizioni vanno soddisfatte prima di procedere, e la scelta dello strumento è registrata separatamente perché ha due strade con costi diversi.

Esito: fatto.

### MS-061 - Rufus verificato per firma, e la fase 2.3 riscritta con la ragione di ogni scelta

Perimetro: `C:\Users\Utente\Desktop\_iso-ubuntu-studio\rufus-4.15p.exe`, riscrittura della sottofase 2.3 e allineamento dell'intestazione e della premessa della procedura.

Scelta la strada della scrittura da Windows con Rufus, fra le due possibili, e va registrato che l'altra esisteva: scrivere la chiavetta dalla macchina Ubuntu con `dd`, previo trasferimento dell'immagine via rete, non richiedeva alcuno strumento nuovo e produceva la chiavetta già dove serve. La scelta è dell'utente e la ragione è la disponibilità del supporto sulla postazione.

Su questa postazione Rufus non risultava installato e nessun supporto rimovibile diverso dall'SSD esterno risultava collegato. Individuata la versione corrente dalla pagina dei rilasci del progetto invece di assumerla, cioè la 4.15, e scaricata la variante portabile `rufus-4.15p.exe`, che non scrive nel registro e non lascia nulla sul sistema.

La verifica di questo file segue una strada diversa da quella dell'immagine, e la differenza è il contenuto tecnico di questo microstep. Per l'immagine la verifica corretta è la somma di controllo la cui firma è stata verificata a parte, perché l'immagine è un dato e la fiducia si ancora alla chiave della distribuzione. Per un eseguibile Windows la verifica più forte disponibile è invece la firma Authenticode, perché il sistema operativo la controlla contro le proprie radici di certificazione fidate: non contro un valore pubblicato sullo stesso sito da cui si è scaricato il file, che è il limite già enunciato in MS-059. Le note del rilascio, del resto, non pubblicano alcuna somma di controllo, quindi la firma non è soltanto la via migliore ma l'unica.

```powershell
Get-AuthenticodeSignature "C:\Users\Utente\Desktop\_iso-ubuntu-studio\rufus-4.15p.exe" | Format-List Status, SignerCertificate
```

Esito: `Status` vale `Valid`, il firmatario è `CN=Akeo Consulting, O=Akeo Consulting, S=Donegal, C=IE`, cioè l'autore di Rufus, con emittente `Sectigo Public Code Signing CA EV R36` e validità fino ad agosto 2027. Registrata anche l'impronta SHA-256 del file scaricato, `84c8a437f8af89257524478489e5c85f1edf25f761d299e2bcde46ac0afbe106`, non come verifica ma come riferimento, così che una copia futura sia confrontabile con questa.

Riscritta la sottofase 2.3, che prima diceva soltanto di usare Rufus in modalità di scrittura diretta. Aggiunte quattro cose che il testo precedente non conteneva e che decidono la riuscita.

Il vincolo di capacità, con la sua ragione numerica invece di un margine di prudenza: 16 GB, perché l'immagine pesa 6,64 GiB e una chiavetta da 8 GB offre circa 7,45 GiB utili, cioè un margine che si esaurisce appena lo strumento debba costruire un filesystem con spazio di servizio.

La modalità di scrittura, che era nominata ma non motivata, e la motivazione è la parte che serve. In modalità immagine ISO lo strumento costruisce sulla chiavetta un filesystem FAT32, scelto per compatibilità di avvio, che non può contenere un singolo file più grande di 4 GB; dentro una immagine live di questa dimensione il filesystem compresso del sistema supera quella soglia. In modalità DD l'immagine è copiata byte per byte, senza costruire nulla, quindi il limite non si presenta e la chiavetta risulta identica al file di cui si è verificata l'impronta. Ne segue anche una proprietà utile: una chiavetta scritta in DD è verificabile a posteriori, una scritta in modalità ISO no.

> *Ritirato il 2026-09-08.* La frase sul filesystem compresso che supera i 4 GB è *falsa* e non va usata: la misura dice 3,83 GiB, sotto il limite. La conclusione, cioè scegliere DD, resta valida per la sola proprietà di verificabilità nominata in fondo al paragrafo. Il paragrafo si conserva come era perché il registro documenta anche gli errori, e la correzione con la misura è in MS-067.

Lo schema GPT con destinazione UEFI senza compatibilità CSM, coerente con la fase 3 e con il fatto che l'installazione esistente è UEFI e la sua partizione EFI va riusata.

E l'avvertenza sul dopo, che è il punto esatto in cui si rovina una chiavetta appena fatta: terminata la scrittura in DD, Windows vede lo spazio non allocato oltre le partizioni dell'immagine e propone di formattarlo o di inizializzare il disco. Va rifiutato, perché quella operazione riscrive la tabella delle partizioni e rende il supporto non avviabile. L'insidia sta nel fatto che l'avviso ha l'aspetto di una richiesta di manutenzione ordinaria.

Allineate infine due dichiarazioni di stato della procedura che erano superate e che, lasciate così, avrebbero fatto ripetere lavoro compiuto o rimettere in discussione una decisione presa. L'intestazione dichiarava non eseguite tutte le fasi dalla 1 in avanti, mentre la 1 è compiuta e della 2 restano solo le chiavette; ora dichiara anche, in apertura, che questa procedura è già stata corretta quattro volte dall'esito reale delle sue prime fasi, con l'elenco delle quattro. La premessa chiedeva all'utente di riconfermare la scelta fra installazione e aggiornamento, cosa avvenuta il 2026-09-07 con ADR-013.

Esito: fatto per la preparazione e per la documentazione; la scrittura della chiavetta resta un'azione dell'utente, che richiede il supporto fisico.

### MS-062 - Due difetti in una sostituzione fatta a mano, e lo strumento che esisteva già

Perimetro: `.claude/memory/progress.md` e `docs/OPERATIONS-LOG.md`, riparazione di danni introdotti in questa sessione.

Secondo episodio della stessa famiglia di MS-056, e va scritto per intero perché la causa è diversa e più insidiosa, e perché la conclusione è che lo strumento corretto era già nel progetto.

Il primo difetto è di ordinamento della lista di sostituzioni. Normalizzando a mano le forme con l'apostrofo al posto dell'accento avevo scritto una lista che comincia con la coppia da `e'` a `è` e prosegue con quella da `perche'` a `perché`. La prima coppia consuma la seconda, perché `e'` è un sottoinsieme di `perche'`: il risultato è *`perchè`*, cioè accento grave dove l'italiano vuole l'acuto. La regola generale che ne discende vale oltre la tipografia: in una lista di sostituzioni un pattern più corto che sia sottostringa di uno più lungo va messo per ultimo, altrimenti il più lungo non viene mai raggiunto. Lo stesso difetto aveva già colpito MS-055 e MS-057 nel registro, con due occorrenze, ed è passato inosservato perché `perchè` è una grafia scorretta ma plausibile, non un carattere di controllo: nessun controllo automatico di questo progetto la segnala, e a video sembra una parola.

Il secondo difetto è di aritmetica sugli indici, e ha prodotto testo duplicato. Per applicare le sostituzioni al solo blocco nuovo avevo estratto una fetta con `b = t[i:i+len(v)+200]`, trasformato `b`, e ricomposto con `t[:i] + b + t[i+len(b):]`. Le sostituzioni *accorciano* la fetta, perché `gia'` diventa `già` perdendo un carattere, quindi `len(b)` dopo la trasformazione è minore della lunghezza della fetta originale e la ricomposizione reinserisce la sovrapposizione. L'esito visibile è stato un paragrafo di una voce precedente che cominciava con `fornite dall'utente: te dall'utente: coincide`. La regola: quando si ricompone una stringa attorno a una fetta trasformata, l'indice di ripresa deve essere quello *originale* della fine della fetta, non uno ricalcolato dalla lunghezza del risultato.

La riparazione non è stata un'altra sostituzione a mano, ed è questo il punto utile. Rimossa la duplicazione e corrette le due occorrenze di `perchè`, la normalizzazione degli accenti del file è stata affidata a `tools/fix-accents.py`, cioè allo strumento che il progetto ha per questo scopo. Ha fatto due cose che la lista scritta a mano non faceva: ha applicato le sostituzioni nell'ordine corretto, convertendo `uniformita'`, `pero'`, `cio'`, `puo'` e `meta'` senza collisioni, e ha lasciato intatto l'unico `c'e'` presente nel file, perché sta dentro un frammento di codice fra apici inversi ed è una citazione deliberata. È esattamente la protezione che a MS-056 era mancata quando la sostituzione globale aveva cancellato gli apostrofi dagli esempi.

Ne segue la lezione, che è la stessa vista da un'altra faccia. A MS-056 il danno veniva dall'aver invocato lo strumento fuori dalla sua mitigazione; qui viene dall'averlo sostituito con codice scritto sul momento. Il denominatore comune è la fretta su un lavoro che sembra troppo semplice per meritare uno strumento, e la conseguenza è che il file di memoria del progetto ha portato per qualche minuto una frase priva di senso. Il presidio che ha funzionato, di nuovo, è la lettura del `git diff` riga per riga: nessuno dei due difetti era rilevabile dai controlli automatici, perché `md-unwrap` non guarda l'ortografia e il controllo dei caratteri anomali non trova nulla in una parola sbagliata scritta con caratteri validi.

Come effetto collaterale utile, il file di memoria è ora integralmente conforme alla convenzione tipografica: le voci delle sessioni precedenti erano state scritte con le forme ad apostrofo e non erano mai state normalizzate, quindi il debito è chiuso invece di essere aumentato con un paragrafo misto.

Esito: fatto, con i due difetti riparati e verificati.

### MS-063 - PA-007 eseguita, immagine spostata e riverificata, e la trappola delle fini riga

Perimetro: chiusura di PA-007, aggiornamento del percorso dell'immagine in quattro documenti, allineamento dello snapshot di sincronizzazione.

Tre cose, di peso diverso.

La prima è l'esecuzione di PA-007, cioè la cancellazione della copia del corredo sul Desktop della postazione. L'utente l'ha eseguita nell'ordine prescritto, con la riverifica delle impronte immediatamente prima: 8 file del manifest e 273 file del corredo tutti coincidenti sulla macchina, poi la cancellazione di 650 file per 2,3 GB, verificata come compiuta. Le voci utili restano in due copie indipendenti, quella sulla macchina e quella dentro l'archivio di `/home`. Delle otto voci scartate dal censimento si è perduta l'unica copia, come previsto e voluto. La voce è chiusa e resta nel registro con il suo esito.

La seconda è lo spostamento dell'immagine di installazione e di Rufus dal disco `E:` al Desktop della postazione, per scelta dell'utente, che li vuole lì finché servono. Il punto tecnico è che questo spostamento attraversa due volumi, quindi non è un rinomino ma una copia seguita da una cancellazione: i byte sono stati riscritti, e una copia può fallire. Entrambe le verifiche sono state quindi rifatte alla nuova posizione invece di essere ereditate, ed entrambe passano: l'immagine dà `OK` contro il file delle somme firmato, e Rufus dà `Status: Valid` con firmatario `Akeo Consulting`. Aggiornato il percorso nei quattro documenti che lo citavano, fra cui il comando di verifica della firma nella sottofase 2.3, dove un percorso vecchio non sarebbe stato un dubbio ma un comando che non trova il file. È la seconda volta in due giorni che un file di lavoro cambia posto, dopo l'archivio di backup in MS-054, e la regola che ne discende per gli strumenti resta quella: la condizione da verificare è l'esistenza per nome, non la presenza a un percorso fisso.

La terza è una trappola dell'ambiente, e va scritta perché ha fatto fallire due modifiche in modo incomprensibile prima di essere capita. Uno script eseguito passandogli il sorgente sull'ingresso standard non riesce a trovare un ancoraggio di testo su più righe se il file di destinazione usa `CRLF` e l'ancoraggio è scritto con `LF`. Il file `.claude/memory/index.md` è `CRLF`, e la ricerca di un blocco di tre righe scritto con interruzioni `LF` non trova nulla: l'errore che si osserva è una asserzione fallita, senza alcun indizio sulla causa, e la tentazione è cercare l'errore nel testo cercato.

La causa profonda è una proprietà voluta di questo progetto e non un difetto: la convenzione Markdown prescrive di conservare la fine riga di ciascun file, `CRLF` o `LF`, e lo strumento `md-unwrap` la rispetta. Ne segue che l'albero contiene file con entrambe le convenzioni, e che qualunque manipolazione testuale scritta a mano deve tenerne conto. Le tre regole operative che ne discendono: preferire ancoraggi di una sola riga, che il problema non hanno; leggere il file con la conservazione delle fini riga e confrontare byte a byte quando l'ancoraggio deve essere multi-riga; oppure usare uno strumento che normalizza il confronto per conto suo, che è la strada giusta e la più economica.

Va aggiunta una nota su una ipotesi sbagliata formulata durante la diagnosi, perché è istruttiva quanto la causa. Avevo supposto che il colpevole fosse la codifica, dato che su questa macchina l'ingresso standard di Python dichiara `cp1252`, e che i caratteri accentati del sorgente arrivassero corrotti. La verifica ha smentito: il sorgente viene decodificato come UTF-8 a prescindere dalla codifica dell'ingresso, e la stringa accentata risultava corretta byte per byte. Ciò che sembrava corruzione era solo la stampa illeggibile sulla console, che è `cp1252` e non sa rappresentare quei caratteri. Due fenomeni distinti, la rappresentazione a schermo e il contenuto in memoria, che a occhio danno lo stesso sintomo: la differenza si vede solo guardando i byte, ed è la ragione per cui la verifica è stata fatta sui byte e non sul `repr`.

La stessa trappola aveva già prodotto un danno silenzioso più grande, scoperto proprio cercandola. Tutti i blocchi inseriti in questa sessione in questo registro e nella pagina sull'SSD esterno erano stati scritti con interruzioni `LF` e inseriti in file `CRLF`, producendo *fini riga miste*: 134 righe `LF` in mezzo a 913 `CRLF` nel registro, 35 in mezzo a 90 nell'altra pagina. Nessuno dei controlli del progetto lo segnalava, perché `md-unwrap` per contratto conserva la fine riga di ciascun file e non ne pretende la coerenza interna, e il rendering a video è identico.

Che finisse nella storia del repository era però certo, e questo è il dato che ha reso la cosa urgente: `core.autocrlf` è `false`, non esiste alcun `.gitattributes`, e il blob del commit precedente contiene già i ritorni carrello, quindi git registra le fini riga così come stanno sul disco senza normalizzarle. Un file misto committato produce differenze rumorose su ogni modifica successiva, perché qualunque strumento che riscriva il file uniforma le interruzioni e trasforma una modifica di due righe in una modifica dell'intero file. Normalizzati entrambi i file alla loro fine riga originale, cioè `CRLF`, con verifica che nell'albero non resti alcun file misto oltre alle due fixture di prova di `md-unwrap`, che sono misti di proposito perché servono a provare che lo strumento li conserva.

Aggiunto quindi uno strumento nuovo, `tools/check-eol.py`, ed è entrato nella sequenza di verifica prima di un commit dichiarata in `CLAUDE.md`. È di sola lettura e non converte niente, perché la decisione su quale fine riga tenere spetta a chi conosce il file; segnala il formato prevalente come suggerimento. Esclude le fixture di `md-unwrap`, che sono miste di proposito.

Al primo lancio si è ripagato, trovando un file misto che non era stato introdotto adesso ma era *già nella storia del repository*: `.claude/settings.json`, con una riga `CRLF` in mezzo a trentasei `LF`. Il difetto era una riga vuota finale terminata con ritorno carrello, cioè la sequenza `}` newline ritorno-carrello newline in coda al file. Corretto togliendo la sola interruzione superflua, con due cautele dichiarate: il contenuto JSON è stato confrontato prima e dopo e risulta identico, e il BOM presente in testa al file è stato conservato, perché la convenzione prescrive di conservarlo e perché toccarlo sarebbe stato un cambiamento non richiesto. Il primo tentativo di correzione, del resto, è fallito proprio sul BOM, dato che il parser JSON lo rifiuta se non gli si dice di aspettarselo: l'errore è arrivato prima della scrittura, quindi non ha prodotto danni, ed è un buon esempio di perché convenga verificare il contenuto prima di riscriverlo e non dopo.

Il ritrovamento più consistente è arrivato lanciandolo sul progetto gemello: *otto file misti*, e sette di essi con esattamente quattro righe `LF` in un corpo di centinaia di `CRLF`. Quattro righe sono la lunghezza dell'intestazione di provenienza che `tools/sync-ambiente.py` antepone a ogni file propagato, e la coincidenza esatta ha indicato subito il colpevole: lo strumento scriveva quella intestazione sempre con `LF`, a prescindere dalla fine riga del corpo. Non era quindi un difetto dei file ma dello strumento che li genera, cioè un difetto che si sarebbe ripresentato a ogni propagazione futura.

Corretto facendo dedurre allo strumento la fine riga dal corpo del file e scrivendo l'intestazione con quella. Ripropagati i sette file, il conteggio dei misti nel gemello è passato da otto a uno, e il residuo era la stessa riga vuota terminata con ritorno carrello di `settings.json`, presente in modo identico anche là: corretta con le stesse due cautele, JSON confrontato prima e dopo e BOM conservato.

Vale registrare la forma del ragionamento, perché è riusabile. Il numero costante di righe anomale attraverso file di dimensione molto diversa è l'indizio che il difetto non sta nei file ma in qualcosa che li tocca tutti allo stesso modo: una anomalia proporzionale alla dimensione indica il contenuto, una anomalia di misura fissa indica il generatore.

È il tipo di difetto che questo progetto deve saper trovare da solo, perché nasce dal fatto stesso di avere una convenzione che conserva due formati invece di imporne uno.

Allineato infine lo snapshot di sincronizzazione, che dichiarava come commit di riferimento uno di due giorni prima e descriveva una storia di quattro commit su origin quando ne esistono ventidue.

Esito: fatto.

### MS-064 - La chiavetta non si formatta, e una lettera di unità non identifica un disco

Perimetro: risposta operativa alla preparazione del supporto, avvertenza aggiunta a PA-004 e allo strumento delle azioni differite.

L'utente ha collegato una chiavetta Kingston DataTraveler 3.0 da 57,7 GB e ha aperto la finestra di formattazione di Windows, chiedendo con quale filesystem formattarla. La risposta corretta è *nessuno*, e vale spiegarla perché è controintuitiva: la finestra di formattazione, in questa procedura, non va usata affatto.

La ragione sta nella modalità di scrittura scelta nella sottofase 2.3. In modalità DD l'immagine viene copiata sul dispositivo byte per byte a partire dal settore zero, quindi sovrascrive la tabella delle partizioni e con essa qualunque filesystem esistente. Formattare prima significa costruire una struttura che verrà cancellata in blocco pochi minuti dopo: non è dannoso, è lavoro senza effetto. La stessa cosa vale per la scelta del filesystem, che in modalità DD non è una scelta dell'utente ma una proprietà dell'immagine. La chiavetta risultava inoltre vuota, 57,7 GB liberi su 57,7, quindi non c'era nulla da preservare e nemmeno la ragione prudenziale di guardare prima cosa contenesse.

La capienza è ampiamente sufficiente per un'immagine da 6,64 GiB, quindi il vincolo dei 16 GB della sottofase 2.3 è rispettato con abbondanza.

Il fatto che merita di essere registrato, però, è un altro, ed è emerso per caso guardando l'elenco dei volumi. La chiavetta ha ricevuto la lettera *`G:`*, che è la stessa con cui PA-004 identifica il disco contenente il materiale EASE Focus 3.1.10 del workshop K-array. Non è quel disco: questo è vuoto e quello contiene una cartella `LIBRARY`. Ma la coincidenza dimostra un difetto di metodo che era latente in quella voce da quando è stata aperta.

Una lettera di unità su Windows non è un identificatore di dispositivo. Il sistema assegna la prima lettera libera al momento del collegamento, quindi la stessa lettera indica dispositivi diversi in momenti diversi, e lo stesso dispositivo si presenta con lettere diverse a seconda di che altro è collegato. PA-004 nasceva dalla lettura di un collegamento `.lnk` che puntava a un percorso su `G:`, e quel percorso è l'unica informazione che il collegamento conteneva: la lettera che vi compare era quella valida sulla macchina nel momento in cui il collegamento fu creato, non una proprietà del disco.

Ne segue la correzione del criterio, scritta sia nella voce sia nello strumento. Il disco cercato si riconosce dal *contenuto*, cioè dalla presenza del percorso completo con la cartella `LIBRARY`, non dalla lettera. Trovare quel percorso su una lettera è una conferma; non trovarlo significa soltanto che quel dispositivo non è collegato adesso; e trovare la lettera occupata da un altro volume non è un indizio di nulla. Lo strumento ora dichiara esplicitamente questo terzo caso, con una riga che avvisa quando la lettera esiste ma il percorso no, così che chi legge l'esito non concluda di aver trovato il disco sbagliato quando semplicemente non c'è.

È la stessa famiglia di errore di MS-054, dove un controllo inchiodava un percorso fisso per un archivio che l'utente poteva spostare, e di MS-063, dove il percorso dell'immagine è cambiato in corsa. Il denominatore comune: in un controllo automatico l'invariante da usare è la proprietà stabile della cosa cercata, cioè il nome di un file o il contenuto di una cartella, non la sua collocazione, che è una circostanza.

Esito: fatto per la parte documentale; la scrittura della chiavetta resta dell'utente.

### MS-065 - La modalità DD si sceglie dopo Avvia, non prima: un difetto di istruzione

Perimetro: sottofase 2.3 della procedura, propagata al progetto gemello.

L'utente ha configurato Rufus e ha chiesto che cosa mancasse, non trovando la scelta della modalità di scrittura. Non mancava nulla: la configurazione era corretta e lo stato dichiarava pronto. Mancava una informazione nella mia istruzione, ed è un difetto di documentazione che vale registrare perché produce esattamente il dubbio che ha prodotto.

La scelta fra modalità immagine ISO e modalità immagine DD *non è un campo della finestra principale*: è una finestra di dialogo che compare dopo aver premuto Avvia, quando Rufus riconosce che l'immagine è di tipo ibrido. La sottofase 2.3, come l'avevo scritta, diceva che Rufus la chiede con una finestra ma non diceva quando, e chi legge cerca fra le opzioni prima di avviare, non trova niente, e conclude che manchi qualcosa da configurare. Una istruzione che nomina una scelta senza dire in quale momento si presenta è incompleta anche se non è sbagliata.

Corretta la sottofase dicendo esplicitamente che la finestra arriva dopo Avvia, e aggiunta la descrizione della configurazione corretta verificata su Rufus 4.15, campo per campo, così che si possa confrontare invece di indovinare: dispositivo la chiavetta, immagine con la spunta verde di riconoscimento, partizione persistente a zero perché si prepara un installatore e non un sistema live con memoria, schema GPT, destinazione UEFI senza CSM, e lo stato che dichiara pronto.

Chiarito anche un campo che a quel punto trae in inganno. Prima di premere Avvia il sistema di file mostra `Large FAT32`, e va lasciato così, perché è il valore che Rufus propone presumendo la modalità ISO e in modalità DD diventa irrilevante, dato che nessun filesystem viene costruito. Il punto tecnico che serve capire è che `Large FAT32` non rimuove il limite di 4 GB per singolo file: rimuove il limite di dimensione del *volume*, consentendo FAT32 oltre i 32 GB. Sono due vincoli diversi e confonderli porta a credere che in modalità ISO il problema del filesystem compresso oltre i 4 GB non esista.

Aggiunta infine una avvertenza sul dispositivo, perché è il campo dove un errore costa caro e perché in questa sessione la circostanza c'era per davvero: alla postazione era collegato anche il disco esterno di lavoro da 465,8 GB accanto alla chiavetta da 57,7, e Rufus cancella per intero il dispositivo che gli si indica. La distinzione si fa sulla capacità dichiarata accanto al nome, non sulla posizione nell'elenco.

Esito: fatto.

### MS-066 - Un avvertimento ritirato: la casella che rende impossibile l'errore che temevo

Perimetro: completamento della sottofase 2.3, ritiro di una avvertenza data in MS-065.

In MS-065 avevo avvertito di non confondere la chiavetta con il disco esterno di lavoro, dato che entrambi erano collegati e Rufus cancella per intero il dispositivo che gli si indica. L'avvertenza era prudente ma *descriveva un rischio che la configurazione in uso aveva già eliminato*, e va ritirata in modo esplicito invece di essere lasciata a scadere: la barra di stato di Rufus dichiarava un solo dispositivo rilevato, e la ragione è che la casella `Elenco unità disco USB` era deselezionata.

Quella casella è il presidio che tiene i dischi rigidi e gli SSD esterni fuori dall'elenco dei dispositivi, lasciandovi soltanto le unità rimovibili. Spenta com'era, il disco di lavoro da 465,8 GB non era selezionabile nemmeno volendo, quindi il rischio di indicare il dispositivo sbagliato non era ridotto ma assente. Attivarla lo reintroduce, ed è la ragione per cui la sottofase ora prescrive di non attivarla senza un motivo preciso: è una impostazione che scambia sicurezza per una capacità che in questa procedura non serve.

La forma corretta di una avvertenza, e vale come regola oltre il caso, è darla insieme alla sua mitigazione. Un avvertimento senza la condizione in cui il rischio si presenta insegna a diffidare di un passo che è sicuro, e la diffidenza generica si spende male: fa controllare due volte la cosa già protetta e distrae dalle altre. Nel caso specifico, il rischio esiste soltanto se si attiva una casella, e dirlo cambia l'istruzione da guarda bene a lascia quella casella come è.

Documentate nella stessa occasione le tre opzioni avanzate di formattazione, che l'utente ha aperto e che non erano descritte. Formattazione rapida e creazione dell'etichetta estesa con i file icona appartengono alla modalità ISO, dove un filesystem viene costruito, quindi in modalità DD non hanno oggetto. Il test dei blocchi errati va lasciato spento, e la ragione non è la fretta: su un supporto nuovo aggiunge una lettura completa dell'intera capacità senza dire nulla che l'esito della scrittura non dica già, e su un supporto sospetto la domanda a cui rispondere non è se abbia blocchi difettosi ma se valga la pena usarlo per un installatore.

Esito: fatto.

### MS-067 - Inferenza ritirata: dentro l'immagine non c'è nessun file oltre i 4 GiB

Perimetro: ritiro di una affermazione data come fatto in MS-059, MS-061 e MS-065 e nella sottofase 2.3, con la misura che la smentisce.

L'utente ha chiesto che cosa significhi la modalità DD, e nel rispondere ho verificato l'affermazione su cui avevo poggiato la raccomandazione invece di ripeterla. Era sbagliata.

Avevo affermato che dentro l'immagine di Ubuntu Studio 26.04.1 il filesystem compresso del sistema supera i 4 GiB, e che quindi la modalità immagine ISO, che costruisce un FAT32, non potesse contenerlo. La misura del contenuto dell'immagine dice il contrario: il file più grande è `casper/minimal.squashfs` con *4.112.433.152 byte*, cioè 3,83 GiB, contro un limite di 4.294.967.295 byte per singolo file su FAT32. Il secondo per dimensione, `casper/minimal.standard.squashfs`, sta a 2.162.012.160 byte. Nessun file supera la soglia, quindi la modalità ISO avrebbe funzionato e il suggerimento dello strumento, che proponeva proprio quella, era corretto.

La progressione dell'errore è la parte da registrare, perché è identica a quella di MS-050 e va riconosciuta prima che si ripeta. In MS-059 l'avevo scritta come probabile, con la formula che il filesystem compresso supera quella soglia con ogni probabilità. In MS-061 era diventata una affermazione senza qualificazioni. In MS-065 la usavo come premessa per spiegare un altro punto, cioè il significato di `Large FAT32`, che è il segno che era stata promossa a fatto e usata come fondamento. Tre passaggi, nessun ritorno alla fonte, e la fonte era a un comando di distanza: l'elenco del contenuto dell'immagine con un archiviatore.

Il margine è del quattro per cento, e questo va detto perché spiega la plausibilità senza scusare la promozione: 3,83 GiB contro 4 GiB è vicinissimo, quindi l'ipotesi era ragionevole come ipotesi. Ne segue anche che l'argomento non è sbagliato in generale ma soltanto su questa immagine: su un'altra derivata, o su una versione futura di questa, quel file può superare la soglia. La prescrizione corretta non è quindi eliminare l'argomento ma renderlo condizionale a una misura, e la misura è entrata nella sottofase 2.3 come comando.

Che cosa non cambia, ed è la ragione per cui l'errore non ha prodotto danni operativi. La scelta della modalità DD resta corretta, ma su due motivi diversi da quello caduto. Il primo è che la chiavetta risulta verificabile a posteriori, essendo un clone esatto di un file di cui si conosce l'impronta firmata, mentre una chiavetta scritta in modalità ISO non è confrontabile con nulla perché il suo contenuto è una struttura nuova. Il secondo è che l'avvio non dipende da un caricatore costruito dallo strumento ma da quello che l'immagine porta con sé, collaudato da chi l'ha pubblicata. Il costo della scelta, in cambio, è che la chiavetta diventa un installatore e nient'altro: non vi si aggiungono file, lo spazio residuo non è utilizzabile, e per riusare il supporto occorre azzerarne la tabella delle partizioni con `diskpart` e la sua operazione `clean`, dato che una formattazione dall'interfaccia grafica non basta.

Riscritta di conseguenza la sottofase 2.3, che ora spiega la differenza fra le due modalità in termini di ricostruzione contro copia esatta, dichiara le due ragioni valide della scelta, dichiara il costo, e riporta l'inferenza ritirata con la misura invece di far sparire il motivo sbagliato. Nel registro il paragrafo di MS-061 è conservato come era, con una nota di ritiro in evidenza: la regola di questo progetto è che una inferenza smentita si ritira esplicitamente e non si cancella in silenzio, altrimenti il documento sembra essere sempre stato giusto e non si impara nulla.

Una nota marginale sul metodo, perché è costata due minuti. Il controllo che uso per non inserire due volte lo stesso microstep cerca l'identificativo nel file, e qui ha rifiutato l'inserimento: l'identificativo c'era già, ma dentro il rimando che avevo appena scritto nella nota di ritiro di MS-061. Una guardia che cerca una stringa qualunque scatta anche sulle citazioni legittime di quella stringa; quella corretta cerca l'intestazione, cioè il marcatore di titolo seguito dall'identificativo.

Esito: fatto.

### MS-068 - Chiavetta scritta in DD, e uno strumento che la verifica invece di crederci

Perimetro: chiusura della sottofase 2.3, nuove sottofasi 2.4 e 2.5 della procedura, nuovo strumento `tools/verify-usb-dd.ps1`, propagato al progetto gemello.

La scrittura è riuscita. Otto minuti e sette secondi, stato verde, e il dispositivo che prima si presentava come un volume unico ora si presenta come partizioni multiple. La struttura risultante è la prova visibile che la modalità DD è stata effettivamente usata: tabella GPT con tre partizioni, cioè il volume principale dell'immagine di circa 6792 MB, una partizione di sistema EFI di 5 MB e una partizione ausiliaria di 0,3 MB. Sono le partizioni che l'immagine ibrida porta con sé, non una struttura costruita dallo strumento di scrittura, che in modalità ISO ne avrebbe creata una sola.

Il resto di questo microstep è la verifica, e vale spiegare perché merita uno strumento invece di una spunta. La modalità DD ha una proprietà che la modalità ISO non ha: la chiavetta è un clone byte per byte del file, quindi i primi N byte del dispositivo grezzo, con N pari alla dimensione esatta dell'immagine, devono avere la stessa impronta del file. È l'unico caso in cui un supporto di installazione si può verificare, invece di accettarne la riuscita sulla parola dello strumento che l'ha scritto. Una chiavetta scritta in modalità ISO non è confrontabile con nulla, perché il suo contenuto è un filesystem nuovo che nessuna impronta pubblicata descrive, e questa è la seconda ragione valida per cui la sottofase 2.3 prescrive DD, dopo il ritiro della prima in MS-067.

Scritto quindi `tools/verify-usb-dd.ps1`, che apre il dispositivo grezzo, ne legge esattamente la dimensione dell'immagine a blocchi da 1 MiB calcolando l'impronta in modo incrementale, e la confronta con quella del file. Tre dettagli di realizzazione meritano di stare a verbale perché sono i punti in cui una versione ingenua fallisce.

Il primo è la condivisione. I volumi della chiavetta risultano montati con lettere proprie subito dopo la scrittura, quindi l'apertura del dispositivo grezzo va fatta dichiarando la condivisione in lettura e scrittura: senza quella dichiarazione l'apertura fallisce con un errore di condivisione, che si legge come un permesso negato e manda a cercare la causa nel posto sbagliato.

Il secondo è l'allineamento ai settori. Un dispositivo grezzo si legge per settori, quindi la dimensione da confrontare deve essere un multiplo di 512. Per una immagine ISO è sempre vero, dato che il suo blocco è di 2048 byte, e per questa in particolare i conti tornano in modo netto: 7.127.195.648 byte sono esattamente 6797 blocchi da 1 MiB. Lo strumento lo verifica comunque e si rifiuta di procedere se il conto non torna, invece di arrotondare: un arrotondamento silenzioso produrrebbe un confronto fra quantità diverse, cioè un esito negativo senza causa apparente.

Il terzo sono i privilegi, ed è la stessa constatazione già fatta due volte in questa sessione sotto forme diverse. Leggere un dispositivo grezzo richiede l'elevazione, perché significa aprire un percorso nello spazio dei nomi dei dispositivi e non un file dentro un filesystem: è la stessa ragione per cui SMART richiede privilegi su Windows come su Linux, cioè che si sta parlando al dispositivo e non al filesystem che vi sta sopra.

Sulla portata della verifica lo strumento è esplicito, e la procedura con lui, perché è il punto in cui si crede di aver verificato più di quanto si è verificato. Il confronto dimostra la fedeltà della copia, cioè che la scrittura non ha introdotto errori e che il supporto rilegge ciò che vi è stato scritto. Non dice nulla sull'autenticità dell'immagine, che è la domanda della sottofase 2.2 e va risolta prima di scrivere, non dopo. Passando allo strumento anche l'impronta attesa, una sola esecuzione risponde a entrambe le domande, ma restano due domande e non una.

Documentate anche le tre cause di un esito negativo, in ordine di probabilità, perché senza di esse un fallimento manda a sospettare la chiavetta per prima quando è la spiegazione meno probabile: scrittura avvenuta in modalità ISO invece che DD, disco sbagliato indicato, oppure un supporto che non conserva ciò che scrive. Solo la terza è un problema del supporto, e in quel caso quella chiavetta non va usata per installare, perché un errore che si manifesta durante la copia dei file di sistema produce un guasto difficile da attribuire.

Riorganizzata infine la fase 2, che ora ha cinque sottofasi invece di tre: scaricamento, verifica dell'immagine, scrittura, verifica della chiavetta, e come 2.5 la scrittura dalla macchina Linux come alternativa, che prima stava in coda alla 2.3 dove sembrava un seguito e non una strada diversa.

Esito: fatto. Resta da eseguire la verifica, che richiede una sessione elevata e quindi è dell'utente.

### MS-069 - Verifica sbagliata, strumento troppo lento, e una domanda semplice complicata

Perimetro: riscrittura della sottofase 2.4, riscoperta del suo scopo, rimozione di uno strumento appena creato, correzione dell'altro.

È il microstep più scomodo della sessione e va scritto per intero, perché l'errore non è tecnico ma di giudizio, e l'utente ha dovuto interromperlo. La domanda era: la chiavetta è pronta, posso azzerare la macchina, dove sono le informazioni per ricostruirla. La risposta corretta era una riga per ognuna. Al suo posto ho costruito due strumenti di verifica, dei quali il primo ha dato un falso allarme e il secondo si è piantato.

*Il falso allarme.* Avevo prescritto, nella sottofase 2.4, di confrontare l'impronta dei primi byte del dispositivo grezzo con quella dell'immagine, sul presupposto che una chiavetta scritta in modalità DD debba restare identica al file. Il confronto ha dato impronte diverse su una chiavetta valida, e il presupposto è falso su Windows per tre ragioni che sono tutte scritture legittime del sistema, non guasti. Una immagine ibrida porta una tabella GPT dimensionata sull'immagine, con la copia di sicurezza alla propria fine; scritta su un supporto da 57,7 GB quella copia si trova a metà disco invece che in fondo, e il sistema la ripara spostandola e riscrivendo l'intestazione primaria, il campo che punta alla copia e il codice di controllo. La zona da cui la copia è stata rimossa cambia a sua volta. E le due partizioni piccole vengono montate con lettera propria, fra cui quella di sistema EFI che è formattata FAT, dove Windows crea le proprie cartelle di servizio al primo accesso.

Ne segue la regola: un confronto byte per byte fra una immagine e il supporto su cui è stata scritta ha senso soltanto su un sistema che non monta i volumi da sè e non ripara le tabelle delle partizioni. Su Windows la differenza è la norma, quindi quel confronto non è una verifica ma un generatore di falsi allarmi. La verifica giusta esisteva già e non l'avevo nominata: è quella che il supporto fa su se stesso dal proprio menu di avvio, alla voce di controllo dei difetti, che confronta le somme che l'immagine porta al proprio interno.

*Lo strumento che si è piantato.* Per capire dove fossero le differenze ho scritto un secondo strumento che confrontava blocco per blocco, e l'ho scritto con un ciclo che confronta i byte uno alla volta in PowerShell: su sette miliardi di byte quel ciclo richiede ore, e l'utente ha visto una finestra ferma allo zero per cento. Non era bloccata, era mal scritta. La lezione tecnica è che in PowerShell l'iterazione elemento per elemento su volumi grandi non è praticabile e va sostituita da un confronto vettoriale o da un altro linguaggio; la lezione di merito è che quello strumento non serviva, perché rispondeva a una domanda che non era stata posta.

Lo strumento è stato rimosso invece di essere ottimizzato, perché ottimizzarlo avrebbe conservato il difetto più grande, cioè l'esistenza. `tools/verify-usb-dd.ps1` invece resta, ma con lo scopo corretto dichiarato in testa al suo docstring: non serve a verificare una chiavetta appena scritta su Windows, e il suo uso legittimo è confrontare una copia grezza che nessun sistema operativo abbia montato né riparato. Corretto anche il messaggio che stampa in caso di esito negativo, che elencava tre cause tutte allarmanti e ometteva quella più probabile: adesso la prima voce dell'elenco è la scrittura legittima del sistema operativo, e il guasto del supporto è l'ultima.

*Il difetto di giudizio, che è la parte che conta.* Ogni singolo passaggio era difendibile: verificare è meglio che fidarsi, e uno strumento è meglio di un comando a mano. Ma sommati hanno prodotto una sessione in cui una chiavetta pronta sembrava sospetta e una domanda semplice non ha ricevuto risposta. La verifica ha un costo, e quel costo va confrontato con il rischio che copre: qui il rischio era una chiavetta scritta male, la cui unica conseguenza sarebbe stata un avvio fallito, cioè cinque minuti e nessun danno, mentre il presidio proposto costava mezz'ora, due strumenti nuovi e un allarme falso. Il criterio corretto è quello: si verifica quando la conseguenza di un errore è costosa o difficile da attribuire, non per completezza.

Va aggiunto che il rischio residuo era anche coperto altrove, e questo rende il presidio non solo costoso ma ridondante: il supporto verifica se stesso all'avvio, e un avvio fallito è immediatamente diagnostico.

Riscritta quindi la sottofase 2.4 in modo che prescriva il controllo dei difetti dal menu di avvio, spieghi perché il confronto integrale non va usato su Windows, e conservi come riferimento la sola cosa utile che l'esecuzione ha prodotto: il fatto che a fine scrittura la chiavetta presenti tre partizioni in tabella GPT, cioè quelle dell'immagine ibrida, e che questo si legga a occhio come conferma che la modalità DD è stata usata, senza bisogno di alcuno strumento.

Esito: fatto. La chiavetta è pronta e i prerequisiti dell'installazione sono soddisfatti.

### MS-070 - La carta era indietro rispetto alla procedura, e nessuno poteva accorgersene

Perimetro: nuovo strumento `tools/make-scheda-docx.py`, `.docx` rigenerato in `C:\Users\Utente\Downloads\`, nota di apertura di `docs/10-ambiente/scheda-reinstallazione.md` corretta, copia precedente del `.docx` conservata sotto `_notes/`.

La sessione del 2026-09-08 si è interrotta per un crash mentre si stava modificando il `.docx` da stampare, e la ripresa ha dovuto ricostruire lo stato dal disco invece che dalla conversazione. La ricostruzione è riuscita e vale registrare su che cosa poggia, perché è un caso in cui i timestamp sono l'unica fonte: il `.docx` in `Downloads` portava l'ora 15:10, la sottofase 4.2 di `installazione-pulita-26-04.md` era stata riscritta alle 15:12 e `scheda-reinstallazione.md` alle 15:14. La carta era quindi *indietro di due minuti* rispetto alla documentazione, e l'estrazione del testo dal `.docx` lo ha confermato senza margini: non conteneva né la parola *filesystem* né la parola *riepilogo*, cioè mancava esattamente di ciò che la fase 4.2 aveva guadagnato alle 15:12.

*Il difetto vero non è il crash.* Il crash ha soltanto reso visibile un difetto che era già lì: il documento di stampa non era riproducibile, perché il codice che lo aveva costruito viveva soltanto nella sessione e con essa è stato perduto. Ne seguivano due conseguenze, e la seconda è peggiore della prima. La prima è che l'unico modo di riallineare la carta alla procedura era riscrivere tutto. La seconda è che `scheda-reinstallazione.md`, che è un file tracciato e quindi una promessa fatta a chi clona il repository, dichiarava in apertura che il `.docx` si generasse con `python tools/make-scheda-docx.py`, e quello strumento non esisteva. Una affermazione falsa in un documento tracciato è peggio di una lacuna, perché la lacuna si vede e l'affermazione no.

Scritto quindi lo strumento, in sola libreria standard come gli altri di questo progetto, dato che un `.docx` è un archivio zip di documenti XML e le cinque parti che servono si scrivono direttamente. La scelta di non usare una libreria di terze parti non è ideologica: `tools/` non ha e non ha mai avuto un file di dipendenze, quindi introdurne una qui significherebbe che gli altri strumenti girano e questo no, su una macchina appena reinstallata che è esattamente lo scenario di questo progetto.

Una proprietà dello strumento va dichiarata perché è un limite e non una comodità. Non converte il Markdown: il contenuto della scheda vive nello strumento come dati, e i due vanno tenuti allineati a mano. La ragione è che la carta ha vincoli che il Markdown non ha, cioè due pagine di spazio, caselle da spuntare a penna e riquadri colorati sul passo irreversibile, e una conversione automatica li perderebbe tutti. Il prezzo è il disallineamento possibile, che è lo stesso difetto che questo microstep sta riparando, e l'unico presidio è la regola già scritta nella scheda: se le due divergono ha ragione la procedura completa.

Su che cosa il `.docx` ha guadagnato rispetto alla versione delle 15:10, ed è la ragione per cui la sessione era stata aperta. L'avvertenza sulla casella di formattazione compare adesso in tre punti, scelti perché sono i tre momenti in cui l'operatore ha gli occhi in tre posti diversi. Un riquadro in testa, intitolato a come si sbaglia in concreto e non al rischio, perché il rischio era già nominato dal riquadro precedente e ripeterlo non aggiunge nulla. La riga di `nvme0n1p4` nella mappa delle partizioni, dove l'azione non è più soltanto di montare e non formattare ma di non toccare il menu del filesystem. E il passo 9 della sequenza, dove l'avvertenza è scritta nella forma dell'azione, cioè che il menu del filesystem non si tocca perché selezionare un filesystem spunta la formattazione da sé.

Aggiunto anche un passo che prima non c'era, ed è il terzo dei tre momenti: la lettura della schermata di riepilogo, dove una formattazione deve comparire soltanto per `nvme0n1p2`. La sequenza passa quindi da dodici a tredici passi. Vale notare perché quel passo mancava del tutto: nella procedura completa la schermata di riepilogo era descritta come una raccomandazione in prosa, e in una lista di cose da spuntare una raccomandazione in prosa non si spunta. Il controllo più importante della fase era l'unico senza casella.

Aggiunta infine una sezione 4 con le tre verifiche al primo avvio, che nella scheda sorgente c'erano e nel `.docx` mancavano del tutto. È un'aggiunta che va oltre l'avvertenza richiesta, e va dichiarata come tale invece di essere fatta passare per parte della richiesta: la ragione è che quei tre comandi sono ciò che dice se `/home` è sopravvissuto, quindi sono il seguito diretto del passo irreversibile e su un foglio che si porta accanto alla macchina servono più che nella pagina che resta sulla postazione.

Sui dati di licenza la scelta è cambiata rispetto a quella che la scheda dichiarava, ed è registrata come ADR-017: il documento generato non li contiene, e li aggiunge soltanto se lo si chiede con `--con-licenza`.

Verificato con tre controlli, in ordine di forza crescente. L'integrità dell'archivio e la buona formazione di tutte e cinque le parti XML, con `zipfile.testzip` e `ElementTree.fromstring` su ciascuna, che ha risposto valido su 556, 297, 282, 41.635 e 881 byte. L'apertura del documento con `python-docx`, che è un lettore indipendente da chi ha scritto il file e quindi vale come prova che il pacchetto è conforme e non solo ben formato: sedici paragrafi e tre tabelle, di cinque righe per cinque colonne, cinque per tre e tredici per tre, cioè i conti attesi. E la rilettura del testo di tutte le celle, che ha confermato la presenza dell'avvertenza nei tre punti e la sequenza a tredici passi. Provata anche la variante `--con-licenza`, che ha prodotto la sezione con i due valori corretti letti dal file riservato; il file di prova è stato cancellato subito dopo il controllo, perché conteneva il codice di attivazione.

Esito: fatto. La copia precedente del `.docx` è conservata in `_notes/scheda-docx-precrash-2026-09-08.docx`, non sovrascritta, perché era il documento che l'utente stava per stampare e il confronto fra le due versioni è la prova di questo microstep.

### MS-071 - Ventotto accenti con l'apostrofo in un file tracciato, e un mio errore nel ripararli

Perimetro: `docs/10-ambiente/scheda-reinstallazione.md`, correzioni tipografiche e di un errore ripetuto.

La scheda sorgente, creata nella sessione interrotta e non ancora tracciata, violava in ventotto punti la convenzione tipografica che questo progetto dichiara vincolante: gli accenti erano scritti con l'apostrofo, nella forma `e'` invece di è e `perche'` invece di perché. Portava inoltre un errore ripetuto tre volte, cioè *si scegle* invece di *si sceglie*, che nella procedura completa era già stato corretto nella stessa giornata ma non nella scheda derivata.

La correzione degli accenti è stata fatta con `python tools/fix-accents.py`, che ha riportato ventinove sostituzioni su otto forme distinte, e la catena è stata completata con `fix-missing-accents.py`, che non ha trovato nulla da fare oltre a centoquattordici forme ambigue lasciate intatte per progetto, e con `fix-dashes.py`, che ha trovato zero trattini lunghi.

*L'errore è nella correzione dell'altro difetto, ed è mio.* Ho sostituito le tre occorrenze di *scegle* con tre regole di `sed` in una sola invocazione, includendo per prudenza anche la forma `si scegli`, e la terza regola ha colpito il risultato prodotto dalla prima: *si sceglie* è diventato *si scegliee* in due dei tre punti. Il difetto è stato visto subito, perché avevo fatto seguire alla sostituzione la rilettura delle righe toccate invece di fidarmi del codice di uscita, e riparato con una quarta sostituzione.

La regola che ne discende vale oltre il caso, perché è la stessa trappola che rende pericolosa qualunque sequenza di sostituzioni testuali: più regole in una sola invocazione si applicano in cascata sul testo già modificato, non in parallelo sul testo originale, quindi una regola il cui bersaglio è un prefisso del risultato di un'altra la corrompe. Il presidio non è scrivere regole più intelligenti ma ordinarle dalla più specifica alla più generica, oppure eseguirle una per volta rileggendo, e in ogni caso rileggere il risultato e non il codice di uscita. Vale ricordare che è la seconda volta in questo progetto che una sostituzione fatta a mano produce un danno tipografico: la prima è MS-062, e la lezione era già la stessa.

Estesa poi la correzione al resto della documentazione, e il modo in cui il perimetro si è ristretto strada facendo è la parte istruttiva. Una prima conta dava venti occorrenze in questo registro e cinque in `CLAUDE.md`, numeri che avrebbero giustificato di rinviare la ripulitura a un commit separato. Guardando le occorrenze una per una invece del solo totale è emerso che quasi tutte stanno dentro code span, cioè sono le forme sbagliate citate di proposito come esempi in MS-014, MS-056 e MS-062, che sono i microstep che raccontano i difetti degli strumenti tipografici. Correggerle avrebbe distrutto la documentazione di quei difetti, riducendo una frase come quella che dice che lo strumento converte correttamente una certa forma a una affermazione priva di senso.

Prima di lanciare lo strumento sui due file ho quindi verificato con un caso minimo se protegge i code span inline, dato che la convenzione dichiara esplicitamente la protezione dei soli blocchi recintati. Li protegge: su un file di prova con tre esempi fra backtick e due errori in prosa ha fatto due sole sostituzioni, quelle in prosa. I difetti reali erano quindi due in questo registro e tre in `CLAUDE.md`, e sono corretti; gli esempi citati sono intatti, riletti uno per uno dopo l'esecuzione.

Il primo tentativo di quel caso minimo è però fallito in un modo che vale registrare, perché l'errore era mio e mi ha quasi fatto concludere il contrario del vero. Avevo scritto il file di prova nella cartella di lavoro temporanea della sessione, che sta su `C:`, e lo strumento è terminato con una eccezione senza modificare niente; avendo silenziato lo standard error per leggere soltanto il file risultante, ho visto un file non modificato e stavo per concluderne che lo strumento protegge tutto, prosa compresa. La causa è il difetto cross-disco già diagnosticato in MS-014 e tracciato in PA-003, cioè `os.path.relpath` fra due lettere di unità diverse, che `md-unwrap.py` ha corretto e i tre strumenti tipografici no. La lezione operativa è duplice: non si silenzia lo standard error di uno strumento di cui si sta misurando il comportamento, e un esito nullo non è un esito negativo finché non si è letto il codice di uscita. Vale anche come conferma indipendente che PA-003 merita di essere chiusa, perché lo stesso difetto è ora costato tempo tre volte.

Resta fuori la grafia nei modelli sotto `.claude/templates/`, per una decina di occorrenze. Non si corregge qui di proposito: quei file sono copie del template, e riscriverli in questo repository allargherebbe la divergenza che PA-003 esiste per chiudere, quindi la correzione appartiene alla propagazione all'indietro e non a questo fronte.

Esito: fatto per la scheda e per la documentazione del progetto, lasciato ai modelli del template il residuo che appartiene a PA-003.

## 2026-09-09, installazione eseguita e verificata da remoto

### MS-072 - La reinstallazione è riuscita e `/home` è intatto, con la prova diretta

Perimetro: sola lettura sulla macchina via SSH, dopo l'installazione eseguita dall'utente l'8 settembre.

Il passo irreversibile è andato bene. La prova non è il riepilogo dell'installatore, che è una dichiarazione di intenti, ma il contenuto reale del disco dopo il primo avvio: la scrivania si è ripresentata con `AKABAK_Pro_v324b126.exe`, `VACS_32_v213b33.exe`, `Ardour projects`, `Room acoustics` e `Progetto-stanza`, e `~/electroacoustics` conta esattamente *281 file per 728 MB*, cioè i due numeri registrati in MS-039 al momento del trasferimento. Anche il prefix Wine `~/.wine` è sopravvissuto con il suo `drive_c`, datato 13 agosto 2025.

Il sistema installato è `Ubuntu 26.04.1 LTS`, kernel `7.0.0-31-generic`, Plasma 6.6.6 su Wayland, e il supporto dichiara `Ubuntu-Studio 26.04.1 LTS "Resolute Raccoon" - Release amd64 (20260826)`. L'identificativo numerico dell'utente è `1000` e `/home/alesop95` appartiene a `1000:1000`: l'utente nuovo ha ereditato l'identità del vecchio, quindi l'avvertenza sui permessi da correggere a mano non si è avverata. La condizione che l'ha evitata è aver creato l'utente con lo stesso nome, che la scheda prescriveva al suo ultimo passo.

L'accesso SSH è stato ristabilito, e il modo in cui è avvenuto merita di stare a verbale perché non era ovvio e ha risparmiato un giro. La radice azzerata ha portato via `openssh-server` e le chiavi d'identità della macchina, ma `authorized_keys` vive in `/home` ed è sopravvissuto: il file porta ancora la data del 7 settembre alle 09:08, con i permessi `600` su una cartella `700`, cioè già conformi a quanto il servizio pretende. È bastato installare il server. Dal lato della postazione è servito rimuovere la voce vecchia dall'archivio delle chiavi note, perché l'identità della macchina è cambiata legittimamente con la reinstallazione, e un cambio di chiave host è indistinguibile da un attacco per chi guarda solo il messaggio d'errore.

Verificato con: connessione non interattiva riuscita, cioè `ssh` con `BatchMode` attivo che ha risposto `CONNESSO`, `alessio-ubuntustudio`, `7.0.0-31-generic`, `Ubuntu 26.04.1 LTS`. Con `BatchMode` nessuna richiesta di password è possibile, quindi l'autenticazione è passata per chiave e l'accesso automatizzato è di nuovo disponibile.

Lo stato del gestore dei pacchetti è pulito: `dpkg --configure -a` seguito da `apt -f install` ha riportato zero pacchetti da aggiornare, installare o rimuovere. La fase interrotta non ha lasciato pacchetti a metà configurazione.

Esito: fatto. Le fasi 4 e 5 della procedura sono chiuse.

### MS-073 - Il blocco di sedici ore era dopo la fine dell'installazione, e il supporto era stato verificato da sé

Perimetro: lettura dei log dell'installatore conservati in `/var/log/installer/` sul sistema installato. Ritira una prescrizione della scheda e una affermazione di MS-069.

L'installazione si è piantata alla schermata `Setting up the system` e vi è rimasta per sedici ore, dalle 18 di sera alle 10 del mattino, finché l'utente ha riavviato togliendo la chiavetta. La macchina si è avviata correttamente. La domanda che restava era che cosa si fosse bloccato e che danno avesse lasciato, e i log copiati nel sistema installato rispondono a entrambe.

Il danno è nessuno, e la ragione è che il blocco era *dopo* la fine dell'installazione vera. L'ultima riga di `curtin-install.log` è `curtin: Installation finished.`, preceduta da `install-grub: SUCCESS` e `configuring-bootloader: SUCCESS`. Curtin è il componente che partiziona, copia il sistema e installa il boot loader: ha completato tutto e ha smontato ordinatamente `/target`. Ciò che è rimasto appeso è un passo successivo dell'interfaccia, e la sua natura resta ignota perché il log di dettaglio richiede privilegi. L'ora dice qualcosa comunque: l'ultima scrittura di log è delle 17:50, quindi il silenzio è cominciato lì.

Le tre osservazioni indipendenti che confermano l'integrità del risultato sono `dpkg` senza pacchetti a metà, `fstab` completo con radice, EFI e `/home` tutti per UUID, e il sistema che si avvia e aggiorna. Nessuna delle tre da sola basterebbe; insieme chiudono la questione.

*Il fatto che ritira una mia prescrizione.* La scheda prescriveva al passo 5 di eseguire `Check disc for defects` dal menu di avvio, e l'utente ha riferito che quella voce non gli veniva offerta. Non era una svista sua: sulle immagini recenti quella voce di menu non esiste più, perché il controllo di integrità del supporto viene eseguito automaticamente all'avvio. Il file `/var/log/installer/casper-md5check.json` ne conserva l'esito, ed è `{"checksum_missmatch": [], "result": "pass"}`, cioè il supporto è stato verificato e ha superato la verifica senza una sola somma discordante.

Ne discende un ritiro esplicito, e riguarda MS-069 oltre alla scheda. Quel microstep aveva rimosso dalla sottofase 2.4 il confronto di impronte, correttamente, ma lo aveva sostituito dichiarando il controllo dal menu di avvio *l'unica verifica autorevole del supporto*. Quella frase è sbagliata su questa immagine per due ragioni cumulative: il controllo non è raggiungibile dal menu, e non è l'unica verifica perché ne esiste una automatica il cui esito è leggibile in un file. La forma corretta della prescrizione non è un'azione dell'operatore ma una lettura a posteriori, cioè controllare `casper-md5check.json` dopo l'installazione.

Vale isolare l'errore di metodo perché è lo stesso di MS-016 e di MS-029. Ho descritto una interfaccia che non avevo osservato, deducendola da come funzionavano le immagini precedenti, e l'ho scritta su un foglio che qualcuno avrebbe seguito davanti alla macchina. Il costo qui è stato lieve, cioè un passo saltato e un dubbio sulla bontà del supporto durato un giorno, ma il presidio è lo stesso di sempre: una prescrizione su una interfaccia si verifica sull'interfaccia, e finché non lo è va marcata come non verificata.

Resta ignota la causa del blocco. Non è una lacuna che si chiude con una ipotesi: il log di dettaglio esiste, `subiquity-server-debug.log`, e va letto con privilegi prima di dichiarare qualunque cosa.

Esito: fatto per la diagnosi dei danni, aperto per la causa.

### MS-074 - Due difetti reali nell'installazione: la swap sul file sbagliato e i limiti realtime non applicati

Perimetro: sola lettura via SSH su `fstab`, `swapon`, `lsblk`, `/etc/security/limits.d/` e appartenenza ai gruppi.

Il primo difetto. L'installatore ha *ignorato la partizione di swap* `nvme0n1p3`, che esiste, è formattata e porta un UUID valido, e ha creato al suo posto un file `/swap.img` da 4 GB sulla radice. È la spiegazione della riga `Unchanged` accanto a `nvme0n1p3` nella schermata di riepilogo, che al momento era sembrata innocua. Le conseguenze sono due e nessuna è grave ma entrambe contraddicono una scelta di progetto: 14,9 GiB di disco restano inutilizzati, e la swap scende da 16 a 4 GB, il che rende impossibile l'ibernazione su una macchina con 16 GB di RAM, che era la ragione dichiarata per cui quella partizione era stata dimensionata pari alla memoria.

Il secondo difetto, e conta di più perché tocca lo scopo della macchina. I file in `/etc/security/limits.d/` concedono `rtprio 95` e `memlock unlimited` ai gruppi `@audio` e `@pipewire`, e Ubuntu Studio li installa da sé in `30-ubuntustudio-audio.conf`. L'utente però non appartiene a nessuno dei due: i suoi gruppi sono `adm cdrom sudo dip plugdev users lpadmin lxd`. I due gruppi esistono, `audio` con identificativo 29 e `pipewire` con 982, quindi non è un problema di configurazione ma di appartenenza. La conseguenza è misurabile e misurata: `ulimit -r` risponde `0` e la memoria bloccabile è 8192 kB, cioè i limiti realtime *non sono in vigore*.

Vale notare come il difetto sarebbe passato inosservato. La verifica prescritta dalla scheda è leggere i valori in `/etc/security/limits.d/`, e quei valori sono giusti: chi si fermasse lì concluderebbe che la catena è configurata. Solo il confronto fra ciò che il file concede e ciò che `ulimit` riporta davvero mostra che il permesso non arriva all'utente. È la stessa differenza fra una regola scritta e una regola in vigore che aveva già prodotto un falso negativo nella fase 6, dove il controllo sul nome del kernel avrebbe bocciato una catena funzionante.

Non verificabile adesso: la Scarlett 2i2 non è collegata al bus USB, quindi `aplay -l` vede la sola scheda integrata `ALC887-VD`. La verifica dell'interfaccia va rifatta con il dispositivo attaccato, e finché non lo è resta non osservata invece che assente.

Esito: fatto per la diagnosi, aperto per la correzione, che è privilegiata e quindi dell'utente.

### MS-075 - I parametri di avvio arrivano da un file che la scheda non nominava

Perimetro: `/proc/cmdline`, `/etc/default/grub`, `/etc/default/grub.d/`, `/etc/update-manager/release-upgrades`.

La catena a bassa latenza è attiva: `/proc/cmdline` contiene `preempt=full threadirqs rcu_nocbs=all`. Ma `/etc/default/grub` contiene soltanto `GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"`, quindi quei parametri non vengono da lì: vengono da `/etc/default/grub.d/ubuntustudio.cfg`, un file che il sistema installa da sé e che estende la variabile invece di sostituirla.

La conseguenza è una correzione della scheda e della fase 6 della procedura, entrambe le quali prescrivevano di aggiungere i due parametri a mano in `/etc/default/grub`. Seguire quella istruzione oggi non romperebbe nulla di visibile ma li duplicherebbe sulla riga di comando del kernel, il che è il genere di configurazione che confonde chi la legge sei mesi dopo e non sa più quale delle due sorgenti comanda. La forma corretta della prescrizione è verificare `/proc/cmdline`, e intervenire soltanto se i parametri mancano.

Nella stessa famiglia cade un secondo passo di igiene. La scheda prescriveva di impostare `Prompt=lts` in `/etc/update-manager/release-upgrades` con un comando `sed`, e quel file *contiene già* `Prompt=lts` su una installazione LTS pulita. Il comando non farebbe danno ed è una non-operazione, ma una scheda che prescrive passi già compiuti insegna a eseguirla senza leggerla, che è il difetto peggiore che possa avere un foglio da seguire davanti a una macchina.

Confermato invece che i codec proprietari sono installati, con `ubuntu-restricted-addons` in stato `ii`: la scelta fatta nell'installatore è stata onorata, il che restringe ulteriormente ciò che il blocco può aver impedito.

Esito: fatto.

### MS-076 - La causa del blocco: l'installazione era già finita, e la schermata mentiva

Perimetro: lettura dei log raccolti in `~/diag/` sulla macchina. Chiude la parte che MS-073 aveva lasciato aperta.

MS-073 aveva stabilito che il riavvio forzato non avesse lasciato danni, e aveva dichiarato aperta la sola domanda residua, cioè che cosa avesse tenuto appeso l'installatore per sedici ore. I log raccolti rispondono, e la risposta ribalta la lettura che l'esperienza dell'utente suggeriva.

L'installazione era finita. Alle 17:50:38 il log registra `finish: subiquity/Install/install/postinstall: SUCCESS: final system configuration`, alle 17:50:40 lo stato dichiarato dall'installatore passa a `DONE`, e subito dopo comincia la fase di chiusura, cioè la copia dei log nel sistema installato. L'utente ha lasciato la macchina alle 18 con la schermata ferma su `Setting up the system`: quella schermata, in quel momento, non descriveva più alcun lavoro in corso.

Sugli orari va dichiarata una avvertenza di lettura, perché altrimenti i numeri sembrano incoerenti e si sospetta un errore dove non c'è. I timestamp dentro i file di log sono in UTC, mentre le date di modifica degli stessi file sono in ora locale CEST, cioè due ore avanti. Le 15:50 del contenuto e le 17:50 dei metadati sono lo stesso istante.

Un limite dell'evidenza va enunciato prima delle conclusioni, perché è strutturale e non un difetto della raccolta. La copia del log che si legge nel sistema installato termina nell'istante in cui viene copiata, dato che sta copiando se stessa: per costruzione non può contenere ciò che è avvenuto dopo. Le ultime righe mostrano l'`rsync` verso `/target/var/log/installer` concluso con successo e la cattura del journal avviata. Ne segue che si può affermare con certezza dove il blocco *non* è, cioè in nessuna delle fasi di installazione, e non si può nominare con certezza dove sia.

Due anomalie sono registrate proprio in coda e sono compatibili con uno stallo nella chiusura, e vanno riportate come indizi e non come causa. La prima è `failed to rmdir /target/cdrom: [Errno 16] Device or resource busy`, cioè il supporto di installazione ancora occupato al momento di rimuovere il punto di montaggio dentro il sistema appena installato. La seconda è `ERROR telemetry: Failed to write report to /var/log/installer/telemetry (Cannot open file)`. Nessuna delle due è dimostrata come causa del blocco, e affermarlo sarebbe esattamente il tipo di promozione da indizio a fatto che questo progetto ha già pagato tre volte.

La regola operativa che ne discende è il guadagno vero di questa vicenda, ed è generale. La schermata di avanzamento di un installatore non è l'autorità sullo stato dell'installazione: l'autorità è lo stato che l'installatore dichiara, ed è consultabile dal vivo aprendo il registro dall'icona a forma di terminale in basso a destra nella finestra. Sedici ore di attesa sono state il costo di non aver guardato lì, e la lettura del registro sarebbe costata due minuti. Ne segue anche che il riavvio forzato è stato, in retrospettiva, l'azione corretta: attendere di più non avrebbe cambiato nulla, e il timore che avesse interrotto qualcosa di essenziale era infondato.

Un esito secondario chiude un dubbio rimasto dal giorno prima. Il supporto di installazione era stato verificato: `casper-md5check.json` riporta `{"checksum_missmatch": [], "result": "pass"}`. La verifica automatica ha quindi coperto il presidio che la scheda prescriveva come azione manuale e che non era eseguibile, e il sospetto sulla chiavetta cade.

Verificato con: lettura di `~/diag/subiquity-tail.txt` e `~/diag/installer-journal-tail.txt`, entrambi raccolti sulla macchina con `sudo tail` e redirezione verso la cartella dell'utente, più la rilettura di `casper-md5check.json` e di `curtin-install.log`.

Esito: fatto. La causa prossima resta non nominata per assenza di evidenza, e questa assenza è dichiarata invece di essere colmata per ipotesi.

### MS-077 - Tre correzioni applicate alla macchina, con il presidio di ciascuna

Perimetro: gruppi dell'utente, `/etc/fstab`, target di sospensione di systemd. Comandi preparati dall'agente ed eseguiti a mano dall'utente, come prescrive la scelta sul lavoro privilegiato.

I tre difetti trovati in MS-074 e MS-075 sono stati corretti in una sola tornata, con la raccolta diagnostica in sola lettura eseguita per prima di proposito: se una correzione fosse andata male su una macchina non presidiata, le prove sarebbero già state al sicuro.

La prima correzione riguarda i limiti realtime, e il difetto era di appartenenza e non di configurazione. I file sotto `/etc/security/limits.d/` concedono `rtprio 95` e `memlock unlimited` ai gruppi `audio` e `pipewire`, che esistono, ma l'utente creato dall'installatore non apparteneva a nessuno dei due.

```bash
sudo usermod -aG audio,pipewire alesop95 && id -nG alesop95
```

La verifica ha richiesto un accorgimento che vale registrare, perché la forma ingenua darebbe un falso negativo. L'appartenenza a un gruppo si applica al login e non alla sessione in corso, quindi controllare `ulimit` nella stessa shell risponderebbe con i valori vecchi. Avviare una sessione di login nuova permette di verificare senza riavviare la macchina.

```bash
sudo -u alesop95 -i bash -c 'id -nG; echo "rtprio: $(ulimit -r)"; echo "memlock: $(ulimit -l)"'
```

L'esito è `rtprio: 95` e `memlock: unlimited`, quindi i limiti risultano in vigore. È migliore dell'atteso: era stato dichiarato che non tutte le configurazioni applicano i limiti a una sessione avviata in questo modo, e la prova definitiva restava un riaccesso vero. Qui la prova è arrivata subito.

La seconda correzione riguarda la swap, che l'installatore aveva collocato su un file da 4 GB sulla radice ignorando la partizione dedicata da 14,9 GiB.

```bash
sudo cp /etc/fstab /etc/fstab.bak-$(date +%F-%H%M) && ls -la /etc/fstab.bak-*
```

```bash
sudo sed -i 's|^/swap.img.*|UUID=50a4c66e-60a4-41a5-8587-e6768b87b7ac none swap sw,nofail 0 0|' /etc/fstab && grep -n swap /etc/fstab
```

Due scelte dentro questo comando vanno spiegate perché non sono cosmetiche. La partizione è indicata per UUID e non per nome di dispositivo, perché un nome come `/dev/nvme0n1p3` dipende dall'ordine di enumerazione del kernel mentre un UUID è una proprietà del filesystem, ed è la stessa forma con cui l'installatore ha scritto tutte le altre voci del file. Le opzioni portano poi `nofail`, che è una rete di sicurezza sul solo rischio reale di questa modifica: senza quella parola un UUID sbagliato costerebbe un avvio bloccato in attesa di un dispositivo inesistente, mentre con essa il sistema si avvia senza swap e il difetto si scopre a freddo. La precauzione era necessaria perché la modifica è stata applicata pochi minuti prima di lasciare la macchina non presidiata.

```bash
sudo swapoff /swap.img && sudo swapon -a && swapon --show && free -h | head -3
```

```bash
swapon --show | grep -q /dev/nvme0n1p3 && sudo rm -f /swap.img && echo "FILE RIMOSSO, swap sulla partizione" || echo "NON RIMOSSO: la partizione non risulta attiva, fermati e dimmelo"
```

L'ordine dei due comandi è il presidio, e la condizione dell'ultimo non è pignoleria. La cancellazione del file è subordinata alla presenza effettiva della partizione nell'output di `swapon --show`, non all'assenza di errori nei comandi precedenti: cancellare prima di aver visto la partizione attiva avrebbe potuto lasciare il sistema senza alcuna swap. L'esito osservato è `/dev/nvme0n1p3`, tipo `partition`, 14,9 GiB, con `free -h` che riporta 14 GiB di swap totale, e il file è stato rimosso.

La terza correzione riguarda la sospensione automatica, tornata attiva perché il sistema è nuovo. Non è un fastidio: è il difetto che ha reso la macchina invisibile alla rete in due sessioni precedenti, e la sua conseguenza è la perdita dell'accesso remoto mentre nessuno è davanti alla macchina.

```bash
sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
```

La forma scelta è più radicale dell'impostazione grafica dell'ambiente desktop, perché impedisce anche la sospensione manuale, e la scelta è deliberata su una macchina che deve restare raggiungibile e che non ha vincoli di risparmio energetico da rispettare. È reversibile con `unmask` sugli stessi quattro bersagli. Il comando di verifica risponde `masked` quattro volte e con codice di uscita diverso da zero, che è la risposta corretta e non un errore, ed è stato dichiarato in anticipo per evitare che l'utente lo leggesse come un fallimento.

Sulla raccolta diagnostica vale una nota tecnica, perché la forma usata non è ovvia e la forma ovvia non avrebbe funzionato. I log dell'installatore richiedono privilegi in lettura, ma la redirezione verso `~/diag/` è eseguita dalla shell dell'utente e non da `sudo`, quindi i file prodotti appartengono all'utente e restano leggibili da remoto senza elevazione. Un `sudo cp` avrebbe prodotto file di `root`, e sarebbe servito un secondo comando per cambiarne il proprietario.

Esito: fatto, tutte e tre verificate sull'output dei comandi e non sul loro codice di uscita.

### MS-078 - Il grassetto nella prosa: una convenzione dichiarata e mai verificata

Perimetro: nuovo strumento `tools/fix-emphasis.py`, sedici file di documentazione, `.claude/context/STACK.md`.

Su richiesta dell'utente la documentazione del progetto è stata riportata allo stile prescritto dal template `template-claude-developing`. La sezione 8 del suo `PROJECT-SYSTEM.md` vieta nella prosa gli elenchi puntati, le emoji e il grassetto, prescrive il corsivo per i termini chiave densi e le note a piè di pagina numerate per gli acronimi. Il divieto sul grassetto era dichiarato anche nella regola `interaction-style.md` di questo progetto, e non era rispettato in nessun punto della documentazione scritta nelle sessioni precedenti.

La misura prima dell'intervento: 582 marcature in grassetto nei file tracciati. Il numero da correggere era però molto minore, 213, e la differenza è istruttiva perché distingue una violazione da un uso legittimo. Il divieto riguarda la prosa: dentro una tabella il grassetto non è discorso ma segnaletica, e nella scheda di reinstallazione la parola che dice di non formattare una partizione è in grassetto di proposito, quindi togliere quel risalto peggiorerebbe un documento di sicurezza. Dentro un blocco recintato il grassetto non è formattazione ma testo, e riscriverlo cambierebbe un comando. E la stessa sezione 8 prescrive il grassetto per le keyword di codice nei blocchi sintattici. Delle 582 marcature, 289 stanno nei modelli sotto `.claude/templates/`, che sono copie del template e la cui correzione appartiene a PA-003, e il resto si divide fra prosa da correggere e tabelle da lasciare.

La correzione è stata affidata a uno strumento e non fatta a mano, per la stessa ragione per cui esistono `fix-accents.py` e `fix-dashes.py`: una convenzione attuata a mano deriva di nuovo alla sessione successiva, ed è precisamente ciò che era accaduto qui. `tools/fix-emphasis.py` percorre i file Markdown riga per riga, salta i blocchi recintati e indentati con lo stesso contratto di `md-unwrap`, salta le righe di tabella e i loro separatori, e converte il resto da doppio a singolo asterisco. Conserva la fine riga di ciascun file, `CRLF` o `LF`, leggendo con `newline` vuoto e riscrivendo nella convenzione trovata. Ha una modalità `--check` non distruttiva che esce con codice diverso da zero, così da poter entrare nella sequenza di verifica prima di un commit, e una `--dettaglio` che mostra ogni riga prima e dopo.

Esito: 213 occorrenze convertite in sedici file, con il controllo che torna a zero. La sequenza di verifica completa passa dopo l'intervento, e in particolare `md-unwrap --check` con l'oracolo di rendering attivo non segnala alcun file il cui rendering sia cambiato in modo illecito.

Una nota di metodo che vale più del conteggio. Il grassetto era stato usato per anni in questo progetto come marcatore di enfasi nei microstep, cioè proprio nel documento che registra le violazioni delle convenzioni altrui: è il caso limite di una regola che si applica a tutti tranne che a chi la scrive. La ragione per cui è sopravvissuto tanto è la stessa che questo progetto ha già isolato tre volte, cioè che una convenzione senza strumento è un'intenzione. Le convenzioni che qui hanno resistito, come la riga sorgente unica per paragrafo e gli accenti veri, sono esattamente quelle che avevano uno strumento.

Esito: fatto.

### MS-079 - Un segnalibro promosso a inventario: la Scarlett 2i2 non appartiene a questo progetto

Perimetro: `docs/10-ambiente/README.md`, `docs/20-misura-stanza.md`, `docs/90-riferimenti/inventario-software.md`, `docs/10-ambiente/installazione-pulita-26-04.md` in sei punti, `docs/10-ambiente/setup-macchina-2026-09.md`, `docs/10-ambiente/scheda-reinstallazione.md`, `docs/10-ambiente/wine-corredo-progetto-stanza.md`, `docs/10-ambiente/wine-vs-emulatore.md`, `.claude/context/STACK.md`, `.claude/context/current-work.md`.

L'utente ha corretto una mia richiesta, cioè quella di collegare la Focusrite Scarlett 2i2 per completare la fase 6, dicendo di non aver mai dichiarato di doverla collegare. Aveva ragione, e la responsabilità non è della sua memoria ma della documentazione: più pagine di questo progetto dichiaravano quella interfaccia come hardware della macchina, al presente e come dato di fatto.

La fonte di quella affermazione è stata isolata, ed è istruttiva. Alla radice del repository viveva un file di testo, `focusrite.txt`, che conteneva una sola riga: l'indirizzo della pagina di download dei driver della Scarlett 2i2 di seconda generazione. Da un segnalibro il documento sorgente aveva ricavato un possesso, e da un possesso quattro pagine avevano ricavato una catena di misura. L'utente ha chiarito il 2026-09-09 di possedere quella interfaccia ma di non impiegarla in questo progetto, quindi il fatto hardware esiste e la sua appartenenza a questa catena no.

Va detto che il progetto aveva la prova della contraddizione da due giorni e non l'aveva risolta. La fotografia del 2026-09-07 registrava correttamente che `lsusb` non riportava alcun dispositivo Focusrite e che le sole schede viste erano l'audio integrato `ALC887-VD` con le sue uscite HDMI, e la verifica del 2026-09-09 lo ha confermato sul sistema nuovo. Ma quella osservazione era stata letta come *interfaccia presente e staccata* invece di *interfaccia assente*, perché altre pagine dichiaravano il possesso, e una osservazione che contraddice una affermazione dichiarata come fatto tende a essere interpretata come un caso particolare di quel fatto. È lo stesso meccanismo di MS-029, dove una diagnosi elaborata poggiava su una premessa implicita nella domanda: qui la premessa era implicita nell'inventario.

La conseguenza a valle è la parte che conta più della correzione, e riguarda `docs/20-misura-stanza.md`. Quella pagina non nominava la Scarlett di passaggio: la usava come premessa per decidere la scelta del microfono di misura, concludendo che un microfono XLR calibrato individualmente battesse l'UMIK-1 perché sfruttava una interfaccia già disponibile, e dichiarando esplicitamente che su una macchina senza interfaccia l'UMIK-1 sarebbe stato la scelta giusta senza discussione. Ritirata la premessa, quella conclusione si rovescia.

La forma in cui è stata riscritta è condizionale e non assertiva, perché è così che stanno le cose: l'utente ha fissato il 2026-09-09 due vincoli sull'interfaccia da acquisire per l'home recording, cioè che sia un dispositivo di classe audio riconosciuto dal kernel senza driver proprietari e che regga anche le misure di questo progetto. Sotto quel vincolo l'interfaccia ci sarà, e la conclusione a favore dell'XLR tiene. Se quell'acquisto non avvenisse, l'UMIK-1 tornerebbe a vincere. Ne segue una dipendenza di ordine che prima non era scritta da nessuna parte: la decisione sul microfono non si prende prima di quella sull'interfaccia.

Tutte le occorrenze sono state riscritte con il ritiro dichiarato invece di far sparire la frase, secondo la regola del progetto per cui una inferenza smentita si ritira esplicitamente e non si cancella in silenzio. I controlli operativi che nominavano l'interfaccia come bersaglio, cioè il controllo di uscita della fase 6 e la verifica della scheda di stampa, sono stati riscritti sui dispositivi effettivamente presenti, con l'avvertenza sui limiti realtime che vanno letti con `ulimit` e non nei file di configurazione.

Verificato con: ricerca di ogni occorrenza della stringa in `docs/` e `.claude/`, riscrittura di ciascuna e nuova ricerca a valle, che lascia soltanto le occorrenze che dichiarano il ritiro o che appartengono al registro dei microstep e al work-log, dove sono voci storiche.

Esito: fatto per la documentazione, aperto come decisione di acquisto, tracciata in PA-012.

### MS-080 - La radice del repository contiene ora soltanto ciò che è tracciato

Perimetro: cinque file di testo spostati da `/` a `_notes/materiale-radice/`, con una pagina di archivio che dichiara che cos'era ciascuno.

La radice portava cinque file di testo scritti a mano più due cartelle di materiale pesante, e nessuno dei file era versionato, dato che il `.gitignore` esclude alla radice i tipi di file di testo con pattern ancorati. Lo spostamento non ha quindi alcun effetto sulla storia di git: il guadagno è che la radice contiene ora soltanto `.gitignore`, `CLAUDE.md` e `README.md` più le cartelle del progetto, così che ciò che si vede aprendo il repository sia ciò che il repository contiene.

Il controllo che ha reso l'operazione sicura è stato verificare che nessuno dei cinque portasse informazione unica, e il risultato è che nessuno la portava. I tre file che contenevano un solo indirizzo ciascuno, cioè la pagina di download dei driver Focusrite, il forum Audio Science Review e l'elenco di strumenti di progettazione di diffusori di diyAudio, erano tutti e tre già registrati in `docs/90-riferimenti/fonti.md`. L'albero testuale del pacchetto software di terze parti era già censito voce per voce in `docs/90-riferimenti/censimento-corredo.md`, con il confronto fra le cartelle dichiarate e quelle realmente presenti. La descrizione sintetica del progetto in una riga di composizione tipografica non era citata da alcun documento, ed è materiale personale da portfolio: resta archiviata, con la nota che il suo testo dichiara Ubuntu Studio 25.04 e va aggiornato se riusato.

Sono stati spostati e non cancellati, e la ragione è la stessa per cui il documento sorgente `.docx` fu archiviato invece di distrutto: il costo di conservare quaranta kilobyte è nullo, mentre il costo di scoprire fra sei mesi che uno di quei file conteneva una riga non registrata altrove non lo è. La cartella porta un proprio `README.md` che dichiara che cos'era ciascun file e dove vive adesso il suo contenuto.

Non è stata spostata la cartella `Akabak + VACS/`, 159 MB e sette file, e la decisione è dell'utente. Il suo contenuto è stato verificato identico per impronta SHA-256 a quello sulla macchina sotto `~/electroacoustics`, con corrispondenza uno a uno di tutti e sette i file: i due installer di VACS e quello di AKABAK in `installers/`, l'archivio di esempi in `examples/`, e la licenza in PDF, lo screenshot dell'aggiornamento e il collegamento al sito dell'autore in `licenze/`. Le dimensioni indicavano 159 MB contro 158, differenza di arrotondamento del filesystem e non un file mancante, e il criterio che decide resta l'impronta del contenuto per la lezione di MS-024.

La cancellazione sarebbe quindi priva di perdita di dati, e non è stata fatta per una ragione che riguarda il rischio e non il contenuto: la macchina non ha ancora un backup, quindi cancellare adesso lascerebbe l'unica copia di quel materiale su un disco che porta ventiquattro spegnimenti non puliti in archivio. L'operazione è subordinata alla chiusura di PA-011.

Verificato con: `sha256sum` sui sette file locali e `find` con `sha256sum` sui file corrispondenti della macchina, con confronto delle impronte ordinate; elenco della radice dopo lo spostamento, che riporta i soli tre file tracciati.

Esito: fatto per i cinque file sciolti, subordinato a PA-011 per la cartella pesante.

### MS-081 - Il pacchetto prescritto non esiste, e la verifica è costata un comando

Perimetro: `docs/10-ambiente/installazione-pulita-26-04.md` alla fase 7, `docs/10-ambiente/scheda-reinstallazione.md`, `docs/10-ambiente/wine-configurazione.md`.

Prima di consegnare all'utente i comandi della fase 7 ho verificato sulla macchina che i pacchetti prescritti esistano, e uno non esiste. La procedura, la scheda di stampa e la pagina di configurazione di Wine prescrivevano tutte `sudo apt install --install-recommends wine-stable winetricks`, e su Ubuntu 26.04 `apt-cache policy wine-stable` risponde `Candidate: (none)`.

La causa è che quel nome appartiene ai repository WineHQ, non all'archivio Ubuntu. Il sistema precedente aveva due repository WineHQ attivi contemporaneamente per due rilasci diversi, che era uno dei fattori di attrito che hanno motivato l'installazione pulita, e la prescrizione era stata scritta guardando quello che c'era su quella macchina invece dell'archivio della distribuzione che si sarebbe installata. Il pacchetto corretto si chiama `wine`, versione `10.0~repack-12ubuntu1`, e `winetricks` esiste con quel nome.

Il controllo ha prodotto anche una conferma non cercata, e vale registrarla perché è la prova pratica di una decisione presa su base documentale. `apt-cache policy wine32` risponde `Candidate: (none)` mentre `wine64` risponde con la versione: `wine32` non è disponibile perché l'architettura `i386` non è ancora dichiarata sul sistema. È esattamente il meccanismo per cui ADR-016 impone di dichiarare `i386` prima di installare Wine e non dopo, e finora quell'ordine era sostenuto dal ragionamento e da un prefix osservato, non da una misura sul sistema nuovo.

La nota di metodo è che questo è il terzo caso in tre giorni della stessa classe di difetto, dopo la voce `Check disc for defects` che non esiste nel menu di avvio in MS-073 e i parametri di avvio attribuiti al file sbagliato in MS-075. La forma comune è una prescrizione operativa scritta guardando un ambiente diverso da quello su cui verrà eseguita, e il presidio che l'ha intercettata questa volta è banale: prima di consegnare un comando, verificarlo dove verrà eseguito. Il costo era un comando di sola lettura.

Verificato con: `apt-cache policy` su sei nomi di pacchetto candidati, eseguito via SSH sulla macchina, che ha risposto `(none)` per `wine-stable` e per `wine32`, con la versione per `wine`, `wine64` e `winetricks`, e nessun pacchetto per `wine-installer`.

Esito: fatto. Le tre pagine prescrivono ora `wine`, con la nota che spiega perché il nome precedente non esiste e da dove veniva.

### MS-082 - `--install-recommends wine` non installa `wine32`, ed è il difetto che ADR-016 doveva prevenire

Perimetro: diagnosi sull'installazione di Wine eseguita dall'utente il 2026-09-09; correzione da applicare a `docs/10-ambiente/installazione-pulita-26-04.md` alla fase 7, alla scheda di stampa e a `docs/10-ambiente/wine-configurazione.md`.

L'utente ha eseguito la fase 7 nell'ordine prescritto: `dpkg --add-architecture i386`, poi `apt update`, poi `apt install --install-recommends wine winetricks`. I primi due passi hanno funzionato, e la prova è che `apt update` ha scaricato gli indici `i386` di tutti i componenti e che `apt-cache policy wine32:i386` è passato da `Candidate: (none)` a `Candidate: 10.0~repack-12ubuntu1`. Il terzo ha installato undici pacchetti e Wine risponde `wine-10.0`.

Il difetto sta in che cosa non ha installato. Nell'elenco dei pacchetti tirati dentro compaiono `wine64`, `libwine`, `wine-common` e le librerie di supporto, mentre `wine32` compare nella sezione dei pacchetti *suggeriti* e non fra quelli installati. La verifica successiva lo conferma senza margini: `dpkg -l wine32:i386` e `apt-cache policy wine32:i386` riportano `Installed: (none)`, e la cartella `/usr/lib/wine/` non contiene alcun binario a 32 bit.

La causa è una distinzione fra livelli di dipendenza di apt che la prescrizione ignorava. Il metapacchetto `wine` di Ubuntu *raccomanda* `wine64` e si limita a *suggerire* `wine32`, e l'opzione `--install-recommends` agisce sui raccomandati e non sui suggeriti. La prescrizione era quindi insufficiente per costruzione, indipendentemente dall'architettura dichiarata: dichiarare `i386` rende `wine32` installabile, non lo installa.

La gravità di questo caso è maggiore dei tre precedenti della stessa classe, e la ragione va detta. Akabak è `PE32 executable, Intel 80386`, cioè a 32 bit, e ADR-016 esiste proprio per questo: aveva ribaltato tre decisioni precedenti stabilendo che l'architettura `i386` va dichiarata e non evitata, perché senza di essa il solo software del progetto che funzionava non funzionerebbe più. Eseguendo la procedura come era scritta si otteneva un sistema con `i386` dichiarata, Wine installato, `wine --version` che risponde, e Akabak che non parte: cioè esattamente l'esito che quella decisione doveva prevenire, raggiunto attraverso un passo che sembrava eseguito correttamente. Un difetto che si manifesta come *il programma non parte* dopo che ogni comando ha risposto bene è il tipo più costoso da attribuire.

Vale isolare perché nessuno dei presidi esistenti lo ha intercettato. La procedura prescriveva l'ordine giusto e il controllo di uscita della fase 7 chiedeva `wine --version`, che risponde correttamente anche con il solo ramo a 64 bit. Il controllo era quindi soddisfatto da un sistema difettoso, ed è la terza volta in questo progetto che un controllo di uscita si rivela più debole di ciò che deve provare, dopo il nome del kernel in fase 6 e la lettura dei file di `limits.d` invece di `ulimit`. Il controllo corretto è l'installazione del pacchetto, cioè `dpkg -l wine32:i386`, oppure la creazione di un prefix a 32 bit, che senza quel pacchetto non riesce.

Verificato con: `dpkg -l wine32:i386` e `apt-cache policy wine32:i386`, entrambi `Installed: (none)`, ed elenco di `/usr/lib/wine/` senza binari a 32 bit. Da notare che `WINEARCH=win32 wine --version` risponde comunque con la versione e non è quindi un controllo valido: la versione si legge senza caricare il loader a 32 bit.

Esito: aperto. La diagnosi è chiusa, la correzione sulla macchina è un comando dell'utente, `sudo apt install wine32:i386`, e la riscrittura del controllo di uscita della fase 7 va fatta quando l'esito è noto.

### MS-083 - `wine32` installato, la scrivania separata dal magazzino, e due lanciatori rotti da mesi

Perimetro: installazione di `wine32:i386` sulla macchina, riorganizzazione di `~/Desktop`, nuova cartella `~/archivio` con la propria pagina di spiegazione, correzione dei due lanciatori. Chiude MS-082.

La correzione diagnosticata in MS-082 è stata applicata: `sudo apt install wine32:i386` ha tirato dentro 263 pacchetti per 250 MB scaricati e 1,1 GB occupati, e `dpkg -l wine32:i386` riporta ora `ii`. Il numero merita una nota perché spiega perché il pacchetto è soltanto suggerito e non raccomandato dal metapacchetto: il ramo a 32 bit non è un binario ma un intero albero di librerie parallelo, dalla `libc` fino a Mesa, GTK e GStreamer. Chi installa Wine per programmi a 64 bit non lo vuole, e chi ha bisogno di Akabak lo deve chiedere.

Sulla riorganizzazione della scrivania, l'esito della misura ha cambiato la proposta. La domanda dell'utente era se convenisse spostare la scrivania altrove per sfruttare tutto il materiale, e il presupposto implicito era che contenesse cose che al progetto servono. Il confronto per impronta lo smentisce: dei 647 valori distinti presenti sulla scrivania, 380 non esistono in `~/electroacoustics`, e la loro ripartizione dice che cosa sono. Trecentosessanta stanno in `DIY Loudspeaker Pack Softwares` e sono LSPCad 6.32 con 191 file, LSPCad 5.25 con 66, FineCone 2.1 con 63, FineMotor 2.5 con 38 e Grenander Loudspeaker Lab con 2, cioè esattamente le voci che ADR-010 ha escluso dal progetto. Sedici stanno in `Simulators` e sono AmpliTube 3, Guitar Rig 5 Pro e POD Farm, cioè simulatori di amplificatori per chitarra, che appartengono al dominio dell'home recording e non a questo. Il resto sono file sciolti.

Ne segue che dalla scrivania non andava spostato nulla dentro il progetto, perché l'albero curato contiene già tutto ciò che il progetto usa. Il problema era un altro, ed è quello che la riorganizzazione ha risolto: la scrivania faceva due lavori insieme, spazio di lavoro e magazzino da 2,3 GB, e questo rendeva impossibile vedere a occhio quale materiale fosse attivo.

La forma adottata separa i due lavori. Sulla scrivania restano i due lanciatori di AKABAK e VACS, la cartella dei progetti Ardour e il collegamento `Progetto-stanza` verso `~/electroacoustics`. Il magazzino è in `~/archivio`, con le tre cartelle grandi spostate integre e i file sciolti sotto `archivio/scrivania`. Le cartelle non sono state divise voce per voce di proposito: dividerle avrebbe richiesto una decisione per file e introdotto il rischio di perdere qualcosa, mentre spostarle intere è una operazione atomica e reversibile. La cartella porta un `LEGGIMI.md` che dichiara che cos'è ciascuna cosa e perché sta là, così che la scelta sopravviva a chi l'ha fatta.

Due file sciolti meritano una riga. I due programmi di installazione di AKABAK e VACS che stavano sulla scrivania sono identici per impronta a quelli in `~/electroacoustics/installers`, verificato prima di spostarli, quindi erano una copia e non un originale. E il file il cui nome è il codice di attivazione di Akabak, vuoto, che era già stato segnalato in MS-051: è stato spostato nell'archivio, ma la raccomandazione resta di cancellarlo, perché quel codice è conservato in modo riservato sulla postazione di sviluppo e averlo come nome di file su una scrivania non aggiunge nulla se non esposizione.

Il difetto trovato per strada è il più istruttivo, e non era stato cercato. I due lanciatori della scrivania invocano il programma con `wine-stable`, cioè il nome del binario dei repository WineHQ che il sistema precedente aveva attivi. Su questo sistema quel binario non esiste, quindi entrambi i lanciatori erano rotti e lo sarebbero stati anche senza alcuna riorganizzazione: chi li avesse cliccati avrebbe visto la finestra non aprirsi e nessun messaggio utile. Sono stati corretti a `wine`. Vale notare che questo è lo stesso nome che MS-081 aveva trovato sbagliato nella documentazione, quindi la stessa assunzione errata viveva in due posti indipendenti, un documento e un file di configurazione del desktop, e sarebbe stata scoperta due volte separatamente.

Verificato con: `dpkg -l wine32:i386` uguale a `ii`; confronto delle impronte dei due installer prima dello spostamento; elenco della scrivania dopo il riordino, che riporta cinque voci contro le sedici di prima; `du -sh` sull'archivio che riporta 1,6 GB, 563 MB, 117 MB e 51 MB nelle quattro sottocartelle; lettura dei due lanciatori corretti.

Esito: fatto. Resta da provare se il prefix `~/.wine` sopravvissuto funzioni con Wine 10, che è la prova che decide se la fase 8 si riduce a una verifica.

### MS-084 - Con wine32 e wine64 installati il comando `wine` sceglie sempre i 64 bit, e MS-083 conteneva una mia affermazione falsa

Perimetro: diagnosi del rifiuto di AKABAK ad avviarsi, lettura degli script di avvio di Wine sulla macchina, correzione dei due lanciatori della scrivania, correzione della fase 7 della procedura e della scheda di stampa. Supera una affermazione di MS-083.

Il primo avvio di AKABAK nel prefix sopravvissuto è fallito con un messaggio esplicito: `wine: '/home/alesop95/.wine' is a 32-bit installation, it cannot support 64-bit applications`. Il messaggio va letto al contrario di come si è tentati di leggerlo: non dice che il prefix sia difettoso, dice che il caricatore avviato era quello a 64 bit e che quel caricatore non lavora su un prefix a 32 bit.

La causa sta in come Ubuntu confeziona il comando. Il file `/usr/bin/wine` è un collegamento che attraverso il sistema delle alternative arriva a `/usr/bin/wine-stable`, che è uno script di poche righe. Quello script contiene la logica che decide: se `/usr/bin/wine64` è eseguibile lo usa e ne esporta il percorso in `WINELOADER`, e ripiega su `/usr/bin/wine32` soltanto se il primo manca. Con entrambi i rami installati, e ADR-016 impone di installarli entrambi, il caricatore a 32 bit non viene mai scelto. La via corretta è invocare `wine32`, che è anch'esso uno script e che esegue `/usr/lib/i386-linux-gnu/wine/wine`, cioè un binario `ELF 32-bit`; va notato che quello script imposta `WINEPREFIX` a `~/.wine32` se la variabile non è definita, quindi il prefix va sempre dichiarato esplicitamente.

Ne discende una prescrizione che la procedura non conteneva e che è il complemento operativo di ADR-016: dichiarare l'architettura e installare `wine32` rende possibile il prefix a 32 bit, ma per usarlo il comando deve essere `wine32` e non `wine`. Senza questa riga la decisione sui 32 bit resta corretta e inapplicabile.

*Il ritiro.* MS-083 afferma che i due lanciatori della scrivania fossero rotti perché invocavano `wine-stable`, un nome che su questo sistema non esisterebbe, e registra la loro correzione a `wine` come un difetto risolto. Quella affermazione è falsa e va ritirata per intero. Il file `/usr/bin/wine-stable` esiste, è installato dal pacchetto `wine`, ed è precisamente lo script a cui `/usr/bin/wine` rimanda: i due nomi sono lo stesso programma. I lanciatori non erano quindi rotti per quel motivo, e la mia correzione era una non-operazione.

Peggio: quella correzione lasciava intatto il difetto reale. Sia `wine` sia `wine-stable` finiscono nel caricatore a 64 bit, quindi entrambi i lanciatori avrebbero fallito sul prefix a 32 bit con lo stesso messaggio visto a riga di comando. Sono stati ora corretti a `wine32`, che è la forma che funziona.

La causa del mio errore va isolata perché è precisa e ripetibile. Avevo verificato l'inesistenza del *pacchetto* `wine-stable` con `apt-cache policy`, che è il controllo giusto per la riga di installazione corretta in MS-081, e ho trasferito quella conclusione al *binario* senza rifare il controllo. Sono due domande diverse con due strumenti diversi: `apt-cache policy` risponde sui pacchetti, `ls` e `command -v` rispondono sui file eseguibili. In Debian e Ubuntu la distinzione è tutt'altro che accademica, perché il sistema delle alternative fa esistere nomi di comando che non corrispondono ad alcun pacchetto omonimo. La regola operativa è che una conclusione ottenuta con uno strumento non si estende a un oggetto diverso senza rifare la misura, ed è la stessa che questo progetto ha già pagato tre volte in forma diversa.

Verificato con: lettura integrale di `/usr/bin/wine-stable` e `/usr/bin/wine32-stable`; elenco dei collegamenti in `/etc/alternatives/`, che mostra `wine` verso `wine-stable`; `file` sul caricatore a 32 bit, che risponde `ELF 32-bit LSB pie executable, Intel i386`; `WINEPREFIX=~/.wine wine32 --version`, che risponde `wine-10.0` senza errori contro il prefix a 32 bit; `grep` su `system.reg` del prefix, che dichiara `#arch=win32`; `file` su `AKABAK.exe`, che conferma `PE32 executable`.

Esito: fatto per la diagnosi e per i lanciatori, aperto per l'avvio effettivo del programma, che richiede una sessione grafica sulla macchina.

### MS-085 - La licenza è viva nel prefix sopravvissuto, e l'attivazione non stava dove l'avevo cercata

Perimetro: verifica dello stato della licenza di AKABAK nel prefix `~/.wine` dopo la reinstallazione, per due vie indipendenti; classificazione dell'output di avvio del programma; correzione delle fasi 8.1 e 8.2 della procedura e della scheda riservata. Chiude la fase 8.2 e riduce la fase 8 a una verifica.

La prima via è deterministica e non richiede una sessione grafica, ed è stata tentata per prima proprio per questo. La ricerca è partita dal registro del prefix, che è il posto dove ADR-019 dichiara che l'attivazione vive, e il registro non l'ha confermato: `grep` su `user.reg` e `system.reg` restituisce soltanto le voci di menu create dall'installer e le associazioni di tipo di file `RDTeam_AKABAK_Project` e `RDTeam_VACS_Form`, nessuna chiave di licenza. L'affermazione secondo cui l'attivazione starebbe nel registro va quindi corretta: sta in un file di configurazione, cioè `C:\ProgramData\RDTeam\Akabak.ini`, che porta una sezione `[Security]` con la voce `SecCode` e un `Username` vuoto. Accanto ad esso, `AppData\Local\RDTeam\Akabak.ini` contiene le sole preferenze di programma, fra cui `PrgVersion=3.2.4`, e nessun dato di licenza.

Il valore di `SecCode` coincide carattere per carattere con il Release Code permanente conservato nella scheda riservata sotto `_notes/`. Il confronto è stato fatto in sessione e il valore non entra qui: la regola è che quel codice non compare in alcun file tracciato, quindi si registra che i due valori coincidono e non i valori.

La collocazione del dato non è un dettaglio di curiosità e vale come regola operativa per il futuro. Una attivazione scritta in `ProgramData` è a livello di macchina e non di utente Windows, il che spiega perché sopravviva indenne alla migrazione del prefix da Wine 9 a Wine 10: la migrazione riscrive il registro e le librerie di sistema del prefix, non i file di dati sotto `drive_c`. E spiega anche perché cercarla nel registro sia stato tempo perso su una assunzione ragionevole ma sbagliata, cioè che un programma Windows conservi la licenza dove il sistema si aspetta che la conservi.

La seconda via è l'osservazione diretta, ed è servita perché l'esito del confronto sul file dice che il codice atteso è scritto, non che il programma lo consideri valido. L'utente ha aperto AKABAK con `WINEPREFIX=$HOME/.wine wine32 "C:/Program Files/RDTeam/AKABAK/AKABAK.exe"` e la voce `Release code` del menu di aiuto, e lo screenshot fornito porta quattro elementi: il campo `Your machine identifier` con `C937-FD3A`, il campo del release code compilato con il codice atteso, la dichiarazione `Release Code valid` con il semaforo verde, e la riga `Security key not connected to the USB port`.

L'esito è la quarta conferma indipendente della stessa affermazione, e la prima raccolta dopo la reinstallazione invece che prima. Le tre precedenti sono la corrispondenza del 13 agosto 2025, la lettura in interfaccia del 2026-09-07 di MS-052 e il confronto sul valore conservato; questa è l'unica che dimostra ciò che ADR-003 asseriva, cioè che una licenza legata alla macchina sopravvive alla reinstallazione del sistema. La fase 8.2 si chiude quindi senza reinserire nulla: non c'è alcun codice da digitare, perché quello valido è già al suo posto e il programma lo accetta.

Sulla riga `Security key not connected to the USB port` vale ripetere quanto MS-052 aveva già stabilito, perché a leggerla fuori contesto sembra un difetto: non è un errore da correggere ma la menzione dell'altro portatore possibile del diritto d'uso, cioè una chiave hardware, che questa licenza non usa. Diventerebbe rilevante nel solo caso che invaliderebbe il codice, cioè un cambio significativo di hardware che alterasse il Machine Identifier.

*L'output di avvio, e perché non è un guasto.* Il lancio ha stampato dodici righe di diagnostica, una sola delle quali è un errore e undici sono avvisi di funzione non implementata. Le undici hanno la forma `fixme` e riguardano stub dichiarati di Wine: la lingua dell'interfaccia con `GetThreadUILanguage` e `RtlGetThreadPreferredUILanguages`, la notifica di sessione con `WTSRegisterSessionNotification`, il disegno con doppio buffer di `uxtheme`, le informazioni di prestazione di `NtQuerySystemInformation`, la soppressione dell'effetto di finestra bloccata, e l'indicatore di avanzamento nella barra delle applicazioni. Wine le stampa per dichiarare che quella chiamata non è implementata e che l'esecuzione prosegue: non sono guasti, e il programma che si apre e mostra una finestra di licenza pienamente funzionante è la prova che nessuna di esse blocca. L'unica riga di errore è `err:setupapi:do_file_copyW Unsupported style(s) 0x10`, che riguarda un attributo non supportato in una operazione di copia file dell'installatore di componenti. Da verificare e non da assumere è la sua attribuzione: porta un identificativo di processo diverso da quello del programma principale, `00b8` contro `0024`, quindi appartiene con ogni probabilità a un processo di servizio del prefix e non ad AKABAK, ma questa è una inferenza dai numeri e non una misura.

*Un difetto trovato per strada, che apre il microstep successivo.* Le fasi 8.1 e 8.2 della procedura prescrivevano ancora `wine` come comando di avvio, e la stessa forma sbagliata viveva nella procedura di inserimento dentro la scheda riservata: ADR-019 aveva corretto la fase 7 e la scheda di stampa senza scendere alla fase 8. Il comando è stato corretto in entrambe. La constatazione che la stessa prescrizione sbagliata viva in più posti indipendenti non si chiude però correggendo i due che si sono incontrati, ed è il motivo per cui il censimento sistematico è diventato un microstep a sé: si veda MS-087, che ne ha trovate ventitré in sette pagine e ha corretto una affermazione di questa voce.

Verificato con: `grep` su `user.reg` e `system.reg` del prefix, che non contengono chiavi di licenza; `find` su `drive_c` per i file `.lic` e `.ini` di RDTeam, che ne individua tre; lettura di `ProgramData/RDTeam/Akabak.ini`, che porta `[Security]` con `SecCode`; confronto del valore con `_notes/licenze-akabak-riservato.md`, che coincide; `dpkg -l wine32:i386`, che risponde `ii` con la versione `10.0~repack-12ubuntu1`; `command -v wine32`, che risponde `/usr/bin/wine32`; elenco del contenuto di `C:\Program Files\RDTeam\AKABAK\`, che contiene `AKABAK.exe`; screenshot della finestra `Release code` fornito dall'utente.

Esito: fatto per la licenza, che è valida e non richiede reinserimento. Resta aperta l'edizione, che questa finestra non dichiara: la finestra di informazioni sul programma è l'unica a portarla, e va aperta per accertare la discrepanza fra `Standard Edition`, osservato il 2026-09-07 e su cui poggiano tre pagine, e `32 Professional`, letto nella barra del titolo il 2026-09-09.

### MS-086 - Tre elementi nuovi dichiarati dall'utente, e che cosa di essi è verificato

Perimetro: registrazione di tre informazioni portate dall'utente il 2026-09-10, con la separazione fra la parte verificata e quella riferita. Nessun intervento sul sistema.

*Il controller MIDI.* L'utente dichiara di possedere un Nektar Impact GX49 e di averne collaudato la connessione sulla macchina, con esito positivo. Il collaudo, però, appartiene al sistema precedente, che la reinstallazione dell'8 settembre ha azzerato nella sua radice, quindi la dichiarazione non si estende al sistema attuale e non va promossa a fatto su di esso. La misura fatta oggi dice due cose distinte. Il dispositivo non è collegato adesso: `lsusb` non ha corrispondenze per Nektar, `amidi -l` restituisce una tabella vuota, e `aconnect -l` elenca soltanto i client di sistema, cioè `Midi Through` e i due client di PipeWire. Lo strato MIDI del sistema, invece, è presente e attivo: PipeWire espone i propri client come `UMP-MIDI2`, che è il protocollo MIDI 2.0, quindi non manca nulla da installare e il collaudo consiste nel collegare il dispositivo e rifare le tre letture. Nella stessa lettura `/proc/asound/cards` riporta la sola scheda `HDA Intel PCH`, che è una conferma indipendente di MS-079: nessuna interfaccia audio esterna è presente su questa macchina.

Il ruolo del controller nel progetto va delimitato, perché è facile sopravvalutarlo. Un controller MIDI a tastiera non entra nella catena di misura né in quella di simulazione: non produce suono da sé, non misura nulla, e la progettazione dei monitor non lo impiega in alcuna delle otto fasi del flusso. È invece hardware pertinente al progetto gemello di home recording, dove serve come dispositivo di ingresso per gli strumenti virtuali. Va quindi inventariato come hardware presente sulla macchina condivisa, che è un fatto utile a entrambi i progetti, senza essere aggiunto al flusso di questo.

*Il backup di macchina intera.* L'utente conferma l'intenzione di prendere un backup completo con Veeam a setup finito, che è esattamente PA-011 e non una voce nuova, e aggiunge di avere già sperimentato Veeam da Ubuntu nel progetto `home-lab-cybersec-networking`. Quest'ultima affermazione va messa accanto all'accertamento del 2026-09-09 registrato in PA-011, perché le due non coincidono: quella ricerca aveva trovato in quel progetto una sola pagina di strategia di backup, `01-veeam-agent-for-windows.md`, e nessuna occorrenza di `linux` o `ubuntu` nel blocco. Le due affermazioni si conciliano in due modi diversi che hanno conseguenze diverse, quindi la discrepanza si dichiara invece di essere risolta a favore di una delle due. Se l'esperimento su Linux è stato eseguito e non documentato, allora esiste esperienza riutilizzabile che va recuperata dalla memoria dell'utente o dalla macchina dove girava, e la sua assenza in quel repository è un difetto di tracciamento di quel progetto. Se invece l'esperimento riguardava l'agente per Windows, come la sola pagina esistente suggerisce, allora l'agente per Linux resta da documentare da zero e la conclusione di PA-011 non cambia. La verifica costa poco e va fatta quando PA-011 si sblocca, non adesso.

*La replica del setup sul portatile.* L'utente indica come direzione futura, dichiarata non urgente, la replica dello stesso setup di Ubuntu Studio sul secondo portatile, un Asus F550CC-XX698H oggi su Ubuntu 24.04 LTS. La richiesta esplicita è di collocarla in roadmap e non nel lavoro corrente, ed è così che è stata trattata: la scheda della macchina e la valutazione di fattibilità stanno in `.claude/context/roadmap.md`, dove vive la direzione, e non in `current-work.md`, che descrive il fronte attivo.

### MS-087 - Il censimento del comando sbagliato: ventitré occorrenze in sette pagine, e `winecfg` non poteva creare il prefix

Perimetro: censimento con `grep` di tutte le invocazioni di Wine su prefix a 32 bit nel blocco `docs/10-ambiente/`, correzione delle ventitré trovate, lettura degli script `winecfg-stable`, `wineboot-stable` e `winetricks` sulla macchina. Discende dalla lezione di MS-085 e ne corregge una affermazione.

*La correzione di MS-085.* Quella voce dichiara che le fasi 8.1 e 8.2 sono state corrette a `wine32` con il prefix `~/.wine`. La prima metà è vera, la seconda no, e la distinzione conta perché confonde due cose diverse. Il comando era sbagliato in senso assoluto, e va corretto sempre. Il prefix `~/wineprefixes/akabak32` che quelle sottofasi nominano non è invece sbagliato: è il prefix che una ricostruzione da zero creerebbe, ed è la scelta giusta per lo scenario che quelle sottofasi descrivono, cioè la perdita di `/home` o una macchina diversa. Il prefix `~/.wine` è quello operativo su questa macchina, ed è un fatto sullo stato attuale, non una prescrizione della procedura. Le sottofasi conservano quindi il proprio prefix e portano una premessa nuova che dichiara i due scenari, mentre il comando è corretto in entrambi.

*Che cosa ha trovato il censimento.* La ricerca ha separato le invocazioni per architettura del prefix di destinazione, che è il criterio corretto perché su un prefix a 64 bit il comando `wine` è giusto e non va toccato. Sui prefix a 32 bit ha trovato ventitré comandi sbagliati in sette pagine, di tre forme diverse. Dieci erano avvii di programma con `wine` invece di `wine32`. Nove erano creazioni o aperture del prefix con `winecfg`. Quattro erano installazioni di dipendenze con `winetricks`. Nessuna invocazione su prefix a 64 bit è stata modificata, e la verifica di non contaminazione è stata eseguita con una ricerca dedicata dopo la correzione.

*Il difetto più grave del gruppo, e non era cercato.* Le nove occorrenze di `winecfg` sono peggiori delle dieci di `wine`, perché stanno nel passo che crea il prefix e non in quello che lo usa. Il file `/usr/bin/winecfg` è un collegamento che arriva a `/usr/bin/winecfg-stable`, che è uno script di cinque righe il cui contenuto è una sola istruzione: ricava il nome del programma dal proprio nome ed esegue `wine-stable`. Non consulta né `WINEARCH` né `WINEPREFIX`, quindi il comando `WINEARCH=win32 WINEPREFIX=... winecfg`, che la procedura prescriveva per creare il prefix di Akabak, finisce nel caricatore a 64 bit esattamente come `wine`. La conseguenza è che il primo comando della fase 7, quello che avrebbe dovuto creare il prefix a 32 bit, non poteva riuscire. Lo stesso vale per `wineboot`, il cui script è identico riga per riga. La forma corretta è passare il programma al caricatore giusto, cioè `wine32 winecfg`, e la prova è che quel comando risponde con esito zero e stampa la lista delle versioni di Windows disponibili, mentre il caricatore a 64 bit sul prefix a 32 bit rifiuta di partire.

Vale registrare come questo difetto è sopravvissuto a due correzioni precedenti, perché il modo è istruttivo. ADR-019 enuncia il principio nella sua forma generale, cioè che la prescrizione vale anche per `winecfg`, `wineboot` e `winetricks` perché tutti passano dal medesimo wrapper. Il principio era corretto e completo; ciò che non fu fatto è scendere dai comandi concreti al principio, cioè cercare nelle pagine i comandi che quel principio rende sbagliati. Una regola scritta e non applicata al testo che la contraddice lascia il testo a contraddirla, e chi legge la pagina non legge la regola.

*La forma corretta per `winetricks`, che è diversa dalle altre due.* Le quattro occorrenze di `winetricks` non si correggono aggiungendo `wine32` davanti al programma, perché `winetricks` non è un wrapper di Wine ma un programma autonomo di quasi ottocento kilobyte che invoca Wine al proprio interno. Il binario che invoca è configurabile e la riga che lo decide è `WINE="${WINE:-wine}"`, cioè usa la variabile di ambiente `WINE` e in sua assenza ripiega sul comando sbagliato. La forma corretta su un prefix a 32 bit è quindi `WINE=wine32` davanti al comando, e le quattro occorrenze sono state riscritte così. La distinzione fra le tre forme non è pedanteria: chi applicasse meccanicamente la stessa correzione a tutti e tre i casi otterrebbe un comando che non esiste.

*La regola che ne discende, ed è la terza volta che questo progetto la paga.* Una prescrizione sbagliata non vive dove la si è incontrata. La stessa assunzione errata sul comando di Wine è stata trovata e corretta in quattro momenti distinti, cioè la riga di installazione in MS-081, i due lanciatori della scrivania in MS-084, la fase 7 con la scheda di stampa in ADR-019, e ora ventitré comandi in sette pagine. Ogni volta la correzione è stata locale e ogni volta è rimasto del difetto altrove. Il modo di chiudere un difetto di questa forma è cercarlo con uno strumento su tutto il corpo della documentazione nel momento in cui lo si capisce, non nel punto in cui lo si è incontrato, e il criterio della ricerca deve essere quello che distingue i casi, qui l'architettura del prefix di destinazione e non il nome del comando.

Verificato con: `grep` ricorsivo su `docs/10-ambiente/` per le tre forme di invocazione, separate per architettura del prefix; lettura integrale di `/usr/bin/winecfg-stable` e `/usr/bin/wineboot-stable`, che eseguono entrambi `wine-stable` senza consultare l'ambiente; lettura di `/usr/bin/wine32-stable`, che esegue il caricatore `/usr/lib/i386-linux-gnu/wine/wine`; `WINEPREFIX=$HOME/.wine wine32 winecfg --help`, che risponde con esito zero; lettura della riga `WINE="${WINE:-wine}"` in `/usr/bin/winetricks`; ricerca di non contaminazione dei prefix a 64 bit dopo la correzione, senza risultati; `git diff --stat`, che conta ventitré righe cambiate su ventitré in sette file.

Esito: fatto per la documentazione. Non richiede alcun intervento sulla macchina, perché il prefix operativo esiste già e funziona: la correzione riguarda la procedura che qualcuno seguirebbe per ricostruirlo, e sarebbe fallita al primo comando.

### MS-088 - Ho introdotto io le fini riga miste in quattro file, e il controllo con cui credevo di essermene guardato era rotto

Perimetro: correzione di quattro file resi misti dalle mie stesse modifiche di questa sessione, cioè `docs/OPERATIONS-LOG.md`, `.claude/context/roadmap.md`, `.claude/context/current-work.md` e `docs/PENDING-ACTIONS.md`. Errore mio, con due cause distinte da isolare separatamente.

*Che cosa è accaduto.* Le voci nuove sono state inserite nei documenti con script che leggono il file conservandone le interruzioni, cioè con `newline=''`, e che però normalizzano a `LF` il testo da inserire. Il risultato è un file la cui parte preesistente resta `CRLF` e le cui righe nuove sono `LF`, che è esattamente il difetto che MS-063 documenta e per cui `tools/check-eol.py` esiste. Il conteggio a correzione fatta dice quanto: cinquantasei righe `LF` nel registro dei microstep, trenta nella roadmap, tredici nella scheda del lavoro corrente, due nelle azioni differite.

*La prima causa, banale e mia.* Avevo normalizzato il testo da inserire per uniformare i frammenti scritti in momenti diversi, che è un gesto ragionevole in sé, e non avevo aggiunto il passo che lo rende corretto, cioè riconvertire il risultato alla fine riga del file di destinazione. Il presidio corretto è duplice: nello script, convertire il contenuto inserito alla fine riga del file che lo riceve; nel processo, rilanciare `python tools/check-eol.py .` dopo le modifiche e non solo prima, perché un controllo eseguito soltanto all'inizio della sessione certifica lo stato di partenza e non quello che si sta consegnando.

*La seconda causa è peggiore, perché è un controllo che dava una risposta falsa.* All'inizio dell'intervento avevo rilevato la fine riga dei file da toccare con un ciclo che cercava il ritorno a capo con `grep -q $'\r'`, e quel ciclo ha risposto `LF` per tutti e nove i file, compresi quelli che erano `CRLF` puro nella storia di git. La risposta era falsa perché la sequenza `$'\r'` non è stata interpretata come il carattere di ritorno a capo dalla shell che ha eseguito il ciclo, quindi la ricerca cercava una stringa letterale che non esiste in nessun file, e l'assenza di corrispondenza è stata letta come assenza del carattere. Sono due modi diversi di non trovare qualcosa, e confonderli è il modo in cui un controllo diventa dannoso invece di inutile: un controllo assente lascia in dubbio, un controllo rotto convince.

Ne discende la regola operativa, che è la generalizzazione di una regola che questo progetto ha già scritto due volte in forme diverse. Un esito negativo di un controllo non è una prova finché non si è verificato che quel controllo sia in grado di dare un esito positivo. La forma minima della verifica è provare lo strumento su un caso che deve fallire, e nel caso specifico bastava contare i byte, cioè leggere il file in binario e contare `\r\n` contro `\n`, oppure lanciare lo strumento del progetto invece di improvvisarne uno. Le due volte precedenti sono MS-084, dove una conclusione ottenuta su un pacchetto è stata trasferita a un binario senza rifare la misura, e MS-014, dove lo standard error silenziato di uno strumento ha fatto leggere una eccezione come una non-modifica.

*Come il difetto è venuto a galla, e non per la via giusta.* Non l'ha trovato `check-eol.py`, perché non lo avevo ancora rilanciato: l'ha trovato un mio script che è fallito con `substring not found` cercando un ancoraggio di tre righe in `.claude/memory/index.md`. La causa di quel fallimento è la trappola che questo stesso registro documenta al microstep sui difetti dell'ambiente: un ancoraggio di più righe scritto con `LF` non si trova in un file `CRLF`, e l'errore che si osserva non dice nulla sulla causa. Quel fallimento è stato una fortuna doppia, perché ha impedito all'unico file rimasto integro di diventare misto e ha portato a controllare gli altri quattro.

*La correzione, e perché la fine riga di destinazione non è stata indovinata.* La prevalenza interna non è una prova sufficiente di quale fosse la fine riga originale, perché in un file misto la maggioranza dice soltanto quale parte è più grande. La fine riga originale è stata letta dalla storia di git, con `git show HEAD:<file>` per ciascuno dei cinque file interessati, e tutti e cinque risultano `CRLF` puro nel commit `b514c33`. I quattro misti sono stati quindi normalizzati a `CRLF`, e il quinto era già integro.

Verificato con: `git show HEAD:<file>` sui cinque file, con conteggio dei byte `\r\n` contro `\n`, che li dà tutti `CRLF` puro; conteggio dei byte sui file di lavoro prima della correzione, che quantifica le righe `LF` introdotte; `python tools/check-eol.py .`, che prima della correzione elenca i quattro file misti con la prevalenza e la fine riga da ripristinare, e dopo la correzione riporta zero misti.

Esito: fatto. Il difetto non è entrato nella storia del repository, perché è stato trovato e corretto prima del commit, che è precisamente il motivo per cui la sequenza di verifica prima di un commit va eseguita per intera e non a campione.

### MS-089 - L'edizione è Standard, la barra del titolo non dichiarava l'edizione, e la documentazione aveva ragione

Perimetro: accertamento della discrepanza sull'edizione di AKABAK, aperta il 2026-09-09 e lasciata aperta da MS-085 perché la finestra del release code non porta quel dato. Chiude la discrepanza. Non ritira nulla della documentazione di progetto, e ritira invece una mia lettura.

La finestra di informazioni sul programma, aperta dal menu di aiuto nel prefix `~/.wine` con `wine32`, dichiara sei dati e li conviene riportare tutti perché quattro di essi confermano affermazioni sparse e due sono nuovi. L'edizione è `Standard Edition`. Il sottotitolo del programma è `Lumped and Boundary Element Analysis`. La versione è `3.2.4 b126 (Akabak)`. La sicurezza è `Valid Release Code`. Il sistema operativo dichiarato dal prefix è `NT 10.0 (Build 19043)`. La memoria è `1876 / 2047 MBytes`.

*L'esito, e chi aveva ragione.* L'edizione è Standard, quindi le tre pagine che lo affermano sulla base delle osservazioni del 2026-09-07 sono confermate, e con esse la spiegazione registrata in `docs/90-riferimenti/licenze-e-registrazioni.md`: l'installer è uno e si chiama `AKABAK_Pro_v324b126.exe`, ma l'edizione la determina il release code e non il file scaricato, coerentemente con la student license per cui l'utente era stato registrato. La conferma vale più di una ripetizione, perché è la prima raccolta dopo la reinstallazione: se l'edizione fosse dipesa da qualcosa che l'azzeramento della radice tocca, questo è il momento in cui si sarebbe visto.

*Che cosa va ritirato, ed è una mia lettura e non un contenuto del progetto.* Il 2026-09-09 avevo registrato che la barra del titolo della finestra principale riportasse `32 Professional` e ne avevo dedotto una discrepanza sull'edizione, scrivendo che le due affermazioni non erano conciliabili. La deduzione era sbagliata: la barra del titolo non dichiara l'edizione di AKABAK, che è dichiarata soltanto qui, e quindi non c'era alcuna contraddizione da conciliare. Il difetto del mio ragionamento è preciso e vale isolarlo: avevo trattato due stringhe come affermazioni sullo stesso attributo per il solo fatto che una parola somigliava a un'altra, senza sapere che cosa la prima dichiarasse. Una discrepanza esiste quando due fonti affermano cose diverse dello stesso attributo, non quando una fonte usa una parola che in un altro contesto ne nomina uno.

Che cosa denoti allora `32 Professional` nella barra del titolo resta da verificare e non va assunto. La lettura plausibile, e va scritta come tale, è che sia la coppia formata dall'architettura del processo e dall'edizione di Windows che il prefix dichiara: il processo è a 32 bit, e la build `19043` corrisponde a un Windows 10 la cui edizione tipica si chiama Professional. Resta una ipotesi finché non la conferma il manuale del programma o una configurazione diversa del prefix, e non serve a nessuna decisione, quindi non vale spendervi tempo adesso.

*I due dati nuovi.* Il primo è `Security: Valid Release Code`, che è una seconda dichiarazione di validità della licenza in una finestra diversa da quella del release code, quindi una conferma indipendente dentro lo stesso programma. Il secondo è `Memory: 1876 / 2047 MBytes`, che è la firma di un processo a 32 bit e la misura del suo tetto: lo spazio indirizzabile è 2047 MByte e quello disponibile al momento della lettura era 1876. Il numero non è una curiosità, perché è il vincolo che la roadmap cita nella valutazione della replica del setup sul secondo portatile, dove i 4 GB di RAM della macchina si scontrano con un tetto che non dipende dalla RAM installata ma dall'architettura del processo; da oggi quel numero è misurato su questo programma e non desunto dalla teoria dei 32 bit.

Il sottotitolo `Lumped and Boundary Element Analysis` merita una riga perché nomina esattamente le due tecniche su cui poggia il flusso di questo progetto, cioè il modello a elementi concentrati per il comportamento a bassa frequenza e gli elementi di contorno per la radiazione, e conferma che l'edizione Standard le porta entrambe. Quali funzioni distinguano la Standard dalla professionale resta non accertato e non va supposto, come `licenze-e-registrazioni.md` già prescrive: se una simulazione urterà un limite di edizione, la verifica è il listino delle funzioni sul sito dell'autore.

Verificato con: finestra di informazioni sul programma di AKABAK aperta nel prefix `~/.wine` con `wine32`, screenshot fornito dall'utente, sei campi letti direttamente dall'immagine.

Esito: fatto. La discrepanza è chiusa, la fase 8 non ha più accertamenti aperti nelle sottofasi 8.1 e 8.2, e il lavoro riprende dalla sottofase 8.3.

## Che cosa resta da fare, e da che cosa dipende

Questa sezione ha cambiato natura quattro volte, e la successione è un progresso e non uno stallo, quindi vale dirla. All'inizio elencava microstep bloccati da una macchina di stato ignoto. Poi il blocco si è ristretto all'installazione della chiave SSH, che era una azione dell'utente non delegabile. Poi, con la chiave installata e le fasi 0 e 1 chiuse, non esisteva più alcun microstep bloccato da una condizione esterna e restava soltanto lavoro da eseguire in ordine. Oggi, al 2026-09-10, la natura è cambiata ancora: il lavoro rimanente è quasi tutto eseguibile subito, e l'unico blocco vero non è tecnico ma un acquisto.

Le fasi da 0 a 7 sono chiuse. La fotografia della macchina precedente sta in `docs/10-ambiente/fotografia-macchina-2026-09-07.md` e ha smentito tre delle quattro cause che avevo attribuito al blocco di aggiornamento, oltre a portare alla scoperta dei 32 bit di ADR-016. Il trasferimento dei materiali è verificato per impronte in MS-039, la copia di sicurezza di `/home` in MS-049, il Machine Identifier in MS-052. L'installazione pulita è eseguita l'8 settembre conservando `/home`, provata dal contenuto reale del disco e non dal riepilogo dell'installatore. L'accesso remoto è ripristinato, i tre difetti dell'installazione sono corretti in MS-077, e l'ambiente Wine è ricostruito nella forma che ADR-016 e ADR-019 prescrivono. Della fase 0 resta non eseguito soltanto l'esito reale di `sudo apt update`, che ADR-013 ha reso irrilevante.

Della fase 8 sono chiuse le sottofasi 8.1 e 8.2 senza accertamenti residui, dato che MS-089 ha chiuso anche la discrepanza sull'edizione, e non perché siano state eseguite ma perché sono diventate inutili: il prefix `~/.wine` è sopravvissuto con i due programmi installati e la licenza attiva, e MS-085 lo ha verificato per due vie. È il primo caso in cui la separazione fra radice e `/home` produce un risparmio misurabile invece di essere soltanto un presidio contro l'errore.

Il lavoro rimanente, in ordine, è il seguente.

La fase 8 dalla sottofase 8.3 in avanti, che è il prossimo passo concreto e non dipende da acquisti: il limite delle pipeline COM da impostare nelle preferenze di AKABAK, il pacchetto degli esempi da estrarre, poi VituixCAD, EASE Focus 3.1.260 con il servizio di database AFMG e il suo database dei GLL, e ARTA. Ramsete resta fuori finché PA-002 non è risolta.

La fase 6, che è l'unica bloccata, e non da una condizione fisica ma da una decisione di acquisto. La macchina ha la sola scheda integrata, verificato due volte a un giorno di distanza, e l'interfaccia esterna che i documenti dichiaravano come propria non appartiene a questo progetto: il ritiro è in MS-079 e la scelta è PA-012. Due parametri della scelta non sono stati dichiarati e vanno chiesti, cioè il numero di ingressi simultanei e un eventuale tetto di spesa.

La fase 10, cioè l'igiene post-installazione, è compiuta nelle sue parti che contano: la direttiva di aggiornamento su `Prompt=lts` era già impostata di serie, la sospensione automatica è disattivata con quattro target `masked`, e la chiave SSH dedicata è installata e funzionante. Restano la disattivazione dell'autenticazione per password e la prenotazione dell'indirizzo sul router, che sono entrambe azioni dell'utente e nessuna delle due blocca il progetto.

La fase 11, cioè la fotografia finale e il confronto con quella iniziale, che si fa a fase 8 chiusa.

Fuori da questa sequenza restano le azioni differite di `docs/PENDING-ACTIONS.md`, che non dipendono dal lavoro qui elencato. Due meritano di essere nominate perché il loro ordine rispetto al resto conta. PA-010, cioè l'inventario per impronta fra le copie esterne e `/home`, va compiuta prima di cancellare qualunque copia esterna di materiale personale, e i due controlli fatti finora coprono un perimetro molto più stretto di quello che serve. PA-011, cioè il backup completo della macchina, va preso a fase 8 chiusa e verificata, e la sua priorità è salita rispetto a quando fu aperta perché la ricostruzione è costata più di un giorno di lavoro. Lo strumento `python tools/check-pending-actions.py` dice quali condizioni sono soddisfatte, così che il controllo sia un comando invece di un ricordo, e le sue condizioni per PA-011 sono state riallineate ai fatti il 2026-09-10, perché riportavano ancora Wine non installato e i limiti realtime da correggere.
