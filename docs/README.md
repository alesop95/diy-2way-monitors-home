# Documentazione tecnica del progetto

> Livello documentale tracciato. Raccoglie in forma navigabile il contenuto del documento sorgente `full_electroacoustics.docx`, che resta locale e ignorato da git come sola fonte di rigenerazione. Ogni pagina si legge da sola; l'ordine dei numeri è l'ordine del workflow, non un vincolo di lettura.

## Come è organizzata

Per capire dove siamo aprire prima [STATO-PROGETTO.md](STATO-PROGETTO.md), oppure il suo [PDF di riepilogo](pdf/recap-progetto.pdf). Riunisce stato della macchina e del progetto, scelte candidate, risultati, documenti disponibili e percorso di lettura. Le verifiche fisiche sono sospese su richiesta dell'utente; il lavoro teorico/software continua e non richiede adesso foto, misure o prove sull'hardware.

La documentazione segue la struttura del progetto reale invece della struttura del documento sorgente. Il workflow complessivo sta in una pagina sola, perché il suo valore è vedere le otto fasi insieme; l'ambiente Linux ha una cartella propria, perché è la parte che serve anche al progetto gemello di home recording e viene mantenuta in due copie sincronizzate; ogni fase del workflow ha poi la sua pagina, con gli strumenti che le appartengono.

## Indice

Relazioni con formule leggibili, aggiornamento 2026-11-20: [crossover in PDF LaTeX](pdf/crossover-pc-pi-analogico.pdf), [sistema PC e autonomo, componenti e collaudo in PDF](pdf/sistema-autonomo-driver-e-collaudo.pdf). Il [progetto 63](63-sistema-autonomo-driver-e-collaudo.md) recepisce l'ascolto senza PC come requisito obbligatorio e sviluppa driver, finali, interfaccia e profili; [sorgenti e compilazione](latex/README.md) rendono ripetibili gli impaginati.

L'ingresso unico è [STATO-PROGETTO.md](STATO-PROGETTO.md), con fonti di verità e documenti da aprire. Il [catalogo con percorsi esatti](90-riferimenti/catalogo-documentazione.md) è l'elenco generato, non un altro stato del progetto; il [pedigree delle fonti](90-riferimenti/fonti-progetto.md) esplicita identità, letture e punti d'uso. L'indice ragionato è ritirato e rimanda all'ingresso unico. Per il DSP valgono il [manuale tecnico](61-camilladsp-manuale-tecnico.md) e il [confronto ingegneristico](62-confronto-crossover-e-verifica-matematica.md).

Gli amplificatori già posseduti, il loro studio circuitale e l'integrazione nell'home recording sono raccolti in [strumenti posseduti](80-strumenti-posseduti/README.md): Marshall MG15, Fender Frontman 65R e recupero dell'amplificatore EKO per basso. Il fronte è aggiunto il 2026-11-18 e comprende inventario, caratterizzazione e interventi, con dati dichiarati e misurati distinti.

Il workflow in otto fasi, dalla misura della stanza alla verifica finale, sta in [00-workflow.md](00-workflow.md).

L'ambiente Linux, cioè Ubuntu Studio e Wine con tutto ciò che serve a far girare i programmi Windows di progettazione, sta nella cartella [10-ambiente/](10-ambiente/README.md). Dentro quel blocco, il documento da cui partire è la [fotografia della macchina al 2026-09-07](10-ambiente/fotografia-macchina-2026-09-07.md), che è l'unico costruito su dati letti dalla macchina reale, e il suo termine di confronto è la [fotografia finale al 2026-09-21](10-ambiente/fotografia-macchina-post-reinstall.md), che chiude la procedura di reinstallazione dichiarando che cosa è cambiato, che cosa no e perché.

Le fasi operative sono documentate una per pagina: [misura reale della stanza](20-misura-stanza.md), [modellazione e simulazione acustica](30-modellazione-e-simulazione.md), [analisi dei dati in Octave](40-analisi-octave.md), [progettazione del monitor](50-progettazione-monitor.md), con il [confronto fra crossover passivo e attivo](52-crossover-passivo-o-attivo.md), [simulazione finale in Akabak](60-simulazione-finale-akabak.md) e [realizzazione con verifica finale](70-realizzazione-e-verifica.md).

Il rilievo geometrico della stanza, cioè quali quote si prendono, in quale ordine e su quali tabelle si scrivono, sta in [35-rilievo-geometrico.md](35-rilievo-geometrico.md). È un allegato operativo alla fase 2 e i suoi campi sono ricavati dall'unione di ciò che le fasi 1, 2 e 3 pretendono, perché il rilievo si fa una volta sola: è il posto dove vive anche il verbale, dato che le tabelle si riempiono lì. Il fronte è PA-020.

