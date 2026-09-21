# Fase 2: modellazione della stanza e simulazione acustica

> Seconda fase operativa. Ricostruisce la geometria dell'ambiente in tre dimensioni e la usa come base per la simulazione del comportamento delle sorgenti. Include la valutazione degli strumenti alternativi, che nel documento sorgente occupava molto spazio e che qui viene ricondotta a una decisione.

## L'obiettivo

Il modello geometrico non serve a fare belle immagini: serve a essere validato dalla misura della fase 1 e poi usato dalla fase 5. Deve contenere le pareti, il soffitto con la sua pendenza, i mobili, lo schermo, la scrivania e la seduta, perché sono tutti oggetti che riflettono, e deve avere le posizioni candidate dei monitor.

Lo strumento è Blender, per tre motivi concreti: dà libertà geometrica superiore a un CAD architettonico, esporta nei formati aperti che servono a valle, cioè `.obj` e `.dae`, ed è già preinstallato nella distribuzione Ubuntu Studio, quindi non aggiunge nulla da configurare.

## Come si ottiene la geometria, che questa pagina dava per scontata

La sezione precedente dice quale strumento costruisce il modello e che cosa il modello deve contenere, e tace su da dove escano le dimensioni. È una lacuna reale, emersa da una domanda dell'utente il 2026-09-21, e va colmata prima della fase 1 perché il rilievo si fa una volta sola e rifarlo costa quanto farlo.

Le vie sono quattro e non valgono lo stesso. La scelta fra loro dipende da quale dispositivo si ha in mano, quindi resta aperta come PA-020 finché quel dato non è noto.

La prima è il metro laser, che costa venti o trenta euro e misura al millimetro. È esatta e lenta. Funziona bene sulle tre dimensioni principali e male su tutto il resto: un soffitto spiovente richiede due altezze e una pendenza in punti spesso irraggiungibili, e rilevare a mano scrivania, schermo, seduta e mobili è mezza giornata che produce soprattutto errori di trascrizione.

La seconda è la fotogrammetria da fotografie, con strumenti liberi e nativi su Linux come Meshroom, che usa AliceVision, oppure COLMAP. Il metodo ricostruisce la geometria riconoscendo gli stessi punti in immagini diverse, e una stanza è il suo caso peggiore: una parete tinteggiata non offre punti da riconoscere, quindi il modello risulta bucato proprio dove servono le superfici che contano. Porta inoltre un limite che non è un difetto ma una proprietà del metodo: dalle sole immagini non si ricava alcuna dimensione assoluta, quindi il modello nasce senza scala e va riscalato includendo nell'inquadratura un oggetto di lunghezza nota.

La terza è la scansione LiDAR[^lidar] da un dispositivo mobile che ne abbia il sensore, cioè gli iPhone e gli iPad Pro dal modello 12 Pro in avanti. È la via che al chiuso funziona davvero, per due ragioni: il sensore misura distanze, quindi la scala è metrica per costruzione, e le superfici lisce non sono un ostacolo perché non occorre riconoscere alcuna trama. Le applicazioni costruite su RoomPlan restituiscono un modello parametrico con pareti, aperture e ingombri dei mobili già quotati; quelle come Polycam o Scaniverse restituiscono una mesh. In entrambi i casi il rilievo dura minuti e la precisione è dell'ordine del centimetro.

La quarta è l'equivalente su Android, basato sull'interfaccia di profondità di ARCore o su un sensore a tempo di volo dove presente. Esiste e funziona, ma la resa dipende dal dispositivo molto più che nel caso precedente, quindi non si può raccomandare senza sapere quale sia.

### La scansione è un riferimento su cui modellare, non il modello

È il punto che decide se il rilievo faccia risparmiare tempo o lo faccia perdere, e va enunciato prima di scegliere lo strumento.

Una mesh di scansione porta centinaia di migliaia di triangoli, con buchi, rumore e superfici che non sono piane. A valle non serve a nulla, e non per una questione di prestazioni: l'analisi modale e la simulazione vogliono piani ideali a cui assegnare un coefficiente di assorbimento, mentre una scansione offre una nuvola di triangoli a cui non si assegna niente. Il modo corretto di usarla è importarla in Blender come sagoma e ricalcarvi sopra una stanza pulita a poche facce, prendendo dalla scansione le proporzioni, gli ingombri e le posizioni, che sono precisamente le cose che a mano costano tempo. Il lavoro è di un'ora invece che di mezza giornata, e il modello che entra nel calcolo è quello ricalcato.

Ne segue che la scansione non sostituisce la comprensione della stanza: la sostituisce soltanto la trascrizione.

