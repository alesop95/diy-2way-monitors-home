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

Realizzare due monitor attivi per home recording e ascolto autonomo a PC spento. Il target storico al punto d'ascolto è 60 Hz-20 kHz entro ±2 dB, ancora da dimostrare sui diffusori reali. Base teorica e compromessi in docs/63; stato di lettura in docs/STATO-PROGETTO.md. Dati macchina già collaudati, nessuna ripetizione del setup.

## Stato del percorso

MS-308 e successivi, 2026-11-23: completato il controllo API/ALSA/PipeWire e il pannello, 45 metodi di prova e banco motore reale file a 44,1/48 kHz; browser desktop/mobile verificato. Pannello installato e verificato in esercizio dal proprietario, MS-317; avvio automatico al login ancora da abilitare, qualifica hardware sospesa. Restano disponibili modello HP35/LT con 486 scenari, dodici casi nel motore e tre CAD esplorativi. Report e simulazioni sono collegati da STATO-PROGETTO; fonti e PDF hanno controlli di provenienza.

## Priorità e dipendenze

La lista operativa unica è docs/PENDING-ACTIONS.md, sezione pendenze correnti. I dati della vista generata sono tools/roadmap-items.yml e si leggono con python tools/roadmap.py. Il controllo quotidiano è sviluppato nel perimetro software definito; i successivi fronti autonomi sono evoluzione meccanica dei modelli, confronto dei limiti e distinta. Le operazioni fisiche sono sospese per ADR-055: gruppo 4 per otto voci interamente fisiche, sola parte teorica attiva nelle voci miste. Nessuna scadenza automatica o nuova richiesta di misure.

La costruzione e il collaudo finale dipendono da driver/componenti definitivi e riapertura volontaria delle verifiche fisiche. Il calcolo nominale non trasforma queste dipendenze in risultati acquisiti. Commit, propagazione delle lezioni e valutazione della storia Git sono attività manuali separate.
