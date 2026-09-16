# Registro dei microstep

> Tracciamento cronologico degli interventi, un microstep per voce. Ogni voce dichiara che cosa è stato fatto, come è stato verificato e con quale esito. La verifica è la parte che conta: un microstep senza esito verificato resta aperto, e la colonna dell'esito non contiene mai una previsione.

## Convenzione

Ogni microstep ha un identificativo progressivo nella forma `MS-NNN`, una data, un titolo, il perimetro dei file toccati, il comando o l'osservazione con cui è stato verificato, e l'esito. Gli stati possibili sono `fatto` quando la verifica è passata, `bloccato` quando la verifica non è eseguibile per una dipendenza esterna, e `aperto` quando il lavoro è iniziato e non concluso. Un microstep bloccato dichiara sempre da che cosa dipende.

Le voci si aggiungono in ordine cronologico crescente, così che il registro si legga come una storia. Non si riscrive una voce passata: se un intervento successivo la corregge, si aggiunge una voce nuova che dichiara di superarla.

## Il legame con il progetto, obbligatorio dal 2026-09-14

Ogni microstep dichiara in apertura, subito dopo il perimetro, a quale fase del workflow in otto fasi serve e che cosa del progetto dipenda da esso. È una frase e non una sezione. Quando l'intervento non serve alcuna fase lo dichiara apertamente, perché un legame inventato è peggio di un legame assente: fa credere che tutto sia giustificato e toglie valore alle giustificazioni vere.

La convenzione nasce da una lacuna reale, cioè che le voci fino a MS-096 spiegano il perché tecnico e non il perché di progetto. Per quelle voci il legame è fornito per blocchi in `docs/90-riferimenti/tracciabilita-microstep.md`, che è la forma additiva della correzione, dato che riscriverle sarebbe vietato dalla regola qui sotto e produrrebbe comunque un documento che sembra essere sempre stato giusto.

## Perché non si riscrive, e perché questo non fa perdere pezzi

La regola di non riscrivere una voce passata è la ragione per cui questo registro conserva anche gli errori, e va capita nel verso giusto perché la sua formulazione ingenua suggerisce il contrario. Non significa che una affermazione sbagliata resti in piedi: significa che resta leggibile insieme a quella che la corregge, cosicché chi legge veda non soltanto la conclusione giusta ma anche come ci si è arrivati e che cosa si era creduto prima. Un registro che si corregge in silenzio racconta un lavoro senza errori, che non è mai esistito, e chi lo eredita ripete gli errori che nessuno ha scritto.

La regola ha però un difetto reale, individuato il 2026-09-14, e la sua correzione è l'indice qui sotto. In un registro che cresce in avanti, una voce superata non sa di esserlo: chi legge MS-083 e si ferma là non ha modo di sapere che MS-084 la smentisce, e la responsabilità di scoprirlo ricade sul lettore che legge fino in fondo. Aggiungere un rimando dentro la voce vecchia sarebbe una riscrittura; aggiungere un indice a parte non lo è, ed è quindi la forma compatibile con la regola.

L'indice va aggiornato ogni volta che una voce nuova ne supera una precedente, e questo è parte della convenzione e non un lavoro facoltativo.

### Indice delle voci superate

| Voce superata | Superata da | Su che cosa |
|---|---|---|
| MS-021 | MS-024 | l'inferenza che le due copie del corredo software differissero, smentita dal confronto diretto |
| MS-059, MS-061, MS-065 | MS-067 | l'affermazione che dentro l'immagine di installazione esistesse un file oltre i 4 GiB, smentita dalla misura |
| MS-065 | MS-066 | l'avvertenza sul rischio di confondere la chiavetta con il disco esterno, resa inutile dalla casella che rende impossibile quell'errore |
| MS-069 | MS-073 | l'affermazione su come si verifichi il supporto di installazione, sostituita dal controllo automatico che il sistema registra da sé |
| più pagine, non una voce sola | MS-079 | l'affermazione che la macchina possedesse la Focusrite Scarlett 2i2, ritirata perché nata da un segnalibro promosso a inventario |
| MS-083 | MS-084 | l'affermazione che i due lanciatori della scrivania fossero rotti perché invocavano un nome inesistente |
| MS-085 | MS-087 | l'affermazione che la correzione delle sottofasi 8.1 e 8.2 riguardasse anche il prefix e non il solo comando |
| MS-112 | MS-113 | l'ipotesi che il rifiuto dei modelli GLL venisse dal provider crittografico di Wine, smentita sostituendolo con quello originale di Windows |

Due ritiri di questa sessione non compaiono in tabella perché non riguardano una voce del registro ma una mia spiegazione scritta altrove: MS-089 ritira la lettura secondo cui la barra del titolo di AKABAK dichiarasse l'edizione, e MS-093 ritira la spiegazione del 2026-09-09 sul perché una sessione SSH disponesse di un display. Restano nominati qui perché chi cerca un ritiro lo cerca in questo elenco.

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

### MS-090 - Il file di aiuto del programma dice più dell'email dell'autore: il trasferimento ha tre modi e non due

Perimetro: estrazione e lettura del file di aiuto compilato di AKABAK dentro il prefix, per accertare che cosa sia esattamente l'impostazione che la sottofase 8.3 prescrive di verificare. Corregge per incompletezza una affermazione che il progetto portava dal 14 agosto 2025, e apre una decisione.

*Perché il file di aiuto invece dei menu.* La sottofase 8.3 prescriveva di verificare una impostazione nelle preferenze di AKABAK senza dire quale, perché l'unica fonte era una frase dell'email dell'autore, che rimandava genericamente alle preferenze e alla guida. Cercarla nei menu davanti alla macchina sarebbe stato possibile ma cieco, e il progetto ha già pagato tre volte il prezzo di un controllo cieco. La guida, però, è dentro il prefix: `C:\Program Files\RDTeam\AKABAK\AKABAK.chm`, diciotto megabyte. Un file di aiuto compilato di Windows è un archivio, quindi `7z x` lo apre su Linux senza alcuna dipendenza aggiuntiva e senza aprire il programma: l'estrazione ha prodotto 1092 file, e la lettura è ridotta a due pagine su 1092 dopo una ricerca per parola.

*Che cosa dice la fonte autorevole.* Il capitolo `VACS` dell'appendice contiene una sezione `Transmission of Data` che è più precisa e più ampia dell'email. Per default AKABAK trasmette i dati spettrali a VACS in modo automatico attraverso COM, e in quello scenario VACS fa da server COM e si avvia da sé se non è già aperto. Esistono però due alternative e non una: gli appunti di sistema, cioè `Clipboard`, e i file su disco, cioè `Files`. La guida dichiara esplicitamente che una alternativa diventa necessaria se il sistema operativo sottostante non supporta la tecnica di trasferimento COM, e nomina Linux come esempio, il che promuove l'affermazione dell'autore da dichiarazione in una email a documentazione ufficiale del prodotto.

*La correzione, che è per incompletezza e non per errore.* La pagina `docs/90-riferimenti/timeline-akabak-vacs.md` afferma che su Linux il trasferimento avviene attraverso gli appunti di sistema. L'affermazione è vera ma incompleta, e l'incompletezza non è innocua perché nasconde l'alternativa migliore: i file. L'autore aveva risposto a una domanda dichiarando di non avere molta esperienza su Linux e aveva nominato la via che gli era venuta in mente; la guida del suo programma ne documenta due. Nessuna delle due fonti è sbagliata, e la lezione operativa è che la documentazione del prodotto batte la corrispondenza con il suo autore quando le due divergono in dettaglio, per la stessa ragione per cui il riferimento dei permessi batte una guida di terze parti.

*I nomi esatti, che sono il vero prodotto di questo microstep.* La selezione globale del modo di trasferimento sta nel menu `Options/Preferences`, pagina `VACS`, che la guida indica come `Options/Preferences-VACS`. Lo stesso modo può essere specificato per singola osservazione nella pagina `Range` della form dell'osservazione, il che significa che la scelta globale è un default e non un vincolo. L'emissione dei dati avviene alla fine di un calcolo, oppure a richiesta con il menu `Processing/Output Spectra`. Con `Clipboard` le curve finiscono negli appunti e nient'altro accade: per incollare si seleziona l'applicazione di destinazione e si usa il suo menu `Edit/Paste`, e in VACS conviene creare prima una form di grafico vuota; a ogni aggiornamento basta incollare di nuovo, perché VACS cerca da sé le curve da aggiornare. Con `Files` i dati vanno su disco con nomi generati automaticamente, in una cartella specificabile globalmente o per osservazione e per default quella del progetto, e in VACS si importano con il menu `IO/Import Data`, che accetta uno o più file, con lo stesso meccanismo di aggiornamento. In entrambi i casi il formato del dataset segue lo schema `VACS - Import Control Setting`, documentato nella guida di VACS.

*Una incoerenza interna alla guida, da registrare perché indirizza la verifica.* La pagina `Form - Preferences` descrive la propria pagina `VACS` come una pagina che informa su dove scaricare il modulo per l'emissione dei risultati delle osservazioni spettrali, e non menziona alcuna selezione del modo di trasferimento; il capitolo `VACS` dell'appendice, invece, indica proprio quella pagina come il luogo della selezione globale. Le due affermazioni non si conciliano leggendo, e la più specifica è la seconda. La conseguenza pratica è che la verifica in interfaccia non è una formalità: serve a stabilire quale delle due descrizioni corrisponda a questa versione del programma, cioè la `3.2.4 b126`.

Un dato accessorio confermato dalla stessa pagina, e che vale perché finora poggiava sulla sola scheda riservata: la guida dichiara che il Release Code di AKABAK abilita automaticamente anche VACS, quindi un solo codice copre i due programmi.

Verificato con: `7z x` sul file `AKABAK.chm` estratto in una cartella temporanea sulla macchina, 1092 file prodotti; lettura integrale, convertita in testo, di `Chapters/Appendix/VacsViewer.html` e di `Chapters/Desktop/Form-Preferences.html`; ricerca per parola su tutto l'albero estratto per individuare le due pagine pertinenti fra le 1092. La cartella temporanea è stata rimossa dopo la lettura, perché il file di aiuto resta nel prefix e l'estrazione è riproducibile con un comando.

Esito: fatto per l'accertamento documentale. La verifica in interfaccia della sottofase 8.3 è ora una verifica mirata su un nome di menu noto invece di una ricerca, e la scelta fra i due modi è registrata come ADR-020.

### MS-091 - Il progetto era indietro rispetto al template, non avanti, e portava ventidue apostrofi orfani

Perimetro: censimento della deriva fra questo progetto e `template-claude-developing` in entrambe le direzioni, allineamento dei ventinove file su cui il template era avanti, riscrittura della sezione sulle divergenze in `CLAUDE.md` e della voce PA-003. Rovescia una affermazione che il progetto portava dal 2026-09-04.

*Perché il censimento è stato fatto in due direzioni.* Il progetto dichiarava due divergenze volute dal template, entrambe da propagare all'indietro, e questa formulazione contiene un presupposto che nessuno aveva più verificato: che il template stesse fermo. Non stava fermo. Una sessione ha lavorato su di esso il 2026-09-07, il 2026-09-08 e il 2026-09-09, quindi la domanda giusta non era quali correzioni portare là, ma in quale direzione fosse la deriva su ciascun file. Il confronto è stato fatto con `diff` ricorsivo su `.claude/` e su `tools/`, e la direzione di ciascuna differenza è stata stabilita con le date di modifica e con la lettura del contenuto, non con una presunzione.

*Il risultato più importante, ed è l'opposto di quanto il progetto affermava.* `CLAUDE.md` dichiarava fra le divergenze volute l'uso qui delle versioni più recenti degli strumenti tipografici, precisando che nel template vivevano in `tools/` alla radice e non nel pacchetto di istanziazione. Al 2026-09-12 quella frase è falsa in entrambe le sue parti. Nel template la copia alla radice e quella nel pacchetto `fix-typography` sono identiche per tutti e cinque i file, quindi lo sfasamento che PA-003 tracciava è già chiuso là. E le versioni del template sono più recenti di quelle di questo progetto su quattro file su cinque: `fix-accents.py` 33356 byte contro 31073, `fix-missing-accents.py` 25234 contro 24451, `test-tipografia.py` 11985 contro 9448, `dashes-exclude.txt` 659 contro 577.

*Che cosa contengono le versioni nuove, perché è la ragione per cui adottarle non è una formalità.* Il `fix-accents.py` del template porta una funzione che il nostro non aveva, `togli_residuo`, con la sua espressione regolare `RESIDUO_DOPPIA_CORREZIONE`, che rimuove l'apostrofo rimasto dopo una vocale già accentata e conta le rimozioni in una voce propria delle statistiche, così che una corsa dichiari quante volte ha riparato invece di quante volte ha convertito. Il suo docstring spiega anche perché non riporta residui indecidibili: una vocale accentata seguita da apostrofo non è una forma dell'italiano, quindi l'unica lettura possibile è che l'apostrofo sia di troppo. È esattamente la riparazione del difetto che MS-014 aveva diagnosticato in questo progetto e che PA-003 tracciava come da propagare: il template l'ha implementata prima, e qui mancava.

*Il danno che quel difetto aveva già fatto, misurato.* Una ricerca del pattern formato da una vocale accentata seguita da apostrofo ha trovato ventidue occorrenze nei file di codice del progetto: nove in `tools/fix-dashes.py`, due in `tools/md-unwrap.py`, e le undici corrispondenti nelle copie sotto `.claude/templates/`. Sono forme come `Perché' esiste`, `più'`, `può'`, e vivono nei docstring, cioè nella prosa dentro il codice. La causa è quella descritta in MS-014, cioè la catena tipografica lanciata su un file di codice, e la prova che si tratti di quel danno e non di una svista di scrittura è che le stesse righe nelle versioni del template sono pulite. Dopo l'adozione delle versioni del template la ricerca restituisce zero.

*Che cosa è stato portato qui.* Dodici file nuovi e diciassette aggiornati. Fra i nuovi la regola `chat-non-e-memoria.md`, i due pacchetti di modelli `alignment` e `anonymization` con i loro strumenti e regole, lo strumento `fetch-reddit.py` del pacchetto `community-sources`, il modello `context/sub-subproject.md` e la copia di `test-tipografia.py` dentro il pacchetto `fix-typography`. Fra gli aggiornati la regola `web-sources-not-fetchable.md`, i cinque strumenti tipografici e `md-unwrap.py` sia in `tools/` sia nei pacchetti, il catalogo `PACKAGES.md`, e i file dei pacchetti `community-sources` e `hooks-starter`. Il `PROJECT-SYSTEM.md` è tornato identico a quello del template, e gli mancava un solo paragrafo, quello che adotta la regola nuova.

*La regola che mancava, e l'ironia della sua assenza.* `chat-non-e-memoria.md` prescrive che nessun contenuto sostanziale resti nella sola conversazione e che i file si aggiornino nello stesso giro di lavoro in cui il contenuto nasce. Il suo preambolo dichiara di nascere da una direttiva d'uso del 2026-09-09 data in un progetto istanziato dal template, e quel progetto è con ogni probabilità questo, perché è la direttiva sul tracciamento integrale che `CLAUDE.md` porta in prosa dal medesimo giorno. La regola è quindi nata qui, è stata scritta nel template, e non era mai tornata indietro: il progetto che l'ha generata era l'unico a non averla in forma caricabile. L'indice dei satelliti in `CLAUDE.md` elenca ora otto regole invece di sette, con due da caricare sempre.

*Che cosa non è stato toccato, e perché.* La regola `git-identity-and-repo.md` diverge perché è istanziata: il template porta segnaposto come `<user-account1>` dove qui stanno le identità reali, gli alias SSH e i percorsi delle chiavi. Sovrascriverla avrebbe rimesso i segnaposto al posto dei valori, che è il modo più rapido di rompere una regola operativa. La skill `studio-didattico` diverge invece perché qui è più corretta: la versione del template marca in grassetto una locuzione che la regola di stile del template stesso vuole in corsivo, quindi questo progetto è avanti di una riga e la correzione va nell'altra direzione.

*Conseguenza sul metodo, e vale oltre questo caso.* Una divergenza dichiarata in un documento invecchia come qualunque altra affermazione, e invecchia peggio delle altre perché nessuno la rilegge: descrive un rapporto fra due cose, quindi resta vera solo finché entrambe stanno ferme. La frase su `CLAUDE.md` era corretta quando fu scritta il 2026-09-04 ed è diventata falsa il 2026-09-09 senza che nulla in questo repository cambiasse. La forma difendibile è quella adottata ora, cioè dichiarare la data del confronto accanto alla divergenza, così che chi legge sappia a quando risale invece di crederla perenne.

Verificato con: `diff -rq --strip-trailing-cr` fra le due cartelle `.claude/` e fra i due `tools/`, con la direzione delle sole differenze stabilita da `stat` sui tempi di modifica e dalla lettura del contenuto; confronto a tre vie fra `tools/` del progetto, `tools/` del template e il pacchetto `fix-typography` del template, che mostra le ultime due identiche; lettura delle righe aggiunte in `fix-accents.py`; ricerca del pattern della vocale accentata seguita da apostrofo su `tools/` e `.claude/`, ventidue occorrenze prima e zero dopo; `diff` finale fra i due `PROJECT-SYSTEM.md`, che non riporta differenze; catena di verifica prima del commit eseguita per intera con gli strumenti nuovi, sei controlli su sei a esito zero.

Esito: fatto. Restano due voci da propagare al template, riscritte in PA-003, e una verifica non decisa dal confronto, cioè la gestione dei percorsi cross-disco, che va accertata con il caso minimo già descritto in MS-014.

### MS-092 - Inventario di `_notes`: che cosa è obsoleto, che cosa è già documentazione e che cosa non va toccato

Perimetro: censimento integrale della cartella privata `_notes`, classificazione di ogni voce, rimozione delle sole due voci la cui perdita non costa nulla, e dichiarazione di quelle che richiedono una decisione dell'utente. Quarantuno megabyte esaminati, due rimossi per zero perdita, quaranta lasciati in decisione.

*Il vincolo che governa questo microstep.* `_notes` è esclusa dal versionamento, quindi una cancellazione qui non è recuperabile da git: non esiste `git restore`, non esiste un commit precedente, e il solo presidio è il backup generale della postazione. Ne segue che il criterio per rimuovere non è che una cosa sembri obsoleta, ma che la sua perdita sia dimostrabilmente nulla, cioè che il contenuto sia rigenerabile da uno strumento versionato oppure già interamente trasferito in un documento tracciato. Tutto ciò che non soddisfa quel criterio resta e viene dichiarato, perché la scelta appartiene a chi possiede il dato.

*Rimosso, con la prova della rigenerabilità.* Il file `scheda-reinstallazione-ubuntu-studio.docx` era l'uscita predefinita di `tools/make-scheda-docx.py`, cioè un artefatto derivato da una sorgente tracciata, `docs/10-ambiente/scheda-reinstallazione.md`, tramite uno strumento versionato. La rigenerazione è stata provata prima di cancellare, scrivendo il documento in una cartella temporanea: lo strumento riporta dodici passi in sequenza, quattro partizioni e quattro voci di BIOS, e produce un file di dimensione equivalente. Solo dopo quella prova il file è stato rimosso. È stata rimossa anche la cartella `tmp`, che era vuota.

*Non rimosso, ed è già documentazione.* La cartella `materiale-radice` contiene i cinque file sciolti che stavano alla radice fino al 2026-09-09, e il lavoro di trasformazione in documentazione è già stato fatto in MS-080: il suo README dichiara per ciascun file che cosa fosse e in quale documento tracciato viva oggi il suo contenuto, cioè `docs/90-riferimenti/fonti.md` per i tre segnalibri e `docs/90-riferimenti/censimento-corredo.md` per l'albero del pacchetto software. Due di quei file meritano di restare là e non altrove per una ragione esplicita e non per inerzia. L'albero del pacchetto nomina cartelle di protezione rimossa, quindi non entra in un file tracciato. E `focusrite.txt`, che contiene un solo indirizzo, è la fonte materiale di un errore documentale, cioè il segnalibro promosso a inventario che fece dichiarare come fatto il possesso di una interfaccia audio: conservarlo è conservare il corpo del reato di MS-079.

*Non rimosso, ed è prova non riproducibile.* La cartella `fotografia-2026-09-07`, ventitré file per settecento kilobyte, è l'uscita grezza della fase 0 sulla macchina prima della reinstallazione. La sua distillazione sta in `docs/10-ambiente/fotografia-macchina-2026-09-07.md`, ma la distillazione non la sostituisce: il sistema che quei file descrivono non esiste più dall'8 settembre, quindi nessun comando può riprodurli. Un documento derivato si può riscrivere, una misura di uno stato scomparso no.

