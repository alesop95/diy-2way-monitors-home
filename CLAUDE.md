# diy-2way-monitors-home

> Istruzioni di progetto, versionate. Le preferenze personali vivono in `CLAUDE.local.md` (ignorato).

## Cos'è questo progetto

Progettazione e costruzione di una coppia di monitor da studio a due vie per un punto di ascolto domestico, con il flusso di lavoro interamente su Linux e i programmi Windows indispensabili sotto Wine. Non è un progetto software: il valore sta nella documentazione tecnica versionata e nella catena di decisioni motivate, non in codice applicativo, che non esiste.

L'impostazione che ne determina la forma è descritta in `README.md` e formalizzata come ADR-002: si progetta a partire dalla stanza, non dal diffusore.

## Da dove partire in una sessione nuova

Il primo comando non legge: verifica che ci si possa credere. Lo strumento `python tools/verifica-ripresa.py` confronta l'impronta registrata alla chiusura della sessione precedente, cioè commit e forma dell'albero di lavoro in quel momento, con lo stato reale di adesso, e dice che cosa una sessione caduta a metà non ha scritto. La procedura che ne interpreta l'esito è la skill `riprendi`, da invocare come primo atto di ogni sessione nuova. La ragione è che un file di ripresa non aggiornato ha esattamente lo stesso aspetto di uno aggiornato, e il danno non è perdere il lavoro, che sta su disco e in git, ma costruire sopra una fotografia vecchia senza accorgersene.

Fatta la verifica, leggere `.claude/memory/index.md`, che è lo snapshot di sincronizzazione e dice cosa è fatto e dove si riprende. Poi `.claude/context/current-work.md` per il fronte attivo e i blocchi. Il file di ripresa rapida è `_notes/RESUME-PROMPT.md`, ignorato da git, e non è una seconda fonte di verità: lo stato canonico resta lo snapshot.

L'ultimo atto di ogni sessione, dopo che l'utente ha fatto i propri commit e dopo aver aggiornato il file di ripresa, è registrare l'impronta con `python tools/verifica-ripresa.py --registra`. Registrarla prima dei commit produce un falso positivo alla riapertura, e un presidio che dà falsi positivi è un presidio che si impara a ignorare.

Poi lanciare `python tools/check-pending-actions.py`, che dice quali azioni differite sono diventate eseguibili. Serve perché alcune dipendono da condizioni esterne che cambiano fra una sessione e l'altra, per esempio un disco esterno collegato o no, e un promemoria che vive solo in una conversazione andrebbe perduto.

Il punto d'ingresso della documentazione tecnica è `docs/README.md`. Il registro cronologico degli interventi, con l'esito verificato di ciascuno, è `docs/OPERATIONS-LOG.md`, e ogni intervento nuovo vi aggiunge un microstep numerato con la propria verifica. Le azioni differite stanno in `docs/PENDING-ACTIONS.md`, e una voce compiuta non si cancella: si marca come compiuta con la data.

## Tracciamento integrale: tutto quello che passa in sessione finisce in documentazione

Istruzione vincolante dell'utente, non una preferenza. Tutto ciò che viene detto, deciso, scoperto, sbagliato o corretto durante una sessione va scritto nella documentazione di progetto, sempre e per intero, non riassunto nella risposta e lasciato lì. Una conversazione non è un supporto di memoria: si perde alla chiusura, non si versiona e non arriva a chi clona il repository.

La ripartizione fra i documenti è la seguente, e va rispettata perché ciascuno ha un lettore diverso. Un intervento tecnico, con il comando che lo ha verificato e il suo esito, diventa un microstep numerato in `docs/OPERATIONS-LOG.md`. Una decisione non ovvia diventa una voce in `.claude/memory/decisions.md`. Un impegno che dipende da una condizione esterna diventa una voce in `docs/PENDING-ACTIONS.md`. Una nozione tecnica che serve a capire, e non solo a sapere che è stata fatta, diventa prosa in una pagina di `docs/`. Il meta-stato di sessione va in `.claude/memory/progress.md`.

Dal 2026-09-17 la ripartizione porta un obbligo in più, dato dall'utente come istruzione vincolante e non come preferenza. Ogni fronte operativo, cioè ogni lavoro fatto di comandi eseguiti su una macchina, produce anche una pagina prescrittiva sotto `docs/` che è la sequenza replicabile con i soli comandi nell'ordine in cui vanno eseguiti, seguita da una sezione di troubleshooting dove ogni voce dichiara sintomo, causa e rimedio. Non è un riassunto dei microstep e non li sostituisce: i microstep raccontano che cosa è successo una volta, in ordine cronologico e con i ritiri, e chi deve rifare la stessa cosa fra sei mesi non può ricostruire una procedura leggendo un registro. La pagina prescrittiva risponde a chi esegue, il registro a chi vuole sapere perché.

