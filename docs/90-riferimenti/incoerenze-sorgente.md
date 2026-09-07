# Le incoerenze del documento sorgente, una per una

> Pagina didattica. Il documento `full_electroacoustics.docx` conteneva sei affermazioni fra loro incompatibili o tecnicamente sbagliate. Questa pagina le spiega tutte e sei nel dettaglio: che cosa diceva il sorgente, perché è sbagliato, come si riconosce l'errore, che cosa dice invece la versione corretta e dove è finita nella documentazione. Serve a due cose: sapere che quelle correzioni sono state fatte deliberatamente e non per distrazione, e imparare a riconoscere la stessa classe di errore la prossima volta.

## Perché una pagina dedicata invece di una nota a piè di pagina

Un appunto scritto in mesi diversi accumula naturalmente contraddizioni: si impara qualcosa, si aggiorna un paragrafo e non l'altro, e alla rilettura successiva non si distingue più quale delle due versioni fosse quella informata. Questo è normale e non è un difetto dell'autore.

Diventa un problema nel momento in cui l'appunto viene usato come procedura. Chi rifà l'installazione seguendo la trascrizione sbagliata la replica, e l'errore si propaga in una macchina reale invece di restare su carta. Quattro delle sei incoerenze qui elencate avrebbero avuto esattamente questo esito. Per questo la correzione è documentata invece che silenziosa: la documentazione che sostituisce un appunto deve dichiarare in che punti si discosta da esso, altrimenti non è verificabile.

## Incoerenza 1: due filesystem sullo stesso punto di montaggio

Che cosa diceva il sorgente. Nella sezione sul partizionamento, l'elenco finale delle partizioni risultanti riportava questo schema.

```
nmveOn1p1   EFI System Partition (FAT32)   ~100MB   /boot/efi
nmveOn1p2   Linux filesystem (EXT4)        80GB     /
nmveOn1p3   Linux swap                     8GB      swap
nmveOn1p4   Linux filesystem (EXT4)        resto    /
```

Perché è sbagliato. La seconda e la quarta partizione sono entrambe dichiarate montate su `/`, e questo non è uno schema realizzabile. Un punto di montaggio è una posizione nell'albero dei file, e in quella posizione può esserci un solo filesystem alla volta: montare un secondo filesystem su una directory già occupata non produce l'unione dei due, ma nasconde il contenuto del primo dietro quello del secondo, che è il comportamento normale del comando `mount` e non un errore da sfruttare. Sulla radice del sistema questo significherebbe rendere invisibile il sistema stesso. L'installatore di Ubuntu, del resto, non lo permette: rifiuta la configurazione prima di scrivere qualsiasi cosa.

Come si riconosce. Basta leggere la colonna dei punti di montaggio cercando duplicati. È un controllo di dieci secondi, e vale la pena farlo su qualunque schema di partizionamento scritto a mano, perché è l'errore di trascrizione più facile da commettere e il più difficile da notare rileggendo distrattamente.

Che cosa è vero. La quarta partizione è `/home`, e lo dice la tabella dello stesso documento, che era corretta.

| Partizione | Filesystem | Dimensione | Mount point |
|---|---|---|---|
| EFI | FAT32 | ~100 MB | `/boot/efi` |
| root | EXT4 | ~80 GB | `/` |
| swap | - | ~16 GB | - |
| home | EXT4 | il resto | `/home` |

L'incoerenza è quindi interna al documento: la tabella e l'elenco finale dicevano cose diverse, e l'elenco era la versione sbagliata. Va notato che le due fonti divergono anche sulla dimensione della swap, 8 GB nell'elenco e circa 16 GB nella tabella: la tabella è coerente con la regola che la dichiara pari alla RAM per rendere possibile l'ibernazione, e la macchina ha 16 GB di RAM, quindi anche qui la tabella è la versione informata.

Perché conta. È la più pericolosa delle sei, perché la separazione di `/home` su una partizione propria è precisamente ciò che rende la reinstallazione pulita una operazione a basso rischio. Un appunto che dichiara due radici e nessuna `/home` porterebbe a rifare l'installazione senza quella separazione, e la volta successiva la reinstallazione costerebbe la perdita di tutti i dati.

Dove è finita. In `docs/10-ambiente/ubuntu-studio-installazione.md`, con la tabella corretta e una sezione finale che dichiara l'errore del sorgente per nome. In `docs/10-ambiente/installazione-pulita-26-04.md` lo schema corretto è il punto di partenza della procedura.

## Incoerenza 2: Akabak descritto come software a 16 bit

Che cosa diceva il sorgente. Nella scheda del programma, due affermazioni a distanza di poche righe.

