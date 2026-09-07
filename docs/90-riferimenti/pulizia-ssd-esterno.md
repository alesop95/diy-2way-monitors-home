# Pulizia dell'SSD esterno: che cosa si può cancellare, e un segnale da leggere

> Risposta a due domande: se tutto ciò che serviva è stato portato sulla macchina, e che cosa si può cancellare dall'SSD esterno per liberare spazio senza perdere niente di utile. Contiene anche una osservazione sulla salute di quel disco, che è emersa guardando la radice del volume e che vale più dello spazio recuperabile.

## Sì, tutto ciò che serviva è sulla macchina, e verificato

La risposta breve è affermativa, e la prova è nelle impronte. Il trasferimento del 2026-09-07 ha portato sulla macchina 8 file del manifest e 6 voci del corredo per 273 file, con tutte le impronte SHA-256 confrontate fra origine e destinazione e tutte coincidenti. Il risultato sulla macchina è di 728 MB in 281 file sotto `~/electroacoustics`, con un collegamento sulla scrivania.

Va però precisato che cosa significa "tutto ciò che serviva", perché la frase nasconde una scelta. Non è stato trasferito tutto il corredo: sono state trasferite le sei voci con verdetto *porta* o *archivia* del censimento, e non le otto con verdetto *scarta*. Quelle otto, per circa 1,7 GB, non sono state portate di proposito, e la ragione per ciascuna è nel censimento: nessuna serve al progetto, e ciascuna ha una ragione funzionale che regge da sola prima e indipendentemente dallo stato di licenza.

Ne segue il conteggio delle copie, che è ciò che rende sicura una cancellazione. Delle voci utili esistono ora due copie, una sul Desktop della postazione Windows e una sulla macchina Ubuntu Studio. Delle voci scartate esiste una copia sola, quella sul Desktop, perché non sono state trasferite. Cancellare la cartella su `J:` lascia quindi due copie di ciò che serve e una di ciò che non serve, e non porta via l'ultima copia di nulla.

## Che cosa si può cancellare da `J:`

Tre categorie, in ordine di sicurezza decrescente.

La prima era la cartella `Progetto stanza (software)`, 2,3 GB, e **non c'è più**: la verifica del 2026-09-07 non la trova sul volume, quindi PA-001 è chiusa. Le sue tre condizioni erano soddisfatte, cioè materiale utile sulla macchina con le impronte verificate e corrispondenza fra le due copie accertata file per file, e le due copie restanti sono intatte.

La seconda sono le cartelle di servizio, che su quel volume sono di due specie. Da macOS arrivano `.Spotlight-V100`, cioè l'indice di ricerca, `.TemporaryItems`, `.Trashes`, cioè il cestino, e `.fseventsd`, il registro degli eventi del filesystem: sono tutte inutili su Windows e su Linux, e la loro presenza dice soltanto che quel disco è stato usato anche su un Mac. Da Windows arrivano `$RECYCLE.BIN`, che è il cestino del volume e si svuota dal cestino invece che a mano, e `System Volume Information`, che contiene punti di ripristino e indici e va lasciata al sistema.

La terza sono le cartelle `FOUND.00x`, che liberano spazio ma soprattutto dicono qualcosa, e hanno una sezione propria qui sotto.

Restano fuori dal perimetro le voci di materiale personale, che sull'elenco completo del volume sono sedici fra cartelle e file: `MAIN`, che da sola pesa 296 GiB, `googleDrive_sync`, `backup-sviluppo`, `SONGWRITING`, `DOCUMENTATION`, `3DS - 03092026`, `_____da sistemare ancora`, `FINANCE`, `_info_PW`, `CV (WORK)`, `Wallpapers`, `_riflessioni profonde`, una cartella di messaggi, due archivi di backup e due file di modello. Non sono oggetto di questo progetto e questa documentazione non le tocca né suggerisce di toccarle, con la sola eccezione dei due archivi di backup, che hanno una sezione propria perché la domanda sullo spazio li riguarda direttamente.

Lo strumento `tools/analisi-ssd-esterno.py` misura ciascuna voce e la classifica secondo queste categorie, riportando peso e numero di file. Non cancella nulla: misura e riferisce, perché la cancellazione di materiale personale è una decisione dell'utente.

