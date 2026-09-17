# Work-log

> Append-only, in ordine cronologico inverso: la voce più recente in alto. Ogni passo significativo lascia una voce con data, file toccati, motivo e commit di riferimento. Il dettaglio tecnico degli interventi, con l'esito verificato di ciascuno, sta in `docs/OPERATIONS-LOG.md`; qui sta il meta-stato.

## 2026-09-17, chiusura - Backup di macchina chiuso, procedura resa portabile, riallineamento al template

Commit di partenza: d2efb3d.

File toccati in questa seconda metà della giornata: `docs/OPERATIONS-LOG.md` con i microstep da MS-128 a MS-135; `docs/10-ambiente/veeam-agent-linux.md`, riscritto in forma parametrica e portato da 152 a oltre 430 righe, più la sua copia nel progetto gemello; `docs/PENDING-ACTIONS.md` con PA-011 chiusa, PA-015 chiusa, PA-003 riscritta e PA-016 aperta e in gran parte compiuta; `tools/check-pending-actions.py`; `CLAUDE.md`; e nel template `.gitignore` e `.claude/rules/git-commands-format.md`.

PA-011 è chiusa dopo sette giorni. L'ordine dei passi è stato quello che la voce prescriveva, cioè prima si finisce di installare e poi si fa il backup, e il criterio di completamento non è stato interpretato al ribasso: l'archivio è stato riletto montandolo e confrontandolo, non soltanto prodotto. Tre limiti restano dichiarati invece di essere taciuti, cioè la destinazione provvisoria, la cifratura rinviata con motivazione e l'assenza di una immagine avviabile.

Due direttive dell'utente hanno cambiato il modo di lavorare, e sono la parte di questa giornata che sopravvive al fronte. La prima è che ogni fronte operativo produca, oltre ai microstep, una procedura replicabile con i soli comandi e il troubleshooting: era stata soddisfatta il 2026-09-16 e non più oggi, ed è ora scritta come obbligo in `CLAUDE.md` invece di dipendere dalla mia attenzione. La seconda è che quella procedura serva su qualunque macchina Linux e non solo su questa, e ha prodotto la riscrittura parametrica della pagina, con i valori da sostituire raccolti in un blocco unico e le tre decisioni che cambiano da macchina a macchina dichiarate accanto.

Il presidio che ne discende è però debole e lo dichiaro: è una riga in un file che va letto, non un controllo che fallisce. Il presidio forte sarebbe uno strumento che si accorge che un fronte operativo ha prodotto microstep senza toccare alcuna pagina prescrittiva, e non esiste. È lo stesso schema di PA-015, che oggi si è chiusa proprio perché una convenzione era stata trasformata in una guardia meccanica.

Tre errori miei sono registrati nei microstep e non nascosti. Un comando consegnato senza dichiarare da quale macchina andasse eseguito, che è MS-126 ed è diventato la quinta causa nella regola sul contesto di shell, portata anche al template. Una affermazione sul deposito dedotta da un `ls` invece che misurata con il comando del programma, ritirata in MS-128. E una affermazione su che cosa riceva chi clona il template, ereditata da PA-003 e da me ripetuta, smentita da `git ls-files` in MS-130. A queste si aggiunge un percorso Windows corrotto in caratteri di controllo mentre scrivevo la chiusura di PA-011, trovato e riparato dentro MS-135.

Il fronte torna alla sottofase 8.6, cioè all'import GLL di EASE Focus, che è l'unico criterio di uscita della fase 8 ancora non soddisfatto e ha un solo candidato residuo, cioè il passaggio ai pacchetti ufficiali di WineHQ. La decisione è dell'utente e oggi è meno rischiosa di due giorni fa, perché lo stato della macchina è recuperabile.

## 2026-09-17 - Ricognizione prima del backup, un comando senza punto di esecuzione, e lo scarto dal template riaperto

Commit di partenza: d2efb3d.

File toccati: `docs/OPERATIONS-LOG.md` con MS-126, MS-127, MS-128 e MS-129; `docs/PENDING-ACTIONS.md` con PA-016 aperta e in gran parte chiusa lo stesso giorno, PA-015 chiusa e PA-003 riscritta; `CLAUDE.md`; `.claude/PROJECT-SYSTEM.md`; quattro regole sotto `.claude/rules/`, di cui una nuova; la skill `studio-didattico`; l'agente `security-auditor`; i quattro strumenti tipografici sotto `tools/` e i loro modelli; i due controlli nuovi `check-copie-modelli.py` e `check-catalogo.py`; sei pacchetti di modelli sotto `.claude/templates/`; questo file.

Il riallineamento al template è stato eseguito oggi e non rimandato. Avevo proposto di rimandarlo a dopo la chiusura di PA-011 per non mescolare due giri di lavoro, l'utente ha ripetuto l'istruzione, e la sua decisione supera la mia proposta: la separazione fra i due giri resta comunque netta, perché il backup non era ancora partito quando il riallineamento è cominciato. Il racconto è in MS-129 e la misura che lo ha preceduto in MS-127.

Motivo. La sessione si è aperta con la skill `riprendi`, e la verifica è uscita pulita: l'impronta del 2026-09-16 descriveva il presente e i due file modificati nell'albero erano quelli attesi. Il fronte è PA-011, cioè il backup di macchina, e prima di creare il lavoro ho misurato lo stato dell'agente invece di fidarmi del comando scritto nel file di ripresa.

Due cose meritano il meta-stato e non solo il registro. La prima è che il primo comando consegnato è fallito per una causa che non sta nel comando: era scritto per la postazione e si apriva con `ssh -t studio`, e l'utente lo ha incollato in un terminale già aperto sulla macchina di destinazione, dove quell'alias non esiste. È una quinta causa rispetto alle quattro che il template sta censendo in queste ore nella regola sul formato dei comandi, e riguarda la macchina invece dello stato di una shell sulla stessa macchina. Vale la pena portarla al template quando si chiude PA-016.

La seconda è che l'utente ha chiesto se stessi tracciando, e la risposta onesta era no: fino a quel momento questa sessione aveva prodotto misure e nessun file, cioè esattamente lo stato che `chat-non-e-memoria.md` esiste per impedire. Il presidio previsto dalla regola, cioè la riga che dichiara quali file sono stati scritti, era assente dalle prime due risposte, ed è così che la sua assenza si nota. Il debito è stato pagato nello stesso giro.

Lo scarto dal template è stato misurato su domanda dell'utente e non chiuso: sei commit dal 2026-09-15, fra cui una regola che qui non esiste e un paragrafo nuovo in una regola che qui si carica sempre. È PA-016, ed è deliberatamente rimandata a dopo la chiusura di PA-011 per non mescolare due giri di lavoro.

## 2026-09-16, chiusura - Allineamento al template per la ripresa di sessione

Commit di partenza: a7dea2b.

File toccati: `tools/verifica-ripresa.py` e `.claude/skills/riprendi/`, nuovi e istanziati dal template; `.claude/PROJECT-SYSTEM.md`, riportato identico a quello del template; `CLAUDE.md`, con la procedura di ripresa nella forma nuova; `_notes/RESUME-PROMPT.md`, rinominato dal minuscolo e riscritto; schede di stato riallineate ad `a7dea2b`.

Motivo. Il template ha introdotto un presidio che questo progetto non aveva: una impronta dello stato di git registrata come ultimo atto della sessione e verificata come primo atto della successiva. Serve a distinguere un file di ripresa aggiornato da uno che non lo è, che dall'esterno hanno lo stesso aspetto, e a dire che cosa una sessione caduta a metà non ha scritto. La prima corsa dello strumento, ancora senza impronta, ha comunque trovato subito uno scarto reale, cioè lo snapshot fermo a `dd3d630` mentre HEAD era già ad `a7dea2b`.

Che cosa resta divergente dal template e non è stato portato qui: la skill `gate-pacchetti`, che riguarda l'adozione dei pacchetti opzionali e non il tracciamento, e che verrà istanziata se e quando servirà.

