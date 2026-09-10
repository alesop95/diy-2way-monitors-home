# Snapshot di sincronizzazione

> Da leggere per primo a inizio sessione. Fotografa lo stato del progetto al commit di riferimento e mappa ogni scheda al suo stato di verifica. È la fonte di verità su cosa è fatto.

## Stato

```
Branch attivo:          main
Commit di riferimento:  633c513
Data snapshot:          2026-09-10
Modifiche non committate: sì, MS-089 e le schede riallineate
```

Il repository conta 33 commit e origin è in pari fino a `633c513`. I due più recenti sono del 2026-09-10: `d8ebf45`, con cui il livello didattico e ADR-019, scritti la sera prima e lasciati sul disco dal riavvio, sono entrati nella storia, e `633c513` con i microstep da MS-085 a MS-088, il censimento dei comandi di Wine e le schede riallineate. I quattro precedenti sono del 2026-09-09 e riguardano tutti la fase 7: `14fcea4` con il setup della macchina documentato e lo stile allineato al template, `8e2e9a7` con il ritiro della Scarlett e l'apertura di PA-012 e ADR-018, `547b2dd` con il nome del pacchetto Wine corretto e l'architettura `i386` verificata, e `b514c33` con la scoperta che il prefix a 32 bit vuole `wine32` e il ritiro di MS-083. Prima di essi, `d9912b1` porta l'installazione eseguita con `/home` intatto, l'accesso SSH e quattro correzioni, e `81793e9` la scheda di stampa generata da uno strumento. Del 2026-09-08 sono `d2905ba` con il Machine Identifier confermato, `351252d` con PA-007 chiusa e il controllo nuovo sulle fini riga, e `cadf335` con la fase 2 chiusa; `1b4e801` porta la sequenza operativa e le verifiche dell'immagine di installazione. I due del 2026-09-04 che hanno impiantato il progetto sono `9e9517e`, con l'allineamento al template e la conversione del documento sorgente, e `3eac5f3`, con l'approfondimento su Wine, la procedura di installazione pulita e lo storico di Akabak e VACS. Commit e push restano operazioni manuali dell'utente.

Sul lavoro non committato vale una avvertenza, perché è la lezione della ripresa del 2026-09-10 e si ripeterà. La sessione del 2026-09-09 si è chiusa con il livello didattico scritto e non committato, cioè ADR-019, la voce di `progress.md`, l'adozione in `CLAUDE.md` e i due file nuovi sotto `.claude/context/`; a quel punto questo snapshot dichiarava ancora `d9912b1` e la scheda del lavoro corrente indicava come passo successivo una prescrizione già ritirata. Una sessione nuova che avesse creduto alle schede invece che a `git log` avrebbe rifatto lavoro fatto e collegato un'interfaccia che non appartiene al progetto. Le due schede sono state riallineate e il lavoro arretrato è stato committato come `d8ebf45`. La regola operativa è che a inizio sessione lo snapshot si confronta con `git log --oneline -8` prima di essere creduto, e la stessa regola vale a fine sessione nel verso opposto: un commit fatto durante la sessione invecchia lo snapshot appena scritto. È accaduto due volte nella stessa sessione del 2026-09-10, con `d8ebf45` e poi con `633c513`, e la conseguenza pratica è che il campo del commit di riferimento va riletto e non ricordato ogni volta che si scrive in questo file.

## Che cos'è questo progetto, in tre righe

Progettazione e costruzione di una coppia di monitor da studio a due vie per un punto di ascolto domestico noto e non trattabile acusticamente. Il flusso di progettazione gira su una macchina Ubuntu Studio, con i programmi Windows indispensabili sotto Wine. Il punto d'ingresso della documentazione è `docs/README.md`; la direzione del progetto è in `.claude/context/roadmap.md`.

## Stato di verifica delle schede

| Scheda | last-verified | Stato |
|---|---|---|
| STACK.md | ba69e0c | aggiornata |
| roadmap.md | 633c513 | aggiornata il 2026-09-10: priorità riscritte, due ipotesi risolte, direzioni future |
| current-work.md | 633c513 | aggiornata il 2026-09-10 |
| design-and-security.md | - | non creata: il progetto non ha codice applicativo né superficie di attacco |
| deployment.md | - | non creata: non c'è deploy; il suo equivalente è `docs/TRANSFER-MANIFEST.md` |
| dev-testing.md | - | non creata: i test sono le suite degli strumenti, descritte in STACK.md |

Le tre schede non create sono una decisione, non una dimenticanza: il sistema di progetto prescrive di adottare la forma minima ed estenderla solo quando la complessità lo richiede.

## Documenti da non confondere

Il registro dei microstep, con l'esito verificato di ogni intervento, è `docs/OPERATIONS-LOG.md`. Il work-log di sessione è `.claude/memory/progress.md`. Il primo è il livello tecnico-didattico rivolto a chi legge il progetto, il secondo è il livello di meta-stato rivolto a chi lo riprende. Le azioni differite, con le condizioni che le sbloccano, stanno in `docs/PENDING-ACTIONS.md`, e sono cosa diversa da entrambi: non sono lavoro fatto né stato del progetto, ma impegni con una condizione esterna.

## Punto di ripresa

Le fasi da 0 a 7 della procedura di installazione pulita sono chiuse, e della fase 8 sono chiuse le sottofasi 8.1 e 8.2 per un motivo che vale più di una spunta: non sono state eseguite, sono diventate inutili. Il prefix `~/.wine` è sopravvissuto all'azzeramento della radice perché vive in `/home`, conteneva AKABAK e VACS installati con la licenza attiva, e aperto con `wine32` sotto Wine 10, dopo una copia di sicurezza da 831 MB, si è migrato senza rompersi. È la prima volta che la separazione fra radice e `/home` produce un risparmio misurabile invece di essere soltanto un presidio.

