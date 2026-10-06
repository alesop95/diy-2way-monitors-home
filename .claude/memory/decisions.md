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

Data: 2026-09-04. Stato: accettata dall'utente in sessione, *rivista da ADR-011 il 2026-09-07*: la verifica sulla macchina ha smentito la premessa del primo dei quattro motivi, che va quindi letto come caduto. La decisione resta difendibile sui tre restanti e va riconfermata dall'utente sulla base corretta. Il testo che segue è quello originale e non è stato riscritto.

Contesto: la macchina è su Ubuntu Studio 25.04, una versione intermedia fuori supporto, e la LTS successiva non è raggiungibile con un salto singolo. La ricostruzione della diagnosi è in `docs/10-ambiente/ubuntu-lts-upgrade.md` e non è ancora verificata sulla macchina.

Decisione: installazione pulita della 26.04 LTS riformattando la sola partizione root e conservando `/home` senza formattarla.

Motivazione: quattro argomenti. È più corta e più prevedibile di due aggiornamenti di rilascio in cascata attraverso archivi storici. Coincide con l'obiettivo dichiarato di un setup pulito, e ricostruire l'ambiente Wine da zero elimina la sedimentazione che ha generato i guasti registrati. Non mette a rischio la licenza di Akabak, che è legata alla macchina e non all'installazione, per ADR-003. Porta su una base con supporto fino al 2031, da cui gli aggiornamenti futuri procedono da LTS a LTS.

Conseguenze: il trasferimento dei materiali va eseguito prima della reinstallazione e non dopo, perché la destinazione è sotto `/home`. Tutti i programmi Windows vanno reinstallati secondo `docs/10-ambiente/wine-configurazione.md`. Il release code di Akabak va reinserito, e la sua accettazione è la prova pratica di ADR-003. Il partizionamento con `/home` separato, scelto all'installazione originaria, è ciò che rende l'operazione a basso rischio.

La decisione è stata confermata dall'utente in sessione. La diagnosi su cui poggia resta non verificata sulla macchina, e questo non contraddice la decisione: la verifica è il primo passo della procedura, così che se la ricostruzione fosse sbagliata lo si scopra prima di toccare il disco e non dopo. La procedura operativa completa, in undici fasi con i controlli di uscita di ciascuna, è in `docs/10-ambiente/installazione-pulita-26-04.md`.

Nota del 2026-09-30, MS-168. Il quarto motivo, cioè la base supportata fino al 2031, era scritto senza fonte e va precisato: il 2031 è il supporto standard della base Ubuntu 26.04 LTS, mentre il flavor Ubuntu Studio dichiara nel proprio annuncio di rilascio un supporto di tre anni, fino ad aprile 2029. La fonte è in `docs/90-riferimenti/fonti.md` e la scadenza è `UBUNTU-STUDIO-EOL` in `data/scadenze.json`. Il motivo resta valido, perché anche tre anni di supporto sono un orizzonte adeguato, ma la macchina va portata alla LTS successiva prima di aprile 2029 e non del 2031.

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

## ADR-011 - Revisione di ADR-006: la motivazione cade da quattro a tre, la decisione va riconfermata

Data: 2026-09-07. Stato: accettata come revisione. La decisione operativa che rivede, cioè ADR-006, resta in attesa di riconferma dall'utente sulla base corretta.

Contesto: ADR-006 aveva scelto l'installazione pulita di Ubuntu Studio 26.04 LTS invece dell'aggiornamento in posto, con quattro motivi, e la diagnosi su cui poggiava non era verificata sulla macchina. La fase 0 della procedura, eseguita il 2026-09-07 e documentata in `docs/10-ambiente/fotografia-macchina-2026-09-07.md`, ha smentito tre delle quattro cause attribuite al blocco di aggiornamento e ha rivelato che l'aggiornamento non era mai stato tentato.

Decisione: registrare che il primo dei quattro motivi di ADR-006 è venuto meno, che gli altri tre restano validi, che se ne aggiunge uno nuovo, e che la decisione va riconfermata dall'utente sapendo questo invece di essere data per acquisita.

Motivazione, motivo per motivo. Il primo motivo era che l'installazione fosse più corta e più prevedibile di due aggiornamenti in cascata attraverso archivi storici: è caduto, perché di cascate non ce n'è bisogno e di archivi storici non se ne attraversa nessuno. L'alternativa reale è un aggiornamento dei 134 pacchetti pendenti, un riavvio che il sistema chiede già, e un solo `do-release-upgrade` verso la 26.04.1 LTS che lo strumento propone adesso. Il secondo motivo, l'ambiente pulito, è non solo valido ma rafforzato: la fotografia ha mostrato la sedimentazione in forma concreta, cioè due repository WineHQ attivi per due rilasci diversi di Ubuntu, `wine-stable 3.0.1` del 2018 accanto a `wine 9.0`, l'architettura `i386` dichiarata, una sorgente `file:/cdrom/` residua e un prefix unico condiviso fra programmi. Il terzo motivo, la licenza di Akabak non a rischio, non è toccato. Il quarto, la base supportata fino al 2031, non è toccato.

Il motivo nuovo che la fotografia rende disponibile: `/home` contiene 3,7 GB su 369 disponibili, cioè il 2 per cento. Il costo del salvataggio dei dati è quindi trascurabile e il rischio dell'operazione è più basso di quanto si potesse stimare senza il dato.

Conseguenze: la decisione resta difendibile, ma su tre motivi invece di quattro, e con una alternativa molto meno onerosa di come era stata descritta. Chi legge la documentazione non deve trovare la vecchia motivazione intatta, quindi la pagina della diagnosi porta l'avvertenza in apertura e le tre cause sono marcate come smentite nel corpo. Se l'utente sceglie di riconfermare l'installazione pulita, il motivo dominante diventa l'ambiente pulito e non la fragilità dell'alternativa. Se sceglie l'aggiornamento in posto, la sequenza è nella strada A della pagina corretta, e il lavoro reale sta nel disattivare i due repository WineHQ prima di iniziare.

Nota metodologica, perché è il vero contenuto di questa voce. ADR-006 era stata registrata come proposta e poi accettata prima che la sua premessa fosse verificata, con la giustificazione che la verifica era il primo passo della procedura. Quella giustificazione era corretta in principio e ha funzionato in pratica, perché la verifica ha effettivamente preceduto qualunque modifica al disco. Ma il fatto che tre cause su quattro fossero sbagliate mostra quanto poco valga una ricostruzione plausibile: la decisione era giusta per ragioni in parte sbagliate, e questo è un esito diverso dall'aver avuto ragione.

## ADR-012 - Il Rod Rain audio è la sorgente della catena di ascolto, e questo anticipa la scelta fra monitor attivi e passivi

Data: 2026-09-07. Stato: accettata per la sorgente; la conseguenza sull'architettura del diffusore resta aperta. Rivista da ADR-018 nella seconda conseguenza, quella sulla catena di misura: l'interfaccia nominata qui non appartiene a questo progetto.

Contesto: la catena di ascolto dei due monitor non era mai stata definita. Il documento sorgente si occupava della catena di misura, cioè microfono e Focusrite Scarlett 2i2, e lasciava il resto implicito. L'utente ha indicato come uscita per i monitor l'unità Rod Rain audio, oggetto di studio del progetto `rodrainaudio-reverse-eng`, precisando che il dispositivo è condiviso con un altro computer.

Decisione: il Rod Rain audio è la sorgente della catena di ascolto. Ciò che ne viene usato è l'uscita a livello di linea su RCA, a circa 2 Vrms, non lo stadio cuffie.

Motivazione: il dispositivo è già in casa, è già caratterizzato in un progetto dedicato che ne documenta la catena interna fino all'uscita di linea, e fornisce esattamente ciò che serve a una sorgente, cioè il livello di linea consumer standard. Non c'è ragione di acquistare un convertitore per questo scopo.

Conseguenze, e la più importante non è ovvia. Due Vrms su RCA sono un segnale e non una potenza, e lo stadio cuffie che segue non può pilotare un altoparlante da 4 o 8 ohm. Ne segue che la scelta della sorgente vincola l'architettura del diffusore: con monitor attivi la catena è completa così com'è, con monitor passivi serve un amplificatore di potenza stereo interposto, che non è fra le cose disponibili e diventerebbe un acquisto.

Il documento sorgente lasciava aperta la scelta fra crossover passivo e attivo, ed era legittimo farlo quando la sorgente non era decisa. Ora quella scelta va anticipata alla fase 4a, prima dell'acquisto dei driver, perché determina se occorre un amplificatore in più e perché cambia il modo in cui il crossover si progetta: passivo significa componenti reali con le loro tolleranze, attivo significa filtro a livello di linea realizzato in analogico o in digitale. Influisce anche su quali driver convengono.

Seconda conseguenza, sulla validità delle misure. La catena di misura usa la Scarlett, perché serve un ingresso microfonico con alimentazione phantom; la catena di ascolto usa il Rod Rain. Per la fase 1 la differenza è irrilevante, perché si misura la stanza e la sorgente è provvisoria. Per la fase 8, cioè la verifica del monitor costruito, non lo è: se si vuole misurare ciò che si ascolterà, il segnale di prova deve uscire dalla catena di ascolto reale, quindi microfono sulla Scarlett e generazione sul Rod Rain, che REW permette configurando dispositivi diversi in ingresso e in uscita.

Terza conseguenza, minore: l'uso condiviso con un altro computer implica scollegare e ricollegare, oppure un commutatore USB. Non è un problema tecnico ma è attrito, e l'attrito scoraggia le misure ripetute, che sono il metodo di questo progetto.

Resta da verificare, e non da assumere, se l'uscita AUDIO OUT sia a livello fisso o segua il controllo di volume: con uscita fissa e monitor attivi il volume deve stare altrove.

## ADR-013 - ADR-006 riconfermata sulla base corretta, e la pulizia di Wine non si fa

Data: 2026-09-07. Stato: accettata. Supera lo stato di attesa di ADR-011 e chiude PA-006.

Contesto: ADR-011 aveva registrato la caduta del primo dei quattro motivi di ADR-006 e rimesso la scelta all'utente, perché tenere una decisione confermata quando una delle sue gambe è caduta significherebbe farla passare per più solida di quanto sia. La lettura SMART del 2026-09-07 ha inoltre escluso il terzo scenario, cioè la sostituzione del disco, perché il disco risulta sano.