*Non rimosso, e non va mai trasformato in documentazione tracciata.* Il file `licenze-akabak-riservato.md` contiene il Release Code permanente di AKABAK e il Machine Identifier a cui è legato. La richiesta di trasformare il contenuto di `_notes` in documentazione di progetto incontra qui il suo unico limite assoluto, e va enunciato perché una richiesta generale non lo prevede: questo file esiste proprio per non essere tracciato. Ciò che di esso poteva diventare documentazione lo è già, cioè lo storico in `docs/90-riferimenti/timeline-akabak-vacs.md` e il quadro di licenza in `licenze-e-registrazioni.md`, entrambi scritti senza i valori.

*Non rimosso, e la decisione è dell'utente.* Il documento sorgente `full_electroacoustics.docx`, novantanove kilobyte, è l'originale da cui l'intero albero `docs/` è stato convertito. La prova che la copertura sia integrale è in `docs/90-riferimenti/copertura-sorgente.md`, e quella prova rende il file rimovibile senza perdita di informazione; resta però l'originale di un documento scritto a mano, e novantanove kilobyte non sono un costo. La raccomandazione è conservarlo, ma la scelta appartiene all'utente.

*Non rimosso, e qui la decisione richiede un accertamento che ho fatto.* I due file `lista-backup-28082026.txt` e `lista-backup-04092026.txt` pesano insieme trentanove megabyte e sono il novantasei per cento della cartella. Sono elenchi prodotti da 7-Zip su due archivi di backup da ventisei gibibyte residenti su `J:`. Tre fatti li riguardano e vanno dichiarati insieme perché nessuno dei tre da solo decide. Il primo è che non contengono impronte per file ma soltanto data, attributi, dimensione e percorso: le occorrenze della stringa `CRC` che una ricerca grezza trova sono nomi di file, non checksum, quindi questi elenchi non possono soddisfare il criterio di PA-010, che richiede esplicitamente il confronto per impronta e non per dimensione occupata. Il secondo è che non riguardano questo progetto: elencano il backup generale della postazione, con la sincronizzazione di Google Drive, il portfolio, i libri di sicurezza informatica e le copie di sviluppo di molti altri repository. Il terzo è che nessun documento tracciato di questo progetto li cita. Sono quindi materiale personale dell'utente, estraneo al perimetro del progetto e non utile all'unica azione differita che avrebbe potuto consumarli.

*Non rimosso, e lo dichiaro come dubbio invece di deciderlo.* Il file `scheda-docx-precrash-2026-09-08.docx`, dodici kilobyte, è la versione del documento di stampa composta a mano prima che lo strumento esistesse, conservata dopo l'incidente che MS-070 racconta. È superata dallo strumento e il suo racconto è nel registro, quindi per il criterio dell'utente è obsoleta; non è però riproducibile, perché il codice che la costruiva viveva soltanto nella sessione. La conservazione costa dodici kilobyte e la cancellazione è definitiva, quindi la proporzione suggerisce di conservarla, ma la voce resta in decisione.

Verificato con: percorso ricorsivo di `_notes` con dimensioni, date e conteggi per cartella; lettura di `materiale-radice/README.md` e dei file di testo che contiene; ispezione della struttura dei due elenchi di backup e verifica che le occorrenze di `CRC` siano nomi di file e non checksum; ricerca di citazioni dei due elenchi nei documenti tracciati, senza risultati; prova di rigenerazione del `.docx` con `tools/make-scheda-docx.py --out` su percorso temporaneo prima della cancellazione.

Esito: fatto per la parte che non richiede decisioni. Restano in decisione dell'utente il documento sorgente, i due elenchi di backup e la scheda precedente allo strumento, e la ragione per cui non li ho rimossi è la stessa per tutti e tre, cioè che nessuno dei tre è riproducibile e la cartella non è versionata.

### MS-093 - AKABAK non parte da SSH, e la spiegazione che avevo dato il 2026-09-09 è smentita

Perimetro: diagnosi del fallimento di avvio di AKABAK da una sessione remota, individuazione della forma di comando che funziona, ritiro di una spiegazione precedente, e scrittura della scheda relativa in `docs/10-ambiente/wine-troubleshooting.md`. La verifica della sottofase 8.3 resta da fare e questo microstep la sblocca.

Il sintomo, sulla riga di comando dell'utente, è stato `err:winediag:nodrv_CreateWindow Application tried to create a window, but no driver could be loaded.` seguito da `The explorer process failed to start.` e da una eccezione non gestita che apre il debugger. Il messaggio non dice che manchi un driver sul sistema e non dice che il prefix sia rotto: dice che Wine non ha trovato alcun driver che sapesse dove disegnare la finestra.

*La diagnosi, e le tre cause escluse prima di cercare la quarta.* I driver esistono per l'architettura giusta, perché `find` li trova sotto `i386-windows` e non soltanto sotto `x86_64-windows`, quindi il ramo a 32 bit è completo. La sessione grafica è viva, perché `loginctl list-sessions` mostra una sessione di tipo `wayland` su `seat0` attiva, accanto a due sessioni remote di tipo `tty`. I socket ci sono entrambi, cioè `wayland-0` in `/run/user/1000` e `X0` in `/tmp/.X11-unix`. E il registro del prefix non dichiara alcun driver grafico: sotto `Software\Wine\Drivers` ci sono le sole voci di `winepulse.drv`, che riguardano l'audio, quindi non esiste una scelta sbagliata scritta da qualche parte.

La causa è la quarta. In una sessione aperta via SSH, sia interattiva sia non interattiva, `DISPLAY` e `WAYLAND_DISPLAY` sono entrambe vuote, mentre `XDG_RUNTIME_DIR` vale `/run/user/1000` e `XDG_SESSION_TYPE` vale `tty`. Wine non ha alcun indirizzo a cui mandare la finestra.

*Il ritiro, ed è di una mia spiegazione e non di un dato.* La voce del 2026-09-09 in `.claude/memory/progress.md` registra che avevo dichiarato che una sessione SSH non ha display, che la finestra era invece comparsa lanciando da remoto, e che la causa sarebbe stata la ricaduta della libreria di Wayland sul socket predefinito dentro `XDG_RUNTIME_DIR`, ereditata dalla sessione remota. La prova di oggi smentisce quella spiegazione in modo diretto: `XDG_RUNTIME_DIR` è impostata, il socket `wayland-0` esiste, e l'avvio fallisce lo stesso; impostando a mano `WAYLAND_DISPLAY=wayland-0` il fallimento resta identico, con le stesse due righe. Il dato osservato allora, cioè che la finestra comparve, resta vero; ciò che era sbagliato è il meccanismo che gli avevo attribuito.

La causa del mio errore va isolata perché è di una forma che non avevo ancora registrato in questo progetto. Non avevo misurato niente di falso: avevo costruito una spiegazione plausibile che si adattava a una osservazione, e l'avevo scritta come se fosse accertata. Una spiegazione che si adatta a una osservazione non è verificata finché non ne predice una seconda, e il momento di metterla alla prova è quello in cui la si scrive, non quello in cui fallisce. La forma minima della prova, qui, sarebbe costata un comando: rilanciare dalla stessa sessione dopo avere svuotato la variabile che si riteneva responsabile, e vedere se il comportamento cambiava.

Perché la via Wayland non funzioni su questa installazione non è accertato, e lo dichiaro invece di riempirlo con una seconda ipotesi. Il modo di accertarlo, se servisse, è dichiarare esplicitamente il driver nel registro del prefix e osservare che cosa cambia. Non serve adesso, perché la via X11 funziona.

*La forma che funziona, e perché servono due variabili e non una.* La prima è `DISPLAY`, che dice a quale server X mandare la finestra, e su questa macchina vale `:0`, cioè XWayland dentro la sessione Plasma. La seconda è `XAUTHORITY`, che indica il file con il biscotto di autorizzazione senza il quale quel server rifiuta la connessione. Le prove sono state fatte con `notepad` invece che con AKABAK, perché è un programma minimo, non scrive configurazione e si chiude da solo con un `timeout`: `WAYLAND_DISPLAY=wayland-0` da sola lascia due occorrenze dell'errore, `DISPLAY=:0` da sola ne lascia due, e le due insieme ne lasciano zero.

Il file di autorizzazione porta un nome con una parte casuale, per esempio `xauth_yEuuxx`, e quel nome cambia a ogni nuovo accesso grafico. Va quindi ricavato e non trascritto, con `$(ls -1 /run/user/$(id -u)/xauth_* | head -1)`, e la ragione non è eleganza: un comando che lo trascrive funziona oggi e fallisce dopo il primo riavvio con un errore diverso, cioè un rifiuto di connessione al server X invece dell'assenza di driver, il che manderebbe la diagnosi successiva su una pista sbagliata.

Va infine osservato che il guasto riguarda il solo lavoro da remoto. Dentro la sessione grafica della macchina, sia dal terminale sia dai lanciatori della scrivania, le due variabili sono già impostate e il comando nudo funziona: è quasi certamente così che la finestra comparve nelle sessioni precedenti, e questa è l'ipotesi più semplice compatibile con entrambe le osservazioni, anche se non è stata verificata chiedendo all'utente dove avesse digitato.

Verificato con: `loginctl list-sessions` e `loginctl show-session` sulle quattro sessioni, che mostrano una sessione `wayland` attiva su `seat0` e due remote di tipo `tty`; `ls -la /run/user/1000`, che elenca `wayland-0` e il file `xauth_*`; `ls -la /tmp/.X11-unix`, che elenca `X0`; `find /usr/lib` per i due driver, presenti anche per `i386`; lettura di `Software\Wine\Drivers` in `user.reg`, che contiene le sole voci audio; lettura delle quattro variabili di ambiente in una shell remota interattiva e in una non interattiva, con lo stesso esito; tre prove di avvio di `notepad` sotto `timeout`, con conteggio delle occorrenze di `nodrv` pari a due, due e zero; prova finale della forma robusta con il file di autorizzazione ricavato, zero occorrenze.

Esito: fatto per la diagnosi e per la documentazione. La sottofase 8.3 è ora eseguibile da remoto e resta da eseguire.

### MS-094 - La sottofase 8.3 è eseguita, e il confronto prima e dopo dà il nome della chiave

Perimetro: esecuzione della sottofase 8.3, cioè l'impostazione del modo di trasferimento dei dati spettrali da AKABAK a VACS, con verifica per confronto dei file di configurazione del prefix prima e dopo l'azione. Chiude la sottofase 8.3, promuove ADR-020 da proposta ad accettata, e risolve la discordanza fra due pagine della guida.

*Il metodo, e perché non era una formalità.* L'azione è un giro di menu in una interfaccia grafica, cioè il genere di intervento che di norma si può solo dichiarare. È stata invece resa misurabile registrando prima le impronte MD5 dei tre file di configurazione del prefix, cioè `C:\ProgramData\RDTeam\Akabak.ini`, `AppData\Local\RDTeam\Akabak.ini` e `AppData\Local\RDTeam\VACS.ini`, e rileggendole dopo. Il guadagno non è la prova che l'utente abbia cliccato: è che il file cambiato e la chiave comparsa dicono dove il programma scrive quella preferenza, e da quel momento l'impostazione è riproducibile su qualunque prefix futuro scrivendo una riga, invece di essere un percorso di menu da ricordare.

*L'esito del confronto.* Delle tre impronte una sola è cambiata, ed è quella di `AppData\Local\RDTeam\Akabak.ini`, da `66cb9388...` a `6c5db196...`. Il file della licenza sotto `ProgramData` è rimasto identico, il che è una conferma utile e non ovvia, perché significa che toccare le preferenze non riscrive l'attivazione. Anche `VACS.ini` è rimasto identico, quindi la scelta vive interamente dal lato di AKABAK.

*Le tre chiavi che governano il trasferimento.* Sono comparse `SpectrumOutputType=3`, `SpectrumOutputAsText=0` e `SpectrumOutputFolder=`, e corrispondono uno a uno ai tre controlli della pagina. Il valore `3` è quello che il menu a tendina mostra come `File`, il `0` corrisponde alla casella `Text format` non spuntata, e la cartella vuota significa che vale il valore predefinito, cioè la cartella del progetto. La corrispondenza fra `3` e `File` è osservata; quale valore corrisponda a COM e quale agli appunti non è accertato e non va supposto, perché per saperlo occorrerebbe cambiare l'impostazione e rileggere, e non serve a nulla adesso.

*Una scoperta collaterale, che vale più della chiave.* Prima dell'azione quel file conteneva cinque chiavi, dopo ne conteneva ventotto. La conferma delle preferenze non ha scritto la sola voce modificata: ha materializzato su disco l'intero insieme delle impostazioni, che fino a quel momento viveva come valore predefinito nel codice e non come dato. Ne discendono due conseguenze. La prima è che lo stato di configurazione del programma è ora ispezionabile e diffabile, cioè è diventato un file di testo che si può confrontare fra due momenti o fra due macchine. La seconda è che alcuni valori che il progetto avrebbe dovuto scoprire più avanti sono già leggibili: `NumSubThreads=8` per il parallelismo del solutore, `NUCType=1` per il metodo predefinito di compensazione della non unicità, `Frequ_f1=10`, `Frequ_f2=2k` e `Frequ_NumFrequs=24` per l'intervallo di frequenza predefinito, che è coerente con l'asse visibile nella finestra principale, e la terna `SaveResultFiles_BEM=1`, `SaveResultFiles_Obs=1` e `SaveResultFiles_Tmp=0`, che dice che i file di risultato si salvano accanto al progetto e non nella cartella temporanea del sistema.

*La discordanza della guida, risolta, e una terza fonte che sbaglia nello stesso verso.* MS-090 aveva registrato che due pagine della guida non concordavano: il capitolo `VACS` dell'appendice indicava la pagina delle preferenze come luogo della selezione, mentre la pagina `Form - Preferences` la descriveva come una pagina che informa soltanto su dove scaricare il modulo. Ha ragione il capitolo dell'appendice. La finestra ha quattro schede, cioè `Graphics`, `Processing`, `VACS` e `Files`, e la scheda `VACS` contiene il controllo `Spectrum way of output` con il menu a tendina, il campo `Folder` con il selettore, e la casella `Text format`.

Va però registrato che il testo informativo stampato dentro quella stessa pagina sbaglia nello stesso verso della pagina di guida incompleta: dichiara che la comunicazione è o automatica tramite interfaccia COM o manuale tramite appunti, e non nomina i file, mentre il menu a tendina che gli sta sotto offre proprio i file. Le fonti che sottostimano le vie sono quindi tre, cioè l'email dell'autore del 2025, la pagina `Form - Preferences` della guida e il testo dentro la pagina stessa; quelle che concordano sulle tre vie sono due, cioè il capitolo dell'appendice e il controllo reale. La regola operativa che ne discende è la stessa già enunciata in MS-090 e vale la pena vederla confermata: fra una descrizione e la cosa descritta, decide la cosa.

Un dettaglio minore ma curioso va annotato perché spiega l'incoerenza invece di lasciarla misteriosa: il testo di quella pagina non nomina AKABAK ma `ABEC`, che è il programma gemello dello stesso autore. La finestra delle preferenze è quindi condivisa fra i due prodotti, e il suo testo è rimasto indietro rispetto ai controlli che la accompagnano.

*Sul comando e sulla sessione, una conferma che chiude MS-093.* L'avvio è stato fatto da una sessione SSH con la forma che MS-093 aveva stabilito, cioè `DISPLAY=:0` insieme a `XAUTHORITY` ricavato dal file della sessione, e l'uscita del programma non contiene alcuna riga `nodrv_CreateWindow`: arriva fino alle chiamate della barra delle applicazioni, come nella corsa riuscita del 2026-09-10, e termina con `WTSUnRegisterSessionNotification` e `BufferedPaintUnInit`, che sono la chiusura regolare. La forma remota è quindi validata sul programma vero e non soltanto sulla prova con `notepad`.

Verificato con: `md5sum` sui tre file di configurazione prima e dopo l'azione, con una sola impronta cambiata; lettura integrale del file cambiato, da cinque a ventotto chiavi; screenshot della scheda `VACS` della finestra delle preferenze fornito dall'utente, che mostra le quattro schede, il controllo `Spectrum way of output` sul valore `File`, il campo `Folder` vuoto e la casella `Text format` non spuntata; lettura dell'uscita di avvio del programma, priva di errori di driver.

Esito: fatto. La sottofase 8.3 è chiusa, ADR-020 passa ad accettata, e la fase 8 prosegue dalla sottofase 8.4, cioè l'estrazione del pacchetto degli esempi.

### MS-095 - La sottofase 8.4 non va eseguita, e il motivo non è che sarebbe inutile ma che sarebbe dannosa

Perimetro: verifica dello stato degli esempi di AKABAK, confronto per CRC-32 fra l'archivio e la copia presente nel prefix, decisione di non eseguire l'estrazione prescritta, riscrittura della sottofase 8.4, e ricognizione dei prerequisiti delle sottofasi da 8.5 a 8.8. Chiude la sottofase 8.4.

*Perché si è guardato prima di eseguire.* La sottofase prescriveva di estrarre `AKABAK-Examples.zip` in `~/AkabakProjects/esempi`. Il comando è innocuo a leggerlo, e questa è precisamente la ragione per cui andava guardato prima: la procedura è stata scritta per una ricostruzione da zero, e questa macchina non è da zero, perché il prefix è sopravvissuto con dentro tutto ciò che vi era stato installato. Le sottofasi 8.1 e 8.2 erano già cadute per lo stesso motivo, quindi la domanda da porsi non era se il comando funzionasse ma se servisse ancora.

*Che cosa si è trovato.* Gli esempi esistono già dentro il prefix, in `C:\Program Files\RDTeam\AKABAK\AKABAK Examples`, con data 13 agosto 2025, cioè da prima della reinstallazione. Non è una cartella qualsiasi: è esattamente il percorso che la chiave `ExamplePath` dichiara nelle preferenze lette in MS-094, cioè quello che il menu `File/Open Example` apre.

*La verifica, e perché non è bastato contare.* Il primo confronto dava 632 file nel prefix contro 681 voci nell'archivio, che sembrava uno scarto di quarantanove. Non lo era: `unzip -l` conta anche le cartelle e `find -type f` no. Il secondo confronto, sui soli file, ha dato 632 contro 632 con zero differenze di nome. Nemmeno questo però era sufficiente, perché un insieme di nomi uguali non dice nulla sui contenuti, e una estrazione interrotta lascia esattamente nomi giusti e contenuti troncati. La verifica che decide è quindi il confronto per impronta, fatto con uno script passato sullo standard input di `python3` sulla macchina: legge i CRC-32 dal direttorio centrale dell'archivio, ricalcola quelli dei file su disco e confronta. Esito: 632 contro 632, zero presenti solo da una parte, zero CRC divergenti.

Vale notare che il CRC-32 è più debole di una impronta crittografica e che qui è la scelta giusta lo stesso, perché non serve difendersi da una manomissione ma accertarsi che una copia sia integra, e quel valore è già scritto dentro l'archivio, quindi il confronto non costa una seconda lettura del file compresso.

*Perché eseguire sarebbe stato dannoso e non soltanto ridondante.* La distinzione è il punto di questo microstep. Una estrazione avrebbe prodotto una seconda copia da 159 MB in `~/AkabakProjects/esempi`, cioè in un percorso che il programma non conosce: il menu degli esempi continuerebbe ad aprire la copia dentro il prefix, quindi chi lavorasse sulla copia nuova modificherebbe file che il programma non apre, e chi aprisse dal menu modificherebbe file che nessun documento nomina. Due copie della stessa cosa che possono divergere, con un documento che prescrive quella sbagliata, sono il difetto che questo progetto ha già registrato in altre forme, e la regola operativa che ne discende è che prima di creare una copia si verifica se il programma dichiari già dove cerca quel materiale, e in caso affermativo si adotta il suo percorso invece di inventarne uno.

*La riscrittura della sottofase.* La 8.4 non prescrive più un'estrazione incondizionata. Dice prima di verificare se gli esempi siano già nel percorso dichiarato da `ExamplePath`, e come verificarlo per impronta e non per presenza; poi di estrarre soltanto se mancano; e in quel caso di estrarre nel percorso che il programma dichiara, oppure, se si sceglie un altro percorso, di aggiornare `ExamplePath` di conseguenza, cosa che MS-094 ha reso possibile senza toccare i menu perché la chiave è nota.