## La misura reale, del 2026-09-07

Il volume contiene circa 372 GiB di materiale personale e **1,2 GiB recuperabile** senza perdere nulla di utile. La cartella `Progetto stanza (software)` non compare più nell'elenco, perché è stata rimossa: la voce PA-001 è chiusa.

Il recuperabile si distribuisce così, e la sorpresa è che quasi tutto sta in tre cartelle.

| Voce | Peso | Natura |
|---|---|---|
| `FOUND.002` | 429 MiB | frammenti orfani di `chkdsk`, 77 file |
| `FOUND.000` | 412 MiB | frammenti orfani di `chkdsk`, 90 file |
| `.Spotlight-V100` | 371 MiB | indice di ricerca di macOS, 76 file |
| `.Trashes`, `$RECYCLE.BIN`, `.fseventsd`, `FOUND.001`, `FOUND.003`, `FOUND.004`, `System Volume Information` | meno di 1 MiB ciascuna | cestini, registri e frammenti residui |

Le tre voci maggiori valgono 1,2 GiB su 1,2 GiB: le altre sette sommate non arrivano a un megabyte, quindi cancellarle non cambia nulla e non vale il rischio di toccare `System Volume Information`, che è gestita dal sistema.

Va segnalato che le due cartelle `FOUND` grandi, cioè la 000 del 30 giugno e la 002 del 27 luglio, contengono 167 file di dati recuperati per 841 MiB complessivi, mentre le tre piccole ne contengono sei in tutto. Prima di cancellarle vale la pena guardare che cosa siano quei 167 file, perché sono l'unica cosa in questo elenco che potrebbe contenere qualcosa di proprio: sono frammenti che il filesystem aveva perso, quindi con nomi come `file0001.chk`, e nella grande maggioranza dei casi sono inservibili, ma la maggioranza non è la totalità.

## I due archivi di backup, che erano invisibili

Questa parte esiste per un difetto dello strumento, corretto, e vale raccontarla perché il difetto era del tipo peggiore.

La prima versione dello strumento iterava le sole cartelle della radice e ignorava i file sciolti. Su questo volume ce ne sono quattro, per **45,2 GiB**, di cui due archivi di backup: `backup 28082026 (tutto tranne main, dasistemareancora).7z` da 25,8 GiB e `backup 04092026 (tutto tranne main, dasistemareancora, 3DS - 03092026).7z` da 19,4 GiB. Lo strumento riportava quindi 326 GiB di materiale personale invece di 371, sbagliando per difetto di 45 GiB senza che nulla lo segnalasse. Un totale sbagliato per difetto è peggio di un totale assente, perché non si vede che manca qualcosa.

Sui due archivi la domanda era se il piu' vecchio fosse superato dal piu' recente, e quindi cancellabile per recuperare 25,8 GiB. **La risposta, misurata il 2026-09-07, e' no: nessuno dei due e' ridondante.**

Il confronto degli indici dei due archivi, ottenuti con `7z l`, da' questo esito.

| | 28/08/2026 | 04/09/2026 |
|---|---|---|
| Voci totali | 159.196 | 94.200 |
| Voci presenti solo qui | 145.483 | 80.487 |
| di cui sotto `backup-sviluppo` | 145.478 | 80.377 |

Nessuno dei due contiene l'altro. La causa e' `backup-sviluppo`, che fra le due date e' cambiato quasi per intero: sono due istantanee diverse della stessa cartella, non due versioni incrementali. Il piu' recente ha in aggiunta 81 voci sotto `_info_PW`, 26 sotto `DOCUMENTATION` e 2 sotto `SONGWRITING`.

Cade anche l'ipotesi avanzata prima della misura, cioe' che la differenza di peso dipendesse dalla cartella dei modelli 3DS esclusa dal piu' recente. Quella cartella non compare fra le differenze, quindi non era nemmeno nel piu' vecchio: coerente con il fatto che porti nel nome una data successiva a quel backup. La differenza di 6 GiB si spiega interamente con il rimescolamento di `backup-sviluppo`.

