# Discesa cavi e ingombro di servizio dello ST-120

MS-327, ricerca narrativa del 27 novembre 2026. Quesito: quanto spazio serve per piegare un cavo a quattro conduttori e sganciare la presa candidata della MS-326 senza attribuire al ripiano una distanza dalla parete mai misurata? Confrontare un cavo con raggio esplicito e la reperibilità documentale di una spina a gomito del produttore.

Query: `site:neutrik.com NL4FRX right angle discontinued successor NL4FXX W speakON 4 pole fit NL4MPXX technical drawing`, `site:neutrik.com speakon 4 pole right angle NL4FRX low profile FXX angle current Neutrik`, `4 x 1.5 speaker cable outer diameter minimum bend radius manufacturer Sommer Meridian SP415 data`, `site:bitner-cablefactory.com LP0285 BiTsound INSTAL 4x1.5 9.1 minimum bending radius installation`. La ricerca non ha consultato rivenditori per prezzo o stock.

| Fonte | Copertura | Impiego |
|---|---|---|
| [Neutrik NL4FXX-W-S](https://www.neutrik.com/en/product/nl4fxx-w-s) e [disegno 20003841](https://www.neutrik.com/media/17072/download/NL4FXX-W-S.pdf?v=1) | Specifiche meccaniche e quote della spina diritta | Limite 82,5 mm di lunghezza totale. L'accoppiamento può sovrapporre parte del naso alla presa. Si usa la somma conservativa con la sporgenza della flangia, anziché stimare la sovrapposizione. |
| [Neutrik NL4FRX](https://www.neutrik.com/en/product/nl4frx) | Stato del prodotto e tipologia | Il produttore lo indica fuori produzione. È un riferimento di forma e non entra nella distinta candidata. |
| [Neutrik serie FXX](https://www.neutrik.com/en/neutrik/products/speakon-r-loudspeaker-connectors/speakon-r-cable-connectors/fxx-series) | Elenco dei tre prodotti | Le due varianti a quattro poli nella pagina sono W-L e W-S. Questo rilievo non esclude altre serie o produttori. |
| [BiTsound INSTAL Speaker Cable OFC, BITNER](https://bitner-cablefactory.com/data/t4txt_photos/09383060420_BiTsound%C2%AEINSTAL%20Speaker%20Cable%20OFC.pdf) | Specifica di curvatura e riga LP0285, pagine PDF 1-2 | 4 × 1,5 mm², guaina Ø9,1 mm, raggio minimo 5 diametri e resistenza massima 12,8 Ω/km per conduttore a 20 °C. Il riferimento del raggio nella sezione non è definito. Il modello assume il raggio sul bordo interno. |

La lunghezza della spina non determina la luce per montarla. Il modello separa l'asse della discesa fissa dalla traslazione riservata per sganciare. Non quantifica lo spazio effettivo per mano e torsione, né la distanza reale dalla parete. Le quote ufficiali dello ST-120 sono già conservate in data/postazione-st120.json. Le due foto autorizzate nel giro precedente sono state cancellate allora, senza una nuova lettura in MS-327.
