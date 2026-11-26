# 13. Una distinta non è ancora una catena compatibile

## Com'era e perché restava aperto

Il capitolo63 aveva già una base concreta e un budget datato: UMC1820, due V3 e driver SB16/SB26 in A24. Simulazioni e CAD nominale erano sviluppati. Restavano però mescolati il modello scelto per lo studio, il collegamento ancora da qualificare e il prezzo finale di un acquisto. Ripetere il nome del componente in un'altra pagina non avrebbe chiuso queste dipendenze.

Un esempio è il percorso cuffie. I due V3 richiedono quattro segnali separati e le cuffie uno stereo a banda intera. Scrivere soltanto “interfaccia con molte uscite” non esplicita quali canali appartengano al crossover. Nel dato consolidato, nominal_channels distingue3/4 cuffie e5/6/7/8 verso LF-L,HF-L,LF-R,HF-R; ogni riga mantiene qualified=false. Le mappe software già esistenti usano gli indici4/5/6/7 e restano non abilitanti.

## La scelta e il costo che non scompare

Il proprietario mantiene i V3 per priorità al costo dopo il confronto con A800. ADR-058 registra questa scelta nel suo perimetro: una base di sviluppo, non una spesa o una prova dell'hardware. Il collegamento fra linea bilanciata e RCA rimane C-01, anche dopo la conferma. Spostare il problema in un cavo senza averne stabilito terminazioni, livello e rumore avrebbe reso la distinta apparentemente finita.

data/catena-riferimento.json separa quantità, prezzi visualizzati, IVA/stock e lotti stimati. Il microfono ora è una riga autonoma: cavo e asta sono un'altra, così non si conta due volte il lotto di misura precedente. Aritmetica decimale: subtotale587,25 euro, budget V3 senza switch867,25-1087,25; l'alternativa A800 aggiunge 160 euro. Spedizioni e differenze IVA non sono prezzi ricavati dalla somma.

## Che cosa è stato verificato

Il controllo documentale confronta quantità e mappa con i JSON canonici, conserva i due example verified=false e controlla A24/SB16/SB26. Le fonti commerciali provano la propria offerta, quelle dei produttori il contratto nominale. Il PDF Dayton con nome plausibile ha invece restituito1157 byte HTML di verifica con HTTP200: non viene chiamato letto. Il portale ufficiale di calibrazione è un'altra fonte e non prova il download di un seriale.

Nessun nuovo test automatico pretende di misurare questi componenti. Le prove software precedenti mantengono il proprio perimetro. La firma di un file, un numero di uscite o un totale di budget non dimostrano rumore, appoggio meccanico o potenza reale.

## Il risultato utile

Il capitolo67 e il dato della catena sostituiscono l'elenco generico con quantità e dipendenze: quattro linee, quattro coppie di potenza indipendenti, sedici centri nominali di montaggio e componenti non duplicati fra modalità. Le viti non vengono ordinate dal solo conteggio dei centri; il retro non viene fresato senza il connettore effettivo. La prossima lavorazione ha un ingresso preciso, C-01 e layout, mentre le qualifiche fisiche restano sospese.
