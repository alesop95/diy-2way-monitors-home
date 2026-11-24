# Fonti

> Riferimenti citati nel documento sorgente, raccolti per argomento. Nessuno di questi indirizzi è stato recuperato durante la conversione: sono trascritti dal sorgente e dai file di collegamento presenti nella cartella del progetto, e vanno verificati al momento dell'uso.

## Sistema operativo e ambiente

Distribuzione e download: `https://ubuntustudio.org/download/`

Panoramica delle funzionalità audio della distribuzione: `https://ubuntustudio.org/tour/audio/`

Metapacchetto per aggiungere l'ambiente Studio a una Ubuntu normale: `https://ubuntustudio.org/ubuntu-studio-installer/`

Annuncio del rilascio di Ubuntu Studio 26.04 LTS, letto il 2026-09-30 ed è la fonte del periodo di supporto del flavor, cioè tre anni fino ad aprile 2029, più breve dei cinque della base Ubuntu: `https://ubuntustudio.org/2026/04/ubuntu-studio-26-04-lts-released/`. È la sola voce di questa sezione recuperata e letta, a differenza di quanto dice la nota in testa per le altre.

Note di rilascio della base Ubuntu 26.04 LTS: `https://documentation.ubuntu.com/release-notes/26.04/`. Elencata dalla ricerca del 2026-09-30 sul periodo di supporto e non letta: il supporto della base resta quindi affermato da ADR-006 e non da questa pagina.

Discussione sull'annuncio di Ubuntu Studio 26.04 LTS e note di rilascio sul forum della comunità Ubuntu: `https://discourse.ubuntu.com/t/ubuntu-studio-26-04-lts-released/80832` e `https://discourse.ubuntu.com/t/ubuntu-studio-26-04-lts-release-notes/79113`. Elencate dalla stessa ricerca e non lette.

## Acustica della stanza

Sito ufficiale di Ramsete, letto il 2026-10-01: `http://ramsete.com/`. Autorevole sull'ultima versione pubblicata, cioè la 3.02 del 2018, sul fatto che il programma funziona in modalità dimostrativa senza la chiave, e sulla cartella di download, che rimanda al repository qui sotto.

Repository degli autori con i pacchetti di installazione, letto il 2026-10-01: `https://github.com/xorgol/Ramsete_Ultimo`. Autorevole sulla modalità dimostrativa senza chiave hardware, con precisione ridotta e funzioni avanzate limitate, corrispondente a Ramsete Lite. La sua cartella `dowload/OldVersions`, letta lo stesso giorno, contiene `Ramsete27b.zip`, scaricato e confrontato per impronta con la copia del corredo in MS-173. Il file `dowload/readme.md`, letto, dice che serve un file `ramsete.key` e che il programma si acquista tramite Spectra.

Pagina di download di `ramsete.com`, letta il 2026-10-01: `http://ramsete.com/download.htm`. Contiene soltanto collegamenti, e non dichiara condizioni di licenza.

Pagina di Ramsete presso l'Università di Parma: `http://pcfarina.eng.unipr.it/ramsete/`. Elencata dalla ricerca e non letta, perché lo strumento di lettura impone HTTPS e il server rifiuta la connessione sulla porta 443.

Distributore italiano Spectra: `https://www.spectra.it/prodotti/software/ramsete/`. Nominato dal readme degli autori come canale d'acquisto e non letto.

## Backup di macchina

Guida di Veeam Agent for Linux, pagina "Types of Backup Files", letta il 2026-09-30: `https://helpcenter.veeam.com/docs/agentforlinux/userguide/backup_files.html`. È autorevole sulle tre estensioni dei file di backup, cioè `.vbk` per il pieno, `.vib` per l'incrementale e `.vbm` per i metadati aggiornati a ogni sessione, ed è la fonte dell'esclusione di PA-013 in MS-169.