La forma di riferimento è `docs/10-ambiente/veeam-agent-linux.md`, che porta entrambe le sezioni nella forma attesa. Le regole che le governano sono tre. Un comando che compare nella sequenza è stato eseguito davvero e il suo esito osservato, mai ricostruito a memoria o dedotto da un aiuto. Una voce di troubleshooting nasce da un caso incontrato e non da una previsione, e lo dichiara nominando la macchina e la data quando il caso è specifico. E la sequenza si scrive nel giro di lavoro in cui i comandi vengono eseguiti, non alla fine, per la stessa ragione per cui `chat-non-e-memoria.md` vieta l'aggiornamento differito.

Dal 2026-09-14 ogni microstep dichiara anche a quale fase del progetto serve e che cosa dipenda da esso, e lo dichiara apertamente anche quando non serve alcuna fase, perché un legame inventato è peggio di un legame assente. Per le voci precedenti il legame è fornito per blocchi in `docs/90-riferimenti/tracciabilita-microstep.md`, che è la forma additiva della correzione, dato che la convenzione del registro vieta di riscrivere una voce passata. La stessa convenzione porta ora l'indice delle voci superate, perché in un registro che cresce in avanti una voce smentita non sa di esserlo.

Tre casi che si è tentati di non scrivere e che invece vanno scritti sempre. Gli errori commessi, compresi quelli dell'agente, con la causa e la regola che ne discende: MS-014 e MS-027 sono di questo tipo. Le inferenze poi smentite, ritirate esplicitamente e non cancellate in silenzio, perché altrimenti il documento sembra essere sempre stato giusto e non si impara nulla: MS-024 è di questo tipo. E i comandi esatti eseguiti dall'utente con il loro output reale, quando l'output insegna qualcosa.

## Satelliti tracciati