*Ricognizione dei prerequisiti delle sottofasi successive, fatta nello stesso giro.* Serve a sapere che cosa manca prima di chiedere all'utente di sedersi davanti alla macchina, invece di scoprirlo a metà. I tre installer sotto `installers/` sono soltanto AKABAK e le due varianti di VACS, per 68 MB, ma il corredo non è perduto e non è là: vive sotto `progetto-stanza/`, per 570 MB, con `VituixCAD_setup.exe` e `Arta/ArtaSetup171.exe` sotto `diy/`, e `EASE_Focus_v3.1.260` con i due installer del servizio di database AFMG sotto `room/`. I percorsi che le sottofasi da 8.5 a 8.7 dichiarano sono quindi corretti e non vanno toccati.

Il database dei GLL è presente e coincide con il censimento documentato fino all'ultimo numero: 221 file totali, 174 con estensione `.gll`, 451 MB. È una conferma che il trasferimento della fase 1 fu completo e che il censimento fu scritto sui fatti.

I prefix esistenti sono due, cioè `~/.wine` in uso e `~/.wine-prima-di-wine10`, che è la copia di sicurezza presa prima della migrazione a Wine 10 e va conservata finché la fase 8 non è chiusa. I tre prefix a 64 bit che le sottofasi successive nominano non esistono ancora, il che è corretto: un prefix si crea al primo comando che lo usa, quindi non c'è nulla da preparare in anticipo.

*Una osservazione che apre il microstep successivo e non questo.* Fra le chiavi materializzate in MS-094 c'è `InitialDir`, che vale `C:\Program Files\RDTeam\AKABAK\AKABAK Examples`, cioè la finestra di apertura e salvataggio parte dentro la cartella degli esempi, che sta dentro `Program Files`. Per aprire un esempio è comodo; per salvare il proprio lavoro è il posto sbagliato, perché metterebbe i progetti dell'utente dentro l'albero del programma, dove una reinstallazione li troverebbe in mezzo ai piedi. La procedura nomina già `~/AkabakProjects` come radice di lavoro, quindi la convenzione esiste e manca solo di essere applicata. Non è stato fatto qui perché è una decisione di convenzione e non un passo meccanico della sottofase 8.4, e mescolare le due cose renderebbe questo microstep irripetibile.

Verificato con: `ls` sulla cartella degli esempi nel prefix, che esiste con data 13 agosto 2025; confronto dei conteggi, 632 file su disco contro 681 voci di archivio, spiegato dalle cartelle; confronto dei soli nomi con `comm` e locale fissato, zero differenze; confronto per CRC-32 con uno script eseguito sulla macchina, 632 contro 632 e zero divergenze; `find` sugli eseguibili e gli archivi sotto `electroacoustics`, che individua il corredo sotto `progetto-stanza`; conteggio del database dei GLL, 221 file e 174 `.gll` per 451 MB, coincidente con il censimento; `ls` dei prefix esistenti, due.

Esito: fatto. La sottofase 8.4 è chiusa senza avere eseguito il suo comando, e la ragione è scritta nella procedura perché chi la rileggesse non la esegua per abitudine. Le sottofasi da 8.5 a 8.7 sono pronte per essere eseguite e richiedono la presenza dell'utente, perché sono installatori con interfaccia grafica.

### MS-096 - La cartella di lavoro dei progetti, e una mia guardia che non guardava

Perimetro: creazione della radice di lavoro dei progetti di AKABAK, correzione della chiave `InitialDir` nelle preferenze del prefix, allineamento della convenzione nella pagina della fase 6 e nella procedura. Contiene anche un mio errore di metodo, il cui esito è stato innocuo per fortuna e non per costruzione.

*Perché adesso e non dopo.* La finestra di apertura e salvataggio di AKABAK partiva da `C:\Program Files\RDTeam\AKABAK\AKABAK Examples`, cioè da dentro l'albero del programma. Per aprire un esempio è comodo, per salvare il proprio lavoro è il posto sbagliato, perché i progetti dell'utente finirebbero mescolati ai file del programma, dove una reinstallazione li troverebbe in mezzo e dove nessuno li cercherebbe. Il momento per correggerlo è precisamente questo, prima che esista un solo progetto: farlo dopo significherebbe spostare file e correggere riferimenti invece di cambiare una riga.

C'è una seconda ragione, che discende da ADR-020 e che da sola basterebbe. Il trasferimento verso VACS è impostato su file, e `SpectrumOutputFolder` è lasciata vuota, il che significa cartella del progetto. Dove vivono i progetti decide quindi anche dove si accumulano tutti i dati spettrali prodotti dalle simulazioni, che nella fase 5 saranno molti perché il ciclo si ripete. Lasciare quella radice dentro `Program Files` avrebbe versato là dentro sia i progetti sia i loro risultati.

*Dove, e perché non dove la procedura diceva.* La procedura nominava `~/AkabakProjects`, e la radice scelta è invece `~/Documents/AkabakProjects`. La deviazione ha tre ragioni e non è una preferenza estetica. La prima è la forma del percorso: dentro il prefix la cartella `Documents` è un collegamento simbolico a `~/Documents`, quindi `C:\users\alesop95\Documents\AkabakProjects` e `~/Documents/AkabakProjects` sono la stessa cartella, e il programma la vede come un percorso su `C:` invece che su `Z:`, che è la lettera con cui Wine espone la radice del filesystem. Un programma Windows si aspetta di lavorare su `C:`, e un percorso su `Z:` è la via che più facilmente incontra difetti in programmi vecchi. La seconda è la coerenza con il programma compagno: `VACS.ini` dichiara già `InitialDir=C:\users\alesop95\Documents\`, quindi VACS partiva dalla cartella dei documenti dell'utente e AKABAK no, e i due lavorano in sequenza. La terza è che `~/Documents` vive in `/home`, cioè nella partizione che la reinstallazione conserva e che il backup di `/home` copre, esattamente come vi vive il prefix.

*Come è stata fatta la modifica, e perché non dai menu.* MS-094 ha stabilito che le preferenze di AKABAK vivono in un file di testo e ne ha dato le chiavi. Ne discende che questa modifica è deterministica invece che manuale: uno script eseguito sulla macchina crea la cartella, verifica che la chiave attesa compaia esattamente una volta, la sostituisce, e rilegge il file dichiarando l'impronta prima e dopo. La differenza rispetto a un giro di menu non è la comodità ma la ripetibilità: su un prefix nuovo la stessa riga si riapplica identica, e l'esito è verificabile leggendo un file invece che guardando una finestra. L'impronta è passata da `6c5db196...` a `a402e6a2...`, il file è rimasto di ventotto righe, e la rilettura mostra `InitialDir=C:\users\alesop95\Documents\AkabakProjects` accanto a `ExamplePath` invariata e alle tre chiavi di ADR-020.

*Un mio errore di metodo, con esito innocuo per fortuna.* Prima della modifica avevo messo una guardia che doveva impedire di scrivere il file se AKABAK fosse stato in esecuzione, perché un programma aperto riscrive le proprie preferenze all'uscita e cancellerebbe la modifica. Quella guardia ha fallito due volte nello stesso comando. Ha prodotto un falso positivo, perché `pgrep -f AKABAK.exe` confronta le righe di comando complete e riconosce anche la propria, quindi ha dichiarato il programma in esecuzione mentre non lo era. E soprattutto non ha impedito nulla: l'avevo concatenata con `&&` a un `echo`, che riesce sempre, quindi il comando successivo è partito lo stesso. Il risultato è stato un avviso stampato e ignorato dallo stesso comando che lo stampava.

L'esito è stato corretto perché il programma davvero non era in esecuzione, accertato dopo con `ps -eo pid,comm,args` e con la verifica che non esistessero né processi di Wine né `wineserver`. Ma è stato corretto per fortuna. La forma giusta della guardia evita entrambi i difetti: si spezza il nome nel modello con una classe di caratteri, così che la riga di comando del controllo non corrisponda a se stessa, e si fa uscire lo script con stato diverso da zero invece di limitarsi a stampare.

```bash
pgrep -f "[A]KABAK.exe" > /dev/null && { echo "AKABAK in esecuzione, non modifico"; exit 1; }
```

La regola che ne discende è più generale del caso: una guardia che stampa un avviso ma non interrompe non è una guardia, è un commento, e un controllo che può riconoscere se stesso non è un controllo. Entrambi i difetti hanno la stessa conseguenza, cioè dare l'impressione di un presidio dove non c'è, ed è la terza volta che questo progetto incontra quella conseguenza in forme diverse, dopo il controllo di uscita della fase 7 che interrogava `wine --version` e la lettura dei file dei limiti realtime invece di `ulimit`.

*Che cosa è stato allineato nella documentazione.* La pagina `docs/60-simulazione-finale-akabak.md` descriveva l'albero del progetto sotto `~/AkabakProjects/2Way_Monitor/` e ora lo descrive sotto la radice reale. Nella sottofase 8.4 della procedura l'esempio di percorso alternativo è stato portato alla stessa convenzione, così che la documentazione non suggerisca due radici diverse in due punti.

Verificato con: `ls -l` su `dosdevices` del prefix, che mostra `c:` verso `drive_c` e `z:` verso la radice; `ls -l` sulle cartelle utente del prefix, che mostra `Documents` come collegamento a `/home/alesop95/Documents`; `ls -ld` su `~/Documents`, che esiste ed era vuota; `grep` su `InitialDir` nei due file di configurazione, che mostrava l'asimmetria fra AKABAK e VACS; impronte MD5 del file prima e dopo la modifica; rilettura delle chiavi pertinenti dopo la scrittura; `ps -eo pid,comm,args` e `pgrep` su Wine e `wineserver`, che escludono processi attivi.

Esito: fatto. La radice di lavoro esiste, è vuota, sta in `/home` e il programma vi punta. La fase 8 prosegue dalla sottofase 8.5, cioè l'installazione di VituixCAD, che richiede la presenza dell'utente perché è un installatore con interfaccia grafica.

### MS-097 - Il registro non diceva a che cosa servisse: la catena col progetto, e l'indice delle voci superate

Perimetro: nuova pagina `docs/90-riferimenti/tracciabilita-microstep.md`, estensione della sezione `Convenzione` del registro con due regole nuove e con l'indice delle voci superate, rimandi da `docs/README.md` e da `docs/90-riferimenti/README.md`, e una voce aggiunta a PA-003.

Legame con il progetto: questo microstep non serve alcuna fase del workflow, e lo dichiara invece di inventarsi un legame. Serve il secondo esito dichiarato del progetto, cioè la comprensione: un registro che non dice a che cosa serva ciò che racconta è una cronaca, non una documentazione tecnico-didattica.

*La lacuna, nominata per quello che è.* Fino a MS-096 le voci spiegano il perché tecnico dell'intervento, cioè perché quel comando e non un altro, e quasi mai il perché di progetto, cioè che cosa di due diffusori da costruire dipenda da quell'intervento. Chi legge il registro dall'inizio incontra fini riga, prefix Wine, allineamenti al template e diagnosi di driver grafici, e può legittimamente chiedersi dove siano finiti gli altoparlanti. La lacuna è stata sollevata dall'utente il 2026-09-14 ed è reale.

*Perché la correzione non poteva essere retroattiva nella forma ovvia.* La forma ovvia sarebbe aggiungere un paragrafo a ciascuna delle novantasei voci. È vietata dalla convenzione del registro, che prescrive di non riscrivere una voce passata, e sarebbe sbagliata anche senza quel divieto: novantasei paragrafi scritti a posteriori produrrebbero un registro che sembra essere sempre stato completo, che è lo stesso difetto per cui questo progetto ritira una inferenza invece di cancellarla. La correzione è quindi additiva, in due pezzi: il legame per il passato si fornisce una volta sola e per blocchi in una pagina nuova, e per il futuro diventa un obbligo scritto nella convenzione.

*Che cosa dice la pagina nuova.* Percorre la catena all'indietro, dall'obiettivo all'ambiente, perché è in quel verso che si capisce perché si passa il tempo su Wine: la risposta va misurata al punto di ascolto reale, quindi la stanza entra nel progetto come vincolo, quindi serve uno strumento che metta insieme stanza e diffusore in un solo calcolo, quindi serve Akabak, che è un programma Windows senza equivalente libero, quindi serve Wine, quindi ogni ora spesa a capire perché il comando `wine` sceglie il caricatore sbagliato è la condizione perché la fase 5 sia eseguibile e non un lavoro che ha sostituito il progetto. Poi mappa sette blocchi di microstep sulla fase che servono, dichiarando per ciascuno che cosa sarebbe impossibile senza di esso. Il settimo blocco, quello dell'igiene documentale e degli strumenti, dichiara di non servire alcuna fase, ed è la voce che rende onesta tutta la mappa.

*Una domanda dell'utente, e la sua risposta verificata.* La convenzione di non riscrivere una voce passata solleva il sospetto che il progetto perda pezzi per costruzione. È il contrario, e vale spiegarlo perché la formulazione ingenua suggerisce l'opposto: la regola non lascia in piedi una affermazione sbagliata, la lascia leggibile accanto a quella che la corregge, cosicché resti visibile non solo la conclusione giusta ma anche che cosa si era creduto prima. Il meccanismo è in uso e si misura: il registro contiene sette ritiri espliciti e una decina di superamenti dichiarati.

Alla domanda se la convenzione derivi dal template la risposta è no, verificata e non ricordata. Il template prescrive la forma `append-only` per `memory/progress.md` e per il registro delle decisioni in forma ADR-lite, ma il registro dei microstep non compare affatto in `PROJECT-SYSTEM.md`: zero occorrenze sia di `OPERATIONS-LOG` sia di `microstep`. Il documento e la sua convenzione sono quindi un'invenzione di questo progetto, ispirata alla stessa filosofia che il template applica ai file di memoria. Ne discende una voce nuova in PA-003: il registro dei microstep è un pattern che il template non ha e che vale la pena propagargli, perché risolve un problema che i suoi file di memoria non coprono, cioè il tracciamento dell'intervento singolo con la sua verifica.

*Il difetto reale della convenzione, e la sua correzione.* In un registro che cresce in avanti una voce superata non sa di esserlo: chi legge MS-083 e si ferma là non ha modo di sapere che MS-084 la smentisce, e la responsabilità di scoprirlo ricade sul lettore che arriva in fondo. Il difetto è reale e la sua correzione doveva rispettare la regola: un rimando dentro la voce vecchia sarebbe una riscrittura, un indice a parte non lo è. La sezione `Convenzione` porta ora l'indice delle voci superate, con sette relazioni ricavate dalle dichiarazioni esplicite delle voci stesse e non dalla memoria, più due ritiri che non riguardano voci del registro ma mie spiegazioni scritte altrove, nominati lì perché è lì che un lettore li cerca. L'aggiornamento dell'indice è parte della convenzione e non un lavoro facoltativo.

Verificato con: `grep` sulle dichiarazioni di superamento e di ritiro nel registro, con lettura della riga di perimetro di ciascuna voce coinvolta per ricavare quale voce superi quale, invece di dedurlo dai titoli; `grep` su `PROJECT-SYSTEM.md` del template per `OPERATIONS-LOG` e `microstep`, zero occorrenze, e per `append-only`, che compare per `progress.md` e per il registro delle decisioni; catena di verifica prima del commit eseguita per intera.

Esito: fatto. Il legame col progetto esiste per il passato in forma di mappa e per il futuro in forma di obbligo, e le voci superate sono raggiungibili da un indice invece che da una lettura integrale.

### MS-098 - Il registro dei microstep diventa un pacchetto del template, e il template risulta non committato

Perimetro: creazione del pacchetto opzionale `operations-log` in `E:\template-claude-developing`, con README, modello del registro e modello della pagina di tracciabilità, più la riga nel catalogo `PACKAGES.md`. Chiude la voce di PA-003 aperta poche ore prima. Tocca un repository diverso da questo.

Legame con il progetto: questo microstep non serve alcuna fase del workflow dei monitor. Serve il secondo esito dichiarato, cioè la comprensione riutilizzabile: un pattern che qui ha raggiunto novantasette voci resta patrimonio di questo solo progetto finché non entra nel template da cui i progetti nuovi discendono.

*Perché si è fatto adesso e non si è rimandato.* PA-003 prescriveva di non toccare il template da qui, perché è una decisione dell'utente su un altro repository. L'utente l'ha presa esplicitamente il 2026-09-14, chiedendo che il registro esista nel template, quindi la condizione che rimandava l'intervento è caduta. Vale precisare che cosa fosse davvero mancante, perché la richiesta poteva essere fraintesa: in questo progetto ogni microstep è già tracciato e il registro conta novantasette voci; ciò che mancava era il pattern nel template, cioè in ciò che un progetto nuovo eredita.

*La forma scelta, e perché non un'altra.* Il pacchetto è opzionale e vive sotto `.claude/templates/operations-log/`, con la riga corrispondente nel catalogo `PACKAGES.md`, che è il meccanismo con cui il template offre i propri pacchetti a un progetto in fase di inizializzazione o di allineamento. Non è stato toccato `PROJECT-SYSTEM.md`, e la ragione è duplice: il template non descrive là i pacchetti opzionali, e quel file era appena tornato identico fra template e progetto in MS-091, quindi modificarlo avrebbe riaperto una divergenza il giorno stesso in cui era stata chiusa.

*Che cosa contiene il pacchetto, e quale parte è la sola non ovvia.* Il modello del registro porta la convenzione nella forma generalizzata, cioè identificativo progressivo, data, titolo, perimetro, legame con lo scopo, verifica ed esito, con gli stati `fatto`, `bloccato` e `aperto`, e la regola `append-only`. La parte che vale l'estrazione sono però i due presidi, perché non sono teorici: vengono entrambi da difetti osservati sul campo in questo progetto. Il primo è la dichiarazione del legame con lo scopo, che nasce da un registro diventato illeggibile come cronaca di sistemistica, rilevato dall'utente in MS-097. Il secondo è l'indice delle voci superate, che nasce dalla constatazione che in un registro che cresce in avanti una voce smentita non sa di esserlo, e che un rimando dentro di essa sarebbe una riscrittura vietata dalla convenzione stessa.

Il gate del pacchetto dichiara anche quando non adottarlo, ed è la parte che ne evita l'abuso: non in un progetto di solo codice applicativo, dove alla domanda su come si sapesse che funzionava rispondono meglio i test, e non in un progetto piccolo dove basta il work log di sessione, perché un registro che nessuno aggiorna è peggio della sua assenza in quanto suggerisce una copertura che non c'è.

Il terzo file è il modello della pagina di tracciabilità, e il suo gate è stretto: si istanzia soltanto in un progetto che abbia già molte voci prive del legame con lo scopo, cioè come correzione additiva del passato, e non in un progetto nuovo, dove quella dichiarazione la porta ogni voce.

*Una scoperta collaterale che vale più del pacchetto, e riguarda il template e non questo progetto.* Eseguendo `git status` nel template per verificare che cosa avessi aggiunto, risultano ventuno file modificati e quattro non tracciati, tutti non committati. Fra essi ci sono `PROJECT-SYSTEM.md`, i cinque strumenti tipografici alla radice e nel pacchetto, `md-unwrap.py`, `CASE-STUDIES.md`, i due pacchetti `alignment` e `anonymization`, e la regola `chat-non-e-memoria.md`. Sono esattamente i file da cui MS-091 ha preso le versioni nuove.

La conseguenza va enunciata con precisione perché cambia la lettura di MS-091. Quel microstep aveva concluso che il template fosse avanti rispetto a questo progetto, ed è vero sul disco; non è vero nella storia di git, dove quel lavoro non è mai entrato. Chi clonasse oggi `template-claude-developing` non riceverebbe né la regola `chat-non-e-memoria.md`, né la riparazione degli apostrofi orfani in `fix-accents.py`, né i due pacchetti, né ora il registro dei microstep. La correzione portata qui da MS-091 resta valida, perché veniva da file reali e verificati; ciò che va corretto è l'idea che il template li conservi. Il template ha lo stesso difetto che questo progetto ha avuto due volte questa settimana, cioè lavoro concluso e lasciato non committato, e la conseguenza è più grave là perché il template è la sorgente da cui altri progetti discendono.

Verificato con: `ls` della cartella del pacchetto nel template, tre file creati; `grep -c` su `PACKAGES.md` per la riga nuova, una occorrenza; `git -C E:/template-claude-developing status --short`, che elenca ventuno file modificati e quattro non tracciati, fra cui la cartella del pacchetto appena creata.

Esito: fatto per la creazione. Resta all'utente il commit nel template, che è un altro repository e la cui storia non è governata da questo progetto; la voce corrispondente di PA-003 è aggiornata di conseguenza e non chiusa, perché un pacchetto creato e non committato non è ancora propagato.

### MS-099 - Wine crea il prefix ma non le cartelle che lo contengono, e la fase 7 non poteva funzionare

Perimetro: diagnosi del fallimento del primo comando della sottofase 8.5, creazione della cartella `~/wineprefixes` sulla macchina, correzione della fase 7 della procedura, e correzione di una affermazione di MS-098 sullo stato del template.

Legame con il progetto: serve la fase 4a, cioè la progettazione del crossover con la direttività in VituixCAD, che è il programma che decide come woofer e tweeter si sommano attorno alla frequenza di incrocio. Senza un prefix a 64 bit quel programma non si installa, quindi questo microstep è ciò che sblocca la sottofase 8.5.

Il sintomo è stato `wine: chdir to /home/alesop95/wineprefixes/vituixcad64 : No such file or directory`, restituito da `wineboot -u` su un prefix che doveva essere creato in quel momento. Il messaggio è preciso e va letto come dice: Wine non stava cercando di creare la cartella, stava cercando di entrarci.

La causa è che Wine crea la cartella del prefix ma non le cartelle che la contengono, e `~/wineprefixes` non esisteva affatto su questa macchina, perché è il primo prefix che vi si crea dopo la reinstallazione: l'unico esistente, `~/.wine`, sta direttamente nella cartella dell'utente. La verifica è stata fatta con un prefix usa e getta invece che ragionando: creata la sola cartella padre, lo stesso comando risponde `wine: created the configuration directory` e produce `dosdevices` e `drive_c`. Il prefix di prova è stato poi rimosso.

*Il difetto non era del mio comando soltanto, ed è la parte che vale.* La fase 7 della procedura crea i quattro prefix con quattro righe di `winecfg`, e nessuna delle precedenti crea `~/wineprefixes`. Chi eseguisse la fase 7 su una macchina ricostruita da zero fallirebbe al primo comando esattamente come è fallito questo, e con lo stesso messaggio, che non nomina la causa. È la stessa famiglia di difetti che questo progetto ha già incontrato più volte, cioè un comando prescritto che non può riuscire nell'ambiente in cui la procedura dice di eseguirlo, ed è l'ennesima conferma che una procedura non eseguita è una procedura non verificata. La fase 7 porta ora la creazione della cartella come primo passo, con la ragione accanto.

*Una correzione a MS-098, che ho scritto ieri sulla base di una lettura parziale.* Avevo registrato che il template avesse ventuno file modificati e quattro non tracciati, tutti non committati, e ne avevo tratto che chi lo clonasse oggi non riceverebbe nulla di quel lavoro. Il `git status` completo, letto dall'utente, mostra un dato che il mio non mostrava: il template non è su `main` ma sul ramo `pacchetto-allineamento`, e quel ramo è allineato con il proprio remoto. La correzione ha due parti. La prima è che il lavoro non è appeso a un disco solo per la parte già committata su quel ramo, perché il ramo è pubblicato. La seconda è che i ventuno file modificati restano modifiche del solo albero di lavoro, quindi per essi l'affermazione resta vera. Ne discende una conseguenza in più che non avevo visto: anche quando quei file saranno committati, resteranno su un ramo di lavoro, quindi non raggiungeranno chi clona il template finché quel ramo non sarà unito al principale. La propagazione di PA-003 non si chiude con un commit ma con una unione.

Verificato con: lettura del messaggio di errore, che parla di `chdir` e non di creazione; `ls -ld` su `~/wineprefixes`, assente; creazione della sola cartella padre e riprova con un prefix usa e getta, che risponde `created the configuration directory` e produce `dosdevices` e `drive_c`; rimozione del prefix di prova; lettura della fase 7 della procedura, che crea quattro prefix e non crea mai la cartella che li contiene; `git status` del template fornito dall'utente, che dichiara il ramo `pacchetto-allineamento` allineato con origin.

Va annotato che la prova senza display ha prodotto tre righe `err:ole` sul marshalling delle interfacce: non sono guasti del prefix ma la conseguenza dell'assenza di una sessione grafica, e il prefix è stato creato correttamente lo stesso.

Esito: fatto. La sottofase 8.5 è sbloccata e il suo primo comando può essere rilanciato senza modifiche.

### MS-100 - Il prefix di VituixCAD esiste e non ha alcun runtime .NET, e una inferenza di MS-085 è confermata

Perimetro: creazione del prefix `~/wineprefixes/vituixcad64` e sua caratterizzazione, accertamento della disponibilità di un runtime .NET, lettura dell'output di creazione. Non tocca la documentazione della procedura.

Legame con il progetto: serve la fase 4a, cioè la progettazione del crossover con la direttività. VituixCAD è il programma che decide come woofer e tweeter si sommano attorno alla frequenza di incrocio, ed è una applicazione .NET: senza un runtime non parte, quindi sapere adesso che nel prefix non ce n'è alcuno evita di scoprirlo a installazione fatta.

Il prefix è stato creato e dichiara `#arch=win64` nel proprio `system.reg`, che è l'architettura voluta: VituixCAD è una applicazione a 64 bit anche se il suo installer è PE32 a 32 bit, e la distinzione fra le due architetture è quella spiegata in `wine-corredo-progetto-stanza.md`.

