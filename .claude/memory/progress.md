# Work-log

> Append-only, in ordine cronologico inverso: la voce più recente in alto. Ogni passo significativo lascia una voce con data, file toccati, motivo e commit di riferimento. Il dettaglio tecnico degli interventi, con l'esito verificato di ciascuno, sta in `docs/OPERATIONS-LOG.md`; qui sta il meta-stato.

## 2026-09-08, ripresa da crash - La carta della reinstallazione, e uno strumento che la rende riproducibile

Commit di partenza: cadf335.

File toccati: `tools/make-scheda-docx.py` nuovo, `docs/10-ambiente/scheda-reinstallazione.md` corretto nella nota di apertura e nella tipografia, `docs/10-ambiente/README.md` con l'indicizzazione della scheda, `.claude/context/STACK.md` con lo strumento nuovo e la correzione dello scopo di `verify-usb-dd.ps1`, `docs/OPERATIONS-LOG.md` con MS-070 e MS-071, `.claude/memory/decisions.md` con ADR-017, `.claude/context/current-work.md` con il fronte nuovo, e `CLAUDE.md` per tre accenti. Fuori dal versionamento: il `.docx` rigenerato in `Downloads` e la copia precedente conservata sotto `_notes/`.

Motivo: la sessione precedente è stata interrotta da un crash di Claude Code mentre si modificava il `.docx` da stampare, e l'utente ha chiesto di riprendere da dove si era rimasti. La macchina va formattata con la chiavetta già pronta, quindi il lavoro residuo era una sola cosa, cioè aggiungere alla scheda una avvertenza precisa prima di stamparla.

Come si è ricostruito lo stato, e vale perché la conversazione non c'era più. Nessuna nota di handoff era stata scritta, quindi la ripresa è poggiata su tre fonti sul disco: lo snapshot in `.claude/memory/index.md`, la coda non committata di `git diff`, e i timestamp dei file, che sono stati la fonte decisiva. Il `.docx` portava l'ora 15:10, la sottofase 4.2 della procedura le 15:12 e la scheda sorgente le 15:14, quindi la carta era indietro di due minuti rispetto alla documentazione. L'estrazione del testo dal `.docx` lo ha confermato: non conteneva né la parola filesystem né la parola riepilogo, cioè mancava esattamente di ciò che la fase 4.2 aveva guadagnato alle 15:12. L'ipotesi su quale fosse l'avvertenza è stata comunque sottoposta all'utente prima di agire, invece di essere data per certa, perché il foglio va in mano a chi azzera il disco.

Esito in sintesi, quattro cose.

La scheda `.docx` è rigenerata e contiene l'avvertenza sul modo concreto in cui il passo irreversibile si sbaglia, cioè che la casella di formattazione si attiva da sé quando si seleziona un filesystem nel menu della riga. L'avvertenza compare in tre punti, e la sequenza operativa passa da dodici a tredici passi perché la lettura della schermata di riepilogo, che nella procedura era una raccomandazione in prosa, è diventata un passo con la sua casella da spuntare: era il controllo più importante della fase e l'unico senza casella. È MS-070.

Il documento di stampa è ora riproducibile, e prima non lo era. Il codice che aveva costruito il `.docx` viveva soltanto nella sessione e il crash lo ha portato via, mentre la scheda tracciata dichiarava uno strumento `tools/make-scheda-docx.py` che non esisteva, cioè un'affermazione falsa in un file versionato. Lo strumento adesso esiste, in sola libreria standard come gli altri, ed è verificato su tre livelli: buona formazione delle cinque parti XML, apertura con un lettore indipendente, e rilettura del testo di tutte le celle.

I dati di licenza di Akabak non entrano nel documento se non lo si chiede, ed è ADR-017. La ragione non è solo di riservatezza ma operativa: alla reinstallazione non servono, perché il codice si reinserisce dal file riservato quando si riapre AKABAK, che è un passo successivo, mentre stamparli metterebbe un codice di attivazione permanente su un foglio che si porta in giro.

