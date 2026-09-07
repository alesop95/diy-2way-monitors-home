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

Data: 2026-09-04. Stato: accettata dall'utente in sessione, **rivista da ADR-011 il 2026-09-07**: la verifica sulla macchina ha smentito la premessa del primo dei quattro motivi, che va quindi letto come caduto. La decisione resta difendibile sui tre restanti e va riconfermata dall'utente sulla base corretta. Il testo che segue è quello originale e non è stato riscritto.

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

## ADR-011 - Revisione di ADR-006: la motivazione cade da quattro a tre, la decisione va riconfermata

Data: 2026-09-07. Stato: accettata come revisione. La decisione operativa che rivede, cioè ADR-006, resta in attesa di riconferma dall'utente sulla base corretta.

Contesto: ADR-006 aveva scelto l'installazione pulita di Ubuntu Studio 26.04 LTS invece dell'aggiornamento in posto, con quattro motivi, e la diagnosi su cui poggiava non era verificata sulla macchina. La fase 0 della procedura, eseguita il 2026-09-07 e documentata in `docs/10-ambiente/fotografia-macchina-2026-09-07.md`, ha smentito tre delle quattro cause attribuite al blocco di aggiornamento e ha rivelato che l'aggiornamento non era mai stato tentato.

Decisione: registrare che il primo dei quattro motivi di ADR-006 è venuto meno, che gli altri tre restano validi, che se ne aggiunge uno nuovo, e che la decisione va riconfermata dall'utente sapendo questo invece di essere data per acquisita.

Motivazione, motivo per motivo. Il primo motivo era che l'installazione fosse più corta e più prevedibile di due aggiornamenti in cascata attraverso archivi storici: è caduto, perché di cascate non ce n'è bisogno e di archivi storici non se ne attraversa nessuno. L'alternativa reale è un aggiornamento dei 134 pacchetti pendenti, un riavvio che il sistema chiede già, e un solo `do-release-upgrade` verso la 26.04.1 LTS che lo strumento propone adesso. Il secondo motivo, l'ambiente pulito, è non solo valido ma rafforzato: la fotografia ha mostrato la sedimentazione in forma concreta, cioè due repository WineHQ attivi per due rilasci diversi di Ubuntu, `wine-stable 3.0.1` del 2018 accanto a `wine 9.0`, l'architettura `i386` dichiarata, una sorgente `file:/cdrom/` residua e un prefix unico condiviso fra programmi. Il terzo motivo, la licenza di Akabak non a rischio, non è toccato. Il quarto, la base supportata fino al 2031, non è toccato.

Il motivo nuovo che la fotografia rende disponibile: `/home` contiene 3,7 GB su 369 disponibili, cioè il 2 per cento. Il costo del salvataggio dei dati è quindi trascurabile e il rischio dell'operazione è più basso di quanto si potesse stimare senza il dato.

Conseguenze: la decisione resta difendibile, ma su tre motivi invece di quattro, e con una alternativa molto meno onerosa di come era stata descritta. Chi legge la documentazione non deve trovare la vecchia motivazione intatta, quindi la pagina della diagnosi porta l'avvertenza in apertura e le tre cause sono marcate come smentite nel corpo. Se l'utente sceglie di riconfermare l'installazione pulita, il motivo dominante diventa l'ambiente pulito e non la fragilità dell'alternativa. Se sceglie l'aggiornamento in posto, la sequenza è nella strada A della pagina corretta, e il lavoro reale sta nel disattivare i due repository WineHQ prima di iniziare.

Nota metodologica, perché è il vero contenuto di questa voce. ADR-006 era stata registrata come proposta e poi accettata prima che la sua premessa fosse verificata, con la giustificazione che la verifica era il primo passo della procedura. Quella giustificazione era corretta in principio e ha funzionato in pratica, perché la verifica ha effettivamente preceduto qualunque modifica al disco. Ma il fatto che tre cause su quattro fossero sbagliate mostra quanto poco valga una ricostruzione plausibile: la decisione era giusta per ragioni in parte sbagliate, e questo è un esito diverso dall'aver avuto ragione.

## ADR-012 - Il Rod Rain audio è la sorgente della catena di ascolto, e questo anticipa la scelta fra monitor attivi e passivi

Data: 2026-09-07. Stato: accettata per la sorgente; la conseguenza sull'architettura del diffusore resta aperta.

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

Conseguenza operativa immediata, e non è ovvia: **la pulizia dell'ambiente Wine non si esegue**. Pulire Wine su un sistema che verrà azzerato è lavoro che si butta, perché la riformattazione di root porta via l'intera installazione dei pacchetti, i due repository WineHQ, l'architettura `i386` e la sorgente residua. L'ambiente pulito si ottiene per costruzione dalla reinstallazione, non da una purga preventiva. Per la stessa ragione non si applicano i 134 pacchetti pendenti e non si esegue il riavvio richiesto: sono operazioni sul sistema che sta per essere sostituito.

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

Decisione: la copia va sulla postazione Windows, come archivio `tar` non compresso prodotto in streaming attraverso `ssh`. Non va su alcuna partizione della macchina. La destinazione scritta all'atto della decisione era `E:\_backup-ubuntu-studio\`; l'utente ha poi spostato l'archivio in `C:\Users\Utente\Desktop\_backup-ubuntu-studio\`, con dimensione identica al byte, e questo **non altera la decisione**, perché la proprietà che la motiva è che il supporto sia una macchina diversa da quella protetta, non una lettera di unità particolare. Ne segue una regola per gli strumenti di verifica: la condizione da controllare è l'esistenza dell'archivio per nome fra più posizioni plausibili, non la presenza di un percorso fisso, altrimenti uno spostamento legittimo fa dichiarare mancante un backup che c'è.

