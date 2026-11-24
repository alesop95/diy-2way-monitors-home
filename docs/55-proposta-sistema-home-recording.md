# Proposta del sistema completo per home recording

Stato documentale aggiornato il 2026-11-20: questa è la proposta iniziale del 17 novembre, conservata per ricostruire requisiti e ragioni. Componenti, autonomia, simulazioni e budget correnti hanno una sola fonte: [capitolo 63](63-sistema-autonomo-driver-e-collaudo.md). Le verifiche fisiche sono sospese come stabilito nel [registro delle pendenze](PENDING-ACTIONS.md); le richieste storiche sotto non sono azioni immediate.

Stato al 2026-11-17: proposta da approvare, non progetto esecutivo e non ordine di acquisto. Il tavolo Stagecaptain ST-120 è acquistato e montato, dichiarazione dell'utente. L'utente delega una proposta dei requisiti per home recording e chiede di valutare anche l'ascolto consumer con gli stessi monitor. Le misure reali della stanza e della posizione d'ascolto restano da consegnare. Prezzi e disponibilità sono fotografie delle pagine lette oggi e vanno ricontrollati al momento dell'ordine; gli importi stimati sono distinti dai prezzi osservati.

## Revisione richiesta: prima il ripiano superiore e la stanza

L'utente ha chiesto di rivedere l'insieme prima di approvare: entrambi i diffusori staranno sul ripiano superiore dello ST-120 e va verificato lo spazio reale e dove si collochi la postazione nella stanza. Dimensioni del cabinet, driver e spesa sotto restano ipotesi di confronto. La prima attività dipendente dalle misure è il modello della postazione; simulazione e distinta esecutiva seguono il suo inviluppo utile. La preparazione software della macchina può continuare senza congelare il mobile.

| Rilievo iniziale | Unità | Valore |
|---|---|---|
| Larghezza nominale del ripiano superiore, pezzo 2 | cm | 118, immagine quotata ufficiale |
| Profondità nominale del ripiano superiore | cm | 30, immagine quotata ufficiale |
| Altezza nominale della superficie superiore da terra | cm | 93, immagine quotata ufficiale |
| Larghezza e posizione dello schermo sul ripiano | cm | Schermo da acquistare; confrontare schede ufficiali e layout, MS-235 |
| Altezza delle orecchie da seduto nella posizione abituale | cm | Da misurare dall'utente |

Il rilievo successivo colloca tavolo, schermo e seduta rispetto a pareti e soffitto secondo `docs/35-rilievo-geometrico.md`: servono distanze dalle pareti, orientamento, aperture e ostacoli. Solo allora si possono confrontare posizione dei centri acustici, orientamento verso le orecchie, distanze dalla parete e riflessioni del piano. Un CAD che entra nel ripiano non dimostra da solo una buona posizione acustica.


### Quote pubbliche verificate e primo vincolo geometrico

