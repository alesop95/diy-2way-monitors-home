# diy-2way-monitors-home

> Istruzioni di progetto, versionate. Le preferenze personali vivono in `CLAUDE.local.md` (ignorato).

## Cos'è questo progetto

Progettazione e costruzione di una coppia di monitor da studio a due vie per un punto di ascolto domestico, con il flusso di lavoro interamente su Linux e i programmi Windows indispensabili sotto Wine. Non è un progetto software: il valore sta nella documentazione tecnica versionata e nella catena di decisioni motivate, non in codice applicativo, che non esiste.

L'impostazione che ne determina la forma è descritta in `README.md` e formalizzata come ADR-002: si progetta a partire dalla stanza, non dal diffusore.

## Da dove partire in una sessione nuova

Leggere `.claude/memory/index.md` per primo, che è lo snapshot di sincronizzazione e dice cosa è fatto e dove si riprende. Poi `.claude/context/current-work.md` per il fronte attivo e i blocchi.

Poi lanciare `python tools/check-pending-actions.py`, che dice quali azioni differite sono diventate eseguibili. Serve perché alcune dipendono da condizioni esterne che cambiano fra una sessione e l'altra, per esempio un disco esterno collegato o no, e un promemoria che vive solo in una conversazione andrebbe perduto.

Il punto d'ingresso della documentazione tecnica è `docs/README.md`. Il registro cronologico degli interventi, con l'esito verificato di ciascuno, è `docs/OPERATIONS-LOG.md`, e ogni intervento nuovo vi aggiunge un microstep numerato con la propria verifica. Le azioni differite stanno in `docs/PENDING-ACTIONS.md`, e una voce compiuta non si cancella: si marca come compiuta con la data.

## Tracciamento integrale: tutto quello che passa in sessione finisce in documentazione

Istruzione vincolante dell'utente, non una preferenza. Tutto ciò che viene detto, deciso, scoperto, sbagliato o corretto durante una sessione va scritto nella documentazione di progetto, sempre e per intero, non riassunto nella risposta e lasciato lì. Una conversazione non è un supporto di memoria: si perde alla chiusura, non si versiona e non arriva a chi clona il repository.

La ripartizione fra i documenti è la seguente, e va rispettata perché ciascuno ha un lettore diverso. Un intervento tecnico, con il comando che lo ha verificato e il suo esito, diventa un microstep numerato in `docs/OPERATIONS-LOG.md`. Una decisione non ovvia diventa una voce in `.claude/memory/decisions.md`. Un impegno che dipende da una condizione esterna diventa una voce in `docs/PENDING-ACTIONS.md`. Una nozione tecnica che serve a capire, e non solo a sapere che è stata fatta, diventa prosa in una pagina di `docs/`. Il meta-stato di sessione va in `.claude/memory/progress.md`.

Tre casi che si è tentati di non scrivere e che invece vanno scritti sempre. Gli errori commessi, compresi quelli dell'agente, con la causa e la regola che ne discende: MS-014 e MS-027 sono di questo tipo. Le inferenze poi smentite, ritirate esplicitamente e non cancellate in silenzio, perché altrimenti il documento sembra essere sempre stato giusto e non si impara nulla: MS-024 è di questo tipo. E i comandi esatti eseguiti dall'utente con il loro output reale, quando l'output insegna qualcosa.

## Satelliti tracciati

Regole modulari sotto `.claude/rules/`: `interaction-style.md` da caricare sempre, più `git-commands-format.md`, `git-identity-and-repo.md`, `manual-screenshots.md`, `security-permissions.md`, `token-economy.md` e `web-sources-not-fetchable.md`.

Schede tecniche sotto `.claude/context/`: `STACK.md` per la catena di strumenti e gli script di manutenzione, `roadmap.md` per la direzione e le priorità, `current-work.md` per il fronte attivo.

Meta-stato sotto `.claude/memory/`: `index.md`, `progress.md`, `decisions.md`.

Livello documentale didattico sotto `.claude/context/`, adottato il 2026-09-09 su richiesta esplicita e non per default: `studio-didattico-master.md` è il punto d'ingresso, un racconto evolutivo che cresce per voci numerate e non si riscrive, e per ogni voce esiste un approfondimento `refactor-NN-<slug>.md` che entra nel codice e negli output reali. Risponde a una domanda che gli altri livelli non coprono, cioè perché una certa forma di fare le cose era fragile e perché quella che l'ha sostituita è migliore. Le schede di stato restano la fonte su che cosa è vero oggi, e questo livello non le sostituisce: chi clona il progetto deve poter rispondere da `STACK.md` senza leggere il racconto. La procedura è nella skill `.claude/skills/studio-didattico/`.