Come si chiude senza produrre un falso positivo, scoperto usando il presidio la prima volta e scritto qui perché altrimenti si ripete l'errore a ogni chiusura. Lo strumento pretende che lo snapshot di memoria dichiari esattamente `HEAD`, senza tolleranza per il commit padre. Aggiornare lo snapshot e poi committarlo lo rimette indietro di uno, perché il commit che lo porta è successivo a quello che dichiara, e la cosa si ripete all'infinito. La sequenza che funziona è quindi: l'utente committa tutto il lavoro, poi si aggiorna lo snapshot perché dichiari il commit appena fatto, e lo si lascia non committato; l'impronta registra insieme il commit e la forma dell'albero, quindi quel singolo file modificato è parte della fotografia e non una anomalia. La sessione successiva lo trova come atteso e lo committa insieme al proprio lavoro. Verificato: con lo snapshot committato il controllo esce con codice 1 e segnala la divergenza, con lo snapshot aggiornato e lasciato sul posto esce con codice 0 e dichiara nessuna divergenza.

## 2026-09-16 - Veeam allestito, il livello di volume escluso per misura, conoscenza estratta in una pagina

File toccati: `docs/OPERATIONS-LOG.md` con MS-117, MS-118, MS-119, MS-120, MS-121 e MS-122; `docs/10-ambiente/veeam-agent-linux.md`, nuovo; `docs/10-ambiente/README.md`; `docs/PENDING-ACTIONS.md`; `tools/check-pending-actions.py`; schede di stato.

Esito. La discrepanza di PA-011 è chiusa leggendo l'altro progetto: l'esperienza esisteva, con ripristino reale collaudato, e viveva in un censimento hardware invece che nella cartella della strategia di backup. L'agente è installato. Il backup a livello di volume è però escluso per misura su questa macchina, e sono cadute due strade in sequenza: la variante senza modulo non lo sa fare su partizioni semplici perché si appoggia agli istantanei di LVM, che qui non c'è, e i due moduli del kernel esistenti non compilano contro il 7.0 perché usano funzioni e strutture rimosse.

Due errori di forma miei, registrati. Un comando con redirezione dato come primo contatto con un programma sconosciuto ha nascosto la richiesta di accettazione della licenza, facendo sembrare bloccato un comando che aspettava una risposta. E un comando che concatenava tre operazioni di `apt` ha fatto ripetere tre volte la stessa compilazione fallita, allungando l'uscita senza aggiungere informazione.

Su richiesta esplicita dell'utente la conoscenza è stata estratta in una pagina prescrittiva, `docs/10-ambiente/veeam-agent-linux.md`, scritta per essere riusabile anche in `home-lab-cybersec-networking`, dove la stessa conoscenza manca.

Resta da creare il lavoro a livello di file, eseguirlo, trasferirlo su J: e provarne il ripristino.

## 2026-09-15, quinta parte - ARTA installato, fase 8 verificata, backup fissato e rimandato a domani

File toccati: `docs/OPERATIONS-LOG.md` con MS-116; `docs/PENDING-ACTIONS.md` con PA-013 e PA-014 e con l'aggiunta a PA-011; `tools/check-pending-actions.py`; `docs/10-ambiente/installazione-pulita-26-04.md` e `docs/10-ambiente/wine-corredo-progetto-stanza.md`; schede di stato.

Esito. La sottofase 8.7 è chiusa: ARTA 1.7.1 installato nel prefix `arta64`, che si apre, con il limite della modalità dimostrativa misurato invece che rimandato. Il controllo di uscita della fase 8 è stato eseguito aprendo i cinque programmi tutti insieme, il che prova che i quattro prefix convivono, e passa in quattro criteri su cinque.

Tre decisioni dell'utente registrate. La destinazione del backup è la radice dell'SSD esterno T7, dichiaratamente provvisoria in attesa del NAS domestico tracciato in un altro progetto. L'ordine è prima finire di installare e poi il backup. E i comandi git si consegnano d'ora in poi con il proprio `cd` e nel solo blocco PowerShell, cosa scritta nella regola invece che ricordata.

Il disco J: è stato staccato dall'utente in corso di sessione e tornerà domattina, quindi il backup slitta a domani; la condizione è ora verificata dallo strumento e non dalla memoria.

## 2026-09-15, seconda parte - L'interfaccia guidata da remoto, e il blocco nuovo sull'importazione dei GLL

Commit di partenza: l'ultimo fatto a mano dopo la prima parte.

File toccati: `docs/OPERATIONS-LOG.md` con MS-111 e MS-112; `docs/10-ambiente/wine-troubleshooting.md` con una scheda nuova sull'automazione dell'interfaccia sotto Wayland; `docs/10-ambiente/wine-corredo-progetto-stanza.md` e `docs/10-ambiente/installazione-pulita-26-04.md`, corretti sul ruolo della cartella dei GLL e sul blocco corrente; schede di stato e `_notes/resume-prompt.md`.

Esito della prima metà. Le due verifiche in interfaccia che restavano sulla sottofase 8.6 sono state rese eseguibili da remoto, cosa che prima si dava per impossibile senza la presenza dell'utente davanti allo schermo. `xdotool` da solo non basta, perché la sessione è Wayland e le finestre di Wine vivono dentro XWayland: le interrogazioni rispondono tutte come previsto e l'iniezione di clic e tasti non arriva, che è un fallimento che riporta successo. La via che funziona è un server X privato con `Xvfb`, dove non esiste compositore a possedere l'input, e lì la prima azione ha funzionato al primo colpo. È MS-111, con due trappole registrate, cioè il comando che uccide la propria shell e gli acceleratori da tastiera incostanti.

Esito della seconda metà, che è un blocco e va detto come tale. L'ipotesi di MS-110 sul database è confermata: il catalogo dei modelli si alimenta per importazione e non copiando file, e la cartella su `Z:` è la sorgente e non la posizione di lettura. L'importazione però rifiuta ogni file provato, compreso un modello che l'installatore stesso del programma ha depositato nel prefix, il che esclude l'età del database e la versione del formato. Quattro cause sono state escluse per misura, cioè un modulo mancante, il servizio di database, i file e la libreria dei certificati. La traccia del caricamento delle librerie isola un solo evento pertinente, il provider di firma digitale `dssenh.dll` che rifiuta i flag richiesti, ed è una ipotesi forte ma non una prova. È MS-112.

Esito della terza parte, che è un ritiro. Il provider è stato sostituito con la libreria originale di Windows presa dalla postazione, in entrambe le architetture e con un override dato sulla riga di comando per poter annullare l'esperimento: il rifiuto di flag scompare, quindi la sostituzione ha funzionato come sostituzione, ma l'importazione fallisce identica. La crittografia è quindi esclusa per misura e l'ipotesi di MS-112 è ritirata, con il prefix riportato allo stato precedente. È MS-113, dove sono registrate anche due osservazioni non cercate, cioè che la preferenza sul riquadro della newsletter non è stabile fra un avvio e l'altro e che il programma non offre alcun registro diagnostico.

Esito della quarta parte, che è un doppio restringimento. Un modello GLL pubblicato nel gennaio 2026, scaricato dal sito di un costruttore, è rifiutato come quelli del 2016 e del 2022, quindi l'età del modello non discrimina; e le tre sole librerie native del programma non importano alcun redistributabile di Visual C++, quindi quel candidato cade a sua volta. Il lettore dei modelli risulta essere codice gestito, il che spiega perché il registro di Wine non riporti errori di caricamento. È MS-114.

Resta un solo candidato, cioè la versione di Wine, che sulla macchina è quella dei repository della distribuzione invece dei pacchetti ufficiali di WineHQ. È una decisione sull'ambiente e non una prova rapida, perché le due provenienze non si mescolano, quindi va posta all'utente prima di essere eseguita.

Una modifica di convenzione, chiesta dall'utente il 2026-09-15 e resa vincolante invece che ricordata: i comandi git per un repository diverso da quello aperto nella sessione si danno sempre con il proprio `cd` in testa al blocco. La regola `.claude/rules/git-commands-format.md` lo prescrive ora esplicitamente.

## 2026-09-15, prima parte - EASE Focus si apre: GDI+ era la causa, e i 451 MB non vanno copiati

Commit di partenza: dd3d630.

