# 11. Un file valido non è ancora un diffusore conforme

## La premessa che mescolava tre passaggi

Il progetto collegava la possibilità di salvare con ARTA alla creazione del GLL, attribuendo inoltre gratuità a SpeakerLab. La ricerca di MS-321 ha separato acquisizione, authoring e autorizzazione del modello. Il [capitolo65](../../docs/65-caratterizzazione-aperta-e-dati-di-misura.md) conserva fonti, versioni e limiti. Il risultato pratico è una strada di confronto su file che può essere sviluppata senza attendere un GLL o riaprire la parte fisica.

## Formato e significato arrivano insieme

[caratterizzazione.py](../../tools/caratterizzazione.py) distingue il FRD numerico dai quattro campi OSM della versione studiata. Il nome dell'estensione non basta a stabilire le colonne. Una fase mancante rimane assente; convertirla in zero creerebbe un dato utilizzabile nelle somme complesse che la misura non aveva fornito.

Lo stesso principio vale per il riferimento di livello. Una curva a -3 dB deve rimanere a -3 dB rispetto al riferimento comune. Il controllo negativo ha sostituito quel riferimento con la media di ogni curva: il test ha rilevato il falso within_bounds. È un difetto che il solo roundtrip del file non potrebbe vedere, perché tutti i byte potrebbero essere salvati correttamente mentre il confronto perderebbe il significato fisico.

## Il bordo non può nascondere l'intervallo

La prima versione tagliava i dati alla banda richiesta prima di misurare gli intervalli. Due file con un ampio vuoto che attraversava un estremo risultavano così abbastanza densi nella sola parte rimasta. Le prove dedicate hanno riprodotto il falso verde.

Il codice corretto sceglie gli intervalli originali che intersecano la banda:

```python
relevant_intervals=(curve.frequency_hz[:-1]<hi)&(curve.frequency_hz[1:]>lo)
original_gaps=np.diff(np.log2(curve.frequency_hz))[relevant_intervals]
```

Solo dopo si valuta l'eventuale interpolazione agli estremi già coperti. Rimane un confronto sui campioni disponibili e sugli estremi interpolati, senza una garanzia continua fra campioni. La soglia della fixture è una scelta dichiarata nel manifesto, non una proprietà misurata del diffusore.

## La firma riguarda i byte effettivamente letti

Il programma legge ogni input in uno snapshot, lo interpreta e conserva gli stessi byte in inputs insieme alla loro impronta. Il check ricostruisce il risultato dagli input correnti e confronta tutti i file. Non normalizza i dati per farli passare e non sovrascrive una cartella esistente.

Un prefisso punto nel percorso aveva prodotto un altro disaccordo: il filesystem lo normalizzava, mentre il manifesto conservava una chiave diversa. La prova ha osservato il fallimento del proprio check; la normalizzazione dei soli percorsi relativi ha risolto il caso. La protezione non si ferma al testo del percorso: una prova con un collegamento di directory reale verifica che la destinazione risolta rimanga nel dataset.

## Due verdetti da conservare fino al terminale

La fixture contiene una valle intenzionalmente oltre il limite. La generazione è riuscita e il pacchetto è integro; i dati sintetici non rispettano il bersaglio. Il terminale espone entrambi i risultati. hardware_qualified resta falso anche quando le curve sono tutte entro i limiti o il manifesto dichiara measured: quella dichiarazione non verifica calibrazione, catena e validità fisica.

Le 26 prove coprono questi contrasti. I dati di esempio e il rapporto sono versionati; i programmi di acquisizione non sono stati eseguiti. È il confine che permette di preparare il collaudo futuro senza fingere di averlo già svolto.
