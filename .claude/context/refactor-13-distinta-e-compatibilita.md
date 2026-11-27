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

## Dal nome del connettore al percorso di corrente, MS-324

Per ogni uscita i tre contatti del jack descrivono la geometria. La parola *bilanciata* descrive le impedenze viste dai due conduttori. Per conoscere la tensione sul solo tip occorre ancora sapere come il circuito genera il segnale. Se due poli uguali sono in opposizione di fase, la tensione fra poli è doppia rispetto al solo tip e la perdita ideale del diretto è 6 dB. Se su un polo c'è solo l'impedenza di bilanciamento, quel rapporto non segue dalla forma della presa.

Il capitolo68 usa questa distinzione per ordinare le prove. Il diretto isola il ring e usa lo sleeve come ritorno. Si conserva il vantaggio di costo soltanto se tensione caricata, risposta e rumore sono adatti. L'isolatore legge tip-ring e offre sul secondario un riferimento per RCA. Il suo rapporto 1:1 lascia aperta la questione del guadagno. Sul ramo woofer vanno controllati anche livello e risposta alle frequenze basse, dove un trasformatore può introdurre perdita o distorsione. Una misura differenziale a monte e un confronto a livello equalizzato a valle mostrano due effetti diversi.

La modalità nel JSON aggiunge `line_label`, `power_label` e `isolator_channel` senza ripetere la mappa di routing. L05 e L07 entrano nel V3 woofer, L06 e L08 nel V3 tweeter. Gli stessi identificativi legano le linee alle coppie P05-P08 in entrambe le varianti. Il confronto della tabella con questi campi ha verificato gli estremi di tutte e quattro le vie. La compatibilità elettrica mantiene il proprio esito sospeso fino al banco. Il tema prosegue qui perché sviluppa la stessa distinzione fra distinta e qualifica della scheda 13.

## La vista della presa e lo spazio della spina, MS-326

Un cerchio centrale e due fori con interassi giusti non determinano il verso di montaggio. Il disegno Neutrik mostra il ritaglio dal lato morsetti. La tavola dell'A24 guarda il lato spina, quindi i centri si specchiano. Il confronto sui centri distingue due disegni con area e diametro identici. La prova volutamente specchiata esercita proprio questa differenza.

La stima della profondità del solo cabinet aveva tre dimensioni dichiarate e un angolo. Il punto terminale della spina richiede un'altra quota a partire dalla faccia della piastra. Con la riserva di 110 mm il risultato supera i 300 mm dello ST-120, se tutto deve restare entro il ripiano. Le foto mostrano il contesto, mentre la formula usa le quote pubbliche. La distanza dalla parete rimane aperta e può consentire una discesa del cavo oltre il bordo. È questa distinzione a evitare che il disegno del pannello sembri già un rilascio costruttivo.
