# Snapshot di sincronizzazione

## Stato corrente, 2026-11-26

Base main19e56b3, chiusura MS-320 acquisita. MS-321 sviluppata e pronta per il versionamento manuale dopo l'ultima verifica: caratterizzazione su file FRD/OSM, esempio analitico, ricerca sulla via aperta e rettifica delle vecchie affermazioni ARTA/GLL. Ingresso docs/STATO-PROGETTO.md; procedura docs/65-caratterizzazione-aperta-e-dati-di-misura.md. Nessun programma installato, acquisto o acquisizione audio.

tools/caratterizzazione.py conserva gli input originali e confronta livello comune, banda, intervalli della griglia, coerenza e direzioni richieste. Fase assente distinta dallo zero, nessuna estrapolazione o normalizzazione per curva. Ventisei test verdi, inclusi manifesti errati, collegamento reale fuori dataset, alterazioni e CLI. I difetti dei grandi intervalli ai bordi e dei percorsi con punto sono stati riprodotti e corretti. La mutazione del riferimento comune è rilevata dalla prova; sorgente ripristinato con SHA identico.

Dataset sintetico versionato in data/caratterizzazione-demo: cinque curve da241 campioni, quattro entro±2dB e verticale+10 fuori, massimo3,29644dB. Rapporto durevole nel topic research-vault/caratterizzazione-aperta-20261126; pacchetto locale build/caratterizzazione-20261126 di17 file firmati più manifesto. Integrità, rispetto del bersaglio sui campioni e qualifica fisica sono esiti distinti. hardware_qualified resta falso anche per dati etichettati measured; nessun GLL generato.

Ricerca narrativa mirata su fonti primarie: coperture e query nel topic del vault, nessun nuovo paper letto integralmente. Gli export OSM1.5.2 sono stati esaminati nel sorgente identificato, senza prova runtime. PA-014 rimane aperta per scelta/qualifica della catena reale e authoring eventuale. Identità storica della fonte VituixCAD conservata: rigenerazione della mappa senza forzare la guardia strutturale. Mappa attuale213 fonti,46 curate e167 storiche,132 file nel perimetro e375 usi; catalogo184 file documentali/bibliografici. Undici approfondimenti didattici.

Primo chiudi in sola verifica concluso con «Controlli verdi»,41 comandi locali. Dopo questa persistenza leggere l'ultima riga di _notes/caratterizzazione-20261126/chiudi-finale.txt: proporre chiudi soltanto se verde. Quattro PDF correnti con QA valido; recap rigenerato e pagine1,4,5,6,7 viste. Rimossi soltanto i cinque PNG di QA con ricevuta. .gitattributes classifica i PDF come binari contro il driver globale astextplain; nessuna conversione dei file di testo. Diff verificato senza avvisi di spaziatura.

## Consegna già acquisita

MS-319:108 casi reflex,27 angolari,18 elettrici e tre geometrie nominali. A24 chiusa/SB16 base, SB15/B27 alternativa e C24 confronto. FreeCAD verificato con sette solidi per variante, riapertura e STEP; CADCraft dodici profili per variante. MS-320 ha reso espliciti i font e autonome le fixture del manifesto:42 test e nove subtest, inclusa ricostruzione reale senza vecchi build. Nessun font installato o pubblicato. Modelli e nativi non modificati da MS-321.

Quattro PDF, quattro SVG del completamento e figura del basso correnti. Kit nominale build/consegna-completamento-20261125.zip verificato:55 file e2.444.936 byte; manifesto nel vault/completamento-20261125. Nessun rebuild gratuito del kit in MS-321. Build è rigenerabile, non sostituisce i sorgenti. Archivi precedenti e ricevute di MS-319/320 preservati; non ripetere pulizie, backup o setup già conclusi.

## Residui e consegna manuale

PENDING-ACTIONS è il solo registro corrente:26 voci roadmap aperte, nessuna chiusa automaticamente. ADR-055 sospende senza scadenza misure, foto, collegamenti, ascolto, prototipo e lavorazioni fisiche. Le scelte esecutive/spesa, le letture autorizzate e le attività di template/altri progetti restano distinte dallo sviluppo concluso. Nessuna prestazione o potenza reale dedotta dalle fixture.

Pannello installato/verificato in MS-317; enable al login ancora manuale. Non riconfigurare runtime audio, rifare setup, banco DSP, backup o reboot. PA-042 manuale, sette lezioni del template aperte; ricevuta personale MS-307 conservata nella ripresa privata. Nessun contenuto aziendale importato, nessun accesso nuovo a J.

Gate pacchetti senza risposta: riferimento template99b13ff,107 voci mai viste e undici presenze non registrate. Nessuna adozione o installazione dedotta, ADR-031 valida. Rapporto vulnerabilità assente: sicurezza non verificata. Quattro ancore di contesto mantenute ai commit verificati: STACK/deployment/roadmap0d95d2e, current-work cf17718; struttura senza difetti, avvisi conservati.

Un solo albero e nessun agente parallelo. Due GRC preesistenti riservati al template, esclusi da COMMIT-SCOPE. Messaggio e perimetro esatto nel livello privato; proprietario esegue chiudi. Nessun add/commit/push/deploy o impronta di chiusura automatica. Dopo la consegna non scrivere mentre l'utente esegue la chiusura.