La prima: Akabak è un software Windows a 16 bit, non compatibile direttamente con sistemi moderni, eseguibile su Linux tramite Wine.

La seconda, poco dopo: esistono due Akabak, cioè le versioni 2.x e 3.x moderne a 64 bit con interfaccia grafica e scripting, che richiedono Windows 7 o superiore, e la 1.x storica a 16 bit e testuale, ancora usata in ambito DIY per i modelli a tromba. E poco oltre: per un workflow serio si scelga la 3.x.

Perché è incompatibile. Le due affermazioni non possono essere vere insieme per lo stesso programma. La prima descrive la 1.x, la seconda sceglie la 3.x, e la scheda le usa entrambe come se parlasse di un solo oggetto. La conseguenza pratica è che dalla prima affermazione seguirebbero decisioni di configurazione sbagliate: un eseguibile a 16 bit non gira in un prefix Wine a 64 bit, e nemmeno in uno a 32 bit sulle versioni moderne di Wine, perché il supporto a 16 bit richiede configurazioni specifiche e su un sistema a 64 bit non è disponibile affatto. Chi partisse da lì cercherebbe di risolvere un problema di compatibilità a 16 bit che non esiste.

Come si riconosce. L'indizio è già nel nome del file che si è scaricato. L'installer è `AKABAK_Pro_v324b126.exe`, cioè versione 3.2.4 build 126, e l'autore nella sua corrispondenza conferma la versione corrente come AKABAK 3.2.4 b126. Un programma a 16 bit non viene distribuito nel 2025 con quel numero di versione, e la conferma è nel campo del formato dell'eseguibile, che si legge in un attimo.

```bash
file ~/electroacoustics/installers/AKABAK_Pro_v324b126.exe
```

Che cosa è vero. La versione in uso è la 3.x professionale, a 64 bit, che richiede Windows 10 o 11 a 64 bit e .NET Framework 4.8. Serve un prefix Wine a 64 bit con profilo Windows 10. Nessuna delle considerazioni sui 16 bit si applica.

Dove è finita. In `docs/10-ambiente/wine-programmi-windows.md`, che dichiara la contraddizione e la risolve, e in `docs/90-riferimenti/timeline-akabak-vacs.md`, dove il numero di versione è confermato da una fonte esterna al documento.

## Incoerenza 3: un prefix Wine annidato dentro un altro prefix

Che cosa diceva il sorgente. Nella sezione di troubleshooting, come rimedio all'errore sul caricamento di `kernel32.dll`, il documento proponeva la creazione di un prefix pulito a 32 bit con questo comando, e i comandi successivi lo usavano coerentemente.

```
WINEPREFIX=~/.wine/wine32 winecfg
WINEPREFIX=~/.wine/wine32 winetricks dotnet48 corefonts
WINEPREFIX=~/.wine/wine32 wine /percorso/al/programma.exe
```

Perché è sbagliato. Un prefix è la radice di un albero che contiene `drive_c`, `dosdevices` e i file di registro. Il percorso `~/.wine/wine32` colloca la radice del nuovo prefix dentro `drive_c` del prefix di default, o meglio dentro la cartella del prefix di default: da quel momento il primo prefix contiene il secondo come se fosse una normale cartella del suo disco C virtuale.

Le conseguenze sono tre, e nessuna si manifesta subito, che è ciò che rende l'errore insidioso. La prima è la confusione degli strumenti: un backup del prefix di default con una copia ricorsiva porta dentro anche l'intero secondo prefix, e un ripristino sovrascrive entrambi. La seconda è la confusione dei programmi: un'applicazione che gira nel prefix esterno e scandisce il proprio disco C trova un albero Windows completo dentro una sottocartella, con un secondo `System32` e un secondo registro. La terza è la fragilità dell'azzeramento: la procedura di pulizia documentata rinomina o rimuove `~/.wine`, e con essa porterebbe via anche il prefix figlio che era stato creato proprio per rimediare al fatto che il primo era corrotto.

Nota che lo stesso documento, poche righe più sotto, scriveva `WINEPREFIX=~/wine32` in una spiegazione, cioè la forma corretta come cartella sorella, senza accorgersi della differenza. È il tipico refuso di un carattere che cambia il significato di una procedura.

Che cosa è vero. I prefix stanno l'uno accanto all'altro, non l'uno dentro l'altro, e conviene raccoglierli sotto una cartella dedicata così che si vedano tutti insieme e nessuno finisca dentro un altro per distrazione.

