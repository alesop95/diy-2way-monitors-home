# Fase 2: modellazione della stanza e simulazione acustica

> Seconda fase operativa. Ricostruisce la geometria dell'ambiente in tre dimensioni e la usa come base per la simulazione del comportamento delle sorgenti. Include la valutazione degli strumenti alternativi, che nel documento sorgente occupava molto spazio e che qui viene ricondotta a una decisione.

## L'obiettivo

Il modello geometrico non serve a fare belle immagini: serve a essere validato dalla misura della fase 1 e poi usato dalla fase 5. Deve contenere le pareti, il soffitto con la sua pendenza, i mobili, lo schermo, la scrivania e la seduta, perché sono tutti oggetti che riflettono, e deve avere le posizioni candidate dei monitor.

Lo strumento è Blender, per tre motivi concreti: dà libertà geometrica superiore a un CAD architettonico, esporta nei formati aperti che servono a valle, cioè `.obj` e `.dae`, ed è già preinstallato nella distribuzione Ubuntu Studio, quindi non aggiunge nulla da configurare.

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
