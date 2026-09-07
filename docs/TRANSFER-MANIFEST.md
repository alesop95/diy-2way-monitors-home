# Manifest di trasferimento verso la macchina Ubuntu Studio

> Che cosa va spostato dal disco di sviluppo alla macchina di destinazione, dove va messo, perché, e come si verifica che il travaso sia integro. Il criterio non è liberare spazio: è mettere ogni file dove viene usato, così che il repository resti leggero e la macchina di lavoro sia autosufficiente.

## Perché questo trasferimento

I materiali pesanti di questo progetto sono installer di programmi Windows che girano sotto Wine sulla macchina Ubuntu Studio, più il pacchetto degli esempi di Akabak, che è materiale di lavoro della fase 5. Sul disco di sviluppo non servono a nulla: non si installano su Windows, non si eseguono, e non entrano nel repository perché il `.gitignore` li esclude per estensione. Sono 159 megabyte che stanno nel posto sbagliato.

Va detto subito, per chiarezza sul rischio: nessuno di questi file è mai entrato nella storia di git. Il repository è di 584 kilobyte totali, e la verifica è che `git count-objects -vH` non mostra alcun oggetto di dimensione anomala e che `git ls-files` non elenca nulla della cartella dei materiali. Il trasferimento è quindi una operazione di igiene del disco, non un intervento di riparazione della storia del repository, che non ne ha bisogno.

## Lo stato della connessione, verificato

La macchina non era raggiungibile al momento della stesura. Le verifiche eseguite dalla postazione Windows sono le seguenti, e portano tutte allo stesso esito.

La risoluzione a livello di rete locale non trova l'host: l'indirizzo `192.168.10.204` non compare nella tabella ARP, mentre gli indirizzi vicini `192.168.10.203` e `192.168.10.205` ci sono. Il ping restituisce *host di destinazione non raggiungibile* generato dall'interfaccia locale stessa, che è la risposta tipica di un indirizzo per cui non esiste una voce ARP nella propria sottorete. Il tentativo di connessione SSH va in timeout sulla porta 22. La traccia dell'instradamento si ferma sulla propria interfaccia.

La sottorete è compatibile: la postazione Windows ha indirizzo `192.168.10.73` con maschera `255.255.224.0`, quindi `192.168.10.204` cade dentro l'intervallo di indirizzi diretti e non richiede instradamento. La rete su cui la postazione si trova ha però più segmenti, con dispositivi visibili anche in `192.168.20.x` e `192.168.30.x`, e un numero di host tale da suggerire una rete di ufficio.

La conclusione è che la macchina Ubuntu Studio non è accesa oppure non è collegata a questo segmento di rete in questo momento. Non è un problema di chiave SSH né di configurazione: non c'è un host a cui parlare. Il trasferimento è quindi preparato e non eseguito, e lo strumento verifica la raggiungibilità prima di iniziare, invece di fallire a metà.

## Che cosa si trasferisce

I sette file binari provengono dalla cartella `Akabak + VACS/` nella radice del progetto, che è ignorata da git. L'ottavo è il documento sorgente, archiviato sotto `_notes/` dopo la verifica di copertura registrata in `docs/90-riferimenti/copertura-sorgente.md`.

| File | Dimensione | Destinazione | Perché |
|---|---|---|---|
| `AKABAK_Pro_v324b126.exe` | 35.280.066 | `~/electroacoustics/installers/` | installer del simulatore, serve alla reinstallazione dopo il setup pulito |
| `VACS_64_v213b33.exe` | 18.114.349 | `~/electroacoustics/installers/` | variante a 64 bit, quella da installare |
| `VACS_32_v213b33.exe` | 17.853.226 | `~/electroacoustics/installers/` | variante a 32 bit, riserva se la prima dà problemi |
| `AKABAK-Examples.zip` | 94.228.740 | `~/electroacoustics/examples/` | materiale di lavoro della fase 5, che comincia adattando un esempio |
| `Gmail - Akabak 3 license.pdf` | 249.386 | `~/electroacoustics/licenze/` | contiene il release code, indispensabile alla riattivazione |
| `update AKABAK (Joerg Panzer)_2026-03-19_10-18-32.jpg` | 98.880 | `~/electroacoustics/licenze/` | schermata di un aggiornamento dell'autore, riferimento |
| `randteam.url` | 114 | `~/electroacoustics/licenze/` | collegamento al sito dell'autore |
| `_notes/full_electroacoustics.docx` | 98.899 | `~/electroacoustics/sorgenti/` | documento sorgente di questa documentazione, conservato come fonte di rigenerazione |

Il totale di questa prima parte è di circa 166 megabyte.

## Che cosa si trasferisce, parte seconda: il corredo Progetto stanza