File toccati: `docs/OPERATIONS-LOG.md` con MS-110; `docs/10-ambiente/wine-corredo-progetto-stanza.md`, `docs/10-ambiente/installazione-pulita-26-04.md` e `docs/10-ambiente/wine-troubleshooting.md`, che porta una scheda nuova sul fallimento dentro `System.Drawing`; `.claude/memory/index.md`, `.claude/context/current-work.md` e `.claude/context/roadmap.md`, riallineate al commit corrente; `_notes/resume-prompt.md`.

Esito. L'ipotesi lasciata aperta da MS-109 era giusta: installato `gdiplus` nel prefix, EASE Focus 3.1.260 si apre. La catena delle dipendenze di questo programma sotto Wine è quindi misurata invece che ereditata, ed è `dotnet48` più `gdiplus`, mentre le altre tre prescritte dalla documentazione restano non installate e non assunte.

Tre accertamenti sono arrivati insieme all'avvio e nessuno era previsto in questa forma. Il primo risolve la domanda aperta in MS-107: l'installatore separato del servizio di database è superfluo, perché il programma avvia il servizio da sé otto secondi dopo la partenza. Il secondo è che quel servizio è una istanza di MongoDB, creata vuota al primo avvio e legata al solo indirizzo locale, il che rende plausibile che il catalogo dei GLL voglia una importazione invece di una cartella, e questa resta una ipotesi da decidere in interfaccia. Il terzo è che i 451 MB del database dei GLL non vanno copiati affatto, perché il prefix mappa `Z:` sulla radice del filesystem e la cartella è già visibile dov'è, con tutti e 221 i suoi file contati da dentro il prefix.

Un residuo va saputo riconoscere: l'elenco delle finestre riporta anche `Wine Debugger` e `Program Error`, che appartengono all'istanza fallita ieri e viva da oltre ventitré ore, non all'avvio di oggi.

La sottofase 8.6 non si chiude qui. Restano due verifiche che richiedono la presenza dell'utente davanti allo schermo, cioè il caricamento di un modello GLL dal percorso su `Z:` e l'osservazione di come il programma tratti il proprio database.

## 2026-09-14, ottava parte - EASE Focus installato e bloccato su GDI+, sessione chiusa

Commit di partenza: 84525ce.

File toccati: `docs/OPERATIONS-LOG.md` con MS-108 e MS-109; `_notes/resume-prompt.md`, nuovo; schede di stato.

Esito. EASE Focus 3.1.260 è installato ma non si apre, e il blocco è stato circoscritto in due passaggi invece che in uno. Con il solo Mono falliva con `ArgumentException` dentro il costruttore di `System.Drawing.Icon`; installato `dotnet48` il messaggio cambia in `ExternalException: A generic error occurred in GDI+` mentre la catena delle chiamate resta identica. Il framework era quindi necessario ma non sufficiente, e la causa non è l'implementazione .NET della grafica ma GDI+ come Wine lo fornisce.

Va registrato che questo rovescia la diagnosi che avevo scritto in MS-108, dove avevo attribuito il fallimento all'incompletezza della libreria grafica di Mono: era plausibile e l'esperimento l'ha smentita. Il valore dell'aver installato una dipendenza alla volta si vede qui: installando in blocco tutte e quattro quelle prescritte dalla documentazione si sarebbe ottenuto lo stesso fallimento senza sapere quale componente avesse cambiato qualcosa.

Il candidato successivo è dichiarato come ipotesi e non come piano: sostituire GDI+ di Wine con la libreria originale di Windows tramite `winetricks -q gdiplus`. Se il programma si apre la causa era quella, se fallisce ancora la diagnosi riprende dalla catena delle chiamate.

La sessione si chiude qui e la ripresa è preparata in `_notes/resume-prompt.md`, con lo stato raggiunto, il blocco in tre righe, i comandi pronti e il prompt da incollare alla riapertura.

## 2026-09-14, settima parte - Sottofase 8.5 chiusa: VituixCAD funziona

Commit di partenza: 407ac4f.

File toccati: `docs/OPERATIONS-LOG.md` con MS-106; `docs/10-ambiente/installazione-pulita-26-04.md` alla sottofase 8.5, propagato al gemello; schede di stato.

Esito. Il primo avvio riuscito ha prodotto centinaia di righe che nominano `mscorsvw.exe`, cioè il servizio con cui .NET precompila le proprie librerie dopo una installazione nuova. Non è un guasto e si esaurisce da sé: la verifica non è stata guardare il terminale, che non distingue un lavoro finito da uno bloccato, ma contare i processi. Nessun `mscorsvw` attivo, carico tornato a riposo, e il processo di VituixCAD vivo da oltre quindici minuti.

La sottofase 8.5 è quindi chiusa in tutti i suoi pezzi: prefix a 64 bit creato, programma installato, architettura reale accertata come AnyCPU con uno strumento scritto per l'occasione, runtime risolto con `dotnet48` dopo avere misurato che Mono non bastava, e primo avvio verificato. Il prossimo passo è la sottofase 8.6, cioè EASE Focus 3.1.260 con il servizio di database AFMG, seguita dalla copia dei 451 MB del database dei GLL, che è lavoro da riga di comando.

## 2026-09-14, sesta parte - Il prefix di VituixCAD, e la voce 2 del racconto didattico

Commit di partenza: f9a829c.

File toccati: `docs/OPERATIONS-LOG.md` con MS-100; `.claude/context/studio-didattico-master.md` con la voce 2; `.claude/context/refactor-02-il-prefix-non-e-una-cartella.md`, nuovo. Sulla macchina: creato il prefix `~/wineprefixes/vituixcad64`.

Motivo: l'utente ha chiesto che ogni dettaglio di ciò che sta accadendo venga spiegato, e questo è precisamente il bisogno che il livello didattico copre, distinto dal registro che dice che cosa è stato fatto e come è stato verificato.

Esito tecnico. Il prefix esiste, dichiara `#arch=win64` come deve, e non ha alcun runtime .NET: Mono assente, `Microsoft.NET` assente, e la cartella `gecko` che sembra un'installazione contiene soltanto un segnaposto. Né Mono né Gecko sono nel sistema, e `wine-mono` non è nei repository di Ubuntu, quindi Wine dovrà scaricarli; il sito risponde. La decisione fra Mono e `dotnet48` si prende al primo avvio del programma, che è il momento in cui Wine chiede da sé. È MS-100.

La voce 2 del racconto didattico generalizza i tre inciampi di questa sottofase in una sola diagnosi: la documentazione trattava il prefix come un percorso mentre è uno stato, ed è la stessa forma della voce 1, dove quattro architetture erano trattate come una. Il deep-dive entra nell'anatomia del prefix con gli output reali, spiega i cinque assi che lo caratterizzano compreso il wow64 sperimentale emerso ora, spiega che cosa siano Mono e Gecko e perché non stiano dentro Wine, e chiude con le quattro letture da fare prima di installare qualunque programma in un prefix nuovo.

Un guadagno di metodo registrato nella stessa voce: una inferenza marcata come tale in MS-085 è stata confermata cinque giorni dopo da una osservazione indipendente, e non lo sarebbe stata se fosse stata scritta come certezza.

## 2026-09-14, quinta parte - Il primo comando della 8.5 fallisce, e la fase 7 aveva lo stesso difetto

Commit di partenza: e45752e.

File toccati: `docs/OPERATIONS-LOG.md` con MS-099; `docs/10-ambiente/installazione-pulita-26-04.md` alla fase 7, propagato al gemello; `docs/PENDING-ACTIONS.md` con PA-003 precisata. Sulla macchina: creata `~/wineprefixes`.

Esito. Wine crea la cartella del prefix ma non quelle che la contengono, e `~/wineprefixes` non esisteva perché l'unico prefix della macchina, `~/.wine`, sta direttamente nella cartella dell'utente. Il difetto non era del mio comando soltanto: la fase 7 della procedura crea quattro prefix e non crea mai la cartella che li contiene, quindi sarebbe fallita al primo comando con un messaggio che parla di accesso e non di creazione. La fase 7 porta ora quel passo con la ragione accanto.

