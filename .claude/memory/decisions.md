# Registro delle decisioni architetturali

> Convenzione ADR-lite, append-only. Ogni decisione non ovvia entra come voce numerata con data, stato, contesto, decisione, motivazione e conseguenze. Una decisione non si cancella e non si riscrive: quando viene superata, si aggiunge una voce nuova che dichiara di superarla e ne cita il numero. Le inferenze non confermate si marcano come da verificare e si promuovono a decisione solo quando una fonte le conferma.

## ADR-001 - Adozione del sistema di progetto portabile

Data: 2026-09-04. Stato: accettata.

Contesto: il progetto necessita di uno stato interamente recuperabile da un clone e di documentazione che resti allineata senza rilettura integrale a ogni sessione.

Decisione: adottare il sistema descritto in `.claude/PROJECT-SYSTEM.md`, con doppio livello documentale tracciato e ignorato, e mantenerlo allineato a `template-claude-developing` come sorgente.

Motivazione: persistenza strutturale su disco indipendente dalla sessione, e controllo umano sul versionamento.

Conseguenze: ogni passo significativo aggiorna schede, snapshot e work-log; commit e push restano manuali.

## ADR-002 - Progettare a partire dalla stanza e non dal diffusore

Data: 2026-09-04, formalizzazione di una scelta già implicita nel documento sorgente. Stato: accettata.

Contesto: il punto di ascolto è in una stanza irregolare, con soffitto spiovente e una parete vicina alle spalle, e non è trattabile acusticamente né riposizionabile per vincoli di arredamento.

Decisione: invertire l'ordine consueto. Misurare la stanza prima, validare un modello geometrico contro quella misura, progettare il diffusore in campo libero in parallelo, e ottimizzare la posizione solo alla fine con i due modelli insieme.

Motivazione: un monitor progettato per essere neutro in campo libero subisce la stanza; qui la stanza è nota e diventa vincolo di progetto invece di disturbo.

Conseguenze: la fase di misura è un prerequisito e non una verifica finale, e va eseguita prima dell'acquisto dei driver. La ripetibilità del setup di misura diventa un requisito, perché la misura della fase 1 e quella della fase 8 devono essere confrontabili a mesi di distanza. Il criterio di successo del progetto è definito al punto di ascolto reale, non in camera anecoica.

## ADR-003 - Wine invece di una macchina virtuale Windows

Data: 2026-09-04, formalizzazione. Stato: accettata.

Contesto: quattro programmi indispensabili al progetto esistono solo per Windows: Akabak, VACS, VituixCAD ed EASE Focus. La macchina di lavoro è Ubuntu Studio.

Decisione: usare Wine con un prefix per programma, e non una macchina virtuale Windows.

Motivazione: tre argomenti indipendenti, tutti verificabili. La catena audio resta quella nativa di Linux con il kernel a bassa latenza, mentre una macchina virtuale aggiungerebbe latenza proprio nella fase in cui si misura il tempo. L'identificativo hardware esposto è quello reale, quindi la licenza machine-based di Akabak sopravvive a reinstallazioni e ricostruzioni dei prefix, mentre in una macchina virtuale sarebbe diverso e andrebbe richiesta di nuovo. Non serve licenza Windows né la manutenzione delle sue patch, perché nessun codice Windows è in esecuzione.

Conseguenze: i guasti hanno la forma di librerie mancanti invece di problemi di driver, e la cura è installare il runtime giusto nel prefix giusto. Un programma che richiedesse un driver in kernel space non funzionerebbe, e per quello servirebbe tornare a una macchina virtuale; nessuno dei quattro programmi del progetto ricade in quel caso. Il backup di un ambiente configurato è una copia di cartella.

## ADR-004 - Un prefix Wine per programma, e nessun prefix a 32 bit

Data: 2026-09-04. Stato: accettata.

Contesto: il documento sorgente registra sia l'uso di un prefix condiviso, che con Akabak è andato bene, sia la buona pratica del prefix separato. Registra anche un guasto reale su `kernel32.dll`, causato da un prefix creato prima che l'architettura a 32 bit fosse dichiarata.

Decisione: un prefix dedicato per ciascuno dei quattro programmi, tutti a 64 bit, e non installare WinISD.

