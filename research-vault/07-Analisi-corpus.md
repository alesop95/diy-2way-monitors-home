---
tipo: analisi
aggiornato: 2026-10-05
---
# Analisi di copertura del corpus di studio

Analisi in sola lettura del materiale convertito nella cache `_notes/.tmp-doc-cache/fonti/`, fatta il 2026-10-05 dal manifesto (`manifest.json`, 1208 voci per impronta), dall'indice di Livello 1 (`_INDEX.md`), dai file `fonti-locali/lotto-*-origine.json` e da `fonti-locali/piano-lotti.md`. Il disco `J:` non è stato aperto. Dove l'indice non porta intestazioni, cosa che accade per 908 dei 957 PDF, il giudizio viene dal titolo del file e, per i soli testi indicati, dal conteggio di pochi termini cercati nel mirror con un'espressione regolare (per esempio `biquad`, `limit cycle`, `vented`, `diffraction`, `room mode`); un conteggio dice che un argomento è nominato, non che è trattato bene, e quando è l'unica prova la cella lo dichiara come da verificare. La libreria JabRef di `fonti.json` porta solo metadati senza PDF e qui non conta come copertura locale; i 29 paper di `tracked-sources.md` sono richiamati solo dove colmano una lacuna.

## 1. Che cosa contiene il corpus

| Lotto | Documenti | Propri | Parole | Formule | Scansioni |
|---|---|---|---|---|---|
| lotto-01 | 16 | 0 (4 per nome) | 1 857 910 | 6 248 | 1 |
| lotto-02 | 123 | 5 | 3 534 793 | 4 442 | 37 |
| lotto-03 | 119 | 2 | 4 379 334 | 0 | 3 |
| lotto-04 | 64 | 17 | 2 404 896 | 859 | 16 |
| lotto-05 | 81 | 49 | 809 695 | 220 | 23 |
| lotto-06 | 322 | 10 | 6 028 860 | 150 | 64 |
| lotto-07 | 33 | 5 | 269 835 | 119 | 5 |
| lotto-08 | 51 | 29 | 1 066 822 | 7 871 | 3 |
| lotto-09 | 31 | 24 | 716 550 | 1 515 | 2 |
| lotto-archivi | 368 | 0 (non marcati) | 15 687 375 | 2 990 | 53 |
| Totale | 1 208 | 141 | 36 756 070 | 24 414 | 207 |

La colonna Propri conta le voci con `proprio: true` nei file di origine; il lotto 01 e il lotto degli archivi non portano il campo, ma per nome il primo contiene quattro appunti dell'utente (EEASE I, EEASE II, EEASE Exercises, l'esercizio sul CMRR) e il secondo è in gran parte la cartella `Tesi Sopranzi`, cioè materiale della tesi magistrale. Le formule si contano solo sui 146 documenti convertiti con pandoc, cioè i `.docx`, quindi la colonna misura gli appunti e non i libri, e il lotto 03 ne riporta zero perché il suo unico appunto lungo, `Linkwitz-Riley crossover Active.docx`, non contiene espressioni LaTeX; le parole degli archivi sono gonfiate da fogli `.xlsx` di dati della tesi (un solo file vale 4,9 milioni di parole). Le scansioni sono le voci sotto le 50 parole, in attesa di OCR[^1]; 17 voci portano inoltre un errore di conversione, quasi tutte `.pptx` o PDF del lotto 04.

Il corpus è fatto di due strati diversi. Sopra stanno i manuali di riferimento, convertiti come testo senza gerarchia di intestazioni (Colloms, Borwick, Beranek e Mellow, Kleiner, Toole, Kuttruff, Oppenheim e Schafer, Lyons, Diniz), che coprono quasi ogni argomento ma non dicono dove; sotto stanno gli appunti dell'utente sui corsi del Politecnico di Milano, pochi documenti con molte formule e una struttura per capitoli leggibile dall'indice, che sono il taglio della tesi.