Decisione: si procede con l'installazione pulita di Ubuntu Studio 26.04 LTS, riformattando la sola partizione root e conservando `/home`. Il lavoro privilegiato si esegue con comandi preparati dall'agente e lanciati dall'utente, senza alcuna regola `sudoers` che conceda privilegi senza password.

Motivazione della prima parte: dei quattro motivi originali ne restano tre, e il dominante è ora l'ambiente pulito, non più la fragilità dell'alternativa. La fotografia ha mostrato che la sedimentazione da rimuovere è reale e concreta, cioè due repository WineHQ attivi per due rilasci diversi di Ubuntu, `wine-stable 3.0.1` del 2018 accanto a `wine 9.0`, l'architettura `i386` dichiarata, una sorgente `file:/cdrom/` residua e un prefix unico condiviso fra programmi. Si aggiunge il motivo reso disponibile dai dati: `/home` contiene 3,7 GB su 369, quindi il costo del salvataggio è trascurabile e il rischio dell'operazione più basso di quanto si potesse stimare.

Motivazione della seconda parte: la regola `sudoers` avrebbe reso autonoma la parte privilegiata, ma amplia ciò che può fare chi ottenesse la chiave SSH, e per una macchina raggiungibile in rete quel prezzo non è giustificato da una comodità di esecuzione. La scelta è quindi di non modificare la postura di sicurezza della macchina.

Conseguenza operativa immediata, e non è ovvia: *la pulizia dell'ambiente Wine non si esegue*. Pulire Wine su un sistema che verrà azzerato è lavoro che si butta, perché la riformattazione di root porta via l'intera installazione dei pacchetti, i due repository WineHQ, l'architettura `i386` e la sorgente residua. L'ambiente pulito si ottiene per costruzione dalla reinstallazione, non da una purga preventiva. Per la stessa ragione non si applicano i 134 pacchetti pendenti e non si esegue il riavvio richiesto: sono operazioni sul sistema che sta per essere sostituito.

L'unica cosa che va conservata dall'ambiente attuale è il prefix `~/.wine`, che vive sotto `/home` e quindi sopravvive: la copia di sicurezza prevista dalla fase 1.2 resta utile non per ripristinarlo, perché i prefix vanno rifatti puliti, ma per poter confrontare configurazioni e librerie se un programma dopo la reinstallazione non si comportasse come prima.

Conseguenza sulla sequenza: si passa direttamente alla fase 1, cioè trasferimento dei materiali e copia di sicurezza di `/home`, e da lì alle fasi da 2 a 11. Le due voci ancora aperte di PA-005, cioè l'esito di `apt update` e il Machine Identifier di Akabak, cambiano di peso: la prima diventa irrilevante perché quel sistema non verrà aggiornato, la seconda resta necessaria e va fatta prima di azzerare, perché dopo non sarebbe più confrontabile.

## ADR-014 - Emendamento ad ADR-012: il vincolo di budget sulla catena di ascolto è rilassato

Data: 2026-09-07. Stato: accettata.

Contesto: ADR-012 aveva registrato che l'uscita a livello di linea del Rod Rain, essendo un segnale e non una potenza, vincola l'architettura del diffusore, e aveva presentato la necessità di un amplificatore di potenza per la strada passiva come un costo da evitare, cioè come un elemento che "diventerebbe un acquisto". L'utente ha precisato che l'acquisto di un buon amplificatore non è un problema quando servirà, e che in alternativa si può valutare la sostituzione del convertitore, ragionando sul miglior compromesso fra qualità e costo.

Decisione: la scelta fra monitor attivi e passivi si prende su criteri tecnici e non sul risparmio di un componente. Il budget non è il vincolo dominante, e né l'amplificatore né la sostituzione del convertitore sono esclusi in partenza.

Motivazione: un vincolo di budget che non esiste distorce una decisione tecnica. Presentare l'amplificatore come un costo da evitare avrebbe spinto verso la strada attiva per la ragione sbagliata, cioè per non comprare un componente, invece che per le sue ragioni proprie, che sono il controllo indipendente per via, l'assenza di componenti passivi in serie all'altoparlante e la possibilità di realizzare il filtro in digitale. Simmetricamente, la strada passiva ha ragioni proprie che vanno pesate: un solo canale di amplificazione per cassa, nessuna alimentazione a bordo del diffusore, e un progetto di crossover verificabile con componenti misurabili.

Conseguenze: la decisione resta aperta e si prende nella fase 4a, dove sarà informata dalle simulazioni invece che dal listino. Restano da confrontare, quando ci si arriverà, tre configurazioni e non due: convertitore attuale più monitor attivi, convertitore attuale più amplificatore di potenza più monitor passivi, e convertitore sostituito con un'interfaccia o un DAC più adatto più una delle due architetture. Il terzo termine è quello che l'utente ha aggiunto e che ADR-012 non contemplava.

Va notato che il terzo termine ha un legame con un'altra voce aperta, e conviene non deciderle separatamente: la valutazione dell'interfaccia audio per l'home recording, tracciata come PA-001 nel progetto gemello, riguarda un dispositivo che potrebbe coprire anche il ruolo di sorgente per l'ascolto. Valutare le due cose insieme evita di comprare due dispositivi dove ne basterebbe uno, oppure di scoprire dopo che quello comprato per la registrazione non è adatto all'ascolto.

## ADR-015 - La copia di sicurezza di /home va su una macchina diversa, in un archivio tar

Data: 2026-09-07. Stato: accettata ed eseguita.

Contesto: la fase 1.3 della procedura richiede una copia di sicurezza di `/home` fuori dalla macchina, ed è l'unico presidio contro l'unico rischio irreversibile dell'installazione pulita, cioè l'errore umano nella selezione della partizione da formattare. L'utente ha chiesto se la destinazione potesse essere una partizione della stessa macchina, oppure temporaneamente la postazione Windows.

Decisione: la copia va sulla postazione Windows, come archivio `tar` non compresso prodotto in streaming attraverso `ssh`. Non va su alcuna partizione della macchina. La destinazione scritta all'atto della decisione era `E:\_backup-ubuntu-studio\`; l'utente ha poi spostato l'archivio in `C:\Users\Utente\Desktop\_backup-ubuntu-studio\`, con dimensione identica al byte, e questo *non altera la decisione*, perché la proprietà che la motiva è che il supporto sia una macchina diversa da quella protetta, non una lettera di unità particolare. Ne segue una regola per gli strumenti di verifica: la condizione da controllare è l'esistenza dell'archivio per nome fra più posizioni plausibili, non la presenza di un percorso fisso, altrimenti uno spostamento legittimo fa dichiarare mancante un backup che c'è.

Motivazione del rifiuto della prima opzione. La verifica mostra che la macchina ha un solo disco, `nvme0n1` da 465,8 GB, con quattro partizioni e nient'altro, e nessun disco USB collegato. Le tre varianti pensabili fallirebbero per ragioni diverse: su root la copia morirebbe con la formattazione, su `/home` stessa non proteggerebbe da nulla perché il rischio da coprire è precisamente la perdita di quella partizione, e una partizione nuova richiederebbe di ridurre `/home` con una operazione rischiosa in sé senza proteggere da un errore di selezione né da un guasto del disco. La regola generale: una copia di sicurezza sullo stesso supporto della cosa che protegge è una copia, e non una copia di sicurezza.

Motivazione della scelta della seconda. `/home` pesa 4,4 GB contro 198 GB liberi sulla destinazione, quindi il costo è trascurabile, e soprattutto è una macchina fisicamente diversa, che è l'unica proprietà che rende un backup un backup.

Motivazione del metodo, che non è un dettaglio. Si usa `tar` in streaming e non `scp` dei file, perché la destinazione è NTFS e non sa rappresentare proprietario, gruppo e permessi POSIX: copiando i file singoli quei metadati andrebbero perduti e il ripristino produrrebbe una `/home` con i permessi sbagliati. Dentro un archivio quei metadati sono contenuto e sopravvivono anche su NTFS. Si usa `--numeric-owner` perché il ripristino non dipenda dall'esistenza dell'utente con quel nome. Non si comprime perché dei 4,4 GB la maggior parte sono installer e archivi già compressi.

Conseguenze: PA-007, cioè la cancellazione della copia del corredo sul Desktop di Windows, è sbloccata. L'archivio va rigenerato se `/home` cambia in modo significativo prima della reinstallazione, e la sua verifica è il confronto fra il numero di file nell'archivio e quelli sulla macchina, non la sola assenza di errori.

## ADR-016 - Akabak è a 32 bit: revisione di ADR-004, ADR-009 e ADR-013 sull'architettura dei prefix

Data: 2026-09-07. Stato: accettata. Supera la parte sull'architettura di ADR-004, ADR-009 e ADR-013.

Contesto: tre decisioni precedenti poggiavano sull'affermazione, presa dal documento sorgente, che Akabak 3 sia una applicazione a 64 bit senza build a 32 bit, e ne concludevano che servisse un prefix a 64 bit e che l'architettura `i386` fosse un residuo da non riprodurre sulla macchina nuova. L'ispezione del prefix funzionante sulla macchina smentisce la premessa.

I fatti misurati. Il prefix in uso è `/home/alesop95/.wine` e il suo registro dichiara `#arch=win32`, cioè è un prefix a *32 bit*; la cartella `syswow64` è assente, come deve essere in un prefix a 32 bit. L'eseguibile installato, `AKABAK.exe`, è `PE32 executable, Intel 80386`, cioè *a 32 bit*. Lo stesso vale per `VACS_32.exe`, e la libreria che entrambi portano si chiama `Matrix32.dll`. Nel prefix non esiste alcun `winetricks.log`, non esiste `Microsoft.NET/Framework/v4` e non è installato alcun font Microsoft di base.

Decisione: Akabak e VACS vanno in un prefix a *32 bit*, senza dipendenze installate con winetricks, riproducendo la configurazione che funziona. L'architettura `i386` va dichiarata sul sistema, perché è necessaria e non residua. VituixCAD ed EASE Focus restano su prefix a 64 bit, perché i loro requisiti sono dichiarati dai rispettivi produttori e su questa macchina non sono mai stati installati, quindi non c'è nulla da riprodurre e nulla da smentire.

