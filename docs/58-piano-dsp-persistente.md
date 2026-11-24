# Piano di implementazione del DSP persistente

Stato documentale aggiornato il 2026-11-20: piano eseguito, conservato come storia dell'implementazione. Per installazione e prove effettive si usa [57-dsp-persistente.md](57-dsp-persistente.md), per uso e limiti correnti [61-camilladsp-manuale-tecnico.md](61-camilladsp-manuale-tecnico.md). Non rilanciare questo piano come se il servizio fosse ancora da preparare.

> Esecuzione autonoma richiesta dall'utente. Si applica la skill executing-plans, con lavoro in questa sessione e registro delle decisioni operative; commit e push restano manuali.

**Goal:** rendere disponibile un servizio DSP utente che riparta silenziato e in attesa, con un banco PipeWire a quattro canali verificabile senza connessioni fisiche automatiche.

**Architecture:** CamillaDSP ufficiale con backend PipeWire, unità systemd utente e client di progetto con operazioni limitate. Il profilo di laboratorio riusa i filtri già misurati su file e crea nodi con nomi separati. Nessuna configurazione di driver viene promossa a definitiva.

**Tech Stack:** CamillaDSP 4.1.3 PipeWire, Python 3, websockets 15.0.1 già presente, systemd utente e PipeWire 1.6.2 della macchina.

**Spec:** `docs/57-dsp-persistente.md`.

## Vincoli globali

Versione motore 4.1.3; archivio PipeWire amd64 con SHA-256 `04388dfbf0999732c51a972fa7c3dc7fa17437333124af7918022445c459851a`. API su `127.0.0.1:12341`, mute iniziale vero, guadagno -60 dB, nessuna configurazione caricata all'avvio. Laboratorio a 48000 Hz, due canali in ingresso e quattro in uscita. File remoti nuovi, nessuna sovrascrittura di configurazioni dell'utente e nessun cambio del dispositivo predefinito. Operazioni che richiedono una password o dati esterni restano dichiarate; le prove disponibili proseguono in autonomia.

## Punti di verifica

| Condizione | Comportamento richiesto |
|---|---|
| Profilo che raggiunge hardware | Rifiutato dal comando laboratorio prima delle richieste mutanti |
| Ripartenza dopo errore | Attesa, mute vero e -60 dB, senza riattivare il profilo precedente |
| Risposta API non riuscita | Errore esplicito e nessuna dichiarazione di caricamento riuscito |
| Stream o server non rispondente | Attesa limitata e rapporto del fallimento |
| Configurazioni o programmi già esistenti | Ispezione prima di modificare; installazione non distruttiva |

### Task 1: binario e controllo del motore

File: `config/camilladsp/laboratorio-pipewire.json`, `tools/monitor_dsp.py`, `tools/test_monitor_dsp.py`. Il client espone `rpc`, `validate_lab_config`, `load_lab` e `read_status`; importa la libreria di rete soltanto quando serve la connessione.

- [x] Scrivere e osservare fallire le prove del rifiuto dei profili hardware e del caricamento silenziato.
- [x] Implementare il controllo minimo e verificare errori API e ordine delle richieste.
- [x] Scaricare e verificare la variante PipeWire in una cartella nuova.
- [x] Ripetere sul binario scelto il collaudo offline già esistente.

### Task 2: servizio utente e ciclo di vita

File: `config/systemd/user/diy-monitor-dsp.service`, `config/camilladsp/monitor-dsp.sh`; procedura condivisa in `docs/10-ambiente/camilladsp-servizio-utente.md` dopo l'esecuzione. Si usano soltanto i nuovi percorsi del progetto nella home.

- [x] Installare sorgenti, profilo e unità senza sovrascrivere file esistenti.
- [x] Verificare il file di unità, avviare e abilitare il servizio dell'utente.
- [x] Leggere via API versione, stato inattivo, mute e volume; verificare l'ascolto locale.
- [x] Caricare il laboratorio senza link automatici e verificare nodi e porte reali.
- [x] Tornare in attesa e verificare la ripartenza con le condizioni iniziali.