Elenco delle estensioni dei file Veeam sul sito della comunità Veeam: `https://community.veeam.com/blogs-and-podcasts-57/veeam-file-extensions-6020`. Elencato dalla ricerca del 2026-09-30 e non letto; la guida ufficiale qui sopra basta al perimetro di PA-013, che riguarda il solo agente per Linux.

## Catena di ingresso audio

Le settantasei fonti, quarantasette delle quali lette, della valutazione di PA-012 del 2026-09-30, fra pagine dei produttori, sorgenti del kernel Linux, manuali, rivenditori e forum, ciascuna con ciò per cui è autorevole e con lo stato di lettura, sono registrate in fondo alla pagina `docs/20-catena-di-ingresso.md` del progetto gemello `home-recording-training-mixing-setup`, a cui la valutazione appartiene. Non si duplicano qui, perché due copie di un registro divergono.

## Crossover

Le sei fonti del confronto fra crossover passivo e attivo, cioè Linkwitz Lab, Elliott Sound Products e il manuale di VituixCAD lette il 2026-10-01, Self 2020 dal materiale di studio locale, e due testi citati da Self e non letti, cioè Self 2018 sui crossover attivi e l'articolo di Linkwitz del 1976 sul JAES, sono registrate con lo stato di lettura in fondo a `docs/52-crossover-passivo-o-attivo.md`, e sono le stesse della bibliografia del report.

## Strumenti di ricerca

Dal 2026-10-01 i tre strumenti non sono più nel progetto, per ADR-031; le fonti restano registrate perché sono quelle su cui la scelta è stata presa. Le fonti operative dei tre strumenti, elencate dal runbook `INTEGRAZIONI-TOOL.md` del pacchetto `academic-researcher` e non lette: il server MCP ufficiale di OpenAlex, `https://github.com/ourresearch/openalex-mcp-server`; PaperQA2, `https://github.com/Future-House/paper-qa`; Feynman, `https://github.com/Companion-Inc/feynman`. Il pacchetto npm `@companion-ai/feynman` è stato interrogato con `npm view` il 2026-10-01, che ha restituito come ultima versione la 0.5.19, quella installata.

## Materiale di studio dell'utente

I libri e gli appunti su cui si costruisce la base di conoscenza, sedici documenti del primo lotto, sono registrati con percorso di origine e impronta SHA-256 in `_notes/fonti-studio/lotto-01-origine.json`, che è locale come il materiale stesso per ADR-028. Le voci bibliografiche dei libri citati dal report si scrivono con `book-bib-extract`, soltanto dopo la conferma dell'utente sul colophon.

## Sistema di progetto

Le fonti su cui poggiano i due pacchetti istanziati il 2026-09-30 non si duplicano qui: stanno nei registri che i pacchetti portano con sé, cioè `docs/anti-slop/FONTI.md` per i segni del testo generato e `docs/separazione-ambienti/FONTI.md` per il modello di ADR-024, dove le sigle C8, F13, F16 e C1 sono quelle citate da quella decisione.

Strumento di verifica dello stato del disco usato per la diagnosi dell'SSD: `https://crystalmark.info/en/software/crystaldiskinfo/`

## Interfaccia audio

Guida utente della Scarlett 2i2 di seconda generazione: `https://fael-downloads-prod.focusrite.com/customer/prod/downloads/Scarlett%202i2%202nd%20Gen%20User%20Guide%20v1.1%20English%20-%20EN.pdf`

Pagina dei download del prodotto: `https://downloads.focusrite.com/focusrite/scarlett-2nd-gen/scarlett-2i2-2nd-gen`

## Akabak e VACS

Pagina del prodotto: `https://www.randteam.de/AKABAK3`

Pagina di download e registrazione: `https://www.randteam.de/AKABAK3/Ak21.html`

Pacchetto degli esempi: `https://www.randteam.de/AKABAK3/AKABAK-Examples.html`

Download della versione professionale, dai link forniti dall'autore con la student license: `https://www.randteam.de/_Software/Akabak_Pro/Download-AKABAK3.html` e `https://www.randteam.de/_Software/VACS2/Download-VACS.html`

