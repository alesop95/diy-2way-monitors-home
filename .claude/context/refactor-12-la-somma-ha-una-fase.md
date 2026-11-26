# 12. La somma ha una fase

## Com'era e perché non bastava

caratterizzazione.Curve conserva il modulo e la fase, distinguendo fase assente da zero. analyse_dataset confronta i campioni di ciascuna risposta con un bersaglio, ma non costruisce la risposta di due driver dopo il crossover. Due curve vicine al livello desiderato possono ancora cancellarsi: il modulo da solo non permette di decidere la somma.

La scorciatoia abs(low)+abs(high) sembra ragionevole nei grafici di ampiezza e fallisce proprio nel caso che interessa al progetto. Con due rami unitari a180 gradi restituisce2 invece di0. La prova test_opposite_driver_phases_cancel_instead_of_adding_magnitudes esercita i numeri complessi reali del nuovo modulo, non un confronto fra etichette.

## Il passaggio nel codice

somma_acustica.sos_response valuta ciascuna sezione con q=exp(-j*2*pi*f/Fs), normalizza i coefficienti rispetto ad a0 e rifiuta poli sul cerchio unitario o esterni. _filtered moltiplica risposta importata, filtro, guadagno, polarità e ritardo esplicito. sum_branches esegue poi:

```python
total = low + high
```

Il controllo della griglia precede il calcolo. Il programma rifiuta la fase mancante; non la riempie con zero. Il manifesto obbliga inoltre a dichiarare riferimenti comuni e risposte dei driver ancora prive del crossover da applicare. Queste dichiarazioni sono condizioni dell'esperimento futuro, non garanzie ricavate dal parser.

## I nulli e i confini dei dati

La somma può arrivare a un nullo anche con due fasi perfettamente definite negli input. Un numero complesso nullo non porta una fase utile: assegnargli0 gradi renderebbe l'export apparentemente completo. Il CSV lascia il campo vuoto nei campioni indistinguibili dal nullo secondo la soglia relativa dichiarata; conserva parte reale e immaginaria. In presenza di un nullo, il FRD rinuncia alla fase per tutto il file e conserva due colonne. Gli altri campioni restano dettagliati nel CSV.

Anche la qualità va trasportata senza inventarla. La coerenza della somma non è il minimo delle coerenze dei driver. Il rapporto conserva la qualità dei singoli input e non assegna una coerenza risultante. Se un input manca di copertura o ha coerenza insufficiente, rimangono diagnostici e originali, ma non viene emesso il dataset che il modulo successivo potrebbe analizzare ignorando quella condizione.

## Che cosa provano i risultati

Ventidue test, inclusi tre casi LR4 e confronto con il modello continuo alla frequenza bilineare. Al taglio: rami allineati1, polarità invertita circa0 e sei campioni di ritardo sqrt(0,5). La mutazione della somma dei moduli fa cadere la prova di cancellazione; ripristino del sorgente verificato per SHA. I pacchetti integri dei due casi negativi conservano outside_bounds.

Il passaggio reale al modulo di caratterizzazione mantiene simulated e hardware_qualified falso. I filtri non diventano una taratura del diffusore e non vengono inviati al motore. La scelta esecutiva dei componenti, la fase acquisita e la calibrazione restano nei loro perimetri sospesi.

La revisione ha aggiunto una ventiduesima prova: due rami che riusano lo stesso percorso mentre il file cambia dopo la prima lettura. Il difetto originale leggeva due volte e sovrascriveva la copia conservata. La cache per percorso normalizzato lega invece calcolo e ricevuta agli stessi byte. Anche questa correzione è stata mutata, vista rossa e ripristinata con SHA identico; i rapporti precedenti sono stati archiviati prima dell'aggiornamento delle impronte.
