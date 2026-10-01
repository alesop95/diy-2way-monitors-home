---
generated-from-commit: 018966796aa08832fe7845387e5e5d28e2448639
generated-from-branch: main
generated-date: 2026-09-30
covers-paths:
  - .claude/context/deployment.md
  - docs/10-ambiente/veeam-agent-linux.md
last-verified-commit: 93bb1e1
---

# Deployment

> Questo progetto non ha codice applicativo né un rilascio: la scheda esiste dal 2026-09-30 per la sola sezione del modello di separazione, chiesta dal gate dell'inizializzazione. Fino a quella data era dichiarata non creata per scelta, e il suo equivalente per il trasferimento dei materiali resta `docs/TRANSFER-MANIFEST.md`. Commit e push restano operazioni manuali dell'utente.

## Modello di separazione fra test e produzione

> Scelto al gate del 2026-09-30 fra i modelli del catalogo `.claude/skills/separazione-ambienti/RIFERIMENTO.md`, registrato come ADR-024 in `memory/decisions.md`. La spiegazione di ciascuna forma sta in `docs/separazione-ambienti/GUIDA.md`, con le fonti in `docs/separazione-ambienti/FONTI.md`.

- Modello: R0, P1 senza richiesta di modifica, D non applicabile, L1.
- Stato: in esercizio. L'unico ambiente è la macchina Ubuntu Studio raggiungibile come `ssh studio`, con i programmi di terzi sotto Wine; non esiste un ambiente di prova, né previsto né creato.
- Scelto il: 2026-09-30, ADR: ADR-024.
- Perché questo e non gli altri: non c'è codice proprio da provare. Sulla macchina si installano soltanto programmi di terzi, e il solo cambiamento è la loro installazione o l'aggiornamento del sistema, che si copre con un punto di ripristino preso prima. Nel repository ci sono soltanto documentazione, memoria e script di manutenzione, e i commit dell'utente vanno direttamente su `main`: è P1 con tutti i percorsi dichiarati diretti sulla branch principale.
- Rischi da presidiare. Il primo è il backup che resta un proposito, cioè il modo in cui R0 fallisce secondo la guida [C8]: qui i punti di ripristino sono presi a mano e non pianificati, e l'utente ha dichiarato il 2026-09-30 che basta così, con un punto preso prima di ogni cambio rischioso alla macchina. La dichiarazione sta fra le asserzioni umane di `data/scadenze.json`, che la ripropone come domanda alla scadenza della sua validità. Il secondo è provare dentro la produzione. È accaduto il 2026-09-17 con il passaggio ai pacchetti di WineHQ, eseguito sulla macchina vera e riportato indietro da un archivio dei prefix preso prima (MS-137 a MS-142). Il presidio è la stessa regola: prima di un cambio all'ambiente Wine o al sistema si prende un archivio o un punto Veeam, con i limiti di ripristino dichiarati nella sezione dei comandi qui sotto. Il terzo è la destinazione provvisoria dei punti di ripristino, che è una voce di `data/scadenze.json`.

## Livelli

Un solo livello, la macchina di lavoro. Non c'è hosting, dominio né rilascio.

## Comandi

Il punto di ripristino si prende e si rilegge con la sequenza di `docs/10-ambiente/veeam-agent-linux.md`, che è la pagina prescrittiva con i soli comandi eseguiti davvero e il troubleshooting: la fase 6 rilegge l'archivio montandolo e confrontando impronte e conteggi. La pagina non documenta il ritorno della macchina a un punto, perché non è mai stato eseguito, e un backup a livello di file non dà un'immagine avviabile. Il solo ritorno eseguito davvero è quello dei tre prefix Wine da un archivio, il 2026-09-17 in MS-142. Per un modello R0, dove la rete di sicurezza è il ripristino, è la lacuna principale, ed è dichiarata qui invece di essere data per coperta.

## Variabili d'ambiente e segreti

Nessuna variabile d'ambiente di progetto e nessun `.env`. I dati di licenza di Akabak stanno fuori dal repository per ADR-017.