## 2. Gli appunti dell'utente, cioè il taglio

Elenco per numero di formule, con le intestazioni di primo e secondo livello viste nell'indice.

- Musical Acoustics - Part I (lotto-08, 3 869 formule, 131 061 parole): sistemi discreti, sistemi continui a una e due dimensioni (corde, membrane, piastre rettangolari e circolari, piastre incastrate, piastre di legno, gusci), propagazione, "Normal modes in enclosures", sorgenti multipolari, radiazione da sorgenti piane in schermo e senza schermo, tubi, trombe e cavità, analoghi di rete; poi strumenti musicali, che il motivo di inclusione esclude. Fonda le appendici D ed E, e con le piastre è l'unico appunto che tocca il capitolo 06.
- EEASE I (lotto-01, 2 490 formule): catena di elaborazione audio, impostazione del guadagno e amplificatore differenziale, CMRR[^2], slew rate, rumore elettronico, "Filters, Tone control, Equalizers" con il filtro attivo a retroazione, mixer, valvole, stadi d'uscita e amplificatori di potenza. Fonda l'appendice B e il paragrafo sul filtro analogico del capitolo 04.
- EEASE Exercises (lotto-01, 1 914 formule): otto lezioni del 2019 (impedenza di sorgente, preamplificatore e INA, rumore, stadi d'uscita, microfoni, altoparlanti) e appendici su analisi per piccoli segnali, accoppiamento AC e DC, impedenza d'ingresso, diagrammi di Bode. Fonda l'appendice B; la lezione 8 tocca l'appendice E.
- EEASE II (lotto-01, 1 725 formule): impedenza d'uscita degli stadi finali, microfoni, "Mechanical quantities, elements and systems", "Acoustical quantities, elements and systems", trasduttore elettromagnetico-meccanico e meccano-acustico, "The full electrical model of a loudspeaker", direzionalità dei microfoni. Fonda l'appendice E e la parte sui parametri del capitolo 05.
- Fundamentals of Acoustics (lotto-08, 1 594 formule): oscillatore libero e forzato, Fourier, equazione delle onde, onde piane e sferiche, intensità e livello, monopolo, dipolo, quadrupolo, array lineare, riflessione e fattore di riflessione, sfera pulsante, sorgente lineare e piana, "Radiation from a plane circular piston", "Diffraction/Scattering", tubi, linee di trasmissione, risonatori, trombe. Fonda l'appendice D e la radiazione del pistone che serve alla direttività del capitolo 05. Il campo `proprio` non è marcato ma il file è citato come appunto proprio nella richiesta dell'utente.
- ESE-FOA (lotto-08, 1 406 formule): esercizi svolti su corde, onde nei gas, intensità, riflessione normale, diffrazione, interferenza, sorgenti multiple, battimenti, tubi. Appendice D.
- Acustica applicata (lotto-04, 854 formule): il mirror non ha intestazioni; le righe iniziali trattano sorgente, propagazione e ricevitore, livello di pressione, potenza e intensità, analisi per bande, e i termini riverberazione (99 occorrenze), Sabine (13) e assorbimento (157) indicano una parte di acustica degli ambienti, da verificare. Candidata per l'appendice D e per i capitoli 01 e 02.
- Tesi magistrale 2020 (lotto-09, 632 formule, con il backup a 652): background e stato dell'arte, metodologia, valutazione, appendice sulla forza elettromotrice. Fonda la forma della tesi e il capitolo 08 per la parte di test d'ascolto e di caratterizzazione per feature.
- Elettricità e magnetismo (lotto-08, 506 formule): elettrostatica, elettrodinamica e magnetismo. Appendice C; il file non è marcato proprio e va confermato con l'utente.
- Gli appunti brevi: Limiti con Taylor (136 formule, appendice A), Loudspeaker Seminar 13/05/2019 sui driver (132 formule: circuiti equivalenti, "Thiele-Small circuit for loudspeaker", comportamento non lineare, misure delle prestazioni; capitolo 05 e appendice E), The Electro-mechanical acoustic model of an Electrodynamic Loudspeaker (110 formule: parte elettromeccanica, modello completo, riporto dell'ammettenza di radiazione al lato meccanico; appendice E), Misure Elettroniche lezione 9 sui parametri RLC reali (90 formule) con le altre lezioni su incertezza, conversione AD e analizzatori di spettro (capitolo 08, appendice B), Why L-PAD and impedance matching XOVER (33 formule, capitolo 04 passivo), Linkwitz-Riley crossover Active (nessuna formula: compressione multibanda e realizzazione del Linkwitz-Riley; capitolo 04).

Ne segue che gli appunti fondano con certezza le appendici B, D ed E e la parte elettroacustica del capitolo 05; toccano il capitolo 04 solo dal lato analogico e il capitolo 06 solo attraverso le piastre di Musical Acoustics; non contengono nulla di riconoscibile su crossover digitale, quantizzazione o equalizzazione della stanza, che dovranno appoggiarsi ai libri e alla letteratura.

## 3. Copertura per capitolo e appendice

| Capitolo | Fonti locali principali | Copertura | Che cosa manca |
|---|---|---|---|
| 00 Introduzione | Genelec 3777 e 5939 (lotto-02), Keele Monitor Loudspeaker Systems 1981 e 1983 (lotto-02), Newell e Holland (lotto-02), Toole (lotto-04) | parziale | Stato dell'arte recente dei monitor attivi con DSP, che nessun titolo del corpus copre dopo il 2018 |
| 01 Misura reale della stanza | Farina 2000, 2007, 2009 e Novak 2010, 2015 sugli sweep (lotto-05), Impulse response measurement techniques (lotto-05), Redaelli, strumento di misura dei parametri acustici (lotto-04), Ferroni, modi a bassa frequenza in stanze piccole (lotto-04), appunti di Misure Elettroniche (lotto-05), Acustica applicata (lotto-04) | parziale | Pratica della misura in stanza: media spaziale su più punti, posizione e calibrazione del microfono, finestratura, risposta stazionaria contro risposta precoce; nessun titolo specifico oltre le due tesi |
| 02 Modello della stanza, modi | Kuttruff Room Acoustics, Master Handbook of Acoustics, Ferroni, Geddes Room Modes (lotto-04), Musical Acoustics "Normal modes in enclosures" (lotto-08) | forte | Modi in stanza non rettangolare o con pareti non rigide, da verificare in Kuttruff |
| 02 Modello della stanza, riflessioni precoci | Toole (lotto-04), Room Reflections Misunderstood? AES123 (lotto-04), reflectgeometry (lotto-04), Loudspeaker Placement in Small Rooms (lotto-04) | parziale | Metodo delle sorgenti immagine (Allen e Berkley è solo proposto), interferenza con i confini vicini al diffusore |
| 02 Modello della stanza, equalizzazione | Genelec 12327 e 12592 sull'equalizzazione modale (lotto-04), Parte 12 Equalizzazione sonora del corso di Ancona (lotto-03), lund_give_peaks_a_chance (lotto-04) | parziale | Correzione digitale della stanza in generale e su più punti; i lavori di riferimento (Cecchi 2018, Bank 2008, Kirkeby 1999, Radlović 2000) sono solo proposti |
| 03 Simulazione acustica della stanza | vorlander2008auralization (lotto-05), Kuttruff (lotto-04), dafx_BOOK (lotto-03) | debole | Sorgenti immagine e tracciamento di raggi validati su stanze piccole, metodi ondulatori a bassa frequenza (FEM[^3], BEM, FDTD), confronto fra simulazione e misura; COMSOL è escluso dai lotti |
| 04 Crossover, teoria comune | Linkwitz 1976, Lipshitz e Vanderkooy 1983 e 1986, Bullock, Fink, Garde, Small 1971, Thiele 2001 (lotto-03), Colloms (lotto-02) | forte | Nulla di evidente sul piano analitico |
| 04 Crossover, passivo | Why L-PAD (appunto, lotto-02), thiele2002passive (lotto-03), Dickason (scansione, lotto-02) | parziale | Il Cookbook di Dickason non è leggibile finché non passa all'OCR |
| 04 Crossover, IIR e biquad | Lyons, Smith, Oppenheim e Schafer, Diniz, Zavalishin (lotto-03), MMSP I (lotto-03), Linkwitz-Riley crossover Active (appunto, lotto-03) | forte | Formule pratiche dei coefficienti (Audio EQ Cookbook solo proposto) |
| 04 Crossover, FIR a fase lineare | Keele 2007 parti 1 e 2 (lotto-03), Hawksford 1997 (lotto-03) e 1999 (archivi), Fundamental FIR Filter Concepts, Eclipse Audio 2019 (archivi), white paper Linea Research (archivi), appunto su banda relativa e transizione (lotto-03) | forte | Costo di latenza e lunghezza del FIR alle basse frequenze di incrocio, da verificare nei testi |
| 04 Crossover, allineamento dei ritardi | Lipshitz e Vanderkooy, fink1980time, iborra2018 e 2020, thiele2001phase (lotto-03 e archivi), Perceptual Study of Loudspeaker Crossover Filters (archivi), liski2018 e makivirta2018 (lotto-03) | parziale | Misura del centro acustico e risoluzione del ritardo nel processore; Vanderkooy e Lipshitz 1984 sul time offset è solo proposto |
| 04 Crossover, quantizzazione | Oppenheim e Schafer, Lyons, Diniz (lotto-03), MIT 6.341 su strutture e quantizzazione (lotto-03), Reay (lotto-03) | parziale | Sensibilità dei coefficienti dei biquad a bassa frequenza e alta frequenza di campionamento, rumore delle forme dirette, aritmetica a virgola fissa dei processori commerciali: solo teoria generale, nulla di specifico al crossover |
| 05 Progetto acustico, parametri di Thiele-Small | Seminario 13/05/2019 e EEASE II (appunti), Electro-mechanical model (appunto), Beranek e Mellow, Colloms, Borwick (lotto-02), A MATLAB Tool for Thiele-Small Parameter Fitting, Xmax, Klippel Training 2-5 (lotto-05) | forte | Modelli dell'induttanza della bobina (Leach 2002 solo proposto) |
| 05 Progetto acustico, cassa chiusa e ventilata | Keele sugli allineamenti in cassa ventilata 1972-1975 (lotto-02), Beranek e Mellow, Colloms, Newell e Holland (lotto-02), Closed-Box Loudspeaker Systems di Small (scansione, lotto-02) | parziale | Thiele 1971 e Small 1973 sulla cassa ventilata sono solo proposti, la cassa chiusa di Small è una scansione non letta |
| 05 Progetto acustico, diffrazione | Colloms, Kleiner, Borwick, Newell e Holland (lotto-02, solo per conteggio dei termini), Fundamentals of Acoustics "Diffraction/Scattering" (appunto) | debole | Teoria della diffrazione dal bordo del pannello e compensazione del gradino del pannello: nessun titolo specifico, Vanderkooy 1991 solo proposto |
| 05 Progetto acustico, direttività | Optimizing the directivity index of a two-way loudspeaker (lotto-05), Geddes directivity e What is a Waveguide (lotto-04), FOA pistone circolare (appunto), Keele 2007 parte 2, Toole | parziale | Progetto della guida d'onda del tweeter e accordo di direttività all'incrocio, D'Appolito 1983 sul lobing solo proposto |
| 05 Amplificazione | Self Audio Power Amplifier Design, Cordell, Nyboe 2005 (lotto-03), EEASE I stadi d'uscita (appunto), slide EEASE sulla classe D (scansione, lotto-02) | parziale | Classe D moderna (Putzeys 2005 solo proposto) |
| 06 Progetto meccanico del cabinet | Musical Acoustics, piastre e gusci (appunto, lotto-08), Colloms e Newell e Holland (da verificare) | debole | Risonanze dei pannelli del cabinet, rinforzi, smorzamento a strato vincolato, materiali, radiazione delle pareti: nessun titolo del corpus |
| 07 Simulazione finale nella stanza | genelec_monitors_in-room_performance e sound_pressure_capacity (lotto-04), Toole (lotto-04), vorlander2008auralization (lotto-05) | debole | Uso dei dati polari misurati nella simulazione, previsione della risposta in stanza, ottimizzazione della posizione |
| 08 Costruzione e verifica finale | Keele Nearfield, Log Sampling, ETC, Polarity (lotto-05), AppNote Loudspeaker EA Measurements, Klippel (lotto-05), struck1994 (archivi), merging_nearfield_and_farfield (archivi, appunto della tesi), Bech 2006 e BS.1534 (archivi), D'Appolito Testing Loudspeakers (scansione) | parziale | Pratica costruttiva del cabinet, assente; il testo di D'Appolito sulla misura non è leggibile |
| A Matematica | Osgood, Broughton e Bryan, Gupta, Golub e Van Loan, Cariolaro (lotto-06), appunti propri su Taylor, integrali, studio di funzione (lotto-06), Advanced Engineering Mathematics (archivi), algebra lineare (lotto-06) | forte | Variabile complessa e residui, da verificare: i testi di metodi matematici (Parodi, Codegone, Barozzi) sono scansioni |
| B Elettrotecnica ed elettronica | Principi di ingegneria elettrica, dispense ed esercizi (lotto-07), EEASE I e Exercises (appunti), Basso, Moschytz, Wai-Kai Chen, Self Small Signal (lotto-01), Conversione AD (appunto, lotto-05) | forte | Convertitori sigma-delta: gli appunti di elettronica digitale e di elettronica analogica sono scansioni |
| C Fisica ed elettromagnetismo | Caciuffo e Melone, due volumi (lotto-08), Elettricità e magnetismo (lotto-08), homework su Coulomb, Gauss, Ampère, Faraday, onde (lotto-08) | forte | Griffiths è una scansione; mancano le correnti parassite nel motore dell'altoparlante, da verificare |
| D Acustica | Fundamentals of Acoustics e ESE-FOA (appunti), Musical Acoustics (appunto), Acustica applicata (appunto), Kuttruff Acoustics an introduction (lotto-08), Beranek e Mellow (lotto-02) | forte | Kinsler e Frey è una scansione (archivi) |
| E Elettroacustica | EEASE II, seminario sui driver, Electro-mechanical model (appunti), Beranek e Mellow, Kleiner, Borwick, Eargle, Ballou (lotto-02), Klippel (lotto-05) | forte | Nulla di rilevante oltre le voci del capitolo 05 |
| F Elaborazione numerica del segnale | Oppenheim e Schafer, Diniz, Lyons, Smith, Kahrs e Brandenburg, DAFX (lotto-03), MMSP I e II, MIT 2.161 e 6.341, corso di Ancona sui banchi di filtri (lotto-03), Foundations of Signal Processing (lotto-06), appunti su FFT e zero padding e sulla convoluzione (lotto-05) | forte | Proakis e Manolakis e Mitra sono scansioni |

## 4. Lacune da colmare con la ricerca bibliografica

Stanza e misura.

- Correzione digitale della stanza su più punti di ascolto: `multi-point room equalization`, `room response equalization`, `mixed-phase room correction`.
- Misura della risposta in stanza: `in-room loudspeaker measurement`, `spatial averaging`, `estimated in-room response CTA-2034`.
- Interferenza con i confini vicini al diffusore: `speaker boundary interference response`, `SBIR`, `loudspeaker placement optimization`.
- Bassi in stanza piccola, ottimizzazione di posizione e di più sorgenti: `low-frequency room optimization`, `multiple subwoofer optimization`, `modal room compensation`.
- Simulazione di stanze piccole e sua validazione: `small room acoustic simulation`, `image source validation measurement`, `wave-based FDTD room low frequency`.

Crossover digitale.

- Crossover misti FIR e IIR e correzione della fase in eccesso: `mixed-phase FIR crossover`, `excess phase correction loudspeaker`, `hybrid IIR FIR crossover`.
- Quantizzazione dei biquad nei processori audio: `biquad coefficient quantization low frequency`, `fixed-point audio filter noise`, `transposed direct form`.
- Allineamento dei ritardi e centro acustico: `acoustic center loudspeaker`, `time alignment crossover measurement`, `fractional delay filter`.
- Udibilità della fase e del ritardo di gruppo, dopo Liski 2018: `group delay audibility`, `crossover phase audibility`.

Diffusore.

- Guida d'onda del tweeter e direttività costante: `waveguide tweeter directivity`, `oblate spheroidal waveguide`, `constant directivity waveguide BEM`.
- Diffrazione dal bordo del pannello: `baffle edge diffraction`, `baffle step compensation`, `cabinet diffraction BEM`.
- Accordo di direttività all'incrocio di un due vie: `directivity matching crossover`, `two-way directivity index`, `lobing vertical crossover`.
- Cabinet: `loudspeaker cabinet panel vibration`, `enclosure bracing`, `constrained layer damping enclosure`.
- Modelli dell'induttanza della bobina oltre Leach: `voice coil inductance model`, `lossy inductance loudspeaker`.
- Compensazione digitale delle non linearità e protezione dell'escursione nei monitor attivi: `loudspeaker nonlinear compensation DSP`, `excursion limiter`, `active loudspeaker protection`.
- Preferenza e risposta in stanza, dopo Olive 2004: `loudspeaker preference model`, `spinorama listening window`.
- Amplificazione in classe D recente: `class D audio amplifier`, `GaN class D`.

Il corpus si ferma per lo più al 2016-2020, con gli ultimi titoli datati Iborra 2020 e il report Elettromedia di febbraio 2020; i filoni sopra in cui il lavoro degli ultimi dieci anni conta di più sono la correzione su più punti, i crossover misti, le guide d'onda progettate con BEM, la misura in stanza secondo CTA-2034 e la compensazione digitale delle non linearità.

## 5. Scansioni ancora da leggere

In ordine di peso per la tesi. Prima il Loudspeaker Design Cookbook di Dickason (lotto-02, tre copie, tutte a 26 parole), che è il testo che la dispensa del corso indica per il crossover (capitoli 7 e 11); poi Closed-Box Loudspeaker Systems di Small (lotto-02, due file a zero parole), fonte primaria della cassa chiusa; poi Testing Loudspeakers di D'Appolito (lotto-05), che serve il capitolo 08. Vengono dopo le slide ufficiali EEASE 2019, quasi tutte a zero parole, in particolare Electromagnetic transducers e Class D Power Amplifiers, che completano gli appunti propri; Fundamentals of Acoustics di Kinsler e Frey (archivi); Proakis e Manolakis e Mitra (lotto-03); gli appunti propri di elettronica analogica e digitale e il riassunto di teoria dell'elettrotecnica (lotto-07); gli appunti completi di acustica e illuminotecnica e le parti AAI (lotto-04, propri, queste ultime con errore di conversione); Griffiths (lotto-08); Izadian (lotto-01); Lathi, Parodi, Codegone e Barozzi (lotto-06). Le due presentazioni di Geddes, OptimalBassPlaybackinSmallRooms, e la lezione propria sugli studi di registrazione non sono scansioni ma `.pptx` falliti in conversione, e la prima conta per il capitolo 02. Due testi superano la soglia ma sono illeggibili: Acustica a bassa frequenza di Cornana (lotto-04), il cui testo esce con i caratteri raddoppiati, e 17-198 di Brüel & Kjær (lotto-04), OCR corrotto; andrebbero riconvertiti. Il Colloms del lotto 02 non è una lacuna: due copie sono scansioni, ma la terza, da 293 092 parole, è leggibile.

## 6. Doppioni da ignorare

Contano una volta sola, e si legge la copia indicata per prima.

- Dickason, Loudspeaker Design Cookbook: `dickason2006loudspeaker.pdf`, `Loudspeaker Design Cookbook - Seventh Edition` e una terza copia (lotto-02), tutte scansioni.
- Colloms, High Performance Loudspeakers: `Colloms - High performance loudspeakers.pdf` leggibile, `High performance loudspeakers 4ed` e `high performance loudspeakers IV` scansioni (lotto-02).
- Borwick, Loudspeaker and Headphone Handbook: `+++Loudspeaker and Headphone Handbook`, una seconda copia (lotto-02) e `borwick2001.pdf` (archivi), stesso numero di parole.
- Toole, Sound Reproduction: due copie nel lotto-04 e una negli archivi.
- EEASE II e EEASE Exercises: lotto-01 e lotto-02, stesso numero di parole; il secondo porta nel nome l'indicazione di leggere l'ultima parte sul fattore Q.
- Hill, Loudspeaker Modelling and Design: `hill2019loudspeaker.pdf` e la copia di SEMINARS (lotto-02).
- The Electro-mechanical acoustic model: due `.docx` quasi uguali (3 671 e 3 330 parole) e un PDF a 20 parole (lotto-02).
- Thiele e Small, Closed-Box: `Closed-Box-Loudspeaker-Systems-Part-I-Analysis.pdf` e `Closed_Box_Loudspeaker_Systems_Part_1-2.pdf` (lotto-02), probabilmente sovrapposti, da verificare dopo l'OCR.
- Tesi magistrale 2020: `2020_06_Sopranzi.docx` nel lotto-09 e negli archivi, il PDF e il backup del 12/05/2020.
- Iborra 2020: due copie nel lotto-03.
- Farina, Nonlinear Convolution, e `004_154-AES110` (lotto-05); `11069 requirements for low frequency` (lotto-04) e `farina2000simultaneous` (lotto-05) hanno lo stesso numero di parole, da verificare per contenuto.
- Kevin Robinson, Practical Audio Electronics, due copie (lotto-01); CMRR con resistori a tolleranza nel lotto-01 e nel lotto-07.
- Keele in preprint e versione pubblicata dello stesso lavoro: Direct LF Driver Synthesis 1981 e 1982, Monitor Loudspeaker Systems 1981 e 1983, New Set of VB Alignments 1974 e 1975, Nearfield 1973 e 1974.
- Homework 1 di Musical Acoustics in tre versioni (lotto-08); ABOUT RELATING SENSORY DATA in due copie (archivi); tracce d'esame EEASE in `.docx` e `.pdf`.

Restano edizioni diverse e non doppioni: Self Small Signal Audio Design 2020 (lotto-01) e self2010small (lotto-01); Kuttruff Room Acoustics (lotto-04) e Kuttruff Acoustics an introduction (lotto-08).

[^1]: OCR, Optical Character Recognition: riconoscimento del testo nelle immagini di una scansione.
[^2]: CMRR, Common-Mode Rejection Ratio: rapporto di reiezione del modo comune di un amplificatore differenziale.
[^3]: FEM, Finite Element Method, BEM, Boundary Element Method, FDTD, Finite-Difference Time-Domain: metodi numerici per la soluzione dell'equazione delle onde, rispettivamente sul volume, sul contorno e alle differenze finite nel tempo.

Torna a [[00-START]]
