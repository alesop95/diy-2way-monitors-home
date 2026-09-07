---
generated-from-commit: 0df04bb7019814cf69b8458e4eaad8eaf71be818
generated-from-branch: main
generated-date: 2026-09-04
covers-paths:
  - docs/**
  - tools/**
  - .claude/**
last-verified-commit: 3eac5f3
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

L'installazione della chiave SSH sulla macchina Ubuntu Studio, che richiede la password una volta sola e va eseguita dall'utente. È l'unico blocco residuo, e il percorso è la fase 10.3 di `docs/10-ambiente/installazione-pulita-26-04.md`.

Il blocco è cambiato natura nel corso della sessione, e vale registrarlo perché è un progresso. La macchina risultava di stato ignoto e la prima diagnosi, in MS-008, la dava per spenta o su un altro segmento. La lettura corretta l'ha data l'utente: si sospende da sola, e una macchina sospesa non risponde nemmeno alle richieste ARP, quindi scompare del tutto dalla rete. Risvegliata, ha risposto al ping con TTL 64 e ha accettato la connessione sulla porta 22, rifiutando l'autenticazione perché nessuna chiave della postazione è autorizzata e perché `~/.ssh/config` non ha una voce per quell'host, quindi `ssh` non prova nemmeno le chiavi esistenti. Le correzioni sono in MS-015 e MS-016.

## Domande aperte per l'utente

Le due decisioni maggiori sono prese e non sono più domande. L'installazione pulita della 26.04 LTS è confermata e registrata come ADR-006 accettata. La macchina è sulla stessa rete della postazione, quindi il travaso dei materiali passa per rete locale e non richiede un supporto fisico.

Resta invece aperta la scelta se propagare al template `template-claude-developing` le quattro correzioni trovate qui. La ripropagazione degli strumenti tipografici nel pacchetto `fix-typography`, che è rimasto indietro rispetto alle copie in `tools/`. La negazione nel `.gitignore` che rende versionabili i modelli `_notes` sotto `.claude/templates/`, oggi persi da qualunque clone. L'allineamento delle regole di prudenza fra `fix-accents.py` e `fix-missing-accents.py`, la cui incoerenza corrompe le forme elise nei file di codice, con la riparazione delle quindici occorrenze già danneggiate nei sorgenti del template stesso. La gestione dei percorsi cross-disco nei tre strumenti tipografici, che `md-unwrap.py` ha già e loro no. Le ultime due sono diagnosticate in MS-014 del registro dei microstep, con i casi minimi che le riproducono.

## Prossimo passo concreto

Installare la chiave SSH dedicata sulla macchina, secondo la fase 10.3 della procedura, poi eseguire la fase 0 della stessa procedura, cioè la fotografia completa in quattordici file. È il passo che conferma o smentisce la diagnosi del blocco di aggiornamento, chiude la lacuna sui prefix Wine esistenti, e verifica che il Machine Identifier di Akabak sia ancora quello a cui il Release Code è legato.
