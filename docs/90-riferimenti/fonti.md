# Fonti

> Riferimenti citati nel documento sorgente, raccolti per argomento. Nessuno di questi indirizzi è stato recuperato durante la conversione: sono trascritti dal sorgente e dai file di collegamento presenti nella cartella del progetto, e vanno verificati al momento dell'uso.

## Sistema operativo e ambiente

Distribuzione e download: `https://ubuntustudio.org/download/`

Panoramica delle funzionalità audio della distribuzione: `https://ubuntustudio.org/tour/audio/`

Metapacchetto per aggiungere l'ambiente Studio a una Ubuntu normale: `https://ubuntustudio.org/ubuntu-studio-installer/`

Annuncio del rilascio di Ubuntu Studio 26.04 LTS, letto il 2026-09-30 ed è la fonte del periodo di supporto del flavor, cioè tre anni fino ad aprile 2029, più breve dei cinque della base Ubuntu: `https://ubuntustudio.org/2026/04/ubuntu-studio-26-04-lts-released/`. È la sola voce di questa sezione recuperata e letta, a differenza di quanto dice la nota in testa per le altre.

Note di rilascio della base Ubuntu 26.04 LTS: `https://documentation.ubuntu.com/release-notes/26.04/`. Elencata dalla ricerca del 2026-09-30 sul periodo di supporto e non letta: il supporto della base resta quindi affermato da ADR-006 e non da questa pagina.

Discussione sull'annuncio di Ubuntu Studio 26.04 LTS e note di rilascio sul forum della comunità Ubuntu: `https://discourse.ubuntu.com/t/ubuntu-studio-26-04-lts-released/80832` e `https://discourse.ubuntu.com/t/ubuntu-studio-26-04-lts-release-notes/79113`. Elencate dalla stessa ricerca e non lette.

## Backup di macchina

Guida di Veeam Agent for Linux, pagina "Types of Backup Files", letta il 2026-09-30: `https://helpcenter.veeam.com/docs/agentforlinux/userguide/backup_files.html`. È autorevole sulle tre estensioni dei file di backup, cioè `.vbk` per il pieno, `.vib` per l'incrementale e `.vbm` per i metadati aggiornati a ogni sessione, ed è la fonte dell'esclusione di PA-013 in MS-169.

Elenco delle estensioni dei file Veeam sul sito della comunità Veeam: `https://community.veeam.com/blogs-and-podcasts-57/veeam-file-extensions-6020`. Elencato dalla ricerca del 2026-09-30 e non letto; la guida ufficiale qui sopra basta al perimetro di PA-013, che riguarda il solo agente per Linux.

## Catena di ingresso audio

Le settantasei fonti, quarantasette delle quali lette, della valutazione di PA-012 del 2026-09-30, fra pagine dei produttori, sorgenti del kernel Linux, manuali, rivenditori e forum, ciascuna con ciò per cui è autorevole e con lo stato di lettura, sono registrate in fondo alla pagina `docs/20-catena-di-ingresso.md` del progetto gemello `home-recording-training-mixing-setup`, a cui la valutazione appartiene. Non si duplicano qui, perché due copie di un registro divergono.

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

## Materiale non pubblico

Gli appunti di una conversazione del luglio 2024 con un collega esperto di acustica degli ambienti, da cui provengono le osservazioni sulla forma della stanza, sul soffitto spiovente e sulla parete alle spalle del punto di ascolto, restano nei materiali locali del progetto e non sono versionati.

La corrispondenza con l'autore di Akabak, che contiene il release code della licenza, resta nei materiali locali per le ragioni indicate nella pagina delle licenze.
