# Discesa dei cavi dietro lo Stagecaptain ST-120

MS-327, 27 novembre 2026. Il confronto conserva l'A24 a 30° e le due coppie sul connettore NL4MPXX del [retro quotato](69-retro-a24-e-passaggio-cavi.md). La decisione dipende dallo spazio fra bordo posteriore del ripiano e parete. Il [rapporto numerico](../data/discesa-st120-a24.json) conserva le quattro alternative e le impronte dei dati di ingresso. La distanza reale resta sconosciuta.

## La spina e la curva del cavo

Il cavo candidato BITNER LP0285 ha quattro conduttori da 1,5 mm² e guaina Ø9,1 mm. Entrambe le quote rientrano nei limiti dichiarati per la NL4FXX-W-S. Il cavo specifica cinque diametri di raggio minimo, pari a 45,5 mm. Il modello assume prudenzialmente questa quota all'intradosso e usa 50,05 mm sull'asse. [Scheda BITNER, pagine 1-2](https://bitner-cablefactory.com/data/t4txt_photos/09383060420_BiTsound%C2%AEINSTAL%20Speaker%20Cable%20OFC.pdf).

Dal disegno della spina si prende 82,5 mm come lunghezza totale massima. Si somma tutta la sporgenza della presa, 7,05 mm, senza sottrarre la parte che entrerà nell'accoppiamento. Si aggiungono 5 mm ipotetici di tratto rettilineo e il quarto di cerchio. Il tratto verticale inizia quindi a 144,6 mm dalla piastra e circa 25 mm sopra il ripiano. Il raggio della guaina è 4,55 mm. I 110 mm del capitolo 69 sono il primo riferimento geometrico privo di questa curva. [Disegno Neutrik 20003841](https://www.neutrik.com/media/17072/download/NL4FXX-W-S.pdf?v=1).

Neutrik indica la spina a gomito NL4FRX come fuori produzione. Nella pagina della serie FXX le due spine a quattro poli documentate sono W-L e W-S diritte. Il progetto conserva quindi la diritta e confronta una flangia arretrata che ne diminuisce l'ingombro. [NL4FRX](https://www.neutrik.com/en/product/nl4frx), [serie FXX](https://www.neutrik.com/en/neutrik/products/speakon-r-loudspeaker-connectors/speakon-r-cable-connectors/fxx-series).

## Come leggere le quote sul ripiano

Il ripiano superiore nominale misura 1.180 × 300 mm a quota 930 mm. Si pone `Y=0` al bordo davanti e `Y=300` al bordo dietro. Per il cabinet sinistro `X=0` è il bordo laterale esterno. La cassa destra è speculare. Con `F` distanza del punto anteriore del cabinet dal bordo, `p` coordinata trasversale locale crescente verso il lato più arretrato, `D=190`, `t=3` ed `e` arretramento della piastra, l'asse della discesa è a `Y = F + p sin(30°) + (D+t-e+144,6) cos(30°)`. La formula sul rettangolo dà 274,5 mm di profondità e 285,5 mm di larghezza per il cabinet a 30°. [Dati ST-120](../data/postazione-st120.json).

Si aggiungono 4,55 mm di guaina e 5 mm di margine sia verso il bordo sia verso la parete. Per paragonare lo sgancio si riservano 15 mm di traslazione assiale con una fascia di presa larga 50 mm. Questi valori di progetto distinguono il cavo fermo dallo spazio di manovra. L'effettiva rotazione della ghiera, la presa con le dita e il percorso oltre il ripiano richiedono prova sul posto. Sul ripiano si conservano 10 mm davanti e dietro al rettangolo di appoggio. La sagoma reale e le rientranze restano da riscontrare.

| Variante a 30° | Posizione e arretramento della presa | Luce bordo-parete per cavo fermo | Luce con riserva di sgancio | Esito del modello |
|---|---|---:|---:|---|
| Centrale | `p=110`, `e=0`, `F=10`, bordo laterale cassa a 10 mm | 66,9 mm | 79,9 mm | Tiene la piastra già quotata. L'asse di discesa è a 357,4 mm dal bordo anteriore. |
| Spostata | `p=60`, `e=0`, `F=10`, bordo laterale cassa a 10 mm | 41,9 mm | 54,9 mm | La guaina esce 16,4 mm oltre la fascia laterale del ripiano. La posizione è scartata nel modello. |
| Arretrata al centro | `p=110`, `e=30`, `F=10`, bordo laterale cassa a 10 mm | 40,9 mm | 53,9 mm | La fascia laterale rientra. Serve un vano sigillato con una nuova tavola costruttiva. |
| Compatta | `p=60`, `e=30`, `F=14`, bordo laterale cassa a 24 mm | 19,9 mm | 32,9 mm | Restano 5,84 mm tra guaina e bordo posteriore e 5,11 mm dalla fascia laterale nello scenario di sgancio. |

Con la variante compatta lo spazio nominale per il telaio dello schermo passa da 569 a 541 mm. I 540 mm del confronto precedente entrano con circa 1 mm di margine ulteriore oltre alle distanze già riservate. La compatta richiede sedi speculari nei due mobili, mantenendo il verso di montaggio della flangia. L'arretramento da 30 mm lascia 9,7 mm fra l'inviluppo interno ipotizzato e il woofer. La verifica tiene conto dell'inviluppo corrente e non comprende ingombro reale di un vano, utensili o capicorda.

## Scelta condizionata e verifica

Con circa 80 mm disponibili nel modello si conserva la piastra centrale, che richiede meno lavorazioni. A partire da circa 54 mm si può approfondire la centrale arretrata, conservando spazio per lo schermo. Con circa 33 mm la compatta entra nelle riserve calcolate. Una luce inferiore richiede di rivedere il percorso, la spina o l'accesso alla presa fuori dal ripiano. A filo parete nessuna delle quattro discese rispetta la riserva. Queste soglie valgono per le posizioni in tabella. I decimali facilitano il confronto e non stimano la precisione del mobile installato.

Il cavo candidato ha resistenza massima di 12,8 Ω/km per conduttore a 20 °C. Tre metri di tratta, scelti solo come caso di confronto, danno circa 0,077 Ω per andata e ritorno e 0,17 dB di attenuazione su 4 Ω resistivi. La lunghezza reale dipende dall'ansa e dalla posizione dei finali. Lo schema conserva i quattro conduttori e nessun ritorno comune. [Dati di sezione e resistenza](https://bitner-cablefactory.com/data/t4txt_photos/09383060420_BiTsound%C2%AEINSTAL%20Speaker%20Cable%20OFC.pdf).

Verificati 101 punti del quarto di cerchio contro il massimo analitico. Tre contrasti rendono leggibile la soglia: parete al bordo respinge tutte, parete a 50 mm distingue centrale e compatta nella riserva di sgancio, e spostare soltanto la presa porta la guaina fuori fascia. Il rilascio della piastra resta subordinato alla luce reale, alla possibilità di sgancio e alla tenuta del vano. Le verifiche fisiche restano differite per ADR-055.
