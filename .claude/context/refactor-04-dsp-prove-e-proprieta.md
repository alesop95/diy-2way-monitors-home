# 04. Provare il DSP e rispettare la proprietà della pipeline

Il 19 novembre il passaggio dal DSP su file al servizio PipeWire ha introdotto una differenza concreta: la prova lavora in una sessione audio condivisa. Un errore può lasciare client e nodi aperti oppure fermare un lavoro che non appartiene al banco. La prestazione del filtro e la correttezza dell'orchestrazione diventano due domande distinte. I microstep MS-246/256 e la revisione successiva conservano le prove; questa pagina spiega le scelte nel codice.

## Un ACK non dimostra processamento

La prima versione di load_lab chiamava wait_state accettando soltanto Running, Paused e Stalled. Sul computer reale i nodi esistevano senza link e il motore restava Starting, in attesa dei buffer. Il client scadeva anche se il profilo era stato accettato. Un test con un falso server che passa direttamente a Stalled non poteva vedere quel percorso.

La versione corrente in `tools/monitor_dsp.py` rilegge GetConfigJson e convalida tipo dei dispositivi, nomi, gruppo e numero di canali. Starting viene restituito come stato osservato, accompagnato da audio_running falso. Il banco chiede Running dopo aver collegato generatore e registratore. La proprietà misurata è dunque esplicita: prima esiste una configurazione accettata, poi il circuito elabora un segnale, infine le misure verificano il risultato del segnale.

```python
wait_state(peer, {'Starting', 'Running', 'Paused', 'Stalled'})
active = peer.call('GetConfigJson')
active = json.loads(active) if isinstance(active, str) else active
```

Leggere il profilo non basta a provare il trasferimento del filtro. Per questo il collaudo su PipeWire conserva il PCM[^1] e misura l'incrocio, le bande e la somma. Il test con lati scambiati modifica davvero la mappa del motore. Il rapporto non sarebbe sufficiente se si limitasse a dire che una stringa di configurazione contiene il numero corretto.

## Il ripristino segue la proprietà del lavoro

La prima orchestrazione aveva un finally che impostava mute e fermava sempre il motore. La revisione ha mostrato un caso importante: se la precondizione iniziale rifiuta un servizio già Running, quel finally interviene comunque sulla pipeline dell'utente. Un codice di rifiuto può quindi produrre proprio l'effetto che pretende di evitare.

In `tools/collauda-dsp-pipewire.py` il controllo dello stato precede ora sia la creazione della cartella sia il blocco che ripristina il motore. owns_pipeline diventa vero soltanto quando il banco inizia il caricamento. La pulizia dei client usa gli oggetti Popen creati dalla stessa esecuzione. Nessuna ricerca per nome di processo diventa un kill globale.

```python
status = read_status(peer)
if status['state'] != 'Inactive' or status['mute'] is not True:
    raise RuntimeError('Il servizio deve essere inattivo e silenziato prima del banco')
```

Il principio si applica anche ai link. `tools/dsp_pipewire.py` controlla tutte le connessioni che toccano i nodi posseduti; una porta collegata all'hardware o a un canale diverso interrompe il banco prima di togliere il mute. Le connessioni estranee fra altri nodi restano fuori dal suo lavoro. La prova del rifiuto iniziale verifica che nessuna richiesta mutante e nessuno Stop vengano inviati.

## Una prova negativa deve fallire per il motivo previsto

Il primo controllo dei lati scambiati catturava ogni AssertionError. Una cattura vuota poteva quindi essere registrata come mutazione rilevata. La revisione ha riprodotto esattamente questo falso successo con un errore di acquisizione. La correzione introduce RoutingMismatch, sollevato quando il tono è presente sul lato estraneo. detect_swapped_channels accetta soltanto quel tipo; errori di durata, formato, volume o ripristino restano fallimenti del banco.

Anche la durata è un'invariante indipendente. Un registratore che termina 0 non ha necessariamente scritto i sei secondi richiesti: validate_exit controlla sempre i 4608000 byte attesi e measure richiede 288000 frame. Questo controllo è distinto dall'eccezione specifica di pw-cat 1.6.2, che può uscire 1 quando raggiunge il limite campioni senza attivare il flag drained. L'eccezione richiede versione, ruolo, dimensione e log coerenti; non sostituisce la verifica dei campioni.

Il mute introduce invece una semantica temporale. Il fader Main ha una rampa: un valore mute true letto via API[^2] è il comando impostato, non la promessa che ogni buffer precedente sia già nullo. Il banco conserva il picco del transitorio e richiede zero a regime; mantiene un limite al transitorio rispetto al livello iniziale -60 dB. Non scarta l'inizio del file senza misurarlo e non presenta questo test come protezione fisica degli altoparlanti.

## La shell è parte dell'esperimento

Due errori hanno insegnato che anche il trasporto del comando va provato. Una regex con pipe è stata reinterpretata fra Windows e SSH[^3], avviando un programma che doveva essere soltanto un nome cercato. Un comando passato a tee ha poi nascosto il codice non zero del programma precedente, perché set -e da solo non propaga quel fallimento.

I comandi composti ora hanno un sorgente leggibile conservato nel progetto, trasportano byte su stdin e usano pipefail. Sorgente, impronta, output e risultato sono conservati insieme per ogni corsa. Il payload non vive nella riga di comando Windows, che aveva superato il limite di lunghezza. Questo conserva il codice realmente inviato e toglie un livello di interpretazione delle virgolette.

## Come estendere il banco

Un nuovo caso inizia dichiarando che cosa possiede e quale fenomeno deve misurare. Prima di riusare il ripristino va provato il rifiuto di una sessione già occupata. Prima di accettare un risultato negativo va distinta l'eccezione che dimostra il difetto da quelle che invalidano l'esperimento. Le prove di forma del grafo e quelle del segnale rimangono entrambe necessarie.

L'installazione corrente mantiene separati client di controllo e versione del banco. Una correzione al verificatore può essere collaudata in una cartella nuova senza sovrascrivere i file della home o cambiare l'avvio del motore. La copia storica resta identificabile e il runbook indica esplicitamente quella corrente. Il costo è conservare pochi file di programma superati; la rimozione dei dati esterni non viene nascosta in un aggiornamento software.

[^1]: *PCM*, Pulse Code Modulation: campioni numerici dell'onda audio nel tempo.

[^2]: *API*, Application Programming Interface: protocollo con cui il client interroga e comanda il motore.

[^3]: *SSH*, Secure Shell: connessione cifrata usata per eseguire i comandi sulla macchina Ubuntu.
