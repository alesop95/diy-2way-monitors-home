# Fase 5: simulazione finale in Akabak 3

> Quinta fase operativa. È il punto in cui i due rami del progetto si incontrano: il modello del diffusore progettato in campo libero e il modello della stanza validato dalle misure reali. Produce la risposta prevista nel punto di ascolto e la posizione ottimale dei monitor.

## Perché questa fase esiste e perché arriva ultima

Solo qui si dispone dei due blocchi necessari, e nessuno dei due può essere sostituito da una stima. Il modello del diffusore viene dalla fase 4a, il modello della stanza dalla fase 3 dopo la validazione contro la misura della fase 1. Anticipare questa fase significherebbe simulare monitor ipotetici in una stanza non validata, e il risultato non direbbe nulla.

Akabak occupa questo posto per una ragione precisa e non per preferenza: è l'unico strumento gratuito che consente la simulazione mista, elettroacustica e acustica ambientale, in un solo passaggio. Gli altri strumenti del corredo coprono metà del problema ciascuno. VituixCAD è orientato al crossover e non fa BEM. EASE Focus calcola il campo diretto e non il riverbero. EASE JR farebbe il lavoro ma è a pagamento e il progetto non lo ha. Pachyderm sarebbe eccellente per l'acustica architettonica ma richiede Rhinoceros, che non gira su Linux.

L'obiettivo concreto è ottimizzare la posizione dei monitor vicino allo schermo e verificare la risposta all'impulso e la SPL risultanti al punto di ascolto, con attenzione al comb filtering, cioè alle cancellazioni per interferenza fra suono diretto e riflessioni.

## Che cosa serve prima di iniziare

Quattro ingressi, e ciascuno viene da una fase precedente.

Le misure reali dei driver, cioè i parametri Thiele/Small e le risposte in formato `.frd` per la risposta in frequenza e `.zma` per l'impedenza, oppure i dati inseriti a mano se le misure non sono disponibili.

La geometria del cabinet, che nel pannello di geometria di Akabak si definisce come volumi, porte, pareti e materiali, e che viene dalla fase 4b.

Il modello a elementi concentrati per il crossover, passivo o attivo, che permette di simulare filtri, equalizzazioni ed eventuale elaborazione digitale prima di costruire qualsiasi cosa.

Il modello a elementi al contorno per il pannello frontale e la diffrazione, che è essenziale per capire la dispersione e la risposta in asse e fuori asse, e che è la parte che nessuno degli altri strumenti gratuiti del corredo fornisce.

## Impostazioni di simulazione

L'intervallo di frequenza va impostato almeno da 20 Hz a 40 kHz, con risoluzione più fine di un ventiquattresimo di ottava. La banda estesa oltre l'udibile non è uno spreco: serve a vedere il comportamento del filtro e della cupola del tweeter oltre la banda utile, dove le risonanze si manifestano prima di rientrare nella risposta udibile.

I materiali vanno impostati con valori realistici, non con i default. Per il legno si usa la densità dell'MDF, fra 700 e 750 chilogrammi per metro cubo, con spessore dei pannelli fra 18 e 25 millimetri. Per l'assorbente interno si può modellare direttamente in Akabak schiuma acustica oppure fibra di poliestere.

La verifica di fase è il controllo che in un monitor da nearfield conta più di ogni altro: la coerenza di fase attorno alla frequenza di incrocio è critica, perché due driver che sommano fuori fase producono un buco nella risposta esattamente nella regione dove l'orecchio è più sensibile. Il controllo incrociato si fa in VituixCAD, che è più orientato al crossover e meno al BEM, e la coerenza fra i due strumenti su questo punto è un buon indicatore che il modello sia sano.

## La struttura del progetto sul disco

La convenzione di organizzazione dei file per un monitor a due vie è la seguente.

```
~/AkabakProjects/2Way_Monitor/
├─ Drivers/
│   ├─ Woofer.frd        risposta in frequenza del woofer
│   └─ Tweeter.frd       risposta in frequenza del tweeter
├─ Cabinet.akp           geometria del cabinet e materiali
├─ Crossover.akp         filtri passivi e simulazioni a elementi concentrati
└─ Project.aks           file principale che collega gli altri
```

Il file del cabinet contiene le pareti con il loro spessore, la posizione dei driver sul pannello frontale, il volume interno destinato al woofer e, se il caricamento è bass reflex, la porta con la sua lunghezza di accordo. Il file di progetto combina i tre calcoli: il BEM per la diffrazione sul pannello, il modello a elementi concentrati per la risposta del crossover, e la mappa SPL per la verifica della dispersione da zero a novanta gradi in asse e fuori asse.

Il modo pratico di iniziare non è costruire da zero ma partire da un file di esempio di sistema a due vie fra quelli distribuiti con il programma, e adattarne driver e dimensioni. Il pacchetto degli esempi è quindi materiale di lavoro, non documentazione accessoria, ed è la ragione per cui compare nel manifest di trasferimento verso la macchina di destinazione.

## Il ciclo di ottimizzazione

La sequenza operativa è aprire il file di progetto, collegare i file dei driver, collegare i file del cabinet e del crossover, e lanciare la simulazione. Si leggono quattro uscite: la risposta in frequenza, il diagramma di fase, l'impedenza del cabinet e la mappa SPL.

Poi si itera. Si modificano parametri e materiali finché non si ottiene una risposta lineare entro più o meno 2 dB, in asse e fino a più o meno dieci gradi fuori asse, nell'intervallo da 60 Hz a circa 20 kHz. È lo stesso criterio dichiarato per la fase 4, e la coincidenza è voluta: qui si verifica in ambiente ciò che là si era ottenuto in campo libero, e la differenza fra i due risultati è la misura di quanto la stanza pesa sul progetto.

## Simulazione in ambiente e alternative

L'ultimo passaggio della fase importa il modello del monitor nel modello della stanza e verifica la copertura e l'interazione con i modi. È il momento in cui la posizione dei monitor rispetto allo schermo, la loro altezza e la loro angolazione diventano parametri da ottimizzare invece di scelte di arredamento.

Fra le alternative, Pachyderm resta annotato nel documento sorgente come sezione mai scritta, ed è escluso per la dipendenza da Rhinoceros già discussa nella pagina della fase 2. Non c'è nulla di verificato da riportare al suo riguardo.
