# Strumenti posseduti e caratterizzazione

Inventario aperto il 2026-11-18 su dichiarazione dell'utente. Il progetto comprende anche lo studio degli amplificatori già disponibili, il loro impiego nell'home recording e il recupero dell'amplificatore per basso. La loro caratterizzazione procede accanto alla progettazione dei monitor: la risposta di un combo per strumento serve uno scopo diverso dalla risposta target della coppia da mix.

| ID | Prodotto dichiarato | Materiale acquisito | Lavoro aperto |
|---|---|---|---|
| AMP-001 | Marshall MG15 | Manuale scansionato fornito dall'utente, OCR e pagine verificate visivamente | Conferma della revisione fisica, schema e caratterizzazione |
| AMP-002 | Fender Frontman 65R | Studio precedente dell'utente e manuale ufficiale del produttore | Confronto con l'esemplare, schema della revisione e misure |
| AMP-003 | EKO basso da 30 W dichiarato; corrispondenza documentale XB30 | Manuale XL/XB fornito, OCR e pagine 1/10/11 verificate; speaker da manuale 10″ 8 Ω | Conferma fisica, diagnosi del suono distorto e possibile sostituzione con il supporto già disponibile |

Le schede sono [Marshall MG15](marshall-mg15.md), [Fender Frontman 65R](fender-frontman-65r.md) e [recupero EKO](eko-basso.md). L'inventario leggibile da programma è `data/strumenti-posseduti.json`. Il possesso è una dichiarazione del proprietario; caratteristiche dei manuali, condizioni reali e risultati misurati sono campi distinti.

## Integrazione nella catena

La prima finalità è usare quanto esiste per suonare, registrare e studiare i sistemi, riducendo gli acquisti quando le misure lo consentono. Le possibilità da valutare comprendono ripresa microfonica del combo, registrazione del preamplificatore dove esiste un'uscita documentata, riproduzione di una traccia attraverso l'amplificatore e confronto con il segnale diretto. Non sono percorsi già collegati o collaudati.

Ogni collegamento deve conservare la distinzione fra ingresso per strumento, ingresso di linea, uscita cuffie e uscita di potenza. Le misure del finale richiedono carico, attenuazione e strumentazione dimensionati; le uscite di potenza non sono ingressi diretti per una scheda audio. Per gli interventi interni e il cambio del trasduttore il riferimento operativo è il supporto indicato dall'utente.

## Percorso di reverse engineering

Si parte dall'identificazione dell'esemplare e della revisione, poi si acquisiscono manuale e schema corrispondenti. Si costruiscono il diagramma dei blocchi e la mappa dei punti di accesso. La prima caratterizzazione elettrica separa preamplificatore e finale dove i connettori lo consentono; la caratterizzazione acustica comprende altoparlante, cabinet, posizione e microfono. Ogni risposta misurata dichiara livello, controlli e carico. Solo dopo si confrontano il modello a piccoli segnali e il comportamento al variare del livello.

I modelli numerici, le simulazioni e gli strumenti di analisi si sviluppano dalla postazione nel repository; Ubuntu serve per la verifica della catena Linux e dei programmi. I rapporti tecnici restano pubblicabili, mentre esportazioni di chat, scansioni, percorsi personali, numeri di serie e recapiti rimangono nel livello privato. Il lavoro è tracciato da PA-038 e PA-039 e dalle rispettive voci della roadmap.