Due difetti trovati per strada e chiusi. Lo scopo di `verify-usb-dd.ps1` era ancora dichiarato in `STACK.md` come la sottofase 2.4 della procedura, che MS-069 gli aveva tolto il giorno stesso. E la grafia degli accenti con l'apostrofo, ventotto occorrenze nella scheda più cinque in prosa fra registro e `CLAUDE.md`, è sanata; il perimetro si è ristretto guardando le occorrenze invece dei totali, perché quasi tutte quelle del registro sono esempi citati dentro code span nei microstep che raccontano i difetti degli strumenti tipografici, e correggerle li avrebbe distrutti. È MS-071.

Due errori miei, entrambi a verbale in MS-071. Una sequenza di sostituzioni con `sed` in cui la terza regola ha colpito il risultato della prima, producendo *scegliee*, vista subito perché avevo riletto le righe invece di fidarmi del codice di uscita. E un caso minimo scritto su `C:` invece che sul disco del progetto, che è terminato con l'eccezione cross-disco di PA-003 mentre io ne avevo silenziato lo standard error: stavo per concludere dal file non modificato che lo strumento protegge la prosa, cioè il contrario del vero.

## 2026-09-08 - Sequenza operativa avviata: PA-009 chiusa, immagine 26.04.1 verificata

Commit di partenza: d2905ba.

Avviata l'esecuzione della sequenza operativa passo per passo, su richiesta dell'utente di farli insieme. Passo 1 risultava già fatto, entrambi i repository committati e in pari con origin.

Passo 3 chiuso, ed è PA-009. SMART dell'SSD esterno letto con CrystalDiskInfo elevato e l'opzione `/CopyExit`, che scrive un rapporto su file invece di richiedere uno screenshot. Il Samsung T7 è **sano**: usura zero, riserva al 100 per cento, zero errori di integrità, zero voci nel registro errori. Delle due cause possibili cade il difetto del supporto e resta la rimozione senza espulsione, con 122 spegnimenti non protetti su 742 cicli, su cui va applicato il correttivo che su USB quel contatore si incrementa anche quando l'espulsione è regolare. Le cinque cartelle `FOUND` restano la prova che conta. Il disco non va sostituito. È MS-058.

Registrato l'ostacolo, valido oltre il caso: la lettura SMART richiede privilegi anche su Windows, dove `Get-StorageReliabilityCounter` risponde `PermissionDenied` senza sessione elevata, per la stessa ragione per cui su Linux serve `sudo` su `/dev/nvme0`.

Passo 4 per due terzi. La fonte ufficiale ha corretto la procedura: nella cartella del rilascio convivono la 26.04 e la **26.04.1**, e la seconda è quella da prendere. La procedura nominava la prima in due punti, uno dei quali dentro il comando `dd`. Immagine scaricata, 7.127.195.648 byte, e verificata due volte: firma del file delle somme buona con la chiave `Ubuntu CD Image Automatic Signing Key (2012)`, impronta dell'immagine `OK`. L'ordine delle due verifiche non è indifferente e la fase 2.2 ora ne chiede due invece di una, perché una somma confrontata con un file preso dallo stesso posto dell'immagine non protegge da chi controlli quel posto. Sono MS-059 e MS-060.

Rufus 4.15 portabile scaricato e verificato per firma Authenticode, `Status: Valid`, firmatario `Akeo Consulting`: per un eseguibile Windows è la verifica più forte disponibile, e le note del rilascio non pubblicano somme di controllo. Riscritta la sottofase 2.3 con il vincolo dei 16 GB motivato numericamente, la ragione della modalità DD contro il limite dei 4 GB di FAT32, e l'avvertenza sul rifiutare la formattazione dello spazio residuo che Windows propone a scrittura finita. È MS-061.

Allineate due dichiarazioni di stato superate nella procedura, che dichiaravano non eseguite fasi compiute e chiedevano una riconferma già data.

Passo 2 compiuto: l'utente ha cancellato la copia del corredo sul Desktop, 650 file per 2,3 GB, dopo la riverifica delle impronte. PA-007 chiusa. Immagine e Rufus spostati sul Desktop per scelta dell'utente: essendo uno spostamento fra volumi, cioè una copia più cancellazione, entrambe le verifiche sono state rifatte alla nuova posizione e passano. Percorso aggiornato in quattro documenti. È MS-063.

