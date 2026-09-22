# Rilievo geometrico della stanza: che cosa si misura, in che ordine, e su che cosa si scrive

> Allegato operativo alla fase 2. La pagina della fase 2 decide con quale strumento si costruisce il modello e da dove escono le dimensioni; questa decide quali quote si prendono, in quale ordine e in quale formato si scrivono, perché il rilievo si fa una volta sola e una quota dimenticata costa un secondo viaggio nella stanza con la scala. Il fronte è tracciato come PA-020.
>
> Stato: protocollo non ancora eseguito, scritto il 2026-09-21. Le quote delle tabelle sono vuote e si riempiono in questa pagina, che diventa così il verbale del rilievo oltre che la sua procedura. La sezione di troubleshooting nasce lo stesso giorno con due voci sole, e la sua brevità è la regola e non una mancanza: una voce nasce da un caso incontrato e non da una previsione, quindi qui stanno i due casi incontrati nella prova di cattura e nient'altro, e la sezione crescerà eseguendo.

## Perché esiste un protocollo invece di un pomeriggio di misure

Il rilievo sembra il lavoro più semplice del progetto e ha la proprietà peggiore: i suoi errori non si manifestano come errori. Una quota sbagliata di cinque centimetri non produce un modello visibilmente storto, produce una frequenza modale spostata di mezzo hertz che nessuno noterà; una scala sbagliata del due per cento sposta tutti i modi nella stessa direzione e si presenta, tre fasi più avanti, come un disaccordo fra Octave e REW che chi lo incontra attribuisce alla modellazione. Le ragioni sono argomentate nella pagina della fase 2, alla sezione sulla precisione, e non si ripetono qui.

Da questo discende la sola cosa che questo protocollo aggiunge davvero, cioè la completezza in un solo passaggio. Il rilievo alimenta tre fasi diverse che chiedono cose diverse, e due di quelle cose sono osservabili soltanto stando dentro la stanza. Chi misura pensando al modello geometrico prende le distanze e dimentica i materiali, e i materiali servono al calcolo del riverbero.

## Che cosa le fasi a valle pretendono, e quale campo si dimentica

La fase 3 calcola le frequenze modali, e per farlo vuole le tre dimensioni principali. Poiché il soffitto è spiovente, la formula rettangolare vale come approssimazione di partenza e non come risultato, il che è dichiarato nella pagina della fase 3: servono quindi le due altezze e la pendenza, non una altezza media, perché è proprio la pendenza che distingue questa stanza da una scatola.

La stessa fase calcola il tempo di riverberazione secondo Sabine, che lega il RT60 al volume e all'assorbimento totale delle superfici. L'assorbimento non è una proprietà della geometria ma del materiale, quindi ogni superficie va rilevata con la sua area e con il materiale di cui è fatta. È il campo che si dimentica, ed è anche il solo che non si può ricostruire dopo: un'area si ricalcola dalle quote, un intonaco non si indovina da casa.

La fase 2 costruisce il modello in Blender, che deve contenere pareti, soffitto con la sua pendenza, mobili, schermo, scrivania e seduta, perché sono tutti oggetti che riflettono, più le posizioni candidate dei monitor. Ne segue che di ogni arredo servono l'ingombro e la posizione, non la forma: un mobile si modella come un parallelepipedo, e misurarne le maniglie è tempo buttato.

La fase 1 misura la stanza con il microfono al punto di ascolto, all'altezza dell'orecchio, quindi quell'altezza è una quota del rilievo e non un dettaglio della misura. Dalla discussione riportata nella pagina della fase 1 vengono due vincoli già noti: il punto di ascolto sta sul lato dove il soffitto è più basso, e la posizione della scrivania non è negoziabile. Il rilievo li registra come sono, non come sarebbe comodo che fossero.

## La convenzione di origine e assi, da fissare prima della prima misura

Senza un'origine dichiarata una posizione non è un dato: dire che la scrivania sta a due metri e dieci non dice da dove. Si sceglie un angolo del pavimento, si fotografa, e lo si dichiara qui sotto come origine; tutte le posizioni sono poi distanze dai due muri che lo formano, misurate lungo il pavimento.