Discussione di comunità sull'esecuzione di Akabak sotto Wine: `https://www.diyaudio.com/community/threads/running-akabak.235846`

## Famiglia EASE

Download gratuito di EASE Focus 3: `https://www.afmg.eu/en/ease-focus-3-free-download`

Modelli GLL di costruttori, scaricabili senza registrazione, usati il 2026-09-15 per la prova di compatibilità di MS-114: `https://audiocenter.com/ease-downloads/`. La pagina elenca archivi per singolo prodotto, con date che arrivano al 2026, ed è utile proprio perché consente di procurarsi un modello recente senza aprire un account, cosa che diversi costruttori richiedono.

## Microfoni di misura

MiniDSP UMIK-1, microfono USB omnidirezionale calibrato: `https://www.costruireaudio.com/minidsp-umik-1-microfono-usb-omnidirezionale-calibrato-per-misurazione.html`

Behringer ECM8000: `https://www.behringer.com/product.html?modelCode=0506-AAA`

Dayton Audio EMM-6, con nota sul file di calibrazione serializzato scaricabile dal sito del costruttore inserendo il numero di serie del microfono: `https://www.costruireaudio.com/dayton-audio-emm-6-electret-measurement-microphone-it-it.html`

## Toolbox per Octave e MATLAB

Acoustics Toolbox: `https://oalib.hlsresearch.com/AcousticsToolbox/`

Auditory Modeling Toolbox: `https://sourceforge.net/projects/amtoolbox/`

ITA-Toolbox dell'Istituto di Acustica Tecnica della RWTH di Aachen: `https://git.rwth-aachen.de/ita/toolbox`

## Comunità e riferimenti generali

Elenco ragionato di strumenti per la progettazione di diffusori, dal forum diyAudio: `https://www.diyaudio.com/forums/software-tools/324068-speaker-design-comprehensive-list-recommended-design-tools.html`

Audio Science Review, forum di misure e recensioni strumentali: `https://www.audiosciencereview.com/forum/index.php?Audio+Reviews/`

## Rilievo tridimensionale della stanza

Fonti raccolte il 2026-09-21 per PA-020, e a differenza di tutte quelle qui sopra queste sono state consultate davvero e non trascritte dal documento sorgente. La distinzione va conservata, perché l'avvertenza in testa a questa pagina vale per le altre sezioni e non per questa.

Documentazione e supporto di Scaniverse, da cui provengono i requisiti su Android, cioè Android 7 o superiore, almeno 4 GB di memoria e il supporto ad ARCore con l'interfaccia di profondità, la dichiarazione che i dispositivi privi di sensore di profondità possono usare la modalità fotogrammetrica, e l'elenco dei formati di esportazione delle mesh, cioè OBJ, FBX, USDZ e LAS: `https://dev.scaniverse.com/support`

Pagina dell'applicazione sullo store, per la disponibilità su Android: `https://play.google.com/store/apps/details?id=com.nianticlabs.scaniverse`

Confronto fra le applicazioni gratuite e la questione dei limiti di esportazione, da cui viene il dato che il piano gratuito di Polycam esporta soltanto in GLTF: `https://www.kiriengine.app/blog/Best_Free_3D_Scanner_Apps_2026` e `https://www.skyebrowse.com/news/posts/polycam-review`

Confronto diretto fra Polycam e Scaniverse, da cui viene l'osservazione che il supporto Android di Polycam è meno curato di quello iOS: `https://www.skyebrowse.com/news/posts/polycam-vs-scaniverse`

Assenza di un sensore di profondità dedicato sui modelli Ultra di Samsung dopo la serie S20, con il supporto all'interfaccia di profondità di ARCore come alternativa software: `https://www.simplywise.com/blog/which-android-phones-scan-rooms/`

