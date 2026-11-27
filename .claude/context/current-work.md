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

## Montaggio e collaudo, MS-328

MS-327 pubblicata in 124a454. MS-328 consolida la preparazione documentale dal preventivo alla taratura. Capitolo70, procedura con sei passi e criteri di avanzamento. Capitolo70a, scheda vuota per montaggio, cablaggio, banco, acquisizione e accettazione. Riscontri per esemplare e profili solo dopo riapertura delle verifiche. Il workflow storico rimane sotto, con marcatura esplicita.

Quattro vie confrontate con la distinta r4 e i contatti NL4MPXX. Prima continuità senza alimentazione, poi misura con carichi fittizi fra i poli, ingresso differenziale adeguato a tensione e commutazione. Limiti di banco e operativi distinti. Qualifica C-01, mappa PC/Pi, protezioni e arresto espliciti. La scheda di misura conserva eccitazione, origine comune, riferimenti, banda, fase e filtri presenti. Il dato di fase mancante non è zero. La misura già filtrata non può ricevere lo stesso crossover nella predizione. Nota TI e due pagine REW registrate con copertura. Il caso sintetico allineato rientra, quello a polarità invertita risulta fuori bersaglio a file integri. Riutilizzati i tre controlli su file con rapporto d'impronte, hardware_qualified sempre falso.

Fonti 230/66 curate/164 storiche, 154 file e 414 usi. Catalogo 207 e didattica13. Guida Dayton ancora non letta. Il taglio del contesto nella mappa lasciava uno spazio finale. Accorciata la frase dell'export nel sorgente, mappa rigenerata e diff pulito. Recap aggiornato con WordCraft/PdfCraft, pagine 1/7 viste e le altre cinque identiche per SHA. Quattordici render temporanei rimossi con impronte conservate. Nessun nuovo modulo, test, hardware, accesso a host o a foto. Il rapporto dopo la persistenza si legge in _notes/montaggio-collaudo-20261127/chiudi-finale.txt prima della proposta manuale.

La sequenza rende disponibili le verifiche future in ordine. Il prossimo passo pratico dipende dalla riapertura della fase A con spazio reale e revisione della tavola. Restano A24, V3, vincolo PC/Pi e soglie di discesa; scelta esecutiva, ordini, montaggio e taratura restano differiti ADR-055. Nessuna nuova richiesta fisica. Enable pannello al login e PA-042 manuali, gate pacchetti senza risposta, sette lezioni aperte, sicurezza non verificata. Due GRC riservati esclusi, zero subagenti e una sola radice di lavoro.