*Che cosa non c'è, e come si è accertato senza fidarsi delle apparenze.* Dentro il prefix esiste una cartella `gecko` sia in `system32` sia in `syswow64`, il che a prima vista suggerisce che il motore di rendering sia installato. Non lo è: la cartella contiene soltanto `plugin`, cioè è un segnaposto che Wine crea comunque. Di Mono non esiste traccia, e `Microsoft.NET` non esiste. Il prefix è quindi privo di qualunque runtime .NET.

A livello di sistema la situazione è la stessa e ha una causa dichiarabile: né `/usr/share/wine/gecko` né `/usr/share/wine/mono` esistono, e `wine-mono` non è disponibile nei repository di Ubuntu, dove `apt-cache policy` non restituisce nulla. Ne segue che Wine non ha una copia locale da installare e deve scaricarla; il sito da cui la prende risponde `HTTP 200` in meno di un secondo, quindi la via è praticabile. Su `winetricks` non esiste un verbo per Mono, mentre esiste `dotnet48`, che scarica e installa il vero .NET Framework di Microsoft.

La conseguenza operativa è che la decisione fra le due vie non va presa adesso ma al primo avvio del programma, che è il momento in cui Wine chiede da sé di scaricare Mono. Se Mono basta, il passo più fragile della fase 8 è evitato; se non basta, si installa `dotnet48` sapendo perché serviva invece di averlo messo per prudenza.

*Una inferenza di MS-085 confermata, e vale registrarlo perché era stata marcata come da verificare.* In quella voce avevo attribuito la riga `err:setupapi:do_file_copyW Unsupported style(s) 0x10`, comparsa all'avvio di AKABAK, a un processo di servizio del prefix e non al programma, deducendolo dal fatto che portasse un identificativo di processo diverso. Era una inferenza dai numeri e l'avevo dichiarata tale. La creazione di questo prefix la conferma per via indipendente: la stessa riga compare cinque volte durante `wineboot -u`, quando nessun programma applicativo è in esecuzione e l'unica attività è la costruzione del prefix. L'inferenza diventa quindi un fatto, e la riga si può classificare come rumore della fase di setup.

*Due altre righe dell'output, classificate perché non allarmino chi le rilegge.* Le righe `err:ole` sul marshalling delle interfacce e su `RpcSs` compaiono alla prima costruzione di un prefix e non impediscono nulla, come mostra il fatto che il prefix sia completo. La riga `err:environ:init_peb starting L"C:\\windows\\syswow64\\rundll32.exe" in experimental wow64 mode` dichiara invece un fatto che vale conoscere prima di installare: in questo prefix a 64 bit i processi a 32 bit girano nella modalità wow64 sperimentale di Wine, cioè senza un caricatore a 32 bit separato. È il modo in cui girerà anche l'installer di VituixCAD, che è a 32 bit, ed è quindi la prima cosa da sospettare se quell'installer si comportasse in modo anomalo.

Verificato con: `grep` su `#arch` in `system.reg` del prefix, che risponde `win64`; `ls` sul contenuto della cartella `gecko` del prefix, che contiene il solo `plugin`; assenza di `windows/mono` e di `windows/Microsoft.NET`; controllo separato di `/usr/share/wine/gecko` e `/usr/share/wine/mono`, entrambi assenti; `apt-cache policy wine-mono`, senza risultati; `curl -I` sul sito di distribuzione di Wine Mono, `HTTP 200`; `winetricks list-all` filtrato, che non offre un verbo per Mono e offre `dotnet48`; `wine --version`, che risponde `wine-10.0`.

Sul metodo va annotata una imprecisione mia, che questa volta non ha prodotto una conclusione sbagliata ma avrebbe potuto. Il primo controllo sulle due cartelle di sistema era `ls cartellaA cartellaB || echo assenti`, che stampa il messaggio anche quando una sola delle due manca: la conclusione era corretta perché mancavano entrambe, ma il controllo non poteva distinguere i due casi. È la terza volta in questa settimana che un controllo scritto in fretta non è in grado di distinguere ciò che deve distinguere, ed è lo stesso difetto della guardia di MS-096 e del rilevamento delle fini riga di MS-088.

Esito: fatto. Il prefix è pronto e caratterizzato. La sottofase 8.5 prosegue con l'installer, e il runtime .NET si decide al primo avvio del programma.

### MS-101 - VituixCAD installato, e il controllo di uscita prescritto avrebbe concluso il contrario del vero

Perimetro: installazione di VituixCAD nel prefix `~/wineprefixes/vituixcad64`, accertamento del percorso reale e dell'architettura dell'eseguibile installato, creazione dello strumento `tools/arch-dotnet.py`, correzione della sottofase 8.5 e della pagina del corredo. Il programma non è ancora stato avviato.

Legame con il progetto: serve la fase 4a, la progettazione del crossover con la direttività. VituixCAD è lo strumento che decide come woofer e tweeter si sommano attorno alla frequenza di incrocio, cioè nella regione dove due driver in controfase producono un buco, che in un monitor da nearfield è il difetto più udibile di tutti.

*Che cosa è stato installato, e dove.* L'installazione è riuscita ed è finita in `C:\Program Files (x86)\VituixCAD`, con tre file: `VituixCAD.exe`, `unins000.exe` e `unins000.dat`. La documentazione del progetto se ne aspettava un'altra, cioè `C:\Program Files\VituixCAD2`, quindi le discrepanze sono due e indipendenti: la vista di `Program Files`, che è quella a 32 bit invece di quella a 64, e il nome della cartella, che è `VituixCAD` senza la cifra.

La ragione della prima è nota e non è un difetto: l'installer è un eseguibile a 32 bit costruito con Inno Setup, e un installer a 32 bit che non dichiari la propria modalità a 64 bit risolve la cartella dei programmi nella vista a 32, che su Windows si chiama `Program Files (x86)` e che Wine riproduce fedelmente. La collocazione è quindi cosmeticamente strana e funzionalmente irrilevante, per la ragione detta sotto, e non va corretta spostando la cartella: sarebbe un intervento che rompe il disinstallatore senza guadagnare nulla.

*Il punto del microstep, ed è il controllo di uscita.* La pagina del corredo prescrive come verifica dell'architettura il comando `file` sull'eseguibile installato, e la documentazione afferma che VituixCAD 2 sia una applicazione .NET a 64 bit, il che è la ragione per cui il prefix è stato creato a 64 bit. Eseguito il controllo prescritto, la risposta è questa.

```
VituixCAD.exe   PE32 executable for MS Windows 4.00 (GUI), Intel i386 Mono/.Net assembly
```

Letta come si legge per un programma nativo, quella risposta dice 32 bit e smentisce la documentazione, e con essa la scelta del prefix. La conclusione sarebbe falsa. Per un assembly .NET l'intestazione PE non determina l'architettura di esecuzione: un assembly compilato *AnyCPU* è anch'esso `PE32` e gira alla larghezza della macchina, quindi a 64 bit su una macchina a 64. Ciò che decide sono tre flag dell'intestazione del runtime CLI, che è la voce 14 della tabella delle directory del PE, e che `file` non guarda.

Letti quei flag, il valore è `0x00000001`, cioè il solo `ILONLY`, con `32BITREQUIRED` e `32BITPREFERRED` entrambi spenti. VituixCAD è quindi AnyCPU e gira davvero a 64 bit: la documentazione aveva ragione, il prefix a 64 bit era la scelta corretta, e il fatto che l'installer abbia messo la cartella nella vista a 32 bit non cambia l'architettura con cui il programma verrà eseguito.

Il controllo prescritto apparteneva quindi alla stessa famiglia di difetti che questo progetto ha già pagato tre volte, cioè un controllo che risponde a una domanda diversa da quella che si sta ponendo e la cui risposta è utilizzabile in entrambi i casi senza distinguerli. È la quarta occorrenza, dopo `wine --version` come prova di un ambiente a 32 bit, la lettura dei file dei limiti realtime invece di `ulimit`, e il nome del kernel come prova della bassa latenza. La differenza rispetto alle altre tre è che qui il controllo non era troppo debole ma proprio sbagliato di segno: avrebbe fatto smontare una configurazione corretta.

*Lo strumento.* Poiché la lettura dei flag CLI non è memorizzabile e non si improvvisa, è stata resa uno strumento del repository, `tools/arch-dotnet.py`. Legge l'intestazione PE, individua la directory del runtime CLI, traduce l'indirizzo virtuale in scostamento nel file attraverso la tabella delle sezioni, e interpreta i tre flag; se l'intestazione CLI manca dichiara il file nativo e riporta l'architettura del formato, che per un nativo è corretta. È di sola lettura, senza dipendenze, e apre il file una volta sola.

È stato verificato su tre casi e non su uno, perché uno strumento provato sul solo caso che lo ha motivato non è provato. Su `VituixCAD.exe` risponde assembly .NET AnyCPU a 64 bit. Su `AKABAK.exe` risponde intestazione CLI assente, eseguibile nativo, 32 bit, che coincide con quanto ADR-016 aveva accertato per altra via. Su `/etc/hostname`, che non è un eseguibile, risponde che manca la firma `MZ` ed esce con codice 2.

*Due letture dell'output dell'installer, registrate perché ricorreranno.* Il primo processo è stato avviato da `Z:\home\alesop95\electroacoustics\progetto-stanza\diy\VituixCAD_setup.exe`, cioè attraverso la lettera che mappa la radice del filesystem Linux: è la conferma pratica che un eseguibile non ha bisogno di stare dentro il prefix per esservi eseguito. Il secondo processo è `VituixCAD_setup.tmp` con l'argomento `/SL5=$1005E,564220,57856,...`, che è la firma di Inno Setup: il primo eseguibile è un contenitore che estrae in una cartella temporanea il vero installatore e gli passa gli scostamenti a cui trovare i dati dentro il file originale. Sapere che i processi sono due e non uno cambia dove si guarda se un giorno una installazione si bloccasse.

Verificato con: confronto del contenuto delle due cartelle `Program Files` prima e dopo l'installazione, con la comparsa della sola voce `VituixCAD` nella vista a 32 bit; `file` sui due eseguibili installati; `python tools/arch-dotnet.py` sui tre casi descritti; elenco dei processi durante l'installazione, che mostra il contenitore e il secondo stadio di Inno Setup; elenco dei processi dopo, che non mostra alcun programma Windows attivo, quindi il programma non è stato avviato.

Sul metodo va annotato un mio errore ripetuto. Il primo controllo sui processi usava `pgrep -f` con il trucco delle parentesi per evitare l'autoriconoscimento, e ha riconosciuto ugualmente la propria riga di comando, perché il modello conteneva altre stringhe presenti nella riga stessa. Il trucco delle parentesi difende dal caso semplice e non da questo. La forma robusta è leggere l'elenco dei processi con `ps` ed escludere esplicitamente la riga del proprio comando, ed è quella usata nella verifica finale. È la seconda occorrenza dello stesso difetto dopo MS-096, e la conclusione allora tratta resta valida: un controllo capace di riconoscere se stesso non è un controllo.

Esito: fatto per l'installazione e per la verifica dell'architettura. Il primo avvio è il passo successivo ed è dove si deciderà la questione del runtime .NET.

### MS-102 - Wine Mono installato, con la versione letta dai binari invece che indovinata

Perimetro: diagnosi del rifiuto di VituixCAD ad avviarsi, individuazione della versione di Wine Mono attesa da questa build, scaricamento del pacchetto, installazione nel prefix `~/wineprefixes/vituixcad64` e verifica. Nessuna modifica alla documentazione della procedura.

Legame con il progetto: serve la fase 4a. VituixCAD è un programma .NET e senza un runtime non parte, quindi questo microstep è la condizione perché lo strumento con cui si progetta il crossover sia utilizzabile.

Il sintomo è stato una riga sola, ed è insolitamente chiara per un messaggio di Wine.

```
err:mscoree:CLRRuntimeInfo_GetRuntimeHost Wine Mono is not installed
```

Conferma quanto MS-100 aveva accertato in anticipo, cioè che il prefix non aveva alcun runtime .NET, e conferma anche che l'accertamento anticipato era servito: senza di esso questo messaggio avrebbe aperto una diagnosi invece di chiuderne una.

*Perché la finestra che offre il download non è mai comparsa.* Il meccanismo esiste, e l'ho verificato leggendo le stringhe di `appwiz.cpl`, dove il testo della finestra è presente per intero, compresa la nota che raccomanda di usare i pacchetti della propria distribuzione. Su Ubuntu però quei pacchetti non esistono, come MS-100 aveva già accertato con `apt-cache policy`. Perché in questa sessione la finestra non sia comparsa non è stato determinato, e lo dichiaro invece di attribuirlo a una causa plausibile: può essere comparsa durante la creazione del prefix senza che venisse notata, oppure la build di Ubuntu può sopprimerla. La domanda non è stata inseguita perché la via manuale è più deterministica di quella interattiva e va documentata comunque.

*Come si trova la versione giusta senza indovinarla.* Ogni versione di Wine si aspetta una versione precisa di Mono, e installarne un'altra produce comportamenti che sembrano difetti del programma. Il numero non va cercato in rete ma letto dal Wine installato, perché è là che è scritto. Le stringhe di un file PE sono codificate a sedici bit, quindi una lettura ingenua non le trova, come è accaduto al primo tentativo; con la codifica giusta il nome del pacchetto compare per intero.

```
wine-mono-9.4.0-x86.msi
wine-gecko-2.47.4-x86_64.msi
```

*Lo scaricamento e la verifica della provenienza.* Il pacchetto è stato preso dal sito di distribuzione di Wine, e prima di usarlo sono state controllate due cose. La dimensione scaricata coincide esattamente con quella dichiarata dal server, cioè 84.639.232 byte, il che esclude un trasferimento interrotto. E i metadati interni del file lo dichiarano per quello che deve essere, cioè un database di installazione MSI intitolato `Wine Mono Runtime` con autore `The Wine Project`, il che è una verifica di identità più forte del nome del file, che chiunque potrebbe scrivere.

*Dove metterlo, e perché questo evita ogni finestra.* Wine cerca i propri componenti aggiuntivi in una cartella di cache dell'utente prima di proporne il download. Mettendo il pacchetto in `~/.cache/wine/`, il comando `wineboot -u` lo trova e lo installa da sé, senza interazione e senza rete. L'installazione è avvenuta in modo pulito e senza bisogno di una sessione grafica, e ha prodotto `C:\windows\mono\mono-2.0` per 233 MB.

Va registrata una conseguenza che vale oltre questo prefix: quella cartella di cache è dell'utente e non del prefix, quindi il pacchetto scaricato una volta serve a tutti i prefix futuri. Ogni altro programma .NET del corredo riceverà Mono senza ripetere lo scaricamento, e la stessa cosa varrà per Gecko se un programma dovesse chiederlo, dato che il nome del pacchetto atteso è ora noto.

*La decisione che questo microstep mette alla prova.* Restava aperta la scelta fra Mono e il vero .NET Framework di Microsoft installato con `winetricks dotnet48`, e il progetto aveva deciso di provare prima il primo. La ragione era asimmetrica: se Mono basta si evita il passo più fragile della fase 8, e se non basta si è pagata solo una attesa e si è guadagnata la ragione per cui quel passo serve. Il verdetto arriva al prossimo avvio del programma.

Verificato con: lettura del messaggio di errore; `strings -el` su `appwiz.cpl` per la versione attesa e per il testo della finestra mai comparsa; `curl -I` sull'indirizzo del pacchetto, che risponde `HTTP 200` con `content-length` di 84.639.232 byte e tipo `application/x-msi`; confronto della dimensione del file scaricato con quella dichiarata, coincidenti; `file` sul pacchetto, che ne dichiara titolo, oggetto e autore; `wineboot -u` nel prefix, senza errori residui dopo il filtraggio del rumore noto; `ls` e `du` su `C:\windows\mono`, che esiste con `mono-2.0` per 233 MB.

