# Censimento del corredo software, e destino di ogni voce

> Censimento completo delle quattordici voci del corredo `Progetto stanza (software)`, con il verdetto per ciascuna e la ragione del verdetto. È il documento che autorizza a togliere quel materiale dall'SSD esterno: finché ogni voce non ha una destinazione dichiarata, cancellare l'SSD significherebbe perdere qualcosa senza sapere cosa.

## Le tre fonti, e la verifica che concordano

Il corredo esiste in tre descrizioni, e la prima cosa fatta è stato verificare che dicano la stessa cosa, invece di fidarsi.

L'inventario testuale è il file `(SSD S7) DIY Loudspeaker Pack Softwares.txt` nella radice di questo progetto. Dichiara 36 cartelle, distribuite su tre alberi. Il confronto con l'SSD, fatto il 2026-09-07 con il disco collegato, dà un esito netto: *tutte e 36 le cartelle dichiarate esistono su `J:`, e su `J:` non c'è alcuna cartella non dichiarata*.

Va spiegato un dettaglio che a prima lettura sembra una lacuna e non lo è. L'inventario testuale non nomina né `VituixCAD_setup.exe` né il collegamento `EASE_Focus_v3.1.10 (k-array) - collegamento.lnk`, benché entrambi esistano. Il motivo è che quel file è l'uscita di un comando che elenca soltanto le cartelle, non i file. È quindi un inventario completo e corretto di ciò che si era proposto di elencare, e la sua incompletezza sui file è una proprietà del comando e non un errore dell'autore. Questo chiude anche in modo definitivo il sospetto, avanzato in una sessione precedente, che l'assenza della versione 3.1.10 dall'inventario indicasse una differenza fra le copie.

La copia di lavoro sul Desktop della postazione Windows e la copia su `J:` sono state confrontate per impronta il 2026-09-07: *650 file per parte, gli stessi nomi, le stesse dimensioni, 2.380.021.546 byte per copia, tutte le impronte SHA-256 coincidenti*. Sono una copia uno a uno, come l'utente dichiarava.

## Il censimento

La colonna del verdetto ha tre valori. *Porta* significa che la voce va sulla macchina Ubuntu Studio e vi viene installata o usata. *Archivia* significa che va sulla macchina ma non si installa, perché ha un valore di riferimento e non operativo. *Scarta* significa che non va da nessuna parte.

| Voce | Peso | Verdetto | Ragione |
|---|---|---|---|
| VituixCAD 2 | 796 KB | **Porta** | è lo strumento della fase 4a, cioè crossover e direttività, e nel workflow non ha sostituti: gratuito, attuale, gestisce risposta in potenza e diagrammi polari |
| EASE Focus 3.1.260 | 58 MB | **Porta** | verifica rapida della copertura di un diffusore di cui si abbia il GLL; è la versione più recente della linea gratuita e la sola da installare |
| Database GLL 2016 | 451 MB | **Porta** | 221 file di cui 174 GLL: sono dati, non un programma, ed evitano di cercare ogni modello sul sito del costruttore. Vale l'intera cartella e non i soli `.gll`, perché i file `.dll` e `.bin` di accompagnamento devono stare accanto al loro GLL |
| ARTA 1.7.1 | 6,3 MB | **Porta** | serve alla fase 8: è la via più diretta per produrre un GLL da un diffusore misurato, quindi rende simulabile il monitor autocostruito. Shareware, cartella con il solo installer ufficiale |
| Ramsete 27b | 9,7 MB | **Archivia** | acustica architettonica, ruolo già coperto da Akabak che è licenziato e funzionante. Applicazione Visual Basic 6, quindi richiederebbe un prefix a 32 bit e l'architettura `i386`. Lo stato di licenza non è accertato: si porta come archivio e si installa solo se PA-002 dà esito favorevole |
| EASE Focus 3.0.18 | 45 MB | **Archivia** | superata dalla 3.1.260, e i GLL sono retrocompatibili. Tre versioni dello stesso programma in tre prefix sono manutenzione senza ritorno. Si conserva come riferimento nel caso la più recente dia problemi |
| FineCone 2.1 | 66 MB | **Scarta** | simula il cono di un altoparlante a elementi finiti: opera a monte di questo progetto, che parte da driver finiti e dai loro parametri Thiele/Small. Inoltre porta una cartella di modifica e un emulatore di chiave hardware |
| FineMotor 2.5 | 21 MB | **Scarta** | simula il motore magnetico di un altoparlante: stesso ragionamento di FineCone, serve a chi costruisce i driver e non a chi li assembla in un sistema. Porta una cartella di modifica |
| LSPCad 5.25 | 5,9 MB | **Scarta** | progetta crossover e casse, ruolo coperto da VituixCAD che è gratuito, molto più recente e gestisce la direttività. È inoltre l'unico programma genuinamente a 16 bit del corredo, quindi richiederebbe un prefix a 32 bit dedicato solo a sé. Porta una cartella di modifica |
| LSPCad 6.32 | 15 MB | **Scarta** | stesso ruolo e stessa sostituzione di VituixCAD. Porta una cartella di modifica e il file descrittivo di un gruppo di distribuzione illecita |
| Grenander Loudspeaker Lab 3.13 | 2,4 MB | **Scarta** | ancora progettazione di diffusori della stessa generazione, e la stessa sostituzione. Porta il file descrittivo di un gruppo |
| AmpliTube 3 | 531 MB | **Scarta** | emulatore di amplificatori per chitarra, nessuna relazione con la progettazione elettroacustica. Porta uno sbloccatore separato accanto all'installer. Per l'home recording l'equivalente nativo libero su Linux è Guitarix |
| Guitar Rig 5 Pro | 813 MB | **Scarta** | come sopra, e dichiarato sbloccato nel nome della cartella |
| POD Farm 1.11 | 251 MB | **Scarta** | come sopra, richiede in ogni caso una licenza Line 6, e accanto all'installer porta il file di provenienza da un servizio di condivisione |

