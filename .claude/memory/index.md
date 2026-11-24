# Snapshot di sincronizzazione

## Stato corrente, 2026-11-23

Mandato: completare il controllo DSP e rendere consultabili tutti i report dettagliati e le simulazioni. Piano docs/piani/2026-11-23-controllo-ascolto.md, decisione ADR-057, cronologia MS-308/317. Sviluppo software completato: API WebSocket reale, configurazione canonica/asincrona, observer ALSA/clock, grafo PC PipeWire attestato, guardia del laboratorio e pannello Mix/Ascolto con volume/mute e watchdog. Quarantasei metodi di test nel perimetro del controllo; motore Ubuntu reale a 44,1/48 kHz e quattro PCM, UI desktop/mobile verificata. Pannello installato e avviato manualmente dal proprietario, verificato via SSH in sola lettura in MS-317: 24 file integri, HTTP 200 e zero riavvii. Avvio automatico ancora disabled alla prova; nessun deploy automatico eseguito. Report e hash in research-vault/sistema-autonomo-20261120/risultati-controllo.json. Gate completo del nuovo blocco riuscito con codice 0 e 28 controlli locali verdi, MS-316.

## Autorità e consegne

Ingresso del proprietario docs/STATO-PROGETTO.md, tecnica docs/63, uso DSP docs/61, residui docs/PENDING-ACTIONS.md. OPS conserva microstep, ADR decisioni, master didattico otto approfondimenti, pedigree 203 risorse con 36 schede curate. Catalogo 169 file documentali/bibliografici; nessuna lettura integrale della biblioteca dichiarata. PDF correnti docs/pdf: recap sette pagine, crossover sei e sistema nove, con sorgenti, QA e impronte nel manifesto. Figure SVG direttamente apribili; kit CAD HTML e FCStd esplorativi. Il pannello è installato su Ubuntu; rapporto risultati-installazione-controllo.json nel vault. Le due modifiche documentali successive nel kit locale non cambiano il runtime installato.

Base teorica invariata: PC per DAW e Pi per ascolto a PC spento, interfaccia candidata UMC1820 alternativa fra host, due V3 stereo e SB16/SB26 in A24; SB15/B27 alternativa. HP35/LT, 486 scenari e dodici casi reali su file già documentati. Marshall, Fender ed EKO 30 W documentati; speaker EKO non diagnosticato. Nessun acquisto, taglio o risposta acustica approvati implicitamente dal software.

## Vincoli e conservazione

ADR-055: verifiche fisiche sospese senza scadenza; non chiedere foto, misure, targhette, ascolto, collegamenti o tecnico. Il residuo reale è nel solo PENDING-ACTIONS; non ripetere setup, reboot o backup già collaudati. Nessun contenuto aziendale importato. PA-042 storia Git resta manuale; sette lezioni per il template ancora aperte. Consegna autorizzata a progetto personale distinto conclusa in MS-307, ricevuta soltanto nella ripresa privata.

Pulizia precedente preservata: 335 derivati rimossi, 1011 prove nel ZIP delle sessioni e circa 433 MiB recuperati, più archivio precedente di 340 prove. Ricevuta _notes/archivio-prove/riordino-corrente.json; originali e biblioteca intatti. Nuovi PCM/FIFO e profili browser temporanei eliminati, due PNG UI e cinque pagine PDF QA ispezionati e rimossi. Snapshot prima del consolidamento nel nuovo ZIP privato controllo-ascolto-20261123. Nessuna cartella PNG per ogni pagina.

## Versionamento e verifica

Branch main, base 0fc4e99, modifiche non committate. tools/controlli-progetto.txt contiene 28 comandi locali. Esito generale corrente nel rapporto _notes/chiudi-autonomia-20261120.txt: codice 0, senza commit. Non anticipare registrazione della ripresa o versionamento. Template avanti di dieci commit all'apertura e due consegne da chiudere a monte; rapporto vulnerabilità assente. Nessun add/commit/push/deploy automatico. Il messaggio proposto è in _notes/COMMIT-MSG.txt, la chiusura la esegue l'utente.

Le ancore last-verified delle schede restano ai commit effettivamente verificati: STACK/deployment/roadmap 0d95d2e e current-work cf17718. Le schede sono aggiornate nel working tree, senza fingere un nuovo commit. La superficie locale HTTP/WebSocket e i limiti sono descritti nel manuale 61 e nel piano ADR-057; le prove in STACK. Non si mantiene la vecchia affermazione di assenza di runtime applicativo.
