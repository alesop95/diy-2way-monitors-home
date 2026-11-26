# Progetto audio domestico: stato e documenti

Aggiornamento del 2026-11-26. Questo è il punto di lettura per il proprietario: riunisce stato, report e simulazioni dalle fonti canoniche. Controllo DSP, confronto reflex/direttività e cabinet nominali dettagliati sono sviluppati e verificati nei rispettivi perimetri. Le verifiche fisiche rimangono sospese; nessun risultato software certifica diffusori o interfaccia fisica.

## Fonti di verità: una per funzione

| Funzione | Fonte canonica |
|---|---|
| Stato e percorso di lettura | Questo documento, `docs/STATO-PROGETTO.md` |
| Progetto tecnico corrente, componenti e calcoli | [Capitolo 63](63-sistema-autonomo-driver-e-collaudo.md) |
| Uso e controllo del DSP | [Manuale CamillaDSP](61-camilladsp-manuale-tecnico.md) |
| Pendenze e verifiche sospese | [PENDING-ACTIONS.md](PENDING-ACTIONS.md) |
| Decisioni e motivazioni | [Registro ADR](../.claude/memory/decisions.md) |
| Cronologia, comandi, errori e prove | [OPERATIONS-LOG.md](OPERATIONS-LOG.md) |
| Dati numerici e configurazioni | `data/`, `config/` e rapporti del [vault del sistema](../research-vault/sistema-autonomo-20261120/brief.md) |
| Provenienza delle fonti | [Pedigree e punti d'uso](90-riferimenti/fonti-progetto.md); bibliografia canonica `research-vault/fonti.json` |
| Lezioni tecnico-didattiche | [Master didattico](../.claude/context/studio-didattico-master.md) |
| PDF correnti | `docs/pdf/`, quattro documenti e manifesto di impronte; gli intermedi restano in `build/` |

Il catalogo è un elenco generato, la roadmap è una vista dell'agenda e le pagine di memoria servono alla ripresa tecnica: non sono altre versioni del progetto da scegliere. `INDICE-RAGIONATO.md` è ritirato e conserva soltanto il rimando a questa pagina. I PNG di controllo e i PCM sintetici non sono documenti da conservare dopo la verifica. Le fonti originali, i risultati e le decisioni rimangono disponibili.

## Che cosa stiamo realizzando

Il progetto comprende una macchina Ubuntu Studio per progettare e fare home recording, una coppia di monitor attivi a due vie costruita su misura, la catena di ingresso e amplificazione, un percorso di ascolto a PC spento e lo studio degli amplificatori già posseduti. La documentazione deve permettere sia di realizzare il sistema sia di capire perché ogni scelta è stata presa.

Lo stato complessivo è questo: la preparazione software ha superato i collaudi descritti nei registri; architettura, candidati, simulazioni e modelli 3D esplorativi sono disponibili. Restano da completare la progettazione esecutiva approvata, gli acquisti definitivi, la costruzione e la taratura acustica. Non esiste ancora una coppia di diffusori costruita e misurata.

## Stato dei sei fronti

| Fronte | Risultato disponibile | Limite attuale |
|---|---|---|
| Ubuntu Studio | Ambiente di lavoro ricostruito, programmi di progettazione e CAD collaudati, profilo CPU corretto, DSP e MIDI verificati anche dopo riavvio/accesso. | Prestazioni con la futura interfaccia e il carico reale di registrazione da qualificare. |
| Protezione del setup | Backup finale riletto, copia esterna verificata e vecchie copie autorizzate ruotate; quattro punti locali conservati nell'ultima verifica. | È un backup a livello di file, non un'immagine avviabile. Qui si riporta la prova conservata, non una nuova verifica del disco. |
| Monitor a due vie | Confronto chiusa/reflex, direttività ideale e livelli; tre assiemi nominali con frontali, incassi e rinforzo, nativi/STEP/DXF e distinte. | Giochi di lavorazione, fissaggi, ingombri reali, giunzioni, appoggi e risposta acustica restano da approvare sul prototipo. |
| DSP sul PC | CamillaDSP 4.1.3 persistente e banco virtuale verificati; filtri, volume, mute, separazione delle vie e ripartenza controllata. | Il servizio è intenzionalmente in attesa silenziata senza profilo finale; il banco non è il crossover calibrato dei diffusori. |
| Ascolto autonomo e controllo comune | Pannello Mix/Ascolto, WebSocket reale, volume/mute, osservazione ALSA/clock, grafo PC PipeWire e sorveglianza sviluppati; prova audio su file a 44,1/48 kHz e browser desktop/mobile. | Pannello installato e attivo in laboratorio; avvio automatico ancora disabilitato. Identità, jack, clock e percorso fisico PC/Pi restano da qualificare. |
| Amplificatori posseduti | Schede Marshall MG15, Fender Frontman 65R ed EKO basso da 30 W, manuali e studio precedente acquisiti. | Nessuna caratterizzazione completa degli esemplari o diagnosi del guasto EKO eseguita. |

Le prove sulla macchina sono descritte in [collaudo dopo riavvio](10-ambiente/collaudo-dopo-riavvio-2026-11.md), [servizio DSP](10-ambiente/camilladsp-servizio-utente.md), [MIDI](10-ambiente/fluidsynth-diagnosi-e-collaudo.md) e [backup finale](10-ambiente/backup-finale-setup-2026-11.md). Non occorre ripetere installazioni, riavvio o backup per poter continuare il progetto teorico.

## Report dettagliati: come ricostruire il lavoro

La documentazione tecnica esiste per ciascun fronte: comandi, risultato atteso e osservato, errori, correzioni e limiti. Non c'è un unico verbale che contenga ogni battitura del terminale. La ricostruzione usa il report tematico e i microstep cronologici; la [mappa delle prove](90-riferimenti/artefatti-e-prove.md) indica anche gli archivi originali. Un vecchio rapporto conserva ciò che si sapeva allora: gli aggiornamenti successivi non ne cancellano la storia.

| Fronte | Report da aprire |
|---|---|
| CPU, servizi e riavvio | [Ricognizione e diagnosi CPU](10-ambiente/verifica-prima-del-trasferimento.md), [collaudo dopo riavvio](10-ambiente/collaudo-dopo-riavvio-2026-11.md) |
| CAD e formati di scambio | [FreeCAD: installazione e collaudo](10-ambiente/freecad-collaudo-native.md), [studio dei cabinet](59-studio-ingombri-cabinet.md) |
| DSP, servizio e segnale | [Setup persistente](10-ambiente/camilladsp-servizio-utente.md), [manuale e controllo quotidiano](61-camilladsp-manuale-tecnico.md) |
| MIDI e FluidSynth | [Diagnosi, correzione e prova funzionale](10-ambiente/fluidsynth-diagnosi-e-collaudo.md) |
| Backup e conservazione | [Backup di ottimizzazione](10-ambiente/backup-ottimizzazione-2026-11.md), [backup finale](10-ambiente/backup-finale-setup-2026-11.md) |
| Calcoli, componenti, costruzione | [Relazione tecnica 63](63-sistema-autonomo-driver-e-collaudo.md), [crossover 62](62-confronto-crossover-e-verifica-matematica.md), [realizzazione 70](70-realizzazione-e-verifica.md) |
| Tutti gli interventi e le motivazioni | [Cronologia dei microstep](OPERATIONS-LOG.md), [decisioni ADR](../.claude/memory/decisions.md), [lezioni didattiche](../.claude/context/studio-didattico-master.md) |

## Come vedere le simulazioni e il 3D

Il [completamento nominale](64-reflex-direttivita-e-cabinet-nominale.md) collega i 108 scenari reflex, le mappe di direttività e il calcolo delle protezioni. La [nuova consegna CAD](../build/consegna-completamento-20261125/README.md) contiene frontali con tagli/incassi, rinforzo, FCStd modificabili, STEP, DXF e tavole. Il [PDF matematico e costruttivo](pdf/reflex-direttivita-cabinet.pdf) raccoglie metodo, risultati e limiti.

- [Basso, protezione HP35 e trasformazione LT](figure/sistema-autonomo/fattibilita-basso.svg): sei combinazioni driver/cabinet, diciotto curve e intervalli dei 486 scenari. È un modello a piccoli segnali, non una misura dei diffusori.
- [Modulo e fase LR4](figure/crossover-20261120/lr4-modulo-fase.svg) e [effetti di ritardo e polarità](figure/crossover-20261120/cammino-e-somma.svg): si aprono nel browser; formule leggibili nel [PDF LaTeX](pdf/crossover-pc-pi-analogico.pdf).
- [Confronto dei tre cabinet](../build/consegna-cabinet-20261119/confronto.html): pagina locale con viste, dimensioni e collegamenti ai file. Le immagini mostrano viste statiche.
- Per ruotare davvero il modello in FreeCAD aprire [A24](../build/consegna-cabinet-20261119/cad/A24/studio.FCStd), [B27](../build/consegna-cabinet-20261119/cad/B27/studio.FCStd) oppure [C24](../build/consegna-cabinet-20261119/cad/C24/studio.FCStd). I tre solidi sono esplorativi: non autorizzano il taglio del legno.

Le figure finali sono in docs/figure; build conserva dati di simulazione e pacchetti CAD rigenerabili. Non vengono create immagini permanenti per ogni pagina PDF. Il pannello è stato installato manualmente e verificato il 23 novembre; rimane da abilitarne l'avvio al login. La [procedura di avvio e consegna](../config/controllo-ascolto/README.md) conserva comandi e verifica.

## Come funzionerà la catena

Il diffusore attivo a due vie richiede due canali di potenza per cassa: uno per il woofer e uno per il tweeter. CamillaDSP riceve lo stereo e produce quattro segnali filtrati. La proposta usa un'interfaccia multicanale e due amplificatori stereo.

```text
Registrazione e lavoro sul PC
Ubuntu / DAW → CamillaDSP PC → interfaccia → quattro canali di potenza
                                             → due woofer e due tweeter

Ascolto con PC spento
CD / sorgente esterna → interfaccia ↔ Raspberry Pi con CamillaDSP
                                     → stessa interfaccia e stessi finali
```

L'ascolto autonomo è obbligatorio. Nella base economica sviluppata, la stessa interfaccia USB appartiene alternativamente al PC o al Pi; i due host non la controllano insieme. Il percorso di registrazione mantiene anche le cuffie su uno stereo a banda intera distinto dalle quattro vie. Gli ingressi digitali del CD richiedono gestione del clock e della frequenza di campionamento.

La proposta è una coppia con profili mix e ascolto. Cambiare profilo può cambiare equalizzazione e livello, ma non elimina limiti di estensione, rumore, escursione o direttività. Un'eventuale seconda coppia consumer rimane una possibilità da motivare, non un acquisto già previsto. Il trasporto può essere bit perfect fino all'ingresso del processore; filtri e volume modificano intenzionalmente i campioni. Il dettaglio è nel [progetto tecnico corrente](63-sistema-autonomo-driver-e-collaudo.md).

## Componenti, mobile e schermo: che cosa è una proposta

La base di sviluppo documentata è UMC1820 per gli otto ingressi condivisi con l'home recording, quattro uscite per le vie, due Fosi V3 stereo e Raspberry Pi 4 completo per l'autonomia. Sono candidati, non componenti dichiarati acquistati o già collaudati sull'intera catena.

Il cabinet di riferimento A24 è largo 220 mm, profondo 190 mm e alto 430 mm, in MDF da 18 mm, chiuso. I driver candidati sono SB16PFCR25-8 e SB26STCN-C000-4. L'alternativa B27 è larga 190 mm, profonda 180 mm e alta 430 mm e usa il woofer SB15NRX2C30-8. C24 è il confronto di maggiore volume. I tre assiemi nominali dettagliati includono tagli, incassi e rinforzo; il kit conserva sette solidi modificabili per cassa e distinte per coppia. Fissaggi, lavorazione e tolleranze definitive dipendono dai riscontri sospesi.

Il ripiano superiore Stagecaptain ST-120 è già documentato: 118 × 30 cm, quota 93 cm. Non viene richiesta una nuova misura di queste quote pubbliche. Nello scenario nominale studiato, A24 lascia circa 569 mm per la larghezza totale dello schermo; B27 circa 631 mm. Questo spiega perché un 27″ largo 61-62 cm e A24 non sono automaticamente compatibili. La scelta dello schermo resta differita: Full HD è il minimo proposto, QHD non è obbligatorio e il gaming non è un requisito.

L'obiettivo storico è circa 60 Hz-20 kHz entro ±2 dB al punto di ascolto, anche nel piccolo intervallo angolare previsto. Non è una prestazione raggiunta. Nel modello chiuso ideale SB16/A24 il volume netto assunto è 9,664 L, la frequenza a -3 dB circa 68 Hz e il livello a 60 Hz circa -4,4 dB: includendo il passa alto protettivo a 35 Hz il risultato è -5,391 dB. La trasformazione nominale sviluppata recupera +3,391 dB a 60 Hz per arrivare a -2 dB, con circa 2,18 volte la potenza a quella frequenza. Dodici casi sono stati collaudati nel motore e 486 scenari mostrano la sensibilità ai parametri: non è una garanzia sugli esemplari non misurati. Le scelte possono cambiare in base al confronto tra volume, emissione, equalizzazione e costo.

## Caratterizzazione su file aperti

Il [capitolo65](65-caratterizzazione-aperta-e-dati-di-misura.md) aggiunge importazione FRD/OSM, conservazione degli input e controllo di livello, banda, griglia, coerenza e direzioni richieste. Ventisei prove e un esempio sintetico distinguono pacchetto integro da bersaglio rispettato: una curva volutamente fuori limite viene rilevata. Non sono misure del diffusore. La ricerca corregge le vecchie affermazioni su ARTA/GLL e gratuità di SpeakerLab; l’eventuale authoring GLL rimane distinto dall’analisi dei dati.

## Quali prove ingegneristiche esistono

Il confronto LR4 è riproducibile su 8194 frequenze e distingue filtro analogico/digitale, somma complessa, polarità e ritardo. Le formule e i risultati sono nel capitolo 62 e nel PDF LaTeX. I risultati verificano il modello ideale; non sostituiscono la misura dei driver montati sul frontale.

Sono inoltre disponibili dodici configurazioni dimostrative a 44,1 e 48 kHz, con percorsi PC e due selezioni d'ingresso autonomo simulate su file. Sono state elaborate dal motore CamillaDSP reale, con controllo della sorgente sbagliata e guardie che rifiutano periferiche hardware nel laboratorio su file. Il taglio elettrico dimostrativo a 2600 Hz non è un crossover acustico definitivo.

I modelli CAD sono stati ricomputati e riaperti; STEP e DXF controllati, compresi casi volutamente alterati. Il kit conserva anche immagini e rapporti. La verifica geometrica non certifica la portata del tavolo, la stabilità degli appoggi o la risposta sonora. Gli script, le configurazioni e i dati permettono di ripetere questi studi dalla postazione.

## Lista della spesa: stato del preventivo

La distinta di riferimento del 20 novembre totalizza 868,80-1088,80 € senza switch USB, oppure 888,80-1128,80 € con switch. Comprende interfaccia, quattro driver, due finali con alimentatori, Pi completo, materiali del mobile, collegamenti/protezioni/supporti e dotazione di misura stimata. È una somma con voci stimate e prezzi datati, non un preventivo chiuso o una nuova verifica commerciale.

Esclude schermo, tavolo già comprato, spedizioni, finitura e utensili. L'alternativa SB15 costa di più; non sono da comprare entrambe le coppie di woofer. Stock, IVA di consegna e offerte del fornitore restano da riscontrare prima dell'ordine. L'obiettivo di spesa minima a qualità adeguata guida il confronto teorico, senza anticipare l'acquisto di componenti non ancora giustificati.

## Apparecchi già posseduti

| Apparecchio | Che cosa abbiamo | Che cosa rimane sospeso |
|---|---|---|
| Marshall MG15 | Manuale MG10/MG15 di dieci pagine, OCR e riscontro visivo di copertina e specifiche; [scheda Marshall](80-strumenti-posseduti/marshall-mg15.md). | Identificazione della revisione fisica, schema corrispondente e misure. |
| Fender Frontman 65R | Manuale ufficiale e studio precedente acquisito e corretto; [scheda Fender](80-strumenti-posseduti/fender-frontman-65r.md). | Riscontro del circuito dell'esemplare e caratterizzazione reale. |
| EKO basso da 30 W | Manuale XL/XB di undici pagine, OCR e immagini 1/10/11 lette; corrispondenza documentale XB30, speaker 10 pollici 8 ohm; [scheda EKO](80-strumenti-posseduti/eko-basso.md). | Diagnosi del suono distorto, trasduttore montato e quote del cabinet; nessun ricambio scelto. |

Le scansioni e gli appunti originali acquisiti restano privati. Reverse engineering significa ancora passare dall'identificazione e dai blocchi funzionali a uno schema verificabile e poi alle misure: non è già disponibile un modello completo dei tre amplificatori.

## Documenti da aprire, in ordine utile

Tutti i percorsi seguenti partono dalla radice locale `E:\diy-2way-monitors-home`. I collegamenti del sorgente Markdown aprono i file nel repository; il catalogo conserva l'elenco completo con percorsi assoluti. Per riprendere non occorre leggere l'intera cronologia.

I capitoli numerati e gli indici tecnici sono sotto `docs/`. Le tre relazioni sono nella cartella `docs/pdf/`, file `crossover-pc-pi-analogico.pdf`, `sistema-autonomo-driver-e-collaudo.pdf` e `reflex-direttivita-cabinet.pdf`; il master didattico è `.claude/context/studio-didattico-master.md`. Il PDF di questo recap è una copia di lettura: per la navigazione cliccabile usare questo Markdown e il catalogo.

| Serve per | Documento da aprire |
|---|---|
| Capire il sistema completo e le scelte correnti | [63-sistema-autonomo-driver-e-collaudo.md](63-sistema-autonomo-driver-e-collaudo.md) |
| Usare e capire CamillaDSP nel nostro setup | [61-camilladsp-manuale-tecnico.md](61-camilladsp-manuale-tecnico.md) |
| Leggere la matematica del crossover | [PDF LaTeX crossover](pdf/crossover-pc-pi-analogico.pdf), sei pagine |
| Leggere componenti, autonomia e protocollo | [PDF LaTeX sistema autonomo](pdf/sistema-autonomo-driver-e-collaudo.pdf), aggiornato con fattibilità del basso |
| Compilare le due relazioni | [Sorgenti e procedura LaTeX](latex/README.md) |
| Confrontare i tre cabinet e gli ingombri | [59-studio-ingombri-cabinet.md](59-studio-ingombri-cabinet.md) |
| Vedere CAD, viste e file esportati | [Kit CAD: confronto.html](../build/consegna-cabinet-20261119/confronto.html) |
| Trovare tutti i documenti | [catalogo completo dei percorsi](90-riferimenti/catalogo-documentazione.md) |
| Trovare PDF, CAD, manuali e prove private | [Mappa degli artefatti](90-riferimenti/artefatti-e-prove.md) |
| Imparare rileggendo le scelte | [Master didattico e approfondimenti](../.claude/context/studio-didattico-master.md) |
| Sapere perché è stata presa una decisione | [Registro ADR](../.claude/memory/decisions.md) |
| Ricostruire ogni intervento e correzione | [OPERATIONS-LOG.md](OPERATIONS-LOG.md) e [tracciabilità per fase](90-riferimenti/tracciabilita-microstep.md) |
| Capire fonti, pedigree e usi | [Mappa delle fonti](90-riferimenti/fonti-progetto.md) e [metodo delle lezioni](90-riferimenti/metodo-fonti-lezioni-riordino.md) |
| Vedere attività differite e sospensioni | [PENDING-ACTIONS.md](PENDING-ACTIONS.md) e dati in `tools/roadmap-items.yml` |

Il capitolo 55 conserva la prima proposta e il suo contesto; per la base corrente di componenti e autonomia si usa il capitolo 63. I microstep descrivono anche ipotesi poi corrette e non vanno letti come se ogni frase storica fosse lo stato attuale.

## Dove sono file, dati e copie

La documentazione e il codice canonici sono nel repository Windows. Ubuntu contiene il setup collaudato e il kit CAD trasferito e riletto il 19 novembre; non si afferma che ogni successivo PDF o file nuovo del repository sia già stato copiato su Ubuntu. Il progetto di home recording è un repository gemello: condivide l'ambiente, la cui copia canonica è qui e viene propagata, ma conserva il proprio contenuto su registrazione e mixing.

`docs/`, `data/`, `config/` e `tools/` conservano documenti, parametri, configurazioni e generatori. `research-vault/` conserva bibliografia, schede, protocollo e risultati di ricerca; `.claude/context/` e `.claude/memory/` conservano stato, decisioni e didattica. `build/` contiene gli output locali, mentre `_notes/` contiene scansioni, acquisizioni e prove private. Gli ignorati non arrivano con un semplice clone Git: vanno conservati con i loro archivi o rigenerati con gli strumenti indicati.

I risultati correnti sono in `build/studio-crossover-20261120-v2/`, `build/sistema-autonomo-20261120-v5/` e `build/collaudo-profili-autonomi-20261120-finale-v5/`. I rapporti leggibili sono copiati nei due topic del vault. I tentativi precedenti, anche falliti, sono nel ZIP `_notes/archivio-prove/20261120/prove-superate.zip`, con 340 file e manifesto dei percorsi originali. La rimozione dei soli espansi ha ridotto di circa 190 MiB lordi le copie, conservando la prova delle correzioni.

La mappa registra 213 riferimenti, con 46 schede curate e 167 riferimenti storici ancora da riconciliare. Censire non equivale a leggere: copertura e verifica rimangono distinte. Linkwitz Lab e OpenCV sono prioritari per indicazione dell'utente. Sette lezioni per il template sono disponibili e ancora da recepire; il percorso didattico comprende undici approfondimenti. Non sono stati importati contenuti aziendali; rimane PA-042 per la valutazione manuale dei vecchi identificatori nelle revisioni Git precedenti.

## Sviluppo e attività residue

Il basso protetto e la trasformazione nominale sono calcolati e verificati nel motore su file. Il controllo comune comprende API reale, osservazione ALSA, percorso PC PipeWire, pannello e sorveglianza: il [manuale](61-camilladsp-manuale-tecnico.md) collega codice, prove e misure. Il pannello è installato e attivo; restano abilitazione al login e qualifica hardware. Il software non certifica diffusori, jack, clock o livelli acustici reali. Il modulo WebSocket già presente su Ubuntu viene riusato senza aggiungere dipendenze al Python Windows.

Le attività residue hanno una sola lista operativa: [PENDING-ACTIONS.md, pendenze correnti](PENDING-ACTIONS.md#pendenze-correnti-dopo-lo-sviluppo-autonomo). Il blocco teorico e software autorizzato è sviluppato: controllo DSP, reflex/direttività, livelli e cabinet nominali. Restano scelta esecutiva, spesa, fonti e versionamento, con lavorazione e qualifica fisica sospese. La roadmap generata legge gli stessi fronti dai dati di pianificazione, senza diventare un secondo registro di pendenze.

I PDF finali sono in `docs/pdf/`, con provenienza e impronte in `docs/pdf/manifest.json`. Le anteprime PNG sono soltanto controlli visivi temporanei: si elimina ogni immagine dopo l'ispezione. `build/` conserva intermedi di compilazione e risultati simulativi rigenerabili, non una seconda consegna dei PDF. Le viste del CAD sono figure di progetto e conservano una funzione distinta dalle anteprime delle pagine.

Da parte dell'utente non è richiesta adesso alcuna foto, misura, ascolto, collegamento, acquisto o visita al tecnico. La parte fisica rimane nel [registro delle sospensioni](PENDING-ACTIONS.md#verifiche-fisiche-sospese-su-richiesta-dellutente) e torna in agenda soltanto quando l'utente chiederà di riaprirla.