I numeri che ne risultano. Si portano cinque voci per circa 524 mebibyte, di cui quattro da installare e una da archiviare in attesa di PA-002; si aggiunge la 3.0.18 come archivio per altri 45 MB. Si scartano otto voci per circa 1,7 GB, cioè quasi tre quarti del peso del corredo.

## Il criterio che decide, e perché non è la licenza

Vale isolare il criterio, perché è quello che rende il censimento ripetibile su materiale nuovo invece di essere un elenco di giudizi.

Il criterio primario è *la posizione nel workflow*. Questo progetto parte da driver finiti, di cui usa i parametri Thiele/Small e le misure, e arriva a un sistema a due vie in una stanza nota. Tutto ciò che opera a monte dei driver finiti, cioè la simulazione del cono e del motore magnetico, sta fuori dal progetto per costruzione, non per giudizio di qualità: FineCone e FineMotor sono strumenti seri, ma servono a chi progetta gli altoparlanti. Tutto ciò che opera in un dominio diverso, cioè gli emulatori di amplificatori per chitarra, sta fuori a maggior ragione.

Il criterio secondario è *la sostituibilità con qualcosa di migliore già disponibile*. LSPCad e Grenander fanno ciò che fa VituixCAD, che è gratuito, di quindici anni più recente e gestisce la direttività e la risposta in potenza, cioè proprio le grandezze che questo progetto misura. Ramsete fa ciò che fa Akabak, che è già licenziato e funzionante sulla macchina.

Lo stato di licenza è un criterio *terziario*, e questo va detto con precisione perché è controintuitivo: nessuna delle otto voci scartate viene esclusa perché porta una protezione rimossa. Vengono escluse perché non servono, e la dimostrazione è che ciascuna ha nella tabella una ragione funzionale che regge da sola. La protezione rimossa è una ragione in più, non la ragione, ed è il motivo per cui non esiste in questa documentazione alcuna procedura di installazione per esse.

## Il destino fisico del materiale

L'obiettivo dichiarato è togliere il materiale dall'SSD esterno e farlo vivere sulla macchina Ubuntu Studio, che verrà sottoposta a backup.

La destinazione è sotto `/home`, ed è una scelta con una ragione precisa: `/home` sta su una partizione separata, quindi quel materiale sopravvive a una reinstallazione del sistema. Metterlo sotto la radice significherebbe perderlo esattamente nel momento in cui serve, cioè quando si ricostruisce l'ambiente.

L'organizzazione è la seguente, e separa ciò che si installa da ciò che si conserva.

```
~/electroacoustics/
├─ installers/          installer di Akabak, VACS e dei programmi da installare
├─ examples/            pacchetto degli esempi di Akabak, materiale di lavoro della fase 5
├─ licenze/             corrispondenza e release code, materiale sensibile
├─ sorgenti/            il documento sorgente della documentazione
└─ progetto-stanza/
   ├─ diy/              VituixCAD, ARTA
   ├─ room/             EASE Focus 3.1.260, database GLL, Ramsete
   └─ archivio/         EASE Focus 3.0.18, e ciò che si conserva senza installare
```

Sulla richiesta che il materiale stia sulla scrivania della macchina, la soluzione adottata concilia le due esigenze senza sacrificarne nessuna. L'albero organizzato resta sotto `~/electroacoustics/`, perché è la struttura che gli strumenti di trasferimento e di verifica conoscono e su cui il manifest calcola le impronte. Sulla scrivania si mette un collegamento simbolico a quella cartella, così che sia raggiungibile con un doppio clic senza duplicare 524 mebibyte né spezzare la corrispondenza fra manifest e disco.

```bash
ln -sfn ~/electroacoustics ~/Desktop/Progetto-stanza
ls -l ~/Desktop/
```

La cancellazione dall'SSD è tracciata come PA-001 e resta subordinata a una sola condizione residua, cioè il completamento verificato del trasferimento. Le altre due, il disco collegato e la corrispondenza fra le copie, sono soddisfatte.

Va infine chiarito che cosa accade alla copia sul Desktop della postazione Windows, perché non è oggetto di PA-001. Quella è la sorgente del trasferimento, quindi resta fino a operazione compiuta; la sua rimozione è una decisione separata da prendere dopo, e non insieme alla cancellazione dell'SSD, perché rimuoverle entrambe nello stesso momento lascerebbe una sola copia del materiale al mondo.
