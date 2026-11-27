# Artefatti, originali e prove conservate

Radice locale: `E:\diy-2way-monitors-home`. I percorsi sotto sono relativi alla radice. L'unico ingresso di lettura è [STATO-PROGETTO.md](../STATO-PROGETTO.md); il [catalogo](catalogo-documentazione.md) elenca i documenti senza duplicarne contenuti o pendenze. Questa pagina risolve i percorsi degli artefatti e delle prove private.

## Consegne e sorgenti

| Artefatto | Percorso esatto | Sorgente o funzione |
|---|---|---|
| Recap stampabile | `docs/pdf/recap-progetto.pdf` | `docs/STATO-PROGETTO.md`; copia di lettura WordCraft, navigazione nel Markdown. |
| Relazione matematica | `docs/pdf/crossover-pc-pi-analogico.pdf` | `docs/62-confronto-crossover-e-verifica-matematica.md`, TeX in `docs/latex/`. |
| Relazione tecnica corrente | `docs/pdf/sistema-autonomo-driver-e-collaudo.pdf` | `docs/63-sistema-autonomo-driver-e-collaudo.md`, TeX in `docs/latex/`. |
| Relazione reflex e cabinet | `docs/pdf/reflex-direttivita-cabinet.pdf` | `docs/64-reflex-direttivita-e-cabinet-nominale.md`, quattro figure e TeX. |
| Kit nominale dettagliato | `build/consegna-completamento-20261125.zip` | 55 file con manifesto; estratto nello stesso percorso senza estensione. Tre FCStd, STEP, DXF, tavole, distinte e viste; nessun ordine di taglio. |
| Somma dei driver su file | `build/somma-acustica-20261126/` | Tre casi analitici di8 file ciascuno; input in data/somma-acustica-demo, rapporti durevoli in research-vault/somma-acustica-20261126. Dataset allineato analizzato in build/caratterizzazione-somma-20261126; nessuna misura. |
| Discesa sullo ST-120 | [Studio del cavo](../69a-discesa-cavi-st120.md) | Dati e impronte in `data/discesa-st120-a24.json`. Quattro proiezioni con raggio del cavo e margine di sgancio. |
| Retro A24 | [Capitolo69](../69-retro-a24-e-passaggio-cavi.md) | Piastra e passaggio a quattro poli, [tavola](../figure/retro-a24-20261127/retro-a24.pdf), [DXF](../figure/retro-a24-20261127/retro-a24.dxf) e riscontro CAD con prova della diagonale. |
| Schema delle quattro vie | [Capitolo68](../68-cablaggio-quattro-vie.md) | L05-L08 e P05-P08, pinout TRS/RCA e alternativa a trasformatore, bilancio e qualifica sospesa. |
| Distinta della catena | `data/catena-riferimento.json` | Revisione26 novembre: componenti, quantità, mappa nominale, prezzi visualizzati e lotti stimati; ADR-058 e docs/67, nessun acquisto o qualifica. |
| Provenienza dei PDF | `docs/pdf/manifest.json` | SHA-256 dei PDF e degli input, controllati da `tools/verifica_documenti.py`. |
| Compilazione | `docs/latex/README.md` | Intermedi in build, consegne in docs/pdf, QA temporaneo eliminato. |
| Kit CAD esplorativo | `build/consegna-cabinet-20261119/confronto.html` | Tre cabinet parametrici, nativi, STEP, DXF, distinta e viste; non ordine di taglio. |
| Dati geometrici | `data/postazione-st120.json`, `config/cabinet/studio-st120.json` | Quote note e ipotesi distinte dai rilievi sospesi. |
| Dati elettroacustici | `data/driver-candidati.json` | Parametri e provenienza dei candidati, non misure sugli esemplari. |
| Configurazioni d'uso futuro | `config/pi/README.md` | Esempi PC/Pi, senza installazione né qualifica hardware. |

## Risultati numerici e pipeline