Lo stato della licenza è verificato per due vie indipendenti il 2026-09-10, ed è MS-085. L'attivazione non vive nel registro del prefix, dove era stata cercata, ma nel file `C:\ProgramData\RDTeam\Akabak.ini` a livello di macchina, il che spiega perché la migrazione del prefix non l'abbia toccata; il codice scritto là coincide con quello conservato nella scheda riservata sotto `_notes/`, e la finestra `Release code` del menu di aiuto dichiara `Release Code valid` con il Machine Identifier `C937-FD3A` invariato. È la quarta conferma indipendente dell'affermazione di ADR-003 e la prima raccolta dopo la reinstallazione, quindi l'unica che la dimostri davvero.

Su Wine il quadro completo è in ADR-016 e ADR-019 e va letto in questo ordine. L'architettura `i386` va dichiarata sul sistema e non evitata, perché Akabak è a 32 bit; e su un prefix a 32 bit il comando è `wine32` con `WINEPREFIX` dichiarato esplicitamente, non `wine`, perché il comando `wine` è uno script che sceglie il caricatore a 64 bit ogni volta che `wine64` esiste. Lo stesso vale per `winecfg` e `wineboot`, che sono script di cinque righe che eseguono incondizionatamente lo stesso wrapper, e per `winetricks`, che va invocato con `WINE=wine32` davanti perché il binario che usa è configurabile e per default è quello sbagliato. Il censimento delle occorrenze sbagliate nella documentazione, ventitré in sette pagine, è MS-087, e la sua lezione è che una prescrizione sbagliata non vive dove la si è incontrata.

Il prossimo passo è la fase 8 dalla sottofase 8.3 in avanti, che è lavoro eseguibile subito e non dipende da acquisti: il limite delle pipeline COM nelle preferenze di AKABAK, gli esempi da estrarre, poi VituixCAD, EASE Focus 3.1.260 con il servizio di database AFMG, e ARTA. Ramsete resta fuori finché PA-002 non è risolta.

L'edizione è accertata il 2026-09-10 ed è `Standard Edition`, letta nella finestra di informazioni sul programma insieme a `Valid Release Code`, al profilo `NT 10.0 (Build 19043)` e alla memoria `1876 / 2047 MBytes` che è la firma del processo a 32 bit. Le tre pagine che affermavano l'edizione Standard sono confermate, e la conferma vale perché è la prima raccolta dopo la reinstallazione. Va invece ritirata una mia lettura: il `32 Professional` della barra del titolo non dichiara l'edizione di AKABAK, quindi non c'era discrepanza da conciliare. È MS-089, e non restano accertamenti aperti nella fase 8.

La fase 6 non è chiusa e non lo sarà per lavoro: è bloccata da una decisione di acquisto, cioè PA-012, e non da una condizione fisica. La macchina ha la sola scheda integrata `ALC887-VD`, verificato due volte a un giorno di distanza, e l'interfaccia esterna che i documenti dichiaravano come propria non appartiene a questo progetto: il ritiro è in MS-079. Due parametri della scelta non sono ancora stati dichiarati dall'utente e vanno chiesti, cioè il numero di ingressi simultanei e un eventuale tetto di spesa.

Sull'hardware presente vale registrare l'inventario misurato il 2026-09-10, perché l'inventario desunto da un ricordo è già costato un ritiro. Il sistema vede una sola scheda audio, la integrata. Il Nektar Impact GX49 dichiarato dall'utente non è collegato adesso, e il collaudo che l'utente ricorda appartiene al sistema precedente, azzerato dalla reinstallazione; lo strato MIDI del sistema però è presente e attivo, con PipeWire che si dichiara `UMP-MIDI2`, quindi il collaudo consiste nel collegare il dispositivo e rifare tre letture. Il controller serve al progetto gemello di home recording e non entra in alcuna delle otto fasi di questo.

Due direzioni sono state dichiarate dall'utente come non urgenti e stanno in `.claude/context/roadmap.md`, dove vive la direzione e non il lavoro attivo: il backup completo della macchina con Veeam, che è PA-011 e sulla cui esperienza precedente esiste una discrepanza dichiarata, e la replica del setup sul secondo portatile, un Asus F550CC-XX698H su Ubuntu 24.04 LTS, per cui la roadmap enuncia i due punti che decidono se valga la pena, cioè i 4 GB di RAM con il tetto di 2047 MByte per un processo a 32 bit, e il fatto che la licenza di Akabak sia legata a una macchina sola e quindi non replicabile.

Lo stato dell'accesso alla macchina: è raggiungibile come `ssh studio`, per chiave e anche in modo non interattivo, verificato il 2026-09-10. La sospensione automatica è disattivata con quattro target `masked` dal 2026-09-09, quindi la macchina non scompare più dalla rete da sé. Resta che `sudo` chiede la password, per scelta dell'utente, quindi il lavoro privilegiato si esegue a mano su comandi preparati. Il suo indirizzo hardware è `2c:4d:54:53:a4:fb`, utile per il Wake-on-LAN e per una prenotazione dell'indirizzo sul router.

Prima di cancellare qualunque copia esterna di materiale personale va compiuta PA-010, l'inventario per impronta fra le copie esterne e `/home`. I due controlli fatti finora coprono un perimetro molto più stretto di quello che serve.