```
z  altezza dal pavimento, positiva verso l'alto
|
|      y  distanza dalla parete che contiene l'origine e corre nella direzione piu' lunga
|     /
|    /
|   /
|  /
| /
+-------------- x  distanza dall'altra parete che forma l'angolo di origine
origine: angolo del pavimento dichiarato in tabella A
```

La regola che rende utile la convenzione è che si misura sempre dagli stessi due muri e mai da un mobile, perché un mobile si sposta e una parete no. Dove un muro non sia accessibile per l'ingombro di un arredo, si misura dal muro opposto e si annota che la quota è complementare, invece di misurare dal mobile.

## La sequenza, e perché l'ordine non è indifferente

Si comincia dal guscio con il metro laser, prima della scansione. La ragione è che la scansione va portata in scala sulle quote del guscio, quindi il guscio deve esistere prima: fare il contrario significa scalare la scansione su se stessa e scoprire dopo che non c'è nulla contro cui verificarla.

Si prosegue con la scansione del telefono, nella stessa sessione e senza spostare nulla. A fine cattura l'applicazione chiede con quale modalità elaborare, e per la stanza si sceglie `Area`, che lavora per fusione di profondità, e non `Detail`, che lavora per fotogrammetria pur essendo quella che l'applicazione raccomanda: la raccomandazione vale per l'oggetto tipico dei suoi utenti e non per un ambiente, e la fotogrammetria dipende dal riconoscimento della trama. La distinzione è stata misurata in MS-161. Due accorgimenti vengono dalla pagina della fase 2 e non si ripetono se non nella forma operativa: si attaccano qualche decina di foglietti adesivi o crocette di nastro di carta sulle pareti lisce, distribuiti e non allineati, perché una parete tinteggiata non offre punti riconoscibili all'algoritmo, che è la stessa causa per cui `Detail` non va usata sull'ambiente; e il soffitto spiovente si inquadra deliberatamente, perché è la parte che si tende a saltare ed è quella da cui dipende tutto.

Si prendono poi le quattro diagonali di controllo, con il metro laser, nella stessa sessione della scansione e con gli arredi nella stessa posizione. È il punto in cui un rilievo si salva o si perde: se qualcuno sposta una sedia fra la scansione e le diagonali, il confronto misura lo spostamento della sedia invece della deriva di scala.

Si tolgono i foglietti, e soltanto dopo si lascia la stanza. Le tabelle vanno riempite stando dentro, non a memoria dopo cena.

Il ricalco in Blender viene dopo e non richiede di essere nella stanza: si importa la mesh come sagoma, si riscala sulle quote del guscio, si ricalcano pareti e soffitto come piani a poche facce, si mettono gli arredi come parallelepipedi alle posizioni della tabella D, e si esporta in `.obj` e `.dae`. Il modello che entra nel calcolo è quello ricalcato e non la scansione, per la ragione argomentata nella pagina della fase 2.

## Tabella A, il guscio

L'origine si dichiara qui, in parole, prima delle quote: sostituire questa riga con l'angolo scelto e il riferimento della fotografia.

| Quota | Simbolo | Valore | Nota |
|---|---|---|---|
| lunghezza alla base, lungo y | `Ly` |  | fra le facce interne dei muri |
| larghezza alla base, lungo x | `Lx` |  | fra le facce interne dei muri |
| altezza al lato basso del soffitto | `h_basso` |  | misurata in verticale, dal pavimento |
| altezza al lato alto del soffitto | `h_alto` |  | misurata in verticale, dal pavimento |
| distanza orizzontale fra i due punti di altezza | `d_pend` |  | misurata lungo il pavimento, non lungo il soffitto |
| pendenza del soffitto | `p` |  | calcolata come `(h_alto - h_basso) / d_pend`, non misurata come angolo |
| quota del pavimento, eventuali dislivelli | | | annotare solo se esistono |