## Materiali e dati

Il materiale scritto a mano vive alla radice come file di testo ed è escluso dal versionamento da pattern ancorati alla radice nel `.gitignore`. I materiali pesanti, cioè installer e pacchetto di esempi, stanno in `Akabak + VACS/`, esclusa per nome, e il documento sorgente della documentazione è archiviato sotto `_notes/`, anch'esso ignorato.

Attenzione a una trappola già scattata una volta: i pattern per tipo di file nel `.gitignore` sono ancorati alla radice di proposito. Se qualcuno li rende globali, tornano a nascondere gli strumenti sotto `tools/` e i modelli sotto `.claude/templates/`, che devono essere versionati.

## Verifica prima di un commit

Tutta non distruttiva, e va eseguita per intera.

```bash
python tools/md-unwrap.py --check .
python tools/lint-md-commands.py .
python tools/check-eol.py .
python tools/test-tipografia.py
python tools/sync-ambiente.py --check
python tools/check-pending-actions.py
```

Il penultimo comando fallisce se il blocco `docs/10-ambiente/` è stato modificato qui e non ancora propagato al progetto gemello `home-recording-training-mixing-setup`, di cui questo repository è la copia canonica.

Il terzo comando, `check-eol.py`, cerca i file di testo che mescolano fini riga `CRLF` e `LF`, ed esiste perché nessun altro controllo può accorgersene: la convenzione Markdown prescrive di conservare la fine riga di ciascun file, quindi `md-unwrap` la rispetta e non ne pretende la coerenza interna, il rendering a video è identico e la catena tipografica guarda i caratteri e non le interruzioni. Non è un problema estetico: con `core.autocrlf` a `false` e senza `.gitattributes`, come in questo repository, git registra le fini riga così come stanno sul disco, quindi un file misto entra nella storia e alla prima riscrittura da parte di qualunque strumento trasforma una modifica di due righe in una modifica dell'intero file. Il difetto è stato introdotto per davvero il 2026-09-08 inserendo blocchi scritti con `LF` in due file `CRLF`, e al primo lancio lo strumento ne ha trovato un terzo che era già nella storia del repository. Il racconto è in MS-063.

La catena tipografica, cioè `fix-accents.py`, `fix-missing-accents.py` e `fix-dashes.py`, non entra in questa sequenza e non si lancia su `.`. Si esegue sui soli file Markdown, e la ragione è un difetto isolato in MS-014 del registro dei microstep: su un file di codice le regole di prudenza dei due strumenti sugli accenti sono incoerenti fra loro, e la catena dei due lascia un apostrofo orfano su forme come `c'e'`, producendo `c'è'`. Gli stessi strumenti terminano inoltre con un errore se ricevono un percorso su un'altra lettera di unità.

## Sviluppo e identità

git locale, identità `alesop95`, alias SSH `github-personal`, remoto `git@github-personal:alesop95/diy-2way-monitors-home.git` già collegato. Commit e push sono sempre manuali dell'utente, e vanno presentati nel formato della regola `git-commands-format.md`.

## Standard

Struttura standard `.claude/PROJECT-SYSTEM.md`, istanziata da `template-claude-developing`. Due divergenze da quel template sono volute e annotate nei file stessi: la negazione nel `.gitignore` che rende versionabili i modelli `_notes` sotto `.claude/templates/`, e l'uso delle versioni più recenti degli strumenti tipografici, che nel template vivono in `tools/` alla radice e non nel pacchetto di istanziazione. Entrambe sono da propagare all'indietro al template.

## Onestà del contenuto, che qui pesa più del solito

Buona parte della documentazione riguarda una macchina che non è quella su cui si apre la sessione, e che al momento della stesura non era raggiungibile in rete. Le pagine che descrivono stati non osservati lo dichiarano in apertura. Nessuna affermazione su quella macchina va promossa da ipotesi a fatto senza averla verificata con un comando eseguito su di essa. La lezione non è teorica: una pagina di diagnosi scritta per ipotesi è stata poi smentita in tre punti su quattro dalla misura, ed è stata rimossa. Il quadro reale è in `docs/10-ambiente/fotografia-macchina-2026-09-07.md`, e il record dell'errore in MS-029 del registro dei microstep.