L'interfaccia dell'applicazione sul dispositivo, osservata il 2026-09-21 su Galaxy S25 Ultra e registrata in MS-159, da cui vengono la dichiarazione che l'esperienza `Classic` è gratuita e senza account richiesto con elaborazione e archiviazione sul dispositivo, e il fatto che l'esperienza nuova sia orientata agli splat gaussiani e dichiari le funzioni di `Classic` come non ancora presenti. È la fonte di rango più alto fra quelle di questa sezione, perché è il programma che parla di sé sul dispositivo reale invece di una pagina che lo descrive, e per questo promuove a fatto due dati che prima venivano da articoli di terze parti. Non copre l'esportazione, che resta da vedere.

Sulla natura di queste fonti va detto che cosa sono e che cosa non sono, perché la gerarchia conta. La documentazione del produttore di Scaniverse è la fonte autorevole sui requisiti e sui formati, e da essa vengono tutti i dati tecnici usati per la scelta. Le altre sono articoli di confronto di terze parti, cioè fonti di livello basso: servono a sapere che un limite esiste e vanno riverificate sul piano tariffario del produttore prima di farne discendere una spesa. Il dato sull'assenza del sensore sul Galaxy S25 Ultra è coerente fra le fonti consultate e con la storia dei modelli precedenti, e resta comunque verificabile in trenta secondi sul dispositivo guardando se una applicazione di scansione offra o no una modalità basata su sensore.

## DAW pilotabile dall'agente: SoundCraft

Voci aggiunte il 2026-10-26 per PA-034, tutte lette quel giorno, per intero o per estratti come indicato.

README del repository ufficiale, letto per intero insieme ai metadati dell'API GitHub dello stesso giorno: licenza rilevata Apache-2.0, ultimo push il 2026-10-26, 2351 fork. È la fonte dei formati di rilascio per Linux, dei dispositivi audio supportati, cioè CoreAudio, WASAPI, ALSA e WebAudio senza nessuna menzione di JACK o PipeWire, dei plugin CLAP, VST3 e AU senza LV2, dell'obbligo di togliere nome e loghi ArtCraft in un fork e della stima di circa il 40% di un sostituto reale di Pro Tools: `https://github.com/storytold/soundcraft`

Manifesto del crate di riproduzione, letto per intero: cpal con la sola feature opzionale `asio`, nessuna feature `jack`. `https://github.com/storytold/soundcraft/blob/main/crates/playback/Cargo.toml`

Sorgente della scelta del dispositivo, letto per estratti: scelta per macchina di host, dispositivo, frequenza e buffer da 32 a 8192 campioni. Il commento nomina JACK fra gli host possibili, ma la presenza di JACK dipende dalle feature di compilazione. `https://github.com/storytold/soundcraft/blob/main/crates/playback/src/devices.rs`

Registro delle lacune dichiarate da upstream, letto per estratti. È la fonte di G-01, che come blocco dell'alpha elenca la mancanza di JACK e della verifica su macOS e Linux, con il mix a blocchi fissi di 512 campioni, e di G-14, secondo cui Linux è esercitato poco a runtime. `https://github.com/storytold/soundcraft/blob/main/docs/gaps.md`

Analizzatore di spettro con Raspberry Pi Pico, articolo di Martin Ossmann pubblicato da Futuranet il 2026-10-15, letto per intero il 2026-10-26 con `curl` e uno user agent da browser, dopo che il recupero ordinario aveva restituito 403. Usa l'ADC interno dell'RP2040 a 12 bit e 500 kS/s, la finestra di Blackman e la FFT con N da 1024 a 16384, e trasmette i dati al PC in seriale a 115200 baud. Il software si scarica dalla pagina Elektor dell'articolo, non letta. È valutato come sottoprogetto in PA-004 del gemello. `https://futuranet.it/progetti/2026/10/15/raspberry-pi-pico-come-analizzatore-di-spettro/`, software alla pagina `https://www.elektormagazine.com/magazine/elektor-312/62150`

## Materiale non pubblico

Gli appunti di una conversazione del luglio 2024 con un collega esperto di acustica degli ambienti, da cui provengono le osservazioni sulla forma della stanza, sul soffitto spiovente e sulla parete alle spalle del punto di ascolto, restano nei materiali locali del progetto e non sono versionati.

