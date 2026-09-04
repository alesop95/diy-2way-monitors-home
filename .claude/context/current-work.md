---
generated-from-commit: 0df04bb7019814cf69b8458e4eaad8eaf71be818
generated-from-branch: main
generated-date: 2026-09-04
covers-paths:
  - docs/**
  - tools/**
  - .claude/**
last-verified-commit: 0df04bb7019814cf69b8458e4eaad8eaf71be818
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

L'accesso alla macchina Ubuntu Studio. L'host `192.168.10.204` non risponde, e la diagnostica registrata in `docs/OPERATIONS-LOG.md` alla voce MS-008 indica che la macchina non è accesa oppure non è su questo segmento di rete. Da questo dipendono cinque microstep già progettati: il trasferimento, la conferma della diagnosi di aggiornamento, l'installazione pulita, la ricostruzione dell'ambiente Wine e la verifica del release code di Akabak.

## Domande aperte per l'utente

Se la macchina sia raggiungibile da un'altra postazione o su un'altra rete, oppure se il travaso dei materiali vada fatto con un supporto fisico. Il manifest resta valido in entrambi i casi.

Se procedere con l'installazione pulita di Ubuntu Studio 26.04 LTS, che è la strada raccomandata con quattro motivi in `docs/10-ambiente/ubuntu-lts-upgrade.md`, oppure con l'aggiornamento in posto in due salti attraverso archivi storici.

Se propagare al template `template-claude-developing` le quattro correzioni trovate qui. La ripropagazione degli strumenti tipografici nel pacchetto `fix-typography`, che è rimasto indietro rispetto alle copie in `tools/`. La negazione nel `.gitignore` che rende versionabili i modelli `_notes` sotto `.claude/templates/`, oggi persi da qualunque clone. L'allineamento delle regole di prudenza fra `fix-accents.py` e `fix-missing-accents.py`, la cui incoerenza corrompe le forme elise nei file di codice, con la riparazione delle quindici occorrenze già danneggiate nei sorgenti del template stesso. La gestione dei percorsi cross-disco nei tre strumenti tipografici, che `md-unwrap.py` ha già e loro no. Le ultime due sono diagnosticate in MS-014 del registro dei microstep, con i casi minimi che le riproducono.

## Prossimo passo concreto

Committare il lavoro di questa sessione, poi accendere o raggiungere la macchina Ubuntu Studio ed eseguire la sequenza di verifica in sola lettura di `docs/10-ambiente/ubuntu-lts-upgrade.md`, confrontando gli esiti reali con quelli attesi.
