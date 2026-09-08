# Snapshot di sincronizzazione

> Da leggere per primo a inizio sessione. Fotografa lo stato del progetto al commit di riferimento e mappa ogni scheda al suo stato di verifica. È la fonte di verità su cosa è fatto.

## Stato

```
Branch attivo:          main
Commit di riferimento:  1b4e801
Data snapshot:          2026-09-08
Modifiche non committate: sì, la coda della sessione del 2026-09-08
```

Il repository conta 22 commit e origin è in pari fino a `1b4e801`. I due più recenti, del 2026-09-08, sono `d2905ba` con il Machine Identifier confermato e la ripulitura delle informazioni superate, e `1b4e801` con la sequenza operativa e le verifiche dell'immagine di installazione. I due del 2026-09-04 che hanno impiantato il progetto sono `9e9517e`, con l'allineamento al template e la conversione del documento sorgente, e `3eac5f3`, con l'approfondimento su Wine, la procedura di installazione pulita e lo storico di Akabak e VACS. Commit e push restano operazioni manuali dell'utente.

## Che cos'è questo progetto, in tre righe

Progettazione e costruzione di una coppia di monitor da studio a due vie per un punto di ascolto domestico noto e non trattabile acusticamente. Il flusso di progettazione gira su una macchina Ubuntu Studio, con i programmi Windows indispensabili sotto Wine. Il punto d'ingresso della documentazione è `docs/README.md`; la direzione del progetto è in `.claude/context/roadmap.md`.

## Stato di verifica delle schede

| Scheda | last-verified | Stato |
|---|---|---|
| STACK.md | ba69e0c | aggiornata |
| roadmap.md | ba69e0c | da rileggere: la fase 0 ha cambiato le priorità |
| current-work.md | ba69e0c | aggiornata |
| design-and-security.md | - | non creata: il progetto non ha codice applicativo né superficie di attacco |
| deployment.md | - | non creata: non c'è deploy; il suo equivalente è `docs/TRANSFER-MANIFEST.md` |
| dev-testing.md | - | non creata: i test sono le suite degli strumenti, descritte in STACK.md |

Le tre schede non create sono una decisione, non una dimenticanza: il sistema di progetto prescrive di adottare la forma minima ed estenderla solo quando la complessità lo richiede.

## Documenti da non confondere

Il registro dei microstep, con l'esito verificato di ogni intervento, è `docs/OPERATIONS-LOG.md`. Il work-log di sessione è `.claude/memory/progress.md`. Il primo è il livello tecnico-didattico rivolto a chi legge il progetto, il secondo è il livello di meta-stato rivolto a chi lo riprende. Le azioni differite, con le condizioni che le sbloccano, stanno in `docs/PENDING-ACTIONS.md`, e sono cosa diversa da entrambi: non sono lavoro fatto né stato del progetto, ma impegni con una condizione esterna.

## Punto di ripresa

L'accesso SSH è aperto e funzionante con la chiave `id_ed25519_studio`, anche in modalità non interattiva. La fase 0 della procedura è eseguita nella sua parte non privilegiata, e il suo esito è in `docs/10-ambiente/fotografia-macchina-2026-09-07.md`.

La decisione è presa: installazione pulita di Ubuntu Studio 26.04 LTS, con il lavoro privilegiato eseguito a mano dall'utente su comandi preparati. È ADR-013, e chiude PA-006. La pulizia dell'ambiente Wine e l'aggiornamento del sistema **non si fanno**, perché sarebbero lavoro buttato su un sistema che verrà azzerato.

La fase 1.1 è compiuta: il trasferimento dei materiali e del corredo è eseguito e verificato, 728 MB e 281 file sotto `~/electroacoustics` sulla macchina, con collegamento sulla scrivania. Questo sblocca PA-001, cioè la cancellazione della copia sull'SSD, che resta un'azione dell'utente.

La fase 1.3 è compiuta: backup di `/home` in `C:\Users\Utente\Desktop\_backup-ubuntu-studio\`, 4,4 GB, verificato per numero di file e permessi. Le fasi 0 e 1 della procedura sono quindi chiuse.

La verifica del Machine Identifier di Akabak è compiuta: coincide con il valore conservato, la licenza è dichiarata valida, e questo chiude nella sostanza PA-005 e con essa la fase 0. È MS-052. Anche PA-009 è chiusa: l'SSD esterno è sano e la causa delle riparazioni del filesystem è la rimozione senza espulsione, non il supporto. È MS-058.

Della fase 2 sono compiute la 2.1 e la 2.2: l'immagine `ubuntustudio-26.04.1-desktop-amd64.iso` è in `C:\Users\Utente\Desktop\_iso-ubuntu-studio\`, verificata per somma di controllo e per firma, e accanto a essa c'è Rufus 4.15 portabile verificato per firma Authenticode. Da prendere è il point release 26.04.1 e non la 26.04 iniziale. Il prossimo passo è quindi la 2.3, cioè scrivere la chiavetta in modalità DD su un supporto da almeno 16 GB, e poi le fasi da 3 a 11. La sequenza completa delle azioni dell'utente, in ordine e con le dipendenze dichiarate, è in testa a `docs/PENDING-ACTIONS.md`. Attenzione: le fasi 7 e 8 sono state corrette il 2026-09-07 per ADR-016, perché Akabak è a 32 bit e non a 64: chi eseguisse una versione precedente della procedura otterrebbe un ambiente in cui il programma non parte.

Lo stato dell'accesso alla macchina: è raggiungibile e la chiave SSH dedicata è installata, quindi l'accesso funziona anche in modo non interattivo. Resta che `sudo` chiede la password, per scelta dell'utente, quindi il lavoro privilegiato si esegue a mano su comandi preparati. Attenzione alla sospensione automatica: la macchina si riaddormenta e scompare dalla rete, quindi conviene risvegliarla prima di ogni sessione di lavoro su di essa. Il suo indirizzo hardware è `2c:4d:54:53:a4:fb`, utile per il Wake-on-LAN e per una prenotazione dell'indirizzo sul router.
