# Backup finale dopo CPU, CAD, DSP e MIDI

Aggiornamento conclusivo del 2026-11-20: supporto ricollegato dall'utente, nuova copia del 19 novembre nuovamente verificata per dimensioni e SHA-256. Completata la sostituzione già autorizzata dei soli archivio e descrittore del 18 novembre, conservando la ricevuta precedente. Recuperati 19909348066 byte, circa 18,54 GiB; un solo pieno esterno completo corrente, quattro punti locali lasciati invariati. Nessun nuovo backup avviato. I paragrafi datati 19 novembre sotto descrivono lo stato prima della pulizia rinviata.

Stato del 2026-11-19: nuovo pieno terminato Success alle 17:49:25, dopo 8 minuti e 14 secondi, conservando i tre punti precedenti. Rilettura riuscita su otto file del setup e tutte le 82 impronte del kit CAD; sessione di mount chiusa. Copia esterna conclusa e verificata alle 17:59:32. L'utente deve scollegare il supporto: nessun trasferimento dell'agente rimane attivo, la pulizia precedente è rinviata al prossimo collegamento. Gli identificativi e i percorsi compilati stanno nel livello privato; non ripetere il backup.

## Perché un nuovo punto e perché il limite è quattro

Il [backup del 18 novembre](backup-ottimizzazione-2026-11.md) precede la correzione CPU, l'installazione CAD/DSP e il drop-in MIDI. Un punto finale serve a conservare anche questo setup, mentre i tre Full precedenti rimangono disponibili per confronto e ritorno. La conservazione era tre: un quarto avvio con lo stesso limite avrebbe potuto eliminare un punto precedente. È stato aumentato a quattro il solo limite del lavoro esistente, rileggendo prima e dopo percorsi ed esclusioni. Non abbassarlo mentre si devono conservare quattro punti, e non avviare una quinta corsa senza riesame.

Prima dell'avvio rilevati circa 304 GB disponibili su home e 86 GB sul supporto esterno. La copia esterna del 18 novembre pesa circa 19,9 GB più descrittore. Lo spazio consente una nuova cartella e la verifica prima della sostituzione, senza eliminare anticipatamente l'unica copia esterna corrente.

## Sequenza già eseguita sulla macchina Ubuntu

```bash
veeamconfig job info --name backup-file-sistema
veeamconfig backup list
veeamconfig session list
df -B1 /home
veeamconfig job edit fileLevel --maxPoints 4 for --name backup-file-sistema
veeamconfig job info --name backup-file-sistema
veeamconfig job start --name backup-file-sistema --activeFull
```

Il programma di avvio richiede il limite iniziale esattamente tre, nessuna sessione che risulti in corso e almeno 60 GB liberi; rifiuta un contesto diverso. Dopo l'aumento richiede una lettura Max points: 4 prima di lanciare il lavoro. L'avvio ha restituito una sessione nuova, conservata nel rapporto privato. Non sono stati modificati gli oggetti inclusi o esclusi, la destinazione o le preferenze degli altri programmi.

## Verifica della corsa e limite della prima lettura

La prima sonda ha eseguito session info sulla sessione già restituita e point list sul deposito esistente. Risultato: Running, 38%, tre vecchi Full non marcati corrotti e il quarto ancora in costruzione. Il quarto compariva con Is corrupt true durante Running: questa osservazione non attesta né un backup concluso riuscito né un guasto conclusivo. La condizione di riuscita richiede Success e il nuovo punto non corrotto dopo il termine.

Prima della consegna vanno montati soltanto il nuovo punto e la sessione di mount restituita dal suo comando; eseguire sole letture, confrontare impronte di file pertinenti e chiudere quella sessione esatta. La [procedura Veeam](veeam-agent-linux.md) distingue la rilettura campionata da un ripristino completo. Vanno verificati anche il mantenimento dei tre Full precedenti e l'assenza del deposito stesso dai dati ripristinabili.

Aggiornamento verificato: il motore dichiara 58,8 GB elaborati e 56,4 GB trasferiti. I quattro punti sono Full e non marcati corrotti. Il punto nuovo è stato montato soltanto dopo Success; nessun mount preesistente o contenuto della cartella è stato nascosto. Confrontate otto coppie SHA-256: fstab, parametri GRUB Ubuntu Studio, modulo CPU aggiornato, nuovo drop-in FluidSynth, unità DSP, comando DSP, wrapper FreeCAD e manifesto del kit. Verificate inoltre tutte le 82 voci del manifesto nella copia ripristinabile. Controllata l'assenza di contenuto del deposito Veeam, per evitare la ricorsione del backup dentro sé stesso.

Il controllo dei percorsi ricostruisce il file ripristinabile dalla sorgente risolta e rifiuta collegamenti che escano dal mount: non confronta per errore il file vivo con sé stesso attraverso un link assoluto. Il mount osservato è ext4 con opzione rw; sono state impartite soltanto letture, non viene qualificato come montaggio in sola lettura. La chiusura della sola sessione restituita termina 0 e il mount non risulta più attivo.

Archivio concluso di 20995842048 byte, descrittore di 35790 byte. Impronte sorgenti calcolate a flusso, senza caricare l'archivio in memoria; rapporto privato con otto confronti, 82 voci e i due file da copiare. Il campionamento non dimostra ripristino integrale o avvio di una macchina ripristinata.

## Copia esterna e autorizzazione alla sostituzione

Nuova copia nella cartella datata 2026-11-19 del deposito esterno del progetto. Archivio e descrittore coincidono per dimensione e SHA-256 con le sorgenti concluse; ricevuta verifica-copia.json conservata accanto ai file. Percorso esatto e impronte nei rapporti privati, comunicati all'utente.

Dopo la verifica è stata chiesta autorizzazione sui due nomi esatti del 18 novembre, per recuperare 19909348066 byte, circa 18,54 GiB. L'utente risponde sì ma deve scollegare subito il supporto: la pulizia è rinviata, nessuna cancellazione eseguita e nessun'altra lettura o scrittura sul supporto avviata. Al prossimo collegamento rileggere le prove e verificare lo stato dei file prima della sostituzione prevista; conservare la ricevuta precedente.

Al termine del 19 novembre nessun file della copia esterna precedente era stato cancellato e restavano temporaneamente due pieni esterni. Al ricollegamento del 20 novembre la verifica SHA-256 della nuova copia è riuscita prima della cancellazione dei due nomi autorizzati; controllo successivo: vecchi archivio e descrittore assenti, ricevuta precedente presente, archivio corrente da 20995842048 byte e descrittore da 35790 byte. Spazio libero dopo la pulizia 84938194944 byte. La politica concordata torna a un pieno esterno verificato; i quattro punti locali hanno conservazione distinta. La fine dei processi dell'agente non dimostra che altri programmi Windows non tengano file aperti: usare l'espulsione sicura del sistema operativo e attendere la conferma prima di scollegare fisicamente il disco. L'agente non ha eseguito né verificato l'espulsione.
