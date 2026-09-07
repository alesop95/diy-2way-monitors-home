# Snapshot di sincronizzazione

> Da leggere per primo a inizio sessione. Fotografa lo stato del progetto al commit di riferimento e mappa ogni scheda al suo stato di verifica. È la fonte di verità su cosa è fatto.

## Stato

```
Branch attivo:          main
Commit di riferimento:  3eac5f3
Data snapshot:          2026-09-07
Modifiche non committate: sì, la sessione del 2026-09-07
```

Due commit del 2026-09-04 sono su origin: `9e9517e` con l'allineamento al template, la conversione del documento sorgente e l'impianto dell'ambiente documentale, e `3eac5f3` con l'approfondimento su Wine, la procedura di installazione pulita, lo storico di Akabak e VACS e il piano del corredo software. Il lavoro del 2026-09-07, cioè la verifica delle copie del corredo e le quattro voci da MS-024 a MS-027, non è ancora committato. Commit e push restano operazioni manuali dell'utente.

## Che cos'è questo progetto, in tre righe

Progettazione e costruzione di una coppia di monitor da studio a due vie per un punto di ascolto domestico noto e non trattabile acusticamente. Il flusso di progettazione gira su una macchina Ubuntu Studio, con i programmi Windows indispensabili sotto Wine. Il punto d'ingresso della documentazione è `docs/README.md`; la direzione del progetto è in `.claude/context/roadmap.md`.

## Stato di verifica delle schede

| Scheda | last-verified | Stato |
|---|---|---|
| STACK.md | 3eac5f3 | aggiornata |
| roadmap.md | 3eac5f3 | aggiornata |
| current-work.md | 3eac5f3 | aggiornata |
| design-and-security.md | - | non creata: il progetto non ha codice applicativo né superficie di attacco |
| deployment.md | - | non creata: non c'è deploy; il suo equivalente è `docs/TRANSFER-MANIFEST.md` |
| dev-testing.md | - | non creata: i test sono le suite degli strumenti, descritte in STACK.md |

Le tre schede non create sono una decisione, non una dimenticanza: il sistema di progetto prescrive di adottare la forma minima ed estenderla solo quando la complessità lo richiede.

## Documenti da non confondere

Il registro dei microstep, con l'esito verificato di ogni intervento, è `docs/OPERATIONS-LOG.md`. Il work-log di sessione è `.claude/memory/progress.md`. Il primo è il livello tecnico-didattico rivolto a chi legge il progetto, il secondo è il livello di meta-stato rivolto a chi lo riprende. Le azioni differite, con le condizioni che le sbloccano, stanno in `docs/PENDING-ACTIONS.md`, e sono cosa diversa da entrambi: non sono lavoro fatto né stato del progetto, ma impegni con una condizione esterna.

## Punto di ripresa

Installare la chiave SSH dedicata sulla macchina Ubuntu Studio secondo la fase 10.3 di `docs/10-ambiente/installazione-pulita-26-04.md`, passaggio che richiede la password una volta sola ed è dell'utente. La chiave `id_ed25519_studio` è già stata generata il 2026-09-07 e non va rigenerata; manca il solo comando che la installa sulla macchina, e in PowerShell non è `ssh-copy-id`, che in quella shell non esiste. Subito dopo, eseguire la fase 0 della stessa procedura: la fotografia completa della macchina in quattordici file, che è il prerequisito di tutto il resto e che conferma o smentisce la diagnosi del blocco di aggiornamento.

Lo stato dell'accesso alla macchina, aggiornato: è sveglia e raggiungibile, `sshd` risponde, l'autenticazione non è ancora configurata. Attenzione alla sospensione automatica: la macchina si riaddormenta e scompare dalla rete, quindi conviene risvegliarla prima di ogni sessione di lavoro su di essa. Il suo indirizzo hardware è `2c:4d:54:53:a4:fb`, utile per il Wake-on-LAN e per una prenotazione dell'indirizzo sul router.