| Passaggio | Codice | Rapporto di riferimento |
|---|---|---|
| Modello LR4 | `tools/verifica-matematica-crossover.py` | `research-vault/crossover-pc-pi-analogico/risultati-modello.json`; run `build/studio-crossover-20261120-v2/`. |
| Driver e profili elettrici | `tools/studio_sistema_audio.py` | `research-vault/sistema-autonomo-20261120/risultati-driver.json`; run `build/sistema-autonomo-20261120-v5/`. |
| Dodici profili nel motore | `tools/collauda-profili-autonomi.py` | `research-vault/sistema-autonomo-20261120/risultati-profili.json`; log/config del run finale-v5 conservati, PCM sintetici eliminati. |
| HP35, LT e sensibilità | `tools/fattibilita_basso.py` | `research-vault/sistema-autonomo-20261120/fattibilita-basso.json`; dodici nuovi casi reali su file, PCM temporanei rimossi. |
| Controllo volume/mute e pannello | `tools/controllo_ascolto.py`, `tools/pannello_ascolto.py`, observer ALSA/PipeWire | `research-vault/sistema-autonomo-20261120/risultati-controllo.json`: due rate, quattro canali, HTTP/WebSocket reali, guasto software e SIGTERM. Hardware non qualificato. |
| Pannello nel browser | `tools/collauda-pannello-browser.py` | `build/controllo-ascolto/browser-qa.json`: desktop/mobile e font verificati, PNG ispezionati e rimossi. |
| Consegna software | `tools/consegna_controllo.py` | `build/controllo-ascolto/controllo-ascolto.zip`, manifesto interno dei file. Installazione persistente manuale, nessun deploy automatico. |
| Installazione verificata | `research-vault/sistema-autonomo-20261120/risultati-installazione-controllo.json` | 24 file della copia trasferita, servizio e pagina verificati in esercizio il 23 novembre; avvio al login ancora disabled alla prova. |
| Figura del basso | `tools/visualizza_simulazioni.py` | `docs/figure/sistema-autonomo/fattibilita-basso.svg`: sei pannelli, diciotto curve, provenienza incorporata e check deterministico. |
| Servizio Ubuntu e banco virtuale | `tools/installa-dsp-utente.py`, `tools/dsp_pipewire.py`, `tools/monitor_dsp.py` | Procedure in `docs/57-dsp-persistente.md` e `docs/10-ambiente/camilladsp-servizio-utente.md`; prove storiche nello ZIP delle sessioni. |
| Reflex, direttività e livelli | `tools/studio_completamento.py`, `tools/figure_completamento.py` | `research-vault/completamento-20261125/risultati.json`: 108 casi reflex, 27 angolari e 18 elettrici; figure in `docs/figure/completamento-20261125/`. |
| CAD nominale e consegna | `tools/collauda-cabinet-dettagli.py`, `tools/consegna_completamento.py` | `research-vault/completamento-20261125/consegna.json`; prove native in `build/completamento-20261125-freecad-verificato/`, tavole in `build/completamento-20261125-cadcraft-verificato/`. |
| Pedigree e punti d'uso | `tools/mappa_fonti_progetto.py` | `research-vault/usi-fonti-progetto.json`, vista `docs/90-riferimenti/fonti-progetto.md`. |
| Caratterizzazione su file | `tools/caratterizzazione.py` | `data/caratterizzazione-demo/manifest.json`, rapporto versionato `research-vault/caratterizzazione-aperta-20261126/risultati-esempio.json`; pacchetto in `build/caratterizzazione-20261126/`, con 17 file firmati più manifesto. Cinque curve sintetiche, non misure hardware. |
| Catalogo dei percorsi | `tools/catalogo_documentazione.py` | `data/catalogo-documentazione.csv`, vista `docs/90-riferimenti/catalogo-documentazione.md`. |

Il modello elettrico e il calcolo di escursione non sono misure della risposta acustica. Ogni rapporto conserva ipotesi e limiti. Il primo kit CAD è esplorativo; il nuovo aggiunge frontali e rinforzo nominali. Fissaggi, giunzioni e quote esecutive dipendono dai componenti definitivi e dai riscontri sospesi.

## Manuali originali privati

Per il setup, i report completi sono `docs/10-ambiente/verifica-prima-del-trasferimento.md` (ricognizione/CPU), `collaudo-dopo-riavvio-2026-11.md`, `freecad-collaudo-native.md`, `camilladsp-servizio-utente.md`, `fluidsynth-diagnosi-e-collaudo.md`, `backup-ottimizzazione-2026-11.md` e `backup-finale-setup-2026-11.md`, tutti nella stessa cartella. Contengono sequenze, errori e criteri; OPS conserva i microstep e [tracciabilita-microstep.md](tracciabilita-microstep.md) la ricerca per fase. Le prove storiche possono essere nel ZIP delle sessioni sotto il percorso originale: non sono andate perdute quando sono stati rimossi gli espansi.