Il corredo software raccolto sotto `C:\Users\Utente\Desktop\Progetto stanza (software)` pesa 2,3 GB, e va sulla macchina soltanto in parte. La selezione non è arbitraria: è il sottoinsieme legittimo e utile, e il criterio con cui ogni voce è stata inclusa o esclusa è documentato voce per voce in `docs/10-ambiente/wine-corredo-progetto-stanza.md`, con il formato reale di ciascun installer letto dai file e non dedotto dal nome.

| Voce | Tipo | Dimensione | Destinazione | Perché |
|---|---|---|---|---|
| `VituixCAD_setup.exe` | file | 796 KB | `~/electroacoustics/progetto-stanza/diy/` | strumento della fase 4a, gratuito |
| `Arta/` | albero | 6,3 MB | `~/electroacoustics/progetto-stanza/diy/` | serve alla fase 8, per produrre un GLL da misure reali |
| `EASE_Focus_v3.1.260/` | albero | 58 MB | `~/electroacoustics/progetto-stanza/room/` | versione da installare, con il servizio di database AFMG |
| `EASE_Focus_3_GLL_Database_2016_10_11/` | albero | 451 MB | `~/electroacoustics/progetto-stanza/room/` | 221 file, di cui 174 GLL: dati, non programma |
| `Ramsete27b - room acoustics/` | albero | 9,7 MB | `~/electroacoustics/progetto-stanza/room/` | supplemento facoltativo, subordinato alla verifica di licenza PA-002 |
| `EASE_Focus_v3.0.18/` | albero | 45 MB | `~/electroacoustics/progetto-stanza/archivio/` | archivio di riserva se la 3.1.260 dà problemi, non si installa |

Il totale di questa seconda parte è di circa 524 mebibyte, quindi il trasferimento complessivo è di circa 682 mebibyte, come riporta lo strumento nella sua fase di sola verifica.

Sulla sorgente da usare, un chiarimento che vale perché è stato oggetto di una domanda. Il corredo esiste in due copie identiche, quella sul Desktop e quella su `J:`, e l'identità è stata verificata il 2026-09-07 per impronta su tutti e 650 i file. La sorgente del trasferimento è quindi indifferente, e lo strumento usa il Desktop soltanto perché è sempre disponibile mentre l'SSD va collegato. La variabile d'ambiente `CORREDO` permette di puntarlo all'SSD se serve.

Ne discende una precauzione sull'ordine, ed è l'unica conseguenza pratica dell'avere due sorgenti: la cancellazione della copia su SSD, tracciata come PA-001, non va eseguita prima che il trasferimento sia compiuto, altrimenti si perde la sorgente alternativa proprio nel momento in cui potrebbe servire.

Il censimento completo delle quattordici voci, con il verdetto e la ragione per ciascuna, è in [90-riferimenti/censimento-corredo.md](90-riferimenti/censimento-corredo.md), che è anche il documento che autorizza a togliere il materiale dall'SSD.

A trasferimento compiuto, sulla scrivania della macchina si mette un collegamento simbolico all'albero, così che sia raggiungibile con un doppio clic senza duplicare i file né spezzare la corrispondenza fra manifest e disco.

```bash
ln -sfn ~/electroacoustics ~/Desktop/Progetto-stanza
```

Le voci escluse sono otto, per circa 1,7 GB, cioè quasi tre quarti del peso del corredo. Sette portano protezioni rimosse e una porta il file di provenienza da un servizio di condivisione. Nessuna serve al progetto, e la pagina sul corredo argomenta il perché per ciascuna insieme alla sostituzione nativa o gratuita che ne copre il ruolo. È esclusa anche EASE Focus 3.0.18, che non ha problemi di licenza ma è superata dalla 3.1.260 con i GLL retrocompatibili: resta materiale d'archivio sulla postazione.

La cartella di destinazione sta sotto `/home`, e la scelta è deliberata: `/home` è su una partizione separata, quindi questi file sopravvivono alla reinstallazione pulita del sistema descritta nella pagina sull'aggiornamento alla LTS. Metterli sotto la radice li farebbe cancellare esattamente nel momento in cui servono.

## Che cosa non si trasferisce

Le copie con protezione rimossa presenti nel pacchetto software ereditato, cioè FineCone, FineMotor, LSPCad e i tre emulatori di amplificatori per chitarra, non sono nel manifest. Non fanno parte del workflow, non ne serve nessuna, e le ragioni per cui non servono sono nell'inventario del software.

Le due versioni superate di EASE Focus e i database GLL non sono in questo manifest perché non stanno su questo disco: risiedono su un supporto esterno, come indica il nome del file di inventario nella radice del progetto. Quando quel supporto sarà a disposizione andranno gestiti con lo stesso criterio, e la sola versione da portare sulla macchina è la 3.1.260 con il database dei GLL, per le ragioni discusse nella pagina della fase 2.

I file di testo e i collegamenti nella radice del progetto restano dove sono. Sono appunti e segnalibri di poche centinaia di byte, ignorati da git, e non c'è motivo di spostarli.

## Verifica di integrità

La verifica avviene in due parti, perché i due gruppi hanno forma diversa e un solo elenco piatto non basterebbe.

