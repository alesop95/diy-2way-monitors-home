# Somma dei driver e crossover sui dati importati

Sviluppo del26 novembre2026, MS-322. Collega la [caratterizzazione su file](65-caratterizzazione-aperta-e-dati-di-misura.md) al confronto del crossover: conserva la risposta complessa di ciascun driver e applica soltanto i filtri e i parametri dichiarati. Non misura un diffusore e non carica configurazioni nel servizio audio.

## Che cosa occorre prima della somma

Servono due curve con fase, identica griglia di frequenze e riferimenti compatibili. Il manifesto speaker-complex-sum-1 dichiara stesso livello di eccitazione elettrica, origine temporale comune, direzione e distanza di osservazione uguali. Le risposte devono precedere il crossover che si vuole applicare: una misura già filtrata non deve riceverlo una seconda volta.

La dichiarazione di questi riferimenti non ne dimostra la validità. Due file FRD formalmente corretti possono provenire da finestre, livelli o riferimenti temporali incompatibili. Il rapporto li marca declared_not_independently_verified; hardware_qualified rimane falso anche se gli input sono dichiarati measured. Il risultato è sempre simulated e conserva input_data_kind e byte originali.

Il programma rifiuta curve senza fase o con griglie diverse. Non interpola la fase, non estrae fase minima, non riallinea impulsi e non normalizza ciascun driver. Le direzioni diverse si studiano con coppie di curve e manifesti distinti; qui non viene ricostruito un diagramma polare da una misura assiale.

## Funzione di trasferimento applicata

Ogni sezione SOS[^1] è dichiarata come [b0,b1,b2,a0,a1,a2]. Alla frequenza f, con campionamento Fs, si pone q=exp(-j*2*pi*f/Fs) e si valuta:

$$H(f)=\prod_k\frac{b_{0,k}+b_{1,k}q+b_{2,k}q^2}{a_{0,k}+a_{1,k}q+a_{2,k}q^2}.$$

Per ciascun ramo il filtro moltiplica la risposta importata, il fattore10^(gain_db/20), la polarità+1/-1 e il termine exp(-j*2*pi*f*delay_ms/1000). Un ritardo positivo ritarda il ramo; la somma finale è quella dei numeri complessi, non dei moduli o dei dB. Il [capitolo62](62-confronto-crossover-e-verifica-matematica.md) conserva le formule LR4 e il confronto continuo/discreto da cui provengono i coefficienti dell'esempio.

Coefficienti non finiti, a0 nullo e poli con modulo maggiore o uguale a1 sono rifiutati. Tutte le frequenze devono essere positive e inferiori a Fs/2. L'elenco SOS vuoto è identità. La stabilità matematica del filtro non qualifica guadagno reale, potenza, rumore o stabilità di una periferica audio.

## Banda valida, coerenza e nulli

Ogni driver dichiara valid_range_hz. Per entrambi vengono verificati copertura del bersaglio, intervalli della griglia originale e coerenza, quando presente. Una banda insufficiente o una coerenza sotto soglia dà input_quality_insufficient e impedisce l'export di system.frd e dataset.json. Rimangono rapporto, CSV diagnostico e copie degli input. Un filtro che attenua un ramo non autorizza a inventare i dati mancanti di quel driver.

La coerenza della somma non è ricavata dal minimo delle coerenze dei rami: quelle degli input restano nel rapporto, quella del risultato è sconosciuta. L'assenza della coerenza negli FRD è dichiarata come null, senza convertirla in una prova di qualità.

Nei nulli la fase non è zero. Il programma la considera numericamente indefinita quando il modulo della somma non supera10^-12 volte la somma dei moduli dei due rami filtrati. È una soglia numerica dichiarata, non una misura del rumore. Il CSV conserva parte reale e immaginaria e lascia vuota la fase in quei campioni. Se almeno un campione non ha fase definita, il FRD risultante ha soltanto frequenza e modulo; le fasi degli altri campioni rimangono nel CSV. Negli altri casi il FRD ha tre colonne.

Il modulo esportato usa un pavimento di-300dB per evitare logaritmi infiniti. Il rapporto conta i campioni interessati e conserva soglia e pavimento; il CSV conserva il residuo complesso prima del pavimento. Una cancellazione numerica vicina a questo limite non è una previsione di attenuazione reale del diffusore.

## Esempio analitico osservato

Il [dataset versionato](../data/somma-acustica-demo/README.md) contiene due driver unitari su242 frequenze, con fase zero costruita e coefficienti elettrici LR4 a2000Hz/48000Hz. Il [rapporto durevole](../research-vault/somma-acustica-20261126/risultati.json) conserva i tre casi, le impronte e i confronti analitici. Non rappresenta i candidati SB o una misura del prototipo.