Trovato nello stesso microstep un difetto di ambiente che aveva fatto fallire due modifiche in modo incomprensibile: un ancoraggio di testo multi-riga scritto con `LF` non trova nulla in un file `CRLF`, e l'albero contiene legittimamente entrambi i formati perché la convenzione prescrive di conservare la fine riga di ciascun file. Ipotesi sbagliata scartata per prima, cioè la codifica: il sorgente è decodificato come UTF-8 comunque, e ciò che sembrava corruzione era la stampa illeggibile su una console `cp1252`.

Da lì un difetto silenzioso più grande, che stavo per committare: i blocchi inseriti in questa sessione erano scritti con `LF` in due file `CRLF`, producendo fini riga miste che nessun controllo del progetto segnalava e che git avrebbe registrato, dato che `core.autocrlf` è `false`. Normalizzati, e aggiunto `tools/check-eol.py` alla sequenza di verifica. Al primo lancio ha trovato un file misto già nella storia del repository, `settings.json`, e sul gemello **otto** file, sette dei quali con esattamente quattro righe anomale: la misura fissa attraverso file di dimensione diversa ha indicato il generatore invece del contenuto, cioè `sync-ambiente.py`, che scriveva l'intestazione di provenienza sempre con `LF`. Corretto lo strumento e ripropagato.

## 2026-09-07, sesta parte - Licenza confermata in interfaccia, fase 0 chiusa, PA-007 detta chiara

Commit di partenza: 0df04bb.

Machine Identifier verificato sulle immagini fornite dall'utente: coincide con il valore conservato sotto `_notes/`, coincide anche il release code, e il programma dichiara `Release Code valid`. Chiude la seconda delle tre voci di PA-005 e con essa la fase 0 nella sostanza, dato che la terza voce, l'esito di `sudo apt update`, è resa irrilevante da ADR-013. È la prova sperimentale che una licenza machine-based sotto Wine resta valida a un anno di distanza, quindi che la reinstallazione pulita non la mette a rischio. È MS-052.

Tre fatti collaterali dalle stesse finestre. L'edizione è **Standard** e non professionale, malgrado l'installer si chiami `AKABAK_Pro_...`: l'edizione la determina il release code, coerentemente con la student license concessa. Il prefix dichiara `NT 10.0 (Build 19043)`, cioè Windows 10, che trasforma in fatto misurato una prescrizione data per uniformità. E la memoria riportata, 2047 MByte su una macchina con 16 GB, è una conferma indipendente di ADR-016, perché è lo spazio di indirizzamento di un processo a 32 bit.

Quella conferma era però disponibile prima dell'indagine che ha stabilito il fatto, nello stesso lotto di screenshot letti per ricostruire la corrispondenza. La lezione, in MS-053, non è leggere tutto: è che quando una premessa regge una decisione, il materiale già in mano va interrogato **su quella premessa**, non solo sul tema per cui era stato raccolto.

Corretto un difetto di verifica introdotto dallo spostamento dell'archivio di backup sul Desktop: lo strumento delle azioni differite cercava un percorso fisso e dichiarava mancante un backup esistente, riportando PA-007 a bloccata per un motivo falso. Ora l'invariante è il nome del file fra più posizioni, con controllo della dimensione. È MS-054, e la lezione è che un errore restrittivo in uno strumento di verifica è peggiore di uno permissivo, perché si crede.

Detto chiaro ciò che era rimasto implicito e che l'utente aveva chiesto due volte: **la copia del corredo sul Desktop si può cancellare adesso.** PA-007 riscritta perché lo dica in apertura.

Ripulite dalle informazioni superate quattro sezioni che dichiaravano pendente lavoro compiuto: la coda del registro dei microstep, che elencava come bloccati passi eseguiti e ripeteva la prescrizione sbagliata sui 64 bit, la sezione finale dello storico Akabak e VACS, le voci residue della fase 0 nella fotografia della macchina, e le sezioni di blocco e prossimo passo del lavoro corrente.

## 2026-09-07, quinta parte - Backup di /home fatto, e Akabak si rivela a 32 bit

Commit di partenza: ba69e0c.

Esito in sintesi, tre cose di peso molto diverso.

