# Backup prima dell'ottimizzazione della macchina

Stato al 2026-11-18: nuovo pieno attivo concluso Success, riletto e copiato fuori macchina con entrambe le impronte verificate; rotazione esterna conclusa. È un backup a livello di file senza snapshot, non un'immagine avviabile. Identificativi dei punti, sessioni e prove dettagliate restano nel livello privato del progetto.

Destinazione effettiva verificata via SSH: `/home/veeam-repo`, sullo stesso SSD interno di Ubuntu, nella partizione home. Il nuovo archivio misura 19909320704 byte, circa 18,54 GiB, ed è accompagnato dal descrittore VBM. Il nome della sottocartella contiene il nome reale della macchina e uno spazio; i percorsi compilati restano privati. La copia esterna è ora verificata in `J:/backup-macchine/<NOME_MACCHINA>/2026-11-18`, con archivio e descrittore. Per trasferirlo dalla postazione servono archivio e descrittore e il confronto delle rispettive impronte, come nella fase 7 della procedura Veeam.

## Presupposti verificati

La sessione SSH attuale appartiene al gruppo `veeam` e può leggere configurazione, elenco dei lavori, backup e sessioni senza sudo. Questo corregge la conclusione troppo ampia della chiusura precedente: l'assenza di sudo non interattivo impedisce l'aggiornamento APT, ma non queste operazioni Veeam. La procedura `veeam-agent-linux.md` lo documentava già con MS-150; è stata riletta e verificata dal vivo.

Il lavoro `backup-file-sistema` include radice e home, esclude il deposito e i filesystem di servizio, non ha una pianificazione attiva e conservava due punti. Entrambi erano pieni, datati 17 e 21 settembre. Avviare un terzo punto con quel limite avrebbe potuto ruotare il più vecchio. La creazione di un secondo lavoro indipendente è stata rifiutata dalla licenza: l'elenco successivo conferma che il lavoro è rimasto uno.

È stata quindi autorizzata e applicata la sola modifica del numero di punti conservati, da due a tre. La lettura successiva conferma il nuovo valore e gli stessi percorsi ed esclusioni. Non riportare il limite a due mentre esistono tre punti da conservare. Prima di un ulteriore backup controllare di nuovo conteggio e limite: tre non significa conservazione illimitata.

## Sequenza eseguita

I comandi seguenti sono stati eseguiti sulla macchina attraverso l'alias SSH `studio`, in una sessione che porta il gruppo `veeam`. Non richiedono sudo in quella sessione.

```bash
id -nG
veeamconfig repository list
veeamconfig job list
veeamconfig job info --name backup-file-sistema
veeamconfig backup list
veeamconfig session list
df -h /home
veeamconfig job edit fileLevel --help
veeamconfig job edit fileLevel --maxPoints 3 for --name backup-file-sistema
veeamconfig job info --name backup-file-sistema
veeamconfig job start --name backup-file-sistema --activeFull
```

L'avvio ha restituito una nuova sessione alle 12:13:10 del 18 novembre. La lettura della sessione corrente e dello spazio libero non modifica né interrompe il lavoro. Il solo avvio riuscito non è un backup riuscito: occorre prima lo stato finale `Success`, poi un punto `Full` leggibile, la presenza dei due punti precedenti e il confronto di file pertinenti dopo il montaggio del nuovo punto. La copia fuori macchina è un criterio ulteriore, distinto dalla copia locale utile al ritorno da un aggiornamento.

## Rilettura e trasferimento

La sessione è terminata Success alle 12:21:26, dopo 8 minuti e 16 secondi; il motore dichiara 57,7 GB elaborati e 55,3 GB trasferiti. L'elenco mostra tre punti Full non marcati corrotti, inclusi entrambi quelli di settembre. Lo spazio disponibile su home dopo la corsa è circa 285 GiB.

Il nuovo punto è stato montato con `veeamconfig point mount --id <ID_PUNTO_NUOVO>`. Sono state confrontate le SHA-256 di `/etc/fstab`, `/etc/default/grub.d/ubuntustudio.cfg`, `/usr/bin/blender`, `/usr/bin/wine` e `/usr/bin/ardour`: cinque coppie identiche. Le cartelle dei programmi elettroacustici e dei prefix Wine hanno rispettivamente 283 e 13327 file, con conteggi uguali agli originali. Il deposito dei backup non è presente nel contenuto ripristinabile. Non sono stati aperti documenti personali.

Il mount esposto da Veeam risultava ext4 con opzione rw: la prova ha impartito soltanto comandi di lettura e non costituisce una prova di montaggio in sola lettura. È stata chiusa la sola sessione restituita dal mount con `veeamconfig session stop --id <ID_SESSIONE_MONTAGGIO>`. Il suo stato finale è Success, il mount non compare più e i tre punti sono ancora elencati. Impronte, identificativi e conteggi dettagliati sono nel rapporto privato.

Questa prova dimostra la rilettura dei file campionati e la corrispondenza dei due conteggi; non prova l'integrità di ogni file, un ripristino completo o l'avvio del sistema ripristinato. Per ripetere la procedura seguire la fase 6 di `veeam-agent-linux.md`.

La destinazione fuori macchina è verificata: cartella datata nuova sul disco esterno già usato dal progetto, archivio e descrittore con SHA-256 uguali alle sorgenti. Dopo l'autorizzazione sui nomi esatti sono stati eliminati soltanto i due archivi di settembre e il loro vecchio descrittore esterno: 35842411050 byte rimossi, circa 33,38 GiB. I due punti di settembre restano su Ubuntu; non sono stati cancellati dal deposito Veeam.

Lo spazio libero finale su J: è 82113986560 byte, circa 76.47 GiB. La politica per questo supporto è conservare un pieno esterno verificato e sostituirlo soltanto dopo la verifica del successivo, evitando l'accumulo di copie. La conservazione locale di tre punti richiede comunque una valutazione prima della prossima corsa.

La prima lettura del rapporto in PowerShell ha contato erroneamente l'array JSON come un solo elemento e fermato l'operazione prima della rimozione. Dopo la correzione del conteggio e il controllo del rapporto reale sono state ricalcolate entrambe le impronte dei file copiati; solo allora sono stati rimossi i tre file autorizzati. Il rapporto interrotto è conservato insieme a quello conclusivo nel livello privato.

## Troubleshooting osservato

### La licenza rifiuta un secondo lavoro

Osservato il 2026-11-18 sulla macchina Ubuntu: `job create fileLevel` con un nome nuovo è stato rifiutato perché la funzione di più lavori richiede una licenza. Nessun nuovo lavoro è comparso nell'elenco. Non è necessario acquistare una licenza per questo intervento: dopo autorizzazione è stata aumentata la conservazione del lavoro esistente e richiesto un pieno attivo. La verifica del valore dopo l'edit precede sempre l'avvio.
