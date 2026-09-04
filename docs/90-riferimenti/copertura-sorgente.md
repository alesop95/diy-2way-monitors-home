# Verifica di copertura del documento sorgente

> Prova che `full_electroacoustics.docx` è stato letto integralmente e che ogni sua sezione ha una destinazione nell'albero `docs/`. È il documento che autorizza a rimuovere il `.docx` dalla radice del progetto: finché questa tabella non copre tutto, il sorgente non è sostituibile.

## Il conteggio

Il documento contiene 507 paragrafi, 4 tabelle e 1 immagine, per circa 10.100 parole. La classificazione dei paragrafi è la seguente.

| Categoria | Numero | Destino |
|---|---|---|
| Titoli | 71 | tutti mappati nella tabella qui sotto |
| Paragrafi di contenuto | 387 | convertiti in prosa nelle pagine di destinazione |
| Paragrafi vuoti | 29 | scartati, sono spaziature del documento |
| Paragrafi segnaposto | 22 | scartati, sono sequenze di lettere ripetute lasciate come promemoria |

I 22 segnaposto sono elencati integralmente per non lasciare dubbi su che cosa è stato buttato: alle posizioni 224, 231, 233, 242, 251, 308, 310, 334, 336, 421, 427, 433, 451, 480, 482, 488, 492, 497, 499, 501, 503 e 504 il testo è una sequenza del tipo `aaaa`, `Aaaaaaa` oppure `aaaq`. La posizione 503 è un caso particolare, perché il segnaposto è il titolo stesso di una sezione, che risulta quindi intitolata `aaaaaaaaa` e priva di contenuto.

Le quattro tabelle sono state riportate integralmente: i requisiti di sistema nella pagina di installazione, lo schema di partizionamento nella stessa pagina, il confronto fra microfoni di misura nella pagina della fase 1, e il changelog fra le due versioni di EASE Focus nella pagina della fase 2.

L'unica immagine presente nel file, di 3.673 byte, era una delle due formule matematiche della sezione sull'analisi in Octave. La seconda formula era già assente dal file. La pagina della fase 3 dichiara questa perdita esplicitamente e rimanda a una fonte esterna per le espressioni, invece di ricostruirle a memoria.

## La mappa sezione per sezione

La colonna dei paragrafi conta il contenuto sostanziale della sezione, esclusi titoli, righe vuote e segnaposto. Un valore zero su una sezione contenitore è normale, perché quella sezione esiste solo per raggruppare le figlie; un valore zero su una sezione foglia significa che nel sorgente quella sezione era vuota, e la colonna della destinazione dice come è stata trattata.

