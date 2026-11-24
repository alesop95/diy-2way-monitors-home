# Collaudo offline del crossover digitale

## Piano operativo del 2026-11-18

Scopo: verificare sul vero motore CamillaDSP la trasformazione stereo in quattro vie prima dell'acquisto dell'interfaccia. Specifica di riferimento: architettura di ADR-033, ADR-045 e ADR-047, descritta in `docs/54-amplificazione-e-dsp.md`. È un collaudo sui campioni digitali, distinto dalla misura del diffusore, dalla latenza e dalla stabilità di Ubuntu. L'utente ha chiesto di proseguire il lavoro indipendente dallo schermo, che non è urgente.

L'esecuzione resta nella sessione principale. Il binario ufficiale portabile è conservato sotto `_notes/`, con versione e impronta verificate, e non viene installato nel sistema. La configurazione di laboratorio usa soltanto ingresso e uscita su file. I percorsi dei file sono relativi a una cartella di prova creata dallo strumento; non si apre una periferica audio. Commit e pubblicazione restano manuali.

| Passo | Prodotto | Criterio di verifica |
|---|---|---|
| Prova prima della configurazione | `tools/collauda-camilladsp.py` | Fallisce se il file di configurazione manca |
| Configurazione di laboratorio | `config/camilladsp/offline-lr4.json` | Il motore la valida e produce quattro canali |
| Ordine dei canali | Sinistro basso/alto, destro basso/alto | Toni separati su L e R non si spostano sull'altro lato |
| Filtri elettrici | LR4 a 2000 Hz, 48 kHz | Circa -6,02 dB su ciascuna via a 2000 Hz, somma elettrica di modulo unitario |
| Bande distanti | Toni a 100 e 8000 Hz | La via esclusa attenua di almeno 40 dB rispetto all'ingresso |
| Volume e mute | Tre corse normali, attenuate e silenziate | -6 dB su tutte le vie; mute a zero |
| Controllo della prova | Configurazioni mutate nella cartella privata | Scambio dei lati e filtro sbagliato devono far fallire il collaudo |

Si accettano soltanto processi conclusi con esito positivo, file non vuoti, numero di canali corretto e misure entro tolleranza. Un file YAML/JSON sintatticamente valido non dimostra il comportamento dei filtri. Le mutazioni non cambiano il file sorgente e non riguardano configurazioni della macchina.

La frequenza di laboratorio non definisce il crossover finale; il modello non contiene taratura dei driver, limitatori di potenza, compensazione del baffle, allineamento dei centri acustici o correzione della stanza. Non va collegato ai tweeter come configurazione operativa.

## Esito del 2026-11-18

Collaudo riuscito con CamillaDSP 4.1.3 su Windows e sulla macchina Ubuntu Studio via SSH. La prova Linux si è svolta in una cartella temporanea nuova, senza installare il programma, avviare servizi o aprire dispositivi audio. L'archivio Windows è stato verificato contro SHA-256 `d949de5ac5fc13282dd47155e0ac67087c09dd84baf7c7d568616bfc6e43d190`; quello Linux contro `55f5ec2ed80fcc79a543672f9f89ace4557d290d80584ef31ee0442111bd0b11`, entrambi dichiarati dal rilascio ufficiale.

| Prova digitale | Esito osservato su Ubuntu |
|---|---|
| Canali | L basso, L alto, R basso, R alto; segnale sul lato corretto |
| Incrocio a 2000 Hz | -6,0206 dB per entrambe le vie |
| Tono a 100 Hz nella via alta | -78,18635 dB rispetto all'ingresso del test |
| Tono a 8000 Hz nella via bassa | -51,38427 dB rispetto all'ingresso del test |
| Somma delle due vie | Circa 0 dB ai tre toni di prova: 100, 2000 e 8000 Hz |
| Volume iniziale a -6 dB | Applicato su tutti i canali, entro la tolleranza di 0,12 dB |
| Mute | Picco digitale 0 su 86400 frame |
| Lati invertiti deliberatamente | Prova fallita con «Canali L/R errati» |
| Passa alto sostituito da passa basso | Prova fallita sulla somma a 100 Hz |

Le misure dei due sistemi coincidono alla precisione di cinque decimali del rapporto; non è stato confrontato ogni byte dei file PCM. L'attenuazione misurata riguarda il segnale digitale sintetico a 16 bit e i filtri, non il rumore dell'interfaccia. Non sono state misurate risposta acustica, tenuta dei driver, ritardo completo o xruns.

Fonte tecnica: [documentazione della versione CamillaDSP 4.1.3](https://github.com/HEnquist/camilladsp/blob/v4.1.3/README.md), sezioni File, BiquadCombo, Mixer e opzioni della riga di comando. I rapporti e gli archivi verificati restano nel livello privato del progetto.

## Sequenza replicabile verificata

Dalla radice del repository su Windows, dopo aver scaricato e verificato il binario ufficiale portabile nella cartella indicata:

```powershell
python tools/collauda-camilladsp.py --bin _notes/camilladsp-v4.1.3-win/camilladsp.exe --mutazioni
```

Il programma crea una cartella di esecuzione nuova, genera i campioni, chiede al motore di validare la configurazione, elabora i file e misura il risultato. Produce `esito.json` soltanto se tutte le prove previste riescono; un'eccezione e un'uscita diversa da zero significano che il collaudo non è superato. Il rapporto annuncia esplicitamente se anche le mutazioni sono state esercitate. Per la ripetizione su Linux sono stati trasferiti lo stesso script, la stessa configurazione e il binario Linux verificato, indicando i relativi percorsi con `--bin`, `--config` e `--dest`; i percorsi temporanei effettivi sono nella prova privata.

La guardia iniziale accetta soltanto i dispositivi `RawFile` e `File`, due canali S16_LE in ingresso e quattro F32_LE in uscita a 48 kHz, con i nomi di file previsti. L'esecuzione Python con ottimizzazione `-O` è rifiutata affinché le asserzioni della prova restino attive. Un backend hardware richiede un altro percorso di collaudo, non una sostituzione rapida nel file di laboratorio.

## Troubleshooting osservato

### Il volume negativo viene interpretato come un'opzione

Osservato sulla postazione Windows il 2026-11-18: il motore rifiuta il parametro separato `--gain -6` con «unexpected argument». Nella prova viene passato `--gain=-6` come singolo argomento; dopo la correzione la misura osserva l'attenuazione su tutte le vie. Il primo giro normale era riuscito, ma questo non chiudeva il criterio sul volume.

### Il sandbox impedisce la scrittura dei campioni

Osservato sulla postazione Windows il 2026-11-18: il primo avvio ha restituito PermissionError creando `input.pcm` nella nuova cartella di prova, prima dell'esecuzione del motore. Il collaudo è stato ripetuto con autorizzazione esplicita; il fallimento di scrittura non è stato interpretato come errore di CamillaDSP. I file sorgente e le precedenti prove non sono stati cancellati.