Esito: fatto. Il runtime è installato e il primo avvio di VituixCAD è il passo successivo.

### MS-103 - Mono non basta per VituixCAD, e la scommessa si chiude con una ragione invece che con un sospetto

Perimetro: primo avvio di VituixCAD con Wine Mono installato, lettura dell'eccezione, e avvio dell'installazione del vero .NET Framework con `winetricks dotnet48` nel prefix `~/wineprefixes/vituixcad64`.

Legame con il progetto: serve la fase 4a. Senza un runtime che accetti il codice del programma, lo strumento con cui si progetta il crossover non si apre, quindi la fase 4a non è eseguibile.

Il programma non è partito, e l'eccezione è specifica.

```
System.TypeInitializationException: The type initializer for 'Vituixman.KSPub' threw an exception.
  ---> System.InvalidProgramException: Invalid IL code in n9i7aXZkmgvOPW0gfW.Psp6qc4024IfeqC1sh:QH7DUSQmKI (int): IL_020a: brfalse IL_0522
```

*Come si legge, e che cosa dice davvero.* `InvalidProgramException` significa che il runtime ha rifiutato il codice intermedio del programma: non è un file danneggiato né una dipendenza mancante, è il verificatore del runtime che ha giudicato non valida una istruzione, qui un salto condizionato a una certa posizione.

Il dato che spiega il resto sta nei nomi. La classe si chiama `n9i7aXZkmgvOPW0gfW`, il tipo `Psp6qc4024IfeqC1sh` e il metodo `QH7DUSQmKI`, mentre la classe esterna conserva un nome leggibile, `Vituixman.KSPub`. Nomi di quella forma non li scrive nessuno: sono il prodotto di un offuscatore, cioè di uno strumento che dopo la compilazione riscrive un programma .NET rendendolo illeggibile a chi tentasse di decompilarlo. È una inferenza dai nomi e non una misura, ma è una inferenza forte, perché quella forma di identificatore non ha altra origine plausibile.

*Perché questo rompe proprio su Mono.* Gli offuscatori, per rendere difficile la decompilazione, producono deliberatamente codice intermedio ai margini di ciò che la specifica consente, contando sul fatto che il runtime di Microsoft lo accetti. Mono ha un verificatore diverso e più severo su quei margini, quindi rifiuta ciò che l'altro esegue. È un modo di fallire noto e ricorrente per le applicazioni .NET protette, e la sua firma è esattamente questa: una eccezione di codice non valido su un metodo dal nome incomprensibile.

*La scommessa, e perché si chiude bene anche se ha perso.* Il progetto aveva deciso di provare Mono prima di installare il vero .NET Framework, con un ragionamento asimmetrico dichiarato in anticipo: se fosse bastato si sarebbe evitato il passo più fragile della fase 8, e se non fosse bastato si sarebbe pagata una attesa e si sarebbe guadagnata la ragione per cui quel passo serve. È andata nel secondo modo, e il guadagno è reale: `dotnet48` non è più una prescrizione ereditata dalla documentazione del corredo e applicata per prudenza, ma la risposta a un difetto misurato e documentato. Chi rileggesse la procedura fra un anno troverà scritto non soltanto che cosa installare ma perché, e potrà riconoscere il caso in cui quel passo si può saltare.

Il costo effettivo della prova va dichiarato perché la valutazione sia onesta: uno scaricamento di ottantaquattro megabyte, 233 MB occupati nel prefix e qualche minuto. Non è nullo, ed è comunque inferiore al costo di non sapere.

*Che cosa comporta il passo successivo.* `winetricks -q dotnet48` scarica l'installatore ufficiale di Microsoft e lo esegue dentro il prefix, in modo non interattivo. È l'operazione più lunga e più fragile di tutta la fase 8, e comporta la rimozione di Wine Mono dal prefix, perché i due runtime non convivono: winetricks lo fa da sé come parte del verbo. All'avvio lo strumento ha emesso tre avvertimenti informativi, cioè che non riconosce l'architettura di `/usr/bin/wine`, che il prefix è a 64 bit mentre molti verbi installano componenti a 32, e che non è riuscito a determinare il tipo di WoW64. Nessuno dei tre è bloccante, e il terzo è coerente con quanto MS-100 aveva già registrato, cioè che questo prefix usa la modalità WoW64 sperimentale.

Verificato con: esecuzione del programma nel prefix con il runtime Mono installato, che restituisce l'eccezione riportata; lettura dei nomi degli identificatori nell'eccezione; avvio di `winetricks -q dotnet48` in modo non interattivo sulla macchina, con l'uscita registrata in un file di log per poterne seguire l'andamento.

Esito: aperto. L'installazione del framework è in corso e il suo esito va verificato riavviando il programma.

### MS-104 - Il pop-up al login era l'aggiornamento automatico di Firefox, e sulla scrivania non c'è nulla da vedere

Perimetro: diagnosi di due osservazioni dell'utente sulla macchina, cioè un avviso comparso e scomparso troppo in fretta per essere letto al nuovo accesso, e l'assenza di qualunque novità sulla scrivania dopo l'installazione di VituixCAD. Nessun intervento, solo lettura.

Legame con il progetto: nessuno diretto, e lo dichiaro. È igiene della macchina di lavoro: un evento non spiegato su di essa resta un sospetto, e un sospetto costa attenzione a ogni sessione successiva finché qualcuno non lo chiude.

*Il pop-up.* Il registro di sistema dell'utente mostra, alle 15:23:28, quattro righe consecutive del demone di KDE che dichiarano di avere soppresso delle notifiche perché troppe e troppo simili in rapida successione. È quindi accertato che una raffica di avvisi sia stata generata e in parte scartata dal sistema, il che spiega perché sia stata percepita come un lampo. Il contenuto di una notifica non finisce nel registro, quindi da solo quel dato non basta.

La causa si ricava dalla coincidenza di tre eventi nello stesso intervallo di pochi secondi. Alle 15:23:33 il sistema chiude il processo di Firefox, riportandone il consumo su cinque giorni di attività. Alle 15:23:34 entra in scena il componente di integrazione di snap con la scrivania, che da quel momento tenta ogni secondo di aggiornare un indicatore di avanzamento sul lanciatore e viene bloccato dal profilo di sicurezza, il che è un difetto noto di quel componente sotto Plasma e non un problema della macchina. E l'elenco delle operazioni di snap riporta, alle 15:23 di oggi, un aggiornamento automatico del pacchetto `firefox`.

La ricostruzione coerente è quindi questa: il gestore dei pacchetti snap aveva un aggiornamento di Firefox in attesa e non poteva applicarlo mentre il programma era in esecuzione; alla disconnessione Firefox si è chiuso, e al nuovo accesso l'aggiornamento è stato applicato con la relativa notifica, che il sistema ha mostrato e in parte soppresso. Non ha alcuna relazione con il lavoro su Wine, e non richiede alcun intervento: al momento della verifica non risultano né aggiornamenti di sistema in attesa, con `apt` che riporta zero pacchetti, né snap da aggiornare.

Va detto che cosa resta non provato, perché la ricostruzione è coerente ma indiretta: il testo dell'avviso non è recuperabile dal registro. Se in futuro dovesse ricapitare, il modo di leggerlo senza ricostruzioni è lo storico delle notifiche di Plasma, accessibile dal vassoio di sistema, che conserva gli avvisi recenti con il loro testo.

*La scrivania.* L'installazione di VituixCAD non ha creato alcuna icona sulla scrivania, e non è un difetto: l'installer ha creato la sola voce di menu, che esiste in `~/.local/share/applications/wine/Programs/VituixCAD/VituixCAD.desktop`. La scrivania contiene ancora le sole quattro voci preesistenti, cioè i due lanciatori di AKABAK e di VACS, il collegamento `Progetto-stanza` e la cartella dei progetti di Ardour, esattamente come MS-083 le aveva lasciate.

Non ho aggiunto un lanciatore sulla scrivania e la ragione è che sarebbe prematuro: il programma non parte ancora, e un lanciatore che non funziona è peggio di nessun lanciatore. Va inoltre ricordato che i lanciatori di questo progetto hanno già dato un problema di forma, cioè invocavano il comando sbagliato per la loro architettura, quindi quando se ne creerà uno andrà scritto con il comando giusto per il suo prefix e verificato cliccandolo, non solo scrivendolo.

Verificato con: `journalctl --user` sull'intervallo, che mostra la soppressione delle notifiche, la chiusura del processo di Firefox e l'attività del componente di integrazione di snap; `snap changes`, che riporta l'aggiornamento automatico di `firefox` alle 15:23 di oggi; `snap refresh --list`, che dichiara tutto aggiornato; `apt list --upgradable`, che riporta zero pacchetti; `ls` sulla scrivania e ricerca delle voci di menu create dall'installer.

Esito: fatto. Entrambe le osservazioni sono spiegate e nessuna richiede un intervento.

### MS-105 - VituixCAD si apre con .NET 4.8, e la dipendenza prescritta è ora verificata invece che ereditata

Perimetro: installazione del .NET Framework 4.8 nel prefix `~/wineprefixes/vituixcad64` con `winetricks -q dotnet48`, rimozione automatica di Wine Mono, primo avvio riuscito del programma, e aggiornamento della pagina del corredo e della sottofase 8.5 con la dipendenza verificata. Chiude la sottofase 8.5.

Legame con il progetto: serve la fase 4a. VituixCAD è lo strumento con cui si progetta il crossover, cioè la rete di filtri che divide il segnale fra woofer e tweeter, e con cui si verifica come le due risposte si sommano attorno alla frequenza di incrocio anche fuori asse. Da questo microstep in avanti quella fase ha il proprio strumento funzionante.

*Che cosa ha fatto l'installazione.* Il verbo `dotnet48` di winetricks ha scaricato ed eseguito l'installatore ufficiale di Microsoft dentro il prefix, in modo non interattivo. Ha rimosso Wine Mono, perché i due runtime non convivono e la rimozione è parte del verbo. Ha scritto `C:\windows\Microsoft.NET\Framework\v4.0.30319` con 435 file, ha registrato le sostituzioni di libreria necessarie con due passaggi di `regedit`, uno nella vista a 32 bit e uno in quella a 64, e ha lasciato un file marcatore `dotnet48.installed.workaround` che serve a winetricks per sapere che il verbo è stato applicato. Il prefix è passato da poche centinaia di megabyte a 2,1 GB, che è il costo reale di questa dipendenza e va conosciuto prima di replicare l'operazione su altri prefix.

*L'esito.* Il programma si avvia. L'eccezione `InvalidProgramException` che Mono produceva su un metodo offuscato non compare più, e il processo resta vivo, il che distingue un avvio riuscito da un avvio che termina subito. La scommessa dichiarata in MS-095 e chiusa in MS-103 è quindi completamente risolta: Mono non basta per questo programma, `dotnet48` sì, e la prescrizione della pagina del corredo passa da ereditata a verificata. Chi rileggerà la procedura troverà scritto non soltanto che cosa installare ma perché, e saprà riconoscere il caso in cui quel passo si può saltare, cioè un programma .NET non offuscato.

*Due righe dell'avvio, classificate.* La prima è `mscorsvw.exe` avviato in modalità WoW64 sperimentale: è il servizio con cui .NET precompila le proprie librerie in codice macchina, gira in secondo piano dopo una installazione nuova e si esaurisce da solo; la sua presenza al primo avvio è attesa e non è un difetto.

La seconda merita più attenzione perché nomina una assenza reale.

```
err:winediag:ntlm_check_version ntlm_auth was not found. Make sure that ntlm_auth >= 3.0.25 is in your path.
err:ntlm:ntlm_LsaApInitializePackage no NTLM support, expect problems
```

NTLM[^1] è il vecchio protocollo di autenticazione di rete di Windows, e Wine lo implementa appoggiandosi a un programma esterno, `ntlm_auth`, che su Ubuntu sta nel pacchetto `winbind` e che su questa macchina non è installato. La conseguenza va dimensionata invece di essere temuta: quel protocollo serve a un programma che si autentichi verso un dominio Windows, una condivisione di rete o un server aziendale, e VituixCAD non fa nulla di tutto ciò, perché è uno strumento di simulazione che lavora su file locali. L'avviso è quindi innocuo in questo contesto, e il pacchetto non è stato installato perché aggiungere una dipendenza per zitto un messaggio è il genere di intervento che questo progetto evita. Va però registrato dove diventerebbe rilevante: se un programma del corredo dovesse in futuro accedere a una risorsa di rete autenticata, quella riga passerebbe da rumore a causa, e la soluzione sarebbe installare `winbind`.

*Un mio errore, terza occorrenza dello stesso difetto.* Durante l'attesa avevo verificato se l'installazione fosse terminata con `pgrep -f winetricks`, che ha risposto affermativamente per nove minuti dopo la fine reale, perché riconosceva la propria riga di comando: la stringa cercata compariva nel comando che la cercava. È la terza volta, dopo MS-096 e MS-101, e le prime due correzioni erano insufficienti: il trucco di spezzare il nome con una classe di caratteri difende solo dal caso più semplice. La forma che funziona davvero, e che è stata usata per la verifica finale, non usa `pgrep` ma legge l'elenco dei processi e scarta esplicitamente la riga del proprio comando.

```bash
ps -eo pid,args --no-headers | awk "/VituixCAD\.exe/ && !/awk/ {print \$1}"
```

La regola generale, ormai pagata tre volte, è che un controllo il cui criterio compare nel controllo stesso non è un controllo, e che la difesa non è rendere il criterio più astuto ma escludere esplicitamente il proprio processo.

Verificato con: `winetricks -q dotnet48` eseguito in modo non interattivo con l'uscita registrata su file; conteggio dei file in `Microsoft.NET\Framework\v4.0.30319`, 435; presenza del marcatore `dotnet48.installed.workaround`; assenza di `C:\windows\mono`, rimosso come atteso; `du` sul prefix, 2,1 GB; avvio del programma senza eccezioni; `ps` con esclusione della propria riga, che mostra il processo vivo.

Esito: fatto. La sottofase 8.5 è chiusa e la fase 8 prosegue con la 8.6, cioè EASE Focus 3.1.260 con il servizio di database AFMG e il database dei GLL.

[^1]: *NTLM*, NT LAN Manager - protocollo di autenticazione di rete di Windows, precedente a Kerberos e ancora usato da condivisioni e server legacy; Wine non lo implementa direttamente ma si appoggia al programma esterno `ntlm_auth`, distribuito su Ubuntu nel pacchetto `winbind`.

### MS-106 - Il diluvio di righe dopo il primo avvio: che cos'è, perché finisce da sé, e la prova che è finito

Perimetro: classificazione dell'uscita del terminale dopo il primo avvio di VituixCAD, verifica che il fenomeno si sia esaurito e che il programma sia utilizzabile. Nessun intervento sul sistema.

Legame con il progetto: serve la fase 4a, e serve in un senso preciso. Il programma del crossover funziona, ma il suo primo avvio produce centinaia di righe che sembrano errori: senza una classificazione scritta, chiunque ripercorra questo setup si fermerà a chiedersi se qualcosa sia rotto, e il tempo speso a chiederselo è esattamente ciò che questa documentazione esiste per risparmiare.

*Il fenomeno.* Subito dopo il primo avvio riuscito, il terminale si è riempito di due righe che si alternano per centinaia di ripetizioni.

```
err:environ:init_peb starting L"C:\windows\Microsoft.NET\Framework\v4.0.30319\mscorsvw.exe" in experimental wow64 mode
err:ole:ifproxy_release_public_refs IRemUnknown_RemRelease failed with error 0x800706be
```

*Che cos'è `mscorsvw.exe`.* È il servizio di generazione delle immagini native di .NET, comunemente chiamato ngen[^1]. Il suo compito discende direttamente da come .NET funziona: un programma .NET contiene codice intermedio che va tradotto in istruzioni macchina, e farlo ogni volta che il programma parte costa tempo all'avvio. Dopo una installazione del framework, quel servizio traduce in anticipo le librerie di sistema e ne salva il risultato su disco, cosicché gli avvii successivi siano più rapidi. È quindi un lavoro una tantum e per definizione temporaneo.

La ragione per cui compare centinaia di volte è che il servizio non è un processo unico e longevo: lavora a code, avvia un processo per ciascun gruppo di librerie da precompilare, lo lascia terminare e ne avvia un altro. Ogni avvio produce una riga, perché Wine annota l'avvio di ogni processo a 32 bit nella modalità WoW64 sperimentale, che è quella di questo prefix come MS-100 aveva registrato.

*La riga che l'accompagna.* `IRemUnknown_RemRelease failed with error 0x800706be` riguarda COM, cioè il meccanismo con cui due processi Windows si scambiano oggetti, e il codice di errore corrisponde a una chiamata remota interrotta. È il sintomo atteso della situazione descritta sopra: i processi del servizio nascono e muoiono in rapida successione, e ogni volta che uno muore le maniglie che altri processi tenevano verso di esso diventano invalide. Non è una anomalia ma la conseguenza meccanica di un ciclo di vita breve.

*La prova che è finito, e non l'impressione.* La distinzione conta, perché un diluvio di righe che smette di scorrere può significare due cose opposte, cioè che il lavoro è finito oppure che si è bloccato. La verifica è stata fatta contando i processi invece di guardare il terminale: `ps` non trova alcun `mscorsvw.exe` attivo, il carico della macchina è tornato basso, e il processo di VituixCAD è vivo da oltre quindici minuti. Le tre letture insieme dicono che la precompilazione si è esaurita da sé e che il programma sta funzionando, che è esattamente ciò che il terminale da solo non poteva dire.

*La conseguenza pratica, per chi ripercorre questo setup.* Il fenomeno è atteso e non richiede alcun intervento, ma va previsto perché altrimenti si interviene per errore, tipicamente interrompendo il programma nel mezzo della precompilazione. Si presenta una volta sola per prefix, dopo l'installazione del framework, e non si ripete agli avvii successivi. Chi volesse un terminale leggibile può semplicemente ignorarne l'uscita, che non contiene informazioni utili in questa fase, oppure avviare il programma dal suo lanciatore invece che da riga di comando una volta che il lanciatore esisterà.

Va segnalato che lo stesso fenomeno si ripresenterà sul prefix di EASE Focus se anche quello richiederà il framework, quindi la classificazione scritta qui vale per la sottofase successiva e non solo per questa.

Verificato con: `ps` con esclusione della propria riga, che non trova processi `mscorsvw.exe` attivi; `ps` sul processo di VituixCAD, vivo da quindici minuti e trentasette secondi; `uptime`, che riporta un carico tornato a valori di riposo.

Esito: fatto. Il fenomeno è classificato, si è esaurito da sé, e il programma della fase 4a è funzionante.

[^1]: *ngen*, Native Image Generator - il servizio con cui .NET traduce in anticipo il codice intermedio delle librerie in istruzioni macchina e ne salva il risultato, per accorciare i tempi di avvio dei programmi che le usano.

### MS-107 - EASE Focus installato, ed è a 32 bit: il prefix a 64 è giusto ma non per la ragione scritta

Perimetro: creazione del prefix `~/wineprefixes/easefocus64`, installazione di EASE Focus 3.1.260 con l'installatore principale, accertamento dei percorsi e delle architetture reali dei due eseguibili installati, verifica dello stato di registrazione del servizio di database. L'installatore separato del servizio non è stato eseguito e la sua necessità resta da accertare.

Legame con il progetto: serve due fasi e non una. EASE Focus simula la copertura acustica di diffusori a partire da modelli GLL forniti dai costruttori, quindi serve alla fase 3 come termine di confronto per la stanza e alla fase 8, quando il monitor autocostruito esisterà e si vorrà confrontarne il comportamento con quello di prodotti commerciali. Il database dei GLL, 451 MB, è il materiale su cui quel confronto si fa.

*Una conferma che arriva gratis.* Alla creazione del prefix Wine ha installato Mono da sé, come mostrano le righe che nominano `removeuserinstalls-x86.exe` e `installinf-x86.exe` sotto `C:\windows\mono\mono-2.0\support`. È la conferma della previsione fatta in MS-102: il pacchetto scaricato una volta e messo nella cache dell'utente serve a tutti i prefix futuri, senza scaricamenti né finestre. Vale registrarlo perché era una previsione e non una constatazione, e ora è verificata.