Corretta anche una affermazione di MS-098, scritta ieri su una lettura parziale: il template non è su `main` ma sul ramo `pacchetto-allineamento`, allineato con il remoto. Ne segue che la propagazione di PA-003 non si chiude con un commit ma con una unione, perché anche una volta committati quei file resterebbero su un ramo di lavoro.

## 2026-09-14, quarta parte - Il registro non diceva a che cosa servisse, e il pattern entra nel template

Commit di partenza: fe64db6, con MS-095 e MS-096 non ancora committati.

File toccati: `docs/OPERATIONS-LOG.md` con MS-097 e MS-098 e con la sezione `Convenzione` estesa; nuova pagina `docs/90-riferimenti/tracciabilita-microstep.md`; `docs/README.md` e `docs/90-riferimenti/README.md` per i rimandi; `docs/PENDING-ACTIONS.md` con PA-003 aggiornata due volte; `CLAUDE.md`. Nel template, cioè in un altro repository: il pacchetto nuovo `.claude/templates/operations-log/` con tre file e la riga nel catalogo `PACKAGES.md`.

Motivo: l'utente ha rilevato che il registro racconta il come e la verifica ma non dice a che cosa serva ciascun intervento rispetto all'obiettivo, cioè due monitor da costruire, e ha chiesto che la lacuna fosse sanata anche per il passato. Ha poi chiesto che il registro esista nel template, perché ogni microstep di ogni progetto sia tracciato.

*La correzione retroattiva non poteva essere retroattiva nella forma ovvia.* Aggiungere un paragrafo a novantasei voci è vietato dalla convenzione del registro e sarebbe stato sbagliato comunque, perché produrrebbe un documento che sembra essere sempre stato completo. La forma adottata è additiva in due pezzi: il legame per il passato in una pagina che mappa sette blocchi di microstep sulla fase che servono, e per il futuro un obbligo scritto nella convenzione. Il settimo blocco dichiara di non servire alcuna fase, ed è la voce che rende onesta tutta la mappa.

*Una domanda dell'utente, con risposta verificata.* La convenzione di non riscrivere non fa perdere pezzi: lascia l'affermazione sbagliata leggibile accanto a quella che la corregge, ed è in uso, con sette ritiri espliciti nel registro. Non deriva dal template, verificato e non ricordato: `PROJECT-SYSTEM.md` non contiene alcuna occorrenza di `OPERATIONS-LOG` né di `microstep`, mentre prescrive `append-only` per il work log e per il registro delle decisioni. Il difetto reale della convenzione era un altro, cioè che una voce superata non sa di esserlo, e la correzione compatibile con la regola è un indice a parte, ora presente con sette relazioni ricavate dalle dichiarazioni delle voci stesse.

*Il pacchetto nel template, e la scoperta che lo accompagna.* Il registro è ora un pacchetto opzionale con README, modello e gate esplicito, compreso il gate negativo che ne evita l'abuso. Verificando `git status` in quel repository sono però emersi ventuno file modificati e quattro non tracciati, tutti non committati, e fra essi esattamente i file da cui MS-091 ha preso le versioni nuove. Ne discende una correzione di lettura: il template è avanti sul disco e non nella storia di git, quindi chi lo clonasse oggi non riceverebbe nulla di quel lavoro. È MS-098, e la propagazione resta non compiuta finché quel commit non esiste.

## 2026-09-14, terza parte - La sottofase 8.4 non si esegue, e la cartella di lavoro prende posto

Commit di partenza: fe64db6.

File toccati: `docs/OPERATIONS-LOG.md` con MS-095 e MS-096; `docs/10-ambiente/installazione-pulita-26-04.md` alla sottofase 8.4, riscritta e propagata al gemello; `docs/60-simulazione-finale-akabak.md` per la radice di lavoro; schede di stato. Sulla macchina: creata `~/Documents/AkabakProjects` e corretta la chiave `InitialDir` nel prefix.

*Sulla 8.4, il punto non è che estrarre fosse inutile ma che fosse dannoso.* Gli esempi erano già nel prefix, nella cartella che la chiave `ExamplePath` dichiara, cioè quella che il menu `File/Open Example` apre. Estrarne una seconda copia in `~/AkabakProjects/esempi` avrebbe prodotto 159 MB in un percorso che il programma non conosce, con la documentazione che nomina l'una e il programma che apre l'altra: due copie della stessa cosa che divergono senza che nessuno se ne accorga. La sottofase è stata riscritta perché chi la rilegge verifichi prima e non esegua per abitudine.

La verifica è passata per tre gradini, e i primi due non bastavano. Il conteggio grezzo dava 632 contro 681 e sembrava uno scarto, mentre era solo `unzip -l` che conta anche le cartelle. Il confronto dei nomi dava zero differenze, ma nomi uguali non dicono nulla sui contenuti, perché una estrazione interrotta lascia proprio nomi giusti e file troncati. Il gradino che decide è il confronto per impronta, e i CRC-32 stanno già dentro l'archivio: 632 contro 632, zero divergenze.

*Sulla cartella di lavoro, il tempismo era la ragione.* La finestra di apertura di AKABAK partiva da dentro `Program Files`, e con ADR-020 che manda i dati spettrali nella cartella del progetto, quella radice decide anche dove si accumulano tutti i risultati delle molte iterazioni della fase 5. Correggerla prima che esista un progetto costa una riga; dopo costerebbe spostare file. La radice scelta è `~/Documents/AkabakProjects` e non `~/AkabakProjects` come la procedura diceva, per tre ragioni: dentro il prefix è un percorso su `C:` invece che su `Z:`, il che è ciò che un programma Windows si aspetta; VACS puntava già alla cartella dei documenti e i due programmi lavorano in sequenza; e sta comunque in `/home`, quindi sotto il presidio della separazione delle partizioni.

*Un mio errore di metodo, con esito innocuo per fortuna.* Avevo messo una guardia per non scrivere il file di configurazione con il programma aperto, e ha fallito due volte nello stesso comando: ha dato un falso positivo, perché `pgrep -f` riconosce anche la propria riga di comando, e soprattutto non ha impedito nulla, perché l'avevo concatenata con `&&` a un `echo` che riesce sempre. Il programma davvero non era in esecuzione, accertato dopo, quindi il danno non c'è stato. La regola che ne discende è che una guardia che stampa un avviso senza interrompere non è una guardia ma un commento, e che un controllo capace di riconoscere se stesso non è un controllo: entrambi danno l'impressione di un presidio dove non c'è, ed è la terza volta che questo progetto paga quella conseguenza in forme diverse.

## 2026-09-14, seconda parte - La sottofase 8.3 è chiusa, e il confronto ha dato la chiave

Commit di partenza: b02a547, con MS-093 non ancora committato.

File toccati: `docs/OPERATIONS-LOG.md` con MS-094; `.claude/memory/decisions.md`, dove ADR-020 passa ad accettata; `docs/10-ambiente/installazione-pulita-26-04.md` alla sottofase 8.3, propagato al gemello; `docs/90-riferimenti/timeline-akabak-vacs.md`; schede di stato.

Esito. L'impostazione esiste ed è fatta. Il controllo si chiama `Spectrum way of output` e sta nella scheda `VACS` della finestra delle preferenze, quindi ha ragione il capitolo dell'appendice della guida e non la pagina che la descriveva come puramente informativa.

Il guadagno vero non è l'impostazione ma il metodo con cui è stata verificata. Avendo registrato prima le impronte dei tre file di configurazione del prefix, il confronto dopo l'azione ha detto che è cambiato il solo `AppData\Local\RDTeam\Akabak.ini` e che vi sono comparse tre chiavi, cioè `SpectrumOutputType=3`, `SpectrumOutputAsText=0` e `SpectrumOutputFolder=` vuota. Da adesso quella preferenza si può scrivere su un prefix nuovo invece di ripetere un giro di menu, e il file della licenza resta dimostrabilmente intatto.