### Task 3: segnale sul grafo e documentazione

File: `tools/collauda-dsp-pipewire.py`, rapporti privati del banco; pagine tecniche di progetto e blocco ambiente condiviso.

- [x] Generare e acquisire segnali soltanto fra i nodi espliciti del banco; interrompere se i nodi o i link non corrispondono.
- [x] Misurare canali, bande, volume e mute e separare queste prove dalla latenza fisica.
- [x] Ripristinare attesa e mute, chiudere soltanto i client creati dalla prova.
- [x] Aggiornare registro operativo, fonti, roadmap, memoria e ripresa, sincronizzare il blocco ambiente e verificare i risultati.

## Registro delle scelte operative

La prima ricognizione PulseAudio non è terminata; la successiva lettura nativa PipeWire con timeout ha risposto. Una successiva espressione Python passata fra virgolette Windows/SSH è stata spezzata prima dell'esecuzione: non è evidenza sulle dipendenze. Per gli script composti si usa trasporto del contenuto come file o byte codificati, con sorgente leggibile conservata nel progetto. Nessuna lettura fallita viene promossa a controllo superato.

Scelta operativa: la ricognizione completa con pw-dump non termina entro cinque secondi, pur avendo risposto la lettura del Core. Si conservano codici d'uscita e contenuto parziale e si prosegue con installazione del binario e controllo in attesa, che non dipendono da una pipeline audio. La prova del grafo resta aperta finché il problema non è risolto; il timeout non diventa un esito positivo.

## Esiti e scelte ulteriori, 2026-11-19

Task 1 completo: cinque prove iniziali, poi sette dopo il caso Starting/configurazione, mutazione del validatore rilevata. Binario PipeWire verificato e collaudo offline riuscito. Task 2 completo nel perimetro servizio utente: client corrente installato, sei link isolati osservati e ripartenza dopo guasto verificata. Task 3: tre casi sul segnale e mutazione reale riusciti, dati e procedure conservati; consolidamento e revisione finale in corso, quindi l'ultima casella resta aperta finché passano i controlli.

Ruling: Starting è un esito valido per profilo caricato senza link, con audio_running falso e configurazione riletta; Running è richiesto solo sul banco connesso. Motivo: osservazione reale del grafo. Costo se errato: falso esito di disponibilità; il collaudo del segnale resta distinto.

Ruling: accettare l'uscita 1 del solo registratore pw-cat 1.6.2 soltanto con condizioni complete in validate_exit. Motivo: sorgente della versione e file esatto osservati. Costo se errato: mascherare un errore; cinque casi negativi e verifica del segnale delimitano l'eccezione.

Ruling: il mute si misura con transitorio dichiarato e zero a regime, mantenendo un limite al transitorio iniziale. Motivo: rampa Main documentata e campioni reali. Costo se errato: sottostimare una perdita iniziale; nessuna connessione hardware è ammessa e la protezione fisica resta separata.

Ruling: installatore versionato aggiunto per ricostruire il setup da un clone, senza sorgenti solo nei payload privati. Motivo: requisito di documentazione riusabile. Costo: un piccolo strumento aggiuntivo, provato su home isolata e in sola verifica su quella operativa.

Ruling: il riavvio del solo WirePlumber è un ripristino osservato, non una diagnosi della causa interna. I processi diagnostici errati sono rimossi e la precedente dichiarazione read-only è rettificata. Nessuna cancellazione di stato o modifica dei profili hardware.

Revisione finale MS-257 conclusa: tre rilievi riprodotti e corretti con prove rosse/verdi; revisore ha riletto il delta senza residui. Banco corrente pipewire-bench-1.0.1, controllo1.0.0 invariato, entrambi verificati dall'installatore aggiornato. Nuova prova reale completa e mutazione riuscite; nessun rilievo rinviato nel perimetro esaminato. La durata e il motivo del controllo negativo sono ora invarianti separati; il banco rifiutato non acquisisce la pipeline.