| Caso | Modulo al taglio, atteso e calcolato | Confronto100-10000Hz entro±0,5dB |
|---|---|---|
| Allineato |1; calcolato1,0000000000000009 | within_bounds; errore massimo dal livello comune circa6,18e-14dB |
| Tweeter invertito |0; residuo numerico circa1,24e-15 | outside_bounds; fase indefinita nel campione2000Hz |
| Tweeter ritardato di sei campioni | sqrt(0,5); calcolato0,7071067811865486 | outside_bounds; scostamento massimo in banda circa3,69233dB |

Sei campioni equivalgono a0,125ms alla frequenza dichiarata. Al taglio il ritardo introduce90 gradi fra i rami e il modulo scende di circa3,0103dB; lo scostamento massimo nella banda non coincide necessariamente con il taglio. Tutti e tre i pacchetti sono integri, ma soltanto il primo rispetta il bersaglio sintetico. Ogni caso conserva sette file firmati più il manifesto.

## Uso ed esecuzioni verificate

Il manifesto di esempio è anche il modello completo dei campi richiesti: provenienza, unità, riferimenti, direzione, campionamento, bersaglio, percorsi relativi e filtri. Per generare un pacchetto si passano --manifest e --out con una cartella nuova; aggiungendo --check si ricalcola dai sorgenti senza scrivere e si confrontano tutti i file. La generazione CLI è esercitata anche dalle prove su cartelle temporanee.

Questi controlli sono stati eseguiti dalla postazione Windows in PowerShell:

```powershell
cd "E:/diy-2way-monitors-home"
python tools/test_somma_acustica.py
python tools/somma_acustica.py --manifest data/somma-acustica-demo/manifest.json --out build/somma-acustica-20261126/allineato --check
python tools/somma_acustica.py --manifest data/somma-acustica-demo/invertito.json --out build/somma-acustica-20261126/invertito --check
python tools/somma_acustica.py --manifest data/somma-acustica-demo/ritardo-6-campioni.json --out build/somma-acustica-20261126/ritardo-6-campioni --check
python tools/caratterizzazione.py --manifest build/somma-acustica-20261126/allineato/dataset.json --out build/caratterizzazione-somma-20261126
python tools/caratterizzazione.py --manifest build/somma-acustica-20261126/allineato/dataset.json --out build/caratterizzazione-somma-20261126 --check
```

Ventidue test superati. I tre check restituiscono integrità verde; i due casi negativi conservano outside_bounds. Il dataset allineato passa realmente al modulo di caratterizzazione e resta simulated, hardware_qualified falso. La cartella del confronto downstream ora esiste: per rigenerarla occorre scegliere una destinazione nuova; --check è ripetibile. I cinque controlli nuovi sono nella chiusura ordinaria, insieme ai precedenti.

## Prove negative e limiti del risultato

È stata applicata la mutazione che sostituisce low+high con abs(low)+abs(high). La prova delle fasi opposte è diventata rossa; sorgente ripristinato con SHA identico. La copia e la ricevuta restano nel livello privato. I test coprono anche input mancanti, riferimenti non dichiarati, filtri instabili, percorso esterno, qualità insufficiente, nulli, alterazioni dei pacchetti e conservazione di file umani preesistenti.

Questo sviluppo non interpreta tutte le configurazioni CamillaDSP, non confronta il nuovo calcolo con una nuova esecuzione del motore e non modifica il servizio. La verifica LR4 confronta la risposta dei coefficienti con il modello analogico alla frequenza trasformata bilinearmente; gli altri collaudi del motore già registrati mantengono il loro perimetro. Fase reale, calibrazione, direttività e livelli dei driver montati restano da qualificare quando le verifiche fisiche saranno riaperte.

## Difetto dello snapshot riprodotto e corretto

Nella revisione del26 novembre è stato provato il caso di due rami che puntano allo stesso file, uno con prefisso punto, mentre il file cambia dopo la prima lettura. La prima implementazione lo leggeva due volte e poteva calcolare i rami con byte diversi, conservando soltanto l'ultima copia. La prova è diventata rossa con due letture invece di una.

Ora i percorsi relativi normalizzati riusano i byte già letti nel pacchetto. La prova verifica sia il numero di letture sia il contenuto conservato e il risultato analitico. La mutazione che ripristina la doppia lettura fa ricomparire il difetto; sorgente nuovamente ripristinato per SHA identico. Prima di aggiornare i rapporti sono stati archiviati e riletti byte per byte25 artefatti; input e risultati numerici sono rimasti invariati.

[^1]: Second-order sections, sezioni del secondo ordine.