Motivazione del rifiuto della prima opzione. La verifica mostra che la macchina ha un solo disco, `nvme0n1` da 465,8 GB, con quattro partizioni e nient'altro, e nessun disco USB collegato. Le tre varianti pensabili fallirebbero per ragioni diverse: su root la copia morirebbe con la formattazione, su `/home` stessa non proteggerebbe da nulla perché il rischio da coprire è precisamente la perdita di quella partizione, e una partizione nuova richiederebbe di ridurre `/home` con una operazione rischiosa in sé senza proteggere da un errore di selezione né da un guasto del disco. La regola generale: una copia di sicurezza sullo stesso supporto della cosa che protegge non è una copia di sicurezza, è una copia.

Motivazione della scelta della seconda. `/home` pesa 4,4 GB contro 198 GB liberi sulla destinazione, quindi il costo è trascurabile, e soprattutto è una macchina fisicamente diversa, che è l'unica proprietà che rende un backup un backup.

Motivazione del metodo, che non è un dettaglio. Si usa `tar` in streaming e non `scp` dei file, perché la destinazione è NTFS e non sa rappresentare proprietario, gruppo e permessi POSIX: copiando i file singoli quei metadati andrebbero perduti e il ripristino produrrebbe una `/home` con i permessi sbagliati. Dentro un archivio quei metadati sono contenuto e sopravvivono anche su NTFS. Si usa `--numeric-owner` perché il ripristino non dipenda dall'esistenza dell'utente con quel nome. Non si comprime perché dei 4,4 GB la maggior parte sono installer e archivi già compressi.

Conseguenze: PA-007, cioè la cancellazione della copia del corredo sul Desktop di Windows, è sbloccata. L'archivio va rigenerato se `/home` cambia in modo significativo prima della reinstallazione, e la sua verifica è il confronto fra il numero di file nell'archivio e quelli sulla macchina, non la sola assenza di errori.

## ADR-016 - Akabak è a 32 bit: revisione di ADR-004, ADR-009 e ADR-013 sull'architettura dei prefix

Data: 2026-09-07. Stato: accettata. Supera la parte sull'architettura di ADR-004, ADR-009 e ADR-013.

Contesto: tre decisioni precedenti poggiavano sull'affermazione, presa dal documento sorgente, che Akabak 3 sia una applicazione a 64 bit senza build a 32 bit, e ne concludevano che servisse un prefix a 64 bit e che l'architettura `i386` fosse un residuo da non riprodurre sulla macchina nuova. L'ispezione del prefix funzionante sulla macchina smentisce la premessa.

I fatti misurati. Il prefix in uso è `/home/alesop95/.wine` e il suo registro dichiara `#arch=win32`, cioè è un prefix a **32 bit**; la cartella `syswow64` è assente, come deve essere in un prefix a 32 bit. L'eseguibile installato, `AKABAK.exe`, è `PE32 executable, Intel 80386`, cioè **a 32 bit**. Lo stesso vale per `VACS_32.exe`, e la libreria che entrambi portano si chiama `Matrix32.dll`. Nel prefix non esiste alcun `winetricks.log`, non esiste `Microsoft.NET/Framework/v4` e non è installato alcun font Microsoft di base.

Decisione: Akabak e VACS vanno in un prefix a **32 bit**, senza dipendenze installate con winetricks, riproducendo la configurazione che funziona. L'architettura `i386` va dichiarata sul sistema, perché è necessaria e non residua. VituixCAD ed EASE Focus restano su prefix a 64 bit, perché i loro requisiti sono dichiarati dai rispettivi produttori e su questa macchina non sono mai stati installati, quindi non c'è nulla da riprodurre e nulla da smentire.

Motivazione: la configurazione che funziona su questa macchina batte qualunque requisito dichiarato in un appunto. Il documento sorgente descriveva Akabak come a 64 bit con bisogno di .NET 4.8 e di font e runtime aggiuntivi, e nessuna di quelle affermazioni è confermata dall'installazione reale: la lista delle dipendenze del sorgente descriveva ciò che era stato tentato durante il troubleshooting, non ciò che serviva.

Conseguenze, e sono sostanziali. La fase 7 della procedura di installazione pulita, che prescriveva quattro prefix a 64 bit con `dotnet48`, è sbagliata per Akabak e VACS e va corretta. Il consiglio di non dichiarare l'architettura `i386`, dato in ADR-009 e ripetuto in ADR-013, è rovesciato: senza `i386` il solo software del progetto che oggi funziona non funzionerebbe più. Il conteggio dei prefix passa da quattro a quattro ma con architetture diverse, cioè uno a 32 bit per Akabak e VACS e tre a 64 bit per gli altri.

Resta valida la parte di ADR-004 che non riguarda l'architettura, cioè un prefix per programma, con l'eccezione dichiarata di Akabak e VACS che condividono il proprio perché si usano in sequenza e perché così è la configurazione funzionante.

Una nota di metodo, che è la lezione vera di questa voce. Tre decisioni consecutive hanno propagato una affermazione non verificata presa da un appunto, e ciascuna l'ha usata come premessa della successiva senza tornare alla fonte. Il costo è stato una prescrizione operativa sbagliata su tre documenti. Il controllo che l'avrebbe evitato costava un comando, cioè `file` sull'eseguibile installato.