Due scoperte collaterali. La conferma delle preferenze materializza su disco l'intero insieme delle impostazioni e non la sola voce toccata, da cinque a ventotto chiavi, quindi la configurazione del programma è diventata un file di testo confrontabile e alcuni valori utili alla fase 5 sono già leggibili, fra cui il numero di thread del solutore, il metodo predefinito di compensazione della non unicità e l'intervallo di frequenza predefinito. E il testo informativo dentro la pagina delle preferenze sottostima le vie di trasferimento esattamente come facevano l'email dell'autore e una pagina della guida, nominando solo COM e appunti mentre il controllo sotto di esso offre i file: la ragione si legge nel testo stesso, che nomina `ABEC` e non AKABAK, cioè la finestra è condivisa con il programma gemello ed è rimasta indietro rispetto ai propri controlli.

Confermata anche la forma remota di MS-093 sul programma vero e non solo sulla prova con `notepad`: l'avvio da SSH con `DISPLAY` e `XAUTHORITY` non produce alcuna riga di errore sul driver e la chiusura è regolare.

## 2026-09-14 - AKABAK non parte da SSH, e una mia spiegazione cade alla prima prova

Commit di partenza: b02a547.

File toccati: `docs/OPERATIONS-LOG.md` con MS-093; `docs/10-ambiente/wine-troubleshooting.md` con la scheda sull'errore `no driver could be loaded`; `docs/10-ambiente/installazione-pulita-26-04.md` con il rimando nella sottofase 8.3, entrambi propagati al gemello; schede di stato riallineate.

Motivo: il lavoro doveva essere la verifica in interfaccia della sottofase 8.3, cioè impostare il modo di trasferimento verso VACS. Il programma non si è aperto, quindi il microstep si è spostato sulla causa.

Esito. Non era il prefix e non era la licenza: in una sessione SSH `DISPLAY` e `WAYLAND_DISPLAY` sono vuote, quindi Wine non ha un indirizzo a cui mandare la finestra. Prima di arrivarci ho escluso tre cause con altrettante misure, cioè driver assenti per i 32 bit, sessione grafica non attiva e driver sbagliato dichiarato nel registro del prefix: nessuna delle tre. La forma che funziona vuole `DISPLAY=:0` insieme a `XAUTHORITY` ricavato dal file della sessione, e le prove sono state fatte con `notepad` sotto `timeout` invece che con AKABAK, contando le occorrenze dell'errore: due con la sola variabile Wayland, due con la sola `DISPLAY`, zero con le due insieme.

*Un mio errore, di una forma nuova per questo progetto.* Il 2026-09-09 avevo scritto che una sessione SSH dispone comunque di un display perché la libreria di Wayland ricade sul socket dentro `XDG_RUNTIME_DIR`. La prova di oggi la smentisce: la variabile è impostata, il socket esiste, e l'avvio fallisce lo stesso; anche forzando `WAYLAND_DISPLAY` il fallimento resta. Il dato osservato allora, cioè che la finestra comparve, resta vero, ed è quasi certo che fosse stata lanciata dalla sessione grafica della macchina. Ciò che era sbagliato è il meccanismo che le avevo attribuito. Non avevo misurato nulla di falso: avevo costruito una spiegazione plausibile e l'avevo scritta come accertata. La regola che ne discende, ed è diversa dalle precedenti di questo registro, è che una spiegazione che si adatta a una osservazione non è verificata finché non ne predice una seconda, e che il momento di metterla alla prova è quello in cui la si scrive.

La sottofase 8.3 resta da eseguire ed è ora sbloccata.

## 2026-09-12 - La pipeline COM letta dalla fonte, il riallineamento al template e l'inventario di `_notes`

Commit di partenza: 633c513.

File toccati: `docs/OPERATIONS-LOG.md` con MS-090, MS-091 e MS-092; `.claude/memory/decisions.md` con ADR-020; `docs/90-riferimenti/timeline-akabak-vacs.md` nella sezione concettuale su COM; `docs/10-ambiente/installazione-pulita-26-04.md` alla sottofase 8.3, poi propagato al gemello; `.claude/context/roadmap.md` con la direzione del report LaTeX; `.claude/PROJECT-SYSTEM.md`, `CLAUDE.md`, `docs/PENDING-ACTIONS.md` con PA-003 riscritta; ventinove file allineati dal template fra `.claude/` e `tools/`; `_notes` ripulita di due voci.

Motivo: la sessione è ripartita dal microstep successivo, cioè la sottofase 8.3 sul limite delle pipeline COM, e durante il lavoro l'utente ha aggiunto due richieste, cioè verificare l'allineamento al template e ripulire `_notes` trasformando in documentazione ciò che merita di restare.

*Sulla pipeline COM, il guadagno è venuto dall'avere letto la fonte invece dei menu.* Il file di aiuto compilato di AKABAK vive dentro il prefix e un file di aiuto di Windows è un archivio, quindi `7z x` lo apre su Linux senza aprire il programma: 1092 file estratti, due letti. Il capitolo autorevole dice più dell'email dell'autore su cui il progetto poggiava dal 2025, e la differenza non è di dettaglio: le alternative a COM sono due e non una, cioè gli appunti e i file su disco. Il progetto sceglie i file, ed è ADR-020, per riproducibilità, ispezionabilità dello stato intermedio, difesa dall'errore silenzioso di portare in VACS un risultato vecchio, e traccia della convergenza attraverso le molte iterazioni della fase 5. Ne è uscito anche il nome esatto dei menu, quindi la verifica in interfaccia è ora mirata invece che una ricerca a vista, ed è MS-090.

*Sul template, il risultato rovescia quanto il progetto affermava.* `CLAUDE.md` dichiarava che qui vivessero le versioni più recenti degli strumenti tipografici: era vero al 2026-09-04 e falso dal 2026-09-09, perché il template ha lavorato nel frattempo. Il progetto era indietro su quattro strumenti su cinque e portava ventidue apostrofi orfani nei docstring, prodotti dal difetto che il template ha poi corretto con una funzione dedicata. Adottate le versioni del template le ventidue occorrenze sono zero. Dodici file nuovi e diciassette aggiornati, `PROJECT-SYSTEM.md` tornato identico, e soprattutto la regola `chat-non-e-memoria.md` finalmente istanziata qui: era nata da una direttiva data in questo progetto il 2026-09-09, era stata scritta nel template, e il progetto che l'aveva generata era l'unico a non averla. È MS-091.

La lezione di metodo vale oltre il caso, e l'ho scritta nel microstep. Una divergenza dichiarata in un documento descrive un rapporto fra due cose, quindi resta vera soltanto finché entrambe stanno ferme, e invecchia peggio di qualunque altra affermazione perché nessuno la rilegge. La forma difendibile è dichiarare accanto ad essa la data del confronto.

*Su `_notes`, ho rimosso soltanto ciò la cui perdita è dimostrabilmente nulla.* La cartella non è versionata, quindi una cancellazione non è recuperabile da git e il criterio non può essere che una cosa sembri obsoleta. Rimossi il `.docx` della scheda, che è l'uscita predefinita di uno strumento versionato e la cui rigenerazione ho provato prima di cancellare, e la cartella `tmp`, vuota. Restano in decisione dell'utente il documento sorgente, i due elenchi di backup da trentanove megabyte e la scheda composta a mano prima dello strumento: nessuno dei tre è riproducibile. Sui due elenchi ho accertato tre fatti che li riguardano, cioè che non contengono impronte ma solo dimensioni, che descrivono il backup generale della postazione e non questo progetto, e che nessun documento tracciato li cita. È MS-092.

## 2026-09-10 - Ripresa dopo il riavvio, licenza verificata, e il censimento del comando sbagliato

Commit di partenza: b514c33, con il lavoro non committato del 2026-09-09 ancora sul disco; quel lavoro è stato committato durante la sessione come `d8ebf45`, che è quindi il commit di riferimento di questa voce.

File toccati: `docs/OPERATIONS-LOG.md` con MS-085, MS-086, MS-087 e MS-088; `docs/10-ambiente/` in sette pagine per il censimento dei comandi di Wine, più `setup-macchina-2026-09.md` con il delta del 10 settembre e l'inventario dei dispositivi; `docs/PENDING-ACTIONS.md` con la discrepanza su Veeam in PA-011; `.claude/context/roadmap.md` con le priorità riscritte, due ipotesi risolte e la sezione delle direzioni future; `.claude/context/current-work.md` e `.claude/memory/index.md` riallineati a `b514c33`; `_notes/licenze-akabak-riservato.md` con lo stato verificato e il comando corretto.

