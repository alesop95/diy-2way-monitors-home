# Controllo di ascolto PC/Pi: progetto e piano esecutivo

Per l'esecuzione si applica executing-plans in questa sessione, con prove prima del codice. L'utente ha già richiesto di completare il lavoro autonomamente: nessuna nuova approvazione di progetto o verifica fisica viene richiesta. Commit e push restano manuali.

## Obiettivo e specifica

Completare il software mancante del controllo DSP: collegamento API reale, osservazione ALSA/clock, selezione dei profili e interfaccia quotidiana locale. Specifica funzionale già nei capitoli [61](../61-camilladsp-manuale-tecnico.md) e [63](../63-sistema-autonomo-driver-e-collaudo.md). Tutto il software può essere sviluppato qui; la qualifica dell'interfaccia/Pi e dei jack resta fisica e sospesa per ADR-055.

Scelte implementative dell'esecutore: Python 3 e websockets 15.0.1 già presente su Ubuntu, RpcPeer esistente, server HTTP della libreria standard e pagina locale con design Intrawelt. Il pannello offre stato, profilo Mix/Ascolto, volume comune e mute. Non installa librerie Windows o servizi privilegiati. Il catalogo del template è stato interrogato: nessun pacchetto pertinente al controllo CamillaDSP; Craft è già adottato per gli artefatti, gli altri risultati della ricerca non coprono questo requisito.

## Contratto del controllo

- Default silenziato a -60 dB; nessun ripristino automatico del vecchio livello.
- Prima di caricare: convalida del profilo, versione 4.1.3, istanza propria e normalizzazione tramite ValidateConfigJson. La configurazione torna in forma canonica con i default del motore; il caricamento è asincrono e richiede rilettura con scadenza.
- Abilitazione soltanto con motore Running, configurazione canonica esatta, identità, rate, routing e clock coerenti. Limite di sviluppo del volume [-60,-6] dB, senza pretesa di calibrazione SPL.
- Backend file di laboratorio come default. Estensione ALSA tramite policy separata e manifest privato di qualifica, hash dei profili e prova attestata; l'esempio verified false non abilita hardware.
- Adapter ALSA in sola lettura: identità USB da sysfs, card ID stabile, parametri PCM correnti da procfs, controlli del clock censiti nel manifest tramite amixer cget. Nessun numid o nome di controllo inventato, nessun amixer cset.
- Perdita di condizioni o comunicazione: tentativo di mute e riduzione del volume, errore conservato se la RPC non riesce, nuova preparazione/abilitazione esplicita dopo il recupero. Un tentativo software non equivale a silenzio fisico garantito.
- HTTP su 127.0.0.1, token di sessione per POST, controllo Host/Origin e profili locali già dichiarati; nessun caricamento arbitrario da browser. Accesso remoto mediante tunnel SSH, non esposizione automatica sulla LAN.
- PCM, FIFO e immagini QA temporanei eliminati in finally. Un rapporto corrente con hash e misure, nessuna cartella per ogni tentativo o pagina PDF.

## File e responsabilità

In revisione è emersa una condizione aggiuntiva: `autoconnect_to: null` impedisce l'autocollegamento, ma non un collegamento manuale successivo. Il laboratorio PipeWire deve sorvegliare il grafo reale; il percorso PC qualificato deve attestare anche nomi di nodi/porte e legare il sink alla stessa card ALSA osservata. Riutilizzo di dsp_pipewire, nessuna nuova libreria. Collegamenti creati soltanto a profilo silenziato, nessuna rimozione di link di altre applicazioni. Sul PC si può qualificare il solo PCM playback, lasciando chiusa la cattura fisica quando non si registra; sul Pi ALSA diretto restano richiesti entrambi i flussi. Le cuffie restano fuori dalle quattro destinazioni attestate. Questa estensione si sviluppa con fixture negative; la mappa fisica resta non qualificata.

La revisione è svolta dall'esecutore: la regola locale `.claude/rules/token-economy.md` vieta di delegare revisione e progettazione. Nessun subagent avviato per questo giro.

