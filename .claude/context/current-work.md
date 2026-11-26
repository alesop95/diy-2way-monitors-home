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

## Somma acustica su file sviluppata, MS-322, 2026-11-26

Base main ea70a7b, MS-321 chiusa dal proprietario. Sviluppati i tre task di docs/piani/2026-11-26-somma-acustica-su-file.md: calcolo SOS, somma complessa con fase, manifesto, diagnostici e pacchetto riproducibile. Riusati Curve e parser della caratterizzazione; nessun interprete generale CamillaDSP o acquisizione audio.

Ventidue test verdi. Griglie identiche, fase e riferimenti comuni obbligatori, stabilità digitale e Nyquist; banda/coerenza degli input controllate senza inventare coerenza risultante. Qualità insufficiente blocca dataset/FRD. Nei nulli fase vuota nel CSV e FRD a due colonne. Il caso rosso del file condiviso modificato fra le letture ora usa un solo snapshot per percorso normalizzato; due mutazioni rilevate e ripristini SHA verificati.

Tre casi analitici LR4 su242 frequenze: al taglio1, circa0 e sqrt(0,5). Soltanto l'allineato rispetta il bersaglio sintetico; tutti i pacchetti sono integri. Tre cartelle da8 file in build/somma-acustica-20261126 e rapporti durevoli nel vault. Dataset allineato passato realmente a caratterizzazione, simulated e hardware_qualified falso. Nessun driver SB o prototipo qualificato.

## Verifica e consegna

Al primo passaggio45 dei46 comandi locali sono verdi; gate fermato dalla firma storica di deployment. Scheda riletta contro prove conservate, ADR e runbook; unità locale coincidente con MS-317. Sola firma aggiornata a ea70a7b, senza nuova prova host; Test-Allineamento mirato ora senza invarianti rotti. Rapporto finale dopo questa persistenza: _notes/somma-acustica-20261126/chiudi-finale.txt, ultima riga da leggere prima di proporre chiudi.

Quattro PDF con QA, recap tutte le sette pagine viste e sette PNG rimossi con ricevuta. Archivi verificati dei25 artefatti prima della correzione e del precedente recap/manifesto. Fonti213/46 curate,139 file nel perimetro e375 usi; catalogo189, didattica12. Nessuna fonte nuova promossa. Kit nominale55 file e modelli108/27/18 precedenti invariati e coerenti.

## Prossimo gesto e vincoli

Versionamento manuale con COMMIT-MSG/COMMIT-SCOPE dopo gate finale verde, due GRC preesistenti esclusi. Nessuna impronta prima del commit/push del proprietario e nessun add/commit/push/deploy dall'agente. Un solo albero, zero agenti paralleli. Dopo la consegna non scrivere mentre chiudi viene eseguito.

PENDING è il solo registro del residuo:26 voci aperte. Fisiche sospese ADR-055; nessuna richiesta di foto, misure, acquisti o tagli. Enable del pannello al login manuale; niente reinstallazione, nuovo setup, backup/reboot o accesso a J. Gate pacchetti senza risposta, sicurezza non verificata. Le altre tre ancore storiche restano esplicite, nessun riallineamento completo dichiarato.
