---
generated-from-commit: 17a70affed584c1b7443d0f250e5cbd552b980f8
generated-from-branch: main
generated-date: 2026-09-04
covers-paths:
  - docs/**
last-verified-commit: 0d95d2efec703c8605e398eca9de6403b941f441
---

# Roadmap

## Direzione corrente

Realizzare due monitor attivi per home recording e ascolto autonomo a PC spento. Il target storico al punto di ascolto è 60 Hz-20 kHz entro ±2 dB, ancora da dimostrare sugli esemplari. Architettura in docs/63, nominale in docs/64, controllo dei dati in docs/65; ingresso del proprietario docs/STATO-PROGETTO.md.

## Stato del percorso

Controllo API/ALSA/PipeWire e pannello sviluppati e collaudati su file; installazione verificata in MS-317, enable al login manuale. Modelli HP35/LT, reflex/direttività e cabinet con frontali/rinforzo consegnati in MS-319. Ricostruzione da sorgenti e risorse esplicite verificata in MS-320, commit19e56b3. Nessuna qualifica fisica dedotta e nessuna ripetizione del setup richiesta.

MS-321 sviluppa il confronto dei dati su file: FRD/OSM, riferimento comune, copertura/griglia/coerenza/direzioni e integrità. Ventisei prove, esempio sintetico con quattro curve entro i limiti e una fuori. La ricerca distingue export della misura, authoring GLL e autorizzazione Focus. Nessuna installazione o acquisizione nuova; PA-014 resta aperta per la scelta e qualifica della catena reale e l’eventuale authoring.

## Priorità e dipendenze

PENDING-ACTIONS è il solo registro corrente e roadmap-items.yml fornisce i dati della vista generata. I blocchi software sviluppati non vanno riaperti come lavoro mancante a ogni ripresa. Restano scelte esecutive e di spesa, fonti e attività nei progetti competenti. Le otto voci interamente fisiche sono sospese per ADR-055; nessuna scadenza o richiesta automatica di misure.

Costruzione e collaudo dipendono dai componenti definitivi e dalla riapertura volontaria delle verifiche. La pipeline distingue coerenza del calcolo e rispetto del bersaglio sui campioni, e mantiene hardware_qualified falso. Commit, propagazione al template e valutazione della storia Git restano gesti manuali.