*La scelta fatta nell'installatore.* Alla schermata `Setup Type` è stato scelto `Typical` invece di `Custom`. La ragione non è la comodità: `Custom` avrebbe permesso di spostare le cartelle dati e la posizione dei file di licenza, ma il percorso in cui il programma cerca i GLL non è ancora noto e va letto dalle sue preferenze al primo avvio. Scegliere i valori predefiniti e poi misurarli è preferibile a sceglierli al buio, ed è la stessa logica con cui in MS-095 non si è spostato il pacchetto degli esempi di AKABAK.

*Che cosa è stato installato, e dove.* L'installatore, di tipo InstallShield con un passaggio da `msiexec`, ha prodotto due componenti in due viste diverse di `Program Files`, e la distinzione non è casuale. Il programma sta in `C:\Program Files (x86)\AFMG\EASE Focus 3\`, insieme a una cinquantina di librerie. Il servizio di database sta invece in `C:\Program Files\AFMG\AFMG Database Service\`, cioè nella vista a 64 bit, con `AFMGDatabaseService.exe` e `AFMGDatabaseUtility.exe`.

*La misura che corregge la documentazione, ed è l'opposto del caso precedente.* Lo strumento `tools/arch-dotnet.py`, scritto in MS-101 proprio per questo genere di domanda, dà due risposte diverse sui due eseguibili.

```
EASE Focus 3.exe        PE32, assembly .NET, flag 0x00000003, 32BITREQUIRED acceso
                        architettura reale: x86, gira sempre a 32 bit
AFMGDatabaseService.exe PE32+, intestazione CLI assente, eseguibile nativo
                        architettura reale: 64 bit
```

Il programma principale è quindi a 32 bit e basta, non AnyCPU: il flag `32BITREQUIRED` è acceso, il che significa che pretende i 32 bit anche su una macchina a 64. È l'esito opposto a quello di VituixCAD, che con lo stesso formato `PE32` risultava AnyCPU a 64 bit, e i due casi insieme mostrano perché lo strumento serve: `file` avrebbe risposto `PE32` a entrambi, cioè la stessa cosa per due situazioni opposte.

Ne discende una correzione alla documentazione che non cambia la scelta ma ne cambia la ragione, e la distinzione conta perché una ragione sbagliata non sopravvive al primo caso diverso. La procedura prescrive per EASE Focus un prefix a 64 bit, e il prefix a 64 bit è effettivamente necessario: non però perché il programma sia a 64 bit, dato che non lo è, ma perché il servizio di database è un eseguibile nativo a 64 bit, e un prefix a 32 bit non potrebbe eseguirlo affatto. Il programma principale, da solo, sarebbe andato benissimo in un prefix a 32 bit. È anche la spiegazione del perché la documentazione prescrivesse la variante `x64` del servizio: quella prescrizione era corretta e la sua ragione era quella giusta, mentre la ragione attribuita al prefix era sbagliata.

*Lo stato del servizio, e la domanda che resta aperta.* La procedura prescrive, dopo l'installatore principale, di eseguire separatamente quello del servizio di database che sta nella sottocartella `AFMGDatabaseService_x64`. L'installatore principale ha però già installato il servizio, quindi quella prescrizione va verificata invece di essere eseguita per abitudine.

Lo stato accertato è intermedio e va descritto con precisione. I file del servizio ci sono. La configurazione c'è, sotto la chiave di registro `Software\AFMG\AFMG Database Service` con una sottochiave `Programs Sharing`. Ma nessun servizio Windows risulta registrato: una ricerca fra le chiavi dei servizi di sistema del prefix non trova alcuna voce che nomini AFMG. Questo è coerente con l'avvertenza che la procedura stessa porta, cioè che sotto Wine un servizio Windows non gira come servizio di sistema ma come processo dentro il prefix.

La domanda se l'installatore separato serva ancora non si decide leggendo il registro ma provando il programma, ed è esattamente ciò che la procedura prescrive di fare in caso di dubbio: se il programma lamenta l'assenza del database, allora il servizio va installato o avviato; se non lo lamenta, l'installatore separato è ridondante e la procedura va corretta. Il passo successivo è quindi il primo avvio, che serve anche a leggere dalle preferenze il percorso in cui il programma cerca i GLL, dato che quel percorso decide dove andranno copiati i 451 MB del database.

Verificato con: elenco delle due viste di `Program Files` nel prefix, con i due componenti in viste diverse; `find` sugli eseguibili installati; `python tools/arch-dotnet.py` su entrambi, con gli esiti riportati sopra; ricerca nel registro del prefix delle chiavi che nominano AFMG, 187 occorrenze, nessuna delle quali è una registrazione di servizio di sistema; `du` sul prefix, 1,6 GB.

Esito: fatto per l'installazione. Restano aperti il primo avvio, la lettura del percorso dei GLL e la decisione sull'installatore separato del servizio.

### MS-108 - Anche EASE Focus rifiuta Mono, e il modo di fallire è diverso ma la causa è la stessa famiglia

Perimetro: primo avvio di EASE Focus nel prefix `~/wineprefixes/easefocus64` con il solo Mono installato, lettura dell'eccezione, e avvio dell'installazione di `dotnet48` in quel prefix. Non è stato installato nient'altro di quanto la pagina del corredo prescrive, e la ragione è dichiarata sotto.

Legame con il progetto: serve la fase 3 e la fase 8. EASE Focus simula la copertura acustica di diffusori a partire dai modelli GLL dei costruttori, quindi serve come termine di confronto per la stanza e, a monitor costruito, per confrontare il proprio diffusore con prodotti commerciali.

Il programma non si apre e l'eccezione è questa.

```
System.ArgumentException: A null reference or invalid value was found [GDI+ status: InvalidParameter]
  at s4dth.eqpe.nwrv (System.String tsnb, System.Byte[] tsnc)
  at ef.yxzl.tkqc (System.String vybb)
  ...
  at ef.yyaj..ctor (System.Drawing.Icon vybb)
```

*Come si legge.* La catena delle chiamate termina nel costruttore di un oggetto `System.Drawing.Icon`, cioè nel codice che carica una icona, e l'errore viene da GDI+[^1], che è il sottosistema grafico di Windows incaricato del disegno. Il programma quindi non fallisce facendo acustica: fallisce costruendo la propria interfaccia, prima ancora di mostrarla.

I nomi delle classi e dei metodi sono di nuovo incomprensibili, cioè `s4dth.eqpe.nwrv` e `ef.yxzl.tkqc`, il che dice che anche questo programma è passato per un offuscatore, come VituixCAD.

*Perché è la stessa famiglia di causa, pur essendo un errore diverso.* In VituixCAD Mono aveva rifiutato il codice intermedio, con `InvalidProgramException`; qui il codice viene eseguito e fallisce dentro l'implementazione di una libreria. La differenza è reale e vale spiegarla, perché altrimenti sembra un difetto senza rapporto con il precedente. Mono non è soltanto un traduttore di codice intermedio: è anche una reimplementazione della libreria standard di .NET, e la parte grafica di quella libreria, `System.Drawing`, è storicamente la meno completa, perché poggia su una riscrittura di GDI+ invece che su quella di Microsoft. Il risultato è che un programma che usi funzioni grafiche poco comuni, come il caricamento di una icona da un vettore di byte, incontra un comportamento diverso da quello atteso.

Il denominatore comune è quindi che Mono è una implementazione alternativa, non la stessa cosa in un pacchetto diverso, e che uno scarto di implementazione si manifesta là dove il programma esce dai sentieri battuti, per offuscamento nel primo caso e per uso della grafica nel secondo.

*La decisione, e perché non si installa tutto ciò che la documentazione elenca.* La pagina del corredo prescrive per questo prefix `dotnet48`, `corefonts`, `vcrun2013` e `vcrun2019`. È stato installato il solo `dotnet48`, e la ragione è di metodo, non di risparmio: `dotnet48` risponde a un difetto misurato, cioè questa eccezione, mentre degli altri tre non esiste ancora alcuna prova che servano. Installarli adesso renderebbe impossibile sapere quale fosse necessario, e produrrebbe una documentazione che elenca dipendenze senza saper dire perché, che è precisamente la situazione da cui questo progetto sta uscendo.

La ragione per cui gli altri tre sono comunque plausibili va però registrata, perché non è arbitraria: la stessa pagina spiega che alcuni moduli GLL portano librerie proprie compilate con compilatori diversi, quindi i redistributabili di Visual C++ diventano sospetti quando un GLL specifico non si carica. È un difetto che si manifesterà, se si manifesterà, soltanto quando il database dei GLL sarà in posizione e si proverà ad aprirne uno, cioè in un microstep successivo e non in questo.

Verificato con: avvio del programma nel prefix con il solo Mono installato, che restituisce l'eccezione riportata; lettura della catena delle chiamate fino al costruttore di `System.Drawing.Icon`; avvio di `winetricks -q dotnet48` su questo prefix in modo non interattivo, con l'uscita registrata su file.

Esito: aperto. L'installazione del framework è in corso e il suo esito va verificato riavviando il programma.

[^1]: *GDI+*, Graphics Device Interface Plus - il sottosistema grafico di Windows per il disegno bidimensionale, le immagini e i caratteri; Mono lo reimplementa in una libreria propria, che è la parte della sua libreria standard storicamente meno completa.

### MS-109 - Per EASE Focus il framework era necessario ma non sufficiente: il blocco è GDI+ di Wine

Perimetro: secondo avvio di EASE Focus nel prefix `~/wineprefixes/easefocus64` dopo l'installazione di `dotnet48`, lettura della nuova eccezione, e confronto con quella prodotta da Mono. Nessun altro intervento.

Legame con il progetto: serve la fase 3 e la fase 8, cioè il confronto con modelli GLL di diffusori commerciali. Finché il programma non si apre, quel confronto non è possibile.

*Che cosa è cambiato, e che cosa no.* L'installazione del framework ha prodotto un effetto misurabile: l'eccezione non è più la stessa. Con Mono era `System.ArgumentException: A null reference or invalid value was found [GDI+ status: InvalidParameter]`; con .NET 4.8 è `System.Runtime.InteropServices.ExternalException: A generic error occurred in GDI+`. Sono due messaggi diversi prodotti da due implementazioni diverse della stessa libreria, il che conferma che il runtime è davvero cambiato e che `dotnet48` è stato installato correttamente.

Ciò che non è cambiato è la catena delle chiamate, identica fino all'ultimo elemento: il programma fallisce dentro il costruttore di `System.Drawing.Icon`, chiamato da `ef.yyce.Main()`, cioè nel punto in cui costruisce la propria icona prima ancora di mostrare qualunque finestra.

*La conclusione, e perché rovescia la diagnosi di MS-108.* In MS-108 avevo attribuito il fallimento all'incompletezza della libreria grafica di Mono, ed era una spiegazione plausibile che l'esito ha smentito: sostituita la libreria di Mono con quella di Microsoft, il fallimento resta nello stesso punto. La causa non è quindi l'implementazione .NET della grafica ma lo strato sottostante, cioè GDI+ come Wine lo fornisce. Il framework di Microsoft non porta con sé un proprio GDI+: si appoggia a quello del sistema, che qui è la reimplementazione di Wine.

Va detto con chiarezza che `dotnet48` non è stato inutile: senza di esso il programma falliva comunque, quindi era necessario. Non era però sufficiente, e la distinzione fra necessario e sufficiente è precisamente ciò che l'esperimento ha misurato. Questo è anche il motivo per cui installare in blocco tutte le dipendenze prescritte sarebbe stato un errore di metodo: avrebbe prodotto lo stesso fallimento senza dire quale componente avesse cambiato qualcosa e quale no.

*Il candidato successivo, dichiarato come ipotesi.* Il rimedio standard per un fallimento di GDI+ sotto Wine è sostituire la reimplementazione di Wine con la libreria originale di Windows, operazione che `winetricks` esegue con il verbo `gdiplus`. È una ipotesi ragionevole e non una certezza, e va provata come tale: se il programma si apre, la causa era quella; se fallisce ancora, la causa sta più a fondo e la diagnosi riprende dalla catena delle chiamate. Non è stata provata in questa sessione perché la sessione si chiude qui.

*Una nota sul rumore, che ora è classificato.* L'avvio ha prodotto di nuovo centinaia di righe che nominano `mscorsvw.exe`, cioè il servizio di precompilazione di .NET, esattamente come MS-106 aveva previsto per il prefix successivo. La previsione si è avverata e la classificazione scritta là vale qui senza ripeterla: è lavoro una tantum che si esaurisce da sé e non va interrotto.

Verificato con: avvio del programma nel prefix con `dotnet48` installato, che restituisce `ExternalException: A generic error occurred in GDI+` invece della `ArgumentException` di Mono; confronto delle due catene di chiamate, identiche fino al costruttore di `System.Drawing.Icon`; presenza delle righe di `mscorsvw.exe` attese dopo una installazione nuova del framework.

Esito: bloccato. Dipende da una prova non ancora eseguita, cioè la sostituzione di GDI+ con la libreria originale di Windows tramite `winetricks -q gdiplus` nel prefix `~/wineprefixes/easefocus64`, seguita da un nuovo avvio.

### MS-110 - EASE Focus si apre: la causa era GDI+ di Wine, il servizio di database si avvia da sé e i 451 MB non vanno copiati

Perimetro: installazione di `gdiplus` nel prefix `~/wineprefixes/easefocus64` con `winetricks -q gdiplus`, avvio riuscito del programma, accertamento della natura e dello stato del servizio di database AFMG, e misura della cartella del database dei GLL vista dall'interno del prefix. Conferma l'ipotesi dichiarata in MS-109 e risolve la domanda lasciata aperta in MS-107. Non chiude la sottofase 8.6, per la ragione dichiarata in fondo.

Legame con il progetto: serve la fase 3 e la fase 8. EASE Focus simula la copertura acustica di diffusori a partire dai modelli GLL dei costruttori, quindi serve come termine di confronto per la stanza e, a monitor costruito, per confrontare il proprio diffusore con prodotti commerciali. Da questo microstep in avanti quel confronto ha il proprio strumento aperto, anche se non ancora alimentato.

*L'ipotesi era giusta, e la sua conferma vale più della comodità di averla azzeccata.* Sostituita la reimplementazione di GDI+ di Wine con la libreria originale di Windows, il programma si apre. La diagnosi di MS-109 reggeva su un ragionamento indiretto, cioè che due implementazioni .NET diverse fallissero nello stesso punto con due messaggi diversi, e un ragionamento indiretto resta una ipotesi finché un esperimento non lo sostiene. L'esperimento lo sostiene, quindi la catena delle dipendenze di questo programma sotto Wine è ora nota e misurata invece che ereditata da una pagina: serve `dotnet48`, che da solo non basta, e serve `gdiplus`, che da solo non è stato provato ma che senza il framework non avrebbe potuto bastare a sua volta, dato che con Mono il fallimento precedeva il disegno.

*Che cosa fa davvero quel verbo, perché il suo costo sorprende.* `winetricks -q gdiplus` non scarica una libreria: scarica i due pacchetti di aggiornamento di Windows 7 SP1, uno per architettura, per circa 1,8 GB complessivi, e da ciascuno estrae con `cabextract` il solo `gdiplus.dll`. Il file a 32 bit, 1.624.576 byte, finisce in `C:\windows\syswow64`, quello a 64 bit, 2.165.248 byte, in `C:\windows\system32`, e una voce di override dichiara a Wine di preferire la libreria nativa alla propria. Che le architetture siano due e non una è la parte che conta qui: MS-107 ha accertato che il programma è a 32 bit e il servizio a 64, quindi in questo prefix servono entrambe, e un verbo che ne avesse installata una sola avrebbe prodotto una correzione a metà, cioè il genere di difetto che si diagnostica male perché qualcosa è cambiato ma non abbastanza.

*Le tre prove dell'avvio, e perché la terza è la più forte.* La prima è l'elenco delle finestre del server grafico, che riporta `[New EASE Focus Project] - EASE Focus 3, Version 3.1.260`. La seconda è la cattura di quella finestra, che mostra l'interfaccia completa e operativa, cioè il pannello delle proprietà di progetto con temperatura, pressione e umidità, la vista dall'alto con l'area di ascolto predefinita, la vista laterale, e le schede dei livelli, della risposta in frequenza e del grafico di distribuzione. La terza, e la più forte, è il registro degli errori del programma stesso, in `C:\users\alesop95\AppData\Local\AFMG\EASE Focus 3\3.1.260.3184\Error.log`: contiene le due eccezioni del 2026-09-14, cioè quella di Mono alle 16:46 e quella di .NET alle 16:56, e nessuna voce successiva. È la prova più forte perché non dipende da ciò che ho osservato io dall'esterno ma da ciò che il programma scrive di sé, e perché un avvio riuscito è esattamente un avvio che in quel file non lascia traccia.

*Il residuo di ieri, che va saputo riconoscere per non scambiarlo per un difetto di oggi.* L'elenco delle finestre riporta anche `Wine Debugger` e `Program Error`, che appartengono al processo dell'istanza fallita il 2026-09-14, viva da oltre ventitré ore con `winedbg --auto` attaccato. Non sono un difetto dell'avvio di oggi: sono la finestra di crash che nessuno ha chiuso, rimasta aperta perché il programma era stato lanciato da una sessione SSH e nessuno guardava lo schermo della macchina. Vale registrarlo perché alla prossima lettura dell'elenco delle finestre quelle due voci suggerirebbero un fallimento appena avvenuto, e sarebbe una lettura sbagliata.

*La domanda di MS-107 ha risposta, ed è l'installatore separato a essere superfluo.* MS-107 aveva accertato che il servizio di database risultava installato dall'installatore principale ma non registrato come servizio di sistema, e aveva lasciato aperta la questione se l'installatore separato sotto `AFMGDatabaseService_x64` andasse comunque eseguito, dichiarando che la si decide provando il programma e non leggendo il registro. La prova è stata fatta e la risposta è netta: otto secondi dopo l'avvio, accanto al processo del programma compare `AFMGDatabaseService.exe`, avviato da esso con la riga di comando `--smallfiles --dbpath "C:\ProgramData\AFMG\AFMG Database Service" --port 27072 --bind_ip 127.0.0.1`, e il programma non lamenta alcuna assenza di database. Il servizio non ha quindi bisogno di essere registrato: lo avvia il programma quando gli serve, che è precisamente il comportamento che la procedura indicava come possibile sotto Wine. L'installatore separato non va eseguito, e la procedura va corretta in questo senso.

Un dettaglio di quella riga di comando merita di essere notato, perché è una buona notizia e non una minuzia: il servizio si lega a `127.0.0.1`, cioè ascolta soltanto da dentro la macchina. Un database che si aprisse sulla rete locale sarebbe una superficie in più su una macchina che ne condivide una con altre, e non lo fa.

*Che cos'è quel servizio, e la conseguenza sul modo in cui il database si alimenta.* I file che il servizio crea sotto `C:\ProgramData\AFMG\AFMG Database Service` sono `mongod.lock`, `local.ns`, `local.0`, una cartella `journal` e un file `KeepAlive` con il suo lucchetto, per 33 MB complessivi. Sono la firma di MongoDB[^1], e l'opzione `--smallfiles` della riga di comando lo conferma. I 33 MB sono spazio preallocato e vuoto, non contenuto: la base di dati è stata creata adesso, al primo avvio, e non contiene ancora nulla.

Ne discende una conseguenza che cambia la forma del lavoro rimanente, e che va dichiarata come ipotesi perché è dedotta e non misurata. Se il catalogo dei diffusori vive in una base di dati a documenti, allora alimentarlo non è copiare file in una cartella ma importarli, ed è plausibile che serva a questo l'eseguibile `AFMGDatabaseUtility.exe` accertato in MS-107 accanto al servizio. Resta una ipotesi finché non la si prova, e la prova è in interfaccia.

*I 451 MB non vanno copiati, e la misura lo dimostra per metà.* Il prefix mappa l'unità `Z:` sulla radice del filesystem Linux, quindi la cartella del database dei GLL, che sta in `~/electroacoustics/progetto-stanza/room/EASE_Focus_3_GLL_Database_2016_10_11`, è già raggiungibile dall'interno del prefix senza copiare nulla. La misura, fatta con `dir` eseguito da `cmd` dentro il prefix, riporta 221 file per 471.669.804 byte al percorso `Z:\home\alesop95\electroacoustics\progetto-stanza\room\EASE_Focus_3_GLL_Database_2016_10_11`, e i 221 file si ripartiscono in 174 modelli `.gll`, 26 librerie `.dll` e 21 file `.bin`.

Ciò che la misura dimostra è la visibilità, non l'uso: che il programma apra un modello da quel percorso resta da verificare in interfaccia. La distinzione va tenuta perché è la stessa lezione di MS-095, dove gli esempi di AKABAK erano già nel prefix e una seconda copia sarebbe stata dannosa invece che ridondante, e perché una copia fatta per abitudine sarebbe mezzo gigabyte occupato due volte su un disco che serve anche alle registrazioni.