Motivazione: la configurazione che funziona su questa macchina batte qualunque requisito dichiarato in un appunto. Il documento sorgente descriveva Akabak come a 64 bit con bisogno di .NET 4.8 e di font e runtime aggiuntivi, e nessuna di quelle affermazioni è confermata dall'installazione reale: la lista delle dipendenze del sorgente descriveva ciò che era stato tentato durante il troubleshooting, non ciò che serviva.

Conseguenze, e sono sostanziali. La fase 7 della procedura di installazione pulita, che prescriveva quattro prefix a 64 bit con `dotnet48`, è sbagliata per Akabak e VACS e va corretta. Il consiglio di non dichiarare l'architettura `i386`, dato in ADR-009 e ripetuto in ADR-013, è rovesciato: senza `i386` il solo software del progetto che oggi funziona non funzionerebbe più. Il conteggio dei prefix passa da quattro a quattro ma con architetture diverse, cioè uno a 32 bit per Akabak e VACS e tre a 64 bit per gli altri.

Resta valida la parte di ADR-004 che non riguarda l'architettura, cioè un prefix per programma, con l'eccezione dichiarata di Akabak e VACS che condividono il proprio perché si usano in sequenza e perché così è la configurazione funzionante.

Una nota di metodo, che è la lezione vera di questa voce. Tre decisioni consecutive hanno propagato una affermazione non verificata presa da un appunto, e ciascuna l'ha usata come premessa della successiva senza tornare alla fonte. Il costo è stato una prescrizione operativa sbagliata su tre documenti. Il controllo che l'avrebbe evitato costava un comando, cioè `file` sull'eseguibile installato.

## ADR-017 - La scheda di stampa si genera con uno strumento, e non porta i dati di licenza

Data: 2026-09-08. Stato: accettata.

Contesto: la reinstallazione si esegue davanti alla macchina e non davanti alla postazione di sviluppo, quindi serve una scheda su carta. La prima versione di quella scheda era stata composta a mano come `.docx` in una sessione poi interrotta da un crash, e ne sono emersi due problemi indipendenti. Il primo è che il documento non era riproducibile, perché il codice che lo aveva costruito viveva soltanto nella sessione: due minuti dopo la sua creazione la procedura ha guadagnato una avvertenza, e la carta è rimasta indietro senza che nulla lo segnalasse. Il secondo è che la scheda sorgente dichiarava di contenere i dati di licenza di Akabak nel documento generato, cioè Machine Identifier e Release Code su un foglio stampato.

Decisione, in due parti. La carta si genera con `tools/make-scheda-docx.py`, che è versionato, e non si compone a mano. I dati di licenza non entrano nel documento generato, se non passando esplicitamente `--con-licenza`.

Motivazione della prima parte: un documento di stampa è una copia di documentazione che circola fuori dal repository, quindi il rischio non è che sia sbagliato ma che diverga in silenzio. Uno strumento versionato non elimina la divergenza, perché il contenuto della scheda vive nello strumento come dati e non è una conversione del Markdown, ma la rende riparabile con un comando invece che con una ricostruzione. La ragione per cui non è una conversione automatica va detta perché è una rinuncia consapevole: la carta ha vincoli che il Markdown non ha, cioè due pagine di spazio, caselle da spuntare a penna e riquadri colorati sul passo irreversibile, e una conversione li perderebbe tutti.

Motivazione della seconda parte, e non è soltanto di riservatezza. Alla reinstallazione quei valori non servono: il Release Code è permanente e legato al Machine Identifier, la cui invarianza è stata verificata in MS-052, quindi si reinserisce dal file riservato al momento di riaprire AKABAK, che è un passo successivo alla reinstallazione e si esegue davanti alla macchina con la postazione disponibile. Stamparli anticiperebbe un codice di attivazione permanente su un foglio che si porta in giro, in cambio di nessun vantaggio operativo. Il valore predefinito è quindi la loro assenza, e non la loro presenza con un avvertimento.

Conseguenze. La nota in apertura di `docs/10-ambiente/scheda-reinstallazione.md` è stata corretta, perché dichiarava la sostituzione dei due segnaposto come comportamento normale dello strumento. Il file riservato `_notes/licenze-akabak-riservato.md` resta la sola sede dei valori, esclusa dal versionamento. Chi usa `--con-licenza` produce un foglio che va trattato come materiale riservato, e lo strumento lo dichiara sul terminale al momento di generarlo.

Alternativa scartata: mettere i valori nel documento e affidarsi alla cura di chi stampa. Scartata perché sposta un presidio da una impostazione predefinita a una abitudine, e le abitudini non sopravvivono alla fretta del giorno in cui si azzera un disco.

## ADR-018 - Emendamento ad ADR-012: la catena di misura non ha un'interfaccia, e questo mette in sequenza due acquisti

Data: 2026-09-09. Stato: accettata. Rivede la seconda conseguenza di ADR-012.

Contesto. ADR-012 aveva definito la catena di ascolto dei due monitor, stabilendo che la sorgente è il Rod Rain audio con uscita di linea su RCA a 2 Vrms, e ne aveva tratto due conseguenze. La prima, sull'anticipo della scelta fra monitor attivi e passivi, resta valida e non è toccata. La seconda affermava che la catena di misura usa la Focusrite Scarlett 2i2 mentre quella di ascolto usa il Rod Rain, e che sono due convertitori diversi con due uscite diverse.

La struttura di quella seconda conseguenza è corretta e va conservata: sono davvero due catene distinte, e per la fase 8, cioè la verifica dei diffusori costruiti, il segnale di prova deve uscire dalla catena di ascolto reale e non da quella di misura, altrimenti si misura un convertitore invece di un diffusore. Ciò che cade è il soggetto: quella interfaccia non appartiene a questo progetto. L'utente ha confermato il 2026-09-09 di possederla ma di non impiegarla qui, e l'affermazione contraria derivava da un file alla radice contenente il solo indirizzo della pagina di download dei driver. Il ritiro documentale è in MS-079.

Decisione. La catena di misura richiede una interfaccia con ingresso microfonico e alimentazione phantom a 48 V, e quale interfaccia non è deciso. La scelta è condivisa con il progetto gemello di home recording, dove l'esigenza primaria è la registrazione multitraccia con Ardour, e porta due vincoli fissati dall'utente: deve essere un dispositivo di classe audio riconosciuto dal kernel Linux senza driver proprietari, e deve reggere anche le misure di questo progetto e non solo la registrazione. È tracciata come PA-012.

Motivazione dei due vincoli, perché non sono preferenze. Il primo elimina la classe di guasti peggiore su questa piattaforma: un produttore che rilasci driver soltanto per Windows e macOS rende l'hardware inutilizzabile a ogni aggiornamento di kernel, e su una macchina che è stata lasciata due anni senza aggiornamenti proprio per timore di rompere l'ambiente questo è un rischio già sperimentato in altra forma. Il secondo evita due acquisti dove ne basta uno, e ha una conseguenza tecnica: una interfaccia che regga la misura deve dichiarare la propria qualità di conversione, perché in fase 8 quel convertitore entra nella catena di cui si misura la risposta.

Conseguenza sulla sequenza delle decisioni, ed è la parte operativa di questo emendamento. La scelta del microfono di misura dipende da quella dell'interfaccia e non è invertibile. La pagina `docs/20-misura-stanza.md` concludeva a favore di un microfono XLR calibrato individualmente contro l'UMIK-1 USB, e quella conclusione poggiava interamente sulla disponibilità di una interfaccia: la stessa pagina dichiarava che su una macchina senza interfaccia l'UMIK-1 sarebbe stato la scelta giusta senza discussione. La conclusione è quindi stata riscritta in forma condizionale, valida se l'interfaccia viene acquisita e rovesciata se non lo fosse.

Due parametri restano non fissati e la loro assenza è dichiarata invece di essere riempita per ipotesi: il numero di ingressi simultanei necessari alla registrazione, che è il vincolo che elimina più modelli di ogni altro, e un eventuale tetto di spesa. Vanno chiesti quando la valutazione si apre, e non assunti.

Alternativa scartata, e vale registrarla perché era la via più rapida. Impiegare in questo progetto l'interfaccia che l'utente già possiede, risolvendo il problema con zero spesa. Scartata perché è una decisione dell'utente sull'uso del proprio hardware e l'ha già presa in senso contrario; il progetto registra la scelta e non la discute.

## ADR-019 - Emendamento ad ADR-016: il prefix a 32 bit si usa con `wine32`, non con `wine`

Data: 2026-09-09. Stato: accettata. Completa ADR-016 senza modificarne le conclusioni.

Contesto. ADR-016 aveva stabilito, sulla base dell'ispezione dell'eseguibile installato, che Akabak e VACS sono a 32 bit e che l'architettura `i386` va dichiarata sul sistema e non evitata, rovesciando tre decisioni precedenti. Quella decisione era corretta e resta valida, ma era incompleta in un punto che si è manifestato solo all'esecuzione: diceva come predisporre l'ambiente e non come usarlo.

Il fatto misurato. Su Ubuntu il comando `wine` è un collegamento che attraverso il sistema delle alternative arriva a uno script, il quale seleziona il caricatore a 64 bit ogni volta che `wine64` è presente sul sistema, senza ispezionare né il prefix né l'architettura dell'eseguibile passato come argomento, e ripiega sul caricatore a 32 bit soltanto se il primo manca. Poiché ADR-016 impone di installare il ramo a 32 bit accanto a quello a 64, entrambi i caricatori esistono, quindi il comando `wine` sceglie sempre quello sbagliato per il prefix di Akabak. L'avvio fallisce con `is a 32-bit installation, it cannot support 64-bit applications`, messaggio che nomina il prefix e accusa il caricatore.

Decisione. Ogni comando rivolto a un prefix a 32 bit si scrive con `wine32` e con `WINEPREFIX` dichiarato esplicitamente. Vale per l'avvio dei programmi, per `winecfg`, per `wineboot` e per `winetricks`, perché tutti passano dal medesimo wrapper. Per i prefix a 64 bit il comando resta `wine`, e la differenza va scritta accanto a ciascun prefix nella tabella della procedura invece di essere ricordata.

Motivazione della dichiarazione esplicita del prefix, che non è ridondanza. Lo script `wine32` impone `WINEPREFIX` a `~/.wine32` quando la variabile non è definita, quindi un comando senza prefix dichiarato non fallisce: crea al volo un prefix vuoto e vi lavora dentro, facendo concludere che il programma non sia installato. È un modo di sbagliare che non produce un errore ma un risultato falso, ed è peggiore di un errore.