La catena di riproduzione, cioè che cosa sta fra il computer e i monitor e come questo vincola l'architettura del diffusore, sta in [75-catena-di-riproduzione.md](75-catena-di-riproduzione.md). Il confronto dei moduli di amplificazione e dei processori digitali per i cabinet attivi, con la configurazione da Linux e la distinta di una soluzione aperta, sta in [54-amplificazione-e-dsp.md](54-amplificazione-e-dsp.md).

I riferimenti stanno nella cartella [90-riferimenti/](90-riferimenti/README.md), e comprendono l'inventario del software disponibile, lo stato delle licenze, lo storico verificato di Akabak e VACS, le cinque incoerenze del documento sorgente spiegate una per una, la prova di copertura della conversione e le fonti citate.

Il registro cronologico dei microstep operativi, con l'esito verificato di ciascuno, sta in [OPERATIONS-LOG.md](OPERATIONS-LOG.md). A che cosa serva ciascun blocco di quel registro, cioè a quale fase del progetto dei monitor, lo dice [tracciabilita-microstep.md](90-riferimenti/tracciabilita-microstep.md), che esiste perché il registro racconta il come e non il perché di progetto.

L'elenco dei materiali pesanti da spostare sulla macchina di lavoro, con destinazioni e impronte di verifica, sta in [TRANSFER-MANIFEST.md](TRANSFER-MANIFEST.md).

Le azioni che non si possono compiere adesso, con la condizione che sblocca ciascuna e il criterio con cui si stabilisce che sono compiute, stanno in [PENDING-ACTIONS.md](PENDING-ACTIONS.md). Conviene leggerlo a inizio sessione, o meglio lanciare `python tools/check-pending-actions.py`, che ne verifica le condizioni automatizzabili.

## Rapporto con il documento sorgente

Il `.docx` di partenza conteneva 507 paragrafi, quattro tabelle e una immagine, per circa diecimila parole, e mescolava in un unico flusso la teoria del workflow, la cronaca dell'installazione della macchina, le schede dei singoli programmi e appunti ancora in forma di segnaposto. La conversione ha separato questi piani, ha promosso a prosa le sequenze che nel sorgente erano elenchi, e ha scartato soltanto i paragrafi segnaposto privi di contenuto, cioè le sequenze di lettere ripetute che l'autore aveva lasciato come promemoria di sezioni da scrivere. Le sezioni che nel sorgente erano marcate come da verificare restano marcate come tali qui, e non sono state promosse a fatto.

Proposta di sistema del 2026-11-17: [monitor, cabinet MDF, catena condivisa e spesa](55-proposta-sistema-home-recording.md), da rivedere prima della simulazione e del taglio.

Verifica del motore DSP prima dell'hardware: [collaudo offline su Windows e Ubuntu](56-collaudo-dsp-offline.md).

Il [DSP persistente](57-dsp-persistente.md) e il [piano eseguito](58-piano-dsp-persistente.md) collegano il collaudo offline al servizio utente e al banco PipeWire. La [procedura Ubuntu](10-ambiente/camilladsp-servizio-utente.md) conserva i comandi e i limiti della verifica virtuale.

Il [completamento del progetto nominale](64-reflex-direttivita-e-cabinet-nominale.md), sviluppato il 25 novembre, aggiunge confronto reflex, direttività ideale, livelli e protezioni, frontali con incassi e rinforzo. Collega il nuovo PDF e il kit FCStd/STEP/DXF verificato; qualifica fisica e rilascio costruttivo restano distinti.

La [caratterizzazione aperta su file](65-caratterizzazione-aperta-e-dati-di-misura.md) aggiunge importazione, confronto e integrità dei dati FRD/OSM, con esempio sintetico riproducibile. Separa i dati di misura dall’eventuale authoring GLL, senza riaprire le prove fisiche.

La [somma complessa dei driver](66-somma-acustica-e-crossover-su-file.md) collega le curve importate a filtro, livello, polarità e ritardo, con esempi LR4 e dataset riutilizzabile nel confronto su file.

La [catena di riferimento consolidata](67-catena-di-riferimento-e-dipendenze-esecutive.md) raccoglie distinta, canali, collegamenti e budget del26 novembre. I V3 sono confermati per priorità al costo. Lo [schema delle quattro vie](68-cablaggio-quattro-vie.md) definisce collegamento diretto e variante isolata, con qualifica differita. Il [retro A24](69-retro-a24-e-passaggio-cavi.md) aggiunge piastra e tavola quotata. Il [confronto sullo ST-120](69a-discesa-cavi-st120.md) determina le luci per discesa e sgancio.