PA-008 compiuta: l'utente ha cancellato le sei voci di servizio su `J:`, recuperando 1,2 GiB. I due frammenti maggiori erano di 247 e 206 MB, cioè metà del totale: il filesystem aveva perso qualcosa di sostanzioso, che è un elemento in più a favore di PA-009.

Backup di `/home` eseguito e verificato, quindi fase 1.3 chiusa. Alla domanda se potesse stare sulla stessa macchina la risposta è no: la macchina ha un solo disco con quattro partizioni, e una copia sullo stesso supporto della cosa che protegge non è un backup. Fatto su Windows con `tar` in streaming su `ssh`, 4,4 GB, 13.498 file nell'archivio contro 13.498 sulla macchina, permessi e proprietario numerico conservati. Registrato come ADR-015. Questo sblocca PA-007.

E la scoperta che costa più di tutte: **Akabak è a 32 bit**. Il prefix funzionante dichiara `#arch=win32`, `AKABAK.exe` è PE32 i386, VACS installato è la build a 32 bit, e nel prefix non c'è né winetricks, né .NET, né corefonts. Tre affermazioni del documento sorgente sono false, e tre decisioni consecutive le avevano propagate senza tornare alla fonte: la prescrizione operativa era sbagliata su sei documenti, e se eseguita avrebbe prodotto un ambiente in cui il programma centrale del progetto non parte. Corretto tutto, registrato come ADR-016. Il controllo che l'avrebbe evitato costava un comando, `file` sull'eseguibile.

Chiuse per conseguenza entrambe le lacune dello storico di Akabak e VACS, e confermata come corretta l'ipotesi che l'utente stesso aveva formulato nella corrispondenza del 13 agosto 2025, cioè che il fallimento di VACS dipendesse dalla variante a 64 bit.

Constatato anche che il corredo era già sulla macchina, sulla scrivania, il che corregge in meglio il ragionamento di MS-044 su PA-007, e che il release code di Akabak esiste in chiaro in due posti sulla macchina, quindi anche dentro l'archivio di backup.

## 2026-09-07, quarta parte - SSD esterno misurato, archivi confrontati, Desktop rinviato

Commit di partenza: ba69e0c.

File toccati: `docs/PENDING-ACTIONS.md` con PA-007, PA-008 e PA-009 nuove, `docs/90-riferimenti/pulizia-ssd-esterno.md` riscritta nella sezione sugli archivi, `docs/OPERATIONS-LOG.md` con MS-040 a MS-045, `tools/check-pending-actions.py` con tre difetti corretti e tre voci nuove, `tools/analisi-ssd-esterno.py` nuovo, `.claude/memory/decisions.md` con ADR-014, `_notes/` con i due indici degli archivi.

Esito in sintesi, quattro cose.

Gli archivi di backup su `J:` sono stati confrontati e **nessuno dei due contiene l'altro**: 145.483 voci solo nel vecchio e 80.487 solo nel nuovo, per il rimescolamento di `backup-sviluppo`. Cancellare il vecchio costerebbe 145.478 versioni di file. Cade anche l'ipotesi sulla cartella 3DS come causa della differenza di peso.

La copia sul Desktop **non si cancella adesso**, e la ragione è il conteggio delle copie: oggi le voci utili sono in due posti, cancellare il Desktop le porta a uno, e questo proprio prima di una reinstallazione che tocca le partizioni. La condizione di sblocco è la copia di sicurezza di `/home`, cioè la fase 1.3.

Chiarito un equivoco che riguardava la fiducia: l'agente non ha cancellato nulla su `J:` e non ha eseguito alcuna cancellazione in tutta la sessione. Le nove voci di servizio sono tutte ancora presenti, e le tre che valgono 1,2 GiB sono da fare.

Tre difetti dello strumento delle azioni differite, tutti trovati leggendo l'output che l'utente ha incollato. La chiusura di PA-006 non era stata applicata perché un `assert` era fallito e non avevo controllato il codice di uscita. Su PA-001 lo strumento nascondeva le condizioni permanenti uscendo subito col disco assente. E confondeva disco assente con cartella già cancellata, cioè un ostacolo con l'obiettivo raggiunto.

