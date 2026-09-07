# Snapshot di sincronizzazione

> Da leggere per primo a inizio sessione. Fotografa lo stato del progetto al commit di riferimento e mappa ogni scheda al suo stato di verifica. È la fonte di verità su cosa è fatto.

## Stato

```
Branch attivo:          main
Commit di riferimento:  f85480d
Data snapshot:          2026-09-07
Modifiche non committate: sì, la coda della sessione del 2026-09-07 su SSD e privilegi
```

Quattro commit sono su origin, gli ultimi due del 2026-09-07: `4863804` con la verifica delle copie del corredo e `f85480d` con la fase 0 eseguita e la diagnosi corretta. I due precedenti, del 2026-09-04, sono: `9e9517e` con l'allineamento al template, la conversione del documento sorgente e l'impianto dell'ambiente documentale, e `3eac5f3` con l'approfondimento su Wine, la procedura di installazione pulita, lo storico di Akabak e VACS e il piano del corredo software. Il lavoro del 2026-09-07, cioè la verifica delle copie del corredo e le quattro voci da MS-024 a MS-027, non è ancora committato. Commit e push restano operazioni manuali dell'utente.

## Che cos'è questo progetto, in tre righe

Progettazione e costruzione di una coppia di monitor da studio a due vie per un punto di ascolto domestico noto e non trattabile acusticamente. Il flusso di progettazione gira su una macchina Ubuntu Studio, con i programmi Windows indispensabili sotto Wine. Il punto d'ingresso della documentazione è `docs/README.md`; la direzione del progetto è in `.claude/context/roadmap.md`.

## Stato di verifica delle schede

| Scheda | last-verified | Stato |
|---|---|---|
| STACK.md | f85480d | aggiornata |
| roadmap.md | f85480d | da rileggere: la fase 0 ha cambiato le priorità |
| current-work.md | f85480d | aggiornata |
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

Il prossimo passo è la fase 1.3, cioè la copia di sicurezza di `/home` fuori dalla macchina, che è l'unico presidio contro l'errore umano nella selezione delle partizioni. Serve una destinazione: un disco esterno collegato alla macchina. Subito dopo, la verifica del Machine Identifier di Akabak, che va fatta prima di azzerare perché dopo non sarebbe più confrontabile, e poi le fasi da 2 a 11. Subito dopo, eseguire la fase 0 della stessa procedura: la fotografia completa della macchina in quattordici file, che è il prerequisito di tutto il resto e che conferma o smentisce la diagnosi del blocco di aggiornamento.

Lo stato dell'accesso alla macchina, aggiornato: è sveglia e raggiungibile, `sshd` risponde, l'autenticazione non è ancora configurata. Attenzione alla sospensione automatica: la macchina si riaddormenta e scompare dalla rete, quindi conviene risvegliarla prima di ogni sessione di lavoro su di essa. Il suo indirizzo hardware è `2c:4d:54:53:a4:fb`, utile per il Wake-on-LAN e per una prenotazione dell'indirizzo sul router.