### Quanta precisione serve, e quale errore è quello pericoloso

Conviene fissare l'ordine di grandezza, perché è facile inseguire una precisione che non cambia alcun risultato e trascurare l'errore che invece li cambia tutti.

La frequenza del primo modo assiale su una dimensione vale `c/(2L)`, quindi su quattro metri cade attorno a 42,9 Hz con la velocità del suono a 343 metri al secondo. Sbagliare quella dimensione di cinque centimetri sposta il modo di circa mezzo hertz, cioè poco più dell'uno per cento, che è trascurabile rispetto all'errore che si commette comunque assumendo pareti perfettamente rigide. Il centimetro basta; il millimetro non serve e non si paga.

L'errore da cui difendersi è di natura diversa, ed è la deriva di scala. Un rilievo che sbagli la scala del due per cento non produce un errore casuale su una quota, produce uno spostamento del due per cento su tutte le frequenze modali, tutte nella stessa direzione. Poiché il criterio di validazione del modello, enunciato nella pagina della fase 1, è che i modi previsti in Octave coincidano con i picchi misurati in REW, un errore di scala si presenta come un disaccordo sistematico fra modello e misura, e chi lo incontra lo attribuisce alla modellazione invece che al rilievo. Una scansione lunga può derivare in questo modo, un metro laser no.

La regola operativa che ne discende costa dieci minuti e vale per tutte e quattro le vie. Si prendono con il metro laser tre o quattro distanze fra punti ben identificabili, scelte lunghe e in direzioni diverse, e si verifica che il modello le riproduca. Se non le riproduce, si riscala il modello su di esse prima di andare avanti. Le distanze misurate e lo scarto trovato si scrivono accanto al modello, perché una verifica di scala non ripetibile vale quanto una non fatta.

[^lidar]: *LiDAR*, Light Detection and Ranging - sensore che misura la distanza di una superficie dal tempo di volo di un impulso luminoso; a differenza della fotogrammetria restituisce dimensioni assolute senza bisogno di un riferimento di lunghezza nota nell'inquadratura.

## La catena di simulazione, e la sua ambiguità nel sorgente

Qui il documento sorgente propone due catene alternative senza scegliere, e il progetto ha bisogno di una scelta. Vale esporre entrambe e dire quale prevale.

La prima catena è Blender più Pachyderm. Pachyderm è uno strumento di acustica architettonica di buona qualità, che calcola riverbero, indice di trasmissione del parlato e distribuzione dell'energia. Il problema è dichiarato nello stesso documento: richiede Rhinoceros e Grasshopper, che non girano nativamente su Linux. Questo lo esclude nella pratica, e la sezione dedicata nel sorgente era rimasta un segnaposto vuoto, cioè non era mai stata affrontata davvero.

La seconda catena è Blender più Octave con MATAA, ed è quella effettivamente perseguita. La geometria esce da Blender e il calcolo modale entra in Octave con script propri, come descritto nella pagina della fase 3. È meno automatica di un simulatore commerciale ma è interamente nativa, interamente ispezionabile e non dipende da software che non può girare sulla macchina.

La conclusione operativa è che Pachyderm resta annotato come alternativa non praticabile su questa macchina, e la catena di riferimento è Blender con Octave.

## La famiglia EASE, e a che cosa serve davvero

Il progetto ha sul disco un corredo notevole di software AFMG, con tre versioni di EASE Focus e un database di GLL molto ampio, e questo ha generato nel documento sorgente una lunga esplorazione. Vale ridurla a ciò che serve, perché il rischio è usare uno strumento per un compito che non è il suo.

EASE SpeakerLab, gratuito, serve a creare il modello acustico di un singolo altoparlante, cioè a produrre un file `.gll` o `.spk` partendo da misure o specifiche, definendo geometria, risposta in frequenza, direttività e fase. Non simula un impianto né una stanza. Nel workflow di questo progetto il suo posto naturale è a valle della costruzione: una volta misurato il monitor autocostruito, SpeakerLab è lo strumento con cui trasformare quelle misure in un GLL utilizzabile dagli altri programmi della famiglia.

EASE Address 2.1 è escluso. Calcola la copertura di colonne di altoparlanti in ambienti semplici, lavora solo in due dimensioni sulla vista laterale, e non gestisce geometrie complesse né riflessioni multiple. Per una stanza domestica irregolare con soffitto spiovente non è lo strumento.