## 2026-09-07, terza parte - SMART, censimento del corredo, catena di ascolto e pulizia

Commit di partenza: f85480d.

File toccati: `docs/90-riferimenti/censimento-corredo.md` e `docs/75-catena-di-riproduzione.md` nuovi, `docs/10-ambiente/fotografia-macchina-2026-09-07.md` con l'analisi SMART, `docs/PENDING-ACTIONS.md`, `docs/TRANSFER-MANIFEST.md`, `docs/OPERATIONS-LOG.md` con MS-033 a MS-037, `.claude/memory/decisions.md` con ADR-012, `tools/check-pending-actions.py`, i tre indici, e nel progetto gemello `docs/PENDING-ACTIONS.md` nuovo con i suoi due indici. Rimossa `docs/10-ambiente/ubuntu-lts-upgrade.md` da entrambi i progetti.

Esito in sintesi, cinque cose.

Lo SMART è stato letto e il disco è sano: `PASSED`, usura al 9 per cento, riserva di blocchi al 100, errori di integrità zero. La voce che poteva spostare la decisione da installazione a sostituzione del disco è chiusa con esito positivo. Due numeri richiedevano una lettura: le 584 voci nel registro degli errori sono tutte `Invalid Field in Command`, cioè risposte a comandi che il controller non implementa e non errori del supporto, come dimostra `smartctl` stesso che ne genera una mentre gira; i 24 spegnimenti non puliti su 135 accensioni sono invece reali e sono un fattore di rischio da tenere in conto durante la reinstallazione. Emerso anche che il disco ha una vita precedente a questa installazione, con 12.787 ore di accensione contro tredici mesi di sistema.

Il censimento del corredo software è completo. L'inventario testuale dichiara 36 cartelle e tutte e 36 esistono su `J:`, senza cartelle non dichiarate: è completo e accurato, e la sua incompletezza sui file è una proprietà del comando che l'ha generato. Le quattordici voci hanno ora un verdetto ciascuna con la ragione, e il criterio che li decide è stato isolato perché è quello che rende il censimento ripetibile: primario la posizione nel workflow, secondario la sostituibilità con qualcosa di migliore già disponibile, e solo terziario lo stato di licenza. Nessuna delle otto voci scartate è esclusa perché porta una protezione rimossa: è esclusa perché non serve, e ciascuna ha una ragione funzionale che regge da sola.

La catena di ascolto è definita, e la definizione ha una conseguenza non ovvia. Il Rod Rain audio fornisce una uscita a livello di linea su RCA a 2 Vrms, che è un segnale e non una potenza: con monitor attivi la catena è completa, con monitor passivi serve un amplificatore interposto che sarebbe un acquisto. La scelta fra attivo e passivo, che il documento sorgente lasciava aperta, va quindi anticipata alla fase 4a. Registrata come ADR-012, con la seconda conseguenza sulla validità delle misure della fase 8, dove il segnale di prova deve uscire dalla catena di ascolto reale e non da quella di misura.

La valutazione di acquisto di una interfaccia audio è registrata nel progetto gemello, che è dove l'esigenza vive: la Scarlett a due ingressi basta al progetto dei monitor e non alla registrazione multitraccia.

La pulizia ha rimosso la pagina della diagnosi smentita da entrambi i progetti, invece di tenerla con l'avvertenza in apertura, e ha corretto quattro affermazioni obsolete che sopravvivevano come dichiarazioni al presente. La conciliazione fra il far sparire ciò che è sbagliato e il tracciare tutto è questa: le affermazioni sbagliate non restano dove qualcuno le leggerebbe come vere, il record di che cosa era sbagliato resta dove il tracciamento vive.

## 2026-09-07, seconda parte - Accesso aperto, fase 0 eseguita, diagnosi smentita

Commit di partenza: 4863804.

File toccati: `docs/10-ambiente/fotografia-macchina-2026-09-07.md` nuovo, `_notes/fotografia-2026-09-07/` con ventitré file di output grezzo non versionati, correzioni sostanziali a `docs/10-ambiente/ubuntu-lts-upgrade.md` e alle fasi 0, 0.1 e 6 di `docs/10-ambiente/installazione-pulita-26-04.md`, `docs/OPERATIONS-LOG.md` con MS-028 a MS-031, `docs/PENDING-ACTIONS.md` con PA-005 e PA-006, `.claude/memory/decisions.md` con ADR-011 e la marcatura di ADR-006, e i due indici.

