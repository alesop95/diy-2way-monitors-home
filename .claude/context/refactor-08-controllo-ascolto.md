# Dal nucleo finto al controllo del motore reale

L'utente chiede di completare il controllo di ascolto e ritrovare ogni passaggio. Il risultato è il [manuale 61](../../docs/61-camilladsp-manuale-tecnico.md), con runtime comune PC/Pi e prove che distinguono contratto software, motore audio, browser e qualifica fisica. La decisione è ADR-057; la cronologia è MS-308 e successivi. Nessuna verifica fisica è riaperta.

## Com'era e dove la prova era debole

Il nucleo passava dieci regressioni su un peer che restituiva esattamente il JSON appena inviato. Il motore reale aggiunge default e applica SetConfigJson in modo asincrono. Confrontare subito il file richiesto con la configurazione attiva confondeva tre oggetti: richiesta, configurazione canonica e stato effettivamente caricato. Un test verde sul peer non copriva questa differenza.

Anche un profilo PipeWire senza autoconnect non garantisce isolamento: un collegamento manuale può raggiungere l'hardware. Una card con indice numerico corretto può essere un dispositivo diverso dopo hotplug. Un valore lock presente non dimostra che il rate sia quello del profilo. Infine un ACK di mute non è una misura di silenzio all'uscita.

## Il salto: canonicalizzare, rileggere e osservare

Controller.prepare valida ingresso e configurazione precedente prima di modificarli, chiede ValidateConfigJson e controlla la forma canonica. Porta mute e volume in attesa, invia la configurazione e attende GetConfigJson identico con scadenza. Enable richiede anche Running e un'Observation coerente. Il ritorno del clock non riattiva il livello: occorrono nuova preparazione e gesto esplicito.

AlsaPolicy lega manifest, prova fisica e hash dei profili; AlsaObserver legge la scheda corrente, procfs e controlli censiti. Un seriale viene conservato solo come hash; in assenza di seriale, la porta USB attestata ha il limite dichiarato di identificare modello/porta, non l'esemplare. Il PC può attestare il solo playback quando la cattura hardware è chiusa. ALSA diretto richiede entrambi i flussi.

PipeWirePolicy e PipeWireObserver richiedono sei collegamenti esatti e un sink appartenente alla card osservata. La prima versione della guardia confrontava le sole coppie di porte: una mutazione con nodo incoerente passava. La prova ha imposto di verificare anche gli estremi nodo/porta. Il binder aggiunge solo i link dichiarati mancanti a profilo mutato; non ripara il grafo cancellando link altrui. La revisione conclusiva ha aggiunto il rifiuto di altri player sulle porte fisiche riservate: controllare solo gli archi che toccano i nodi DSP lasciava passare un bypass. La nuova prova era rossa; la guardia ora controlla anche le destinazioni riservate, lasciando le altre porte cuffie indipendenti. La guardia del laboratorio riusa dsp_pipewire e rifiuta l'uscita verso hardware.

## Difetti che hanno cambiato l'implementazione

| Evidenza osservata | Correzione e motivo |
|---|---|
| Timeout del caricamento sul banco FIFO | Keeper FIFO aperto, produttore a ritmo audio e stop ordinato. Il banco non deve introdurre un blocco che non appartiene al DSP. |
| Tweeter quasi privo di segnale con un solo tono basso | Due toni per lato e RMS minimo in ogni via: il rapporto di volume non deve confrontare rumore numerico. |
| Passo volume misurato 6,1137 dB, oltre 0,1 dB ammessi | La finestra era indicizzata sui campioni inviati in FIFO. Il produttore può precedere l'uscita; ora gli indici derivano dai frame realmente scritti nel file PCM. La tolleranza resta invariata. |
| Default mute/scale null nel parser reale | Accettati i default neutri, mantenuto il rifiuto del mute attivo nelle righe di routing. |
| Mute non confermato durante perdita RPC | Stato distinto e ritentativo al recupero; niente falso stato silenziato o ripristino del volume. |
| Perdita identità durante una nuova preparazione | Hold immediato sulla sessione già posseduta, prima dell'errore. |
| HTTP 403 con reset TCP su Windows | Consumo del body limitato prima della risposta. Nessun retry nel test per nascondere il difetto. |
| Test browser verde senza motore audio | È una prova UI separata. Il banco reale misura i PCM e il rapporto lega ogni misura alle sorgenti. |

## Quanto dimostra ogni livello

Quarantasei metodi di test coprono nucleo, policy ALSA, grafo PC, sessione/HTTP e mutazioni del rapporto reale. Il motore Ubuntu viene esercitato a 44,1 e 48 kHz, quattro canali, passo volume, mute, cambio profilo, perdita di una condizione software e SIGTERM. Il browser usa la pagina corrente a 1280 e 390 px, con font e controlli verificati. File PCM, FIFO, profili browser e PNG QA sono temporanei ed eliminati.

Il rapporto conservato è [risultati-controllo.json](../../research-vault/sistema-autonomo-20261120/risultati-controllo.json). I suoi hash permettono di rilevare che una misura appartiene a codice diverso da quello corrente. I controlli mutano il rapporto vero e devono respingere gain errato, mute rumoroso, rate duplicato, assenza di segnale e sorgenti diverse. Questo non costituisce una firma contro chi riscrive tutti i file.

La qualifica ARM/USB, i jack, il vero clock S/PDIF, le cuffie, il carico DAW e le protezioni elettriche restano sospesi. Una sorveglianza periodica con RPC e subprocess non è una protezione a latenza garantita. Il costo della soluzione è mantenere un manifest attestato per ciascun percorso e rifare la qualifica quando cambiano cablaggio, profili o identità; il vantaggio è rendere osservabile che cosa autorizza l'ascolto.

## Rilettura e riproduzione

Il [piano](../../docs/piani/2026-11-23-controllo-ascolto.md) elenca i passi e i controlli; [README della consegna](../../config/controllo-ascolto/README.md) separa prove eseguite e installazione manuale. Il kit è prodotto da consegna_controllo.py, non spedito o attivato automaticamente. Le fonti del protocollo, del parser, ALSA e PipeWire sono nel pedigree con copertura mirata e punti d'uso, senza dichiarare letto l'intero repository upstream.