EASE Focus 3 simula sistemi di diffusione in due e tre dimensioni usando i GLL, e dà mappe di copertura SPL e il livello in punti specifici. Il suo limite è dichiarato: calcola il campo diretto, non il riverbero realistico né la propagazione complessa in ambienti generici. È gratuito e la licenza è inclusa.

EASE JR è la versione a pagamento di fascia bassa della famiglia completa, e fa quello che Focus non fa: definisce la geometria della stanza in tre dimensioni, assegna coefficienti di assorbimento diversi a pareti, soffitto e arredi, calcola riflessioni multiple e tempi di riverberazione, e mostra la distribuzione del suono in campo diretto e riverberato. Il suo limite, cioè il numero ridotto di sorgenti, è irrilevante quando le sorgenti sono due monitor.

La valutazione comparativa che ne segue è quella dichiarata nel sorgente, e va registrata come tale: per ottimizzare monitor in una stanza domestica EASE JR è superiore a EASE Focus 3, perché restituisce il comportamento ambientale e non soltanto la copertura diretta. Resta però software a pagamento, e il progetto non ne dispone. Nella pratica il ruolo di EASE JR nel workflow è coperto da Akabak nella fase 5, che fa elettroacustica e acustica ambientale in un solo passaggio ed è gratuito per uso privato.

Ne discende l'uso concreto di EASE Focus 3 in questo progetto: uno strumento di verifica rapida della copertura e del tilt di un diffusore di cui si abbia il GLL, utile per confronto e per esplorazione, non il motore della simulazione ambientale.

## Le tre versioni di EASE Focus sul disco, e quale usare

Le versioni presenti sono la 3.0.18, la 3.1.10 arrivata da un workshop con materiale didattico e progetti di esempio, e la 3.1.260, che è la più recente della linea gratuita.

Le differenze fra la 3.0.18 e la 3.1.10 sono documentate dal changelog del produttore.

| Area | Cambiamento dalla 3.0.18 alla 3.1.10 | Impatto per questo progetto |
|---|---|---|
| Compatibilità GLL | supporto ai GLL versione 2.6 e successive | medio: serve solo per caricare GLL recenti |
| Database AFMG | nuovo servizio di database per scaricare e aggiornare la libreria GLL | alto: evita di scaricare a mano ogni GLL dal sito del costruttore |
| Interfaccia e workflow | editing dei progetti, gestione del layout, scala e zoom migliorati | basso: comodità, non cambia la fisica |
| Prestazioni | calcolo SPL e tempi di rendering ottimizzati | irrilevante con una o due sorgenti in un ambiente piccolo |
| Correzioni | errori di rendering e compatibilità con Windows 10 e 11 | medio: meno crash, e conta soprattutto sotto Wine |

La 3.1.260 aggiunge correzioni, aggiornamenti di compatibilità e qualche ottimizzazione nella gestione dei file GLL, mantenendo gli stessi limiti concettuali. Le versioni sono retrocompatibili, quindi i GLL del 2016 continuano a funzionare.

La conclusione è installare la 3.1.260 e ignorare le altre due. Le ragioni sono l'accesso ai GLL recenti, il database integrato che risparmia la ricerca manuale, e la voce sulle correzioni di rendering, che sotto Wine è quella che pesa più di tutte. Le due versioni precedenti restano sul disco come materiale d'archivio, non come installazioni parallele: tre versioni dello stesso programma in tre prefix sono manutenzione senza ritorno.

## Il vincolo dei GLL per un diffusore autocostruito

C'è un limite strutturale nell'uso della famiglia EASE in un progetto DIY, e va detto prima di investirvi tempo. Un GLL è il modello acustico di un diffusore specifico, fornito e licenziato dal costruttore. Un monitor autocostruito non ha un GLL ufficiale, quindi si può soltanto approssimarlo con il GLL di un modello commerciale simile in risposta e dispersione, oppure crearne uno partendo da misure reali con EASE SpeakerLab o con software di misura come ARTA.

Questo significa che, finché i monitor non sono costruiti e misurati, ogni simulazione fatta in EASE Focus su un GLL di un altro diffusore è un esercizio di approssimazione, utile per capire l'ordine di grandezza degli effetti ma non per progettare. La progettazione vera passa da VituixCAD e Akabak, che lavorano sui parametri dei driver invece che su un modello preconfezionato del diffusore finito.

## Alternative annotate e non valutate

Ramsete 27b compare nel corredo software e nel documento sorgente come alternativa per l'acustica degli ambienti, ma la sezione era un segnaposto vuoto. Resta annotato come da valutare, senza alcuna affermazione sul suo funzionamento sotto Wine o sulla sua idoneità, perché nulla di ciò è stato verificato.
