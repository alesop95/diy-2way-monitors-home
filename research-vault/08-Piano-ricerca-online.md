---
tipo: protocollo
aggiornato: 2026-10-05
---
# Piano della ricerca bibliografica online, primo giro

> Proposto il 2026-10-05 (MS-192), dopo l'analisi di copertura di [[07-Analisi-corpus]]. Si esegue quando l'utente lo conferma, perché la ricerca è nella forma propongo e conferma ([[scope]]).

## Da dove parte

La ricerca non cerca da zero: cerca dove il corpus locale è assente o debole, e lo dice per ogni filone. Il corpus copre bene la teoria del crossover, i parametri di Thiele e Small, i modi della stanza, l'elettroacustica e le appendici di base; si ferma per lo più fra il 2016 e il 2020. Le lacune sono quelle elencate nella sezione 4 dell'analisi, e qui sono raggruppate in dodici filoni di ricerca.

## I dodici filoni, con le query del primo giro

| Filone | Capitolo | Query |
|---|---|---|
| R1 correzione della stanza su più punti | 02, 07 | multi-point room equalization; room response equalization review; mixed-phase room correction |
| R2 misura in stanza | 01, 08 | in-room loudspeaker measurement spatial averaging; estimated in-room response CTA-2034 |
| R3 interferenza con i confini | 02, 07 | speaker boundary interference response; loudspeaker placement optimization small room |
| R4 bassi in stanza piccola | 02 | low-frequency room optimization; modal room compensation loudspeaker |
| R5 simulazione di stanze piccole | 03 | small room acoustic simulation validation; image source method measurement comparison; FDTD room low frequency |
| R6 crossover misti FIR e IIR | 04 | mixed-phase FIR crossover; excess phase correction loudspeaker; hybrid IIR FIR crossover |
| R7 quantizzazione dei biquad | 04, F | biquad coefficient quantization low frequency; fixed-point audio filter noise; transposed direct form II audio |
| R8 ritardi e centro acustico | 04, 08 | acoustic center loudspeaker measurement; crossover time alignment; fractional delay filter design |
| R9 guida d'onda e direttività | 05 | waveguide tweeter directivity; oblate spheroidal waveguide; directivity matching crossover two-way |
| R10 diffrazione del pannello | 05 | baffle edge diffraction model; baffle step compensation; cabinet diffraction BEM |
| R11 cabinet | 06 | loudspeaker cabinet panel vibration; enclosure bracing damping; constrained layer damping loudspeaker |
| R12 monitor attivi oggi | 00, 05 | active studio monitor DSP design; loudspeaker nonlinear compensation DSP; excursion protection active loudspeaker; class D audio amplifier review |

## Il criterio di scelta dei paper: l'analisi stadio per stadio

Aggiunto il 2026-10-06 su indicazione dell'utente. Il modello di lavoro che l'utente vuole ritrovare nei paper è quello dell'analisi del Tube Screamer TS808 negli esercizi del corso EEASE: un circuito reale, scomposto stadio per stadio, con il modello a piccolo segnale di ciascuno, le formule di guadagno, poli e zeri, e i valori numerici ricavati dai componenti veri. A parità di pertinenza, il vaglio di ogni giro preferisce quindi i paper e le tesi che analizzano un circuito o un sistema esistente con questa scomposizione, rispetto alle rassegne qualitative e ai lavori che danno solo il risultato. Nella query si aggiungono termini come "stage-by-stage analysis", "circuit analysis", "small-signal model" e "case study". Il criterio vale per tutti i filoni, e in particolare per R9, R10, R12 e per l'accoppiamento fra amplificatore e altoparlante.

## Filoni per altri progetti: l'ingegnerizzazione dei pedali per chitarra

Il ramo Guitar and effects engineering della biblioteca, nato in MS-208, è un filone di ricerca a sé e non appartiene alla tesi sui monitor. L'utente vuole progettare una pedaliera analogica per chitarra, dal circuito al PCB fino all'ordine dei componenti. La ricerca bibliografica di quel filone si svolgerà nel progetto dedicato, quando l'utente lo crea, con lo stesso metodo e lo stesso criterio dello stadio per stadio. Il punto di partenza sono le circa 130 voci del ramo nella biblioteca su `J:` e la pagina della wiki sul TS808.

## Il metodo, sul modello di intralino

Per ogni filone si cerca in tre canali:
- gli archivi primari, cioè AES E-Library, IEEE Xplore e JASA;
- gli indici aperti, cioè Crossref e Semantic Scholar via web;
- Google Scholar per allargare.

Di ogni query si conservano la stringa esatta, la data, il canale, il numero di risultati vagliati, e per ciascun risultato incluso o escluso il motivo. Il registro di ogni giro è una nota numerata di questo vault, come in intralino. I candidati inclusi entrano in `fonti-proposte.json` con il filone e lo stato da verificare, e passano dal registro unico di `tools/registro-fonti.py`. Prima di proporre un candidato si controlla che non sia già nel corpus, nella libreria JabRef o nella bibliografia della tesi del 2020, che è la lezione del 2026-10-02 portata nel template.

La divisione del lavoro è questa. L'agente esegue le query sul web, vaglia per titolo e abstract e riscontra i metadati sulle pagine dell'editore. L'utente, con i propri accessi, scarica i PDF scelti; quando un archivio non è leggibile dagli strumenti dell'agente, come accade alla AES E-Library che risponde 403, esegue lui la query nel browser e ne salva la pagina dei risultati.

Il criterio di arresto è quello di intralino: un filone si chiude dopo due giri consecutivi senza nuovi studi pertinenti, e lo si dichiara come saturazione della ricerca, non come completezza.

## Conferma richiesta all'utente

Sono da confermare i dodici filoni, l'ordine (proposto: R6, R1, R9, R10, R7, R8, poi gli altri) e la divisione del lavoro.

Torna a [[00-START]]
