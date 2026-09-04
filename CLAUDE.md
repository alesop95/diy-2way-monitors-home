# diy-2way-monitors-home

> Istruzioni di progetto, versionate. Le preferenze personali vivono in `CLAUDE.local.md` (ignorato).

## Cos'è questo progetto

Progettazione e costruzione di una coppia di monitor da studio a due vie per un punto di ascolto domestico, con il flusso di lavoro interamente su Linux e i programmi Windows indispensabili sotto Wine. Non è un progetto software: il valore sta nella documentazione tecnica versionata e nella catena di decisioni motivate, non in codice applicativo, che non esiste.

L'impostazione che ne determina la forma è descritta in `README.md` e formalizzata come ADR-002: si progetta a partire dalla stanza, non dal diffusore.

## Da dove partire in una sessione nuova

Leggere `.claude/memory/index.md` per primo, che è lo snapshot di sincronizzazione e dice cosa è fatto e dove si riprende. Poi `.claude/context/current-work.md` per il fronte attivo e i blocchi.

Il punto d'ingresso della documentazione tecnica è `docs/README.md`. Il registro cronologico degli interventi, con l'esito verificato di ciascuno, è `docs/OPERATIONS-LOG.md`, e ogni intervento nuovo vi aggiunge un microstep numerato con la propria verifica.

## Satelliti tracciati

Regole modulari sotto `.claude/rules/`: `interaction-style.md` da caricare sempre, più `git-commands-format.md`, `git-identity-and-repo.md`, `manual-screenshots.md`, `security-permissions.md`, `token-economy.md` e `web-sources-not-fetchable.md`.

Schede tecniche sotto `.claude/context/`: `STACK.md` per la catena di strumenti e gli script di manutenzione, `roadmap.md` per la direzione e le priorità, `current-work.md` per il fronte attivo.

Meta-stato sotto `.claude/memory/`: `index.md`, `progress.md`, `decisions.md`.

## Materiali e dati

Il materiale scritto a mano vive alla radice come file di testo ed è escluso dal versionamento da pattern ancorati alla radice nel `.gitignore`. I materiali pesanti, cioè installer e pacchetto di esempi, stanno in `Akabak + VACS/`, esclusa per nome, e il documento sorgente della documentazione è archiviato sotto `_notes/`, anch'esso ignorato.

Attenzione a una trappola già scattata una volta: i pattern per tipo di file nel `.gitignore` sono ancorati alla radice di proposito. Se qualcuno li rende globali, tornano a nascondere gli strumenti sotto `tools/` e i modelli sotto `.claude/templates/`, che devono essere versionati.

## Verifica prima di un commit

Tutta non distruttiva, e va eseguita per intera.

```bash
python tools/md-unwrap.py --check .
python tools/lint-md-commands.py .
python tools/test-tipografia.py
python tools/sync-ambiente.py --check
```

L'ultimo comando fallisce se il blocco `docs/10-ambiente/` è stato modificato qui e non ancora propagato al progetto gemello `home-recording-training-mixing-setup`, di cui questo repository è la copia canonica.

La catena tipografica, cioè `fix-accents.py`, `fix-missing-accents.py` e `fix-dashes.py`, non entra in questa sequenza e non si lancia su `.`. Si esegue sui soli file Markdown, e la ragione è un difetto isolato in MS-014 del registro dei microstep: su un file di codice le regole di prudenza dei due strumenti sugli accenti sono incoerenti fra loro, e la catena dei due lascia un apostrofo orfano su forme come `c'e'`, producendo `c'è'`. Gli stessi strumenti terminano inoltre con un errore se ricevono un percorso su un'altra lettera di unità.

## Sviluppo e identità

git locale, identità `alesop95`, alias SSH `github-personal`, remoto `git@github-personal:alesop95/diy-2way-monitors-home.git` già collegato. Commit e push sono sempre manuali dell'utente, e vanno presentati nel formato della regola `git-commands-format.md`.

## Standard

Struttura standard `.claude/PROJECT-SYSTEM.md`, istanziata da `template-claude-developing`. Due divergenze da quel template sono volute e annotate nei file stessi: la negazione nel `.gitignore` che rende versionabili i modelli `_notes` sotto `.claude/templates/`, e l'uso delle versioni più recenti degli strumenti tipografici, che nel template vivono in `tools/` alla radice e non nel pacchetto di istanziazione. Entrambe sono da propagare all'indietro al template.

## Onestà del contenuto, che qui pesa più del solito

Buona parte della documentazione riguarda una macchina che non è quella su cui si apre la sessione, e che al momento della stesura non era raggiungibile in rete. Le pagine che descrivono stati non osservati lo dichiarano in apertura. Nessuna affermazione su quella macchina va promossa da ipotesi a fatto senza averla verificata con un comando eseguito su di essa, e la pagina `docs/10-ambiente/ubuntu-lts-upgrade.md` contiene la sequenza di verifica proprio per questo.