Il motivo per cui la pendenza si calcola invece di misurarla merita una riga, perché il metro laser invita a fare il contrario. Uno strumento a mano libera puntato lungo una superficie inclinata misura la distanza dal primo ostacolo che incontra, e l'angolo che si crede di leggere dipende da come si tiene lo strumento; due altezze verticali e una distanza orizzontale sono invece tre misure che lo strumento fa bene, e la pendenza che ne esce è un rapporto fra numeri e non una posa della mano.

## Tabella B, le aperture

| Apertura | Larghezza | Altezza | Posizione x | Posizione y | Quota inferiore dal pavimento | Nota |
|---|---|---|---|---|---|---|
| porta |  |  |  |  |  | verso di apertura |
| finestra 1 |  |  |  |  |  | vetro singolo o doppio |
| finestra 2 |  |  |  |  |  |  |

Le aperture contano due volte, come geometria e come materiale, perché un vetro riflette quasi tutto alle basse frequenze e una porta di legno no. Il verso di apertura serve al modello solo se la porta resta aperta durante le misure, e in quel caso va modellata.

## Tabella C, superfici e materiali, che è la tabella che si dimentica

| Superficie | Area | Materiale osservato | Nota |
|---|---|---|---|
| pavimento |  |  | eventuale tappeto con la sua area a parte |
| soffitto spiovente |  |  |  |
| parete con la porta |  |  |  |
| parete con la finestra |  |  |  |
| parete dietro il punto di ascolto |  |  | è il secondo problema noto della stanza |
| parete rimanente |  |  |  |
| vetri |  |  | dalla tabella B |

L'area si ricava dalle quote e non va misurata a parte; il materiale invece si osserva, e va scritto come si vede e non come si suppone: intonaco su muratura, cartongesso, legno, vetro, moquette, parquet. Il coefficiente di assorbimento non si scrive qui, perché non è un dato del rilievo ma un valore da una fonte, e la regola del progetto vuole che ogni valore così abbia la sua fonte dichiarata al momento in cui entra nel calcolo.

## Tabella D, arredi e ingombri

| Oggetto | Larghezza | Profondità | Altezza | Posizione x | Posizione y | Nota |
|---|---|---|---|---|---|---|
| scrivania |  |  |  |  |  | posizione non negoziabile, fase 1 |
| schermo |  |  |  |  |  | altezza del centro dello schermo |
| seduta |  |  |  |  |  | posizione d'uso, non da riposo |
| mobile 1 |  |  |  |  |  |  |
| mobile 2 |  |  |  |  |  |  |

Di ogni oggetto serve il parallelepipedo che lo contiene e la posizione di un suo angolo rispetto all'origine, che è quanto basta a farne una superficie riflettente nel modello. Un oggetto piccolo rispetto alla lunghezza d'onda che interessa non riflette in modo utile e si può omettere, ma l'omissione va scritta invece di essere silenziosa.

## Tabella E, punto di ascolto e posizioni candidate dei monitor

| Grandezza | Valore | Nota |
|---|---|---|
| altezza dell'orecchio dal pavimento, seduti in posizione d'uso |  | è la quota del microfono nella fase 1 |
| distanza dell'orecchio dalla parete alle spalle |  | governa il secondo problema noto |
| distanza dell'orecchio dalle due pareti laterali |  | l'asimmetria, se c'è, va registrata |
| posizione candidata monitor sinistro, x, y, z |  | z è l'altezza del centro del woofer |
| posizione candidata monitor destro, x, y, z |  |  |
| distanza fra i due monitor |  |  |
| distanza monitor-orecchio |  | la stessa per i due, se differisce va scritto |

## Tabella F, le quattro diagonali di controllo della scala

| Diagonale | Da punto | A punto | Misurato col laser | Letto sul modello | Scarto |
|---|---|---|---|---|---|
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |
| 3 |  |  |  |  |  |
| 4 |  |  |  |  |  |

Le quattro si scelgono lunghe e in direzioni diverse, fra punti che si riconoscano anche nella scansione, per esempio due angoli opposti del pavimento, un angolo del pavimento e lo spigolo opposto del soffitto, due spigoli di aperture. I punti si descrivono a parole nelle prime due colonne, perché una diagonale fra punti non identificabili non è ripetibile e una verifica non ripetibile vale quanto una non fatta.