Motivo: la postazione si è riavviata da sé la notte fra il 9 e il 10 settembre per un aggiornamento pianificato di Windows, quindi la sessione precedente si è chiusa senza commit e senza riallineare le schede di stato. La richiesta era recuperare il contesto e riprendere un microstep alla volta.

*Che cosa ha insegnato la ripresa, e riguarda il sistema di memoria e non il progetto.* Lo snapshot `index.md` dichiarava `d9912b1` mentre HEAD era `b514c33`, quindi non copriva quattro commit, e la scheda del lavoro corrente indicava come passo successivo il collegamento della Focusrite Scarlett 2i2, che è una prescrizione ritirata in MS-079 il giorno prima. Una sessione che avesse creduto alle schede invece che a `git log` avrebbe rifatto lavoro fatto e cercato un'interfaccia che non appartiene al progetto. La regola operativa aggiunta allo snapshot è che a inizio sessione lo si confronta con `git log --oneline -8` prima di crederlo, e la ragione strutturale è che lo snapshot si aggiorna a mano mentre `git log` si aggiorna da sé.

Esito tecnico in sintesi. La licenza di AKABAK è viva nel prefix sopravvissuto e la sottofase 8.2 si chiude senza reinserire nulla, verificata per due vie indipendenti in MS-085: il file di configurazione a livello di macchina, dove l'attivazione stava e non nel registro come avevo assunto, e la finestra `Release code` del menu di aiuto, che dichiara `Release Code valid` con il Machine Identifier invariato. La fase 8 comincia quindi dalla sottofase 8.3, ed è lavoro eseguibile subito senza acquisti.

Il risultato più utile della giornata non era però cercato. Applicando la lezione di MS-085, cioè che una prescrizione sbagliata non vive dove la si è incontrata, il censimento con `grep` di tutte le invocazioni di Wine su prefix a 32 bit ha trovato ventitré comandi sbagliati in sette pagine, ed è MS-087. Nove di essi erano `winecfg`, che è peggio di `wine` perché sta nel passo che crea il prefix: `/usr/bin/winecfg` è uno script di cinque righe che esegue incondizionatamente il wrapper a 64 bit, quindi il primo comando della fase 7 non poteva riuscire. Quattro erano `winetricks`, che non si corregge nello stesso modo perché non è un wrapper ma un programma autonomo il cui binario di Wine si sceglie con la variabile `WINE`. ADR-019 aveva enunciato il principio in forma generale il giorno prima; ciò che non era stato fatto è scendere dal principio ai comandi che lo contraddicono.

*Un errore mio, corretto prima del commit e documentato in MS-088.* Inserendo le voci nuove con script ho reso misti nelle fini riga quattro file che erano `CRLF` puri, cinquantasei righe nel registro e altre quarantacinque fra roadmap, lavoro corrente e azioni differite. Le cause sono due e vanno separate: la normalizzazione del testo inserito senza riconversione alla fine riga del file di destinazione, e un controllo iniziale improvvisato con `grep -q $'\r'` che ha risposto `LF` per tutti i file, compresi quelli che non lo erano, perché la sequenza non è stata interpretata come carattere e l'assenza di corrispondenza è stata letta come assenza del carattere. La regola che ne discende generalizza due voci precedenti: un esito negativo non è una prova finché non si è verificato che quel controllo sappia dare un esito positivo. La fine riga originale è stata poi letta da `git show HEAD:<file>` e non dedotta dalla prevalenza interna, e i quattro file sono normalizzati.

Tre elementi nuovi dichiarati dall'utente sono registrati in MS-086, con la separazione fra la parte verificata e quella riferita. Il Nektar Impact GX49 esiste ma non è collegato adesso, e il collaudo che l'utente ricorda appartiene al sistema precedente; lo strato MIDI del sistema è invece presente e attivo. L'esperienza precedente con Veeam su Linux non coincide con l'accertamento del giorno prima, e la discrepanza è dichiarata in PA-011 invece di essere risolta a favore di una delle due versioni. La replica del setup sul secondo portatile è collocata in roadmap come richiesto, con i due punti che decidono se valga la pena, cioè i 4 GB di RAM e il fatto che la licenza di Akabak sia legata a una macchina sola.

L'ultimo accertamento aperto è stato chiuso nel corso della stessa sessione ed è MS-089. L'edizione è `Standard Edition`, quindi la documentazione aveva ragione e la conferma è la prima post-reinstallazione; la discrepanza che avevo dichiarato il giorno prima non esisteva, perché il `32 Professional` della barra del titolo non dichiara l'edizione. L'errore di lettura è isolato come regola: una discrepanza esiste quando due fonti affermano cose diverse dello stesso attributo, non quando una fonte usa una parola che in un altro contesto ne nomina uno. La finestra ha portato anche la misura del tetto di memoria del processo a 32 bit, `2047 MBytes`, che è il numero su cui poggia la valutazione della replica del setup sul portatile in roadmap: da oggi è misurato e non desunto.

## 2026-09-09, sera - AKABAK riparte nel prefix sopravvissuto, e nasce il livello didattico

Commit di partenza: ce42d7a.

File toccati: `.claude/context/studio-didattico-master.md` e `.claude/context/refactor-01-wine-32-bit-su-ubuntu.md` nuovi, `.claude/memory/decisions.md` con ADR-019, `docs/OPERATIONS-LOG.md` con MS-084, `docs/10-ambiente/installazione-pulita-26-04.md` alla fase 7, `docs/10-ambiente/scheda-reinstallazione.md`, `docs/10-ambiente/setup-macchina-2026-09.md` con il ritiro dichiarato, `CLAUDE.md` con l'adozione del livello didattico. Sulla macchina: `wine32:i386` installato, scrivania separata dal magazzino, due lanciatori corretti.

Motivo: l'avvio di AKABAK nel prefix sopravvissuto alla reinstallazione è fallito malgrado ogni passo della procedura risultasse eseguito, e l'utente ha chiesto una documentazione tecnico-didattica dedicata su che cosa fosse successo. La richiesta esplicita è l'adozione del livello previsto dalla skill `studio-didattico`, che questo progetto non aveva.

Esito in sintesi. Il programma parte: `3.2.4 b126 - 32 Professional` nel prefix `~/.wine` migrato da Wine 9 a Wine 10, con copia di sicurezza da 831 MB fatta prima. La fase 8 si riduce quindi a una verifica invece di una reinstallazione con riattivazione, ed è la prima volta che la separazione fra radice e `/home` produce un risparmio misurabile e non solo un presidio.

La causa del fallimento era la quarta di quattro architetture che la documentazione trattava come una: il comando. Su Ubuntu `wine` è un collegamento a uno script che sceglie il caricatore a 64 bit ogni volta che `wine64` esiste, senza guardare il prefix, e ADR-016 impone di averlo. Su un prefix `win32` fallisce sempre. La forma corretta è `wine32` con `WINEPREFIX` dichiarato, ed è ADR-019.

Il difetto peggiore non era però nei comandi ma nel presidio: il controllo di uscita della fase 7 era `wine --version`, che risponde bene senza caricare alcun prefix, quindi passava su un ambiente incapace di eseguire il programma. È il terzo caso della stessa forma in questo progetto, dopo il nome del kernel nella fase 6 e la lettura dei file dei limiti realtime invece di `ulimit`. Sostituito con lo stato di installazione di `wine32:i386`.

Due miei errori ritirati, entrambi con la causa isolata come regola. Avevo dichiarato che una sessione SSH non ha display, mentre la finestra è comparsa lanciando da remoto: l'assenza di una variabile non dimostra l'assenza della risorsa, perché la libreria di Wayland ricade sul socket predefinito dentro `XDG_RUNTIME_DIR`, che la sessione remota eredita. E avevo dichiarato rotti due lanciatori perché invocavano `wine-stable`, nome che credevo inesistente: quel file esiste ed è lo stesso script di `wine`, quindi la correzione era una non-operazione che lasciava intatto il difetto vero. La causa è aver trasferito al binario una conclusione verificata sul pacchetto.

