---
generated-from-commit: 17a70affed584c1b7443d0f250e5cbd552b980f8
generated-from-branch: main
generated-date: 2026-09-04
covers-paths:
  - docs/**
  - tools/**
  - .claude/**
last-verified-commit: cf177180ef9f2a3ef325247dd07c973eb544d949
---

# Lavoro corrente

## Ripresa verificata del 2026-11-25

HEAD main 1e6e44b, un solo albero. Dopo l'impronta 3edf3de sono arrivati due commit di allineamento, senza cambiamenti al codice DSP o ai documenti di prodotto. Due modifiche preesistenti alle skill GRC del modello restano riservate alla chiusura dal template. Nessuna verifica runtime nuova: il risultato del pannello resta quello osservato in MS-317.

Sync-context: STACK, deployment e roadmap sono superate rispetto all'ancora 0d95d2e; current-work rispetto a cf17718. Verifica-schede non trova difetti strutturali; nessun bump generale delle firme. Rapporto vulnerabilità assente, sicurezza non verificata. Roadmap del 25 novembre con 26 voci aperte; prevale la sospensione delle verifiche fisiche in PENDING-ACTIONS.

Il proprietario chiede prima comandi di versionamento completi di cd, poi completamento dello sviluppo. Commit limitato ai tre file di memoria/contesto, con le due skill GRC escluse. Prossimo fronte: confronto reflex/direttività, CAD con distinta e livelli/protezioni nel perimetro teorico; piano software del controllo già concluso. Per il pannello resta enable manuale al login, senza reinstallazione. Gate dovuto ancora senza risposta: nessuna adozione o installazione, ADR-031 valida. Nessuna verifica fisica riattivata.

## Mandato e risultato

2026-11-23, MS-308 e successivi: controllo DSP software completato e report/simulazioni collegati nell'ingresso docs/STATO-PROGETTO.md. La specifica e le prove sono nel piano docs/piani/2026-11-23-controllo-ascolto.md e nel manuale 61, ADR-057. API reale canonica/asincrona, ALSA/clock, grafo PC qualificato e laboratorio isolato, pannello HTTP e watchdog implementati. Quarantasei metodi di test; banco motore reale 44,1/48 kHz a quattro canali e browser desktop/mobile verificati. Installazione e avvio manuali del pannello eseguiti dal proprietario, MS-317; 24 file e pagina/API/font verificati, zero riavvii. Avvio automatico al login ancora disabilitato alla prova. Nessun deploy automatico.

## Consegna e prossima azione

PDF correnti in docs/pdf, formule leggibili in LaTeX, figure SVG e modelli FCStd accessibili dall'indice. docs/PENDING-ACTIONS.md è il solo registro del residuo: qualifica hardware sospesa, futuri affinamenti teorici/CAD e decisioni di spesa separati dal controllo già sviluppato. Master didattico con otto approfondimenti; fonti curate e punti d'uso nel pedigree. Gate completo del nuovo blocco riuscito con codice 0 e 28 controlli locali verdi, MS-316; rapporto corrente privato. Resta il comando manuale enable per l'avvio al login; chiudi e versionamento sono manuali, senza nuova richiesta fisica.

## Limiti e vincoli

Nessuna misura acustica, dei jack, di ARM/USB o della DAW reale dedotta dal banco file. Le verifiche fisiche restano sospese per ADR-055 senza richieste all'utente. Non ripetere backup, installazioni o riavvio; il servizio DSP principale è rimasto Inactive/mute/-60 durante il test. Niente add/commit/push/deploy automatico; impronta di ripresa dopo i commit dell'utente. Template e sicurezza restano separati dal gate documentale. Snapshot canonico in memory/index; cronologia in progress/OPS, prove storiche e precedenti snapshot negli archivi privati.