Il criterio è che lo scarto resti sotto l'uno per cento su ciascuna delle quattro. Se supera, si riscala il modello sulle quattro prima di andare avanti; se supera in modo diverso da diagonale a diagonale non è una deriva di scala ma una deformazione, e allora la scansione non è riscalabile e il guscio va ricostruito dalle sole quote del laser.

## Che cosa serve avere in mano

Il metro laser, che è l'unico acquisto e costa venti o trenta euro. Il telefono con Scaniverse installato, per la via decisa in PA-020. Qualche decina di foglietti adesivi o un rotolo di nastro di carta per le crocette. Una scala o uno sgabello per le altezze del soffitto, che è anche la ragione per cui conviene avere le tabelle stampate invece di battere le quote su un telefono tenendosi con una mano.

Un metro a nastro non sostituisce il laser sulle altezze del soffitto spiovente, dove il punto da raggiungere è fuori portata, ma sostituisce benissimo il laser sugli ingombri degli arredi, che si misurano da vicino. Dove il laser non fosse ancora arrivato, le tabelle B, C, D ed E si possono riempire con un metro a nastro e la tabella A no, ed è un modo sensato di spezzare il lavoro invece di attenderlo tutto.

## Troubleshooting: sintomo, causa, rimedio

Due voci sole, ed è la regola di questo progetto: una voce nasce da un caso incontrato e non da una previsione. Entrambe vengono dalla prova di cattura del 2026-09-21 sul Galaxy S25 Ultra, registrata in MS-161.

### A, l'elaborazione si ferma sul passo di ricerca dei punti corrispondenti

Sintomo: scelta la modalità `Detail`, l'elaborazione avanza di pochi punti percentuali sul passo dichiarato come `MATCHING FEATURES` e si interrompe con un errore. Causa: quella modalità è fotogrammetrica, quindi ricostruisce la geometria riconoscendo gli stessi punti in immagini diverse, e il soggetto era un foglio bianco con una scatolina di cartone chiaro, cioè due superfici quasi prive di trama; il passo che fallisce è letteralmente quello che cerca i punti che non esistono. Rimedio: dare trama al soggetto oppure cambiare modalità.

Per il riferimento di scala il rimedio migliore è il primo, e non costa nulla: si usa un foglio stampato invece di uno bianco, cioè una pagina di testo qualunque. Resta esattamente 297 millimetri per la ISO 216, quindi il riferimento non perde precisione, e diventa una superficie ricca di punti riconoscibili. Per la stanza il rimedio è il secondo, cioè `Area`, che non dipende dalla trama, ed è la ragione per cui la sequenza prescrive quella modalità e non la raccomandata.

Il collegamento che vale ricordare è che questo non è un difetto dell'applicazione né del dispositivo: è il difetto strutturale della fotogrammetria che la pagina della fase 2 descrive per le pareti tinteggiate, incontrato su scala ridotta. La stessa causa spiega perché il protocollo prescrive i foglietti adesivi sulle pareti lisce.

### B, l'anteprima della fotocamera appare a righe diagonali rosse e bianche

Sintomo: registrando lo schermo durante la cattura, l'anteprima della fotocamera non si vede e al suo posto compare un motivo a righe diagonali rosse e bianche. Causa presunta, non verificata: Android sostituisce con un motivo segnaposto le superfici che non consente di registrare, e l'anteprima della fotocamera è una di queste, quindi l'artefatto sta nella registrazione e non nell'applicazione. Rimedio: non registrare lo schermo durante la cattura, e per documentare un passaggio usare uno scatto singolo o descriverlo.

La voce resta marcata come presunta finché la verifica non è fatta, e la verifica costa un secondo: si guarda lo schermo mentre si scansiona senza registrare. La distinzione conta, perché se le righe comparissero anche senza registrazione il problema sarebbe nell'accesso alla fotocamera e nessuna scelta di modalità di elaborazione lo salverebbe.