La corrispondenza con l'autore di Akabak, che contiene il release code della licenza, resta nei materiali locali per le ragioni indicate nella pagina delle licenze.

## Ricognizione e proposta della catena condivisa, 2026-11-17

Fonti primarie lette: Ubuntu Studio Audio Configuration (`https://ubuntustudio.org/audio-configuration/`) per la regolazione di PipeWire; documentazione kernel intel_pstate (`https://docs.kernel.org/admin-guide/pm/intel_pstate.html`) per la distinzione fra policy e frequenza fissa; changelog Ubuntu cpupower-gui (`https://lists.ubuntu.com/archives/resolute-changes/2026-September/029924.html`) per le correzioni del servizio; Behringer UMC1820 (`https://behringer.com/en/products/0805-AAN`) per ingressi e uscite; repository CamillaDSP (`https://github.com/HEnquist/camilladsp`) per filtri, mixer e controllo di volume; schede SB16PFCR25-8 (`https://sbacoustics.com/wp-content/uploads/2024/01/6in-SB16PFCR25-8.pdf`) e SB26STCN-C000-4 (`https://sbacoustics.com/wp-content/uploads/2020/02/SB26STCN-C000-4.pdf`) per parametri dichiarati, non misurati sugli esemplari.

Pagine commerciali lette per prezzo e disponibilità, validità limitata alla fotografia odierna: Thomann Italia UMC404HD 98 €, UMC1820 175 €, A800 179 € e 3-4 settimane; SoundImports SB16PFCR25-8 31,45 € disponibile, SB26STCN-C000-4 36,45 € esaurito, EMM-6 78,45 € esaurito con rientro indicato il 18 dicembre. Collegamenti e limiti di IVA e spedizione nella proposta. Kirstein ST-120 (`https://www.kirstein.de/Studiomoebel/Stagecaptain-ST-120-Studiotisch.html`) conferma due moduli rack da 3U; non si deducono da questo le quote effettive della postazione montata. Le proprietà del microfono sono confrontate con la guida ufficiale Dayton indicata nella proposta. Il PDF Music Tribe UMC404HD trovato dal motore di ricerca non è stato letto: recupero web fallito con 502; nessun dettaglio esclusivo di quel PDF è promosso a verificato. Nessun paper aggiunto alla bibliografia della tesi.

## Quote Stagecaptain ST-120, 2026-11-17

Letti il manuale ufficiale versione 01.2025 (`https://www.kirstein.de/docs/manuals/00106799/manual_EN.pdf?h=1ecf4368fd8ab20c3c92818e95c8e66c`) e la pagina prodotto con la sua immagine quotata (`https://www.kirstein.de/Studiomoebel/Stagecaptain-ST-120-Studiotisch.html`). Il PDF è stato scaricato via curl dopo il fallimento del lettore web e del proxy nel sandbox; testo estratto e pagina 7 ispezionata come immagine per identificare il pezzo 2. La figura ufficiale quotata (`https://img.kirstein.de/out/pictures/generated/product/9/2000_2000_75/6570c468a762c122194f883e11b84239_9.jpg`), letta visivamente nella pagina prodotto, mostra ripiano superiore 118 × 30 cm, quota 93 cm e piano principale 118 × 60 cm. Fonte verificata per queste quote, non per la disposizione nella stanza o per le dimensioni dello schermo. Copia del manuale e prova visiva nel livello privato. Il limite della profondità con cabinet ruotati è calcolo del progetto, non una dichiarazione del produttore.

## Scelta dello schermo, 2026-11-17

