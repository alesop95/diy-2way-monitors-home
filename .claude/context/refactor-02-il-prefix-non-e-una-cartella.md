# Un prefix non è una cartella: anatomia di ciò che Wine costruisce, e perché tre comandi sono falliti

> Approfondimento della voce 2 di `studio-didattico-master.md`. Entra nel dettaglio di che cosa sia un prefix Wine, che cosa contenga, quali assi lo caratterizzino e quali di essi la documentazione del progetto trattava come uno solo. Gli estratti sono output reali della macchina, raccolti fra il 2026-09-09 e il 2026-09-14.

## Il punto di partenza: che cosa stiamo facendo, e perché

Il progetto costruisce due monitor da studio a due vie per un punto di ascolto domestico noto. La catena che porta da quell'obiettivo a questo documento è breve e vale ripercorrerla, perché altrimenti un testo su Wine sembra fuori tema. La risposta va misurata al punto di ascolto reale e non in campo libero, quindi la stanza entra nel progetto come vincolo; da qui serve uno strumento che metta insieme il modello della stanza e quello del diffusore in un solo calcolo, ed è Akabak, per la fase 5. Serve inoltre uno strumento che progetti il crossover tenendo conto della direttività, cioè di come la risposta cambia fuori asse, ed è VituixCAD, per la fase 4a. Entrambi sono programmi Windows senza equivalente libero, quindi il progetto ha bisogno di Wine, e l'ambiente Wine è la parte fragile del setup.

Quello che sta accadendo adesso è l'installazione di VituixCAD nel proprio prefix. È la sottofase 8.5 della procedura, ed è il primo dei tre installatori con interfaccia grafica che restano.

## Che cos'è un prefix, materialmente

Un prefix[^1] non è una cartella di lavoro né una cartella di installazione: è una installazione di Windows completa, ridotta all'osso e contenuta in una cartella. Wine non emula un processore e non virtualizza un sistema: traduce le chiamate che un programma Windows fa al sistema operativo in chiamate equivalenti verso Linux. Perché quella traduzione funzioni, al programma deve sembrare di trovarsi dentro Windows, e il prefix è precisamente l'illusione di quel Windows.

La struttura si legge con un comando. Sul prefix appena creato per VituixCAD il primo livello contiene due voci.

```
drwxrwxr-x 4 alesop95 alesop95 4096 Sep 14 11:02 /home/alesop95/wineprefixes/vituixcad64
dosdevices
drive_c
```

`drive_c` è la radice del disco `C:` che il programma vedrà, con dentro `windows`, `Program Files`, `users` e `ProgramData`, esattamente come su un Windows reale. `dosdevices` è la tabella che traduce le lettere di unità in percorsi Linux, ed è la parte che rende il prefix una finestra sul sistema ospite invece che una scatola chiusa. Sul prefix di AKABAK contiene, fra le altre, queste due voci.

```
lrwxrwxrwx c: -> ../drive_c
lrwxrwxrwx z: -> /
```

La prima è attesa. La seconda dice una cosa che vale conoscere: la lettera `Z:` mappa la radice dell'intero filesystem Linux, quindi da dentro il prefix ogni file della macchina è raggiungibile come `Z:\percorso\del\file`. Non è una falla di sicurezza ma il comportamento predefinito di Wine, ed è la ragione per cui un programma Windows sotto Wine può aprire un file che sta in `/home` senza che nessuno lo copi dentro `drive_c`.

Accanto a questo c'è un secondo meccanismo di collegamento, dentro la cartella utente del prefix.

```
lrwxrwxrwx Desktop   -> /home/alesop95/Desktop
lrwxrwxrwx Documents -> /home/alesop95/Documents
lrwxrwxrwx Downloads -> /home/alesop95/Downloads
```

Le cartelle personali dell'utente Windows non sono cartelle vere dentro il prefix: sono collegamenti a quelle Linux. Ne discende un fatto che il progetto ha usato per una decisione, in MS-096: `C:\users\alesop95\Documents\AkabakProjects` e `~/Documents/AkabakProjects` sono la stessa cartella. Poter scegliere un percorso su `C:` invece che su `Z:` senza per questo nascondere i file dentro il prefix è il motivo per cui la radice di lavoro dei progetti è stata messa là e non altrove: un programma Windows si aspetta di lavorare su `C:`, e `Z:` è la via che più facilmente incontra difetti nei programmi vecchi.