Motivazione: l'isolamento evita che un programma che pretende una versione diversa di .NET o di una DLL rompa gli altri, e permette il backup indipendente di ciascun ambiente. WinISD è il solo programma che richiederebbe un prefix a 32 bit, ed è ridondante rispetto a VituixCAD e Akabak: rinunciarvi elimina un prefix, l'architettura `i386` da mantenere e la classe di guasti che ne deriva.

Conseguenze: qualche comando più lungo e più spazio su disco. L'architettura `i386` non va aggiunta sulla macchina nuova, il che rimuove anche uno dei fattori di attrito degli aggiornamenti di rilascio. Se in futuro servisse un programma a 32 bit, la decisione va rivista con una voce nuova.

## ADR-005 - Blocco documentale sull'ambiente condiviso fra due progetti, con propagazione unidirezionale

Data: 2026-09-04. Stato: accettata.

Contesto: la stessa macchina Ubuntu Studio serve alla progettazione elettroacustica di questo progetto e all'home recording di `home-recording-training-mixing-setup`. La documentazione dell'ambiente serve a entrambi.

Decisione: tenere il blocco `docs/10-ambiente/` come copia canonica in questo progetto e propagarlo al gemello con `tools/sync-ambiente.py`, in una sola direzione, marcando ogni copia con una intestazione che ne dichiara la provenienza.

Motivazione: le alternative sono peggiori. Duplicare a mano garantisce la divergenza silenziosa. Un submodule git aggiungerebbe una dipendenza fra due repository personali per otto file di testo. Una sincronizzazione bidirezionale richiederebbe risoluzione dei conflitti, che a due copie non vale il costo.

Conseguenze: il blocco si modifica solo qui. Lo strumento rileva i file orfani nel gemello ma non li rimuove, perché una rimozione automatica su un altro repository è un rischio che non compensa. Il controllo `python tools/sync-ambiente.py --check` entra nella sequenza di verifica prima di un commit.

## ADR-006 - Installazione pulita di Ubuntu Studio 26.04 LTS invece dell'aggiornamento in posto

Data: 2026-09-04. Stato: accettata dall'utente in sessione. La conferma della diagnosi resta un prerequisito di esecuzione, non della decisione: è la fase 0.1 della procedura.

Contesto: la macchina è su Ubuntu Studio 25.04, una versione intermedia fuori supporto, e la LTS successiva non è raggiungibile con un salto singolo. La ricostruzione della diagnosi è in `docs/10-ambiente/ubuntu-lts-upgrade.md` e non è ancora verificata sulla macchina.

Decisione: installazione pulita della 26.04 LTS riformattando la sola partizione root e conservando `/home` senza formattarla.

Motivazione: quattro argomenti. È più corta e più prevedibile di due aggiornamenti di rilascio in cascata attraverso archivi storici. Coincide con l'obiettivo dichiarato di un setup pulito, e ricostruire l'ambiente Wine da zero elimina la sedimentazione che ha generato i guasti registrati. Non mette a rischio la licenza di Akabak, che è legata alla macchina e non all'installazione, per ADR-003. Porta su una base con supporto fino al 2031, da cui gli aggiornamenti futuri procedono da LTS a LTS.

Conseguenze: il trasferimento dei materiali va eseguito prima della reinstallazione e non dopo, perché la destinazione è sotto `/home`. Tutti i programmi Windows vanno reinstallati secondo `docs/10-ambiente/wine-configurazione.md`. Il release code di Akabak va reinserito, e la sua accettazione è la prova pratica di ADR-003. Il partizionamento con `/home` separato, scelto all'installazione originaria, è ciò che rende l'operazione a basso rischio.

La decisione è stata confermata dall'utente in sessione. La diagnosi su cui poggia resta non verificata sulla macchina, e questo non contraddice la decisione: la verifica è il primo passo della procedura, così che se la ricostruzione fosse sbagliata lo si scopra prima di toccare il disco e non dopo. La procedura operativa completa, in undici fasi con i controlli di uscita di ciascuna, è in `docs/10-ambiente/installazione-pulita-26-04.md`.

## ADR-007 - Accettare il passaggio dati per appunti fra Akabak e VACS

Data: 2026-09-04. Stato: accettata.