Regole modulari sotto `.claude/rules/`: `interaction-style.md` e `chat-non-e-memoria.md` da caricare sempre, più `git-commands-format.md`, `git-identity-and-repo.md`, `manual-screenshots.md`, `prove-che-misurano.md`, `security-permissions.md`, `token-economy.md` e `web-sources-not-fetchable.md`. La penultima delle otto è arrivata qui il 2026-09-17 con il riallineamento di MS-129 e dice che una prova verde non è di per sé una misura: raccoglie i tre modi documentati in cui una prova passa senza misurare niente, e vale in questo progetto anche fuori dal codice, perché un controllo che esce zero mentre elenca file da correggere è la stessa vacuità osservata dentro una suite. La seconda delle due da caricare sempre è la forma modulare e generale della prescrizione sul tracciamento integrale scritta qui sopra: nasce da una direttiva data in questo progetto il 2026-09-09, è stata scritta nel template e istanziata qui il 2026-09-12, ed è il motivo per cui quella prescrizione ora vive in un file caricabile invece che nella sola prosa di questo indice.

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
python tools/check-copie-modelli.py
python tools/check-pending-actions.py
```

Il quintultimo comando fallisce se il blocco `docs/10-ambiente/` è stato modificato qui e non ancora propagato al progetto gemello `home-recording-training-mixing-setup`, di cui questo repository è la copia canonica.

Il penultimo è arrivato il 2026-09-17 e chiude un buco che non aveva alcun presidio. Ogni strumento condiviso esiste qui in due esemplari, cioè il modello sotto `.claude/templates/<pacchetto>/` e la copia sotto `tools/` che è quella che gira davvero, e nulla li teneva insieme: si corregge la copia perché è quella che si esegue, il modello resta indietro, e il difetto non si manifesta in questo repository ma nel prossimo progetto allineato, che riceve uno strumento privo di una protezione che la documentazione dichiara presente. Lo strumento confronta i due esemplari byte per byte e fallisce quando divergono, senza scegliere da sé il verso della riconciliazione, che è una decisione e non una copia. Accanto vive `python tools/check-catalogo.py`, che verifica che il catalogo dei pacchetti descriva le cartelle presenti sul disco e non quelle di ieri, e che non sta nella sequenza obbligatoria perché il catalogo qui è una copia e non la sorgente.

Il terzo comando, `check-eol.py`, cerca i file di testo che mescolano fini riga `CRLF` e `LF`, ed esiste perché nessun altro controllo può accorgersene: la convenzione Markdown prescrive di conservare la fine riga di ciascun file, quindi `md-unwrap` la rispetta e non ne pretende la coerenza interna, il rendering a video è identico e la catena tipografica guarda i caratteri e non le interruzioni. Non è un problema estetico: con `core.autocrlf` a `false` e senza `.gitattributes`, come in questo repository, git registra le fini riga così come stanno sul disco, quindi un file misto entra nella storia e alla prima riscrittura da parte di qualunque strumento trasforma una modifica di due righe in una modifica dell'intero file. Il difetto è stato introdotto per davvero il 2026-09-08 inserendo blocchi scritti con `LF` in due file `CRLF`, e al primo lancio lo strumento ne ha trovato un terzo che era già nella storia del repository. Il racconto è in MS-063.

La catena tipografica, cioè `fix-accents.py`, `fix-missing-accents.py` e `fix-dashes.py`, non entra in questa sequenza e non si lancia su `.`. Si esegue sui soli file Markdown, e la ragione è un difetto isolato in MS-014 del registro dei microstep: su un file di codice le regole di prudenza dei due strumenti sugli accenti sono incoerenti fra loro, e la catena dei due lascia un apostrofo orfano su forme come `c'e'`, producendo `c'è'`. Gli stessi strumenti terminano inoltre con un errore se ricevono un percorso su un'altra lettera di unità.

## Sviluppo e identità

git locale, identità `alesop95`, alias SSH `github-personal`, remoto `git@github-personal:alesop95/diy-2way-monitors-home.git` già collegato. Commit e push sono sempre manuali dell'utente, e vanno presentati nel formato della regola `git-commands-format.md`.

## Standard

Struttura standard `.claude/PROJECT-SYSTEM.md`, istanziata da `template-claude-developing` e riallineata il 2026-09-12, quando `PROJECT-SYSTEM.md` è tornato identico a quello del template, la regola `chat-non-e-memoria.md` è stata istanziata, due pacchetti di modelli mancanti sono stati portati qui e la catena tipografica è stata aggiornata alle versioni del template, che nel frattempo l'avevano superata. Il censimento e le sue conseguenze sono in MS-091.

Il riallineamento è stato ripetuto il 2026-09-17, perché in cinque giorni lo scarto si era riaperto: il verso discendente, cioè dal template ai progetti, non ha alcun automatismo e dipende da chi se ne ricorda, mentre il verso ascendente è un atto deliberato che si compie quando una cosa nasce quaggiù, e fra il 12 e il 17 settembre il secondo è stato percorso due volte e il primo nessuna. Sono arrivate qui la regola `prove-che-misurano.md`, l'eccezione sul grassetto in `interaction-style.md`, la sezione sul contesto di shell in `git-commands-format.md`, la sezione 9 di `PROJECT-SYSTEM.md`, i quattro strumenti tipografici con la guardia di PA-015 e il rientro corretto in `--check`, i due controlli nuovi e i sei pacchetti di modelli che mancavano. Il racconto è in MS-129.

Le due divergenze che andavano verso il template sono state portate là lo stesso 2026-09-17, cioè la negazione nel `.gitignore` sui modelli `_notes` e la quinta causa nella sezione sul contesto di shell di `git-commands-format.md`. Della prima va ritirata la motivazione che questo indice dava poche ore prima: non è vero che chi clona il template non riceva quei modelli, perché sono tracciati e un pattern del `.gitignore` non tocca ciò che è già nell'indice; la negazione previene il caso futuro e non ne ripara uno in corso, e la misura è in MS-130. Restano non committate nel template, che è su un ramo di lavoro, quindi la propagazione si chiuderà con una unione e non con un commit. In senso discendente è invece comparsa una voce nuova mentre lavoravo, cioè il quarto asse di identità della GitHub CLI, che qui richiede una re-istanziazione e non una copia: sta in PA-016. Verso questo progetto non resta nulla di misurato: `check-copie-modelli.py` riporta quattordici copie allineate e nessuna divergente, e `check-catalogo.py` nessun problema. La divergenza di stile nella skill `studio-didattico` è caduta da sé, perché il template ha risolto la stessa questione togliendo l'enfasi invece di convertirla in corsivo, e la sua copia qui è ora identica.

## Onestà del contenuto, che qui pesa più del solito

Buona parte della documentazione riguarda una macchina che non è quella su cui si apre la sessione, e che al momento della stesura non era raggiungibile in rete. Le pagine che descrivono stati non osservati lo dichiarano in apertura. Nessuna affermazione su quella macchina va promossa da ipotesi a fatto senza averla verificata con un comando eseguito su di essa. La lezione non è teorica: una pagina di diagnosi scritta per ipotesi è stata poi smentita in tre punti su quattro dalla misura, ed è stata rimossa. Il quadro reale è in `docs/10-ambiente/fotografia-macchina-2026-09-07.md`, e il record dell'errore in MS-029 del registro dei microstep.