Conseguenze. La fase 7 della procedura di installazione pulita e la scheda di stampa portano ora questa prescrizione. Il controllo di uscita della stessa fase è stato sostituito, perché interrogava `wine --version`, che risponde con la versione senza caricare alcun prefix e quindi passa anche su un ambiente incapace di eseguire il programma: il controllo corretto è lo stato di installazione di `wine32:i386`, oppure l'avvio effettivo dentro il prefix. I due lanciatori sulla scrivania della macchina sono stati corretti a `wine32`.

Un fatto che discende da questa decisione e che vale registrare perché cambia il costo di una fase. Il prefix `~/.wine` è sopravvissuto alla reinstallazione, dato che vive in `/home`, e conteneva Akabak e VACS installati con l'attivazione della licenza scritta nel proprio registro. Aperto con `wine32` sotto Wine 10, dopo una copia di sicurezza da 831 MB, si è migrato senza rompersi e il programma è partito. La fase 8, che prevedeva reinstallazione e riattivazione, si riduce quindi a una verifica.

Resta aperta una discrepanza da accertare e non da assumere: la finestra dichiara l'edizione `32 Professional`, mentre la documentazione del progetto afferma che l'edizione ottenuta sia Standard malgrado il nome dell'installer. Le due affermazioni non sono conciliabili senza una verifica dello stato del release code dal menu di aiuto.

Il racconto completo, con gli script letti riga per riga e i due miei errori di diagnosi ritirati, è nel deep-dive didattico `refactor-01-wine-32-bit-su-ubuntu.md`.

## ADR-020 - Il trasferimento AKABAK verso VACS si imposta su `Files` e non su `Clipboard`

Data: 2026-09-10. Stato: accettata il 2026-09-14, quando la verifica in interfaccia ha confermato che l'opzione esiste e l'ha impostata. Il controllo si chiama `Spectrum way of output` e sta nella scheda `VACS` della finestra delle preferenze; il valore scelto si scrive come `SpectrumOutputType=3` in `AppData\Local\RDTeam\Akabak.ini`, accanto a `SpectrumOutputAsText=0` e a `SpectrumOutputFolder=` lasciata vuota, che significa cartella del progetto. Il racconto della verifica è MS-094.

Contesto. Su Windows AKABAK consegna i risultati spettrali a VACS attraverso COM, in modo automatico e senza intervento dell'operatore. Wine implementa COM solo in parte e non copre questo caso, e la guida del programma dichiara esplicitamente che su Linux serve una alternativa. Fino a MS-090 il progetto credeva che l'alternativa fosse una sola, gli appunti di sistema, perché così l'autore aveva risposto in una email del 14 agosto 2025; la guida del prodotto ne documenta due, cioè `Clipboard` e `Files`.

Decisione. Si imposta `Files`, con la cartella di destinazione lasciata a quella del progetto, che è il default. Il modo si seleziona globalmente in `Options/Preferences`, pagina `VACS`, e resta sovrascrivibile per singola osservazione nella pagina `Range` della sua form, quindi la decisione globale non preclude un uso puntuale degli appunti.

Motivazione, e sono quattro ragioni che convergono. La prima è la riproducibilità: un file su disco con un nome generato dal programma resta leggibile alla sessione successiva, mentre gli appunti di sistema non sopravvivono alla chiusura dell'applicazione e nemmeno a una copia fatta nel frattempo per altro scopo. La seconda è l'ispezionabilità, e coincide con un principio che questo sistema di progetto ha già scritto altrove: uno stato intermedio su disco si può guardare, confrontare e correggere, mentre uno stato volatile si può soltanto usare o perdere. La terza è la difesa dall'errore silenzioso che la pagina sul limite di COM già temeva, cioè incollare in VACS il risultato di una simulazione precedente credendo che sia quella appena eseguita: con i file l'errore diventa visibile, perché il file porta un nome e una data di modifica, mentre negli appunti il dato sbagliato è indistinguibile da quello giusto. La quarta è il numero di iterazioni: la fase 5 consiste nel modificare parametri finché la risposta rientra nella tolleranza, quindi il ciclo si ripete molte volte, e un ciclo che lascia una traccia su disco a ogni giro produce una storia della convergenza, che con gli appunti non esiste.

Conseguenza sul documento didattico che il progetto produrrà. La scelta dei file rende disponibile, senza lavoro aggiuntivo, la serie dei risultati intermedi di ogni iterazione della fase 5, che è precisamente il materiale su cui poggia il racconto di come si è arrivati al progetto finale. Con gli appunti quel materiale andrebbe ricostruito a mano o non esisterebbe.

Alternativa scartata, e va detto perché era quella suggerita dall'autore. `Clipboard` è più immediata alla prima iterazione, perché non richiede di scegliere una cartella né di importare, e per una prova isolata è la via più corta. Resta preferibile in un caso soltanto, cioè quando si vuole guardare una curva una volta e non conservarla, e per quel caso resta disponibile come sovrascrittura sulla singola osservazione.

Rischio residuo dichiarato. La sequenza di lavoro con i file non è stata ancora eseguita su questa macchina, quindi non è verificato quanti file produca una osservazione tipica né quanto sia comodo il meccanismo di aggiornamento all'importazione in VACS. Se l'attrito risultasse maggiore del previsto la decisione si rivede, e la revisione costerebbe una voce nuova e non un lavoro.

## ADR-021 - Emendamento ad ADR-016: su Ubuntu 26.04 la fornitura di Wine può essere soltanto quella della distribuzione

Data: 2026-09-21. Stato: accettata. Emenda ADR-016 e ne conferma la decisione per una ragione che nel 2026-09-09 non era nota e non era conoscibile.

Contesto. ADR-016 stabilisce che l'architettura `i386` va dichiarata sul sistema perché AKABAK è a 32 bit, e ADR-019 ne precisa la conseguenza sul comando. Restava però aperta, e più volte richiamata nella documentazione del progetto, la raccomandazione generale di preferire i pacchetti ufficiali di WineHQ a quelli della distribuzione: è una raccomandazione ragionevole e quasi universale, perché la distribuzione insegue la versione di Wine con mesi di ritardo. Il 2026-09-17 quella raccomandazione è stata seguita ed è fallita, con sette misure fra MS-137 e MS-142, ma la causa prima del fallimento non era stata isolata e MS-141 lo dichiarava apertamente.

Decisione. Su Ubuntu 26.04 questo progetto usa i pacchetti Wine della distribuzione e non quelli di WineHQ, e la raccomandazione contraria che compare nella documentazione precedente va letta come superata per questa versione del sistema operativo. La scelta è l'unico fornitore possibile, e non una preferenza fra due fornitori possibili.

Motivazione, misurata il 2026-09-21 e non dedotta. Il file `Release` pubblicato da WineHQ dichiara `Architectures: amd64 i386` per le suite `noble`, cioè la 24.04 LTS, e `plucky`, cioè la 25.04, e dichiara il solo `amd64` per `questing`, cioè la 25.10, e per `resolute`, cioè la 26.04 LTS. L'indice `binary-i386` di `resolute` risponde con un codice 404. Ne segue che su questa versione di Ubuntu il pacchetto del caricatore a 32 bit non esiste da installare, quindi l'unica forma disponibile è il WoW64 nuovo, che su questa macchina non popola `syswow64`. Tutti i programmi del corredo di questo progetto sono a 32 bit, quindi la fornitura di WineHQ non è utilizzabile qui, indipendentemente da quanto sia più aggiornata.

Conseguenze. La prima è che ADR-016 esce rafforzata: dichiarare `i386` sul sistema non è una concessione a un residuo ma il presupposto dell'unica catena che funziona. La seconda è che l'ottava esclusione di MS-143, con cui si è chiusa la sottofase 8.6, non è più un comportamento osservato su una macchina ma una proprietà verificabile di un repository, quindi non va riprovata sperando in una configurazione diversa. La terza è che questa decisione ha una scadenza dichiarata e non è eterna: se WineHQ tornasse a pubblicare `i386` per una versione futura di Ubuntu, oppure se il corredo diventasse a 64 bit, la decisione andrebbe riaperta con una voce nuova. La quarta è operativa e riguarda la macchina, dove il repository di WineHQ è rimasto configurato dopo l'annullamento del tentativo: che farne è PA-018.

Alternativa scartata, e va nominata perché è quella che si ripresenterà. Compilare Wine dai sorgenti con il supporto a 32 bit darebbe una catena funzionante e aggiornata, e nessuno la vieta. Resta scartata perché il costo di manutenzione è ricorrente, va pagato a ogni aggiornamento e ricade su una persona sola, mentre il guadagno rispetto alla versione della distribuzione, oggi la 10.0, non è misurato e non risolve alcun problema aperto: il solo problema che avrebbe potuto risolvere, cioè l'importazione dei GLL, è stato chiuso in MS-143 per otto cause escluse e non per mancanza di una versione più recente.

## ADR-022 - Il pacchetto LaTeX si istanzia in entrambi i progetti, e l'innesco dichiarato nella roadmap viene anticipato

Data: 2026-09-21. Stato: accettata, su scelta esplicita dell'utente.

Contesto. La roadmap di questo progetto prevede un report LaTeX del progetto dei monitor con un innesco dichiarato, cioè che si scriva quando si arriva alle fasi 4 e 5 e non prima, e la ragione dell'innesco è che un approfondimento scritto prima di avere in mano una simulazione reale spiegherebbe la teoria di due metodi invece della loro applicazione a questo diffusore. Il 2026-09-21 l'utente ha chiesto un documento diverso, cioè un report sul gain staging della catena di ingresso per l'home recording, e ha scelto di istanziare il pacchetto in entrambi i progetti invece che nel solo gemello.

Decisione. Il pacchetto `latex` è istanziato sia in `diy-2way-monitors-home` sia in `home-recording-training-mixing-setup`, ciascuno con i propri sette file e il proprio blocco nel `.gitignore`. Il report sul gain staging vive nel gemello; il report di progetto dei monitor resta previsto qui, con il proprio innesco intatto.

Motivazione, che è dell'utente e non mia, e va riportata come tale. Avere l'ambiente pronto in entrambi i progetti toglie una dipendenza fra i due repository e permette di scrivere un documento in ciascuno senza prima allestire nulla. Il costo è la manutenzione doppia, cioè due copie degli script e due manifesti da tenere allineati, mitigata dal fatto che la distribuzione TeX è una sola, user-local e condivisa, quindi non si duplica la parte pesante.

