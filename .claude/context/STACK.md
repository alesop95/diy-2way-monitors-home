---
generated-from-commit: 0df04bb7019814cf69b8458e4eaad8eaf71be818
generated-from-branch: main
generated-date: 2026-09-04
covers-paths:
  - tools/**
  - docs/**
last-verified-commit: f85480d
---

# Stack del progetto

> Documento di recupero: un collega che clona questo repository deve capire da qui con che cosa si lavora e perché. Questo progetto non ha codice applicativo, quindi lo stack non è un insieme di librerie ma la catena di strumenti di progettazione più gli script di manutenzione della documentazione.

## Che tipo di progetto è

È un progetto di ingegneria elettroacustica documentato, non un progetto software. Il repository contiene documentazione tecnica versionata sotto `docs/`, gli strumenti di verifica e manutenzione sotto `tools/`, e il sistema di contesto dell'agente sotto `.claude/`. I materiali binari, cioè installer e pacchetti di esempio, sono deliberatamente fuori dal versionamento e vivono sulla macchina di lavoro.

Ne segue una conseguenza sulla lettura del repository: il valore non sta nel codice ma nella catena di decisioni documentate, e il punto d'ingresso è `docs/README.md`.

## Catena di strumenti di progettazione

La catena vive sulla macchina Ubuntu Studio descritta in `docs/10-ambiente/README.md`, non su questa postazione. La regola di composizione è nativo Linux dove possibile, Wine dove non esiste alternativa seria.

Nativi: REW per la misura acustica, Blender per la geometria della stanza, GNU Octave con il toolbox MATAA per l'analisi modale e il calcolo dei tempi di riverberazione, FreeCAD per la progettazione meccanica del cabinet.

Sotto Wine, ciascuno nel proprio prefix a 64 bit: Akabak 3 per la simulazione mista elettroacustica e ambientale, VACS come suo strumento di visualizzazione nello stesso prefix, VituixCAD 2 per crossover e direttività, EASE Focus 3.1.260 con il servizio di database AFMG per la verifica di copertura, e ARTA 1.7.1 per produrre un file GLL da un diffusore misurato. La mappa completa dei prefix con le dipendenze di ciascuno è in `docs/10-ambiente/wine-corredo-progetto-stanza.md`.

WinISD è disponibile ma deliberatamente non installato. Ramsete 27b è sospeso in attesa della verifica del suo stato di licenza, e sarebbe il solo a richiedere un prefix a 32 bit, per ADR-009.

L'hardware di misura è una Focusrite Scarlett 2i2 di seconda generazione con alimentazione phantom, e un microfono di misura calibrato individualmente ancora da acquistare.

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

I file `tools/fix-accents.py`, `tools/fix-missing-accents.py` e `tools/fix-dashes.py` attuano le convenzioni tipografiche: accenti veri al posto dell'apostrofo, ripristino degli accenti mancanti dove la forma senza accento non è una parola italiana, e trattini brevi al posto dei trattini lunghi. Il file `tools/test-tipografia.py` è la loro suite di prova, e `tools/dashes-exclude.txt` il loro sidecar di esclusioni.

Su questi tre strumenti valgono due avvertenze, entrambe verificate con casi minimi e documentate in MS-014 del registro dei microstep. Si eseguono sui soli file Markdown e non su `.`, perché su un file di codice le regole di prudenza di `fix-accents.py` e `fix-missing-accents.py` sono incoerenti fra loro: il primo si astiene sulle forme elise come `c'e'`, il secondo no, e la catena dei due lascia un apostrofo orfano producendo `c'è'`, che poi nessuno dei due riconosce più. E terminano con un errore se ricevono un percorso su un'altra lettera di unità, difetto che `md-unwrap.py` ha già corretto e questi no.

Il file `tools/sync-ambiente.py` propaga il blocco `docs/10-ambiente/` al progetto gemello di home recording, in una sola direzione, marcando le copie e segnalando gli orfani senza rimuoverli.

I file `tools/transfer-to-studio.sh` e `tools/transfer-to-studio.ps1` eseguono il trasferimento dei materiali pesanti verso la macchina di lavoro, con verifica delle impronte, secondo `docs/TRANSFER-MANIFEST.md`. I due non hanno lo stesso perimetro, e la differenza è dichiarata nell'intestazione del secondo: la versione bash copre sia gli otto file piatti del manifest sia gli alberi del corredo software, con confronto ricorsivo delle impronte; la versione PowerShell copre i soli file piatti.

Il file `tools/check-pending-actions.py` verifica quali azioni differite di `docs/PENDING-ACTIONS.md` sono diventate eseguibili, leggendo le condizioni automatizzabili come la presenza di un disco esterno, e con `--confronta` confronta per impronta le due copie del corredo software prima di autorizzarne la cancellazione. È di sola lettura e non cancella nulla.

Il file `tools/latest-screenshot.ps1` restituisce lo screenshot più recente della cartella di cattura, per i passi manuali che l'agente non può osservare da sé.

## Rapporto con gli altri progetti

Il blocco `docs/10-ambiente/` è condiviso con `home-recording-training-mixing-setup`, perché la macchina Ubuntu Studio serve a entrambi. La copia canonica è quella di questo progetto e la propagazione è unidirezionale.

Il sistema sotto `.claude/` è istanziato da `template-claude-developing`, che è la sua sorgente. Due divergenze da quel template sono volute e annotate: la negazione nel `.gitignore` che rende versionabili i modelli `_notes` sotto `.claude/templates/`, e l'uso delle versioni più recenti degli strumenti tipografici, che nel template stanno in `tools/` alla radice e non nel pacchetto di istanziazione.

## Verifica prima di un commit

La sequenza di controllo, tutta non distruttiva, è la seguente.

```bash
python tools/md-unwrap.py --check .
python tools/lint-md-commands.py .
python tools/test-tipografia.py
python tools/sync-ambiente.py --check
python tools/check-pending-actions.py
```
