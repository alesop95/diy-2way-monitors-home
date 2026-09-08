---
generated-from-commit: 0df04bb7019814cf69b8458e4eaad8eaf71be818
generated-from-branch: main
generated-date: 2026-09-04
covers-paths:
  - docs/**
  - tools/**
  - .claude/**
last-verified-commit: ba69e0c
---

# Lavoro corrente

> Feature attiva, definizione di finito e domande aperte. Si aggiorna a ogni cambio di fronte di lavoro, non a ogni commit.

## Fronte attivo

Impianto del progetto: allineamento al template, conversione del documento sorgente in documentazione navigabile, preparazione dell'ambiente di lavoro e della sua manutenzione. È lavoro di infrastruttura documentale, non ancora lavoro di progettazione elettroacustica.

## Definizione di finito per questo fronte

Il progetto allineato al template, con le sette regole, le skill e il catalogo dei pacchetti aggiornati, e i valori specifici di macchina re-istanziati nelle regole che li richiedono. Raggiunto.

Il documento sorgente convertito in un albero `docs/` navigabile, con la prova documentata che la copertura è integrale, così che il `.docx` sia rimovibile senza perdita. Raggiunto; la prova è in `docs/90-riferimenti/copertura-sorgente.md`.

Il blocco sull'ambiente isolato e propagato al progetto gemello con uno strumento invece che a mano. Raggiunto.

Il trasferimento dei materiali pesanti preparato con manifest, impronte e strumenti che verificano prima di copiare. Raggiunto per la preparazione, non per l'esecuzione.

Il version control in ordine, cioè un `.gitignore` che non nasconde file da versionare e non versiona materiale pesante, e l'identità git verificata. Raggiunto.

La roadmap del progetto scritta con priorità motivate e decisioni aperte dichiarate. Raggiunto.

Il registro dei microstep con l'esito verificato di ciascuno. Raggiunto, in `docs/OPERATIONS-LOG.md`.

## Che cosa manca a questo fronte

Il commit e il push, che restano operazioni manuali dell'utente.

## Bloccato da

Nulla. È la prima volta in questa sessione che questa sezione può dirlo senza qualificazioni, e vale registrarlo perché fino a poche ore prima elencava due dipendenze.

Le due dipendenze che c'erano sono cadute entrambe. La decisione fra installazione pulita e aggiornamento in posto è presa e riconfermata dall'utente, ed è ADR-013, che chiude PA-006. Dei tre controlli privilegiati della fase 0, tracciati come PA-005, i due che potevano spostare una decisione sono eseguiti: il disco risulta sano e il Machine Identifier di Akabak coincide con quello a cui il Release Code è legato. Il terzo, l'esito reale di `sudo apt update`, non è eseguito ma ADR-013 lo ha reso irrilevante, perché su un sistema che verrà azzerato non informa nessuna scelta.

La storia del blocco, che è finita, vale come traccia. Macchina di stato ignoto, poi scoperta sospesa e quindi invisibile anche all'ARP, poi sveglia ma senza autenticazione configurata, poi accessibile. Le correzioni sono in MS-015, MS-016 e MS-028.

## Domande aperte per l'utente

Le due decisioni maggiori sono prese e non sono più domande. L'installazione pulita della 26.04 LTS è confermata e registrata come ADR-006 accettata. La macchina è sulla stessa rete della postazione, quindi il travaso dei materiali passa per rete locale e non richiede un supporto fisico.

Resta invece aperta la scelta se propagare al template `template-claude-developing` le quattro correzioni trovate qui. La ripropagazione degli strumenti tipografici nel pacchetto `fix-typography`, che è rimasto indietro rispetto alle copie in `tools/`. La negazione nel `.gitignore` che rende versionabili i modelli `_notes` sotto `.claude/templates/`, oggi persi da qualunque clone. L'allineamento delle regole di prudenza fra `fix-accents.py` e `fix-missing-accents.py`, la cui incoerenza corrompe le forme elise nei file di codice, con la riparazione delle quindici occorrenze già danneggiate nei sorgenti del template stesso. La gestione dei percorsi cross-disco nei tre strumenti tipografici, che `md-unwrap.py` ha già e loro no. Le ultime due sono diagnosticate in MS-014 del registro dei microstep, con i casi minimi che le riproducono.

## Il fronte del 2026-09-08: la carta per la reinstallazione

La fase 2 è chiusa e committata, quindi il fronte attivo non è più la preparazione del supporto ma la scheda che si porta accanto alla macchina durante la reinstallazione. La sua sorgente tracciata è `docs/10-ambiente/scheda-reinstallazione.md`, il documento stampabile si genera con `python tools/make-scheda-docx.py` e la decisione che governa i due è ADR-017.

Definizione di finito per questo fronte, raggiunta. La scheda contiene l'avvertenza sul modo concreto in cui il passo irreversibile si sbaglia, cioè che la casella di formattazione si attiva da sé selezionando un filesystem nel menu della riga, e la contiene nei tre punti in cui l'operatore ha gli occhi in tre posti diversi. Il controllo sulla schermata di riepilogo è un passo con la sua casella da spuntare e non una raccomandazione in prosa. Il documento di stampa è riproducibile da uno strumento versionato invece di essere composto a mano. Il racconto è in MS-070.

## Lavoro noto e non fatto, senza condizioni esterne

Questa sezione è diversa da `docs/PENDING-ACTIONS.md` e la distinzione va tenuta: là stanno gli impegni che dipendono da una condizione esterna, qui il lavoro che si può fare in qualunque momento e non è stato fatto. Tenerlo fuori da entrambi i posti è il modo in cui un difetto noto diventa un difetto dimenticato.

La grafia degli accenti con l'apostrofo sopravvive nei modelli sotto `.claude/templates/`, per una decina di occorrenze fra il pacchetto `md-unwrap`, il catalogo degli agenti, il pacchetto `fix-typography`, il documento di handoff e la skill di estrazione bibliografica. Non si corregge qui: quei file sono copie del template, e riscriverli in questo repository allargherebbe la divergenza che PA-003 esiste per chiudere, quindi la correzione appartiene alla propagazione all'indietro e non a questo fronte.

Nei file di documentazione del progetto la grafia è invece stata sanata il 2026-09-08, ed è utile registrare perché il conteggio iniziale era molto più alto della realtà. Una prima conta dava venti occorrenze in `docs/OPERATIONS-LOG.md` e cinque in `CLAUDE.md`, ma quasi tutte stavano dentro code span, cioè erano le forme sbagliate citate di proposito come esempi negli stessi microstep che raccontano i difetti degli strumenti tipografici. I difetti reali in prosa erano due nel registro e tre in `CLAUDE.md`, e sono corretti. La verifica che ha reso sicura la correzione è stata un caso minimo su un file di prova, che ha mostrato che `fix-accents.py` protegge il contenuto dei code span inline esattamente come quello dei blocchi recintati; senza quella prova la ripulitura avrebbe distrutto la documentazione dei difetti. Il caso della scheda, che ne portava ventotto in prosa, è chiuso in MS-071.

## Prossimo passo concreto

Le fasi 0 e 1 sono chiuse, quindi il prossimo passo è l'installazione pulita di Ubuntu Studio 26.04 LTS conservando `/home`, cioè le fasi da 2 a 5 della procedura. Il presidio contro l'unico rischio irreversibile, l'errore umano nella selezione delle partizioni, è già in posizione: la copia di sicurezza di `/home` esiste su una macchina diversa, verificata per numero di file e permessi.

Un avviso che vale più della sequenza. Le fasi 7 e 8 sono state corrette il 2026-09-07 per ADR-016: chi eseguisse una versione precedente della procedura otterrebbe un ambiente in cui Akabak non parte, perché l'architettura `i386` va dichiarata e non evitata e il prefix di Akabak va creato a 32 bit.

Due azioni dell'utente sono eseguibili adesso e non dipendono dalla reinstallazione: la cancellazione della copia del corredo sul Desktop, PA-007, sbloccata dal backup verificato, e la lettura dello SMART dell'SSD esterno, PA-009.