La mia obiezione, registrata perché sia verificabile e perché l'utente l'ha superata. Avevo proposto di istanziare nel solo gemello, sul ragionamento che l'innesco dichiarato nella roadmap esiste per impedire che il report dei monitor nasca prima di avere qualcosa da raccontare, e che istanziare l'ambiente qui lo rende disponibile e quindi invitante. L'obiezione resta valida come rischio e non come divieto: l'innesco riguarda quando si scrive il documento, non quando esiste l'ambiente per compilarlo, e tenere le due cose distinte è precisamente ciò che questa voce fa.

Conseguenze. Il primo documento LaTeX del progetto resta quello previsto per le fasi 4 e 5, e scriverne uno prima richiede una voce nuova che dichiari di superare questa. La distribuzione TeX non è installata da questa decisione: `scripts/setup-tex` va eseguito una volta sulla postazione, e serve a entrambi i progetti. Il blocco degli artefatti nel `.gitignore` ha richiesto due correzioni rispetto al modello, raccontate in MS-153, ed entrambe derivano dalla convenzione di questo progetto sull'ancoraggio dei pattern.

## ADR-023 - Nessun server MCP di progetto, per decisione presa al gate dell'inizializzazione

Data: 2026-09-30. Stato: accettata.

Contesto. Il Passo 4 del runbook di inizializzazione chiede sempre, anche in allineamento, se configurare un server MCP di progetto in `.mcp.json`, e in allineamento il consigliato è `code-context-provider-mcp`, che espone struttura e simboli di una base di codice. Questo progetto non ha codice applicativo: il repository contiene documentazione e script di manutenzione piccoli e senza dipendenze.

Decisione. Nessun `.mcp.json` e nessuna cartella `mcp/`. Il progetto resta a sole skill locali.

Motivazione. Il server consigliato serve a mappare una base di codice che qui non c'è, e ogni server connesso occupa token a ogni turno anche quando nessuno lo usa, secondo il vincolo del gate dei pacchetti. I server già attivi a livello di account, come quello sui vault Obsidian, non dipendono da questa scelta.

Conseguenze. Il gate si ripropone a ogni tornata di allineamento, e la domanda torna pertinente se il progetto acquisisce un servizio esterno da interrogare o una base di codice da mappare.

## ADR-024 - Modello di separazione fra test e produzione: R0, P1 senza richiesta di modifica, D non applicabile, L1

- Data: 2026-09-30
- Stato: accettata
- Contesto: fatti dichiarati al gate del runbook di inizializzazione, raccolti in sola lettura. L'unica produzione è la macchina Ubuntu Studio con programmi di terzi sotto Wine, raggiunta come `ssh studio`; una persona; nessun codice proprio da provare; nessun dato sensibile di utenti e nessun fornitore di identità; nessuna pipeline, nessun file di composizione, nessun `.env`; un solo albero di lavoro e la sola branch `main`, con i commit dell'utente diretti su di essa.
- Decisione: R0, cioè un solo ambiente con la rete di sicurezza nel ripristino, in esercizio; P1 nella variante senza richiesta di modifica, con tutti i percorsi dichiarati diretti sulla branch principale, perché il repository contiene soltanto documentazione, memoria e script di manutenzione; D non applicabile, perché non esiste un ambiente di prova con dati propri; L1.
- Alternative considerate: R1 e R2 richiederebbero un secondo ambiente dove provare prima, che per programmi di terzi installati sotto Wine nessuno manterrebbe allineato, secondo il campo "Che cosa significa sceglierla" di R0 in `docs/separazione-ambienti/GUIDA.md`; P1 con richiesta di modifica aggiungerebbe una revisione e una verifica automatica su un repository senza codice applicativo e con un solo autore.
- Conseguenze: il rischio principale di R0, cioè il backup che resta un proposito, qui è coperto da una scelta dichiarata dall'utente: un punto Veeam o un archivio dei prefix preso a mano prima di ogni cambio rischioso, senza cadenza pianificata, con la dichiarazione riproposta come domanda da `data/scadenze.json`. Il secondo rischio, provare dentro la produzione, è già accaduto con WineHQ il 2026-09-17 ed è stato riportato indietro dall'archivio dei prefix. Il ritorno della macchina intera a un punto Veeam non è mai stato eseguito, e la scheda `deployment.md` lo dichiara come lacuna. Si passa ad altro se il progetto comincia a scrivere codice proprio da eseguire sulla macchina, o se la macchina comincia a servire più persone.
- Fonti: C8 per R0; F13, F16 e C1 per P1; le sigle sono in `docs/separazione-ambienti/FONTI.md`.

## ADR-025 - La deriva di stile si ripulisce nei soli documenti vivi, e il registro storico resta com'è

Data: 2026-09-30. Stato: accettata.

Contesto. La documentazione già committata porta grassetto in prosa, che lo stile del template vieta, e `tools/lint-prosa.py` vi riporta 76 segnalazioni in 23 file, 62 delle quali sono parallelismi negativi. La convenzione del registro dei microstep vieta di riscrivere una voce passata, e la maggior parte del grassetto sta proprio in voci storiche. La decisione era aperta dal 2026-09-09 nella scheda del lavoro corrente.

Decisione. Si ripuliscono i soli documenti vivi, cioè le pagine di `docs/` che descrivono uno stato o una procedura, le schede di `.claude/context/` e il README. Non si toccano il registro dei microstep, le voci datate del work-log, il registro delle decisioni e le voci datate delle pendenze, che sono documentazione storica.

Motivazione. Un documento vivo si legge per sapere com'è una cosa oggi, e la sua forma conta per ogni lettore futuro; una voce storica si legge per sapere che cosa è successo e perché, e riscriverla, anche solo nella forma, produce un documento che sembra essere sempre stato giusto, cioè il difetto che la convenzione del registro esiste per evitare. Le segnalazioni di `lint-prosa.py` sono indizi da rileggere e non errori, quindi la pulizia le valuta una per una e non le sostituisce in blocco.

Conseguenze. La pulizia è una milestone a sé, con il proprio microstep e il conteggio prima e dopo, perimetro dichiarato. Il registro storico continuerà a mostrare le segnalazioni, e questo è atteso.

## ADR-026 - Ramsete 2.7b resta fuori dal corredo, con la provenienza accertata e il diritto d'uso chiarito

Data: 2026-10-01. Stato: accettata, revocabile.

Contesto. PA-002 chiedeva se la copia di Ramsete 27b del corredo fosse una versione dimostrativa liberamente distribuibile o una copia completa che richiede licenza, e legava a questa risposta l'installazione o l'esclusione. MS-173 ha accertato che i tre file della copia coincidono per impronta con lo zip `Ramsete27b.zip` pubblicato dagli autori nel repository che il sito ufficiale indica per il download, e che le fonti degli autori legano l'uso completo a una chiave acquistabile tramite Spectra, con una modalità dimostrativa a precisione ridotta in sua assenza.

Decisione. Ramsete non si installa. Il prefix a 32 bit `ramsete32` non si crea.

Motivazione. Una modalità a precisione ridotta non serve a un calcolo su cui si progettano due diffusori, e la versione completa è un acquisto che il progetto non ha motivo di fare, perché il ruolo di Ramsete, cioè l'acustica della stanza, è coperto da Akabak, licenziato e funzionante. La parte condizionata di ADR-009, che apriva a un prefix a 32 bit anche per Ramsete, decade senza effetti pratici, perché l'architettura `i386` è comunque necessaria per Akabak secondo ADR-016.

Conseguenze. La procedura di installazione resta scritta in `docs/10-ambiente/wine-corredo-progetto-stanza.md`, con il percorso corretto, per il caso in cui la decisione venga rivista. Si rivede se le simulazioni di Akabak si rivelassero insufficienti sull'acustica della stanza, oppure se diventasse disponibile una licenza.

## ADR-027 - Gli acquisti si fanno tutti insieme, alla fine

Data: 2026-10-01. Stato: accettata.

Contesto. Tre voci aperte dipendono da un acquisto: il metro laser di PA-020, la catena di ingresso di PA-012 e il microfono di misura che ne dipende. Le prime due bloccano le fasi 2 e 1 del workflow.

Decisione. L'utente compera tutto alla fine, in un'unica tornata, e non voce per voce.

Conseguenze. Le fasi 1 e 2 del workflow restano ferme fino agli acquisti, e con esse le fasi successive che ne dipendono. Nel frattempo si fa il lavoro che non chiede di comprare nulla: le tabelle B, C, D ed E del protocollo di rilievo con un metro a nastro, la fase 10 della procedura di installazione, e le decisioni di progetto che non dipendono da una misura. La valutazione di PA-012 resta valida, ma i prezzi letti il 2026-09-30 vanno riletti al momento dell'acquisto.

## ADR-028 - Il materiale di studio dell'utente, libri compresi, si usa soltanto in locale e non entra mai nel repository

Data: 2026-10-01. Stato: accettata, su scelta esplicita dell'utente.

Contesto. L'utente ha chiesto di costruire una base di conoscenza sui propri appunti e libri di elettronica e di filtri, che stanno su `J:`, per sostenere le decisioni di progetto e il report. Per una parte dei PDF la provenienza non è documentata. ADR-010 aveva escluso dal corredo il software di provenienza non lecita, e la domanda sull'uso del materiale è stata posta per coerenza. Il repository è pubblico.

Decisione. Si usano tutti i materiali indicati, per studio personale e soltanto in locale. Le copie stanno in `_notes/fonti-studio/`, le conversioni in `_notes/.tmp-doc-cache/`, la wiki compilata e le sue fonti in `knowledge/sources/` e `knowledge/wiki/`, le skill generate dai libri sotto `.claude/skills/libro-*/`: tutti ignorati da git. Restano tracciati soltanto gli strumenti, le skill di procedura, lo schema e il registro della wiki. Il report cita i testi in bibliografia e non ne riproduce il contenuto.

Motivazione. La scelta è dell'utente, che ha preferito l'uso locale per studio alla lista di testi da procurarsi. La differenza rispetto ad ADR-010 è che quella decisione riguarda programmi installati ed eseguiti come corredo del progetto, mentre qui si tratta di materiale di studio che non viene ridistribuito né incorporato.

Conseguenze. Nessun estratto testuale di quei libri entra nei documenti tracciati: le pagine di `docs/` e il report parafrasano e citano. I file su `J:` si leggono e basta, secondo il vincolo di `CLAUDE.md`.

