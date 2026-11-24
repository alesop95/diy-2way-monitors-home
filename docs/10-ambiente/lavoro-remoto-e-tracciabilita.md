# Sviluppo dalla postazione e modifiche tracciate

Direttiva dell'utente del 2026-11-18: sviluppare dalla postazione attuale tutto ciò che può essere sviluppato qui e usare SSH per preparare e collaudare Ubuntu Studio finché è raggiungibile. Ogni ottimizzazione e sviluppo deve conservare il motivo della scelta e le prove. È una modalità di lavoro, non una dichiarazione che la macchina sia già pronta.

## Dove vive il lavoro

Codice, configurazioni, modelli parametrici, simulazioni, distinta e documentazione tecnica nascono nel repository di progetto sulla postazione. Ubuntu è la macchina sulla quale verificare il comportamento Linux, l'integrazione audio e le applicazioni installate. Ogni trasferimento deve indicare quali file e versione sono stati usati: la sola copia presente sul sistema remoto non diventa la fonte del progetto. Il blocco ambiente viene propagato al progetto gemello con `tools/sync-ambiente.py`.

Lo sviluppo teorico, geometrico e documentale continua dalla postazione anche quando Ubuntu non è in rete. Il collaudo che richiede quella macchina rimane aperto finché non viene eseguito. Le operazioni con password sudo si eseguono nel terminale SSH interattivo dell'utente; l'agente prepara i comandi e acquisisce poi le prove. Commit e push restano manuali.

## Che cosa registrare per ogni intervento

| Campo | Contenuto richiesto |
|---|---|
| Problema e motivo | Quale comportamento va migliorato e perché serve a registrazione, ascolto, simulazione o costruzione |
| Stato precedente | Versioni e configurazioni pertinenti; quando si cerca una prestazione, misura iniziale sul carico reale |
| Modifica | File e comandi esatti, versioni degli artefatti, eventuali privilegi |
| Risultato atteso | Un criterio osservabile che distingua successo e fallimento |
| Prova effettiva | Output, confronto prima/dopo ed eventuale persistenza dopo riavvio |
| Ripristino | Punto disponibile e configurazione precedente, senza promettere un ripristino mai provato |
| Costo e limiti | Spazio, tempo macchina, energia, dipendenze e ciò che il collaudo non copre |

Il registro pubblico è `docs/OPERATIONS-LOG.md`; procedure e motivazioni operative stanno in questo blocco. Le decisioni che cambiano l'architettura passano anche per il registro delle decisioni del progetto. Le prove grezze, i percorsi con nomi reali e i dati della macchina restano sotto `_notes/`, ignorata da Git; nei documenti pubblici si usano parametri. Un comando preparato è dichiarato preparato, non eseguito. Un intervento non si chiude per il solo fatto che il comando sia terminato senza errori.

## Gestione CPU: aggiornamento eseguito

Il problema misurato era il servizio `cpupower-gui.service` fallito con il pacchetto 1.0.0-6: l'unità invocava la configurazione grafica senza applicare il profilo. L'utente ha eseguito dalla postazione il seguente comando SSH interattivo il 2026-11-18:

```powershell
ssh -t studio "sudo apt update && sudo apt-get --no-remove install --only-upgrade cpupower-gui"
```

`apt update` aggiorna l'elenco dei pacchetti disponibili; il secondo comando aggiorna il componente nominato e impedisce rimozioni di pacchetti. Il piano osservato ha aggiornato soltanto cpupower-gui da 1.0.0-6 a 1.0.0-6ubuntu0.26.04.3, senza nuove installazioni o rimozioni. Gli avvisi Python comparsi durante l'installazione non l'hanno interrotta; la prova funzionale successiva è il servizio riuscito, non l'assenza di avvisi.

La verifica dell'agente via SSH rileva unità con `ExecStart=/usr/bin/cpupower-gui config -a`, servizio abilitato, `Result=success`, `ExecMainStatus=0` e applicazione ai processori logici da 0 a 7. Il servizio è di tipo oneshot: dopo il lavoro termina e lo stato inattivo va letto insieme a risultato e codice d'uscita. Il profilo applicato è powersave con limiti configurati da 800 a 4000 MHz; questo non misura consumo, rumore o stabilità audio. Non è ancora stato provato un nuovo avvio del sistema.

Versione, unità, journal, parametri e cronologia APT sono conservati nel rapporto privato `_notes/cpu-dopo-aggiornamento-20261118.log`. Le prossime verifiche sono la persistenza dopo riavvio e il collaudo degli strumenti CAD. L'utente non deve impartire di nuovo il comando già riuscito.

Ottimizzare non significa imporre sempre il profilo di massima prestazione. Per questo progetto si confrontano un uso ordinario adattivo e un profilo audio sotto carico, misurando interruzioni, latenza e, quando misurabili, consumo e rumore. Le modifiche a kernel, affinità CPU, priorità o quantum richiedono un problema e una prova pertinenti; i parametri realtime già presenti non vengono duplicati per abitudine. La politica finale dipende dai risultati.

## Backup e continuità

Il pieno del 18 novembre è stato verificato nel deposito locale `/home/veeam-repo`, che si trova sullo stesso SSD della macchina. Il solo elenco del deposito non prova che esista una copia sulla postazione. Prima del trasferimento fisico va completata la copia fuori macchina di archivio e descrittore, confrontando entrambe le impronte. Nome della cartella, nomi esatti dei file e comandi compilati sono nelle prove private. Lo stato resta quello della [procedura del backup](backup-ottimizzazione-2026-11.md).

Sul disco esterno resta un solo pieno verificato, dopo la sostituzione autorizzata dei vecchi file. La conservazione locale attuale è tre punti e tutti e tre sono da preservare: non si avvia automaticamente un quarto backup a ogni modifica. Prima di una nuova corsa si rivaluta la conservazione e la destinazione. Il software può essere pronto al trasferimento prima di schermo e diffusori; il nuovo indirizzo di casa e i futuri collaudi hardware si verificano quando diventano disponibili.
