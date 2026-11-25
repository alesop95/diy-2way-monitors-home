# Completamento teorico di reflex, direttività e cabinet

> Esecuzione inline con writing-plans ed executing-plans. Il proprietario ha chiesto di completare autonomamente lo sviluppo dopo il commit 7c7c864; non si ripete una richiesta di avvio già concessa. Nessun add, commit, push, acquisto o deploy automatico.

## Obiettivo e specifica

Completare gli strumenti e gli elaborati ancora mancanti in docs/63 e docs/70: confronto chiusa/reflex con ingombro e velocità nel condotto, direttività ideale con interferenza dei due driver, frontali parametrizzati sui disegni del produttore e distinta con rinforzo, analisi elettrica delle protezioni. I risultati sono di progetto nominale e non qualificano stanza, esemplari o crossover acustico.

## Architettura e scelte dell'esecutore

Riutilizzare dati e geometria esistenti, senza cambiare il controllo DSP già consegnato. Nuovi moduli Python separano fisica, geometria e produzione degli artefatti. NumPy è già disponibile; SciPy non lo è e non viene installato. Per il pistone si integra l'apertura circolare con quadratura deterministica; l'atteso della prova usa valori indipendenti di Bessel.

Il reflex usa il circuito acustico a parametri concentrati, con resistenza del condotto variabile. La geometria sottrae il volume del tubo dal volume utile e risolve insieme accordo e lunghezza. Il confronto non ignora un tubo che non entra o una velocità eccessiva. Correzione terminale, parete del tubo, occupazione interna e Q sono ipotesi esplicite, non dati misurati.

Il CAD conserva A24/SB16 come base e B27/SB15 come alternativa; C24 resta confronto di volume. Le quote di telai, forature e profondità vengono dai tre PDF SB Acoustics riletti e ispezionati il 25 novembre. Giochi e rinforzo sono scelte dell'esecutore modificabili, non istruzioni di taglio approvate. Le curve dei datasheet non vengono sostituite da una presunta misura di fase: il modello angolare rimane ideale.

## Vincoli globali

Verifiche fisiche sospese secondo ADR-055. Nessuna nuova dipendenza o installazione. I due file GRC preesistenti non si toccano. Le uscite nuove vanno in una cartella nuova; i rapporti versionati portano hash delle sorgenti e degli input. Le prove nominali non abilitano mappe hardware o livelli reali. Nessun prezzo aggiornato o potenza continua viene dedotto dai modelli.

Ruling: proseguire nel singolo albero main indicato dal proprietario dopo il suo commit; evitare operazioni Git e preservare i due file riservati al template. Rischio: la consegna richiede un perimetro esplicito al prossimo commit. Revisione in prima persona, come imposto dalla regola locale che vieta di delegare progettazione e revisione.

## Task 1: circuito reflex e direttività

File nuovi: tools/acustica_cabinet.py e tools/test_acustica_cabinet.py.

Interfacce: vented_box(frequency, fs, qts, vas_l, vb_l, fb_hz, port_q), port_geometry(volume_l, fb_hz, diameter_mm, wall_mm, end_factor), piston_directivity(argument), two_way_response(frequency, angle_deg, woofer_sd_cm2, tweeter_sd_cm2, spacing_mm, crossover_hz, offset_mm).

- [x] Scrivere e osservare rosse le prove: allineamento B4 a -3,0103 dB e forma 1/sqrt(1+r^-8), minimo del cono e contributo del condotto all'accordo, accordo/volume conservati, primo nullo del pistone, somma LR4 e cancellazione da cammino.
- [x] Implementare il circuito e le grandezze complesse senza divisioni singolari all'accordo; rifiutare dati non finiti o non fisici.
- [x] Verificare le prove e una mutazione del contributo del condotto; nessun effetto sul runtime audio.

## Task 2: geometria dei frontali e distinta

File nuovi: data/driver-geometria.json, config/cabinet/progetto-candidato.json, tools/progetto_cabinet.py, tools/test_progetto_cabinet.py.

Interfacce: analyse_variant(variant, drivers), con pannelli, cerchi di taglio e incasso, centri di montaggio, rinforzo, giochi, volume del legno e inviluppi conservativi dei driver.

- [x] Provare prima la sottrazione del volume dei fori/incassi, il contatto del rinforzo, il rigetto di fori che escono dal pannello e dei driver che interferiscono.
- [x] Implementare usando panel_specs esistente; distinguere montaggio nominale da appoggio reale, tolleranze e fissaggi da confermare.
- [x] Rileggere distinta e coordinate prodotte su A24, B27 e C24; nessuna distinta etichettata esecutiva.