Le 26 librerie `.dll` dentro quel pacchetto sono inoltre la conferma concreta dell'avvertenza registrata in MS-108 sui redistributabili di Visual C++: alcuni modelli portano codice proprio del costruttore, compilato con compilatori diversi, e sono quelli i candidati a fallire se `vcrun2013` o `vcrun2019` mancassero. Il difetto, se esiste, si manifesterà aprendo uno di quei modelli e non prima, quindi gli altri tre verbi restano non installati e la loro necessità continua a non essere assunta.

*Il pop-up, che è della stessa famiglia di quello di MS-104.* Insieme alla finestra principale si apre un riquadro `Sign Up for AFMG News`, che chiede se si vogliano notizie sul programma e notifiche sugli aggiornamenti gratuiti, e porta una casella `Don't ask me again`. Non è un errore né un difetto di Wine: è la sollecitazione commerciale che il programma mostra al primo avvio, esattamente come il pop-up di VituixCAD classificato in MS-104. Si chiude spuntando la casella e rispondendo di no.

*Perché la sottofase 8.6 non si chiude qui.* Resta il lavoro che richiede la presenza dell'utente davanti allo schermo della macchina, ed è di due tipi. Il primo è chiudere il pop-up e provare a caricare un modello GLL dal percorso su `Z:`, che è la verifica capace di trasformare in fatto la metà non misurata del paragrafo precedente. Il secondo è osservare, in quella stessa occasione, se il programma offra una funzione di importazione nel proprio database e se lamenti qualcosa, il che deciderebbe l'ipotesi su MongoDB e su `AFMGDatabaseUtility.exe`. Finché quelle due cose non sono fatte la sottofase resta aperta, e dichiararla chiusa perché il programma si apre sarebbe la forma tipica di ottimismo che questo registro esiste per evitare.

Verificato con: `winetricks -q gdiplus` sul prefix, con l'uscita registrata su file, che estrae e installa le due varianti della libreria nei due percorsi e imposta l'override; `ls -l` sui due file installati, 1.624.576 byte in `syswow64` e 2.165.248 byte in `system32`; avvio del programma in modo distaccato con `DISPLAY` e `XAUTHORITY` nella forma di MS-093; `wmctrl -l`, che elenca la finestra principale con titolo e versione; cattura della finestra con `import` e sua lettura; `cat` su `Error.log`, che non porta voci successive a quelle del 2026-09-14; `ps` con la riga di comando completa, che mostra il servizio di database avviato dal programma otto secondi dopo; `ls -la` e `du -sh` sulla cartella del servizio, 33 MB con la firma di MongoDB; `dir` eseguito da `cmd` dentro il prefix sul percorso `Z:` della cartella dei GLL, 221 file per 471.669.804 byte, con la ripartizione per estensione contata separatamente.

Esito: fatto per l'avvio, che era il blocco. La sottofase 8.6 resta aperta e dipende da due verifiche in interfaccia, cioè il caricamento di un modello GLL dal percorso su `Z:` e l'osservazione del comportamento del programma verso il proprio database.

[^1]: *MongoDB* - base di dati a documenti, cioè che conserva record a struttura libera invece di righe in tabelle; i suoi file caratteristici sono un `mongod.lock` e una coppia di file per ogni base di dati, qui `local.ns` e `local.0`, e l'opzione `--smallfiles` ne riduce la dimensione dei blocchi preallocati.

### MS-111 - L'interfaccia non si guida da remoto sotto Wayland, e il server X privato che lo rende possibile

Perimetro: installazione di `xdotool` e `xvfb` sulla macchina, tentativi falliti di iniezione di clic e tasti sul display della sessione, diagnosi della causa, avvio di un server X privato su `:9` e riavvio là dentro di EASE Focus, chiusura del riquadro della newsletter, e rimozione dei residui di crash del 2026-09-14. Non riguarda l'acustica e lo dichiara apertamente.

Legame con il progetto: serve la fase 3 e la fase 8 per via indiretta, ed è onesto dirlo così invece di attribuirgli un legame diretto. Le sottofasi da 8.5 a 8.7 comprendono verifiche che si fanno soltanto dentro l'interfaccia dei programmi, e finora erano descritte come lavoro che richiede la presenza dell'utente davanti allo schermo della macchina. Questo microstep rimuove quel vincolo, quindi non fa avanzare il progetto di per sé ma rende eseguibile da remoto il lavoro che lo fa avanzare.

*Il primo tentativo, e perché il suo fallimento inganna.* Installato `xdotool`, la sequenza naturale è attivare la finestra e cliccare la casella `Don't ask me again` del riquadro della newsletter. Ogni comando risponde come se avesse funzionato: `xdotool windowactivate` non dà errore, `xdotool getactivewindow getwindowname` restituisce `Sign Up for AFMG News`, `xdotool getmouselocation` conferma il puntatore alle coordinate chieste. La casella però non si spunta. Provate anche la barra spaziatrice sulla casella, che aveva già il fuoco come mostra il rettangolo tratteggiato attorno alla sua etichetta, e l'acceleratore `alt+d` che la lettera sottolineata dichiara, entrambe sia per iniezione sia per invio diretto alla finestra con l'opzione che usa `XSendEvent` invece di `XTEST`. Quattro forme diverse, nessun effetto e nessun errore.

Un fallimento che riporta successo costa più di uno che riporta errore, ed è la stessa lezione già scritta in questo progetto a proposito del recupero di una pagina web che risponde con un codice di successo e un corpo vuoto. Qui la forma è identica: tutto ciò che si può interrogare dice di sì, e l'unica cosa che conta dice di no.

*La causa, che è strutturale e non un errore di coordinate.* La sessione grafica della macchina è Wayland, e le finestre di Wine vivono dentro XWayland, cioè il server X che Wayland ospita per i programmi che parlano X11. Lo dichiara `xdpyinfo`, che fra le estensioni del display `:0` elenca `XWAYLAND` accanto a `XTEST`. In quella configurazione l'input reale lo governa il compositore Wayland, non il server X: `XTEST` modifica lo stato interno di XWayland, che però non è ciò da cui i client ricevono gli eventi. Le interrogazioni funzionano perché riguardano quello stato interno; l'iniezione no perché l'input vero passa da un'altra parte.

Ne discende una regola generale che vale oltre questo caso: sotto Wayland l'automazione di una interfaccia non si fa con gli strumenti X11, e il fatto che quegli strumenti siano installati e rispondano non significa che funzionino.

*La via che funziona, e che cosa comporta.* Si dà al programma un server X tutto suo, dove non esiste alcun compositore a possedere l'input. `Xvfb` è un server X senza schermo fisico: si avvia su un display libero, in questo caso `:9` con una superficie di 1680 per 1050 punti, e lì dentro `XTEST` è l'unica sorgente di input che esista, quindi l'iniezione arriva. La prova è immediata e netta: sul display privato la casella si è spuntata al primo clic, dopo essere rimasta inerte a quattro tentativi sul display della sessione.

Due conseguenze vanno sapute prima e non scoperte dopo, perché su quel display non gira alcun gestore di finestre. La prima è che le finestre non hanno barra del titolo e non si spostano trascinandole, ma si spostano con `xdotool windowmove`, il che serve davvero: la finestra `Manage System Definitions` nasce parzialmente fuori dallo schermo e i suoi pulsanti in basso sono invisibili finché non la si sposta. La seconda è che il fuoco della tastiera segue il puntatore, quindi prima di premere un tasto il puntatore va portato sopra la finestra a cui il tasto è destinato.

*Due trappole operative che sono costate tempo e vanno registrate.* La prima è un comando che uccide se stesso. Terminare il programma con `pkill -f "EASE Focus 3.exe"` non funziona, perché l'opzione confronta l'intera riga di comando e quella riga contiene la stringa cercata anche nella shell che la esegue: il comando uccide la propria shell prima di arrivare al resto, e il sintomo è un comando che non produce alcuna uscita e non fa nulla, che è il modo più fastidioso di fallire. La forma che funziona sottrae la coincidenza rendendo il punto una classe di caratteri, cioè `pkill -f "EASE Focus 3[.]exe"`, che descrive lo stesso processo ma non se stesso.

La seconda è che gli acceleratori da tastiera del programma sono incostanti: `ctrl+i` apre la finestra di importazione alcune volte e altre no, senza differenze visibili nel contesto. I clic sulle voci di menu, invece, non hanno mai fallito. La regola operativa che ne segue è di guidare l'interfaccia con il mouse e di tenere la tastiera per il solo testo, verificando comunque con l'elenco delle finestre che la finestra attesa sia comparsa prima di agire su di essa.

*Il riquadro della newsletter, chiuso e verificato.* Spuntata la casella `Don't ask me again` e risposto di no, il riquadro si chiude. La verifica non è averlo visto sparire ma il riavvio successivo del programma, al quale non è ricomparso: è la differenza fra avere chiuso una finestra e avere registrato una preferenza.

*I residui del 2026-09-14, rimossi.* Le finestre `Wine Debugger` e `Program Error` che MS-110 aveva classificato come residui appartenevano al processo dell'istanza fallita il giorno prima, viva da oltre ventitré ore insieme al proprio debugger e alla propria console. Terminati i tre processi, le finestre sono sparite e l'elenco riporta ora soltanto ciò che appartiene all'istanza corrente.

Verificato con: `xdpyinfo` sul display `:0`, che elenca l'estensione `XWAYLAND`, e sul display `:9`, che non la elenca; quattro forme di iniezione provate su `:0` senza effetto e con la casella fotografata invariata dopo ciascuna; `xdotool getactivewindow getwindowname` e `xdotool getmouselocation`, che riportano entrambi lo stato atteso mentre l'input non arriva; avvio di `Xvfb :9 -screen 0 1680x1050x24` e verifica con `xdpyinfo` delle sue dimensioni; clic sulla casella su `:9` con la casella fotografata spuntata subito dopo; riavvio del programma con il riquadro che non ricompare; `pgrep` e `wmctrl -l` prima e dopo la terminazione dei processi residui.

Esito: fatto. Il lavoro in interfaccia dei programmi del corredo è ora eseguibile da remoto, e la sua verifica resta fotografica.

### MS-112 - Il database dei GLL si alimenta per importazione, e l'importazione fallisce: la traccia isola il provider crittografico

Perimetro: esplorazione delle due voci di menu che riguardano i modelli, quattro tentativi di importazione su tre file diversi, lettura del registro degli errori del programma e del registro di Wine, avvio con la traccia del caricamento delle librerie, installazione della libreria dei certificati nativa e nuova prova. Nessun modello è stato importato.

Legame con il progetto: serve la fase 3 e la fase 8. Il confronto della propria stanza e del proprio monitor con diffusori commerciali si fa sui modelli GLL dei costruttori, quindi finché il catalogo resta vuoto EASE Focus è un programma che si apre e non serve a nulla.

*L'ipotesi di MS-110 è confermata, e cambia il ruolo di una misura invece di annullarla.* Il catalogo dei diffusori vive davvero nella base di dati e si alimenta per importazione, non copiando file in una cartella. Lo dicono due cose viste in interfaccia. La finestra `Manage System Definitions` offre soltanto `Remove`, `Export` e `Close`, con i primi due disattivati perché non c'è nulla su cui agire, e nessuna funzione di importazione; l'importazione è una voce di menu a sé, `Import System Definition File`, il cui filtro dichiara `System Definition Files (*.gll)`. Un GLL è quindi il tipo di file atteso, e la cartella su `Z:` resta utile ma cambia natura: non è la posizione da cui il programma legge, è la sorgente da cui si importa. La visibilità misurata in MS-110 non era sbagliata, era la risposta a una domanda diversa da quella che conta.

Lo stato di partenza del catalogo è vuoto, e va registrato perché è il riferimento di ogni prova successiva: la lista dei costruttori contiene la sola voce `[All]` e l'elenco dei sistemi dichiara `There are no items matching your search`.

*Che cosa fallisce, e la forma esatta del rifiuto.* Ogni importazione tentata termina con la stessa finestra, che dice `The following file is no System Definition or not compatible to the current version of the application`, seguita dal nome del file e dall'invito a cercare una versione più recente del programma o a contattare il fornitore del dato.

I tre file provati sono stati scelti per separare ipotesi diverse e non a caso, ed è la parte che dà valore al risultato. Il primo è `AT108ND.gll`, 1.877.866 byte del 2016, cioè un diffusore singolo del database del 2016: il suo rifiuto era compatibile con l'ipotesi che EASE Focus accetti soltanto i modelli che descrivono un sistema orientabile e non un diffusore semplice. Il secondo è `HDL20-A.gll`, 24.734.241 byte dello stesso database, che è un line array e quindi un sistema a tutti gli effetti: il suo rifiuto smentisce quella ipotesi. Il terzo è `2-Way Speaker (v1.1).gll`, 43.335 byte del 2022, che non viene dal database del 2016 ma è stato installato dall'installatore stesso del programma sotto i documenti pubblici del prefix, ed è il più istruttivo dei tre, perché è un file del produttore per questa esatta versione del programma: il suo rifiuto esclude sia l'età del database sia la versione del formato.

*Che cosa non è, accertato per esclusione e non per opinione.* Non è un modulo mancante: il registro di Wine, letto per intero nella finestra temporale dell'importazione, non contiene alcun errore di caricamento di libreria. Non è il servizio di database: è vivo e in ascolto su `127.0.0.1:27072`, verificato con `ss`. Non sono i file: portano la firma `EGLL` nei primi quattro byte e hanno dimensioni plausibili. Non è la libreria dei certificati di Wine: installata quella originale di Windows con `winetricks -q crypt32`, il rifiuto è identico. E non è una eccezione non gestita, perché il registro degli errori del programma non aggiunge alcuna voce: il programma sa di fallire e lo comunica, il che significa che il difetto sta dentro un percorso che il programma prevede.

*Che cosa dice la traccia, e la lettura che ne do.* Avviato il programma con la traccia del caricamento delle librerie attiva e ripetuta l'importazione, nella finestra temporale dell'operazione compare un solo evento pertinente, ripetuto due volte.

```
trace:loaddll:build_module Loaded L"C:\\windows\\system32\\dssenh.dll" : builtin
fixme:dssenh:CPAcquireContext unsupported flags f0000008
trace:loaddll:free_modref Unloaded module L"C:\\windows\\system32\\dssenh.dll" : builtin
```

La libreria `dssenh.dll` è il provider crittografico DSS[^1] di Windows, e `CPAcquireContext` è la funzione con cui un programma ne ottiene un contesto di lavoro. I flag rifiutati valgono `CRYPT_VERIFYCONTEXT` combinato con `CRYPT_NEWKEYSET`, cioè la richiesta di un contesto per la sola verifica insieme alla creazione di un contenitore di chiavi. La lettura coerente con tutto il resto è che il lettore di GLL verifichi la firma digitale del file e che la reimplementazione di Wine di quel provider non accetti quella combinazione, con il risultato che la verifica non si compie e il programma conclude che il file non sia valido.

Va detto con precisione quanto questa lettura sia solida, perché è una ipotesi e non un fatto. È forte per tre ragioni: è l'unico evento crittografico nella finestra dell'operazione, spiega perché il rifiuto colpisca ogni file compreso quello del produttore, e spiega perché il programma fallisca senza alcun errore di modulo. Non è però dimostrata, perché un messaggio di funzionalità mancante è un avviso e non la prova che la chiamata sia fallita in modo fatale, e la prova richiederebbe di sostituire quel provider e osservare il cambiamento.

*I candidati successivi, in ordine di costo.* Il primo è sostituire `dssenh.dll` con l'originale di Windows. Il pacchetto di Windows 7 SP1 già presente nella cache non la contiene, e non è una supposizione: l'elenco completo dei suoi 5503 file è stato letto e non porta quel nome. La libreria esiste però sulla postazione Windows da cui si amministra il progetto, in entrambe le architetture, 138.976 byte nella vista a 32 bit e 187.416 in quella a 64, quindi la prova è eseguibile senza procurarsi nulla. Il secondo è una versione più recente di Wine: la macchina ha `wine-10.0` dai repository della distribuzione, e la pagina sull'ambiente Wine di questo progetto già raccomanda i pacchetti ufficiali di WineHQ proprio per il supporto alle funzioni che i programmi di questo corredo usano. Il terzo sono i redistributabili di Visual C++, che restano nella lista dei plausibili ma sono scesi di rango, perché un redistributabile mancante si manifesterebbe come una libreria che non si carica e nel registro non ce n'è traccia.

*La conseguenza per il progetto, che è un blocco nuovo e non il precedente.* La sottofase 8.6 resta aperta, ma il blocco non è più quello di MS-109. Il programma si apre, l'interfaccia risponde, la base di dati è in piedi e la via di alimentazione è nota: ciò che non funziona è l'atto di alimentarla. È un progresso, perché il perimetro del problema si è ristretto da tutto il programma a una singola chiamata, e allo stesso tempo è un blocco vero, perché senza catalogo le fasi 3 e 8 non possono usare questo strumento.

Verificato con: apertura di `Manage System Definitions`, che mostra il catalogo vuoto e i soli pulsanti `Remove`, `Export` e `Close`; apertura di `Import System Definition File` e lettura del suo filtro, che dichiara `System Definition Files (*.gll)` e `All Files (*.*)`; quattro importazioni tentate su tre file, ciascuna con la finestra di rifiuto fotografata; `ls -l` e lettura dei primi byte dei file, che riportano dimensioni plausibili e la firma `EGLL`; `pgrep` e `ss -ltnp` sul servizio di database, vivo e in ascolto sul solo indirizzo locale; lettura del registro degli errori del programma, che non aggiunge voci; avvio con `WINEDEBUG=+loaddll` e lettura della porzione di registro prodotta dall'importazione, che contiene il solo evento su `dssenh.dll`; `cabextract -l` sul pacchetto di Windows 7 SP1 a 32 bit, 5503 voci, nessuna delle quali è `dssenh.dll`; `winetricks -q crypt32` seguito da una nuova importazione, con esito identico; `wine --version`, che riporta `wine-10.0 (Ubuntu 10.0~repack-12ubuntu1)`.

Esito: bloccato. Dipende da una prova non ancora eseguita, cioè la sostituzione del provider crittografico `dssenh.dll` con la libreria originale di Windows, disponibile sulla postazione, seguita da una nuova importazione.

[^1]: *DSS*, Digital Signature Standard - lo standard di firma digitale a cui appartiene il provider crittografico `dssenh.dll` di Windows; un provider di questo tipo non cifra dati ma calcola e verifica firme, ed è quindi il componente che un programma usa per accertare che un file venga davvero da chi dichiara.

### MS-113 - Il provider crittografico non era la causa: l'ipotesi di MS-112 è smentita dalla sostituzione

Perimetro: copia del provider `dssenh.dll` originale di Windows dalla postazione alla macchina nelle due architetture, installazione nel prefix `~/wineprefixes/easefocus64` con l'override che lo rende preferito, nuova importazione, ripristino della libreria di Wine, ispezione delle opzioni del programma alla ricerca di un registro diagnostico, e verifica della firma dei quattro modelli di esempio installati dal programma. Nessun modello è stato importato.

Legame con il progetto: serve la fase 3 e la fase 8, per la stessa ragione di MS-112, cioè che il confronto con diffusori commerciali si fa sui modelli GLL dei costruttori e il catalogo è vuoto.

*L'esperimento, e perché era quello giusto da fare anche sapendo che poteva fallire.* MS-112 aveva isolato un solo evento anomalo nella finestra temporale dell'importazione, cioè il provider di firma digitale di Wine che rifiuta i flag richiesti con `fixme:dssenh:CPAcquireContext unsupported flags f0000008`, e aveva dichiarato quella lettura come ipotesi forte e non come fatto, aggiungendo che la prova richiedeva di sostituire il provider e osservare il cambiamento. La sostituzione è stata fatta, ed è la ragione per cui questo microstep esiste: una ipotesi che si lascia in piedi senza provarla diventa nel giro di due sessioni una causa creduta vera.

*Che cosa è stato fatto, e in che forma reversibile.* Le due varianti di `dssenh.dll` della postazione Windows, 138.976 byte per i 32 bit e 187.416 per i 64, sono state copiate rispettivamente in `C:\windows\syswow64` e in `C:\windows\system32` del prefix, dopo avere messo da parte le due di Wine, 204.524 e 222.644 byte. L'override è stato dato sulla riga di comando dell'avvio con `WINEDLLOVERRIDES="dssenh=n"` invece che scritto nel registro del prefix, e la ragione è che un esperimento deve potersi annullare senza lasciare tracce: se avesse funzionato lo si sarebbe reso permanente, e non avendo funzionato non c'è nulla da disfare oltre ai due file, che infatti sono stati ripristinati.