Per le simulazioni aprire nel browser `docs/figure/crossover-20261120/lr4-modulo-fase.svg`, `cammino-e-somma.svg` nella stessa cartella e la figura basso sopra. Per ruotare i cabinet usare FreeCAD e `build/consegna-cabinet-20261119/cad/A24/studio.FCStd`, oppure B27/C24 nello stesso schema; il confronto HTML usa viste statiche. Riferimenti cliccabili riuniti in [STATO-PROGETTO.md](../STATO-PROGETTO.md#come-vedere-le-simulazioni-e-il-3d).

Su Ubuntu FreeCAD è già predisposto come `~/.local/bin/freecad-1.1.4`; la copia persistente delle viste native è in `~/electroacoustics/progetti/cabinet-st120-20261119/viste/`, verificata nel [collaudo dopo riavvio](../10-ambiente/collaudo-dopo-riavvio-2026-11.md). Dalla sessione grafica si apre FreeCAD e si sceglie il file FCStd di A24, B27 o C24 da quella cartella. Un collegamento FCStd da Windows richiede FreeCAD sul computer che lo apre: HTML, SVG e PDF invece si consultano già dal browser della postazione. Nessuna nuova applicazione viene installata per leggere le viste statiche.

Su Ubuntu FreeCAD è già predisposto come `~/.local/bin/freecad-1.1.4`; la copia persistente delle viste native è in `~/electroacoustics/progetti/cabinet-st120-20261119/viste/`, verificata nel [collaudo dopo riavvio](../10-ambiente/collaudo-dopo-riavvio-2026-11.md). Dalla sessione grafica si apre FreeCAD e si sceglie il file FCStd di A24, B27 o C24 da quella cartella. Un collegamento FCStd da Windows richiede FreeCAD sul computer che lo apre: HTML, SVG e PDF invece si consultano già dal browser della postazione. Nessuna nuova applicazione viene installata per leggere le viste statiche.

| Oggetto | Documentazione | Originale conservato |
|---|---|---|
| Marshall MG15 | `docs/80-strumenti-posseduti/marshall-mg15.md` | `_notes/fonti-amplificatori/marshall-mg15-manuale-originale.pdf`; manuale MG10/MG15 già letto, OCR testuale conservato, PNG di riscontro eliminati. |
| Fender Frontman 65R | `docs/80-strumenti-posseduti/fender-frontman-65r.md` | Studio originale e metadati sotto `_notes/fonti-amplificatori/`; dettagli privati nelle ricevute di acquisizione. |
| EKO basso 30 W | `docs/80-strumenti-posseduti/eko-basso.md` | `_notes/fonti-amplificatori/eko-basso-manuale-originale.pdf` e `eko-basso-ocr.txt`; manuale XL/XB di undici pagine, candidato XB30 con 10 pollici 8 ohm. |

Gli originali non sono stati ridotti o ricompressi. Sono state rimosse soltanto copie OCR dei PDF e immagini derivate. La diagnosi dello speaker EKO rimane sospesa, non dimostrata dal manuale.

Il manuale originale del tavolo è `_notes/fonti-postazione/Stagecaptain-ST-120-manual-EN.pdf`. Il contatto già disponibile per falegname e diffusori è conservato privatamente in `_notes/fonti-amplificatori/contatto-supporto-realizzazione.png`. I pacchetti originali CamillaDSP sono in `_notes/fonti-camilladsp/`. Cinque ricollocazioni sono verificate con SHA-256 e mappate dalla ricevuta corrente. Il documento sorgente `full_electroacoustics.docx` conserva il percorso storico `_notes/full_electroacoustics.docx`.

## Archivi storici e ricevute

| Oggetto | Percorso esatto | Come si consulta |
|---|---|---|
| 340 prove di run superati | `_notes/archivio-prove/20261120/prove-superate.zip` | Percorsi originali build nel ZIP; impronte in `manifest.json`, rimozioni in `ricevuta-riordino.json` della stessa cartella. |
| Sessioni e script ad uso singolo | `_notes/archivio-prove/sessioni-storiche.zip` | Percorsi originali _notes nel ZIP; elenco e SHA-256 nella ricevuta corrente. Comprende i vecchi censimenti e le copie degli snapshot prima del consolidamento. |
| Pulizia corrente | `_notes/archivio-prove/riordino-corrente.json` | File eliminati o archiviati, byte e hash; la ricevuta precedente incorporata conserva le prime 81 rimozioni. |
| Ultimo controllo completo | `_notes/chiudi-autonomia-20261120.txt` | Uscita effettiva di chiudi in sola verifica; nessun commit eseguito. |
| Ripresa locale | `_notes/RESUME-PROMPT.md` | Puntatore allo snapshot versionato, senza una seconda cronologia. |

Per ricostruire una prova si cerca il percorso originale nel manifesto o nella ricevuta e si estrae il solo membro necessario in una cartella nuova. I microstep storici non vengono riscritti per fingere che il file sia sempre stato nel ZIP. Gli archivi sullo stesso disco sono conservazione della storia, non backup. Nessuna pulizia ha riguardato J, la biblioteca o altri progetti.

Esito corrente MS-304/305: 335 derivati eliminati per 247.522.428 byte; 1011 prove storiche conservate nel ZIP da 16.568.199 byte, con 223.076.568 byte di espansi rimossi e una copia della prima chiusura fallita. Recupero complessivo di questo giro 454.030.797 byte, circa 433 MiB, separato dalla pulizia precedente dei 340 file. In radice a _notes rimangono sette file: sei per ripresa/verifica e il sorgente DOCX storico. La cache testuale della biblioteca sotto `_notes/.tmp-doc-cache/` rimane una cache persistente di studio censita, non un temporaneo abbandonato; non è stata cancellata con la pulizia del laboratorio.
