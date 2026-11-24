# DSP persistente: architettura del banco di prova

Specifica del 2026-11-19, eseguita nell'autonomia richiesta dall'utente. Il requisito è preparare CamillaDSP per la coppia di monitor attivi a due vie, con quattro canali complessivi, senza presentare il crossover dimostrativo come taratura finale e senza collegare automaticamente le uscite fisiche. La scheda audio attuale non è il dispositivo multicanale previsto dal progetto.

## Scelta del percorso

Il binario già collaudato su file include ALSA; per creare nodi nel grafo audio si sceglie il rilascio ufficiale PipeWire della stessa versione 4.1.3. Questo usa il server PipeWire già presente e consente un banco di laboratorio isolato dai connettori fisici. Il percorso ALSA resta utile per un'eventuale configurazione dedicata futura; la variante PulseAudio aggiungerebbe un livello di compatibilità non necessario per questo banco. Si misura il comportamento reale del binario scelto, invece di dedurlo dal nome del pacchetto.

Il server viene eseguito come servizio dell'utente, con API locale su `127.0.0.1:12341`, avvio in attesa di configurazione, mute attivo e guadagno iniziale -60 dB. Non usa un file di stato che riattivi una vecchia configurazione. La scelta -60 dB è un valore digitale iniziale del banco e non una taratura del livello acustico o una soglia di protezione dei driver. All'avvio non viene aperta una pipeline audio.

Il profilo di laboratorio crea cattura stereo e riproduzione a quattro canali, con nomi propri del progetto, gruppo comune e `autoconnect_to` nullo su entrambi i lati. La mappa è L basso, L alto, R basso, R alto. Il filtro LR4 a 2 kHz resta un esempio per il collaudo. L'interfaccia di comando espone stato, silenzio, caricamento del solo laboratorio validato e ritorno in attesa; le prove possono usare il protocollo completo solo sui nodi di laboratorio verificati.

## Prove richieste

| Aspetto | Evidenza necessaria |
|---|---|
| Binario | Archivio ufficiale e SHA-256, backend effettivi e collaudo su file |
| Avvio | Servizio attivo e interrogabile, stato inattivo, mute vero, volume -60 dB |
| Esposizione | Ascolto esclusivamente su localhost |
| Configurazione | Il controllo rifiuta backend fisici e collegamenti automatici prima di inviare una richiesta |
| Laboratorio | Due nodi, due canali in ingresso e quattro in uscita, senza link all'hardware |
| Segnale | Stimoli e uscita misurati sui soli nodi del banco, con ordine e bande verificati |
| Ripartenza | Ritorno in attesa con mute e guadagno iniziali e senza nodi residui del banco |
| Convivenza | Dispositivo predefinito e collegamenti preesistenti non vengono cambiati |

Un servizio soltanto attivo non dimostra la separazione dei canali o la prestazione audio. La risposta acustica, il cablaggio fisico, la latenza per il musicista e i limiti di livello richiedono la catena reale. L'impostazione di quantum esistente viene registrata e non è sostituita da un'ipotesi di bassa latenza.

## Implementazione e fonti

Il piano è in [58-piano-dsp-persistente.md](58-piano-dsp-persistente.md). Il protocollo applicativo viene dalla [documentazione WebSocket CamillaDSP 4.1.3](https://github.com/HEnquist/camilladsp/blob/v4.1.3/websocket.md), i nodi dal [backend PipeWire della stessa versione](https://github.com/HEnquist/camilladsp/blob/v4.1.3/backend_pipewire.md). Il client usa la libreria [websockets 15.0.1](https://websockets.readthedocs.io/en/15.0.1/reference/sync/client.html) già rilevata sul sistema. Le procedure operative saranno aggiornate con i soli comandi realmente eseguiti e con i rispettivi risultati.
