# Caratterizzazione su file e via aperta, piano inline

Esecuzione con writing-plans ed executing-plans, sul main19e56b3 indicato dal proprietario. Mandato persistente di completamento autonomo, nessuna nuova domanda di avvio; niente add/commit/push/deploy, installazioni o collaudi fisici. Revisione in prima persona, nessun subagent. Due GRC preesistenti esclusi.

## Specifica e alternative

La ricerca è in research-vault/caratterizzazione-aperta-20261126. La via GLL diretta richiede authoring e autorizzazioni non provati nella catena libera; rifare l'acquisizione audio è fuori dal perimetro sospeso. Si sceglie l'analisi dei file aperti come sviluppo dell'esecutore: conserva la catena di misura esistente, rende utilizzabili gli export e non introduce spese o dipendenze. Non è una scelta d'acquisto del proprietario. Il catalogo non contiene un parser/controllo FRD pertinente; non viene installato un pacchetto.

Nuovo modulo tools/caratterizzazione.py, relativa suite tools/test_caratterizzazione.py, manifesto sintetico e cinque curve di esempio, pagina65 di metodo/uso. NumPy e libreria standard già presenti. Il programma non apre periferiche, non modifica i filtri e non produce GLL.

## Task1: dati numerici e fase

- [x] Provare prima lettura FRD a due/tre colonne e OSM v1.5.2 FRD/CSV a quattro, BOM/commenti, zero validi, valori non finiti, frequenze non crescenti, colonne incoerenti e coerenza fuori intervallo.
- [x] Implementare Curve e read_curve(path, format), con fase/coerenza opzionali, e complex_response che rifiuta fase assente. Nessuna correzione automatica di ritardo, polarità o fase minima.
- [x] Verificare roundtrip FRD a tre colonne e CSV che conserva coerenza; non esportare FRD di fase se l'input non la contiene.

## Task2: confronto e integrità del dataset

- [x] Provare bersaglio 60-20000Hz ±2dB riferito al livello esplicito, direzioni mancanti, estremi non coperti, buchi nella griglia, banda valida dichiarata insufficiente e coerenza bassa.
- [x] Implementare analyse_curve e analyse_dataset: interpolazione logaritmica solo agli estremi coperti, controllo sui campioni e massimo salto in ottave dichiarato. Nessuna garanzia tra campioni o sulla stanza. Un riferimento comune evita di normalizzare ogni curva separatamente.
- [x] Verificare ID/direzioni univoci, percorsi relativi contenuti nel dataset anche dopo risoluzione dei link, hash di codice/input/output. CLI su cartella nuova, --check rifiuta modifiche ai risultati; hardware_qualified sempre falso e provenienza dichiarata separata dalla verifica.

## Task3: esempio e consegna

- [x] Eseguire esempio sintetico con cinque direzioni, includendo un caso fuori bersaglio riconoscibile. Conservare JSON, CSV e FRD canonici senza chiamarli misure.
- [x] Correggere le affermazioni GLL nelle pagine correnti e istruire PA-014 senza promettere una catena proprietaria gratuita. Fonti curate, indici, roadmap, memoria e didattica aggiornati nello stesso giro.
- [x] Aggiungere suite e controllo alla chiusura, rigenerare i documenti toccati, QA e gate completo prima di proporre la milestone manuale.

## Focus della revisione

Fase assente non significa zero; quattro colonne OSM non sono tre FRD. La media dei dB non è una somma complessa. Un insieme rado o una direzione mancante non può diventare conforme. La banda fisicamente valida è distinta dalla mera presenza dei bin FFT. Anche dati etichettati measured non sono qualificati dal solo manifesto. Gli export di OSM sono documentati dal sorgente della versione scelta, senza affermare una prova runtime dell'app.


## Esito osservato, 26 novembre

Ventisei test verdi, mutazione del riferimento comune rilevata e sorgente ripristinato con SHA identico. Cinque curve analitiche da241 campioni: quattro entro i limiti e verticale+10 fuori di3,29644dB. Pacchetto coerente di17 file firmati più manifesto; hardware_qualified falso. I dati sintetici non qualificano un diffusore.

Quattro PDF correnti con QA valido; recap rigenerato e pagine1/4/5/6/7 ispezionate. Primo controllo completo concluso con «Controlli verdi»,41 comandi locali. Verifica finale dopo la persistenza nel rapporto privato chiudi-finale.txt, da leggere prima della proposta manuale. Mappa213 fonti/46 curate, catalogo184; identità VituixCAD conservata senza forzare la guardia. Classificazione binaria dei PDF aggiunta contro il driver Git globale astextplain, senza conversione dei file di testo. PA-014 resta aperta per le scelte e qualifiche reali sospese.
