# CamillaDSP: servizio utente e banco PipeWire

Verificato su Ubuntu il 2026-11-19. CamillaDSP 4.1.3 con backend PipeWire è installato nella home, abilitato come servizio dell'utente e interrogabile su `127.0.0.1:12341`. Parte Inactive, mute true, volume -60 dB e configurazione null. Sono riusciti segnale stereo verso quattro vie virtuali, volume, mute a regime, controllo negativo dei lati e ripartenza dopo arresto forzato. Il [collaudo dopo il successivo riavvio e accesso utente](collaudo-dopo-riavvio-2026-11.md) ha confermato stato iniziale e intero banco. Nessuna interfaccia multicanale o risposta acustica è qualificata da questa prova.

## Percorsi e scelta di avvio

| Elemento | Percorso nella home |
|---|---|
| Motore | `.local/opt/camilladsp-4.1.3-pipewire/camilladsp` |
| Client di controllo | `.local/share/diy-2way-monitors/releases/dsp-control-1.0.0/` |
| Banco corrente | `.local/share/diy-2way-monitors/releases/pipewire-bench-1.0.1/` |
| Comando corrente | `.local/bin/diy-monitor-dsp` |
| Unità | `.config/systemd/user/diy-monitor-dsp.service` |
| Profilo del banco | `.config/diy-2way-monitors/camilladsp/laboratorio-pipewire.json` |
| Prove persistenti | `electroacoustics/collaudi/dsp-pipewire-20261119/` |

Il comando corrente è `diy-monitor-dsp`. Il precedente `monitor-dsp`, creato durante la prima prova, rimane come prototipo storico e non va usato per caricare il laboratorio: quella versione scade in Starting. Nessun file precedente è stato cancellato o sovrascritto per installare il client corretto.

L'unità esegue il motore con `--address 127.0.0.1 --port 12341 --wait --mute --gain=-60`, senza statefile e senza profilo all'avvio. La ripartenza non richiama una configurazione lasciata dalla sessione precedente. Il servizio è dell'utente: enabled non dimostra da solo che sia disponibile prima del login o che sopravviva a un riavvio della macchina.

## Preparazione ripetibile

I sorgenti restano nel repository canonico dei monitor, nelle cartelle `tools/` e `config/`. Il blocco ambiente copiato al gemello contiene la procedura; non duplica il software. Sono necessari Python 3, la libreria websockets già rilevata alla versione 15.0.1 e PipeWire con pw-cat, pw-link e pw-dump. Non è stato eseguito un pip install e non sono stati aggiornati i pacchetti audio del sistema.

Il download seguente è stato eseguito nella cartella temporanea nuova restituita da mktemp. `<CARTELLA_PROVA>` e `<SORGENTI>` sostituiscono soltanto percorsi locali; il repository pubblico non conserva la destinazione SSH reale.

```bash
mktemp -d /tmp/diy-dsp-20261119-XXXXXXXX
curl --fail --location --retry 2 --output <CARTELLA_PROVA>/camilladsp-linux-pipewire-amd64.tar.gz https://github.com/HEnquist/camilladsp/releases/download/v4.1.3/camilladsp-linux-pipewire-amd64.tar.gz
```

L'archivio ufficiale è di 3010119 byte, SHA-256 `04388dfbf0999732c51a972fa7c3dc7fa17437333124af7918022445c459851a`. Il binario estratto ha SHA-256 `933502e484f4696a218a0a935d8fa240ba0045e2a4af929fc920d54195180081`. Il file `tools/installa-dsp-utente.py` verifica entrambe, accetta soltanto l'unico membro regolare camilladsp e scrive ogni file in esclusiva. Prima controlla tutte le destinazioni, incluse unità e comando; se una esiste interrompe senza iniziare a copiarle. Non attiva servizi.

L'installatore è stato provato con l'archivio reale in una home di prova nuova; la seconda esecuzione sullo stesso insieme è stata rifiutata e tutte le impronte sono rimaste uguali. La verifica senza scritture è riuscita anche sulla home operativa, dopo l'installazione dei file durante i microstep. I due comandi parametrizzati seguenti sono le forme eseguite, rispettivamente nella home di prova e in quella operativa.

```bash
python3 <SORGENTI>/tools/installa-dsp-utente.py --home <HOME_NUOVA_DI_PROVA> --archivio <CARTELLA_PROVA>/camilladsp-linux-pipewire-amd64.tar.gz
python3 <SORGENTI>/tools/installa-dsp-utente.py --verifica
```