| Par. | Liv. | Sezione del sorgente | Contenuto | Destinazione |
|---|---|---|---|---|
| 0 | H2 | Progetti elettroacustici / programmazione a scopo privato | 0 | contenitore, nessun contenuto |
| 1 | H3 | Progetto monitor due-vie con Linux per uso domestico | 0 | contenitore |
| 2 | H4 | Il workflow in linea teorica | 34 | `00-workflow.md` |
| 37 | H4 | Installazioni preliminari | 0 | contenitore |
| 38 | H5 | Ubuntu Studio 25.04 | 0 | contenitore |
| 39 | H6 | Introduzione e prerequisiti | 5 | `10-ambiente/ubuntu-studio-installazione.md` |
| 46 | H7 | Partizionamento | 37 | `10-ambiente/ubuntu-studio-installazione.md` |
| 85 | H6 | Wine | 0 | contenitore |
| 86 | H7 | Introduzione | 7 | `10-ambiente/wine-vs-emulatore.md` |
| 94 | H8 | I prefix e le dipendenze | 24 | `10-ambiente/wine-prefix-e-dipendenze.md` |
| 119 | H9 | Differenza prefissi a 32bit e 64 bit | 8 | `10-ambiente/wine-prefix-e-dipendenze.md` |
| 128 | H9 | Gestione di licenze legate alla macchina | 5 | `10-ambiente/wine-prefix-e-dipendenze.md` e `90-riferimenti/licenze-e-registrazioni.md` |
| 135 | H7 | Configurazione di Wine | 0 | contenitore |
| 136 | H8 | Pulizia e (re)installazione | 18 | `10-ambiente/wine-configurazione.md` |
| 155 | H8 | Impostazione del bottle e configurazioni specifiche | 36 | `10-ambiente/wine-configurazione.md` |
| 192 | H7 | Installazione programmi Windows in Ubuntu | 0 | contenitore |
| 193 | H8 | Akabak | 23 | `10-ambiente/wine-programmi-windows.md` |
| 220 | H9 | Utilizzo della licenza | 3 | `90-riferimenti/licenze-e-registrazioni.md` |
| 226 | H9 | Creare un launcher | 1 | `10-ambiente/wine-configurazione.md` |
| 228 | H8 | VituixCAD 2 | 10 | `10-ambiente/wine-programmi-windows.md` |
| 243 | H8 | WinISD (optional) | 7 | `10-ambiente/wine-programmi-windows.md` e `50-progettazione-monitor.md` |
| 252 | H7 | Troubleshooting | 20 | `10-ambiente/wine-troubleshooting.md` |
| 279 | H4 | 1) Misurazione reale stanza | 0 | contenitore |
| 280 | H5 | Introduzione | 2 | `20-misura-stanza.md` |
| 283 | H5 | REW (Room EQ Wizard) | 6 | `20-misura-stanza.md` |
| 290 | H6 | Microfono di misura calibrato | 16 | `20-misura-stanza.md` |
| 309 | H5 | Passaggi pratici | 8 | `20-misura-stanza.md` |
| 319 | H4 | 2) Modellazione della stanza e simulazione acustica | 1 | `30-modellazione-e-simulazione.md` |
| 321 | H5 | Introduzione | 7 | `30-modellazione-e-simulazione.md` |
| 330 | H5 | Blender | 2 | `30-modellazione-e-simulazione.md` |
| 333 | H6 | Alternative | 0 | contenitore |
| 335 | H7 | (TBC) Ramsete 27b | 0 | vuota nel sorgente; annotata come non valutata in `30-modellazione-e-simulazione.md` e in `90-riferimenti/inventario-software.md` |
| 339 | H7 | EASE SpeakerLab (Free) | 3 | `30-modellazione-e-simulazione.md` |
| 343 | H7 | EASE Address 2.1 | 2 | `30-modellazione-e-simulazione.md`, con la motivazione dell'esclusione |
| 346 | H7 | EEASE Focus | 0 | contenitore |
| 347 | H8 | EEASE Focus v3.0.18 | 7 | `30-modellazione-e-simulazione.md` |
| 356 | H8 | EASE_Focus_v3.1.10 | 8 | `30-modellazione-e-simulazione.md` |
| 366 | H8 | EASE_Focus_v3.1.260 | 3 | `30-modellazione-e-simulazione.md` |
| 370 | H9 | Installazione su Ubuntu Studio 2025 (altro prefix) | 25 | `10-ambiente/wine-programmi-windows.md` |
| 396 | H9 | (TBC) Check quali programmi richiedono stessi .dll e .net | 0 | vuota nel sorgente; riportata come domanda aperta nella sezione conclusiva di `10-ambiente/wine-programmi-windows.md` |
| 397 | H7 | DIY Loudspeaker Pack Softwares | 10 | `90-riferimenti/inventario-software.md`, con la parte di definizione di monitor DIY in `00-workflow.md` |
| 408 | H4 | 3) Analisi acustica dei dati | 0 | contenitore |
| 409 | H5 | Octave/MATAA | 4 | `40-analisi-octave.md` |
| 416 | H5 | Altre risorse in ambiente GNU Octave | 0 | contenitore |
| 417 | H6 | Acoustics Toolbox | 3 | `40-analisi-octave.md` |
| 422 | H6 | Auditory Modeling Toolbox (AMT) | 4 | `40-analisi-octave.md` |
| 428 | H6 | ITA-Toolbox (RWTH Aachen) | 4 | `40-analisi-octave.md` |
| 434 | H4 | 4) Progettazione completa monitor | 0 | contenitore |
| 435 | H5 | Introduzione | 2 | `50-progettazione-monitor.md` |
| 438 | H5 | 4a) Progettazione completa simulata | 0 | contenitore |
| 439 | H6 | VituixCAD 2 | 1 | `50-progettazione-monitor.md` |
| 441 | H5 | 4b) Progettazione meccanica del monitor | 0 | contenitore |
| 442 | H6 | FreeCAD | 6 | `50-progettazione-monitor.md` |
| 450 | H5 | 4c) Ottimizzazione accordo | 0 | contenitore |
| 452 | H6 | WinSD | 1 | `50-progettazione-monitor.md`, con la conclusione di ridondanza |
| 454 | H4 | 5) Simulazione finale (controllo onda stazionaria) | 0 | contenitore |
| 455 | H5 | Introduzione | 5 | `60-simulazione-finale-akabak.md` |
| 461 | H5 | Akabak 3 | 0 | contenitore |
| 462 | H6 | Must per il progetto e passi operativi | 16 | `60-simulazione-finale-akabak.md` |
| 479 | H6 | Alternative | 0 | contenitore |
| 481 | H7 | Pachyderm | 0 | vuota nel sorgente; l'esclusione e la sua motivazione sono in `30-modellazione-e-simulazione.md` e richiamate in `60-simulazione-finale-akabak.md` |
| 484 | H5 | Simulazione in ambiente | 1 | `60-simulazione-finale-akabak.md` |
| 486 | H4 | 6) Acquisto driver | 0 | contenitore |
| 487 | H5 | Acquisto driver | 0 | vuota nel sorgente; `70-realizzazione-e-verifica.md` dichiara che cosa la fase dovrà produrre e quali decisioni sono aperte |
| 489 | H4 | 7) Montaggio | 0 | contenitore |
| 491 | H5 | Pannelli legno e progetto | 0 | vuota nel sorgente; trattata come sopra in `70-realizzazione-e-verifica.md` |
| 493 | H4 | 8) Verifica finale con nuove misure REW | 1 | `70-realizzazione-e-verifica.md` |
| 496 | H3 | Personalizzazione dell'amplificatore per il basso | 0 | vuota nel sorgente; annotata come lavoro separato fuori scopo in `70-realizzazione-e-verifica.md` |
| 498 | H4 | Introduzione | 0 | vuota nel sorgente, come sopra |
| 500 | H5 | Il modello | 0 | vuota nel sorgente, come sopra |
| 503 | H4 | (titolo segnaposto) | 0 | scartata, il titolo stesso è un segnaposto |

