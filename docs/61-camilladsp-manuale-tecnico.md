# CamillaDSP: manuale tecnico del setup di progetto

Versione del documento: 2026-11-23. Motore qualificato nel laboratorio: CamillaDSP 4.1.3 su Ubuntu Studio. Questo è il riferimento tecnico per leggere e usare il setup già costruito; il [runbook di installazione e collaudo](10-ambiente/camilladsp-servizio-utente.md) conserva la sequenza eseguita e gli incidenti. Per il significato quotidiano partire dalla [guida breve](10-ambiente/camilladsp-uso-quotidiano.md); per le prove matematiche dal [confronto ingegneristico](62-confronto-crossover-e-verifica-matematica.md).

## Perimetro attuale e stato corretto

Requisito aggiornato ADR-051: l'ascolto senza PC è obbligatorio. Questo manuale descrive l'istanza PC già installata; il [progetto delle due modalità](63-sistema-autonomo-driver-e-collaudo.md) sviluppa anche Raspberry Pi, ingressi CD/analogici, clock e riuso dell'interfaccia. La modalità autonoma non è stata ancora installata su un Pi assente.

Il motore è un servizio dell'utente che resta disponibile per il controllo, senza aprire una pipeline finale all'avvio. Interrogazione SSH del 23 novembre dopo l'installazione manuale del pannello: versione 4.1.3, Inactive, mute true e volume_db -60.0. Inactive è lo stato della pipeline CamillaDSP; il servizio systemd che ospita il processo può essere contemporaneamente active/running. Il pannello HTTP è anch'esso active/running e non prepara automaticamente un profilo. Questa distinzione impedisce di interpretare l'attesa come un'installazione fallita o, all'opposto, il servizio attivo come audio già elaborato.

Nel setup è installato il pannello Mix/Ascolto di laboratorio, con controllo API e sorveglianza. Restano da qualificare profilo acustico definitivo, collegamento ai quattro jack e hardware. Il banco virtuale stereo verso quattro canali è già verificato, con sorgenti e registratore creati appositamente e collegamenti controllati.

## Componenti e percorsi

| Componente | Percorso relativo alla home Ubuntu | Ruolo |
|---|---|---|
| Motore | .local/opt/camilladsp-4.1.3-pipewire/camilladsp | Elaborazione e API locale |
| Servizio | .config/systemd/user/diy-monitor-dsp.service | Avvio dell'istanza e ripartenza |
| Comando corrente | .local/bin/diy-monitor-dsp | Client di progetto |
| Client versionato | .local/share/diy-2way-monitors/releases/dsp-control-1.0.0/ | Protocollo, validazione e comandi |
| Banco corrente | .local/share/diy-2way-monitors/releases/pipewire-bench-1.0.1/ | Generazione, routing, acquisizione e misure |
| Profilo dimostrativo | .config/diy-2way-monitors/camilladsp/laboratorio-pipewire.json | Solo laboratorio isolato |
| Prove dopo boot | electroacoustics/collaudi/postboot-20261119/ | Rapporti e acquisizioni già verificate |

Il precedente comando monitor-dsp resta un prototipo storico e non è il comando corrente. Le copie operative hanno origine da tools/monitor_dsp.py, tools/dsp_pipewire.py, tools/collauda-dsp-pipewire.py, tools/installa-dsp-utente.py e config/ del repository canonico. Le release sono separate per versione; l'installatore non aggiorna sovrascrivendo file già presenti.

## Avvio e accesso

L'unità configura --address 127.0.0.1 --port 12341 --wait --mute --gain=-60. Non passa un profilo o uno statefile che ripristini il precedente ascolto. La ripartenza da guasto ricrea quindi un motore in attesa silenziata, come provato nel collaudo del servizio. Non è un sistema completo di protezione contro errori di cablaggio, rotture o segnali inviati direttamente agli amplificatori.

L'API WebSocket ascolta soltanto su localhost. Non è una pagina web da aprire direttamente e non è esposta in rete locale. L'interfaccia CamillaGUI è un componente separato dell'ecosistema e non è stata installata qui. Il client usa la connessione locale del processo Python su Ubuntu, anche quando lo si invoca via SSH da Windows.

