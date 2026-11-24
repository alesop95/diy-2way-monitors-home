# 5. Filtro, calcolatore e diffusore sono tre livelli diversi

Approfondimento del 2026-11-20, richiesto dall'utente insieme alla ricerca sul crossover. Non cambia il servizio o i filtri operativi: aggiunge il modello e il criterio per interpretare le prove. Punto d'ingresso nel [master didattico](studio-didattico-master.md), risultato tecnico nel [dossier](../../docs/62-confronto-crossover-e-verifica-matematica.md).

## La premessa che va resa esplicita

Il banco esistente di tools/collauda-dsp-pipewire.py e il profilo in config dimostrano elaborazione, ordine dei canali, volume e mute. Un errore di lettura possibile è passare da «il LR4 si somma nel banco» a «il monitor reale si sommerà», oppure da «CamillaDSP è installato sul PC» a «il Raspberry è escluso». Le seconde affermazioni richiedono dati diversi dalle prime.

Il costo di quella confusione arriverebbe alla costruzione: acquistare un convertitore prima di sapere chi ospita il processo, fissare un crossover prima dei driver, oppure promettere autonomia con la stessa interfaccia ancora impegnata dal PC della DAW. La correzione di qualità consiste nel separare funzione del filtro, risorse del calcolatore e somma acustica.

## Che cosa dimostra il codice già presente

Il client tools/monitor_dsp.py, nel caricamento del laboratorio, compie questi passi reali:

```python
validate_lab_config(config)
if peer.call('GetVersion') != '4.1.3':
    raise ValueError('Motore diverso dalla versione 4.1.3 collaudata')
peer.call({'SetMute': True})
peer.call({'SetVolume': -60.0})
peer.call({'SetConfigJson': json.dumps(config)})
```

Il banco controlla successivamente grafo e segnale. Il codice è corretto per il suo perimetro; non interroga un driver acustico perché non è stato ancora scelto. Aggiungere la parola «calibrato» al risultato sarebbe un errore documentale, anche senza un difetto nel programma.

## Il nuovo modello e il controesempio

tools/verifica-matematica-crossover.py rende verificabile il passaggio successivo. Prima calcola le funzioni ideali:

```python
low, high = analog_lr4(frequency, cutoff)
```

Poi modifica davvero una delle funzioni complesse, aggiungendo un ritardo:

```python
delayed_sum = low + high * np.exp(-2j*math.pi*frequency*path_delay)
```

Il primo caso ha modulo della somma unitario, mentre il secondo dipende dalla fase. Al crossover di esempio un errore di cammino di 20 mm vale 41,9825 gradi e -0,596456 dB nel modello a livelli uguali. Il controllo negativo con mezzo periodo o inversione di polarità produce il nullo: la prova vede l'effetto specifico, non un generico fallimento del processo.

Questa estensione non è una simulazione completa del cabinet. Il rapporto dichiara assenza di driver, stanza, conversioni e non linearità. Il vantaggio è poter rispondere separatamente a due domande: «il programma calcola il filtro?» e «quel filtro, insieme al driver e alla geometria, dà la risposta desiderata?». Soltanto la prima è già verificata dal banco operativo.

## La proprietà che aiuta il doppio uso

Un'EQ comune ai rami di una cassa si fattorizza fuori dalla somma e si cancella nel rapporto fra i contributi. Il codice confronta quel rapporto prima e dopo il profilo su tutta la griglia. Ciò permette di progettare preferenze mix/ascolto conservando la relazione lineare del crossover, purché i due rami restino gli stessi e non intervengano clipping o dinamiche differenti.

È un vantaggio di controllo e ripetibilità, non un'esclusiva fisica del digitale: anche una rete analogica comune può modificare la risposta complessiva. E non permette di superare escursione, potenza o volume. Il progetto guadagna una condizione verificabile al posto di uno slogan sul DSP.

## Come si conserva la catena della prova

Il protocollo è stato scritto prima del calcolo; il rapporto conserva input, ambiente e hash del sorgente. Le figure sono calcoli originali, con sorgente riproducibile e CSV nei derivati. Una prima esportazione con legende arrotondate è stata rifatta in una cartella nuova per rispettare la geometria del design di account: le serie precedenti sono conservate e il modello non cambia.

Linkwitz Lab è registrato come fonte prioritaria, con sezioni lette e limiti. La review AES è una fonte scientifica di contesto letta per passaggi dichiarati; non rende consultate le opere che cita. Il registro operativo racconta il giro concreto, mentre questo approfondimento conserva il principio riutilizzabile: un'uguaglianza dimostrata va mantenuta nel suo dominio prima di trasferirla al sistema fisico.
