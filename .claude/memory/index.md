# Snapshot di sincronizzazione

> Da leggere per primo a inizio sessione. Fotografa lo stato del progetto al commit di riferimento e mappa ogni scheda al suo stato di verifica. È la fonte di verità su cosa è fatto.

## Stato

```
Branch attivo:          main
Commit di riferimento:  0df04bb7019814cf69b8458e4eaad8eaf71be818
Data snapshot:          2026-09-04
Modifiche non committate: sì, l'intero lavoro della sessione del 2026-09-04
```

Il commit di riferimento è precedente al lavoro di questa sessione, perché commit e push restano operazioni manuali dell'utente. Alla prima sessione successiva al commit, i campi `last-verified-commit` delle schede vanno aggiornati al nuovo hash.

## Che cos'è questo progetto, in tre righe

Progettazione e costruzione di una coppia di monitor da studio a due vie per un punto di ascolto domestico noto e non trattabile acusticamente. Il flusso di progettazione gira su una macchina Ubuntu Studio, con i programmi Windows indispensabili sotto Wine. Il punto d'ingresso della documentazione è `docs/README.md`; la direzione del progetto è in `.claude/context/roadmap.md`.

## Stato di verifica delle schede

| Scheda | last-verified | Stato |
|---|---|---|
| STACK.md | 0df04bb | aggiornata, scritta in questa sessione |
| roadmap.md | 0df04bb | aggiornata, scritta in questa sessione |
| current-work.md | 0df04bb | aggiornata, scritta in questa sessione |
| design-and-security.md | - | non creata: il progetto non ha codice applicativo né superficie di attacco |
| deployment.md | - | non creata: non c'è deploy; il suo equivalente è `docs/TRANSFER-MANIFEST.md` |
| dev-testing.md | - | non creata: i test sono le suite degli strumenti, descritte in STACK.md |

Le tre schede non create sono una decisione, non una dimenticanza: il sistema di progetto prescrive di adottare la forma minima ed estenderla solo quando la complessità lo richiede.

## Documenti da non confondere

Il registro dei microstep, con l'esito verificato di ogni intervento, è `docs/OPERATIONS-LOG.md`. Il work-log di sessione è `.claude/memory/progress.md`. Il primo è il livello tecnico-didattico rivolto a chi legge il progetto, il secondo è il livello di meta-stato rivolto a chi lo riprende.

## Punto di ripresa

Committare il lavoro della sessione del 2026-09-04, poi raggiungere la macchina Ubuntu Studio ed eseguire la sequenza di verifica in sola lettura di `docs/10-ambiente/ubuntu-lts-upgrade.md` per confermare o smentire la diagnosi del blocco di aggiornamento.