Il perché di tutto questo, con gli script letti riga per riga, gli output reali e la classificazione delle righe `err` e `fixme`, sta nel deep-dive `refactor-01-wine-32-bit-su-ubuntu.md`; questa voce lo indicizza e non lo duplica.

Resta una discrepanza aperta e dichiarata: la finestra riporta l'edizione `32 Professional` mentre la documentazione afferma che l'edizione ottenuta sia Standard. Va accertata leggendo lo stato del release code dal menu di aiuto, non assunta.

## 2026-09-09 - Installazione eseguita, verificata da remoto e documentata

Commit di partenza: d9912b1.

File toccati: `docs/10-ambiente/setup-macchina-2026-09.md` nuovo, `docs/OPERATIONS-LOG.md` con MS-076 e MS-077, `docs/PENDING-ACTIONS.md` con PA-010 e PA-011, `tools/check-pending-actions.py` esteso alle due voci nuove, `docs/10-ambiente/installazione-pulita-26-04.md` alla fase 6, `docs/10-ambiente/scheda-reinstallazione.md` su quattro punti, `tools/make-scheda-docx.py` allineato, `docs/10-ambiente/README.md` con l'indice e una affermazione obsoleta corretta, `.claude/memory/index.md` e `.claude/context/current-work.md`.

Motivo: l'utente ha eseguito l'installazione l'8 settembre sera, l'ha trovata apparentemente bloccata per sedici ore e ha riavviato a forza. La sessione del 9 è servita a stabilire se il riavvio avesse rotto qualcosa, a ripristinare l'accesso remoto e a documentare per intero la cronologia e il razionale del setup, che l'utente ha chiesto esplicitamente di non lasciare in conversazione.

Esito in sintesi, sei cose.

L'installazione è riuscita e `/home` è intatto, provato dal contenuto reale del disco invece che dal riepilogo dell'installatore. Il sistema è `Ubuntu 26.04.1 LTS` con kernel `7.0.0-31-generic`, l'utente ha ereditato l'identificativo numerico `1000`, e `~/electroacoustics` conta esattamente i 281 file per 728 MB registrati al trasferimento.

Il blocco di sedici ore non era un blocco dell'installazione: i log dicono stato `DONE` alle 17:50:40, con `curtin: Installation finished.` e il boot loader installato. Ciò che restava appeso era la fase di chiusura. La regola che ne discende è che la schermata di avanzamento non è l'autorità sullo stato dell'installazione, e il registro consultabile dall'icona a forma di terminale lo è. La causa prossima resta non nominata per assenza di evidenza, e l'assenza è dichiarata: la copia del log nel sistema installato termina nell'istante in cui copia se stessa.

L'accesso remoto è ripristinato e ora si usa come `ssh studio`. Ha funzionato perché `authorized_keys` vive in `/home`, che è la stessa separazione su cui poggia tutta la strategia di reinstallazione.

Tre difetti reali dell'installazione sono stati corretti, con i comandi preparati e la ragione di ciascun presidio a verbale: gruppi `audio` e `pipewire` mancanti con i limiti realtime scritti ma non in vigore, swap su un file da 4 GB invece della partizione da 14,9 GiB, e sospensione automatica di nuovo attiva.

Due prescrizioni della documentazione sono state ritirate perché smentite dall'uso reale. La voce `Check disc for defects` non esiste su questa immagine e il controllo del supporto è automatico, quindi MS-069 aveva sostituito una prescrizione sbagliata con un'altra. E i parametri di avvio a bassa latenza arrivano da un drop-in di Ubuntu Studio e non da `/etc/default/grub`, quindi aggiungerli a mano li duplicherebbe.

La cronologia e il razionale del setup vivono ora in una pagina propria, `docs/10-ambiente/setup-macchina-2026-09.md`, scritta nello stile della sezione 8 del template, cioè senza grassetto nella prosa e con gli acronimi in note a piè di pagina. Serve a una domanda a cui nessuno degli altri documenti rispondeva: perché la configurazione è quella che è.

Due errori miei, entrambi visti subito e nessuno arrivato su disco. Un pattern di sostituzione scritto con fini riga `LF` su un file `CRLF`, che non ha combaciato e che, se avesse combaciato sui primi due casi, avrebbe inserito righe miste, cioè esattamente il difetto per cui esiste `check-eol.py`. E un grassetto in prosa introdotto nel README del blocco pochi minuti dopo aver dichiarato che il template lo vieta.

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

Passo 3 chiuso, ed è PA-009. SMART dell'SSD esterno letto con CrystalDiskInfo elevato e l'opzione `/CopyExit`, che scrive un rapporto su file invece di richiedere uno screenshot. Il Samsung T7 è *sano*: usura zero, riserva al 100 per cento, zero errori di integrità, zero voci nel registro errori. Delle due cause possibili cade il difetto del supporto e resta la rimozione senza espulsione, con 122 spegnimenti non protetti su 742 cicli, su cui va applicato il correttivo che su USB quel contatore si incrementa anche quando l'espulsione è regolare. Le cinque cartelle `FOUND` restano la prova che conta. Il disco non va sostituito. È MS-058.

Registrato l'ostacolo, valido oltre il caso: la lettura SMART richiede privilegi anche su Windows, dove `Get-StorageReliabilityCounter` risponde `PermissionDenied` senza sessione elevata, per la stessa ragione per cui su Linux serve `sudo` su `/dev/nvme0`.

Passo 4 per due terzi. La fonte ufficiale ha corretto la procedura: nella cartella del rilascio convivono la 26.04 e la *26.04.1*, e la seconda è quella da prendere. La procedura nominava la prima in due punti, uno dei quali dentro il comando `dd`. Immagine scaricata, 7.127.195.648 byte, e verificata due volte: firma del file delle somme buona con la chiave `Ubuntu CD Image Automatic Signing Key (2012)`, impronta dell'immagine `OK`. L'ordine delle due verifiche non è indifferente e la fase 2.2 ora ne chiede due invece di una, perché una somma confrontata con un file preso dallo stesso posto dell'immagine non protegge da chi controlli quel posto. Sono MS-059 e MS-060.

Rufus 4.15 portabile scaricato e verificato per firma Authenticode, `Status: Valid`, firmatario `Akeo Consulting`: per un eseguibile Windows è la verifica più forte disponibile, e le note del rilascio non pubblicano somme di controllo. Riscritta la sottofase 2.3 con il vincolo dei 16 GB motivato numericamente, la ragione della modalità DD contro il limite dei 4 GB di FAT32, e l'avvertenza sul rifiutare la formattazione dello spazio residuo che Windows propone a scrittura finita. È MS-061.

Allineate due dichiarazioni di stato superate nella procedura, che dichiaravano non eseguite fasi compiute e chiedevano una riconferma già data.

Passo 2 compiuto: l'utente ha cancellato la copia del corredo sul Desktop, 650 file per 2,3 GB, dopo la riverifica delle impronte. PA-007 chiusa. Immagine e Rufus spostati sul Desktop per scelta dell'utente: essendo uno spostamento fra volumi, cioè una copia più cancellazione, entrambe le verifiche sono state rifatte alla nuova posizione e passano. Percorso aggiornato in quattro documenti. È MS-063.

Trovato nello stesso microstep un difetto di ambiente che aveva fatto fallire due modifiche in modo incomprensibile: un ancoraggio di testo multi-riga scritto con `LF` non trova nulla in un file `CRLF`, e l'albero contiene legittimamente entrambi i formati perché la convenzione prescrive di conservare la fine riga di ciascun file. Ipotesi sbagliata scartata per prima, cioè la codifica: il sorgente è decodificato come UTF-8 comunque, e ciò che sembrava corruzione era la stampa illeggibile su una console `cp1252`.