Il terzo componente del prefix non si vede nell'elenco perché è un file: il registro. Wine lo tiene in tre file di testo nella radice del prefix, cioè `system.reg`, `user.reg` e `userdef.reg`, che sono l'equivalente delle arnie del registro di Windows. È un dettaglio operativamente prezioso, perché rende ispezionabile con `grep` uno stato che su Windows richiederebbe un editor dedicato. La prima riga di `system.reg` dichiara l'architettura del prefix.

```
#arch=win64
```

## I cinque assi che caratterizzano un prefix, e quanti la documentazione ne nominava

La voce 1 del racconto didattico ne aveva isolati quattro, e il lavoro del 2026-09-14 ne ha aggiunto un quinto. Vale enumerarli tutti insieme, perché il difetto ricorrente di questo progetto è stato trattarne diversi come se fossero uno.

Il primo è l'architettura che il sistema operativo accetta di installare, cioè se `dpkg` conosca l'architettura `i386` accanto a `amd64`. È quella che ADR-016 impone di dichiarare prima di installare Wine.

Il secondo è la presenza fisica del caricatore corrispondente sul disco, cioè se il pacchetto `wine32:i386` sia installato davvero. Non discende dal primo: MS-082 ha mostrato che `apt install --install-recommends wine` non lo installa, perché il metapacchetto si limita a suggerirlo e nessuna opzione tira dentro i suggeriti.

Il terzo è l'architettura dichiarata dentro il prefix, cioè la riga `#arch` del registro, che si fissa al momento della creazione con `WINEARCH` e non si cambia dopo.

Il quarto è l'architettura del comando che si digita. È l'asse che nessun documento nominava e che ADR-019 ha aggiunto: su Ubuntu `wine` è un collegamento a uno script che sceglie il caricatore a 64 bit ogni volta che `wine64` esiste, senza guardare né il prefix né l'eseguibile, quindi su un prefix a 32 bit fallisce sempre e la forma corretta è `wine32`.

Il quinto è emerso il 2026-09-14 leggendo l'output di creazione del prefix a 64 bit, e riguarda come i processi a 32 bit girano dentro un prefix a 64 bit.

```
00e4:err:environ:init_peb starting L"C:\windows\syswow64\rundll32.exe" in experimental wow64 mode
```

Su Windows reale, il sottosistema che fa girare i programmi a 32 bit dentro un sistema a 64 si chiama WoW64[^2], e la cartella `syswow64` che compare nel messaggio è proprio la sua. Wine lo implementa in due modi. Quello storico usa un caricatore separato a 32 bit, cioè il binario che `wine32` esegue. Quello nuovo, dichiarato sperimentale, fa girare il codice a 32 bit dentro il medesimo processo a 64 bit traducendo le chiamate al confine. Questo prefix usa il secondo, e la conseguenza pratica è che l'installer di VituixCAD, che è un eseguibile a 32 bit, girerà in modalità sperimentale: non è un problema previsto, ma è la prima cosa da sospettare se quell'installer si comportasse in modo anomalo, ed è meglio saperlo prima che dopo.

## Perché un prefix per programma, e non uno solo

La scelta di dare a ciascun programma il proprio prefix non è una precauzione generica e va motivata, perché costa spazio e ripetizione. La ragione è che le dipendenze che un programma Windows richiede si installano dentro il prefix e non accanto al programma: una libreria di runtime, un insieme di font, una versione del framework .NET diventano parte di quel finto Windows. Due programmi che chiedono versioni incompatibili della stessa libreria, messi nello stesso prefix, si contendono lo stesso file, e il secondo installato vince. La pagina dei guasti di questo progetto documenta esattamente questo esito su `kernel32.dll`, in un prefix che aveva accumulato installazioni successive.

Il costo dello spazio è inoltre minore di quanto sembri, perché il grosso di un prefix sono collegamenti e file di configurazione, non copie di Windows.

## Il primo comando fallito: Wine crea il prefix ma non ciò che lo contiene

Il comando prescritto per creare il prefix di VituixCAD ha risposto così.

```
wine: chdir to /home/alesop95/wineprefixes/vituixcad64 : No such file or directory
```