Motivo: l'utente ha installato la chiave SSH, sbloccando l'accesso alla macchina che era il vincolo delle due sessioni precedenti. Con l'accesso è diventato possibile eseguire la fase 0 della procedura, cioè mettere alla prova la diagnosi scritta per ipotesi.

Esito in sintesi, e non è quello che mi aspettavo. **Tre delle quattro cause che avevo attribuito al blocco di aggiornamento sono false.** Il salto diretto alla LTS è offerto, e `do-release-upgrade -c` risponde che la 26.04.1 LTS è disponibile. La direttiva è `Prompt=normal` e non `lts`, e il commento dello stesso file di configurazione dichiara che con `lts` su un rilascio non-LTS l'aggiornatore assume `normal`, quindi quella causa non poteva agire nemmeno in principio: la risposta era scritta dentro il file che stavo ipotizzando. Gli archivi della 25.04 sono ancora vivi e rispondono 200, non sono stati spostati su `old-releases`, che sulla stessa risorsa risponde 404.

Il fatto che riorganizza tutto è però un altro: `/var/log/dist-upgrade/` è vuota, quindi **l'aggiornamento non è mai stato tentato**. Non c'era un blocco da diagnosticare. La cronologia di apt lo conferma dall'altro lato, con l'ultima operazione datata 13 agosto 2025, e la simulazione elenca 134 pacchetti pendenti senza conflitti. La lezione metodologica è che avevo costruito una diagnosi elaborata su una premessa implicita nella domanda e mai verificata, cioè che un tentativo fosse stato fatto e fosse fallito.

L'unica parte confermata è la quarta, i fattori di attrito, in forma più grave del previsto: due repository WineHQ attivi contemporaneamente per due rilasci diversi di Ubuntu, più `wine-stable 3.0.1` del 2018 accanto a `wine 9.0`, l'architettura `i386`, una sorgente `file:/cdrom/` residua e un solo prefix Wine condiviso.

Altri due esiti della fotografia. La catena a bassa latenza è attiva e configurata bene, ma il controllo che la fase 6 prescriveva, cioè il nome del kernel, avrebbe dato un falso negativo: il kernel è generico e le proprietà arrivano da `preempt=full` e `threadirqs` sulla riga di comando, con `rtprio 95` per il gruppo audio. Corretto. E la partizione EFI è di 1,1 GB e non dei circa 100 MB che il documento sorgente dichiarava, mentre `/home` usa 3,7 GB su 369.

Conseguenza sulle decisioni. Il primo dei quattro motivi di ADR-006 è caduto, gli altri tre tengono, e se ne aggiunge uno nuovo reso disponibile dai dati. La revisione è ADR-011, ADR-006 è marcata come rivista senza essere riscritta, e la riconferma della scelta è tracciata come PA-006 perché è dell'utente e non mia.

Un riscontro positivo che vale registrare: la cronologia di apt conferma con data e ora la sequenza di installazioni e purghe di Wine che il documento sorgente descriveva. È la prima volta che una affermazione di quel documento viene confermata da una fonte indipendente sulla macchina stessa.

## 2026-09-07, prima parte - Verifica delle copie del corredo, e apertura dell'accesso alla macchina

Commit di partenza: 3eac5f3. Commit di arrivo: da assegnare.

File toccati: `docs/PENDING-ACTIONS.md` con PA-001 riscritta e PA-004 nuova, `docs/10-ambiente/wine-corredo-progetto-stanza.md`, `docs/10-ambiente/installazione-pulita-26-04.md` alla fase 10.3, `docs/TRANSFER-MANIFEST.md`, `docs/OPERATIONS-LOG.md` con MS-024 a MS-027 e la correzione di MS-021 e MS-023, `tools/check-pending-actions.py`, `.claude/memory/decisions.md` con la correzione di ADR-010, e `CLAUDE.md` con la regola nuova sul tracciamento integrale.

