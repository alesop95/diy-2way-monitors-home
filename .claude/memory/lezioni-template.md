# Lezioni per il template

> Le lezioni nate in questo progetto che valgono oltre il progetto, cioè che passano le due domande della sezione 16 di `.claude/PROJECT-SYSTEM.md`: restano vere tolti i nomi propri, e non sono già nella testa di chi lavora bene. Una voce per lezione, creata con `python .claude/templates/tools/lezioni-template.py nuova` nel giro di lavoro in cui la lezione nasce. Lo stato non si scrive qui: una lezione è recepita quando il template la elenca in `.claude/templates/lezioni-recepite.json`, che arriva con l'allineamento.

Adottato il: 2026-11-20

## L-001 - 2026-11-20 - Identità della fonte, lettura e uso sono tre contratti distinti

Nel progetto audio il nuovo registro collega ID, versione, alias e citekey ai punti di uso. Il censimento trova anche vecchi riferimenti: marcarli tutti letti sarebbe falso. La registrazione, la verifica dei metadati e la copertura della lettura hanno campi separati. Prova locale: tools/test_mappa_fonti.py verifica che un riferimento non curato rimanga da verificare e da riconciliare; research-vault/usi-fonti-progetto.json elenca sezioni e righe. La regola vale per ogni progetto che usa un corpus senza averlo letto integralmente.

## L-002 - 2026-11-20 - Rifiutare collisioni prima di costruire una mappa

L'unione dei seed in un dizionario perde un ID duplicato prima che il conteggio finale possa rilevarlo. Il nuovo seed_index rifiuta il doppione prima dell'assegnazione; alias_index rifiuta un URL assegnato a due ID. I test sono stati rossi e poi verdi. Una conta degli identificativi dopo una sovrascrittura non misura l'unicità degli input. Evidenza: tools/test_mappa_fonti.py, MS-292.

## L-003 - 2026-11-20 - Una guardia di laboratorio deve agire prima del processo esterno

Il banco CamillaDSP destinato ai file deve rifiutare backend hardware, percorsi e formati estranei prima di avviare il motore. La prova usa un binario inesistente: un errore di avvio dimostrerebbe che la guardia è arrivata troppo tardi. Due sottocasi alterati sono rifiutati prima del processo. Evidenza locale: tools/test_studio_sistema.py e MS-291. Il principio è riutilizzabile per ogni collaudo che promette isolamento.

## L-004 - 2026-11-20 - Le anteprime devono identificare l'artefatto che rappresentano

Una vecchia immagine della relazione faceva apparire tagliato un PDF successivamente corretto. Le anteprime correnti sono state rigenerate dai due PDF finali e associate alle loro impronte. La verifica del sorgente o di una PNG precedente non certifica il documento consegnato. Evidenza: MS-286/290, docs/latex/README.md e rapporto preview-consegna-v5. Lo stesso vincolo vale per screenshot, rendering CAD ed export.

Sviluppo MS-300/305: le immagini QA diventano effimere dopo l'ispezione; il manifesto corrente conserva l'identità del PDF e dei sorgenti, e tools/test_verifica_documenti.py rileva anche un sorgente cambiato con PDF integro. Non serve conservare ogni bitmap per mantenere controllabile la provenienza.

## L-005 - 2026-11-20 - Le verifiche specifiche appartengono alla chiusura ordinaria

La chiusura generica non eseguiva le suite DSP e geometriche del progetto. Registrarle in tools/controlli-progetto.txt rende il controllo ripetibile su Windows e Unix, senza una lista ricordata dall'agente. Il nuovo generatore di fonti aggiunge sia il confronto dell'output sia le regressioni: una suite solo sintattica non avrebbe rilevato il KeyError sul censimento reale. Evidenza: MS-291/292 e i comandi locali di chiudi.

## L-006 - 2026-11-20 - Comprimere le prove superate conserva la storia senza copie espanse

Trecentoquaranta file di run e preview precedenti sono stati archiviati con percorsi originali, elenco esatto e SHA-256 ricalcolato su ogni membro. Solo dopo sono state rimosse quattordici cartelle espanse, ricontrollando contenimento e originali. Restano anche i run falliti, perché spiegano le correzioni. Evidenza: MS-293 e manifest/ricevuta privati indicati nella procedura docs/90-riferimenti/metodo-fonti-lezioni-riordino.md. L'archivio sullo stesso disco non è un backup.

## L-007 - 2026-11-20 - Un confronto fra metodi non autorizza il trasferimento dei dati

Il proprietario ha autorizzato il confronto di regole documentali imponendo un confine assoluto fra ambiente aziendale e progetto privato. Si applicano soltanto principi generici e prove nate nel progetto audio. Non si importano nomi, percorsi, dati, esempi o casi aziendali, neppure negli ignorati. La procedura descrive il perimetro senza allegare i documenti esterni. Il controllo di privacy del repository resta distinto dalla legittimità della lettura autorizzata.