Il messaggio va letto per quello che dice, ed è una distinzione che si perde facilmente: Wine non stava tentando di creare la cartella, stava tentando di entrarci. La causa è che Wine crea la cartella del prefix ma non le cartelle che la contengono, e `~/wineprefixes` non esisteva affatto, perché l'unico prefix presente sulla macchina, `~/.wine`, sta direttamente nella cartella dell'utente ed è nato lì nel 2025.

La verifica è stata fatta con un prefix usa e getta invece che ragionando: creata la sola cartella padre, lo stesso comando ha risposto in modo diverso.

```
wine: created the configuration directory '/home/alesop95/wineprefixes/prova-diagnosi'
```

La parte istruttiva non è il difetto ma la sua estensione. La fase 7 della procedura crea quattro prefix con quattro righe consecutive e non crea mai la cartella che li contiene: chiunque ricostruisse l'ambiente da zero fallirebbe al primo comando con quel messaggio, che parla di un accesso e non di una creazione, e manderebbe la diagnosi sulla pista sbagliata. È lo stesso difetto di forma già incontrato con `winecfg`, cioè un comando prescritto che non può riuscire nell'ambiente in cui la procedura dice di eseguirlo, ed è la ragione per cui una procedura non eseguita non è una procedura verificata.

## I runtime: Wine non è .NET, e non lo contiene

Qui sta la parte meno intuitiva, e riguarda direttamente il programma che stiamo installando. Wine implementa le interfacce di programmazione di Windows, cioè quello che Microsoft chiama Win32. Non implementa invece i due grandi ambienti di esecuzione che molte applicazioni moderne richiedono e che su Windows sono componenti separati anche là: il motore di rendering delle pagine web e il framework .NET[^3].

Per coprirli, il progetto Wine distribuisce due componenti a parte. Gecko è il motore di rendering, ed è la controparte del componente di Internet Explorer che molti programmi usano per mostrare una schermata di aiuto o un pannello. Mono è una implementazione libera del framework .NET, ed è la controparte del runtime che un programma scritto in .NET richiede per partire.

Nessuno dei due è dentro Wine, e su questa macchina nessuno dei due è nemmeno nel sistema.

```
/usr/share/wine/gecko        ASSENTE
/usr/share/wine/mono         ASSENTE
```

Il pacchetto `wine-mono` non esiste nei repository di Ubuntu, verificato con `apt-cache policy`, che non restituisce nulla. Quando mancano, Wine li scarica dal proprio sito al momento del bisogno, e il sito risponde `HTTP 200` da questa macchina, quindi la via è praticabile.

Una trappola di lettura va segnalata perché ci sono quasi cascato. Dentro il prefix appena creato esiste una cartella `gecko`, sia in `system32` sia in `syswow64`, e la sua presenza suggerisce che il componente sia installato. Non lo è: contiene soltanto una sottocartella `plugin`, cioè è un segnaposto che Wine crea comunque. La verifica corretta non è l'esistenza della cartella ma il suo contenuto, ed è la stessa lezione del confronto degli esempi di AKABAK, dove nomi di file identici non provavano contenuti identici finché non si sono confrontate le impronte.

## Che cos'è .NET, e perché VituixCAD lo richiede

Vale spiegarlo perché decide il passo successivo. Un programma scritto in un linguaggio come C non contiene altro che istruzioni per il processore: si esegue e basta. Un programma scritto per .NET contiene invece un codice intermedio, che non è istruzioni per il processore ma per una macchina astratta, e ha bisogno di un runtime che lo traduca mentre gira e che gli fornisca la libreria standard, la gestione della memoria e l'interfaccia grafica. Senza quel runtime il file esiste e non parte, e il messaggio d'errore tipicamente non nomina la causa.

VituixCAD 2 è una applicazione .NET, ed è anche la ragione per cui è a 64 bit mentre il suo installer è a 32: sono due programmi diversi, scritti in tempi e con strumenti diversi, e la regola corretta è guardare l'architettura dell'applicazione installata e non quella del suo installatore.

Le vie per fornirgli il runtime sono due e non equivalenti. La prima è Mono, cioè l'implementazione libera che Wine scarica da sé, leggera e integrata, che copre bene la maggior parte delle applicazioni .NET ma non tutte. La seconda è installare il vero .NET Framework di Microsoft dentro il prefix, cosa che `winetricks` sa fare con il verbo `dotnet48`: è più fedele e molto più pesante, scarica e installa un pacchetto Microsoft dentro il finto Windows, impiega parecchi minuti e storicamente è uno dei passi più fragili di qualunque configurazione Wine.