Motivo: il disco `J:` è stato collegato, il che ha permesso di verificare la corrispondenza fra le due copie del corredo software, e l'utente ha chiesto di includere anche quel contenuto nel perimetro di installazione. In parallelo è emerso un errore nella documentazione fornita per aprire l'accesso SSH.

Esito in sintesi. Quattro microstep nuovi, da MS-024 a MS-027, e due voci precedenti corrette esplicitamente invece che riscritte in silenzio.

Il risultato principale è una smentita, ed è il motivo per cui questa sessione conta più di quanto la sua lunghezza suggerisca. Le due copie del corredo sono identiche: 650 file per parte, stesse dimensioni, 2.380.021.546 byte per copia, tutte le impronte SHA-256 coincidenti. L'inferenza scritta nella sessione precedente, secondo cui la versione 3.1.10 di EASE Focus esistesse sul solo SSD e le due copie quindi divergessero, era sbagliata: il collegamento è identico su entrambe. Era marcata come probabile e non come certa, che è il minimo, ma restava una supposizione dove bastava leggere un file.

Il tranello che l'aveva alimentata va registrato perché è generale: `du -sh` mostrava differenze vistose fra le due copie, fino a 14 MB contro 5,9 MB sulla stessa cartella, e non erano reali. Quel comando misura lo spazio occupato, che dipende dalla dimensione dei cluster del filesystem e arrotonda per eccesso ogni file; su 650 file l'arrotondamento si accumula. Il criterio giusto è l'impronta del contenuto.

Dalla lettura del collegamento è venuta una scoperta: punta a un quarto disco `G:`, al percorso del workshop K-array, mai menzionato in nessun documento del progetto. Non collegato, quindi non ispezionato, e tracciato come PA-004 a priorità bassa perché la versione da installare è la 3.1.260.

Sul perimetro di installazione, la risposta alla domanda dell'utente è che `J:` non era incluso, perché nel messaggio precedente era nominato con il ruolo opposto, cioè come la copia da cancellare. La richiesta di includerlo non ha però conseguenze pratiche, proprio perché le due copie sono identiche: il piano già scritto le copre entrambe e nessuna voce va aggiunta.

Un errore mio, corretto e documentato come MS-027. Il comando `ssh-copy-id` fornito in un blocco PowerShell non esiste in quella shell: è uno script POSIX presente su Windows solo dentro Git Bash. L'utente ha generato la chiave con successo e il secondo comando è fallito. La causa è l'assunzione che due blocchi per due shell differiscano solo nella sintassi, mentre qui differiva la disponibilità del comando. La fase 10.3 riporta ora tre forme, con l'aggiunta dei permessi espliciti sul file delle chiavi autorizzate, che il servizio SSH pretende e la cui assenza farebbe fallire l'autenticazione senza spiegare perché.

Infine, l'istruzione dell'utente di scrivere in documentazione tutto ciò che passa in sessione è stata resa vincolante in `CLAUDE.md`, con la ripartizione fra i documenti e i tre casi che si è tentati di non scrivere: gli errori, comprese le inferenze smentite da ritirare esplicitamente, e i comandi eseguiti con il loro output reale quando insegna qualcosa.

## 2026-09-04 - Impianto del progetto: allineamento, conversione, ambiente

Commit di partenza: 0df04bb. Commit prodotti: 9e9517e per la prima parte e 3eac5f3 per la seconda, entrambi su origin.

File toccati: `.claude/rules/` tutte e sette le regole, `.claude/PROJECT-SYSTEM.md`, i due prompt di sistema, `.claude/skills/`, l'intero `.claude/templates/`, le tre schede nuove sotto `.claude/context/`, i tre file di `.claude/memory/`, l'albero `docs/` con ventitré file, sei script sotto `tools/`, `.gitignore`, `CLAUDE.md`, `README.md`. Spostato `full_electroacoustics.docx` dalla radice a `_notes/`.

Motivo: il progetto era indietro di sette commit rispetto al template, il documento sorgente non era stato convertito, i materiali pesanti stavano sul disco di sviluppo invece che sulla macchina di lavoro, e il `.gitignore` nascondeva per errore file che devono essere versionati.

