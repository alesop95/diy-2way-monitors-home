# Snapshot di sincronizzazione

> Da leggere per primo a inizio sessione. Fotografa lo stato del progetto al commit di riferimento e mappa ogni scheda al suo stato di verifica. È la fonte di verità su cosa è fatto.

## Stato

```
Branch attivo:          main
Commit di riferimento:  cadf335
Data snapshot:          2026-09-08
Modifiche non committate: sì, la coda della ripresa dal crash del 2026-09-08
```

Il repository conta 24 commit e origin è in pari fino a `cadf335`, verificato con `git rev-list --left-right --count origin/main...HEAD` che ha risposto zero e zero. I tre più recenti, tutti del 2026-09-08, sono `d2905ba` con il Machine Identifier confermato e la ripulitura delle informazioni superate, `351252d` con PA-007 chiusa e il controllo nuovo sulle fini riga, e `cadf335` con la fase 2 chiusa, cioè la chiavetta scritta e la verifica corretta nella sottofase 2.4. Prima di essi `1b4e801` porta la sequenza operativa e le verifiche dell'immagine di installazione. I due del 2026-09-04 che hanno impiantato il progetto sono `9e9517e`, con l'allineamento al template e la conversione del documento sorgente, e `3eac5f3`, con l'approfondimento su Wine, la procedura di installazione pulita e lo storico di Akabak e VACS. Commit e push restano operazioni manuali dell'utente.

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

**La fase 2 è chiusa per intero.** L'immagine `ubuntustudio-26.04.1-desktop-amd64.iso` è in `C:\Users\Utente\Desktop\_iso-ubuntu-studio\`, verificata per somma di controllo e per firma, con Rufus 4.15 portabile verificato per firma Authenticode; da prendere è il point release 26.04.1 e non la 26.04 iniziale. La chiavetta è scritta in modalità DD, in otto minuti e sette secondi, e la sua struttura a tre partizioni in tabella GPT è la conferma leggibile a occhio che la modalità DD è stata usata. La verifica della chiavetta è quella che il supporto fa su se stesso dal proprio menu di avvio, alla voce `Check disc for defects`, e non un confronto di impronte: su Windows quel confronto genera falsi allarmi perché il sistema monta i volumi da sé e ripara la tabella delle partizioni, e la smentita è in MS-069.

Il supporto è quindi pronto e il prossimo passo è l'installazione, cioè le fasi da 3 a 11. Accanto alla macchina si porta la scheda stampata, la cui sorgente è `docs/10-ambiente/scheda-reinstallazione.md` e il cui `.docx` si genera con `python tools/make-scheda-docx.py`, per ADR-017. La scheda porta l'avvertenza che conta e che la sola prescrizione di non formattare `/home` non trasmette: la casella di formattazione si attiva da sé quando si seleziona un filesystem nel menu della riga, quindi su `nvme0n1p4` il menu del filesystem non si tocca affatto, e il controllo che decide è la schermata di riepilogo, dove una formattazione deve comparire soltanto per `nvme0n1p2`. La sequenza completa delle azioni dell'utente, in ordine e con le dipendenze dichiarate, è in testa a `docs/PENDING-ACTIONS.md`. Attenzione: le fasi 7 e 8 sono state corrette il 2026-09-07 per ADR-016, perché Akabak è a 32 bit e non a 64: chi eseguisse una versione precedente della procedura otterrebbe un ambiente in cui il programma non parte.

Lo stato dell'accesso alla macchina: è raggiungibile e la chiave SSH dedicata è installata, quindi l'accesso funziona anche in modo non interattivo. Resta che `sudo` chiede la password, per scelta dell'utente, quindi il lavoro privilegiato si esegue a mano su comandi preparati. Attenzione alla sospensione automatica: la macchina si riaddormenta e scompare dalla rete, quindi conviene risvegliarla prima di ogni sessione di lavoro su di essa. Il suo indirizzo hardware è `2c:4d:54:53:a4:fb`, utile per il Wake-on-LAN e per una prenotazione dell'indirizzo sul router.