L'unità è abilitata per la sessione utente e Linger è no. La disponibilità dopo riavvio e nuovo accesso è stata verificata; non si promette esecuzione prima del login. Il comportamento futuro senza desktop o con Raspberry Pi dedicato richiederà una configurazione d'avvio e un collaudo propri.

## Comandi del client e loro effetti

| Comando | Effetto previsto dal sorgente verificato | Limite operativo |
|---|---|---|
| stato | Legge versione, stato, mute, volume e stop reason | Non cambia routing o profilo |
| silenzio | Imposta mute e rilegge lo stato | Il fader può avere una rampa; non è un sezionatore fisico |
| attesa | Imposta mute e -60 dB, invia Stop, richiede Inactive | Ferma la pipeline della nostra istanza |
| laboratorio | Valida e carica soltanto il profilo isolato 2/4 PipeWire, mantenendo mute e -60 | Non è l'ascolto dei monitor e non crea da solo i link di prova |

Questa tabella è un riferimento delle funzioni implementate, non l'invito a invocare tutte in sequenza durante una registrazione. L'unico comando necessario per leggere il setup è stato eseguito dalla postazione Windows con alias studio già configurato:

```powershell
cd E:\diy-2way-monitors-home
& 'C:/Windows/System32/OpenSSH/ssh.exe' -o BatchMode=yes -o ConnectTimeout=6 -o ConnectionAttempts=1 studio '.local/bin/diy-monitor-dsp stato'
```

Sulla macchina Ubuntu lo stesso client si esegue dal percorso nella tabella. Gli altri tre comandi e i relativi esiti sono documentati nel runbook delle prove del 19 novembre. Quel client installato non espone volume o profili: queste funzioni appartengono al nuovo pannello descritto sotto, collaudato il 23 novembre in un'istanza temporanea e consegnato per attivazione manuale.

## Configurazione, pipeline e ordine dei canali

Il banco descrive un ingresso stereo e quattro uscite logiche: woofer L, tweeter L, woofer R, tweeter R. Ogni cassa rimane un due vie. Mixer, filtri e pipeline sono oggetti distinti: il mixer distribuisce i canali, i filtri determinano trasferimenti e livelli, la pipeline stabilisce dove applicarli. La duplicazione di un lato verso due uscite distinte non è una somma di due segnali sullo stesso bus e non implica automaticamente +6 dB.

Il profilo scelto per la prova usa un LR4 a 2 kHz, volume di preparazione e autoconnect nullo. Il client ne verifica backend, nomi e gruppo dei nodi, due/quattro canali e assenza di agganci automatici prima di inviare richieste mutanti. I coefficienti e le frequenze del laboratorio non sono una raccomandazione per un tweeter reale.

Nel backend PipeWire i nodi devono essere collegati nel grafo. Il banco genera due canali, collega soltanto i propri processi verificati, acquisisce quattro canali e controlla il segnale. Un ACK di caricamento e uno stato Starting senza primi buffer non dimostrano un guasto o una misura audio riuscita: il rapporto distingue configurazione accettata e processamento effettivo.