Esito in sintesi. Ventitré microstep chiusi con verifica, tracciati come MS-001 a MS-023 in `docs/OPERATIONS-LOG.md`. Dieci microstep progettati e bloccati, elencati nello stesso registro con la fase della procedura a cui corrispondono.

Il blocco è cambiato natura tre volte nel corso della sessione, e la storia è tracciata perché è istruttiva. La macchina risultava di stato ignoto e la prima diagnosi la dava per spenta o su un altro segmento di rete. La lettura corretta l'ha data l'utente: si sospende da sola, e una macchina sospesa non risponde nemmeno alle richieste ARP, quindi scompare del tutto dalla rete invece di rispondere male. Risvegliata, ha risposto al ping con TTL 64 e ha accettato la connessione sulla porta 22, rifiutando l'autenticazione. Il blocco residuo è quindi una singola azione dell'utente, cioè l'installazione di una chiave SSH, che richiede la password una volta sola.

Nella seconda parte della sessione è entrato nel perimetro il corredo software `Progetto stanza (software)`, 2,3 GB sul Desktop della postazione, da far funzionare sotto Wine sulla macchina. L'ispezione diretta dei file, invece della lettura dell'inventario testuale, ha corretto tre affermazioni, ne ha aggiunta una che nessun documento riportava, ha rivelato un passo di installazione mancante ed emendato due decisioni architetturali.

Tre difetti trovati e corretti in questo progetto. Il `.gitignore` con pattern globali invece che ancorati alla radice, che escludeva strumenti e modelli da versionare. La regola di identità git tornata genericizzata dopo la copia dal template, con in più una attribuzione errata del profilo di questo repository. Cinque incoerenze interne al documento sorgente, corrette e segnalate nelle pagine di destinazione invece di essere ricopiate.

Quattro difetti trovati nel template di origine e non ancora propagati all'indietro. Il pacchetto `fix-typography` contiene versioni degli strumenti più vecchie delle copie in `tools/` alla radice del template, quindi istanziare dal pacchetto darebbe strumenti peggiori. I modelli `_notes` sotto `.claude/templates/` non sono versionati perché il `.gitignore` del template li esclude con un pattern globale, quindi un clone del template li perde. Le regole di prudenza di `fix-accents.py` e `fix-missing-accents.py` sono incoerenti fra loro sui file di codice, e la catena dei due lascia un apostrofo orfano su forme come `c'e'`: il danno è già presente in quindici punti dei sorgenti del template. I tre strumenti tipografici terminano con un errore su percorsi cross-disco, difetto che `md-unwrap.py` ha già corretto. Tutti e quattro sono annotati come domanda aperta in `.claude/context/current-work.md`, e gli ultimi due sono diagnosticati con casi minimi in MS-014.

Registro delle azioni differite, nuovo. Tre voci, con le condizioni di sblocco di ciascuna e uno strumento che le verifica. La prima nasce da una richiesta esplicita dell'utente, cioè ricordare di cancellare la copia ridondante del corredo su SSD esterno: un promemoria che vive in una conversazione è perduto, quindi vive in `docs/PENDING-ACTIONS.md` e in `tools/check-pending-actions.py`.

Riconciliazione del documento sorgente: `full_electroacoustics.docx`, 507 paragrafi, 4 tabelle, 1 immagine, circa 10.100 parole. Copertura integrale verificata e documentata in `docs/90-riferimenti/copertura-sorgente.md`. Non trasferiti soltanto 29 paragrafi vuoti, 22 segnaposto e una formula presente solo come immagine, tutti dichiarati uno per uno. Sei incoerenze interne o rispetto ai file sono state corrette e spiegate una per una in una pagina didattica dedicata, divise in quattro tipi con il metodo per riconoscere ciascuno. Il sorgente è stato archiviato sotto `_notes/`, non distrutto, con impronta SHA-256 verificata identica dopo lo spostamento.

## Precedente al 2026-09-04

Il progetto esisteva come impalcatura standard con `CLAUDE.md`, `README.md` e il sistema `.claude/` istanziato, senza documentazione tecnica propria. Il remoto GitHub era già collegato tramite l'alias SSH personale e il repository era in pari. Il materiale di progetto viveva alla radice come file di testo e un documento `.docx`, tutto ignorato da git.
