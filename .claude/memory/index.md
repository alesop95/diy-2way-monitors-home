# Snapshot di sincronizzazione

## Stato corrente, 2026-11-26

Base main ea70a7b, chiusura MS-321 acquisita. MS-322 sviluppata: somma complessa delle risposte dei due driver dopo coefficienti SOS, guadagno, polarità e ritardo espliciti. Procedura docs/66-somma-acustica-e-crossover-su-file.md; ingresso del proprietario docs/STATO-PROGETTO.md. Nessuna acquisizione, installazione, licenza o modifica del servizio audio.

tools/somma_acustica.py riusa Curve e parsing di caratterizzazione. Griglie identiche, fase obbligatoria, riferimenti comuni di livello/tempo/osservazione e risposte senza crossover da dichiarare. Filtri digitali stabili e frequenze sotto Nyquist. Coerenza della somma non inventata; qualità insufficiente degli input blocca dataset/FRD, preservando diagnostici e originali. Nei nulli fase vuota nel CSV e FRD a due colonne, soglia e pavimento dichiarati. Ogni percorso normalizzato è letto una sola volta: risolto il difetto riprodotto del file condiviso che cambia fra due letture.

Ventidue test verdi, inclusa trasformazione bilineare LR4 e passaggio reale al modulo di caratterizzazione. Due mutazioni rilevate: somma dei moduli e doppia lettura; ripristino SHA verificato per ciascuna base. Data/somma-acustica-demo contiene242 frequenze e tre manifesti. Moduli al taglio1, circa0 e sqrt(0,5): allineato within_bounds, invertito/ritardato outside_bounds. Tre pacchetti locali da8 file in build/somma-acustica-20261126; rapporti durevoli nel vault. Il risultato resta simulated, hardware_qualified falso anche con input dichiarati measured.

Al primo gate sono passati45 dei46 comandi locali. La chiusura si è fermata su Test-Allineamento per l'ancora di deployment anteriore al contenuto3ce3c93. Scheda riletta per intero contro ADR, ricevuta MS-317, unità locale coincidente e runbook: aggiornata soltanto la firma a ea70a7b; nessuna nuova verifica host. Controllo mirato ora senza invarianti rotti, avviso di freschezza conservato. Dopo questa persistenza leggere l'ultima riga di _notes/somma-acustica-20261126/chiudi-finale.txt: proporre chiudi soltanto se termina «Controlli verdi».

Quattro PDF correnti con QA. Recap rigenerato con Craft e tutte le sette pagine viste; sette PNG QA rimossi con ricevuta. Prima dell'aggiornamento delle impronte sono stati archiviati e riletti25 artefatti della somma; risultati numerici e input invariati. Recap/manifesto precedenti conservati. Nessun nuovo paper o sito letto: fonti213,46 curate,167 storiche;139 file nel perimetro e375 usi. Catalogo189 file documentali/bibliografici, didattica12. Mappa e catalogo rigenerati con archivio e guardia strutturale.

## Consegne già acquisite

MS-319:108 casi reflex,27 angolari,18 elettrici e tre geometrie nominali. A24 chiusa/SB16 base, SB15/B27 alternativa, C24 confronto. FreeCAD con sette solidi per variante e formati riaperti; CADCraft dodici profili. MS-320: ricostruzione reale senza vecchi build, risorse esplicite e fixture autonome,42 test e nove subtest. Nessun font installato/pubblicato. Kit nominale55 file/2.444.936 byte ancora coerente, nessuna rigenerazione in MS-322.

MS-321: importatore FRD/OSM e confronto su file,26 test, cinque curve sintetiche e un caso fuori bersaglio rilevato. Ricerca primaria e correzioni ARTA/GLL nel capitolo65. I dati aperti non richiedono un GLL; PA-014 resta aperta per scelta/qualifica reale e authoring eventuale. Nessuna proprietà fisica dedotta dagli esempi analitici.

## Residui e consegna manuale

PENDING-ACTIONS è il solo registro corrente; roadmap26 voci aperte. ADR-055 sospende senza scadenza misure, foto, ascolto, collegamenti, prototipo e lavorazioni. Restano scelte esecutive/spesa, letture autorizzate e attività di template/altri progetti. Non richiedere acquisti o riscontri fisici adesso.

Pannello installato/verificato in MS-317; enable al login manuale. Non riconfigurare runtime audio o ripetere setup, banco DSP, backup/reboot. PA-042 manuale, sette lezioni del template aperte; ricevuta personale MS-307 nella ripresa privata. Nessun accesso nuovo a J o contenuto aziendale importato.

Gate pacchetti senza risposta: riferimento template99b13ff,107 voci mai viste e undici presenze non registrate, nessuna adozione/installazione dedotta. Sicurezza senza rapporto qualificante, non verificata. Ancore STACK/roadmap0d95d2e e current-work cf17718 ancora storiche, nessun riallineamento completo dichiarato; deployment firmata dopo la sola rilettura documentale. Un solo albero, zero agenti paralleli.

COMMIT-MSG e perimetro nel livello privato; due GRC preesistenti riservati al template esclusi. Nessun add/commit/push/deploy o impronta automatica. Proprietario esegue chiudi soltanto con gate finale verde. Dopo la consegna non scrivere mentre lo esegue.
