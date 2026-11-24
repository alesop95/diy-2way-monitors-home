# Review tecnica del crossover e della piattaforma

## Abstract

Questa review narrativa del 20 novembre 2026 combina documentazione primaria, una review AES e calcoli originali riproducibili. Confronta CamillaDSP sul PC di progetto, lo stesso tipo di DSP su Raspberry Pi e un crossover analogico attivo. Le proprietà matematiche dipendono dalla funzione di trasferimento e dalle sorgenti acustiche; autonomia e costo dipendono dalla piattaforma e dai collegamenti. Il richiamo software dei profili è utile al doppio uso, senza renderlo esclusivo del digitale.

## Metodo e fonti

Domande, inventario locale, query, parametri e criteri sono nel [protocollo](scope.md). Fonti primarie S1-S6 e review S7 sono registrate con passaggi letti e limiti in [sources.md](sources.md); non è stato eseguito uno screening sistematico dell'intera letteratura. I registri preesistenti del progetto sono usati per ricostruire le decisioni, non come sostituti delle fonti fisiche. Le schede bibliografiche precedenti non sono promosse integralmente per la sola lettura di alcuni passaggi.

## Sintesi delle evidenze

Linkwitz Lab collega i filtri attivi alla risposta dei trasduttori; W3C fornisce le forme dei biquad, TI la relazione fra parametri e componenti. Cecchi e coautori distinguono requisiti di modulo, fase, direttività, latenza e complessità nelle famiglie di crossover: una risposta piatta nel modulo non esaurisce la qualità del sistema. CamillaDSP documenta binari x86/ARM e backend; Raspberry Pi documenta modalità audio, senza qualificare l'interfaccia multicanale da acquistare. Sono tipi di evidenza diversi, non benchmark comparativi.

Il dossier deriva la somma allpass LR4, la discretizzazione con mappatura bilineare, il ruolo del Q analogico, la sensibilità al ritardo e l'invarianza del rapporto fra rami sotto un profilo comune. Il [rapporto numerico](risultati-modello.json) documenta le verifiche e i controesempi. Le figure sono generate dai calcoli, non copiate dalle fonti.

## Dissensi e interpretazioni da evitare

Sono respinte tre generalizzazioni: che il digitale garantisca da solo un diffusore migliore; che il Pi sia automaticamente più conveniente per l'intera catena condivisa; che due profili digitali garantiscano estensione e pressione sufficienti per ogni impiego. Il confronto non mostra una superiorità sonora universale. La possibilità di un'EQ comune esiste anche nell'analogico; la praticità del richiamo software resta un vantaggio operativo, condizionato da avvio e routing affidabili.

## Limiti e lavoro aperto

Non sono stati confrontati consumi, costi correnti, stabilità con la DAW o latenze end-to-end delle tre piattaforme. Non sono disponibili driver definitivi, misure del cabinet, polarità acustica, risposta nella stanza o taratura dei livelli fisici. Il modello assume LTI e sorgenti normalizzate: non descrive clipping, limitatori dinamici, compressione termica o riflessioni. Il progetto acustico e il collaudo hardware restano necessari prima di chiamare pronti i profili mix/ascolto.

La lettura della review AES è parziale; i lavori citati al suo interno rimangono riferimenti da esaminare. Ogni claim conserva il passaggio letto, la derivazione o la prova che lo sostiene. L'uso futuro di Raspberry Pi rimane una possibilità progettuale da qualificare nella catena reale.

## Dove proseguire

[Manuale operativo](../../docs/61-camilladsp-manuale-tecnico.md), [dossier ingegneristico](../../docs/62-confronto-crossover-e-verifica-matematica.md), [indice della documentazione](../../docs/INDICE-RAGIONATO.md) e [scheda prioritaria Linkwitz Lab](../web/linkwitzlab-active-filters.md) sono i punti d'ingresso. La bibliografia tecnica e gli URL di questa review restano nel registro del topic; l'aggiornamento del .bib segue i controlli canonici del progetto.