Il protocollo 4.1.3 usato dal codice comprende GetVersion, GetState, GetMute, GetVolume, GetConfigJson, SetConfigJson, SetMute, SetVolume e Stop. Il programma controlla ACK e stato risultante; il protocollo generico non sostituisce le precondizioni del banco. Il [manuale WebSocket fissato alla versione](https://github.com/HEnquist/camilladsp/blob/v4.1.3/websocket.md) e il sorgente del client sono i riferimenti della sintassi, senza caricare esempi upstream su hardware non verificato.

## Volume, ritardi, EQ e headroom

Il volume -60 dB iniziale è un guadagno numerico del banco, non un SPL d'ascolto o un limite di potenza dei driver. Mute, volume software, guadagni analogici e potenza sono grandezze diverse. Nel collaudo il mute ha un transitorio iniziale molto attenuato prima dello zero a regime, coerente con la rampa Main; il rapporto conserva entrambi i valori.

I ritardi possono correggere un disallineamento misurato delle vie. La versione documentata prevede anche un'opzione subsample con approssimazione allpass; la sua accuratezza non va assunta costante su tutta la banda. Un ritardo del filtro e la latenza totale di acquisizione/riproduzione non sono la stessa misura. La prova attuale non qualifica cuffie per il musicista o monitoring a bassa latenza.

Qualunque aumento di EQ deve entrare nel budget dei livelli: controllo dei picchi digitali, capacità dei convertitori e dei finali, escursione e riscaldamento. Il motore non rende sicuro un boost arbitrario. La [dimostrazione ingegneristica](62-confronto-crossover-e-verifica-matematica.md) mostra un esempio sinusoidale, i limiti della maggiorazione e un controesempio di cancellazione acustica.

## Qualifica fisica prima dell'uso sui diffusori

Questa è una specifica delle verifiche future, non una sequenza di operazioni già eseguita sui diffusori. Prima della prima riproduzione reale occorrono risposta dei driver montati e geometria, progetto del crossover acustico, mappa fisica delle quattro uscite, taratura dei guadagni, verifica del cablaggio e delle protezioni, instradamento del player/DAW e controllo del ritorno da errore. Si partirà con livelli e condizioni di prova definiti per la catena reale.

Il profilo mix deve rappresentare il target scelto. Il profilo ascolto può cambiare la preferenza timbrica mantenendo il crossover e le condizioni dei driver; una modifica comune ai rami preserva il rapporto lineare fra essi sotto le ipotesi dimostrate. Volumi maggiori o estensione più profonda possono superare limiti fisici anche con un profilo matematicamente corretto. Il selettore software dei due profili è disponibile; non equivale alla loro taratura acustica.

Il carico DAW con registrazione e il monitoraggio cuffie richiedono un protocollo proprio. Il clock osservato è 48 kHz con quantum 1024; non lo si riduce per presumere una latenza migliore senza controllare dropout e carico. Un'eventuale uscita consumer separata deve avere routing e guadagni dichiarati, senza sdoppiare segnali o trattare le casse possedute come equivalenti ai driver progettati.

Il profilo di laboratorio contiene anche chunksize=256, verificato dal client. È un parametro della configurazione CamillaDSP distinto dal quantum osservato sul grafo PipeWire. La presenza dei due valori non costituisce una misura del ritardo totale: per il percorso hardware si dovranno rilevare configurazione attiva, clock e latenza effettiva insieme.

## Controlli e troubleshooting realmente osservati

| Sintomo | Distinzione o verifica utile | Evidenza/procedura |
|---|---|---|
| Servizio attivo, pipeline Inactive | Attesa iniziale prevista; leggere versione, mute e volume | Stato del 20 novembre e runbook |
| Starting dopo caricamento | In assenza di link può attendere il primo buffer | Rapporto del client separa audio_running |
| Attivazione riuscita ma audio non dimostrato | Servono grafo e campioni, non solo ACK | Banco PipeWire con acquisizione |
| pw-cat esce 1 dopo lunghezza esatta | Eccezione stretta per versione 1.6.2, log vuoto e registratore soltanto | Runbook e test del banco |
| Prime frazioni del mute non zero | Rampa Main; transitorio e regime misurati separatamente | Collaudo 19 novembre |
| Interrogazioni audio bloccate | Ripristino osservato di WirePlumber dopo diagnosi; non riavviare durante una registrazione | Troubleshooting del runbook |

Il collaudo automatico rifiuta una pipeline già occupata senza fermarla. Il cleanup riguarda soltanto risorse possedute dalla corsa. Non usare riavvii di servizio, kill o mute globale come risposta automatica a un errore durante lavoro musicale. Il dettaglio dei difetti corretti e dei controlli negativi è nel [deep dive didattico 4](../.claude/context/refactor-04-dsp-prove-e-proprieta.md).

## Controllo quotidiano completato e prove riproducibili

Aggiornamento del 23 novembre: implementati API reale, osservazione ALSA/clock, percorso PC PipeWire e pannello locale Mix/Ascolto. La qualifica fisica resta sospesa. Il progetto e il piano esecutivo sono in [piani/2026-11-23-controllo-ascolto.md](piani/2026-11-23-controllo-ascolto.md); la [consegna e procedura di avvio](../config/controllo-ascolto/README.md) distingue i comandi già collaudati dall'installazione persistente preparata per esecuzione manuale. Non viene modificato al boot un percorso musicale senza una preparazione esplicita.

### Architettura del software

Installazione manuale eseguita e verificata il 23 novembre, MS-317: 24 file coincidono con il manifesto trasferito, unità installata identica al kit, servizio active/running dopo 103,4 secondi e zero riavvii. Pagina, API e due font rispondono HTTP 200; stato atteso Inactive, mute true, -60 dB e nessun errore. La schermata fornita conferma il pannello di laboratorio pronto per la preparazione, senza audio abilitato. Il [rapporto di installazione](../research-vault/sistema-autonomo-20261120/risultati-installazione-controllo.json) conserva impronte e perimetro della verifica. L'avvio automatico ai prossimi accessi è ancora disabled: dopo questa verifica l'utente può eseguire `systemctl --user enable diy-listening-control.service` e controllare `systemctl --user is-enabled diy-listening-control.service`. Nessuna prova di riavvio o qualifica hardware viene dedotta dall'avvio corrente.

| Modulo | Responsabilità e prova |
|---|---|
| controllo_ascolto.py | Prepare, enable, mute e perdita di qualifica; dodici test, inclusi default canonici e caricamento differito. |
| ascolto_alsa.py | Manifest, profili attestati, identità USB, parametri PCM e controlli clock; undici test. |
| ascolto_pipewire.py | Laboratorio isolato oppure grafo PC attestato, card ALSA del sink e soli link dichiarati; nove test. |
| pannello_ascolto.py | Peer WebSocket reale, sessione, watchdog e HTTP locale; tredici test di sessione/API, inclusi richieste estranee e perdita di comunicazione. |
| collauda-controllo-ascolto.py | Motore reale temporaneo, HTTP/WebSocket e misura di quattro PCM; rapporto e hash, due frequenze. |
| test_collaudo_controllo.py | Mutazioni dei risultati reali per verificare che il controllo del rapporto respinga un falso verde. |
| collauda-pannello-browser.py | Edge reale sulla pagina corrente, font e controlli desktop/mobile; peer simulato, non prova audio. |

I sorgenti sono sotto tools; pagina e configurazioni sotto config/controllo-ascolto. Il runtime usa Python e websockets 15.0.1 già disponibile su Ubuntu. Non è stato aggiunto un secondo client con dipendenze diverse: WebSocketPeer riusa RpcPeer. Il server HTTP è limitato a 127.0.0.1, con token di sessione sui POST, controllo Host/Origin, schema di azioni ristretto e nessuna RPC o lettura di file arbitraria dal browser. Il token protegge il percorso browser; non autentica l'API CamillaDSP verso altri processi locali.

### Sequenza, stati e motivazioni

1. Prepare convalida versione 4.1.3, profilo richiesto e istanza precedente. Una configurazione estranea non viene sostituita. ValidateConfigJson restituisce la forma canonica; la policy la ricontrolla. Vengono impostati mute e -60 dB e riletti entrambi. SetConfigJson è asincrono: GetConfigJson deve coincidere entro due secondi, altrimenti la preparazione fallisce.
2. Sul PC qualificato vengono risolti nodi e porte attestati. Il binder aggiunge solo i collegamenti attesi mancanti, a segnale mutato; non rimuove link di altre applicazioni. Un collegamento estraneo causa errore e revoca della preparazione. I canali delle cuffie non appartengono alle quattro uscite gestite.
3. Avvia ascolto è esplicito: motore Running, configurazione canonica identica, rate, identità, routing e clock coerenti. Il fader Main controlla tutte le vie insieme. Il livello richiesto deve essere finito e compreso in [-60,-6] dB: non è una calibrazione SPL.
4. Silenzia mantiene una preparazione valida ma imposta mute e -60 dB. Un guasto revoca invece la preparazione. Il watchdog interroga il percorso ogni 250 ms, con periodo effettivo dipendente dalle letture e dai timeout. Il ritorno del clock o della rete non riattiva automaticamente l'audio.
5. Se una RPC di mute fallisce, lo stato visibile indica mute non confermato; il tentativo viene ripetuto quando la comunicazione torna. La chiusura ordinata/SIGTERM tenta di silenziare solo la configurazione posseduta. SIGKILL, crash dell'host e transitori richiedono protezioni e qualifica fisica: non esiste una garanzia elettrica derivata dal solo watchdog.

### ALSA diretto sul Pi e PipeWire sul PC

Il manifest privato lega profili normalizzati e prova di qualifica con SHA-256. La prova deve contenere routing fisico e catena del volume verificati e gli stessi campi di identità, PCM, clock e profili. verified true da solo non basta. Gli hash rilevano modifiche incoerenti: chi può riscrivere prova e manifest può riattestarli, dunque non sono firme di autenticazione.

AlsaObserver legge card ID stabile, VID/PID USB e hash del seriale, oppure una porta USB fisica attestata se il dispositivo non espone seriale. Nel secondo caso si identifica modello e porta, non un esemplare unico; la sostituzione sulla stessa porta richiede nuova qualifica. Legge procfs per formato/canali/rate e amixer cget per controlli già censiti. Non scrive controlli ALSA e non presume che un clock presente abbia il rate corretto. Per clock esterno servono source, lock e rate attestati; per interno la sorgente attestata e i parametri PCM. Gli alias dei formati kernel/Camilla sono confrontati esplicitamente.

Il Pi con ALSA diretto richiede cattura e playback aperti e coerenti; il candidato seleziona due sorgenti nel PCM multicanale e mappa solo le quattro vie alle uscite fisiche. Il PC qualificato usa cattura stereo PipeWire e quattro porte logiche; il manifest può attestare il solo PCM playback così la cattura fisica non deve essere aperta quando non si registra. Il sink PipeWire deve appartenere alla stessa card osservata; gli ID variabili vengono risolti dai nomi stabili attestati ad ogni lettura. Grafo richiesto: due collegamenti in ingresso e quattro in uscita, nessun altro link che tocchi i nodi DSP o le porte fisiche riservate alle quattro vie. Anche un altro player collegato direttamente a una di queste porte revoca la preparazione; i collegamenti alle porte cuffie separate restano ammessi.

Il laboratorio PipeWire è distinto: sono ammessi soltanto generatore, DSP e registratore virtuali del banco. autoconnect null non protegge da collegamenti manuali: anche il laboratorio controlla il grafo effettivo. Nessuna mappa example abilita oggi l'interfaccia acquistabile o il Pi; restano verified false e i controlli clock non sono inventati.

### Prova reale e risultati conservati

La prova è stata eseguita via SSH su Ubuntu con istanza distinta dal servizio principale, due rate 44,1/48 kHz, due toni per lato e uscita a quattro canali float32. Si misura un passo da -24 a -18 dB, con errore ammesso inferiore a 0,1 dB su ciascuna via. Ogni banda deve ricevere segnale utile; RMS minimo maggiore di 0,000001. I mute iniziale, manuale, dopo perdita software del clock e dopo SIGTERM devono avere RMS inferiore a 0,00000001. Si verifica anche il cambio Mix/Ascolto e il rifiuto del ripristino senza nuova preparazione.

I valori effettivi e l'ambiente sono nel [rapporto corrente](../research-vault/sistema-autonomo-20261120/risultati-controllo.json), insieme a hash delle sorgenti e del binario. Il guasto clock è un predicato software iniettato nel banco file: non simula elettricamente la perdita S/PDIF. I candidati ALSA e PC vengono soltanto normalizzati dal parser reale con ReadConfigJson, senza caricarli. Il servizio principale è stato riletto prima/dopo in stato Inactive, mute true e -60 dB; i temporanei sono rimossi. La prova browser usa la pagina effettiva a 1280/390 px, font caricati e nessun overflow; i due PNG sono stati ispezionati ed eliminati.

```powershell
python tools/test_controllo_ascolto.py
python tools/test_ascolto_alsa.py
python tools/test_ascolto_pipewire.py
python tools/test_pannello_ascolto.py
python tools/collauda-controllo-ascolto.py --ssh studio
python tools/collauda-controllo-ascolto.py --check
python tools/test_collaudo_controllo.py
python tools/collauda-pannello-browser.py --check
```

Gli ultimi due controlli di rapporto non aprono periferiche. Il collaudo SSH usa il binario già presente e non installa dipendenze. Il [deep dive 8](../.claude/context/refactor-08-controllo-ascolto.md) spiega i difetti trovati nel passaggio da peer finto a motore reale e i limiti della qualifica. Tutte le verifiche fisiche dell'utente rimangono sospese in PA-041.

## Provenienza, backup e riferimenti

Il setup CPU/CAD/DSP/MIDI e il kit hanno un backup finale riletto il 19 novembre, con copia esterna verificata e rotazione conclusa il 20. Non avviare un altro punto per il solo fatto di consultare questo manuale; la conservazione locale è quattro e una quinta corsa richiede riesame. Il registro dei [microstep](OPERATIONS-LOG.md), il [runbook backup](10-ambiente/backup-finale-setup-2026-11.md) e l'[indice ragionato](INDICE-RAGIONATO.md) distinguono sorgenti, procedure e prove private.

Fonti software: [README 4.1.3](https://github.com/HEnquist/camilladsp/blob/v4.1.3/README.md), [backend PipeWire](https://github.com/HEnquist/camilladsp/blob/v4.1.3/backend_pipewire.md), protocollo e sorgenti del progetto. I risultati numerici del banco derivano dai rapporti locali, non da un esempio prestazionale pubblicato upstream. Nessuna misura acustica, di fruscio o di latenza hardware viene dedotta dall'installazione riuscita.

Fonti primarie della nuova implementazione, identificate nel [pedigree](90-riferimenti/fonti-progetto.md):

- SRC-CAMILLADSP-WEBSOCKET-4-1-3: [protocollo del tag](https://github.com/HEnquist/camilladsp/blob/v4.1.3/websocket.md), richieste di lettura/validazione e controllo del Main.
- SRC-CAMILLADSP-SOCKETSERVER-4-1-3: [socketserver.rs](https://github.com/HEnquist/camilladsp/blob/v4.1.3/src/socketserver.rs), lettura mirata delle branche ReadConfigJson, ValidateConfigJson e SetConfigJson. La prima normalizza senza aprire hardware; la validazione può interrogarne le capacità, quindi i candidati vengono soltanto letti finché non qualificati.
- SRC-CAMILLADSP-ALSA-4-1-3: [backend ALSA](https://github.com/HEnquist/camilladsp/blob/v4.1.3/backend_alsa.md), distinzione card/device/subdevice, nomi e formati.
- SRC-KERNEL-ALSA-PROC: [procfs ALSA](https://docs.kernel.org/sound/designs/procfile.html), significato di id e hw_params; sostiene il confronto dei parametri effettivi.
- SRC-ALSAUTILS-AMIXER-1-2-14: [amixer.1](https://github.com/alsa-project/alsa-utils/blob/v1.2.14/amixer/amixer.1), cget e selezione della card, senza scritture ai controlli.
- SRC-2AFD8DC105BFCA8A e SRC-PIPEWIRE-PW-LINK: [dump JSON](https://docs.pipewire.org/page_man_pw-dump_1.html) e [creazione dei link per ID](https://docs.pipewire.org/page_man_pw-link_1.html). La documentazione online letta riporta 1.6.11; il sistema osservato usa 1.6.2. Il codice riusa i comandi già collaudati sul sistema, senza equiparare le versioni.
- SRC-KERNEL-USB-SYSFS-7: [sorgente sysfs USB](https://github.com/torvalds/linux/blob/v7.0/drivers/usb/core/sysfs.c), attributi VID/PID/seriale e assenza del seriale se non fornito. La [pagina ABI stabile](https://github.com/torvalds/linux/blob/v7.0/Documentation/ABI/stable/sysfs-bus-usb), SRC-KERNEL-USB-ABI-7, è stata letta come ricerca preliminare: documenta altri attributi e non viene usata come prova dei tre campi di identità.
