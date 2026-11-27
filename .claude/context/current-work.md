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

## Schema delle quattro vie, MS-324

MS-324 pubblicata dal proprietario in 2992e12 il 27 novembre. Il lavoro del 26 sviluppa C-01 in docs/68-cablaggio-quattro-vie.md e nella revisione r2 di data/catena-riferimento.json. Schema L05-L08 e P05-P08 verificato contro la mappa nominale, con coppie di potenza indipendenti. V3 confermati in ADR-058. ADR-059 registra la sequenza proposta per qualificare la linea.

Prima variante: quattro cavi TRS-RCA con tip al centro, sleeve alla corona e ring aperto/isolato. Il manuale UMC1820 non autorizza un ponte ring-sleeve. Il resoconto su un esemplare favorevole al diretto rimane un indizio. Riserva: due ART DTI con quattro cavi TRS-TRS e quattro RCA-RCA, primari differenziali e secondari isolati. Le misure di carico, livello, fase e rumore restano differite.

Quattro linee ricontate con gli indici 4/5/6/7 e due gruppi LF/HF. Riferimento +16 dBu pari a 4,889919 V RMS; ampiezze ricavate sotto l'ipotesi dichiarata di riferimento a fondo scala. Due DTI a 77 euro IVA inclusa nella pagina aperta danno 154 euro. L'isolamento porta il budget a 1021,25-1241,25 euro prima di cavi extra e spedizione. DTI resta una variante condizionata, nessun acquisto o rilascio costruttivo autorizzato.

Mappa 219 fonti/55 curate/164 storiche, 145 file e 400 usi. Quattro fonti C-01 aggiunte con copertura esplicita. Una scheda curata resta non letta, la guida Dayton. Catalogo 198 file, didattica13. Recap aggiornato e ispezionato: pagine 1/4/5/6/7 cambiate e viste, 2/3 identiche per SHA alle pagine già verificate. Quattro PDF correnti e precedenti conservati; 14 PNG di confronto archiviati come impronte e rimossi. La prima lettura concorrente del controllo PDF ha visto un intermedio in rigenerazione. Dopo il termine del build il controllo è verde. Una successiva compilazione ha richiesto accesso alla cartella temporanea Windows, con approvazione del comando.

Esito di pubblicazione registrato nel diario il 2026-11-27, MS-325, dopo aver riprodotto il divario di data di lint-memoria. Per il commit di questa registrazione vale il rapporto _notes/cablaggio-20261126/chiudi-riallineamento.txt. Identità sui tracciati senza riscontri, sicurezza non verificata. Nessun add/commit/push/deploy dall'agente. Due GRC riservati al template esclusi. Un albero, zero agenti paralleli.

Prossima attività documentale: layout posteriore A24, scelta candidata del connettore a quattro poli e fissaggi/giunzioni a partire dagli ingombri dichiarati. PENDING-ACTIONS è il registro corrente. La roadmap mantiene 26 voci aperte, incluse 8 interamente fisiche sospese per ADR-055. Rumore, livelli, guadagni, protezioni, costruzione e taratura sono differiti. Enable del pannello al login manuale. Gate pacchetti senza risposta, sette lezioni aperte, PA-042 manuale. Ancore storiche dichiarate e deployment ea70a7b della sola rilettura precedente.
