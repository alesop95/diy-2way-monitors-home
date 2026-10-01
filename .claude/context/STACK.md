---
generated-from-commit: 0df04bb7019814cf69b8458e4eaad8eaf71be818
generated-from-branch: main
generated-date: 2026-09-04
covers-paths:
  - tools/**
  - docs/**
last-verified-commit: 93bb1e1
---

# Stack del progetto

> Documento di recupero: un collega che clona questo repository deve capire da qui con che cosa si lavora e perché. Questo progetto non ha codice applicativo, quindi lo stack non è un insieme di librerie ma la catena di strumenti di progettazione più gli script di manutenzione della documentazione.

## Che tipo di progetto è

È un progetto di ingegneria elettroacustica documentato, non un progetto software. Il repository contiene documentazione tecnica versionata sotto `docs/`, gli strumenti di verifica e manutenzione sotto `tools/`, e il sistema di contesto dell'agente sotto `.claude/`. I materiali binari, cioè installer e pacchetti di esempio, sono deliberatamente fuori dal versionamento e vivono sulla macchina di lavoro.

Ne segue una conseguenza sulla lettura del repository: il valore non sta nel codice ma nella catena di decisioni documentate, e il punto d'ingresso è `docs/README.md`.

## Catena di strumenti di progettazione

La catena vive sulla macchina Ubuntu Studio descritta in `docs/10-ambiente/README.md`, non su questa postazione. La regola di composizione è nativo Linux dove possibile, Wine dove non esiste alternativa seria.

Nativi: REW per la misura acustica, Blender per la geometria della stanza, GNU Octave con il toolbox MATAA per l'analisi modale e il calcolo dei tempi di riverberazione, FreeCAD per la progettazione meccanica del cabinet.

Sotto Wine, ciascuno nel proprio prefix, con l'architettura che ADR-016 ha corretto il 2026-09-07 e che non è uniforme: Akabak 3 per la simulazione mista elettroacustica e ambientale e VACS come suo strumento di visualizzazione, entrambi in un prefix a *32 bit* e senza alcuna dipendenza installata, e a 64 bit VituixCAD 2 per crossover e direttività, EASE Focus 3.1.260 con il servizio di database AFMG per la verifica di copertura, e ARTA 1.7.1 per produrre un file GLL da un diffusore misurato, con un limite da conoscere: è shareware e la modalità dimostrativa è pienamente funzionante tranne caricamento e salvataggio dei file, quindi quel ruolo non è esercitabile senza licenza e la decisione è tracciata come PA-014. La mappa completa dei prefix con le dipendenze di ciascuno è in `docs/10-ambiente/wine-corredo-progetto-stanza.md`.

WinISD è disponibile ma deliberatamente non installato. Ramsete 27b è sospeso in attesa della verifica del suo stato di licenza. L'affermazione precedente di questa scheda, secondo cui sarebbe il solo a richiedere un prefix a 32 bit per ADR-009, è ritirata: ADR-016 ha stabilito che Akabak e VACS sono a 32 bit, quindi l'architettura `i386` va dichiarata sul sistema in ogni caso e non è una eccezione di un solo programma.

L'hardware di misura non è deciso. Le versioni precedenti di questa scheda dichiaravano come fatto che fosse una Focusrite Scarlett 2i2 di seconda generazione con alimentazione phantom: l'affermazione è ritirata in MS-079, perché derivava da un segnalibro e non da un inventario, e l'utente ha confermato di possedere quella interfaccia ma di non impiegarla qui. Il requisito è un ingresso microfonico con alimentazione phantom e una qualità di conversione nota, più un microfono di misura calibrato individualmente, entrambi da acquisire. La valutazione dell'interfaccia è condivisa con il progetto gemello di home recording, con due vincoli fissati dall'utente: deve funzionare come dispositivo di classe audio senza driver proprietari, e deve reggere anche le misure della fase 8.

## Alternative deliberatamente escluse

Otto voci del corredo software con protezione rimossa o provenienza non lecita, per circa 1,7 GB. Escluse per ADR-010, e la ragione che regge da sola è che nessuna serve al progetto: la motivazione voce per voce, con la sostituzione nativa o gratuita che ne copre il ruolo, è in `docs/10-ambiente/wine-corredo-progetto-stanza.md`.

Una macchina virtuale Windows invece di Wine. Esclusa per tre motivi documentati in `docs/10-ambiente/wine-vs-emulatore.md`: la latenza aggiuntiva sulla catena audio proprio nella fase in cui si misura il tempo, l'identificativo hardware virtuale che invaliderebbe la licenza di Akabak, e il costo di licenza e manutenzione di un sistema ospite.

Pachyderm per l'acustica architettonica. Escluso perché richiede Rhinoceros e Grasshopper, che non girano nativamente su Linux.

EASE JR, che per l'ottimizzazione di monitor in una stanza domestica sarebbe superiore a EASE Focus 3 perché restituisce anche il comportamento ambientale. Escluso perché a pagamento; il suo ruolo è coperto da Akabak, che è gratuito per uso privato e fa elettroacustica e acustica ambientale in un solo passaggio.

EASE Address 2.1. Escluso perché lavora in due dimensioni sulla vista laterale e non gestisce geometrie complesse né riflessioni multiple, mentre la stanza del progetto è irregolare con soffitto spiovente.

WinISD. Non escluso in assoluto ma non installato, perché ridondante rispetto a VituixCAD e Akabak, e perché è il solo programma che richiederebbe un prefix Wine a 32 bit con la classe di problemi che ne deriva.

## Strumenti di manutenzione nel repository

Gli script sotto `tools/` sono istanziati dai pacchetti del template e servono a far rispettare meccanicamente le convenzioni invece di affidarle alla memoria.

Il file `tools/md-unwrap.py` attua la convenzione della riga sorgente unica per paragrafo, unendo le righe di continuazione senza normalizzare nient'altro, e rifiuta di scrivere un file il cui rendering cambierebbe. La verifica non distruttiva prima di un commit è `python tools/md-unwrap.py --check .`.

Il file `tools/lint-md-commands.py` percorre i blocchi di shell nei file Markdown e segnala continuazioni di riga, heredoc e comandi git che proseguono sulla riga seguente, perché un comando spezzato dentro un blocco recintato non lo corregge nessun altro strumento.

Il file `tools/check-eol.py` segnala i file di testo che mescolano fini riga `CRLF` e `LF`. Esiste perché nessun altro controllo può accorgersene, e la ragione è strutturale: la convenzione prescrive di conservare la fine riga di ciascun file, quindi `md-unwrap` la rispetta e non ne pretende la coerenza interna, mentre il rendering a video di un file misto è identico a quello di uno coerente. Con `core.autocrlf` a `false` e senza `.gitattributes` git registra le interruzioni così come stanno sul disco, quindi un file misto entra nella storia e alla prima riscrittura da parte di qualunque strumento trasforma una modifica di due righe in una modifica dell'intero file. Lo strumento è di sola lettura e non converte niente, perché la scelta di quale formato tenere spetta a chi conosce il file, e indica il prevalente come suggerimento; esclude le fixture di prova di `md-unwrap`, che sono miste di proposito. La verifica prima di un commit è `python tools/check-eol.py .`.

Il file `tools/verify-usb-dd.ps1` verifica che una chiavetta di installazione scritta in modalità immagine DD sia identica all'immagine di origine, confrontando l'impronta SHA-256 dei primi byte del dispositivo grezzo con quella del file. È l'unico caso in cui un supporto di installazione si può verificare invece di essere dato per buono sulla parola dello strumento di scrittura, e la ragione è che in modalità DD la chiavetta è un clone byte per byte: una scritta in modalità immagine ISO contiene un filesystem nuovo che nessuna impronta pubblicata descrive. Richiede privilegi di amministratore, perché legge un dispositivo grezzo e non un file, ed è di sola lettura. Accetta anche l'impronta attesa dell'immagine, così che una sola esecuzione dica se il file è quello pubblicato e se la chiavetta corrisponde al file. Attenzione allo scopo, che è stato corretto il 2026-09-08 e non è quello per cui lo strumento era nato: non appartiene più alla sottofase 2.4 della procedura e non serve a verificare una chiavetta appena scritta su Windows, perché quel sistema monta i volumi da sé e ripara la tabella delle partizioni, quindi le impronte differiscono legittimamente e il confronto genera falsi allarmi. Il suo uso legittimo è confrontare un'immagine con una copia grezza che nessun sistema abbia montato né riparato. La smentita è in MS-069.

Il file `tools/make-scheda-docx.py` genera la scheda operativa di reinstallazione in `.docx`, pronta da stampare, e la scrive sotto `_notes/` oppure dove indica `--out`. Non converte il Markdown: il contenuto vive nello strumento come dati, perché la carta ha vincoli che il Markdown non ha, cioè due pagine di spazio, caselle da spuntare a penna e riquadri colorati sul passo irreversibile, quindi la sorgente `docs/10-ambiente/scheda-reinstallazione.md` e lo strumento vanno tenuti allineati a mano. Non usa librerie di terze parti, perché un `.docx` è un archivio zip di documenti XML e le cinque parti che servono si scrivono direttamente, il che lo fa girare su qualunque Python 3 senza installare nulla, come gli altri strumenti di questo progetto. I dati di licenza di Akabak non entrano nel documento se non lo si chiede con `--con-licenza`, per ADR-017. La ragione per cui è uno strumento e non un documento composto a mano è in MS-070: la versione fatta a mano era rimasta indietro di due minuti rispetto alla procedura e il codice che l'aveva prodotta era andato perduto con la sessione.

Il file `tools/fix-emphasis.py` attua il divieto di grassetto nella prosa prescritto dalla sezione 8 di `.claude/PROJECT-SYSTEM.md`, convertendolo in corsivo. Le esclusioni sono sostanziali e non prudenziali: salta i blocchi recintati e indentati, dove il grassetto è testo e non formattazione, e salta le righe di tabella, dove non è prosa ma segnaletica, come la parola che nella scheda di reinstallazione dice di non formattare una partizione. Salta anche i modelli sotto `.claude/templates/`, che sono copie del template e la cui correzione appartiene a PA-003. Conserva la fine riga di ciascun file e ha una modalità `--check` non distruttiva che esce con codice diverso da zero. La sua prima applicazione, con la misura della deriva, è in MS-078.

I file `tools/fix-accents.py`, `tools/fix-missing-accents.py` e `tools/fix-dashes.py` attuano le convenzioni tipografiche: accenti veri al posto dell'apostrofo, ripristino degli accenti mancanti dove la forma senza accento non è una parola italiana, e trattini brevi al posto dei trattini lunghi. Il file `tools/test-tipografia.py` è la loro suite di prova, e `tools/dashes-exclude.txt` il loro sidecar di esclusioni.

Su questi tre strumenti valeva una doppia avvertenza, diagnosticata con casi minimi in MS-014, e va letta con la sua data. L'incoerenza fra le regole di prudenza di `fix-accents.py` e `fix-missing-accents.py` sulle forme elise, che lasciava un apostrofo orfano su `c'e'` producendo `c'è'`, è stata chiusa nel template e adottata qui il 2026-09-12 con MS-091, e dal 2026-09-17 una guardia impedisce agli strumenti di scrivere sotto `.claude/templates/` (PA-015); la catena si lancia quindi anche in controllo su `.`, come fa `chiudi`. La gestione dei percorsi su un'altra lettera di unità resta invece non verificata in nessuno dei due versi, ed è una voce di PA-003.

Il file `tools/sync-ambiente.py` propaga il blocco `docs/10-ambiente/` al progetto gemello di home recording, in una sola direzione, marcando le copie e segnalando gli orfani senza rimuoverli.

I file `tools/transfer-to-studio.sh` e `tools/transfer-to-studio.ps1` eseguono il trasferimento dei materiali pesanti verso la macchina di lavoro, con verifica delle impronte, secondo `docs/TRANSFER-MANIFEST.md`. I due non hanno lo stesso perimetro, e la differenza è dichiarata nell'intestazione del secondo: la versione bash copre sia gli otto file piatti del manifest sia gli alberi del corredo software, con confronto ricorsivo delle impronte; la versione PowerShell copre i soli file piatti.

Il file `tools/check-pending-actions.py` verifica quali azioni differite di `docs/PENDING-ACTIONS.md` sono diventate eseguibili, leggendo le condizioni automatizzabili come la presenza di un disco esterno, e con `--confronta` confronta per impronta le due copie del corredo software prima di autorizzarne la cancellazione. È di sola lettura e non cancella nulla.

Il file `tools/latest-screenshot.ps1` restituisce lo screenshot più recente della cartella di cattura, per i passi manuali che l'agente non può osservare da sé.

Il file `tools/arch-dotnet.py` dice l'architettura reale di un eseguibile Windows, ed esiste perché per un assembly .NET il comando `file` risponde a una domanda diversa da quella che si sta ponendo. Per un programma nativo `PE32` significa 32 bit e `PE32+` significa 64, e la lettura basta; per un assembly .NET compilato *AnyCPU* il formato resta `PE32` mentre il programma gira alla larghezza della macchina, quindi a 64 bit su una macchina a 64. Lo strumento legge i tre flag dell'intestazione del runtime CLI che decidono davvero, e sui file nativi dichiara l'assenza di quella intestazione e riporta l'architettura del formato. È di sola lettura, senza dipendenze, e restituisce codice 2 su un file che non sia un eseguibile Windows. La ragione per cui è nato è in MS-101: il controllo prescritto avrebbe fatto concludere che VituixCAD fosse a 32 bit e smontare un prefix corretto.

Il file `tools/analisi-ssd-esterno.py` misura lo spazio recuperabile sull'SSD esterno e segnala gli indizi di guasto, fra cui le cartelle `FOUND.00x` lasciate da più riparazioni di `chkdsk`. È di sola lettura ed è lo strumento dietro PA-008.

Il file `tools/obj-bbox.py` misura il parallelepipedo che contiene una mesh OBJ e lo confronta con una dimensione nota, per verificare la scala di una scansione. È nato per la via della scansione di PA-020, poi abbandonata, e resta l'attuazione delle diagonali di controllo della tabella F del protocollo di rilievo; il suo limite, che i lati orizzontali sovrastimano su un oggetto ruotato, è in MS-160.

Gli strumenti che seguono sono quelli del sistema di progetto, e la ragione per cui sono qui è la stessa degli altri: fare di una convenzione un controllo.

Il file `tools/verifica-ripresa.py` confronta, alla riapertura, l'impronta registrata a fine sessione con lo stato reale di git, e con `--registra` la registra dopo i commit. È eseguito da sé dall'hook `apertura-sessione`, e la skill `riprendi` ne interpreta l'esito.

Il file `tools/check-copie-modelli.py` confronta byte per byte ogni strumento istanziato con il suo modello sotto `.claude/templates/` e fallisce quando divergono, senza scegliere il verso della riconciliazione. Il file `tools/check-catalogo.py` verifica che il catalogo dei pacchetti descriva le cartelle presenti sul disco; qui il catalogo è una copia e non la sorgente, quindi non sta nella sequenza obbligatoria.

Il file `tools/misura-istruzioni.py` somma i caratteri degli instruction file che Claude Code carica a ogni avvio, cioè `CLAUDE.md` e le regole, e fallisce oltre la soglia di guardia di 100 000. Il file `tools/lint-md-tables.py` controlla che ogni cella di una tabella Markdown stia su una riga e che ogni riga porti tutte le colonne, cosa che `md-unwrap` per contratto non guarda. Il file `tools/sync-codex-skills.py` genera sotto `.agents/skills/` i wrapper con cui Codex scopre le skill canoniche, e con `--check` ne verifica l'allineamento. Il file `tools/chiudi-sessione.ps1` è lo script che la funzione `chiudi` del profilo PowerShell lancia: controlli, commit con conferma, push verificato, registrazione dell'impronta e wipe degli account. In un progetto esegue soltanto i controlli generici, e non quelli propri di questo progetto, che è una voce di PA-003.

Il file `tools/lint-memoria.py` segnala i commit più recenti dell'ultima voce del work-log e le pendenze chiuse senza data, ed è adattato ai registri di questo progetto come il suo pacchetto prescrive. Il file `tools/Test-Allineamento.py` legge `data/scadenze.json` e dice quali affermazioni stanno invecchiando: scadenze, misure con una cadenza, asserzioni umane con la loro validità, più quattro invarianti fra cui l'elenco degli strumenti di questa scheda. Gira all'apertura di ogni sessione e attua la regola `affermazioni-verificabili.md`.

Il file `tools/roadmap.py` rigenera la lista di che cosa resta da fare da `tools/roadmap-items.yml`, ordinata per costo e non per importanza, con l'esito dei controlli misurato dal vivo; `--format html --write` scrive una pagina stampabile sotto `build/`, ignorata. Il file `tools/costruisci-timeline.py` rigenera `docs/TIMELINE.html`, la linea temporale che affianca a ogni passo la sua ragione, dai microstep che portano il campo `Data:` e dal work-log. Il file `tools/lint-prosa.py` segnala i segni ricorrenti del testo generato e non riscrive nulla; gira come avviso nel `pre-commit` dei commit manuali, e la guida con le fonti sta in `docs/anti-slop/`.

Strumenti della base di conoscenza, arrivati il 2026-10-01 con MS-179. Il file `tools/doc-ingest.py` converte PDF, DOCX e affini in Markdown con `markitdown`, in locale e senza modelli, nella cache ignorata `_notes/.tmp-doc-cache/` con un indice dei capitoli, e riconverte soltanto ciò che cambia. I file `tools/extract-titlepages.py` e `tools/render-bib-registry.py` sono del pacchetto `book-bib-extract`: il primo rende in immagine le pagine di frontespizio con Poppler, il secondo rigenera la tabella leggibile del registro bibliografico `_notes/book-bib-registry.json`. Fuori da `tools/` stanno PaperQA2, nell'ambiente virtuale `.venv` del progetto, e Feynman, installato globalmente con npm: entrambi aspettano le credenziali di PA-023.

## Rapporto con gli altri progetti

Il blocco `docs/10-ambiente/` è condiviso con `home-recording-training-mixing-setup`, perché la macchina Ubuntu Studio serve a entrambi. La copia canonica è quella di questo progetto e la propagazione è unidirezionale.

Il sistema sotto `.claude/` è istanziato da `template-claude-developing`, che è la sua sorgente, e si riallinea con lo strumento `allinea-tutti.ps1` del template, che registra l'ultimo allineamento in `.claude/allineamento-template.json`. Le due divergenze che questa scheda dichiarava fino al 2026-09-12 non esistono più: la negazione nel `.gitignore` sui modelli `_notes` è stata portata al template il 2026-09-17, e gli strumenti tipografici sono identici ai modelli, come misura `check-copie-modelli.py`. Le copie che divergono per mestiere sono dichiarate in quello strumento, cioè `tools/dashes-exclude.txt` e `tools/lint-memoria.py`.

## Verifica prima di un commit

La sequenza di controllo, tutta non distruttiva, è la seguente.

```bash
python tools/md-unwrap.py --check .
python tools/lint-md-commands.py .
python tools/check-eol.py .
python tools/test-tipografia.py
python tools/sync-ambiente.py --check
python tools/check-copie-modelli.py
python tools/check-pending-actions.py
python tools/misura-istruzioni.py
python tools/lint-md-tables.py .
python tools/sync-codex-skills.py --check
python tools/lint-memoria.py
python tools/Test-Allineamento.py
```

La sequenza è la stessa di `CLAUDE.md`, che ne è la fonte, e va eseguita per intero prima di proporre `chiudi`.