## Task 3: livelli, condensatore e rapporto riproducibile

File nuovi: tools/studio_completamento.py e test pertinenti; rapporto in research-vault/completamento-20261125/.

- [x] Provare le conversioni dBu/Vrms e il polo RC, incluso segno della fase e variazione del crossover causata dal condensatore.
- [x] Calcolare i confronti reflex, gli scenari angolari e i livelli soltanto per guadagni ipotetici dichiarati; separare limiti resistivi, escursione e tenuta IEC.
- [x] Produrre JSON/CSV e figure scientifiche con font e colori Intrawelt; verificare gli input hash e il rifiuto di un rapporto alterato.

## Task 4: CAD e consegna documentale

File nuovi per CADCraft e FreeCAD, pagina di completamento collegata da docs/63 e STATO-PROGETTO; aggiornamenti a STACK, controlli-progetto, fonti, roadmap, memoria e ripresa.

- [x] Produrre DXF con CADCraft 0.20.1 e rileggere cerchi, raggi, coordinate e unità; convertire la tavola in PDF/SVG e ispezionarla.
- [x] Produrre assieme FreeCAD/STEP con il programma già presente, verificando volumi dei solidi e riapertura. Esecuzione soltanto in un ambiente di prova nuovo, senza modificare l'installazione ordinaria.
- [x] Integrare risultati, ipotesi e limiti nei documenti, senza dichiarare chiuse qualifiche sospese.
- [x] Eseguire suite pertinenti e controlli completi di chiusura; proporre una sola milestone verificata.

## Focus della revisione

La somma cono/condotto deve conservare la fase. Il volume occupato dal condotto non può sparire dal conto. Il pistone mantiene il segno oltre il primo nullo. I cerchi di fissaggio non diventano diametri di taglio. Il condensatore cambia fase e livello del ramo tweeter, quindi non può essere aggiunto dopo il calcolo del crossover senza rifarlo. Ogni caso ha una prova nel task che ne possiede il codice.

## Registro di esecuzione

Base 7c7c864. Commit/push del proprietario verificati; soltanto due modifiche GRC preesistenti prima dell'avvio. Nessun subagent avviato.

### Prove e scelte osservate

31 test e nove subtest superati nella suite nuova. Le prove rosse hanno preceduto le implementazioni; il contributo del condotto invertito e un raggio CAD alterato sono stati rilevati. Il report alterato, un STEP cambiato prima della firma e un file estratto cambiato dopo la consegna sono rifiutati. La data del rapporto non cambia per una rigenerazione identica. Gli SVG già presenti non bloccano un rebuild in una nuova cartella.

FreeCAD 1.1.4 ha prodotto tre assiemi da sette solidi: volumi analitici, assenza di intersezioni, variazione di larghezza e ripristino, riapertura del nativo e reimportazione STEP verificati. Le prime alias di Spreadsheet W/H/T erano rifiutate: una prova minima ha isolato il problema, risolto con prefisso Dim. Non si interpreta il solo codice del launcher come esito CAD. GUI isolata e viste ispezionate. CADCraft 0.20.1 ha riletto dodici profili chiusi per variante, con unità, aree, perimetri e centri verificati. I centri di fissaggio rimangono croci di costruzione, senza diametro pilota inventato.

Rapporto: 108 casi reflex, 27 scenari angolari, 18 elettrici e tre geometrie. A24 chiusa rimane base. Le tavole sono nominali, i modelli ideali. Kit locale da 52 file con manifesto, codice e dati; si rigenera dopo il QA finale dei PDF. Nessuna dipendenza installata, nessun runtime audio modificato. L'esecuzione dei test temporanei richiede permessi appropriati su Windows: la prima negazione della sandbox è conservata, senza chiamarla errore del modello.

Revisione in prima persona: confrontate equazioni, unità, quote ufficiali, artefatti riaperti e controlli negativi. Le ipotesi del condotto e della direttività non sono misure; una potenza resistiva richiesta sopra il limite ideale dei rail non è una potenza disponibile. Primo gate generale fermato dai correttori degli accenti, pur avendo superato tutti i 37 controlli locali. Corrette le forme nel sorgente e nel README del kit, rigenerati gli artefatti interessati e confermata identità delle sei immagini PDF rispetto al QA già letto. Secondo gate completo con «Controlli verdi». Quattro PDF correnti, 52 file del kit verificati, 34 PNG QA rimossi con ricevuta. Dopo la persistenza finale si ripete il gate prima di proporre chiudi; i due file GRC rimangono esclusi con COMMIT-SCOPE. Tutti i task autorizzati del piano sono sviluppati; qualifica fisica e lavorazione esecutiva restano sospese.
