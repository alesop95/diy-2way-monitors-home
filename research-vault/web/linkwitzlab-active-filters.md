# Linkwitz Lab: fonte tecnica prioritaria

URL canonico: [Active Filters](https://www.linkwitzlab.com/filters.htm). Autore: Siegfried Linkwitz. Accesso: 2026-11-20. Priorità esplicita assegnata dall'utente durante la ricerca sul crossover. Fonte primaria di progetto e didattica; la priorità non equivale a verifica di tutto il sito.

## Lettura verificata e collegamento al nostro lavoro

Sono stati letti l'inquadramento dei circuiti a livello di linea e i passaggi delle sezioni 2 e 3 su LR2/LR4: relazione fra filtro elettrico e risposta degli altoparlanti montati, rami LR4 a -6 dB all'incrocio, cascata di sezioni del secondo ordine. I valori arrotondati del sito sono interpretati come tali; nei calcoli usiamo Q=1/sqrt(2), non 0,71 esatto.

Letto anche il testo della sezione 4 sulle reti allpass di primo ordine per correggere differenze di fase fra driver. I circuiti nelle immagini collegate non sono stati analizzati componente per componente. Le formule e i grafici prodotti nel dossier vengono derivati e ricalcolati nel nostro modello; non sono figure copiate dal sito. Le sezioni 5-8 su shelving e notch restano punti di studio successivi, senza attribuire a tutte una lettura analitica già completata.

Lettura successiva MS-301: sezione 9, Linkwitz Transform, per sostituire la coppia di poli del modello di cassa chiusa con quella target. Il progetto deriva la funzione complessa in docs/63, include HP35 e verifica dodici configurazioni nel motore CamillaDSP 4.1.3, con un target alterato come controllo negativo. La sensibilità ai parametri rimane esplicita: la cancellazione nominale non equivale a una taratura dell'esemplare. Nessuna analisi componente per componente del circuito analogico o lettura integrale del sito.

## Perché è una fonte principale

Collega realizzazione analogica, risposta del trasduttore e geometria: consente di confrontare PC, Raspberry Pi e analogico sullo stesso problema acustico. Nel nostro progetto serve a evitare che la scelta del software venga scambiata per la progettazione del diffusore. Le conclusioni sul monitor reale restano soggette alle misure e ai limiti dei driver scelti.

Rimandi: [registro fonti del confronto](../crossover-pc-pi-analogico/sources.md), [protocollo](../crossover-pc-pi-analogico/scope.md), [fonti generali](../../docs/90-riferimenti/fonti.md). Le eventuali letture successive aggiornano questa scheda per sezione, senza dichiarare studiata in blocco l'intera raccolta Linkwitz Lab.