```bash
WINEARCH=win32 WINEPREFIX=~/wineprefixes/wine32 winecfg
WINEPREFIX=~/wineprefixes/wine32 winetricks dotnet48 corefonts
```

Dove è finita. In `docs/10-ambiente/wine-troubleshooting.md`, con un avvertimento esplicito sulla forma del percorso, e in `docs/10-ambiente/wine-prefix-e-dipendenze.md`, dove la convenzione `~/wineprefixes/` è adottata in tutti gli esempi.

## Incoerenza 4: il tweeter da quattro pollici

Che cosa dicevano gli appunti. Negli appunti della conversazione del luglio 2024, la configurazione ipotizzata è riportata come sistema con woofer da quattro pollici e tweeter da quattro pollici, in caricamento bass reflex.

Perché è fuori scala. Un tweeter riproduce le alte frequenze, e per farlo la sua membrana deve essere piccola e leggera: piccola perché il diametro determina la frequenza a cui la radiazione smette di essere omnidirezionale e comincia a concentrarsi in asse, leggera perché la massa mobile limita l'accelerazione ottenibile e quindi l'estensione verso l'alto. Un diaframma da quattro pollici, cioè circa cento millimetri, ha una direttività già molto stretta alle frequenze che a un tweeter si chiedono, e una massa mobile incompatibile con esse.

L'ordine di grandezza corretto per un tweeter a cupola in un sistema da nearfield sta fra tre quarti di pollice e un pollice, cioè fra circa venti e ventisei millimetri. Un tweeter da quattro pollici, in pratica, non è un tweeter: è un mediorange.

Come si riconosce. La coincidenza esatta con il diametro del woofer è il segnale. In un sistema a due vie i due driver hanno diametri diversi per costruzione, perché si dividono lo spettro e ciascuno è dimensionato per la propria porzione. Due misure identiche in un due vie descrivono un altro tipo di sistema, per esempio una configurazione a doppio woofer, che non è ciò che il resto degli appunti descrive.

Che cosa è vero. Il woofer da quattro pollici è plausibile e resta l'ipotesi di partenza. La misura del tweeter è una decisione ancora aperta, e non è arbitraria: dipende dalla frequenza di incrocio, perché il tweeter deve poter lavorare con margine sotto quella frequenza senza sforzo, e la frequenza di incrocio esce dalla simulazione della fase 4a. È quindi una decisione che si prende dentro quella fase e non prima.

Dove è finita. In `docs/50-progettazione-monitor.md`, sezione sulle decisioni di progetto già prese, dove è marcata come errore di trascrizione e come decisione aperta, e in `docs/70-realizzazione-e-verifica.md`, dove la scelta dei driver dipende da essa.

## Incoerenza 5: due catene di simulazione alternative, senza sceglierne una

Che cosa diceva il sorgente. Nella sezione sulla modellazione della stanza, il documento proponeva in punti diversi due catene diverse, senza mai dichiarare quale fosse quella del progetto.

La prima: Blender più Pachyderm, con Pachyderm come strumento di acustica architettonica per riverbero, indice di trasmissione del parlato e distribuzione dell'energia, e Blender o SketchUp per il modello da esportare in CAD.

La seconda, nel riassunto del workflow: Blender per la geometria e MATAA su Octave per l'analisi modale, con il confronto contro la misura reale come criterio di validazione.

Perché è un problema, e perché non è solo una questione di ordine. Le due catene non sono varianti della stessa procedura: producono grandezze diverse, hanno criteri di validazione diversi e comportano lavoro diverso. Lasciarle entrambe aperte significa che la fase 2 non ha una definizione di finito, quindi non si sa quando è conclusa, e la fase 5 non sa quale formato di modello aspettarsi.

C'è però un fatto decisivo, che lo stesso documento riporta a poche righe di distanza senza collegarlo alla scelta: Pachyderm richiede Rhinoceros e Grasshopper, che non girano nativamente su Linux. La prima catena, quindi, non è una alternativa più laboriosa: è una alternativa non eseguibile sulla macchina del progetto. La sezione dedicata a Pachyderm nel sorgente, coerentemente, era rimasta un segnaposto vuoto, cioè non era mai stata affrontata.

Come si riconosce questa classe di errore. Quando un documento presenta due strade e una delle due ha, scritto altrove nello stesso documento, un requisito che l'ambiente non soddisfa, non ci sono due strade: ce n'è una e un desiderio. Il modo di trovarlo è leggere i requisiti insieme alle proposte, non separatamente.

