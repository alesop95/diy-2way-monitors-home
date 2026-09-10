---
generated-from-commit: 0df04bb7019814cf69b8458e4eaad8eaf71be818
generated-from-branch: main
generated-date: 2026-09-04
covers-paths:
  - docs/**
  - tools/**
  - .claude/**
last-verified-commit: 633c513
---

# Lavoro corrente

> Feature attiva, definizione di finito e domande aperte. Si aggiorna a ogni cambio di fronte di lavoro, non a ogni commit.

## Fronte attivo

Ricostruzione dell'ambiente sulla macchina reinstallata, dal 2026-09-09.

L'installazione è compiuta e verificata, quindi il fronte non è più documentale ma operativo, e si svolge sulla macchina via `ssh studio`. Lo stato di partenza è fotografato in `docs/10-ambiente/setup-macchina-2026-09.md`, che è anche il documento dove la cronologia e il razionale del setup vanno tenuti aggiornati mano a mano.

Definizione di finito per questo fronte. La catena audio verificata per quanto è verificabile senza acquisti, cioè i parametri di avvio e i limiti realtime, che sono già a posto, più i dispositivi presenti visti in ingresso e in uscita con una riproduzione di prova che si sente. L'ambiente Wine ricostruito con l'architettura `i386` dichiarata prima dell'installazione di Wine, per ADR-016. Akabak e VACS funzionanti in un prefix a 32 bit con la licenza valida: raggiunto il 2026-09-09 e verificato il 2026-09-10, e per una via diversa da quella prevista, cioè senza reinstallare e senza reinserire il codice. Il corredo `Progetto stanza` installato secondo le sottofasi da 8.5 a 8.9.

Bloccato da una decisione e non da una condizione fisica, e la differenza è emersa il 2026-09-09. Sulla macchina c'è la sola scheda integrata `ALC887-VD`, e l'interfaccia esterna che i documenti dichiaravano come presente non appartiene a questo progetto: il ritiro è in MS-079. Quale interfaccia acquisire è una scelta condivisa con il progetto gemello di home recording, con due vincoli fissati dall'utente, cioè dispositivo di classe audio senza driver proprietari e capacità di reggere anche le misure della fase 8. Da quella scelta dipende quella del microfono, e l'ordine non è invertibile.

*Ipotesi risolta il 2026-09-09, e il suo esito ha ridotto il fronte.* Il prefix `~/.wine` è sopravvissuto all'azzeramento della radice con AKABAK installato dentro e la licenza attiva, e la domanda era se la migrazione automatica che Wine applica ai prefix creati da versioni molto precedenti lo avrebbe rotto. Non lo ha rotto: aperto con `wine32` sotto Wine 10, dopo una copia di sicurezza da 831 MB, il prefix si è migrato e il programma è partito. Il 2026-09-10 lo stato della licenza è stato verificato per due vie indipendenti, cioè il file di configurazione a livello di macchina e la finestra `Release code` del menu di aiuto, che dichiara `Release Code valid` con il Machine Identifier invariato. Le sottofasi 8.1 e 8.2, cioè reinstallazione e riattivazione, non vanno quindi eseguite: il racconto è in MS-085. Restano in procedura per chi ricostruisse da zero, e il loro comando è stato corretto insieme alle altre ventuno occorrenze sbagliate censite in MS-087.

## Fronte chiuso il 2026-09-04: impianto del progetto

Impianto del progetto: allineamento al template, conversione del documento sorgente in documentazione navigabile, preparazione dell'ambiente di lavoro e della sua manutenzione. È lavoro di infrastruttura documentale, non ancora lavoro di progettazione elettroacustica.

### Definizione di finito per questo fronte

Il progetto allineato al template, con le sette regole, le skill e il catalogo dei pacchetti aggiornati, e i valori specifici di macchina re-istanziati nelle regole che li richiedono. Raggiunto.

Il documento sorgente convertito in un albero `docs/` navigabile, con la prova documentata che la copertura è integrale, così che il `.docx` sia rimovibile senza perdita. Raggiunto; la prova è in `docs/90-riferimenti/copertura-sorgente.md`.

Il blocco sull'ambiente isolato e propagato al progetto gemello con uno strumento invece che a mano. Raggiunto.

Il trasferimento dei materiali pesanti preparato con manifest, impronte e strumenti che verificano prima di copiare. Raggiunto per la preparazione, non per l'esecuzione.

Il version control in ordine, cioè un `.gitignore` che non nasconde file da versionare e non versiona materiale pesante, e l'identità git verificata. Raggiunto.

La roadmap del progetto scritta con priorità motivate e decisioni aperte dichiarate. Raggiunto.

Il registro dei microstep con l'esito verificato di ciascuno. Raggiunto, in `docs/OPERATIONS-LOG.md`.

### Che cosa manca a questo fronte

Il commit e il push, che restano operazioni manuali dell'utente.

### Bloccato da

Nulla. È la prima volta in questa sessione che questa sezione può dirlo senza qualificazioni, e vale registrarlo perché fino a poche ore prima elencava due dipendenze.

Le due dipendenze che c'erano sono cadute entrambe. La decisione fra installazione pulita e aggiornamento in posto è presa e riconfermata dall'utente, ed è ADR-013, che chiude PA-006. Dei tre controlli privilegiati della fase 0, tracciati come PA-005, i due che potevano spostare una decisione sono eseguiti: il disco risulta sano e il Machine Identifier di Akabak coincide con quello a cui il Release Code è legato. Il terzo, l'esito reale di `sudo apt update`, non è eseguito ma ADR-013 lo ha reso irrilevante, perché su un sistema che verrà azzerato non informa nessuna scelta.

La storia del blocco, che è finita, vale come traccia. Macchina di stato ignoto, poi scoperta sospesa e quindi invisibile anche all'ARP, poi sveglia ma senza autenticazione configurata, poi accessibile. Le correzioni sono in MS-015, MS-016 e MS-028.

### Domande aperte per l'utente

Le due decisioni maggiori sono prese e non sono più domande. L'installazione pulita della 26.04 LTS è confermata e registrata come ADR-006 accettata. La macchina è sulla stessa rete della postazione, quindi il travaso dei materiali passa per rete locale e non richiede un supporto fisico.

Resta invece aperta la scelta se propagare al template `template-claude-developing` le quattro correzioni trovate qui. La ripropagazione degli strumenti tipografici nel pacchetto `fix-typography`, che è rimasto indietro rispetto alle copie in `tools/`. La negazione nel `.gitignore` che rende versionabili i modelli `_notes` sotto `.claude/templates/`, oggi persi da qualunque clone. L'allineamento delle regole di prudenza fra `fix-accents.py` e `fix-missing-accents.py`, la cui incoerenza corrompe le forme elise nei file di codice, con la riparazione delle quindici occorrenze già danneggiate nei sorgenti del template stesso. La gestione dei percorsi cross-disco nei tre strumenti tipografici, che `md-unwrap.py` ha già e loro no. Le ultime due sono diagnosticate in MS-014 del registro dei microstep, con i casi minimi che le riproducono.

## Fronte chiuso il 2026-09-08: la carta per la reinstallazione

La fase 2 è chiusa e committata, quindi il fronte attivo non è più la preparazione del supporto ma la scheda che si porta accanto alla macchina durante la reinstallazione. La sua sorgente tracciata è `docs/10-ambiente/scheda-reinstallazione.md`, il documento stampabile si genera con `python tools/make-scheda-docx.py` e la decisione che governa i due è ADR-017.

Definizione di finito per questo fronte, raggiunta. La scheda contiene l'avvertenza sul modo concreto in cui il passo irreversibile si sbaglia, cioè che la casella di formattazione si attiva da sé selezionando un filesystem nel menu della riga, e la contiene nei tre punti in cui l'operatore ha gli occhi in tre posti diversi. Il controllo sulla schermata di riepilogo è un passo con la sua casella da spuntare e non una raccomandazione in prosa. Il documento di stampa è riproducibile da uno strumento versionato invece di essere composto a mano. Il racconto è in MS-070.

## Lavoro noto e non fatto, senza condizioni esterne

Questa sezione è diversa da `docs/PENDING-ACTIONS.md` e la distinzione va tenuta: là stanno gli impegni che dipendono da una condizione esterna, qui il lavoro che si può fare in qualunque momento e non è stato fatto. Tenerlo fuori da entrambi i posti è il modo in cui un difetto noto diventa un difetto dimenticato.

La grafia degli accenti con l'apostrofo sopravvive nei modelli sotto `.claude/templates/`, per una decina di occorrenze fra il pacchetto `md-unwrap`, il catalogo degli agenti, il pacchetto `fix-typography`, il documento di handoff e la skill di estrazione bibliografica. Non si corregge qui: quei file sono copie del template, e riscriverli in questo repository allargherebbe la divergenza che PA-003 esiste per chiudere, quindi la correzione appartiene alla propagazione all'indietro e non a questo fronte.

Nei file di documentazione del progetto la grafia è invece stata sanata il 2026-09-08, ed è utile registrare perché il conteggio iniziale era molto più alto della realtà. Una prima conta dava venti occorrenze in `docs/OPERATIONS-LOG.md` e cinque in `CLAUDE.md`, ma quasi tutte stavano dentro code span, cioè erano le forme sbagliate citate di proposito come esempi negli stessi microstep che raccontano i difetti degli strumenti tipografici. I difetti reali in prosa erano due nel registro e tre in `CLAUDE.md`, e sono corretti. La verifica che ha reso sicura la correzione è stata un caso minimo su un file di prova, che ha mostrato che `fix-accents.py` protegge il contenuto dei code span inline esattamente come quello dei blocchi recintati; senza quella prova la ripulitura avrebbe distrutto la documentazione dei difetti. Il caso della scheda, che ne portava ventotto in prosa, è chiuso in MS-071.

## Deriva di stile rispetto al template

Il template `template-claude-developing` prescrive alla sezione 8 di `PROJECT-SYSTEM.md` che nella prosa non si usino elenchi puntati, emoji né grassetto, e che gli acronimi si spieghino in note a piè di pagina numerate. Parte della documentazione di questo progetto non lo rispetta, e la deriva è quantificata: `docs/OPERATIONS-LOG.md` contiene grassetto in prosa in gran quantità, `docs/10-ambiente/installazione-pulita-26-04.md` in ventotto punti, `docs/10-ambiente/fotografia-macchina-2026-09-07.md` in ventiquattro, e `.claude/memory/progress.md` in undici. Le note a piè di pagina esistono in cinque pagine su dodici del blocco ambiente.

Dal 2026-09-09 la documentazione nuova rispetta lo stile del template, e `docs/10-ambiente/setup-macchina-2026-09.md` ne è la prima applicazione integrale, con zero grassetto in prosa e sei note a piè di pagina. La ripulitura del pregresso non è stata eseguita per una ragione che va dichiarata invece di sembrare una dimenticanza: il registro dei microstep proibisce di riscrivere una voce passata, e la maggior parte del grassetto in prosa vive dentro voci già committate. La riscrittura di quelle voci va quindi decisa esplicitamente, perché è una modifica alla forma di documentazione storica e non una correzione di contenuto.

## Prossimo passo concreto

Le fasi da 0 a 7 sono chiuse, e della fase 8 sono chiuse le due sottofasi che riguardano l'installazione e la licenza, per il motivo detto sopra. Il prossimo passo è quindi la fase 8 dalla sottofase 8.3 in avanti, che è lavoro eseguibile adesso e non dipende da alcun acquisto: il limite delle pipeline COM da impostare nelle preferenze di AKABAK, il pacchetto degli esempi da estrarre, poi VituixCAD, EASE Focus 3.1.260 con il servizio di database AFMG e il suo database dei GLL, e ARTA. Ramsete resta fuori finché PA-002 non è risolta.

L'accertamento sull'edizione è chiuso il 2026-09-10 e non resta nulla di aperto nelle sottofasi 8.1 e 8.2. L'edizione è `Standard Edition`, come le tre pagine che la affermavano già dicevano, e la finestra di informazioni sul programma porta insieme a essa `Valid Release Code`, il profilo `NT 10.0 (Build 19043)` e la memoria `1876 / 2047 MBytes`. La discrepanza che avevo dichiarato non esisteva: il `32 Professional` della barra del titolo non è l'edizione di AKABAK, e averlo trattato come tale è l'errore di lettura ritirato in MS-089.

Attenzione a una prescrizione ritirata il 2026-09-09, perché una versione precedente di questa sezione diceva il contrario: il passo successivo non è collegare la Focusrite Scarlett 2i2 per completare la fase 6. Quella interfaccia esiste ma non appartiene a questo progetto, il ritiro è in MS-079, e la misura del 2026-09-10 lo conferma indipendentemente, dato che `/proc/asound/cards` riporta la sola scheda integrata. La fase 6 non attende un cavo ma la decisione di acquisto di PA-012, e da quella dipende la scelta del microfono in un ordine che non si può invertire.

Prima di cancellare qualunque copia esterna di materiale personale va compiuta PA-010, cioè l'inventario per impronta fra le copie esterne e `/home`. I due controlli fatti finora coprono un perimetro molto più stretto di quello che serve, e la cancellazione non è autorizzata da un'impressione visiva.

A fase 8 chiusa e verificata va preso il backup completo della macchina di PA-011, che è cosa diversa dall'archivio di `/home` già esistente: quello contiene i dati e non il sistema, e lo scopo del secondo è rendere ripetibile in poche ore un risultato che è costato più di un giorno. Sulla voce esiste ora una discrepanza dichiarata a proposito dell'esperienza precedente dell'utente con Veeam su Linux, ed è annotata in PA-011.

Una decisione resta da prendere e non è mia: se ripulire la deriva di stile rispetto al template nella documentazione già committata, quantificata nella sezione dedicata più sopra.