Per una ricostruzione si conserva la struttura tools/config delle sorgenti e si sceglie la home di destinazione soltanto dopo avere ispezionato i percorsi esistenti. Non si usa l'installatore per aggiornare sopra una versione precedente. Il file eseguibile e le sorgenti del client sono isolati per versione; i documenti e gli account dell'utente non sono ingressi dell'installatore.

## Attivazione e uso: comandi eseguiti

```bash
systemd-analyze --user verify "$HOME/.config/systemd/user/diy-monitor-dsp.service"
systemctl --user daemon-reload
systemctl --user enable --now diy-monitor-dsp.service
systemctl --user show diy-monitor-dsp.service -p ActiveState -p SubState -p MainPID -p UnitFileState
"$HOME/.local/bin/diy-monitor-dsp" stato
"$HOME/.local/bin/diy-monitor-dsp" laboratorio
"$HOME/.local/bin/diy-monitor-dsp" attesa
```

Stato deve riportare 4.1.3, Inactive, mute true e -60.0 prima del banco. Laboratorio convalida il solo backend PipeWire, nomi e gruppo dedicati, canali 2/4 e autoconnect nullo, prima di inviare richieste mutanti. Dopo l'ACK rilegge la configurazione e distingue il profilo caricato dal processamento. Starting con audio_running false è l'attesa del primo buffer osservata quando non ci sono link; non è una misura di segnale. Attesa imposta mute e -60 dB, ferma la pipeline e verifica Inactive.

## Collaudo del segnale e della ripartenza

Il comando seguente è stato eseguito anche sulla copia installata. Crea una sottocartella nuova per ogni corsa e conserva dati, grafo collegato, codici dei processi, stato del motore e misure.

```bash
python3 "$HOME/.local/share/diy-2way-monitors/releases/pipewire-bench-1.0.1/collauda-dsp-pipewire.py" --dest "$HOME/electroacoustics/collaudi/dsp-pipewire-20261119" --mutazioni
systemctl --user restart diy-monitor-dsp.service
"$HOME/.local/bin/diy-monitor-dsp" stato
```

Due client pw-cat nascono con `--target 0`, senza autoconnect, nei nodi nominati del banco. Il controllo verifica che appartengano ai processi appena creati, controlla direzione e indice delle porte e autorizza soltanto sei link espliciti: due verso la cattura DSP e quattro dal DSP al registratore. Prima di togliere il mute ricontrolla il grafo. In uscita le posizioni sono UNK, quindi l'ordine è provato dal segnale e dagli indici, non dal nome di un jack. I client creati dal banco vengono terminati anche in caso di errore e il DSP torna inattivo e silenziato; un errore di ripristino produce un rapporto fallito.

Ogni acquisizione normale, volume e mute contiene 288000 frame a 48 kHz e quattro float32, sei secondi. I toni sono 100/2000/8000 Hz a sinistra e 200/2500/9000 Hz a destra. Sul tratto centrale si misurano separazione dei lati, bande, incrocio e somma. Le somme normali sono entro 0,001 dB da 0 dB; quelle del secondo caso entro 0,001 dB da -6 dB. Il caso con lati realmente scambiati nella configurazione fallisce sul segnale acquisito.

Il mute software usa la rampa Main predefinita di 400 ms. È stato osservato un picco iniziale di `6.771774110347906e-7` in unità digitali, poi zero dal secondo 1 per tutto il resto della cattura. Il banco registra separatamente transitorio e regime: limita il primo rispetto alla preparazione a -60 dB e richiede picco inferiore a `1e-8` a regime. Non dichiara silenzio istantaneo e non certifica una protezione hardware per i tweeter.

È stata eseguita anche una prova di guasto controllato del solo servizio nuovo, mentre i nodi erano isolati e silenziati:

```bash
systemctl --user show diy-monitor-dsp.service -p MainPID -p NRestarts
systemctl --user kill --kill-whom=main --signal=KILL diy-monitor-dsp.service
systemctl --user show diy-monitor-dsp.service -p MainPID -p NRestarts -p ActiveState -p Result
ss -ltnp
```

La nuova istanza ha PID diverso e contatore NRestarts aumentato di uno. La lettura API conferma Inactive, mute true, -60.0 e configurazione null; nessun nodo del banco residuo e unica porta API su localhost. Il confronto del grafo prima/dopo il collaudo conferma metadati predefiniti invariati, sorgente analogica e uscita IEC958 ancora presenti, zero link residui. Forzature globali rimaste 48000 Hz e quantum 1024; non è una certificazione di bassa latenza.

## Troubleshooting osservato

### Le interrogazioni audio restano in attesa