Fonti primarie lette: Dell P2425H (`https://www.dell.com/en-gb/shop/dell-24-monitor-p2425h/apd/210-bmff/`), Dell P2725D (`https://www.dell.com/en-us/shop/Monitors/apd/Dell-Pro-P-27-QHD-Monitor---P2725D/p2725d_monitor/-`) e P3223DE (`https://www.dell.com/en-gb/shop/p3223de-monitor/apd/210-bdgb/`) per formato, risoluzione e dimensioni; manuale ufficiale Philips 24E1N1100A e famiglia (`https://www.documents.philips.com/assets/20241209/4601f6a3000541aa84d0b24100909f9e.pdf`), in particolare pagine fisiche 10 e 18-21 per regolazioni, dimensioni e condizioni del consumo; scheda Philips 27E1N1600AE (`https://www.documents.philips.com/assets/20240328/705dcf330a63436b894bb141000cd47a.pdf`) per l'esempio QHD poi mantenuto opzionale. Le schede EPREL `https://eprel.ec.europa.eu/fiches/electronicdisplays/Fiche_1865623_EN.pdf` e `https://eprel.ec.europa.eu/fiches/electronicdisplays/Fiche_2173550_EN.pdf` dichiarano rispettivamente 11,7 W SDR classe C per P2425H e 18,8 W SDR classe E per P2725D, entrambe 0,3 W in standby. Questi sono dati di modelli precisi, non proprietà necessarie di una risoluzione. Densità di pixel e ingombri sono calcoli del progetto. Prezzi, catalogo e stock Esprinet non verificati; richiesta di preventivo affidata all'utente, senza comunicazioni esterne dell'agente.

## Preparazione CAD e collaudo DSP, 2026-11-18

Fonti primarie lette: rilascio CamillaDSP 4.1.3 (`https://github.com/HEnquist/camilladsp/releases/tag/v4.1.3`), metadati dei suoi asset e documentazione della stessa versione (`https://github.com/HEnquist/camilladsp/blob/v4.1.3/README.md`) per backend su file, mixer, BiquadCombo e opzioni CLI. Gli archivi Windows e Linux sono stati scaricati e verificati contro le impronte pubblicate, prima del collaudo. FreeCAD 1.1.4 (`https://github.com/FreeCAD/FreeCAD/releases/tag/1.1.4`) e API del rilascio per il canale AppImage, dimensione e impronta: individuato, non scaricato né provato sulla macchina. La pagina download freecad.org non è stata letta per rifiuto 403; la disponibilità dichiarata si fonda sul rilascio ufficiale GitHub, non su quella pagina. Le misure dei filtri vengono dalle esecuzioni conservate privatamente, non dai valori teorici del README.

## Strumenti posseduti e CAD, giro 2026-11-18/19

Marshall MG10 & MG15 Owners Manual: scansione fornita dall'utente, dieci pagine; originale e impronta nel livello privato. PdfCraft 0.21.1, OCR seguito da verifica visiva di copertina e pagina PDF 7 per le specifiche. Nessun altro file della cartella personale acquisito. Studio Fender precedente: esportazione integrale privata, trattata come appunti da verificare, non come fonte del circuito. Il file originale nominato è stato rimosso solo dopo acquisizione e verifica.