*L'esito, che è netto in entrambe le direzioni.* La sostituzione ha funzionato come sostituzione: il registro di Wine dichiara ora `Loaded L"C:\\windows\\system32\\dssenh.dll" : native` invece di `: builtin`, e soprattutto il messaggio sui flag non compare più, il che significa che la chiamata che prima veniva rifiutata ora viene accettata. L'importazione però fallisce esattamente come prima, con la stessa finestra e lo stesso testo.

Ne segue il ritiro dell'ipotesi di MS-112, e va detto senza attenuanti: il provider crittografico non era la causa. Resta vero che quel rifiuto di flag esisteva ed era una anomalia reale; era però una anomalia innocua, cioè il genere di cosa che un registro di traccia mostra in abbondanza e che sembra una causa soltanto perché è l'unica cosa visibile. La lezione generale è che un messaggio di funzionalità mancante in un registro è un candidato e non una causa, e che l'unica cosa che lo promuove a causa è la sostituzione seguita dall'osservazione. Vale anche il rovescio, che è la parte utile: un esperimento negativo ben fatto ha ristretto il campo, perché adesso la crittografia è esclusa per misura e non più soltanto sospettata.

*Due osservazioni raccolte per strada, che vanno registrate perché nessuna è stata cercata.* La prima è che il riquadro della newsletter è ricomparso a questo avvio, benché la casella `Don't ask me again` fosse stata spuntata e benché all'avvio immediatamente successivo a quella spunta, in MS-111, non fosse ricomparso. La preferenza non è quindi stabile, e la ricerca nel registro del prefix sotto la chiave del programma non trova nulla che la riguardi. È un dato che non ha una spiegazione e non gliene va data una: viene registrato perché un programma che non conserva una preferenza banale potrebbe non conservarne altre, e perché chi riprende questo lavoro deve aspettarsi il riquadro a ogni avvio invece di stupirsene.

La seconda è che il programma non offre alcun registro diagnostico. La voce `Options` del menu `File` apre una finestra con sei pagine, e l'ultima, `Environment`, contiene lingua, unità di misura, raggruppamento dei guadagni e una voce `Mode` impostata su `Standard`. Non c'è alcun controllo di verbosità né percorso di registro, quindi la diagnosi successiva non può venire da dentro il programma e deve continuare a venire da fuori.

*Una verifica che rafforza MS-112 invece di indebolirlo.* Poiché il ragionamento di quella voce poggia sul rifiuto di un modello depositato nel prefix dall'installatore stesso, valeva accertarsi che quei file fossero modelli veri e non frammenti temporanei, dato che stanno in una cartella chiamata `Temp`. Tutti e quattro portano la firma `EGLL` nei primi quattro byte, come i modelli del database del 2016, quindi sono file GLL a tutti gli effetti e l'argomento di MS-112 regge.

*Che cosa resta, in ordine di costo.* Il candidato ora più forte è la versione di Wine. La macchina ha `wine-10.0` dai repository della distribuzione, e la pagina sull'ambiente Wine di questo progetto raccomanda da sempre i pacchetti ufficiali di WineHQ, con una avvertenza che qui torna pertinente: non si mescolano le due provenienze, quindi il passaggio è una decisione sull'ambiente e non una prova rapida. Il candidato successivo restano i redistributabili di Visual C++, che continuano a non spiegare l'assenza di errori di caricamento nel registro. Resta infine una via che non è stata ancora tentata e che costa poco, cioè verificare se AFMG distribuisca modelli GLL più recenti del database del 2016 e provarne uno scaricato oggi: non risolverebbe la causa ma direbbe se il problema riguardi tutti i modelli o soltanto quelli prodotti prima di una certa data, e questa distinzione non è ancora stata fatta perché il modello dell'installatore, pur essendo del produttore, è del 2022 e non di oggi.

Verificato con: copia dei due file dalla postazione e loro installazione nel prefix, con le dimensioni verificate dopo la copia; avvio con `WINEDLLOVERRIDES="dssenh=n"` e `WINEDEBUG=+loaddll`, con il registro che dichiara la libreria caricata come `native`; assenza del messaggio sui flag nella porzione di registro prodotta dall'importazione; nuova importazione dello stesso modello `HDL20-A.gll`, con la finestra di rifiuto fotografata e identica nel testo a quelle di MS-112; ripristino delle due librerie di Wine con le dimensioni verificate dopo il ripristino; apertura di `File` e `Options` e lettura delle sei pagine; lettura dei primi byte dei quattro modelli di esempio, tutti con la firma `EGLL`.

Esito: bloccato, e il blocco è lo stesso di MS-112 con un candidato in meno. L'ipotesi sul provider crittografico è ritirata.

### MS-114 - Il rifiuto non dipende dall'età del modello, e i redistributabili non c'entrano: due candidati caduti insieme

Perimetro: scaricamento di un modello GLL pubblicato nel 2026 dal sito di un costruttore, sua importazione, classificazione delle librerie del programma che leggono i modelli, lettura delle loro tabelle di importazione, e ispezione del file di configurazione .NET del programma. Nessun modello è stato importato.

Legame con il progetto: serve la fase 3 e la fase 8, per la stessa ragione di MS-112, cioè che il catalogo dei diffusori commerciali è il materiale su cui il confronto si fa.

*La domanda che questo microstep chiude, e il perché era rimasta aperta.* MS-113 aveva lasciato una verifica a basso costo non fatta: provare un modello scaricato oggi, per sapere se il rifiuto colpisca tutti i modelli o soltanto quelli prodotti prima di una certa data. La distinzione non era oziosa, perché le tre prove precedenti riguardavano modelli del 2016 e del 2022, e una incompatibilità di formato fra un programma e modelli più vecchi di lui è un fenomeno reale e documentato nel messaggio stesso, che nomina esplicitamente la compatibilità con la versione dell'applicazione.

Il modello scelto è quello di un diffusore amplificato pubblicato il 30 gennaio 2026, 1.059.561 byte, con la firma `EGLL` verificata dopo lo scaricamento. È stato rifiutato esattamente come gli altri. Il rifiuto copre quindi modelli del 2016, del 2022 e del 2026, e l'età del modello è esclusa come fattore: qualunque sia la causa, non discrimina per data.

Va registrato anche il modo in cui il materiale è arrivato, perché è la prima volta in questo progetto che una fonte esterna produce un file e non una informazione. Lo scaricamento è stato fatto con `curl` dalla macchina, con uno user agent da browser, e ha risposto con codice 200 e 974.565 byte; l'archivio contiene un solo file. Il materiale sta in `~/electroacoustics/gll-prova-2026` e non è versionato, coerentemente con il trattamento di tutto il corredo.

*Il terzo candidato di MS-108, finalmente misurato invece che assunto.* MS-108 aveva elencato `corefonts`, `vcrun2013` e `vcrun2019` come dipendenze plausibili, con la ragione che alcuni moduli GLL portano librerie proprie compilate con compilatori diversi, e aveva deciso di non installarle finché un difetto non le chiamasse in causa. La misura di oggi chiude la questione per quanto riguarda il programma.

Lo strumento `tools/arch-dotnet.py`, portato sulla macchina per l'occasione, divide le librerie del programma in due gruppi. Quelle che leggono i modelli sono codice gestito: `S4.FormatSpecs.Gll.dll` è un assembly .NET con il flag `32BITREQUIRED` acceso, `S3.GLI.dll` e `Crc32.dll` sono assembly .NET indipendenti dall'architettura, `S4.Cryptography.dll` è un assembly .NET a 32 bit. Native sono soltanto tre librerie, `EaseLAud.dll`, `Nspp5.dll` e `Nelson_Dll.dll`, tutte PE32 a 32 bit, e la lettura delle loro tabelle di importazione con `objdump` dice che cosa chiedono al sistema: la prima nomina `VERSION`, `KERNEL32`, `USER32`, `SHLWAPI`, `OLEACC`, `GDI32`, `WINSPOOL.DRV`, `comdlg32` e `OLEAUT32`, la seconda `KERNEL32` e `USER32`, la terza il solo `KERNEL32`. Nessuna nomina un redistributabile di Visual C++, il che significa che incorporano staticamente la propria libreria di esecuzione.

Ne segue che `vcrun2013` e `vcrun2019` non servono al programma e la loro assenza non può spiegare il rifiuto. Resta vera la ragione originale per cui erano plausibili, e va tenuta distinta: riguarda le librerie che alcuni costruttori distribuiscono dentro i propri modelli, 26 delle quali stanno nel pacchetto del 2016, e quella questione si porrà soltanto quando l'importazione funzionerà e si aprirà uno di quei modelli. È una domanda diversa, rimandata e non chiusa.

Il fatto che il lettore dei modelli sia codice gestito spiega inoltre un dato che finora era soltanto negativo, cioè l'assenza di errori di caricamento nel registro di Wine: un assembly .NET che fallisca non produce un errore di modulo, produce una eccezione che il programma può intercettare, ed è esattamente ciò che si osserva.

*Due osservazioni dal file di configurazione, registrate come tali e non come cause.* Il programma porta un file di configurazione .NET di 55.628 byte con centinaia di impostazioni, e tre di esse riguardano la base di dati: `NoSqlDatabaseName`, `NoSqlGllCollectionName` e `NoSqlServerConnectionString`, tutte e tre con valore vuoto. Non se ne deduce nulla, perché un valore vuoto in quel file può essere sovrascritto a tempo di esecuzione, e la finestra di gestione dei modelli interroga la base di dati senza lamentarsi; sono registrate perché nominano esattamente la parte del programma che fallisce e perché chi riprende la diagnosi vorrà sapere che esistono. La seconda osservazione è che il programma dichiara di essere compilato per il .NET Framework 4.6.1, requisito che la versione 4.8 installata soddisfa.

Il file non contiene alcun interruttore di traccia e alcuna sezione di diagnostica, il che conferma dall'interno ciò che MS-113 aveva constatato dalle opzioni: la diagnosi non può venire da dentro il programma.

*Che cosa resta.* Delle tre cause plausibili elencate a settembre ne sono cadute due misurate, cioè la crittografia in MS-113 e i redistributabili qui, e con esse è caduta l'età del modello. Il candidato che resta è l'ambiente, cioè la versione di Wine, e la sua verifica non è un esperimento rapido ma una decisione: la macchina ha `wine-10.0` dai repository della distribuzione, la documentazione di questo progetto raccomanda da sempre i pacchetti ufficiali di WineHQ, e le due provenienze non si mescolano. Va quindi posta all'utente invece di essere eseguita.

Verificato con: `curl` con user agent da browser sul sito del costruttore, codice 200 e 974.565 byte scaricati; `unzip` e `head -c` sul file estratto, 1.059.561 byte con firma `EGLL`; importazione del modello, con la finestra di rifiuto identica nel testo a quelle precedenti; `python3 tools/arch-dotnet.py` su sette librerie del programma, con gli esiti riportati sopra; `objdump -p` sulle tre librerie native e lettura delle loro tabelle di importazione; lettura del file di configurazione del programma e ricerca al suo interno di sezioni di diagnostica, che non esistono, e delle tre impostazioni sulla base di dati, tutte vuote.

Esito: bloccato. Due candidati sono caduti e la diagnosi si è ristretta all'ambiente; la prova successiva è una decisione dell'utente sulla provenienza dei pacchetti di Wine.

### MS-115 - La catena tipografica lanciata su un perimetro troppo largo, e la regola che ne discende

Perimetro: correzione di un apostrofo in `.claude/context/STACK.md` e ripristino di una correzione analoga in `.claude/templates/context/sub-subproject.md`, che non andava fatta in questo repository. Non serve alcuna fase del progetto e lo dichiara apertamente: è un errore mio e la voce esiste perché la convenzione di questo registro prescrive di scrivere anche quelli.

*Che cosa è successo.* Al termine del lavoro di MS-114 ho lanciato `fix-accents.py` e `fix-dashes.py` passando come percorsi `docs` e `.claude` interi, invece dei soli file che avevo scritto. I due strumenti hanno fatto esattamente il loro mestiere e hanno corretto due difetti reali che stavano lì da prima e che non avevo toccato io: un `e'` in `STACK.md` e un gruppo di sei forme apostrofate in un modello sotto `.claude/templates/`.

*Perché una delle due correzioni era un danno e non un guadagno.* La prima resta, perché `STACK.md` è una scheda di questo progetto e la convenzione tipografica vi si applica: correggerla è ciò che la regola chiede, anche se l'ho fatto per sbaglio. La seconda è stata ripristinata, perché i file sotto `.claude/templates/` sono copie del template `template-claude-developing` e `CLAUDE.md` prescrive esplicitamente di non correggerveli qui: la correzione appartiene alla propagazione all'indietro tracciata come PA-003, e farla in questo repository allarga la divergenza che quella voce esiste per chiudere, trasformando una differenza nota e sanabile in una differenza in più da conciliare.

È la stessa classe di errore di MS-014 e MS-027, cioè uno strumento corretto applicato a un perimetro sbagliato, e il fatto che si ripresenti dopo che la documentazione lo descriveva già dice che descriverlo non basta.

*La regola che ne discende.* La catena tipografica si lancia sui soli file scritti o modificati nel giro di lavoro corrente, elencandoli, e non su una cartella intera. Il lancio su `.` resta legittimo nella sola forma di verifica non distruttiva prima di un commit, cioè con `--check` dove lo strumento lo prevede, perché là serve sapere se qualcosa non rispetti la convenzione senza riscrivere nulla. Su `.claude/templates/` non si lancia mai, in nessuna forma che scriva.

Verificato con: `git status` dopo il lancio, che ha mostrato due file modificati e non attesi; `git diff` su entrambi, che ha mostrato la natura delle due correzioni; `git checkout --` sul solo file del modello, con `git status` che dopo il ripristino non lo elenca più.

Esito: fatto. Una correzione conservata perché legittima, una annullata perché fuori perimetro, e la regola scritta qui invece che ricordata.

### MS-116 - ARTA installato e sottofase 8.7 chiusa, con il limite della modalità dimostrativa misurato invece che rimandato

Perimetro: creazione del prefix `~/wineprefixes/arta64`, installazione di ARTA 1.7.1 guidata in interfaccia dal display privato di MS-111, primo avvio, lettura del testo di licenza sia nella finestra sia nel file di accompagnamento, e controllo di uscita della fase 8 con l'apertura simultanea di tutti i programmi del corredo. Apre PA-014.

Legame con il progetto: serve la fase 8, quella in cui il monitor autocostruito esiste e va caratterizzato. Fino a quel momento ARTA resta inutilizzato, perché la misura acustica la fa REW, che è nativo e non passa da Wine. La sottofase esisteva per avere lo strumento pronto e verificato prima di averne bisogno, non per usarlo adesso.

*L'installazione, senza sorprese.* Il pacchetto `ArtaSetup171.exe` è un PE32 a 32 bit del 2018 costruito con Inno Setup, e produce quindi due processi come già osservato per VituixCAD in MS-101. La destinazione proposta è `C:\Program Files (x86)\ArtaSoftware` ed è stata accettata, per la stessa ragione di MS-101: un installatore a 32 bit risolve la cartella dei programmi nella vista a 32 bit, spostare il risultato romperebbe il disinstallatore, e non c'è alcun vantaggio nel farlo. Il prefix pesa 1,6 GB.

Ciò che si installa sono tre programmi e non uno, e la distinzione serve perché la documentazione del progetto nomina soltanto il primo. `Arta.exe` misura la risposta all'impulso e fa analisi di spettro in tempo reale, `Steps.exe` misura la risposta in frequenza con eccitazione a sinusoide a gradini, `Limp.exe` misura l'impedenza del diffusore e ne stima i parametri. Accanto stanno i tre manuali in formato di aiuto compilato e una cartella di esempio con un solo file.

*Il punto che la procedura aveva lasciato aperto, ora chiuso.* La pagina del corredo dichiarava che ARTA è shareware e che senza registrazione funziona in modalità dimostrativa con limitazioni da verificare al momento dell'uso. La verifica è stata fatta adesso invece che rimandata, e il limite è dichiarato in due posti concordi: la finestra che il programma mostra all'avvio e il file `Readme.txt` accanto all'eseguibile, che lo scrive così, e vale citarlo alla lettera perché una parafrasi lo ammorbidirebbe.

```
The demo mode of the program is fully functional except loading and saving of files.
```

La modalità dimostrativa è quindi pienamente funzionante tranne che per il caricamento e il salvataggio dei file. Si misura, si vede il risultato a schermo, e non lo si conserva.

*La conseguenza per il progetto, che non è piccola e va detta adesso.* Il ruolo che questo progetto attribuisce ad ARTA è produrre un file GLL a partire da un diffusore misurato, cioè esattamente un salvataggio. In modalità dimostrativa quel ruolo non è esercitabile, e nessun accorgimento lo aggira, perché non è una limitazione di funzionalità ma di persistenza. Ne segue che, quando la fase 8 arriverà, o si acquista la licenza o si sceglie un'altra via verso il GLL. Non blocca nulla oggi, perché la fase 8 richiede un diffusore che non esiste ancora, e proprio per questo la decisione va registrata invece di essere presa di corsa fra un anno: è PA-014.

*Una discrepanza minore, registrata perché non risolta.* Il file di accompagnamento si apre dichiarando `ARTA Software, release 1.7.0`, mentre il pacchetto si chiama `ArtaSetup171.exe` e la documentazione del progetto parla di 1.7.1. La spiegazione più semplice è un file non aggiornato dall'autore, ma non è stata verificata leggendo la finestra di informazioni del programma, quindi resta una osservazione e non un fatto.

*Il controllo di uscita della fase 8, eseguito.* La procedura prescrive che Akabak, VACS, VituixCAD, EASE Focus e ARTA aprano la propria finestra, che Akabak sia attivato con il codice esistente e VACS non ne chieda un secondo, che EASE Focus carichi almeno un GLL dal database, e che i prefix siano quattro e non cinque.

Quattro criteri su cinque sono soddisfatti, e il modo in cui è stato verificato il primo merita una riga: i cinque programmi sono stati aperti tutti insieme sullo stesso display, e l'elenco delle finestre li riporta contemporaneamente, cioè `Akabak - (new)` a 1272 per 686, `VACS - (new)` a 992 per 599, `VituixCAD` a 1358 per 710, `[New EASE Focus Project] - EASE Focus 3, Version 3.1.260` a 1432 per 752 e `Untitled - Arta` a 1252 per 753. Aprirli insieme invece che uno per volta non è esibizionismo: è la prova che i quattro prefix convivono senza interferenze, che è precisamente ciò che la separazione in prefix distinti esiste per garantire e che finora era una aspettativa. I prefix sono quattro, cioè `~/.wine` con 838 MB, `arta64` con 1,6 GB, `easefocus64` con 2,7 GB e `vituixcad64` con 2,6 GB, come prescritto.

Il criterio non soddisfatto è quello su EASE Focus, che resta bloccato per la ragione di MS-112 e MS-114, cioè che il catalogo dei modelli non si lascia alimentare. È l'unico residuo della fase 8.

*Che cosa resta non verificabile, e va detto invece di essere taciuto.* L'avvertimento della pagina del corredo sull'accesso di ARTA alla scheda audio sotto Wine non è stato messo alla prova e non lo sarà finché l'interfaccia audio di PA-012 non esisterà. Il programma si apre e disegna, il che dice che l'interfaccia grafica funziona, e non dice nulla sulla latenza né sulla stabilità di una misura dal vivo. La documentazione già indica REW per quel compito, quindi la questione non è urgente, ma non va scambiata per risolta.

Verificato con: `file` sull'installatore, che riporta PE32 per Intel i386; installazione guidata in interfaccia sul display privato, con le schermate di destinazione e di riepilogo fotografate; elenco del contenuto della cartella di installazione, con i tre eseguibili, i tre manuali e la cartella di esempio; `du -sh` sul prefix, 1,6 GB; primo avvio, che apre la finestra di registrazione della licenza, e prosecuzione in modalità dimostrativa, che apre la finestra principale a 1252 per 753 con lo stato `Ready`; lettura del testo di licenza nella finestra e in `Readme.txt`, concordi; apertura simultanea dei cinque programmi del corredo e lettura dell'elenco delle finestre; conteggio e misura dei quattro prefix.

Esito: fatto. La sottofase 8.7 è chiusa, il controllo di uscita della fase 8 è superato in quattro criteri su cinque, e il quinto dipende dal blocco già tracciato su EASE Focus.

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