Su Ubuntu il 19 novembre, pactl e pw-dump scadevano mentre il Core e liste parziali rispondevano. È stato individuato un WirePlumber aggiuntivo avviato per errore dal quoting di una vecchia diagnosi; rimuoverlo non ha risolto il timeout. Dopo snapshot dello stato del gestore e verifica dei nodi Closed, il riavvio del solo servizio gestito ha ripristinato le interrogazioni:

```bash
timeout -k 1 6 pw-dump -N
timeout -k 1 6 pactl info
systemctl --user restart wireplumber
```

I comandi di lettura sono stati ripetuti dopo il riavvio e hanno terminato 0. Non sono stati cancellati file di stato o riavviati gli altri servizi. La causa interna dello stallo resta aperta; questo caso non autorizza a riavviare il gestore durante una registrazione. Il censimento precedente che si dichiarava soltanto in lettura è rettificato in MS-248.

### Il laboratorio crea i nodi ma il client scade in Starting

Il primo client attendeva solo Running, Paused o Stalled. La misura del grafo senza link ha smentito quella precondizione. Il client corrente legge il profilo e restituisce Starting con audio_running false; il collaudo richiede Running soltanto dopo avere costruito il grafo. Il prototipo rimane distinguibile dal comando corrente.

### pw-cat restituisce 1 dopo avere scritto tutti i frame

Osservato sulla versione 1.6.2: il ramo sample_limit di on_process termina il loop senza impostare drained, mentre il main restituisce successo solo con quel flag. Il [sorgente ufficiale pw-cat 1.6.2](https://github.com/PipeWire/pipewire/blob/1.6.2/src/tools/pw-cat.c) riscontra il comportamento. L'eccezione del controllo vale solo per il registratore, codice 1, entrambe le versioni compilata e collegata 1.6.2, numero esatto di byte e log vuoto. File corto, log d'errore, altra versione o generatore fallito restano errori. Il generatore arriva a EOF senza sample_limit e termina 0. Cinque condizioni negative sono esercitate dalle prove del banco.

### Il mute non è zero nei primi buffer

La prima aspettativa richiedeva zero nell'intero file e ha fallito. L'analisi campione per campione mostra un transitorio molto attenuato e zero successivo; la [documentazione CamillaDSP 4.1.3](https://github.com/HEnquist/camilladsp/blob/v4.1.3/README.md) specifica la rampa predefinita del fader Main. La prova distingue intervallo iniziale e regime, conserva i valori reali e rifiuta sia un transitorio oltre il limite sia una perdita persistente. La soglia non viene semplicemente alzata per rendere verde la corsa.

### Il codice finale della pipeline nasconde un errore

Un comando laboratorio passato a tee aveva restituito timeout, ma la shell con il solo set -e aveva riportato 0 dalla pipeline. È stato rilevato leggendo l'output e corretto nelle esecuzioni successive con `set -euo pipefail`. Il codice finale e il rapporto interno vanno entrambi letti. Il trasferimento iniziale di script codificati nella riga di comando ha poi superato il limite Windows: il payload ASCII è ora passato su stdin a SSH e decodificato sul destinatario. Sorgente leggibile, impronta, output e risultato di ogni esecuzione sono conservati nel livello privato del progetto.

## Prove ancora necessarie

Il riavvio Ubuntu è stato collaudato nel nuovo accesso utente del 19 novembre. Restano una prova prolungata sotto carico DAW e la catena fisica scelta: quattro uscite effettive, latenza, rumore, guadagni e protezioni. Nessun valore della risposta dei driver o della stanza viene dedotto da questo banco virtuale. Il confronto di quantum e politica CPU deve usare quelle misure; i valori globali esistenti non sono stati cambiati per ottenere questo esito. Linger è no: questa configurazione non promette un DSP operativo prima del login.

## Correzioni della revisione finale

La versione corrente del banco è pipewire-bench-1.0.1, MS-257. La prima copia del banco dentro dsp-control-1.0.0 resta conservata ma superata. La revisione ha corretto tre percorsi non coperti dalle prime prove: rifiutare una pipeline già occupata non deve fermarla; codice 0 non autorizza una cattura corta; un errore di acquisizione non dimostra lo scambio dei lati. Undici prove del banco e sette del client passano, il revisore ha verificato le correzioni e il collaudo reale completo della nuova copia è riuscito. L'installatore corrente verifica otto file, lasciando fuori le due vecchie copie del banco preservate nella cartella di controllo.

Il banco richiede esattamente 288000 frame per ogni caso, anche se il registratore termina 0. Il controllo negativo accetta soltanto RoutingMismatch, cioè il tono sul lato estraneo, dopo aver verificato durata e integrità dei campioni. Il rifiuto della precondizione avviene prima di acquisire la pipeline e non invia mute o Stop. Questi controlli sono parte della validità dell'esperimento, non nuove prestazioni audio.