La conseguenza operativa: **cancellare il piu' vecchio costa 145.478 versioni di file che non esistono altrove in forma archiviata.** Se quelle versioni servano e' una decisione dell'utente, non una questione tecnica: la cartella `backup-sviluppo` esiste ancora sul disco con il suo contenuto corrente, e i due archivi sono istantanee storiche. Ma la domanda "posso cancellare il vecchio perche' c'e' il nuovo" ha una risposta negativa e documentata.

```bash
python tools/analisi-ssd-esterno.py
```

Va detto che su un volume di decine di gigabyte la misura richiede qualche minuto, perché per conoscere il peso reale di una cartella occorre attraversarne tutti i file.

## Il segnale: cinque cartelle FOUND in due mesi

Questa è l'osservazione che vale più dello spazio, ed è emersa guardando la radice del volume senza cercarla.

Una cartella `FOUND.00x` non è una cartella qualsiasi: è il deposito in cui `chkdsk` mette i frammenti orfani quando ripara il filesystem, cioè i pezzi di file di cui ha trovato i dati ma non il nome. Averne una significa che il filesystem è stato riparato una volta. Sul volume ce ne sono **cinque**, `FOUND.000` fino a `FOUND.004`, con date che vanno dal 30 giugno al 3 settembre. Cinque riparazioni in poco più di due mesi.

Le cause tipiche sono due e vanno distinte, perché portano a rimedi opposti.

La prima è la rimozione del disco senza espulsione sicura, cioè scollegarlo mentre il sistema ha ancora scritture in sospeso nella cache. È un problema di abitudine, si risolve espellendo il volume prima di staccarlo, e non dice nulla sulla salute del supporto.

La seconda è un difetto del supporto o del suo controllore, e in quel caso il rimedio non è un'abitudine ma la sostituzione, o almeno la decisione di non tenere su quel disco l'unica copia di qualcosa.

C'è un elemento di contesto che rende la prima ipotesi meno rassicurante di quanto sembri, e vale metterlo in relazione invece di lasciarlo isolato: la lettura SMART del disco interno della macchina Ubuntu Studio ha riportato 24 spegnimenti non puliti su 135 accensioni, cioè circa uno su sei. Due dischi diversi con due sintomi diversi che puntano nella stessa direzione, cioè verso una gestione dell'alimentazione e delle rimozioni poco pulita, sono un indizio più forte di due sintomi isolati. Resta un indizio e non una conclusione.

Il controllo che chiude la questione è la lettura SMART dell'SSD esterno, che si fa con `smartctl` da Linux oppure con CrystalDiskInfo da Windows, cioè lo stesso strumento con cui il disco interno era stato valutato nel 2025. Gli indicatori da guardare sono gli stessi: la percentuale di usura, la riserva di blocchi disponibili e il conteggio degli errori di integrità dei dati.

```powershell
smartctl -a /dev/sdb
```

Il nome del dispositivo va identificato prima e non assunto, perché su un disco esterno dipende dall'ordine di collegamento.

La conseguenza pratica, qualunque sia la causa, è già chiara e non aspetta la diagnosi: quel disco non è il posto dove tenere l'unica copia di qualcosa. Il che è esattamente il motivo per cui la cancellazione di `Progetto stanza (software)` è stata subordinata alla verifica che il materiale fosse altrove, invece di essere eseguita sulla fiducia.

## Che cosa resta da decidere sulla copia sul Desktop

La cancellazione su `J:` non chiude la questione dello spazio, perché la copia sul Desktop della postazione Windows resta, con tutte e quattordici le voci, comprese le otto che il censimento ha scartato.

La decisione su quella copia è separata e va presa dopo, non insieme, e la ragione è di ordine e non di merito: rimuoverle entrambe nello stesso momento lascerebbe una sola copia del materiale utile, cioè quella sulla macchina, in un momento in cui la macchina è in procinto di essere reinstallata. Finita la reinstallazione e verificato che i programmi funzionino, la copia sul Desktop diventa ridondante e può andare.

Sulle otto voci scartate la considerazione è diversa e più semplice, perché non sono state trasferite e non lo saranno: la loro unica copia è sul Desktop, e cancellarla significa non averle più. Dato che il censimento stabilisce che nessuna serve al progetto, e dato che per ciascuna esiste una sostituzione nativa o gratuita già disponibile, non c'è ragione di conservarle. Ma è materiale personale e la decisione è dell'utente, quindi resta dichiarata qui e non eseguita.