Contesto: l'autore del software ha dichiarato nell'agosto 2025 che su Linux le pipeline COM non funzionano per i suoi programmi, perché Wine implementa COM solo in parte, e che il trasferimento dei dati fra Akabak e VACS avviene attraverso gli appunti di sistema. La constatazione non era nel documento sorgente ed emerge dalla corrispondenza, ricostruita in `docs/90-riferimenti/timeline-akabak-vacs.md`.

Decisione: accettare il passaggio manuale come proprietà dell'ambiente e pianificarlo, invece di cercare di ripristinare COM sotto Wine o di spostare i due programmi in una macchina virtuale.

Motivazione: il confronto corretto non è fra un passaggio automatico e uno manuale, ma fra un passo manuale nella fase di simulazione e la somma dei costi dell'alternativa, cioè licenza Windows, latenza permanente sulla catena audio nella fase in cui si misura il tempo, e licenza di Akabak da richiedere di nuovo per un identificativo hardware virtuale. Il primo costo è chiaramente il minore, quindi il limite non riapre ADR-003.

Conseguenze: ogni iterazione della fase 5 del progetto ha un passo manuale in più, e le iterazioni sono molte. Serve una disciplina di denominazione dei risultati e un controllo a ogni incollaggio, perché incollare in VACS il risultato di una simulazione precedente non produce alcun errore visibile ma un grafico plausibile e sbagliato. L'impostazione relativa nelle preferenze di Akabak va verificata subito dopo la reinstallazione, alla fase 8.3 della procedura, e non alla prima iterazione.

## ADR-008 - La macchina di lavoro resta raggiungibile in rete, con chiave dedicata

Data: 2026-09-04. Stato: accettata.

Contesto: la macchina risultava irraggiungibile e la diagnosi iniziale ipotizzava che fosse spenta o su un altro segmento di rete. La lettura corretta l'ha data l'utente: la macchina si sospende da sola. Una macchina sospesa non risponde nemmeno alle richieste ARP, quindi scompare del tutto dalla rete, ed è esattamente il quadro osservato, con gli indirizzi vicini presenti nella tabella e il suo assente. Una volta sveglia ha risposto al ping e ha accettato la connessione sulla porta 22, rifiutando l'autenticazione: nessuna delle chiavi presenti sulla postazione era autorizzata, e `ssh` non provava nemmeno quelle esistenti perché mancava una voce di configurazione per quell'host.

Decisione: la macchina resta raggiungibile in rete per l'amministrazione remota. Si disattiva la sospensione automatica, si abilita il Wake-on-LAN come rete di sicurezza, si genera una chiave SSH dedicata a questo host separata da quelle di GitHub, e si fissa l'indirizzo con una prenotazione sul router.

Motivazione: l'amministrazione remota è ciò che rende possibile eseguire e tracciare le procedure di questo progetto invece di descriverle. Una chiave per host, invece del riuso delle chiavi di GitHub, limita il danno di una chiave compromessa e rende il comando corto e ripetibile tramite un alias.

Conseguenze: la macchina consuma più energia perché non si sospende, ed è il prezzo accettato. La chiave dedicata va generata sulla postazione e installata sulla macchina con un passaggio interattivo che richiede la password una volta sola. Una volta che la chiave funziona, l'autenticazione per password va disattivata sul servizio SSH, verificando la configurazione con `sshd -t` prima di riavviare il servizio, perché riavviare `sshd` con una configurazione non valida su una macchina raggiungibile solo in rete significa chiudersi fuori.

## ADR-009 - Emendamento ad ADR-004: il divieto di prefix a 32 bit decade

Data: 2026-09-04. Stato: accettata, con una parte condizionata.

Contesto: ADR-004 aveva stabilito un prefix per programma, tutti a 64 bit, e nessun prefix a 32 bit, con la motivazione che l'unico candidato a richiederlo era WinISD, escluso perché ridondante. L'ispezione diretta del corredo software sul Desktop della postazione ha cambiato il quadro. Il formato reale di ogni installer, letto con `file` invece di essere dedotto dal nome, mostra che tutti gli installer del corredo sono a 32 bit, che LSPCad 5.25 è genuinamente a 16 bit nel formato NE per Windows 3.1, e che Ramsete 27b è una applicazione Visual Basic 6, quindi a 32 bit e con bisogno del runtime `vb6run`, come rivela la struttura del suo `SETUP.LST`.

