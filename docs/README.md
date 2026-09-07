# Documentazione tecnica del progetto

> Livello documentale tracciato. Raccoglie in forma navigabile il contenuto del documento sorgente `full_electroacoustics.docx`, che resta locale e ignorato da git come sola fonte di rigenerazione. Ogni pagina si legge da sola; l'ordine dei numeri è l'ordine del workflow, non un vincolo di lettura.

## Come è organizzata

La documentazione segue la struttura del progetto reale invece della struttura del documento sorgente. Il workflow complessivo sta in una pagina sola, perché il suo valore è vedere le otto fasi insieme; l'ambiente Linux ha una cartella propria, perché è la parte che serve anche al progetto gemello di home recording e viene mantenuta in due copie sincronizzate; ogni fase del workflow ha poi la sua pagina, con gli strumenti che le appartengono.

## Indice

Il workflow in otto fasi, dalla misura della stanza alla verifica finale, sta in [00-workflow.md](00-workflow.md).

L'ambiente Linux, cioè Ubuntu Studio e Wine con tutto ciò che serve a far girare i programmi Windows di progettazione, sta nella cartella [10-ambiente/](10-ambiente/README.md). Dentro quel blocco, il documento da cui partire è la [fotografia della macchina al 2026-09-07](10-ambiente/fotografia-macchina-2026-09-07.md), che è l'unico costruito su dati letti dalla macchina reale.

Le fasi operative sono documentate una per pagina: [misura reale della stanza](20-misura-stanza.md), [modellazione e simulazione acustica](30-modellazione-e-simulazione.md), [analisi dei dati in Octave](40-analisi-octave.md), [progettazione del monitor](50-progettazione-monitor.md), [simulazione finale in Akabak](60-simulazione-finale-akabak.md) e [realizzazione con verifica finale](70-realizzazione-e-verifica.md).

La catena di riproduzione, cioè che cosa sta fra il computer e i monitor e come questo vincola l'architettura del diffusore, sta in [75-catena-di-riproduzione.md](75-catena-di-riproduzione.md).

I riferimenti stanno nella cartella [90-riferimenti/](90-riferimenti/README.md), e comprendono l'inventario del software disponibile, lo stato delle licenze, lo storico verificato di Akabak e VACS, le cinque incoerenze del documento sorgente spiegate una per una, la prova di copertura della conversione e le fonti citate.

Il registro cronologico dei microstep operativi, con l'esito verificato di ciascuno, sta in [OPERATIONS-LOG.md](OPERATIONS-LOG.md).

L'elenco dei materiali pesanti da spostare sulla macchina di lavoro, con destinazioni e impronte di verifica, sta in [TRANSFER-MANIFEST.md](TRANSFER-MANIFEST.md).

Le azioni che non si possono compiere adesso, con la condizione che sblocca ciascuna e il criterio con cui si stabilisce che sono compiute, stanno in [PENDING-ACTIONS.md](PENDING-ACTIONS.md). Conviene leggerlo a inizio sessione, o meglio lanciare `python tools/check-pending-actions.py`, che ne verifica le condizioni automatizzabili.

## Rapporto con il documento sorgente

Il `.docx` di partenza conteneva 507 paragrafi, quattro tabelle e una immagine, per circa diecimila parole, e mescolava in un unico flusso la teoria del workflow, la cronaca dell'installazione della macchina, le schede dei singoli programmi e appunti ancora in forma di segnaposto. La conversione ha separato questi piani, ha promosso a prosa le sequenze che nel sorgente erano elenchi, e ha scartato soltanto i paragrafi segnaposto privi di contenuto, cioè le sequenze di lettere ripetute che l'autore aveva lasciato come promemoria di sezioni da scrivere. Le sezioni che nel sorgente erano marcate come da verificare restano marcate come tali qui, e non sono state promosse a fatto.