## Materiale aggiunto in conversione

Tre contenuti nell'albero `docs/` non provengono dal `.docx` e vanno distinti perché il sorgente non li contiene.

Gli appunti di una conversazione del luglio 2024 con un collega esperto di acustica degli ambienti, che stanno in un file di testo nella radice del progetto. Da lì vengono le osservazioni sulla forma irregolare della stanza, sul soffitto spiovente, sulla parete alle spalle del punto di ascolto, sulla configurazione ipotizzata a due vie reflex, sulla curva target e sul vincolo di reperibilità dei driver. Sono distribuite fra `20-misura-stanza.md`, `50-progettazione-monitor.md` e `70-realizzazione-e-verifica.md`.

L'inventario del pacchetto software ereditato, che sta in un altro file di testo nella radice e non nel `.docx`. Alimenta `90-riferimenti/inventario-software.md`, incluse le voci escluse dal workflow.

La pagina `10-ambiente/ubuntu-lts-upgrade.md`, che non ha corrispondente nel sorgente perché il problema che descrive è emerso dopo la sua stesura. È dichiaratamente una ipotesi con la propria procedura di verifica, non una cronaca.

## Conclusione

Il sorgente è coperto integralmente. Le sole informazioni non trasferite sono i 29 paragrafi vuoti, i 22 segnaposto e la formula presente come immagine, tutti dichiarati sopra uno per uno.

Il `.docx` può quindi essere rimosso dalla radice del progetto. Non viene distrutto: si sposta sotto `_notes/`, che è ignorato da git, e resta nel manifest di trasferimento verso la macchina Ubuntu Studio, dove conserva il ruolo di fonte di rigenerazione se un domani si volesse ricostruire questa documentazione con un convertitore automatico invece che a mano.