Correzione del 2026-11-17, MS-234. Le tre quote del tavolo sopra erano pubbliche e la richiesta di farle rimisurare dall'utente è ritirata. Il [manuale ufficiale, versione 01.2025](https://www.kirstein.de/docs/manuals/00106799/manual_EN.pdf?h=1ecf4368fd8ab20c3c92818e95c8e66c), pagina 7, identifica il pannello superiore come pezzo 2; l'[immagine quotata ufficiale](https://img.kirstein.de/out/pictures/generated/product/9/2000_2000_75/6570c468a762c122194f883e11b84239_9.jpg) mostra larghezza 118 cm, profondità 30 cm e quota superiore 93 cm da terra. Il piano principale è 118 × 60 cm. Si distinguono dimensioni nominali e spazio rimasto libero con lo schermo e i cavi. I valori sono registrati anche in `data/postazione-st120.json`, con i dati della stanza e dell'ascoltatore ancora nulli. Il bordo posteriore presenta rientranze visibili nella distinta del manuale: il rettangolo nominale non ne descrive i contorni esatti.

La proposta iniziale di base 23 × 30 cm entra nel rettangolo nominale soltanto con i lati paralleli e senza margine in profondità. Con i cabinet dritti, due larghezze da 23 cm lasciano al massimo 72 cm fra i lati interni e 95 cm fra i centri dei cabinet, prima di margini o accessori. Questi limiti geometrici non sono la posizione approvata né una garanzia che lo schermo trovi posto.

La rotazione orizzontale cambia il conto. Per una base rettangolare larga W e profonda D, ruotata di un angolo θ compreso fra 0° e 90°, gli ingombri rispetto ai bordi del ripiano sono W cos θ + D sin θ in larghezza e D cos θ + W sin θ in profondità. Con W = 23 cm, D = 30 cm e θ = 30°, gli ingombri sono circa 34,92 × 37,48 cm: manca appoggio completo nei 30 cm di profondità. I 30° sono un caso di studio per un possibile ascolto a triangolo equilatero, non un orientamento già deciso. Mantenendo W = 23 cm e θ = 30°, una base interamente appoggiata nel rettangolo da 30 cm richiederebbe D non maggiore di circa 21,36 cm, ancora senza margini.

La conseguenza è rivedere insieme forma e volume del cabinet, orientamento e supporti prima di congelare i driver. Un cabinet meno profondo cambia volume e accordo; lasciarlo parallelo al ripiano richiede di progettare e verificare la risposta fuori asse nel punto d'ascolto; un supporto con sporgenza richiede una verifica meccanica propria. Nessuna di queste vie è scelta in questa correzione. Il modello 3D potrà rappresentare i contatti, le interferenze con lo schermo e i cavi e le posizioni ammissibili; la risposta nella stanza richiederà poi i dati acustici.

## Schermo da acquistare: specifiche minime e richiesta al fornitore

Mandato del 2026-11-17, MS-235: anche lo schermo è da acquistare. L'utente può chiedere un preventivo al proprio fornitore tramite Esprinet; chiede specifiche sufficienti a home recording e progettazione, senza gaming, con priorità a costo, consumi e comodità. Dopo un primo assenso alla proposta 27 pollici QHD, precisa che la risoluzione si può ridurre se non necessaria. Full HD è quindi il requisito minimo proposto; diagonale e modello restano da scegliere sul confronto fra prezzi e layout, non sono un acquisto già autorizzato.

QHD offre più area di lavoro per pannelli, tracce e finestre, ma non è indispensabile ad Ardour, REW o al CAD del cabinet. Un 27 pollici Full HD ha gli stessi 1920 × 1080 pixel di un 24 Full HD, distribuiti su una superficie maggiore: non aggiunge area di lavoro logica a pari scala e rende i pixel più grandi. Le densità calcolate sono circa 92,6 ppi per 23,8 Full HD, 81,6 per 27 Full HD e 108,8 per 27 QHD. A distanza maggiore la dimensione dei caratteri può contare più della densità: la scelta si verifica sulla posizione d'ascolto, non sul solo numero di pollici.

Propongo di chiedere per primo il prezzo di un 23,8-24 pollici Full HD IPS opaco, con il 27 Full HD come confronto se si preferiscono caratteri fisicamente più grandi. Il 24 facilita anche la convivenza con le casse: esempi ufficiali hanno larghezza circa 54 cm contro circa 61-62 cm dei 27. I cabinet e la loro rotazione restano da definire. Con casse larghe 23 cm parallele al ripiano, il limite laterale teorico dello schermo è 72 cm; riservando, a titolo di progetto, 2 cm da ogni cassa e 1 cm a ogni bordo esterno, scende a 66 cm. Questi margini sono scelte esplorative, non quote del produttore. Un 32 come il Dell P3223DE largo 71,242 cm rientrerebbe solo nel caso nominale senza margini, mentre un 34 ultrawide supera già i 72 cm con la sola area attiva. Nessuno di questi conti autorizza a considerare il 27 garantito con le casse ruotate.

| Voce da richiedere | Specifica proposta |
|---|---|
| Diagonale e risoluzione | Preventivo base 23,8-24 pollici, 1920 × 1080; confronto 27 Full HD |
| Pannello e superficie | IPS, piatto, opaco; luminosità regolabile fino a un livello confortevole nella stanza |
| Frequenza | 60 Hz sufficienti; 75-100 Hz accettati se inclusi nel prezzo migliore |
| Posizione | Inclinazione regolabile; altezza regolabile preferita se il sovrapprezzo è contenuto e utile alla quota sul ripiano |
| Ingressi | HDMI o DisplayPort compatibile con l'uscita fisica del PC da riscontrare; cavo incluso o quotato |
| Supporti | Base interamente collocabile nei 30 cm, con spazio cavi; VESA preferibile per poter cambiare supporto |
| Comfort | Retroilluminazione dichiarata senza sfarfallio, trattamento antiriflesso, impostazioni accessibili dal monitor |
| Energia | Scheda EPREL del codice esatto, consumo SDR e standby; confrontare dati con lo stesso metodo |
| Prezzo | Prezzo finale con IVA, trasporto, cavo e garanzia; nessun prezzo Esprinet o stock verificato in sessione |

Non è previsto un sovrapprezzo per HDR, tempi di risposta da gaming, hub USB-C con ricarica o funzioni di rete che il progetto non richiede. Un modello più accessoriato può comunque risultare il più conveniente se offerto a prezzo inferiore. Non si scarta un monitor solo perché dichiara 100 Hz, ma non si usa quella frequenza come requisito d'acquisto.

Due codici per un preventivo confrontabile sono Philips 24E1N1100A/00 come esempio essenziale e Dell P2425H come esempio con maggiore regolabilità. Il [manuale Philips](https://www.documents.philips.com/assets/20241209/4601f6a3000541aa84d0b24100909f9e.pdf) riporta 542 × 417 × 180 mm con base e inclinazione, senza una regolazione verticale indicata. La [pagina Dell](https://www.dell.com/en-gb/shop/dell-24-monitor-p2425h/apd/210-bmff/) riporta larghezza 538,64 mm e altezza con supporto variabile da 364 a 496,53 mm. Sono esempi da quotare, non prodotti di cui si sia verificato il listino del distributore. Un equivalente meno caro che rispetti le specifiche va confrontato prima di scegliere.

Per l'energia il [registro EPREL P2425H](https://eprel.ec.europa.eu/fiches/electronicdisplays/Fiche_1865623_EN.pdf) riporta 11,7 W in SDR, 0,3 W in standby e classe C; il [P2725D](https://eprel.ec.europa.eu/fiches/electronicdisplays/Fiche_2173550_EN.pdf) riporta 18,8 W in SDR, 0,3 W in standby e classe E. È un confronto fra questi modelli, non la prova che ogni Full HD consumi meno di ogni QHD. Il consumo tipico Philips del manuale ha condizioni proprie e non viene ordinato direttamente contro questi due valori EPREL. Cinque watt risparmiati per un esempio d'uso di 8 ore per 220 giorni corrispondono a 8,8 kWh annui: valutare il risparmio insieme al prezzo e all'ergonomia, senza pagare un grande sovrapprezzo per un beneficio elettrico piccolo.

Richiesta pronta da inoltrare dall'utente: «Cerco un monitor per home recording e CAD leggero: quotate un 23,8-24 pollici Full HD IPS opaco e, come confronto, un 27 Full HD. Sono sufficienti 60 Hz. Priorità a prezzo finale basso, consumi SDR contenuti e posizione comoda; indicate quanto costa la regolazione in altezza rispetto al modello base. HDMI o DisplayPort, base compatibile con un ripiano profondo 30 cm, codice esatto, scheda EPREL, garanzia, disponibilità e cavo incluso. Esempi da confrontare: Philips 24E1N1100A/00, Dell P2425H o equivalenti più convenienti». Nessuna comunicazione è stata inviata al fornitore dall'agente.

La spesa per lo schermo va aggiunta al totale della catena audio già indicato; prezzo e modello restano in attesa dei preventivi. Il 27 QHD non è più trattato come requisito minimo.

## La scelta che raccomando

Aggiornamento 2026-11-20, ADR-051: l'utente richiede esplicitamente ascolto da CD o riproduttori con PC spento. Si sviluppano modalità PC e Raspberry Pi, riusando l'interfaccia fra i due host. Il [progetto aggiornato](63-sistema-autonomo-driver-e-collaudo.md) propone driver, finali, cassa chiusa nei volumi esplorati, profili dimostrativi e collaudo DAW, con budget ricalcolato. Prevale sulla precedente esclusione del processore autonomo dalla prima spesa e sull'inviluppo iniziale da 15 litri; le tabelle storiche sotto restano proposte datate, non ordini o risultati acustici.

Il sistema serve anche `home-recording-training-mixing-setup`: i due repository hanno storia Git distinta, mentre il blocco `docs/10-ambiente/` nasce qui ed è propagato dal comando `python tools/sync-ambiente.py`. Questo legame è verificato nel sorgente dello strumento e nel `CLAUDE.md` del gemello. I requisiti dell'interfaccia si riconciliano fra i due usi prima dell'acquisto; la fonte degli otto ingressi è la valutazione nel gemello, non un requisito nuovo inventato qui. La ricognizione della macchina è pubblicata nel blocco condiviso come `verifica-prima-del-trasferimento.md`.

Una sola coppia di due vie attivi, con due profili CamillaDSP: riferimento per registrare e mixare, ascolto personale per musica e contenuti. La seconda coppia non entra nella prima spesa. Cambiare profilo non aumenta escursione, potenza o estensione fisica: se in seguito si desiderano bassi profondi a livello elevato si dimensiona un subwoofer, senza pretendere che l'equalizzazione sostituisca un trasduttore.

Tre architetture sono state considerate. La coppia unica con due profili riusa quattro canali di conversione e quattro di amplificazione; è la raccomandazione perché evita di duplicare il costo maggiore. Una seconda coppia consumer amplificata richiede altre due uscite di linea, quindi sei complessive; può servire come confronto con un altro diffusore, cosa che un preset non replica. Due coppie entrambe attive a due vie richiedono otto uscite e otto finali se devono restare collegate e operative insieme. In alternativa si possono commutare quattro uscite a impianto silenziato, ma cambiano cablaggio e affidabilità. La proposta non include questa complessità iniziale.

## Requisiti proposti, da verificare prima del taglio

| Grandezza | Proposta iniziale | Come si conferma |
|---|---|---|
| Distanza fra orecchie e ciascun diffusore | 1 m nominale, intervallo da studiare 0,8-1,2 m | Rilievo con tavolo e seduta definitivi |
| Riferimento di lavoro | 75 dB SPL al punto d'ascolto, con segnale e pesatura da fissare nel protocollo | Taratura della catena di misura; non è una prescrizione sanitaria |
| Picco di progetto | 95 dB SPL per la coppia al punto d'ascolto in banda media | Simulazione di tensione, escursione e compressione; prova finale con segnale definito |
| Bassa frequenza | Mantenere l'obiettivo precedente da 60 Hz, senza imporre 35-40 Hz | Simulazione della cassa e misura quasi anecoica composta |
| Risposta del diffusore | Obiettivo storico ±2 dB, 60 Hz-20 kHz, in asse e a ±10° | Distinguere piano orizzontale e verticale, distanza, finestra e smoothing prima della prova |
| Profilo ascolto | Shelf iniziale +2 dB sotto circa 120 Hz, compensato in livello | Margine digitale, escursione e ascolto comparato; valori proposti, non curva già scelta |

La risposta diretta del diffusore e quella misurata nella stanza sono due obiettivi distinti. Non si impone alla misura al sedile la stessa rettilineità della risposta diretta e non si amplificano i null profondi della stanza. Il profilo mix mantiene invariati crossover, ritardi e protezioni; il profilo ascolto aggiunge soltanto una preferenza a monte. Confrontare i profili a volume percepito equivalente impedisce che il più forte sembri automaticamente migliore.

## Interfaccia: risolvere la contraddizione fra quattro e otto ingressi

ADR-046 conserva la UMC404HD come candidata economica per monitor e misura. La pagina del progetto gemello `docs/20-catena-di-ingresso.md`, riletta oggi, registra però otto ingressi simultanei per batteria stereo, chitarra, basso e voce con margine. Quattro ingressi non soddisfano quel requisito. L'utente oggi non lo ha revocato.

Propongo per il sistema completo la [Behringer UMC1820](https://behringer.com/en/products/0805-AAN), con otto ingressi e uscite di linea bilanciate 3-10 oltre alle principali. Il prezzo osservato su [Thomann Italia](https://www.thomann.it/behringer_umc1820.htm) è 175 €, disponibile; la [UMC404HD](https://www.thomann.it/behringer_umc404hd.htm) è a 98 €. Il maggior costo osservato è 77 €. I 159 € dei risultati di ricerca esteri non sono il prezzo letto nella pagina italiana. La conformità USB su Linux, il routing multicanale, il fruscio e il comportamento alla riconnessione restano da provare sull'esemplare: il produttore documenta l'uso senza driver su Mac, che da solo non è una certificazione Linux.

Mappa logica proposta: quattro uscite di linea per woofer sinistro, tweeter sinistro, woofer destro e tweeter destro. Le quattro uscite aggiuntive possono servire una seconda coppia biamplificata; in alternativa, due servono consumer già amplificati e due rimangono di riserva. Queste alternative non si sommano. La corrispondenza fra indice ALSA, canale PipeWire ed etichetta fisica si misura prima di collegare i tweeter. Le cuffie hanno il proprio percorso stereo completo e non devono ricevere una coppia woofer/tweeter. Il direct monitoring dell'interfaccia non deve alimentare direttamente una via dei monitor saltando il crossover.

## Cabinet e legno: un ingombro calcolato da cui partire

Propongo MDF da 18 mm, giunti a battuta incollati, driver a filo del frontale, rinforzo interno aperto e smorzamento sulle pareti. La finitura iniziale è semplice e riparabile. Il legno massello non porta un vantaggio dimostrato rispetto al costo; il multistrato di betulla resta l'alternativa quando contino soprattutto peso e resistenza alle movimentazioni. Il materiale finale si confronta sui preventivi locali, includendo taglio e fresatura.

L'inviluppo proposto per ogni cassa è largo 230, alto 360 e profondo 300 mm. Con pannelli uniformi da 18 mm il vano interno geometrico è 194 × 324 × 264 mm, cioè 16,595 litri prima degli ingombri. L'obiettivo esplorativo è circa 15 litri netti: driver, condotto e rinforzi vanno sottratti dal modello solido, non valutati definitivamente a occhio. Se la simulazione richiede un altro volume cambia il modello, non si conserva l'ingombro per ragioni estetiche.

| Pannello | Misura nominale in mm | Quantità per coppia |
|---|---|---|
| Frontale e posteriore a tutta superficie | 230 × 360 × 18 | 4 |
| Fianchi fra frontale e posteriore | 264 × 360 × 18 | 4 |
| Superiore e inferiore fra i fianchi | 194 × 264 × 18 | 4 |

La tabella serve al preventivo preliminare: non è una distinta autorizzata al taglio. L'area nominale dei dodici pannelli è circa 0,916 m², esclusi rinforzi, sfrido, larghezza della lama, tolleranze e pezzi di prova. La posizione dei trasduttori, le fresature, i raccordi del frontale e il condotto si congelano solo dopo verifica di direttività e interferenze. Per un reflex iniziale da 15 litri e 45 Hz, un tubo di diametro interno 50 mm dà una lunghezza indicativa di circa 157 mm con una comune correzione delle estremità; è soltanto un controllo d'ordine di grandezza. Si devono verificare velocità dell'aria, risonanze, distanza dalle pareti e ingombri. Nessuna scelta definitiva fra porta anteriore e posteriore precede il posizionamento reale sul tavolo.

La rosa iniziale comprende il woofer [SB16PFCR25-8](https://sbacoustics.com/wp-content/uploads/2024/01/6in-SB16PFCR25-8.pdf) e il tweeter [SB26STCN-C000-4](https://sbacoustics.com/wp-content/uploads/2020/02/SB26STCN-C000-4.pdf). Il primo dichiara Fs 38 Hz, Qts 0,40, Vas 27 litri, Sd 124 cm² e corsa lineare totale 9 mm: per le simulazioni l'escursione in una direzione è 4,5 mm, non 9. Il secondo dichiara Fs 960 Hz; l'incrocio iniziale da esplorare è fra 2,2 e 2,8 kHz con pendenze acustiche adeguate. Non è una coppia già validata: vanno esaminate risposta fuori asse, distorsione, centro acustico e margine del tweeter. Una frequenza di crossover impostata nel DSP non dimostra da sola la pendenza acustica desiderata.

## Programmi e consegna del 3D

Avanzamento del 2026-11-18: lo schermo è un acquisto differito. Il collaudo CamillaDSP su file descritto in `docs/56-collaudo-dsp-offline.md` è riuscito anche sulla macchina Ubuntu; non è un servizio installato né un crossover acustico validato. FreeCAD 1.1.4 è stato individuato come AppImage ufficiale, senza installazione o prova sulla macchina. Il supporto al progetto e al falegname è già disponibile per dichiarazione dell'utente, PA-037.

La verifica locale trova CADCraft 0.20.1 su Windows. L'aiuto offre DXF/DWG e il catalogo mostra operazioni su regioni, senza un percorso STEP di solidi parametrici identificato nella ricognizione: è candidato per tavole 2D, non è stato dimostrato sufficiente come sorgente del cabinet. Il percorso già previsto dal progetto resta FreeCAD per il solido e Blender per stanza, tavolo e viste d'insieme. Su Ubuntu la ricognizione trova Blender 5.0.1; FreeCAD e CamillaDSP non sono stati trovati dai controlli di pacchetto e PATH, che non escludono un'AppImage o un binario fuori PATH.

Il filone a monte del 2026-11-16 ha catalogato `blender-skills`, non lo ha installato né collaudato qui. Il catalogo dichiara Blender 5.2 o successivo: la versione osservata non soddisfa quella condizione. Prima di aggiornare Blender si verifica il requisito upstream e il beneficio reale; non si cambia la distribuzione per installare una skill. Nessun server MCP è necessario alla prima modellazione. CADCraft può produrre le tavole solo dopo aver dimostrato con un pezzo campione che quote, unità e scala sopravvivono all'esportazione.

La consegna prevista comprende il modello parametrico nativo, STEP per ogni pannello e per l'assieme, DXF quotati in millimetri, distinta taglio con schema di incollaggio, volume netto e distinta ferramenta. La scena Blender contiene stanza, ST-120 misurato e diffusori; non è la sorgente dimensionale per il falegname. Nessuno di questi file CAD è stato ancora prodotto: questa proposta ne definisce i parametri e i controlli.

## Lista della spesa residua

| Voce | Quantità | Prezzo osservato o accantonamento per la coppia | Stato |
|---|---|---|---|
| Stagecaptain ST-120 | 1 | 0 € residui | Già acquistato e montato, dichiarato dall'utente |
| UMC1820 | 1 | 175 € osservati | Candidata per rispettare gli otto ingressi |
| SB16PFCR25-8 | 2 | 62,90 € osservati | [31,45 € ciascuno, disponibile](https://www.soundimports.eu/en/sb-acoustics-sb16pfcr25-8.html); da simulare |
| SB26STCN-C000-4 | 2 | 72,90 € osservati | [36,45 € ciascuno, esaurito](https://www.soundimports.eu/en/sb-acoustics-sb26stcn-c000-4.html); reperire o confrontare alternativa |
| Microfono XLR calibrato EMM-6 | 1 | 78,45 € osservati | [Esaurito, rientro indicato 18 dicembre](https://www.soundimports.eu/en/dayton-audio-emm-6.html); non promettere consegna immediata |
| MDF, taglio, fresatura e rinforzi | Lotto | 80-140 € stimati | Preventivo del falegname, inclusi fori e battute |
| Assorbente interno, guarnizione, colla, inserti e viti | Lotto | 30-50 € stimati | Escludere ciò che è già disponibile |
| Condotti e connessioni di potenza a quattro poli | Coppia | 25-45 € stimati | Modello da fissare con il cabinet |
| Amplificazione esterna a quattro canali, ingressi bilanciati | Lotto | 180-280 € come obiettivo economico, non offerta verificata | Mancano modello e verifica di guadagno, rumore e alimentazione |
| Cavi: quattro linee bilanciate, potenza quattro conduttori, XLR e loopback | Lotto | 45-75 € stimati | Lunghezze da misurare, evitare doppio conteggio delle connessioni |
| Asta microfono e supporti per i diffusori | Lotto | 25-55 € stimati | Riutilizzare i supporti posseduti; verificare altezza tweeter |
| Metro laser | 1 | 25-45 € stimati | Serve al rilievo alto del soffitto; prima valutare prestito |

Il totale di pianificazione della catena di misura e dei due monitor è circa 800-1.080 €, esclusi tavolo già pagato, spedizioni, finitura estetica, utensili non disponibili, strumenti musicali, microfoni da registrazione e trattamento della stanza. Non è un preventivo chiuso: il blocco amplificazione economica non ha ancora un prodotto qualificato. I prezzi SoundImports letti presentano imponibile e prezzo lordo; l'IVA applicabile alla consegna italiana e il trasporto possono modificarli.

Un riferimento concreto per confrontare l'autocostruzione degli amplificatori è costituito da due [Behringer A800](https://www.thomann.it/behringer_a800.htm), 179 € ciascuno e disponibilità indicata in 3-4 settimane: quattro canali completi a 358 €. Il [produttore](https://www.behringer.com/en/products/0105-ABA) dichiara raffreddamento a convezione. È una soluzione ingombrante e sovradimensionata da confrontare, non la raccomandazione definitiva per un tweeter sensibile: fruscio, attenuazione e protezione vanno comunque verificati. Con questa alternativa il totale stimato diventa circa 975-1.160 €. Un modulo economico con alimentatore, contenitore, ricevitore differenziale e cablaggio può costare quanto un finale finito: il confronto riguarda l'intero oggetto, non il prezzo della sola scheda.

Per contenere la spesa non aggiungerei ora DSP hardware dedicato, DAC stereo separato, seconda coppia di casse, subwoofer, finali con ventole o licenze di programmi ridondanti. Il microfono di misura si compra con il suo file individuale: la sola sigla del modello non basta. La [guida Dayton](https://www.daytonaudio.com/images/resources/390-801-dayton-audio-emm-6-quick-reference-guide%282%29.pdf) descrive il recupero del file. Non si assume che il microfono di misura sostituisca quello per registrare la voce.

## Ubuntu Studio: ottimizzare il lavoro completo

La ricognizione SSH del 2026-11-17 osserva i7-6700, 16 GB di RAM, grafica Intel HD 530, SSD NVMe, circa 49 GiB liberi sulla radice e 303 GiB su home. La base è Ubuntu 26.04.1 con kernel 7.0.0-43-generic, `preempt=full threadirqs rcu_nocbs=all`, PipeWire 1.6.2 e WirePlumber 0.5.13. I servizi audio sono attivi, con limiti rtprio 95 e memoria bloccabile illimitata. Questi fatti non dimostrano ancora che un grafo multicanale regga senza interruzioni. Il dispositivo osservato è soltanto quello integrato; non c'è un'interfaccia USB da collaudare.

La prima correzione ha una causa osservata: `cpupower-gui.service` avvia `cpupower-gui config`, senza applicare il profilo, e fallisce con `cannot open display`. Il pacchetto installato è 1.0.0-6; il catalogo APT locale offre 1.0.0-6ubuntu0.26.04.3. Il [changelog Ubuntu](https://lists.ubuntu.com/archives/resolute-changes/2026-September/029924.html) documenta correzioni al servizio e all'applicazione dei profili. Si preferisce verificare l'aggiornamento della distribuzione, con backup, simulazione APT e prova dopo riavvio, prima di inventare un servizio sostitutivo. Nessun aggiornamento è stato eseguito in questa sessione.

La CPU usa `intel_pstate` con policy `powersave` e turbo disponibile. Il nome non prova che la CPU sia bloccata alla frequenza minima: la [documentazione del kernel](https://docs.kernel.org/admin-guide/pm/intel_pstate.html) distingue le politiche di quel driver. La proposta è un profilo bilanciato per CAD e ascolto, e un profilo performance da confrontare per registrazioni e misure. Si sceglie su interruzioni audio, temperatura e rumore delle ventole; non sulla frequenza letta a riposo. Non disattiverei a priori turbo, SMT o stati di riposo, e non aggiungerei isolamento dei core o un kernel realtime senza un problema misurato.

PipeWire è forzato oggi a 48 kHz e quantum 1024, cioè 21,33 ms per quantum: il rapporto non è una misura della latenza completa. Per ascolto va confrontato con 512; per registrare si provano 256 e poi 128, rispettivamente 5,33 e 2,67 ms per quantum, mantenendo solo il valore stabile. Il [pannello ufficiale Ubuntu Studio](https://ubuntustudio.org/audio-configuration/) gestisce questi parametri. La latenza reale comprende anche convertitori, USB, buffer DSP e plugin; si misura in loopback. Per il monitoraggio dal vivo si parte da crossover IIR e si rinvia la convoluzione FIR lunga.

Ardour rimane la DAW già installata, versione osservata 9.0. SoundCraft e un suo fork non sono prerequisiti per portare a casa la macchina. REW, VituixCAD, Akabak/VACS e FreeCAD devono aprire un progetto campione e salvare dove previsto, senza reinstallare automaticamente prefix o licenze. La catena DSP deve partire silenziata, applicare crossover e filtri di protezione prima di abilitare le quattro uscite, controllare il volume su tutte le vie insieme e tornare silenziosa se manca la configurazione. I guadagni dei finali e un'eventuale protezione passiva del tweeter si dimensionano insieme ai driver; un limite digitale non protegge da ogni guasto hardware.

Prima del trasferimento si richiedono avvio senza servizi falliti pertinenti, prova CAD con esportazione verificata, progetti audio e Wine riaperti, backup recente riletto e inventario privato delle versioni e dei collegamenti. Con l'interfaccia disponibile si aggiungono mappa canali a finali scollegati, loopback, fruscio e almeno un'ora del carico di registrazione previsto senza xruns osservati. Il banco di prova deve includere i plugin e il numero di tracce effettivi: una macchina ferma con servizi attivi non misura questo requisito. A casa si completano prenotazione DHCP, altezza dei tweeter, geometria della stanza, posizione rispetto alle pareti e misure acustiche; questi punti non impediscono di completare prima il software.

## Confine della consegna di oggi

Sono completate la ricognizione di sola lettura, la ricerca mirata dei prezzi e questa proposta confrontabile. Restano da approvare requisiti e architettura; poi si producono simulazione, modello 3D e distinta esecutiva. Le modifiche privilegiate di Ubuntu restano manuali dell'utente secondo le istruzioni del progetto; prima di eseguirle si prepara una sequenza concreta con backup e verifica. Le prove grezze con indirizzi e nomi macchina vivono soltanto in `_notes/`. Questo documento non dichiara la macchina ottimizzata, i monitor simulati o un carrello pronto da ordinare.