Manuale ufficiale [Fender Frontman 65R](https://www.fmicassets.com/Damroot/Original/10001/OM_leg_gtramp_Frontman_65R.pdf), sezione italiana stampata 12-13, letto per i punti di accesso e le specifiche dichiarate; corrispondenza con l'esemplare da confermare. Julius O. Smith, [Minimum-Phase Filters](https://www.dsprelated.com/freebooks/filters/Minimum_Phase_Filters.html), letto sulla copia pubblica del libro per distinguere fase minima e LTI. Il primo recupero dal sito Stanford è fallito e non viene dichiarato letto.

[FreeCAD 1.1.4](https://github.com/FreeCAD/FreeCAD/releases/tag/1.1.4): rilascio e descrittore ufficiali per il binario scelto. Versione, formati e comportamento vengono dai collaudi della macchina e dai file riaperti, non dalle note del rilascio. La pagina `docs/10-ambiente/freecad-collaudo-native.md` conserva sequenza, misure e limiti.

## Fonti del servizio DSP e del banco, verificate il 2026-11-19

Per i profili del cabinet è stato letto il [README ufficiale CADCraft, sezione Fonts](https://github.com/storytold/cadcraft#fonts), che descrive la risoluzione dei caratteri installati per nome del file o della famiglia. Versione locale 0.20.1 e proprietà trueType sono state misurate con la CLI, non dedotte dal documento corrente a monte. La geometria e le quantità dei pannelli sono calcoli e collaudi del progetto.

Il [protocollo WebSocket CamillaDSP 4.1.3](https://github.com/HEnquist/camilladsp/blob/v4.1.3/websocket.md), il [backend PipeWire della stessa versione](https://github.com/HEnquist/camilladsp/blob/v4.1.3/backend_pipewire.md) e il [README fissato alla versione](https://github.com/HEnquist/camilladsp/blob/v4.1.3/README.md) sostengono comandi, nodi senza autoconnect e rampa Main. Il [rilascio ufficiale](https://github.com/HEnquist/camilladsp/releases/tag/v4.1.3) è la provenienza del binario PipeWire con impronte riportate nella procedura.

La [API sincrona websockets 15.0.1](https://websockets.readthedocs.io/en/15.0.1/reference/sync/client.html) sostiene connessione locale, proxy disattivato e timeout; la dipendenza era già presente. Il [sorgente ufficiale pw-cat 1.6.2](https://github.com/PipeWire/pipewire/blob/1.6.2/src/tools/pw-cat.c), rami on_process e fine main, riscontra l'uscita 1 al limite campioni senza drained. La [pagina ufficiale pw-cli](https://docs.pipewire.org/devel/page_man_pw-cli_1.html) distingue comando singolo e modalità interattiva; la [pagina pw-dump](https://docs.pipewire.org/page_man_pw-dump_1.html) definisce il dump dello stato. I risultati numerici del banco sono misure locali, non dati di questi manuali.

## Crossover e piattaforme, 2026-11-20

[Linkwitz Lab, Active Filters](https://www.linkwitzlab.com/filters.htm) è fonte tecnica prioritaria per indicazione esplicita dell'utente, ADR-050. Lettura delle sezioni LR2/LR4 e riferimenti alla correzione del ritardo; non dichiarata la lettura dell'intero sito. Scheda con copertura e studio successivo in [linkwitzlab-active-filters.md](../../research-vault/web/linkwitzlab-active-filters.md).

Il [registro del confronto](../../research-vault/crossover-pc-pi-analogico/sources.md) collega W3C Audio EQ Cookbook, nota applicativa TI SLOA049D, documentazione ufficiale Raspberry Pi e la review AES di Cecchi e coautori, DOI 10.17743/jaes.2022.0100. I passaggi consultati e i limiti sono dichiarati per fonte; le simulazioni originali non sono misure dei monitor. Il [dossier matematico](../62-confronto-crossover-e-verifica-matematica.md) distingue formule, risultati riproducibili e collaudo hardware ancora aperto.

Il [registro del sistema autonomo](../../research-vault/sistema-autonomo-20261120/sources.md) aggiunge manuale UMC1820, dati SB16/SB15/SB26, finali e switch, metodi di stima da foto e prezzi dei componenti rilevati il 20 novembre. La [proposta con calcoli e protocollo](../63-sistema-autonomo-driver-e-collaudo.md) e i [PDF LaTeX](../latex/README.md) mantengono separati datasheet, risultati originali, stime e prove hardware da eseguire.

## Identità e punti d'uso, 2026-11-20

La [mappa del pedigree](fonti-progetto.md) attribuisce identificativi permanenti ai riferimenti e collega versione, copertura della lettura e usi con file, sezione e riga. Il JSON completo è `research-vault/usi-fonti-progetto.json`; i metadati curati sono in `research-vault/anagrafiche-fonti-web.json`. La bibliografia storica resta `research-vault/fonti.json`, senza ricostruire il registro o rileggere la biblioteca privata. Le fonti storiche censite automaticamente sono dichiarate da riconciliare; nessuna promozione automatica a lette o verificate. [Metodo e lezioni](metodo-fonti-lezioni-riordino.md) spiegano la distinzione e la conservazione delle prove.