Per gli otto file del manifest si confronta un elenco di impronte per nome di file, ed è quello riportato qui sotto, calcolato prima del trasferimento.

Per il corredo, che è fatto di alberi di cartelle, lo strumento confronta voce per voce l'elenco completo delle impronte relative alla radice di quella voce, sull'origine e sulla destinazione, e riporta il numero di file e le differenze. Le impronte del corredo non sono trascritte in questo documento perché sono qualche centinaio e perderebbero di utilità: il confronto è meccanico e il suo esito è nell'output dello strumento.

Le impronte SHA-256 degli otto file del manifest sono le seguenti.

```
9807e96d2e5bff1c76b22ee510768571330dd49e727ad167ea0324d350fc5cff  AKABAK_Pro_v324b126.exe
581522f6e3248aa18e6e3fb13c23c1b62a749ce0dab3f23cc527c8ecc052183f  VACS_64_v213b33.exe
349074312a0cf71642f436fac45a3dd0ab9f9e698dda06760bfb553ef200635f  VACS_32_v213b33.exe
9d8d42ae05f8f5477d7719947002f0ecc50d9a7ef8803f528d69ff2296c21149  AKABAK-Examples.zip
1c18ed617293fadc17c17f755f735974107f29632f752c6636c95762158432f8  Gmail - Akabak 3 license.pdf
371d6215aca3d89a7bb0a685fd5f033c0f79c559a2c29993da93eb676f3c091a  update AKABAK (Joerg Panzer)_2026-03-19_10-18-32.jpg
e00d1cd2723a193878175f471ef86fc306dc884e9caee35c838201236f03a9bd  randteam.url
1374305c72d73a6453add083c78be4dd46e1ef0146cb550bb0040bf3265785af  full_electroacoustics.docx
```

Dopo il trasferimento le stesse impronte si ricalcolano sulla macchina di destinazione e si confrontano. Lo strumento `tools/transfer-to-studio.sh` lo fa da sé e riporta la differenza; il confronto manuale, dalla macchina Ubuntu, è il seguente.

```bash
cd ~/electroacoustics
find . -type f -exec sha256sum {} + | sort -k2
```

## Come si esegue

Lo strumento sta in `tools/transfer-to-studio.sh` per bash e `tools/transfer-to-studio.ps1` per PowerShell. Fa quattro cose in ordine: verifica i presupposti, cioè strumenti disponibili, corrispondenza fra manifest e disco, raggiungibilità dell'host e spazio sulla destinazione; crea l'albero di destinazione; copia; ricalcola le impronte sulla destinazione e le confronta con quelle di origine.

Sulla copia c'è una avvertenza pratica. Lo strumento preferisce `rsync`, che riprende un trasferimento interrotto, ma `rsync` non è presente in Git Bash per Windows, e in sua assenza degrada su `scp`, che copia sempre da capo. La versione PowerShell usa `scp` in ogni caso. Su una rete locale i 158 megabyte passano comunque in poco tempo, quindi la perdita della ripresa è accettabile; su un collegamento lento conviene invece eseguire lo strumento da una macchina dove `rsync` esiste.

Non cancella nulla sull'origine. La rimozione dei file dal disco di sviluppo è una decisione separata, da prendere dopo che il confronto delle impronte è andato a buon fine, e resta manuale. In particolare, il completamento verificato di questo trasferimento è una delle tre condizioni che sbloccano la cancellazione della copia ridondante del corredo sull'SSD esterno, tracciata come PA-001 in `docs/PENDING-ACTIONS.md`: lo strumento lo ricorda nel proprio messaggio finale.

Una asimmetria fra le due versioni dello strumento, da conoscere. La versione bash gestisce entrambe le parti del manifest. La versione PowerShell gestisce soltanto gli otto file piatti e non il corredo, e lo dichiara nella propria intestazione: duplicare in PowerShell la logica di confronto ricorsivo raddoppierebbe la superficie da mantenere per un caso che Git Bash copre già ed è installato su questa postazione.

```bash
bash tools/transfer-to-studio.sh --verifica
bash tools/transfer-to-studio.sh
```

Il primo comando esegue solo i controlli preliminari, cioè raggiungibilità dell'host, presenza degli strumenti e spazio disponibile sulla destinazione, senza copiare nulla. Il secondo esegue il trasferimento.

## Alternativa se la macchina resta irraggiungibile

Se la macchina è a casa e la postazione di sviluppo è altrove, la rete locale non è una strada. In quel caso il travaso si fa con una chiavetta o un disco esterno, e il manifest resta valido come elenco di che cosa copiare e dove metterlo; le impronte SHA-256 servono allo stesso scopo e si verificano nello stesso modo.

Vale una nota di prudenza sul PDF della licenza: contiene un codice di attivazione legato alla macchina, quindi non va caricato su servizi di archiviazione condivisi né inviato per posta a terzi. Il trasferimento diretto, per rete locale o per supporto fisico, è la strada corretta.