Da lì un difetto silenzioso più grande, che stavo per committare: i blocchi inseriti in questa sessione erano scritti con `LF` in due file `CRLF`, producendo fini riga miste che nessun controllo del progetto segnalava e che git avrebbe registrato, dato che `core.autocrlf` è `false`. Normalizzati, e aggiunto `tools/check-eol.py` alla sequenza di verifica. Al primo lancio ha trovato un file misto già nella storia del repository, `settings.json`, e sul gemello *otto* file, sette dei quali con esattamente quattro righe anomale: la misura fissa attraverso file di dimensione diversa ha indicato il generatore invece del contenuto, cioè `sync-ambiente.py`, che scriveva l'intestazione di provenienza sempre con `LF`. Corretto lo strumento e ripropagato.

## 2026-09-07, sesta parte - Licenza confermata in interfaccia, fase 0 chiusa, PA-007 detta chiara

Commit di partenza: 0df04bb.

Machine Identifier verificato sulle immagini fornite dall'utente: coincide con il valore conservato sotto `_notes/`, coincide anche il release code, e il programma dichiara `Release Code valid`. Chiude la seconda delle tre voci di PA-005 e con essa la fase 0 nella sostanza, dato che la terza voce, l'esito di `sudo apt update`, è resa irrilevante da ADR-013. È la prova sperimentale che una licenza machine-based sotto Wine resta valida a un anno di distanza, quindi che la reinstallazione pulita non la mette a rischio. È MS-052.

Tre fatti collaterali dalle stesse finestre. L'edizione è *Standard* e non professionale, malgrado l'installer si chiami `AKABAK_Pro_...`: l'edizione la determina il release code, coerentemente con la student license concessa. Il prefix dichiara `NT 10.0 (Build 19043)`, cioè Windows 10, che trasforma in fatto misurato una prescrizione data per uniformità. E la memoria riportata, 2047 MByte su una macchina con 16 GB, è una conferma indipendente di ADR-016, perché è lo spazio di indirizzamento di un processo a 32 bit.

Quella conferma era però disponibile prima dell'indagine che ha stabilito il fatto, nello stesso lotto di screenshot letti per ricostruire la corrispondenza. La lezione, in MS-053, non è leggere tutto: è che quando una premessa regge una decisione, il materiale già in mano va interrogato *su quella premessa*, non solo sul tema per cui era stato raccolto.

Corretto un difetto di verifica introdotto dallo spostamento dell'archivio di backup sul Desktop: lo strumento delle azioni differite cercava un percorso fisso e dichiarava mancante un backup esistente, riportando PA-007 a bloccata per un motivo falso. Ora l'invariante è il nome del file fra più posizioni, con controllo della dimensione. È MS-054, e la lezione è che un errore restrittivo in uno strumento di verifica è peggiore di uno permissivo, perché si crede.

Detto chiaro ciò che era rimasto implicito e che l'utente aveva chiesto due volte: *la copia del corredo sul Desktop si può cancellare adesso.* PA-007 riscritta perché lo dica in apertura.

Ripulite dalle informazioni superate quattro sezioni che dichiaravano pendente lavoro compiuto: la coda del registro dei microstep, che elencava come bloccati passi eseguiti e ripeteva la prescrizione sbagliata sui 64 bit, la sezione finale dello storico Akabak e VACS, le voci residue della fase 0 nella fotografia della macchina, e le sezioni di blocco e prossimo passo del lavoro corrente.

## 2026-09-07, quinta parte - Backup di /home fatto, e Akabak si rivela a 32 bit

Commit di partenza: ba69e0c.

Esito in sintesi, tre cose di peso molto diverso.

PA-008 compiuta: l'utente ha cancellato le sei voci di servizio su `J:`, recuperando 1,2 GiB. I due frammenti maggiori erano di 247 e 206 MB, cioè metà del totale: il filesystem aveva perso qualcosa di sostanzioso, che è un elemento in più a favore di PA-009.

Backup di `/home` eseguito e verificato, quindi fase 1.3 chiusa. Alla domanda se potesse stare sulla stessa macchina la risposta è no: la macchina ha un solo disco con quattro partizioni, e una copia sullo stesso supporto della cosa che protegge non è un backup. Fatto su Windows con `tar` in streaming su `ssh`, 4,4 GB, 13.498 file nell'archivio contro 13.498 sulla macchina, permessi e proprietario numerico conservati. Registrato come ADR-015. Questo sblocca PA-007.

E la scoperta che costa più di tutte: *Akabak è a 32 bit*. Il prefix funzionante dichiara `#arch=win32`, `AKABAK.exe` è PE32 i386, VACS installato è la build a 32 bit, e nel prefix non c'è né winetricks, né .NET, né corefonts. Tre affermazioni del documento sorgente sono false, e tre decisioni consecutive le avevano propagate senza tornare alla fonte: la prescrizione operativa era sbagliata su sei documenti, e se eseguita avrebbe prodotto un ambiente in cui il programma centrale del progetto non parte. Corretto tutto, registrato come ADR-016. Il controllo che l'avrebbe evitato costava un comando, `file` sull'eseguibile.

Chiuse per conseguenza entrambe le lacune dello storico di Akabak e VACS, e confermata come corretta l'ipotesi che l'utente stesso aveva formulato nella corrispondenza del 13 agosto 2025, cioè che il fallimento di VACS dipendesse dalla variante a 64 bit.

Constatato anche che il corredo era già sulla macchina, sulla scrivania, il che corregge in meglio il ragionamento di MS-044 su PA-007, e che il release code di Akabak esiste in chiaro in due posti sulla macchina, quindi anche dentro l'archivio di backup.

## 2026-09-07, quarta parte - SSD esterno misurato, archivi confrontati, Desktop rinviato

Commit di partenza: ba69e0c.

File toccati: `docs/PENDING-ACTIONS.md` con PA-007, PA-008 e PA-009 nuove, `docs/90-riferimenti/pulizia-ssd-esterno.md` riscritta nella sezione sugli archivi, `docs/OPERATIONS-LOG.md` con MS-040 a MS-045, `tools/check-pending-actions.py` con tre difetti corretti e tre voci nuove, `tools/analisi-ssd-esterno.py` nuovo, `.claude/memory/decisions.md` con ADR-014, `_notes/` con i due indici degli archivi.

Esito in sintesi, quattro cose.

Gli archivi di backup su `J:` sono stati confrontati e *nessuno dei due contiene l'altro*: 145.483 voci solo nel vecchio e 80.487 solo nel nuovo, per il rimescolamento di `backup-sviluppo`. Cancellare il vecchio costerebbe 145.478 versioni di file. Cade anche l'ipotesi sulla cartella 3DS come causa della differenza di peso.

La copia sul Desktop *non si cancella adesso*, e la ragione è il conteggio delle copie: oggi le voci utili sono in due posti, cancellare il Desktop le porta a uno, e questo proprio prima di una reinstallazione che tocca le partizioni. La condizione di sblocco è la copia di sicurezza di `/home`, cioè la fase 1.3.

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

Esito in sintesi, e non è quello che mi aspettavo. *Tre delle quattro cause che avevo attribuito al blocco di aggiornamento sono false.* Il salto diretto alla LTS è offerto, e `do-release-upgrade -c` risponde che la 26.04.1 LTS è disponibile. La direttiva è `Prompt=normal` e non `lts`, e il commento dello stesso file di configurazione dichiara che con `lts` su un rilascio non-LTS l'aggiornatore assume `normal`, quindi quella causa non poteva agire nemmeno in principio: la risposta era scritta dentro il file che stavo ipotizzando. Gli archivi della 25.04 sono ancora vivi e rispondono 200, non sono stati spostati su `old-releases`, che sulla stessa risorsa risponde 404.

Il fatto che riorganizza tutto è però un altro: `/var/log/dist-upgrade/` è vuota, quindi *l'aggiornamento non è mai stato tentato*. Non c'era un blocco da diagnosticare. La cronologia di apt lo conferma dall'altro lato, con l'ultima operazione datata 13 agosto 2025, e la simulazione elenca 134 pacchetti pendenti senza conflitti. La lezione metodologica è che avevo costruito una diagnosi elaborata su una premessa implicita nella domanda e mai verificata, cioè che un tentativo fosse stato fatto e fosse fallito.

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