Decisione: la regola resta un prefix per programma e la preferenza resta per i 64 bit, ma il divieto assoluto di un prefix a 32 bit decade, perché era motivato da un solo candidato escluso e non da un principio. Se e quando Ramsete verrà installato, avrà un prefix a 32 bit isolato dagli altri. La parte condizionata è proprio questa: l'installazione di Ramsete è subordinata alla verifica del suo stato di licenza, tracciata come PA-002, e finché quella verifica non è fatta il prefix non si crea.

Motivazione: una decisione architetturale motivata da un solo caso non regge quando quel caso cambia, e mantenerla per coerenza formale porterebbe a escludere un programma per la ragione sbagliata. Al tempo stesso il costo del prefix a 32 bit non è nullo e va pagato solo quando serve: richiede di dichiarare l'architettura `i386` sul sistema, che raddoppia l'insieme dei pacchetti per molte librerie ed è uno dei fattori di attrito degli aggiornamenti di rilascio. È uno dei motivi per cui la macchina si trova nella situazione da cui questa documentazione parte, quindi reintrodurlo a cuor leggero sarebbe ripetere l'errore.

Conseguenze: durante l'installazione pulita l'architettura `i386` non si dichiara, e la fase 8.8 della procedura lo dice esplicitamente. Si aggiunge soltanto se Ramsete supera la verifica di licenza e si decide di installarlo. Rimandare quel passo costa un comando; anticiparlo costa attrito permanente. Resta inoltre chiarita una distinzione che ADR-004 non faceva e che è fonte di errori: l'architettura dell'installer non è quella dell'applicazione, e un installer a 32 bit gira senza problemi in un prefix a 64 bit. La sola eccezione netta è un eseguibile a 16 bit, che in un prefix a 64 bit non gira affatto.

## ADR-010 - Il corredo software si trasferisce per sottoinsieme selezionato

Data: 2026-09-04. Stato: accettata.

Contesto: il corredo `Progetto stanza (software)` pesa 2,3 GB e contiene quattordici voci. L'ispezione ha accertato che otto di esse portano protezioni rimosse o provenienza non lecita, riconoscibili da cartelle di modifica dichiarate nel nome, da un emulatore di chiave hardware, da uno sbloccatore separato, da file descrittivi di gruppi di distribuzione illecita e, in un caso, dal file di provenienza da un servizio di condivisione.

Decisione: sulla macchina Ubuntu Studio si trasferisce e si installa soltanto il sottoinsieme legittimo, cioè VituixCAD, ARTA, EASE Focus 3.1.260 con il suo servizio di database, il database dei GLL del 2016, e Ramsete subordinato alla verifica di licenza. Le otto voci restanti non si trasferiscono e non si installano.

Motivazione: la ragione che regge da sola, a prescindere da ogni altra, è che nessuna delle otto serve al progetto. FineCone e FineMotor simulano cono e motore magnetico di un altoparlante, quindi operano a monte di dove questo progetto lavora, che parte da driver finiti e dai loro parametri Thiele/Small. LSPCad e Grenander Loudspeaker Lab sono coperti da VituixCAD, gratuito, molto più recente e con gestione della direttività e della risposta in potenza. AmpliTube, Guitar Rig e POD Farm sono emulatori di amplificatori per chitarra, senza relazione con la progettazione elettroacustica, e per il progetto gemello di home recording esistono equivalenti nativi liberi come Guitarix e Rakarrack.

Conseguenze: il trasferimento passa da 2,3 GB a circa 524 mebibyte, e il numero di prefix Wine da mantenere resta quattro invece di dieci. La cancellazione della copia ridondante su SSD, tracciata come PA-001, riguarda l'intera cartella e non il solo sottoinsieme, quindi va preceduta dal confronto per impronte fra le due copie. Quel confronto è stato eseguito il 2026-09-07 e ha dato copie identiche, 650 file per parte con tutte le impronte coincidenti, quindi la cancellazione è sicura dal punto di vista della ridondanza e resta subordinata al solo completamento del trasferimento. La presunta divergenza sul collegamento della versione 3.1.10, ipotizzata quando questa voce è stata scritta, si è rivelata inesistente, e la lettura del collegamento ha invece portato alla scoperta di un quarto disco: si vedano MS-024 e MS-025.
