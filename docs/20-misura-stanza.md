# Fase 1: misura reale della stanza

> Prima fase operativa del workflow. Produce la risposta all'impulso dell'ambiente nel punto di ascolto, che è il dato su cui si validerà tutto il modello geometrico costruito nelle fasi successive.

## Che cosa si sta misurando, e che cosa no

Il fraintendimento da evitare all'inizio è credere che questa fase misuri la qualità di un diffusore. Non lo fa. Ciò che si misura è la risposta della stanza: i tempi di riverberazione, i modi stazionari, le riflessioni precoci e i decadimenti. Il diffusore usato per eccitare l'ambiente è uno strumento di misura provvisorio, non l'oggetto della misura, e per questo la fase si può eseguire prima di avere i monitor progettati, usando qualunque altoparlante con risposta sufficientemente estesa.

Il valore della misura è che diventa il criterio di validazione del modello. Se l'analisi modale in Octave prevede un modo forte a una certa frequenza e la misura in REW mostra un picco alla stessa frequenza, il modello geometrico della stanza è corretto e le sue previsioni si possono usare. Se le due cose non coincidono, il modello va corretto prima di andare avanti, e quella discrepanza vale più di qualunque simulazione fatta senza riscontro.

## Lo strumento

REW è gratuito e copre tutto il necessario per questa fase. Misura la risposta all'impulso con uno sweep logaritmico, calcola i parametri di decadimento T20, T30 e Topt, l'early decay time, cioè EDT, e i parametri di chiarezza C50 e C80, e visualizza il decadimento a banda stretta con il waterfall e con lo spettrogramma.

Il waterfall è la vista che conta di più in questo contesto, perché mostra quanto a lungo una banda stretta continua a suonare dopo che il segnale è cessato, ed è il modo diretto per vedere un modo stazionario invece di dedurlo da un picco nella risposta in frequenza.

## La catena di misura

Servono una interfaccia audio a bassa latenza, un cavo bilanciato, un supporto microfonico e un microfono di misura calibrato. Sulla macchina l'interfaccia è già disponibile, una Focusrite Scarlett 2i2 di seconda generazione con alimentazione phantom a 48 V e preamplificatori di qualità adeguata.

La disponibilità della Scarlett è la premessa che decide la scelta del microfono, e vale seguire il ragionamento perché è un caso in cui la risposta ovvia non è quella corretta.

La scelta di default nella comunità è l'UMIK-1, un microfono USB calibrato. Il suo vantaggio è la semplicità: non serve interfaccia, non serve alimentazione phantom, non servono driver ASIO, e riduce il numero di variabili in gioco, cioè cavi, guadagno del preamplificatore e rumore di fondo. Su una macchina senza interfaccia audio sarebbe la scelta giusta senza discussione.

Avendo però già la Scarlett, l'USB diventa un vincolo invece di una comodità: obbliga a una catena separata e non riutilizzabile. Un microfono XLR calibrato individualmente costa quanto l'UMIK-1, sfrutta l'interfaccia che c'è, e resta usabile con altri sistemi in futuro.

| Modello | Prezzo indicativo | Calibrazione | Pro | Contro |
|---|---|---|---|---|
| Behringer ECM8000 | 40-60 euro | generica, custom opzionale | economico, facile da trovare | alta variabilità fra le unità, alte frequenze meno precise |
| Dayton Audio EMM-6 | 70-90 euro | file individuale incluso | più consistente dell'ECM8000, file personalizzato | disponibilità in Europa variabile |
| Sonarworks SoundID Reference Mic | 70-90 euro | file individuale | affidabile, compatibile con REW | leggermente più rumoroso dell'EMM-6 |
| iSEMcon EMX-7150 | circa 200 euro | individuale | standard professionale, ottima linearità e stabilità | costo più alto |

La scelta per questo progetto è il Dayton Audio EMM-6, con la Sonarworks come alternativa equivalente. Il file di calibrazione è incluso nel prezzo e si scarica dal sito del costruttore inserendo il numero di serie stampato sulla base del microfono; il file si carica in REW e da quel momento le misure tengono conto delle correzioni individuali di quella unità.

## Il ruolo della calibrazione, ridimensionato con onestà

Vale precisare quanto conta davvero la calibrazione in questo scenario, perché è facile sovrastimarla.

Entrambi i microfoni economici misurano correttamente da 20 Hz a 20 kHz, e in una stanza non trattata le variazioni introdotte dall'ambiente superano di molto la differenza fra un ECM8000 non calibrato e un microfono calibrato individualmente. L'errore di calibrazione diventa rilevante nell'analisi fine delle alte frequenze, cioè sulle riflessioni e sui decadimenti rapidi.

L'argomento più forte a favore della calibrazione individuale, cioè la ripetibilità fra misure prima e dopo un trattamento acustico, in questo progetto non si applica: la stanza non verrà trattata, quindi non ci saranno misure comparative pre e post.

Resta però un argomento valido, ed è quello che fa pendere la scelta. La precisione sopra i 10 kHz è poco critica per la messa a punto di bassi e medi, ma influisce sul disegno del tweeter e sulla frequenza di incrocio del crossover, che sono esattamente due degli output della fase 4a. Un microfono calibrato individualmente riduce l'incertezza in quella zona, e quindi migliora la coerenza del progetto del diffusore, non la caratterizzazione della stanza.

## La procedura

Si collega il microfono all'interfaccia, si configura la scheda audio in REW e si carica il file di calibrazione del microfono. Si esegue uno sweep logaritmico da 20 Hz a 20 kHz con il microfono nel punto di ascolto, all'altezza dell'orecchio. Si salvano tre artefatti, e ciascuno serve a una cosa diversa: la risposta all'impulso in formato `.wav`, che è il dato grezzo da passare a Octave nella fase 3; la risposta in frequenza in formato `.txt`, che è il dato da importare in VituixCAD nella fase 4a; la sessione in formato `.mdat`, che conserva tutto il contesto della misura e permette di rifare l'analisi senza rimisurare.

I parametri da leggere e conservare sono RT60, C50 e C80, ed EDT.

## Il vincolo della stanza, che è già noto

Dalla discussione con un collega esperto di acustica degli ambienti, riportata negli appunti del progetto, emergono tre elementi che questa misura dovrà quantificare e che sono già identificati qualitativamente.

La forma irregolare della stanza è un vantaggio, perché distribuisce i modi invece di concentrarli come farebbe una stanza rettangolare.

Il soffitto spiovente è il problema maggiore, e la mitigazione pratica è posizionare il punto di ascolto sul lato dove il soffitto è più basso, così da ridurre al minimo la riflessione problematica.

La parete vicina alle spalle del punto di ascolto è il secondo problema, e riguarda le riflessioni alle basse frequenze. La posizione della scrivania non è negoziabile per ragioni di arredamento, quindi il vincolo va accettato e compensato nel progetto del diffusore invece di essere eliminato: è precisamente la ragione per cui questo progetto parte dalla stanza.