| File | Responsabilità |
|---|---|
| tools/controllo_ascolto.py | Macchina a stati e convalida della configurazione canonica, riusata dal pannello. |
| tools/ascolto_alsa.py | Manifest/policy e osservatore Linux, parsers verificabili senza periferiche. |
| tools/ascolto_pipewire.py | Grafo virtuale isolato e percorso PC attestato, sink legato alla card, binder di soli collegamenti dichiarati. |
| tools/pannello_ascolto.py | Peer WebSocket, sessione, sorveglianza e API HTTP locale. |
| config/controllo-ascolto/ | Pagina del pannello, profili dichiarati, manifest example e avvio non abilitante. |
| tools/collauda-controllo-ascolto.py | Motore reale separato su FIFO/file, richieste HTTP/WebSocket e misure audio; esecuzione locale Linux o orchestrata via SSH. |
| tools/test_controllo_ascolto.py e suite delle due estensioni | Contratti, perdite di condizioni, manifest non valido e richieste browser respinte. |
| docs/STATO-PROGETTO.md e mappa artefatti | Percorso preciso ai report tecnici e alle viste delle simulazioni, senza un nuovo riepilogo concorrente. |

## Esecuzione e prove

- [x] Riprodurre il limite del nucleo con configurazione normalizzata e caricamento differito; test rosso, correzione e regressioni precedenti verdi.
- [x] Scrivere prove per identità/rate/clock/routing ALSA, hotplug e manifest non qualificato; implementare osservatore e policy, senza aprire hardware.
- [x] Scrivere prove per sessione e HTTP: preparazione muta, abilitazione esplicita, perdita clock/config, profilo estraneo, CSRF e input non ammessi; implementare pannello e sorveglianza.
- [x] Collaudare contro CamillaDSP 4.1.3 reale in istanza separata: FIFO alimentata a ritmo audio, quattro canali su file, cambi di volume/mute/profilo e guasto controllato. Misurare l'uscita, non solo ACK. Conservare rapporto e hash, rimuovere i temporanei.
- [x] Verificare il pannello con il browser e la pagina effettiva; eliminare lo screenshot QA dopo l'ispezione.
- [x] Collegare report CPU/CAD/DSP/MIDI/backup e viste 3D/grafici ai documenti esistenti. Aggiornare manuale, stato, residui e fonti distinguendo software implementato da hardware non qualificato.
- [x] Ripetere i controlli pertinenti e il gate completo, aggiornare memoria/ripresa e messaggio proposto. Nessun commit automatico.

Esito: gate completo con codice 0 e 28 controlli propri verdi, rapporto _notes/chiudi-autonomia-20261120.txt. Software verificato nel perimetro dichiarato; installazione persistente manuale e qualifica fisica sono distinte. Quarantasei metodi coprono il controllo, oltre al banco audio e al browser. Kit estratto con verifica di 24 file e mutazione rilevata, estrazione temporanea rimossa. Fonti, report, figure, PDF e catalogo hanno controlli di coerenza registrati; nessun add/commit/push/deploy eseguito.

## Rischi da esercitare nella revisione

La risposta API contiene default assenti dal file richiesto; il controllo deve confrontare la forma canonica. Un ACK non implica modifica già applicata. Un clock presente con rate errato non qualifica ascolto. La scheda può scomparire o cambiare indice; l'identità non è il solo numero di card. Un file attestato ma cambiato non può essere caricato. Un errore mute non va nascosto. La chiusura del pannello deve tentare l'attesa silenziata soltanto sulla sessione gestita. I casi sintetici non sostituiscono la misura dei jack o dei transitori.

## Fonti primarie lette per questa estensione

README, websocket.md, socketserver.rs e backend_alsa.md del tag v4.1.3 di CamillaDSP. Lettura mirata: ValidateConfigJson/ReadConfigJson, configurazione asincrona, RawFile/FIFO e parametri ALSA. L'osservatore procfs/sysfs richiede anche la documentazione ALSA/kernel pertinente; copertura e punti d'uso saranno registrati nel pedigree, senza dichiarare letto tutto il repository.