Che cosa è vero. La catena del progetto è Blender più Octave con MATAA. È meno automatica di un simulatore commerciale, ma è interamente nativa, interamente ispezionabile, e il suo criterio di validazione è definito: l'accordo fra i modi predetti e i picchi misurati in REW. Pachyderm resta annotato come alternativa non praticabile su questa macchina, con la ragione, invece di restare un'opzione sospesa.

Dove è finita. In `docs/30-modellazione-e-simulazione.md`, in una sezione che espone entrambe le catene e dichiara quale prevale e perché, e in `docs/60-simulazione-finale-akabak.md`, dove l'esclusione è richiamata insieme al motivo per cui Akabak occupa quel posto.

## Incoerenza 6: un installer con un nome che non esiste

Che cosa diceva il sorgente. Nella sezione sull'installazione di EASE Focus, la procedura indicava di posizionarsi nella cartella dell'installer e lanciarlo per nome.

```
cd /percorso/dove/hai/EASE_Focus_Setup_v3.1.260.exe
wine EASE_Focus_Setup_v3.1.260.exe
```

Perché è sbagliato. Quel file non esiste. L'ispezione diretta della cartella `EASE_Focus_v3.1.260` nel corredo mostra un pacchetto InstallShield composto da `setup.exe`, `EASE Focus 3.msi`, `Data1.cab`, `ISSetup.dll`, `Setup.ini`, `0x0409.ini` e `Setup.bmp`, più tre sottocartelle. L'eseguibile da lanciare si chiama `setup.exe` e pesa circa un megabyte.

C'è una seconda conseguenza, più importante del nome. La prima riga del sorgente suggerisce di trattare l'installer come un file singolo da spostare dove serve. Un pacchetto InstallShield non funziona così: `setup.exe` è un avviatore che cerca accanto a sé il file MSI e gli archivi `.cab`, quindi va lanciato da dentro la sua cartella, con tutti i suoi file al loro posto. Copiare il solo `setup.exe` altrove produce un errore che non nomina la causa vera.

Come si riconosce. Questa è la sola delle sei incoerenze che non si trova rileggendo il documento, perché il documento è internamente coerente: si trova soltanto guardando i file. È il caso che giustifica la regola di ispezionare il materiale prima di scrivere una procedura che lo usa, e non fidarsi di un nome trascritto mesi prima.

```bash
ls -la "Room acoustics/EEASE Focus/EASE_Focus_v3.1.260/"
```

Che cosa è vero, e un passo che mancava del tutto. La procedura corretta entra nella cartella e lancia `setup.exe`. E l'ispezione ha rivelato un passo di installazione che il sorgente non menzionava affatto: accanto all'installer principale ci sono `AFMGDatabaseService` e `AFMGDatabaseService_x64`, due installer MSI distinti. È il servizio di database che nella tabella del changelog dello stesso documento era valutato di impatto alto, perché evita di scaricare a mano ogni GLL dal sito del costruttore. Il documento ne descriveva il valore in una tabella e ne ometteva l'installazione nella procedura.

Dove è finita. In `docs/10-ambiente/wine-corredo-progetto-stanza.md`, con la procedura corretta e i due installer, e in `docs/10-ambiente/installazione-pulita-26-04.md`, dove la fase 8.5 è stata corretta di conseguenza.

## La classe di errore, in generale

Le sei incoerenze non sono sei casi indipendenti: sono quattro tipi.

Le prime tre sono errori di trascrizione, cioè un carattere o una riga sbagliati in un punto mentre la versione corretta è presente altrove nello stesso documento. Si trovano confrontando due passaggi che parlano della stessa cosa, e il metodo è cercare i duplicati: due punti di montaggio uguali, due numeri di versione diversi, due percorsi che differiscono di uno slash.

La quarta è un errore di ordine di grandezza, cioè un numero plausibile come numero ma non come misura fisica di quell'oggetto. Si trova conoscendo l'intervallo tipico della grandezza, ed è il motivo per cui vale imparare gli ordini di grandezza di ciò che si progetta anche prima di saperne calcolare i dettagli.

La quinta è una decisione non presa, travestita da elenco di alternative. Si trova chiedendo, per ogni alternativa, se l'ambiente soddisfa i suoi requisiti, e la risposta è spesso già scritta poche righe più in là.

La sesta è di tipo diverso da tutte le altre, ed è la ragione per cui vale la pena distinguerle. Non è una contraddizione interna e non si trova rileggendo: il documento è coerente con se stesso e semplicemente non corrisponde ai file. Si trova solo confrontando la procedura con il materiale su cui dovrebbe operare, ed è il tipo di errore che si moltiplica quando una procedura viene scritta a memoria a distanza di mesi dal materiale. Il metodo, di conseguenza, è elencare i file prima di scrivere il comando che li usa.