## ADR-029 - Il report LaTeX dei monitor si apre adesso e cresce con il progetto, superando l'innesco di ADR-022

Data: 2026-10-01. Stato: accettata, su scelta esplicita dell'utente.

Contesto. ADR-022 lasciava intatto l'innesco della roadmap per cui il report di progetto si scrive soltanto arrivati alle fasi 4 e 5, per non scrivere la teoria di due metodi prima di averne l'applicazione. L'utente ha chiesto un report LaTeX dettagliato anche matematicamente, da ingegnere elettroacustico, di ciò che il progetto fa.

Decisione. Il report si apre adesso con la struttura completa, e ogni capitolo si scrive quando la fase corrispondente produce dati o decisioni, con la matematica e le fonti; la teoria entra quando serve a una decisione reale, cominciando dal confronto fra crossover passivo e attivo.

Motivazione. L'innesco di ADR-022 proteggeva dal rischio di un documento teorico scollegato dal diffusore. Un report che cresce capitolo per capitolo, legato alle decisioni man mano che si prendono, conserva quella protezione senza rimandare la scrittura.

Conseguenze. ADR-022 resta valida per l'istanziazione del pacchetto `latex` e decade soltanto per l'innesco. Ogni capitolo dichiara lo stato delle grandezze che usa, cioè misurate, simulate o ipotizzate.

## ADR-030 - Il server MCP di OpenAlex entra nel progetto, superando ADR-023

Data: 2026-10-01. Stato: accettata, su scelta esplicita dell'utente al gate dei pacchetti.

Contesto. ADR-023 non configurava alcun server MCP, perché il progetto non aveva un servizio esterno da interrogare. Con il report ingegneristico e la base di conoscenza il progetto ha bisogno di letteratura scientifica con metadati verificabili, ed era l'innesco dichiarato del rinvio di OpenAlex.

Decisione. `.mcp.json` in radice dichiara il server ufficiale `openalex` su `https://mcp.openalex.org/mcp`, e `.codex/config.toml` lo stesso per Codex. Nessun token nei file: il login OAuth si fa nello store privato del client.

Motivazione. È il server ufficiale indicato dal runbook del pacchetto, e copre la scoperta di articoli e la risoluzione dei riferimenti, che il report richiederà.

Conseguenze. Il server occupa token a ogni turno quando è connesso. Il login lo fa l'utente con `/mcp` in una sessione nuova di Claude Code. Il conteggio dei server di progetto passa da zero a uno.

## ADR-031 - Nessuno strumento di ricerca a consumo: OpenAlex, PaperQA2 e Feynman tolti, ADR-030 superata

Data: 2026-10-01. Stato: accettata, su scelta esplicita dell'utente.

Contesto. MS-179 aveva dichiarato OpenAlex in `.mcp.json` e installato PaperQA2 e Feynman, in attesa delle credenziali dell'utente. Spiegate le credenziali, l'utente ha chiesto se fossero a consumo e ha deciso di lasciar perdere: PaperQA2 e Feynman usano un modello linguistico tramite API, pagata per token e non coperta dall'abbonamento con cui si lavora qui, salvo un modello locale; OpenAlex ha un uso gratuito con limiti, con condizioni non verificate.

Decisione. `.mcp.json` e `.codex/config.toml` sono tolti, l'ambiente virtuale `.venv` con PaperQA2 è rimosso, e Feynman è disinstallato dal sistema con il permesso esplicito dell'utente. Il progetto torna senza server MCP, come in ADR-023.

Motivazione. Nessuno dei tre strumenti serve a ciò che il progetto fa senza una spesa ricorrente, e la ricerca bibliografica si fa con le fonti lette in rete e registrate, con la base di conoscenza locale e con le skill di `academic-researcher`, che restano.

Conseguenze. ADR-030 è superata. Le skill di `academic-researcher` restano istanziate e funzionano senza i tre strumenti, con la ricerca manuale. Il gate si potrà riproporre se diventasse disponibile un modello locale adeguato.

## ADR-032 - Il report LaTeX resta fuori dal versionamento finché non è completo

Data: 2026-10-01. Stato: accettata, su scelta esplicita dell'utente.

Contesto. ADR-029 ha aperto il report dei monitor come documento che cresce con il progetto. L'utente ha chiesto di versionarlo soltanto quando sarà completo.

Decisione. La cartella `report/` è nel `.gitignore`. Quando il report sarà completo si toglie quella riga e lo si versiona.