La scelta del progetto è provare prima Mono, e installare `dotnet48` soltanto se il programma non parte. Il ragionamento è asimmetrico e conviene renderlo esplicito: se Mono basta, si è evitato il passo più fragile della fase 8; se non basta, si sono persi pochi minuti e si è guadagnata la ragione per cui quel passo serve, invece di averlo eseguito per prudenza senza sapere se fosse necessario. La documentazione del corredo prescriveva `dotnet48` e `corefonts` per questo prefix, e quella prescrizione non è sbagliata: è non verificata, e la differenza fra le due cose è il tema ricorrente di questo progetto.

## Il rumore, e come si classifica

L'output di creazione di un prefix contiene molte righe che sembrano errori e non lo sono. Vale classificarle una volta, perché la stessa classificazione serve a ogni installazione successiva.

Le righe `err:ole` sul marshalling delle interfacce e su `RpcSs` riguardano il meccanismo con cui, su Windows, due processi si scambiano oggetti. Compaiono alla prima costruzione di un prefix, quando i servizi non sono ancora in piedi, e non impediscono nulla: la prova è che il prefix risulta completo.

Le righe `fixme` non sono errori per definizione: Wine le stampa per dichiarare che una certa funzione di Windows non è implementata e che l'esecuzione prosegue comunque.

Una riga merita una nota perché è stata oggetto di una inferenza poi confermata.

```
002c:err:setupapi:do_file_copyW Unsupported style(s) 0x10
```

In MS-085 questa riga era comparsa all'avvio di AKABAK, e l'avevo attribuita a un processo di servizio del prefix e non al programma, deducendolo dal fatto che portasse un identificativo di processo diverso da quello principale. Era una inferenza dai numeri e l'avevo dichiarata tale invece di darla per certa. La creazione di questo prefix la conferma per via indipendente: la stessa riga compare cinque volte durante la costruzione, quando nessun programma applicativo è in esecuzione e l'unica attività è il popolamento del finto Windows. Da inferenza marcata diventa fatto, ed è un buon esempio del perché convenga marcarle invece di scriverle come certezze: la conferma è arrivata da sola cinque giorni dopo, e sarebbe stata impossibile se la prima affermazione fosse stata scritta come fatto.

## Come si estende il pattern

Prima di installare un programma Windows in un prefix nuovo, la caratterizzazione del prefix va fatta e non assunta, e consiste in quattro letture che costano pochi secondi. Si legge la riga `#arch` del registro per sapere l'architettura reale del prefix. Si verifica la presenza dei runtime guardando il contenuto delle cartelle e non la loro esistenza, perché Wine crea segnaposto. Si stabilisce quale comando serva a quel prefix, cioè `wine` per i 64 bit e `wine32` per i 32. E si legge l'architettura dell'eseguibile installato con `file` a installazione finita, per confermare o smentire ciò che la documentazione del produttore afferma.

Il principio generale che tiene insieme tutto il documento è che un prefix è uno stato, non un percorso. Ogni volta che il progetto lo ha trattato come un percorso, cioè come una cartella da nominare in un comando, è emerso un difetto: il caricatore sbagliato perché il comando non guardava lo stato, la cartella padre mancante perché nessuno aveva eseguito il comando, il runtime assente perché la documentazione elencava dipendenze senza verificarle. Trattarlo come uno stato significa leggerlo prima di agirci dentro, ed è economico: quattro comandi contro un'ora di diagnosi.

[^1]: *prefix*, prefisso - la cartella che contiene l'intera installazione Windows simulata da Wine, con il proprio disco `C:`, il proprio registro e le proprie dipendenze; la variabile `WINEPREFIX` dice a Wine quale usare, e in sua assenza vale `~/.wine`.

[^2]: *WoW64*, Windows on Windows 64-bit - il sottosistema con cui un Windows a 64 bit esegue programmi a 32 bit; la cartella `syswow64` contiene le librerie di sistema a 32 bit, e il nome confonde perché su Windows `system32` contiene quelle a 64.

[^3]: *.NET* - piattaforma di esecuzione di Microsoft in cui i programmi non contengono istruzioni per il processore ma un codice intermedio, tradotto mentre gira da un runtime che fornisce anche libreria standard, gestione della memoria e interfaccia grafica; senza quel runtime il programma esiste e non parte.