Conseguenze. Finché resta ignorato, il report non è nella storia di git né su GitHub: la sua sola copia di sicurezza è quella giornaliera di `sync-dev`, che copia `E:\` sull'SSD esterno. Lo stato del report si traccia comunque nel registro dei microstep e nel work-log, capitolo per capitolo, così che il lavoro sia ricostruibile anche senza il sorgente.

## ADR-033 - I monitor si progettano attivi, con il crossover in un processore digitale

Data: 2026-10-02. Stato: accettata, su scelta esplicita dell'utente.

Contesto. L'utente partiva dall'ipotesi del passivo e ha chiesto un confronto scritto prima di decidere, che è `docs/52-crossover-passivo-o-attivo.md` con il capitolo sul crossover del report. Il confronto ha indicato due punti propri di questo progetto: con un processore digitale la risposta si corregge dopo la misura in stanza, compresi i modi della stanza alle basse frequenze, e la stanza non è trattabile acusticamente; e il programma di configurazione di un processore va verificato su Linux. Ha dichiarato anche che le due fonti tecniche lette, Linkwitz ed Elliott, sono favorevoli all'attivo.

Decisione. Diffusori attivi a due vie, con un canale di amplificazione per altoparlante e il crossover realizzato in un processore digitale di segnale.

Motivazione. La possibilità di correggere in un processore è il vantaggio più legato alla premessa del progetto, cioè una stanza nota e non trattabile, con una verifica finale al punto di ascolto; l'attivo toglie inoltre la dipendenza del filtro dall'impedenza degli altoparlanti, e completa la catena di ascolto di ADR-012 senza un amplificatore di potenza esterno.

Conseguenze. Il progetto in VituixCAD produce coefficienti biquad e ritardi invece di valori di componenti. Gli acquisti finali di ADR-027 comprendono, per ciascun cabinet, due canali di amplificazione e un processore, oppure un modulo che li integri, invece dell'amplificatore stereo esterno e dei componenti della rete; la scelta del modulo e la verifica della compatibilità con Linux del suo programma di configurazione sono PA-024. Il capitolo del report sul crossover prosegue sulla realizzazione digitale.

## ADR-034 - Il progetto diventa una tesi, con la matematica dimostrata da zero, e la documentazione operativa resta aggiornata a ogni passo

Data: 2026-10-02. Stato: accettata, su scelta esplicita dell'utente.

Contesto. L'utente ha dichiarato di voler fare di questo progetto praticamente una tesi: matematica che dimostra le cose, spiegata come se si partisse da zero, con appendici di elettronica, acustica ed elettroacustica, e una ricerca bibliografica come prescrive il template. Il report LaTeX di ADR-029 esiste già in `report/` con un capitolo per fase e un'appendice di notazione.

Decisione. Il report di ADR-029 diventa la tesi e continua a crescere con il progetto, invece di essere scritto alla fine o in un documento separato. Ogni risultato usato in un capitolo si deriva, e le basi che servono a derivarlo stanno in appendici: matematica, elettrotecnica ed elettronica, fisica ed elettromagnetismo, acustica, elettroacustica, elaborazione numerica del segnale. Accanto alla tesi, le pagine Markdown di `docs/` restano il resoconto contestuale e sempre aggiornato di ogni punto del progetto, comprese le operazioni e i setup eseguiti, secondo la regola delle pagine prescrittive di `CLAUDE.md`: l'utente ha chiesto esplicitamente che nessun passaggio operativo vada perso. La ricerca bibliografica segue il pacchetto `academic-researcher`, con lo scope in `research-vault/scope.md`, il registro in `research-vault/tracked-sources.md`, il `.bib` in `research-vault/bibliography.bib`, e i PDF in `research-vault/papers/`, ignorata da git. L'autonomia è propongo e l'utente conferma.

Motivazione. Una tesi che cresce con il progetto obbliga a scrivere la ragione di una scelta quando la si prende, che è la stessa ragione per cui esiste `chat-non-e-memoria.md`; scriverla dopo significherebbe ricostruirla. Le due forme hanno lettori diversi: la tesi spiega perché e dimostra, le pagine di `docs/` dicono che cosa è stato fatto e come rifarlo.

Conseguenze. Il capitolo sul crossover, già scritto, va ripreso con le derivazioni complete. Restano valide ADR-028 per i libri, ADR-031 per gli strumenti a consumo e ADR-032 per il versionamento della tesi. La tesi magistrale dell'utente del 2020, censita su `J:` in MS-185, è il primo modello di struttura e stile da leggere.

## ADR-035 - Il vault di ricerca è un vault Obsidian sul modello di intralino, e contiene le copie locali di tutto il materiale

Data: 2026-10-02. Stato: accettata, su richiesta esplicita dell'utente.

Contesto. La ricerca bibliografica della tesi di ADR-034 aveva il materiale sparso: le copie dei lotti e la libreria JabRef sotto `_notes/fonti-studio/`, lo scope e il registro in `research-vault/`. L'utente ha chiesto di portare nel vault di ricerca una copia di tutto ciò che serve e di inizializzarlo come vault Obsidian con le stesse caratteristiche di quello del progetto `D:\intralino-benchmark`.

Decisione. `research-vault/` è un vault Obsidian con la configurazione e i tre plugin comunitari di intralino, una nota d'ingresso `00-START`, note numerate, una scheda per fonte selezionata in `paper/`, il registro unico `fonti.json` generato da `tools/registro-fonti.py` e i PDF in `papers/` con il manifesto delle impronte. Le copie del materiale di studio stanno in `research-vault/fonti-locali/lotto-NN/`, copiate da `tools/copia-lotti.py`, e le basi di terzi in `research-vault/basi/`. Questo supera la posizione `_notes/fonti-studio/` di MS-179 e del piano di MS-184.

Motivazione. Un solo posto per la ricerca rende possibile un registro unico delle provenienze, che l'utente ha chiesto completo di ciò che c'è, di ciò che scarica e di ciò che l'agente propone. Il grafo di Obsidian funziona soltanto se schede e note stanno nello stesso vault.

Conseguenze. Il `.gitignore` tiene locali copie, basi di terzi, PDF, plugin e stato dell'interfaccia, per ADR-028; si versionano note, configurazione, schede, registro e manifesto. Chi clona il repository reinstalla i plugin con BRAT. Restano valide ADR-028 e ADR-031.

## ADR-036 - Il materiale di studio resta su J: e il progetto lo indicizza, invece di copiarlo

Data: 2026-10-02. Stato: accettata, su scelta esplicita dell'utente; supera la parte di ADR-035 che metteva le copie del materiale dentro il vault.

Contesto. Con MS-189 il vault di ricerca conteneva 4039 file copiati da `J:`, per 5,62 GiB. Il progetto è oggetto di una copia di sicurezza giornaliera due volte al giorno, e l'utente ha chiesto di portare il materiale in `J:\MAIN` e di indicizzare tutto da questo progetto. Dei 5,62 GiB, 3,95 erano copie identiche per impronta di file che stanno già in `J:\MAIN`; gli altri 1,67 erano i file estratti dai dieci archivi, che su `J:` non esistevano estratti.

Decisione. Fra due vie, l'utente ha scelto quella senza doppioni. Le copie dei lotti sono tolte dal progetto, e l'indice punta agli originali in `J:\MAIN`. I soli file estratti dagli archivi sono scritti su `J:`, nella cartella nuova `J:\MAIN\_ESTRATTI ARCHIVI TESI`, con il permesso esplicito dell'utente dato per quei file. Il progetto conserva i registri `lotto-NN-origine.json` con posizione e impronta di ogni file, il piano, i censimenti e i manifesti. La cache di conversione in Markdown resta nel progetto, in `_notes/.tmp-doc-cache/fonti/`: è testo leggero e serve anche con il disco scollegato.

Motivazione. Un doppione di materiale che esiste già non aggiunge sicurezza e appesantisce ogni copia di sicurezza; un indice con l'impronta permette invece di accorgersi se un originale cambia o sparisce, con `tools/indicizza-lotti.py --verifica`.

Conseguenze. La conversione e la lettura dei documenti richiedono `J:` collegato; la cache convertita no. Gli strumenti di copia diventano strumenti di indice: `copia-lotti.py` è sostituito da `indicizza-lotti.py`, `estrai-archivi.py` scrive solo nella destinazione indicata dall'utente e non cancella nulla, e `converti-fonti.py` legge da `J:`. Restano valide ADR-028, ADR-035 per la forma del vault, e il vincolo di `CLAUDE.md` su `J:`: nessuna scrittura senza permesso esplicito per i file nominati.

## ADR-037 - Il taglio della tesi è quello degli appunti dell'utente sulle lezioni del Politecnico

Data: 2026-10-05. Stato: accettata, dichiarata dall'utente.

Contesto. ADR-034 fissa che la tesi dimostra la matematica da zero e ha appendici di base, ma non dice con quale taglio. L'utente ha indicato il 2026-10-05 che i suoi `.docx` della cartella `LOUDSPEAKERS & ELECTROACOUSTIC`, dove ha messo le formule e ha sbobinato le lezioni del Politecnico di Milano, sono quel taglio, e che EEASE II ed EEASE Exercises sono interessanti quanto EEASE I.

Decisione. Il riferimento di stile e di livello della tesi sono quegli appunti, con EEASE I, EEASE II ed EEASE Exercises in testa, insieme a Fundamentals of Acoustics, Musical Acoustics e Acustica applicata: lo stesso ordine di derivazione, la stessa notazione dove possibile, lo stesso grado di dettaglio nei passaggi. I libri e i paper servono a completare, verificare e citare, non a cambiare il taglio.

Motivazione. Gli appunti sono già la forma in cui l'utente ha capito la materia, e una tesi che li riprende resta la sua; un testo che riprendesse il taglio di un manuale sarebbe un riassunto.

Conseguenze. Le formule degli appunti si estraggono con pandoc, perché markitdown le perde (MS-191). Prima di scrivere un capitolo si legge la parte degli appunti che lo tratta, e la notazione dell'appendice a1 si allinea a quella degli appunti, dichiarando le eccezioni.

## ADR-038 - Le fonti vivono in un vault su J:, la ricerca resta nel repository, e la biblioteca è la più completa possibile

Data: 2026-10-05. Stato: accettata, su scelta esplicita dell'utente; precisa ADR-035 e ADR-036.

Contesto. Con MS-196 e MS-197 è emerso che l'indice copriva una parte selezionata a mano del materiale di `J:`. L'utente ha chiesto tre cose: l'analisi di tutte le sottocartelle pertinenti di `J:\MAIN` e di `J:\_____da sistemare ancora`; una biblioteca con tutti i paper, suddivisa per gruppi come la libreria JabRef `ELE_Technical_Library.bib`; e un vault completo delle fonti dentro `J:\MAIN\LOUDSPEAKERS & ELECTROACOUSTIC`.

Decisione. Le scelte dell'utente sono quattro.
- Il censimento copre le cartelle tecniche e l'università: `z_____UNIVERSITA`, `ANALOG (AUDIO) ELECTRONICS`, `MATH and CALCULUS`, `TLC, SIGNAL PROCESSING and DIGITAL FILTERS`, le due `COMPUTER MUSIC`, `F.I.S.I.C.A and ELECTROMAGNETISM`, `MACHINE LEARNING`, `LATEX(+typesetting)`, `SOLIDWORKS` ed `ELETTROTECNICA`, più `ELE_Technical_Library.bib` e `materiale_formazione_elettronica.docx` di `J:\_____da sistemare ancora`. Restano fuori `PROGRAMMING`, `ISTAO`, `MARKETING`, `ENGLISH`, `SOFT SKILLS`, `PROJECT MANAGEMENT`, `FIRMWARE`, `DATA ANALYSIS`, `MUSIC`, `Teaching` e `ALTRO`.
- Il vault su `J:` contiene una nota per ogni fonte, accanto al materiale, organizzata per gruppi. `research-vault/` nel repository resta il luogo della ricerca, cioè protocollo, registri, piano e analisi, e rimanda al vault su `J:`. Uno strumento rigenera il vault su `J:` dall'indice senza sovrascrivere le note scritte a mano.
- La biblioteca va riorganizzata "nella versione più completa che sia mai esistita", con le parole dell'utente. L'albero dei gruppi di quella libreria è il punto di partenza e non il limite. Entrano tutte le fonti dell'indice, dei paper scaricati, delle proposte e della libreria JabRef, con gruppi per disciplina, un ramo per i capitoli della tesi e per i filoni R1-R12, e il campo `file` verso la posizione su `J:`.
- Delle copie estratte in `J:\MAIN\_ESTRATTI ARCHIVI TESI` si cancellano software e dati, e si tengono i documenti, i modelli COMSOL e il toolbox MPM.

Motivazione. Il materiale vive su `J:` per ADR-036, quindi le note che lo descrivono stanno meglio accanto a esso, mentre il lavoro di ricerca, che cambia a ogni sessione, va versionato. Una biblioteca organizzata per disciplina e per capitolo risponde a due domande diverse: che cosa c'è su un argomento, e che cosa sostiene un punto della tesi.

Conseguenze. Scrivere il vault su `J:` è una scrittura di file nuovi, autorizzata dall'utente con questa decisione, e lo strumento non cancella né sovrascrive nulla di esistente. La biblioteca si genera da uno strumento e non si compila a mano, così che si rigeneri quando l'indice cresce. Il lavoro è PA-027.

## ADR-039 - Il vault delle fonti su J: è la fonte bibliografica di tutti i progetti di acustica

Data: 2026-10-05. Stato: accettata, istruzione dell'utente; estende ADR-038 oltre questo progetto.

Contesto. Con MS-201 `tools/biblioteca.py` ha generato in `J:\MAIN\LOUDSPEAKERS & ELECTROACOUSTIC\_VAULT FONTI\` la biblioteca JabRef e il vault con 8194 fonti. L'utente ha chiesto che tutti i progetti attinenti all'acustica vadano a cercare lì le loro fonti.

Decisione. Il vault su `J:` è la base bibliografica comune dei progetti di acustica, elettroacustica, audio ed elaborazione del segnale dell'utente. Un progetto di quel dominio cerca prima nel vault, cita la chiave della biblioteca, e porta ciò che trova di nuovo nel registro di questo progetto, così che la rigenerazione lo includa. Le note di lettura scritte nel vault valgono per tutti i progetti.

Motivazione. Una biblioteca per progetto duplica il lavoro di censimento e di classificazione, e le copie divergono. Una sola biblioteca, rigenerata da uno strumento, resta coerente.

Conseguenze. Questo progetto resta il proprietario dello strumento, delle regole e del registro. Gli altri progetti leggono il vault e non lo rigenerano. La propagazione dell'istruzione nei progetti candidati si fa in una sessione aperta in ciascuno di essi, perché l'agente resta sul perimetro di questo progetto, ed è PA-029. Se il disco `J:` non è collegato, il vault non è raggiungibile: un progetto che ne dipende lo dichiara invece di supporre le fonti.

## ADR-040 - Niente di ciò che viene dall'SSD privato entra in un file tracciato

Data: 2026-10-05. Stato: accettata, istruzione dell'utente; rafforza ADR-028.

Contesto. Il repository è pubblico, e il materiale di studio viene dall'SSD privato dell'utente. ADR-028 teneva fuori dai file tracciati i percorsi e il contenuto dei libri, ma non i titoli dei file. Così il commit della mattina del 2026-10-05, poi sostituito, ha pubblicato in `fonti.json` i titoli di 3300 file, compresi documenti personali e nomi di persone. L'utente ha chiesto di stare molto attenti a che cosa finisce su GitHub.

Decisione. Nessun file tracciato contiene titoli, nomi di file, percorsi di singoli file o nomi di persone che vengono dal disco privato, salvo le citazioni bibliografiche di opere pubblicate. I registri e le regole che descrivono il disco vivono in `_notes/`, che è ignorata. Ogni commit passa da `tools/check-privato.py`, che cerca i termini dell'elenco locale `_notes/privacy/termini.txt`, le tracce di provenienza non ufficiale dei libri e i percorsi di singoli file su `J:`. Le persone da cui veniva il materiale si anonimizzano anche sul disco, con il permesso dell'utente elenco alla mano, e gli autori dei testi restano.

Motivazione. Un dato pubblicato non si ritira davvero, perché la storia e le copie restano. L'unico momento in cui la protezione costa poco è prima del commit, e un controllo meccanico non dipende dall'attenzione di chi scrive.

Conseguenze. Il registro pubblico tiene libreria, tesi del 2020, proposte e scaricati, mentre il registro completo è locale. Le pagine di `docs/` descrivono il disco per categorie e non per file. L'elenco dei termini cresce con ogni nome o documento da proteggere. La regola e lo strumento vanno al template, come voce di PA-003.

## ADR-041 - La wiki da J:/MAIN si costruisce a tre livelli, un lotto alla volta su permesso

Data: 2026-10-06. Stato: accettata, risposte dell'utente alle sette domande di `research-vault/10-Piano-digestione-MAIN.md`.

Contesto. L'utente vuole nella wiki tutto ciò che di utile c'è in `J:\MAIN`. Alla profondità degli appunti EEASE, circa 5 token per parola, i 91,2 milioni di parole in testo costerebbero oltre 450 milioni di token (MS-209).

Decisione. Tre livelli. Il livello 1 è la lettura profonda del nucleo, cioè gli appunti dei corsi pertinenti, i manuali cardine della tesi e i paper centrali scelti con il criterio dello stadio per stadio. Il livello 2 è una scheda di fonte del modello economico per ogni documento pertinente, sul perimetro di cartelle e corsi proposto nella domanda 4 e accettato per intero. Il livello 3 è la sola voce di biblioteca. Il materiale sui pedali va al progetto della pedaliera di PA-030, con la sua wiki. Gli appunti diventano pagine della wiki, i manuali skill `libro-` con `book-digest`, e l'impianto di conversione del template resta intero. Si misura prima un lotto di prova per livello, poi l'utente decide lotto per lotto, e ogni lotto parte solo dopo il suo permesso.

Motivazione. La lettura profonda di tutto non è sostenibile, e le schede fanno sapere alla wiki che cosa esiste senza leggerlo per intero. Il permesso per lotto tiene la spesa sotto il controllo dell'utente, che è la sola persona a conoscere la quota e le priorità del momento.

Conseguenze. Le fonti non lette non escono dall'orizzonte dell'agente: chi risponde dalla wiki sa che esistono la biblioteca e il vault su `J:`, le schede del livello 2 e la cache convertita, e li consulta o lo dichiara prima di concludere che una fonte manca. La voce 25 della roadmap diventa il lotto di prova, in attesa del permesso.

## ADR-042 - I documenti personali non si leggono mai senza richiesta espressa

Data: 2026-10-06. Stato: accettata, istruzione vincolante dell'utente, da portare anche nel template come regola generale.

Contesto. La conversione con OCR rilanciata il 2026-10-06 lavorava su tutto ciò che era indicizzato in `J:\MAIN`, comprese le cartelle con contratti, pratiche di borsa di studio, documenti d'identità, certificati e ricevute. Gli schemi sui soli percorsi ne riconoscono 54 indicizzati, già convertiti in testo nella cache locale dalle corse precedenti.

Decisione. I documenti personali non si leggono, non si convertono, non si passano all'OCR e non si sintetizzano, a nessun livello, se non su richiesta espressa dell'utente per quei documenti. La regola è `.claude/rules/documenti-personali.md`, scritta nel template e istanziata qui. Gli strumenti `converti-fonti.py` e `biblioteca.py` li escludono dal percorso prima di aprirli, con `tools/privato_esclusi.py` e gli schemi nel file locale `_notes/privacy/esclusi-personali.txt`, e senza quel file si fermano.

Motivazione. Un'esclusione affidata a chi lancia lo strumento si perde alla prima corsa di massa, che è esattamente quella che stava succedendo. Un filtro nello strumento non dipende dal ricordarsene.

Conseguenze. L'OCR in corso è stato fermato prima di arrivare a quei documenti. Le copie in testo già nella cache si trattano secondo PA-031, su decisione dell'utente.

## ADR-043 - La base di conoscenza serve i monitor, e non sostituisce il loro progetto

Data: 2026-10-06. Stato: accettata, richiamo dell'utente.

Contesto. Nella giornata del 2026-10-06 il lavoro è andato quasi tutto alla base di conoscenza: OCR, 450 schede di fonte, tre fonti di livello 1, le correzioni degli appunti originali, le lezioni per il template. L'utente ha riconosciuto il valore di quel lavoro e ha ricordato che lo scopo del progetto resta progettare e costruire la coppia di monitor a due vie, con la tesi che li sostiene.

Decisione. La base di conoscenza è uno strumento della tesi e del progetto, e non un fine. Ogni volta che l'agente propone i passi successivi dopo un lavoro sulla base di conoscenza, propone anche il passo concreto successivo sul nucleo del progetto, cioè la stanza, i driver, la cassa, il crossover, il processore e le misure, preso dalla roadmap. La digestione di `J:\MAIN` procede per lotti finché serve ai capitoli della tesi che si stanno scrivendo, e non per completezza.

Motivazione. Un lavoro di raccolta ha sempre un lotto successivo, e senza un richiamo esplicito tende a occupare tutte le sessioni. Il progetto si misura sui monitor costruiti e sulla tesi scritta, non sulle pagine della wiki.

Conseguenze. La chiusura di ogni risposta, che già riporta la roadmap, nomina anche il primo passo del nucleo. La voce 25 della roadmap passa a una cadenza decisa dai capitoli in stesura.

## ADR-044 - J:\MAIN è l'archivio principale dell'utente, non un'appendice del progetto

Data: 2026-10-06. Stato: accettata, precisazione dell'utente.

Contesto. Il progetto ha indicizzato, convertito e in qualche punto modificato file di `J:\MAIN`: la biblioteca e il vault delle fonti, le copie parallele degli appunti EEASE e i commenti negli appunti originali. L'utente ha ricordato che `MAIN` è il suo archivio principale di tutto, a prescindere da questo progetto.

Decisione. Ogni intervento su `J:\MAIN` si giudica per l'archivio nel suo insieme e non per la comodità del progetto. Non si riorganizzano cartelle per farle combaciare con la struttura della tesi. Una copia parallela di un file in più cartelle è ammessa quando l'utente la vuole, perché ciascuna cartella è un punto in cui la cerca. Restano valide le regole già in vigore: nessuna scrittura senza il permesso esplicito per i file nominati, dalla sezione sui dati personali di `CLAUDE.md`, e nessuna lettura dei documenti personali, da ADR-042.

Motivazione. L'archivio esisteva prima del progetto e servirà ad altri, come la pedaliera di PA-030 e i progetti di acustica di PA-029. Una modifica pensata solo per questo progetto può peggiorarlo per gli altri usi.

Conseguenze. Prima di proporre una scrittura su `J:\MAIN` l'agente dichiara che effetto ha sull'archivio e non solo sul progetto. Il vault delle fonti su `J:` è una vista dell'archivio, e la sua tassonomia resta generale.

## ADR-045 - Il convertitore della catena di ascolto si sceglie con l'elettronica dei monitor, e il Rod Rain non è un vincolo

Data: 2026-10-06. Stato: accettata, precisazione dell'utente; rivede ADR-012.

Contesto. ADR-012 aveva fissato il Rod Rain audio come sorgente della catena di ascolto, con l'uscita analogica su RCA, perché era già in casa. Nella ricerca di PA-024 l'agente ha trattato quella decisione come un vincolo, e ne ha dedotto un problema d'ingresso per le soluzioni con il processore in un calcolatore. L'utente ha chiarito che il Rod Rain non va usato per forza, e che si può comprare un altro convertitore.

Decisione. Il convertitore della catena di ascolto dei monitor non è fissato. Si sceglie insieme al processore digitale e agli amplificatori di PA-024, con il criterio del costo minimo e della soluzione aperta più completa. Il Rod Rain resta disponibile per le cuffie e per l'altro computer, ed è una delle opzioni, non la premessa.

Motivazione. In una catena attiva con processore digitale il segnale nasce in digitale nel computer, e un convertitore scelto prima del processore impone una conversione in più senza beneficio. La scelta va fatta sull'architettura intera.

Conseguenze. ADR-012 resta valida come descrizione del dispositivo e del suo uso con le cuffie, ma non vincola i monitor. `docs/54-amplificazione-e-dsp.md` ragiona sulla catena da zero, e la candidata più forte diventa CamillaDSP sulla macchina di progetto con un'interfaccia USB a quattro uscite, che può coincidere con l'interfaccia di misura di PA-012. `docs/75-catena-di-riproduzione.md` va riletta alla scelta di PA-024.

## ADR-046 - L'interfaccia candidata per monitor e misura è il Behringer UMC404HD, confermata solo da una misura del fruscio

Data: 2026-10-06. Stato: accettata come candidata, su scelta dell'utente; la conferma dipende da una misura.

Contesto. Con ADR-033 e ADR-045 i monitor sono attivi, con il crossover in CamillaDSP sulla macchina di progetto, e l'interfaccia USB fa da convertitore a quattro canali verso gli amplificatori e da ingresso per il microfono di misura. La ricerca di MS-223 ha confrontato sei interfacce con il criterio dell'utente, cioè costo minimo e soluzione aperta più completa.

Decisione. La candidata è il Behringer UMC404HD, con quattro uscite bilanciate, quattro ingressi con alimentazione phantom e nessuno strumento proprietario nelle fonti lette. Diventa definitiva solo se il fruscio misurato al tweeter, con l'ingresso in silenzio e REW al punto d'ascolto, risulta inudibile con la sensibilità del tweeter e il guadagno degli amplificatori scelti nella fase 4a. Se non lo è, si sale al Focusrite Scarlett 4i4 di quarta generazione o al MOTU M4. L'utente concorda che sensibilità e guadagno si fissano con gli altoparlanti.

Motivazione. È l'interfaccia meno cara che soddisfa tutti i requisiti letti, e il suo solo rischio, la dinamica dichiarata più bassa, si chiude con una misura che il progetto deve fare comunque. Comprare subito un'interfaccia più costosa pagherebbe in anticipo un rischio non ancora accertato.

Conseguenze. L'acquisto resta alla fine con gli altri, per ADR-027, e la misura del fruscio entra nella verifica della fase 8. La scelta vale anche per il progetto gemello, dove PA-012 va aggiornata in una sessione aperta lì.
