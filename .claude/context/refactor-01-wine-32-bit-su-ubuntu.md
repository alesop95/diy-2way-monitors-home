# Deep-dive 01: le quattro architetture di Wine, e perché tre su quattro non bastano

> Approfondimento della voce 1 di [studio-didattico-master.md](studio-didattico-master.md). Racconta per intero, con gli output reali dei comandi, perché AKABAK non partiva su un sistema in cui ogni singolo passo della procedura risultava eseguito correttamente, e perché la risposta stava in una distinzione che la documentazione del progetto non faceva. Contiene anche il ritiro di due affermazioni sbagliate che avevo scritto nel corso della diagnosi, con la causa di ciascuna.

## Il problema, come si è presentato

Dopo la reinstallazione del sistema, l'ambiente Wine era stato ricostruito seguendo l'ordine imposto da ADR-016: dichiarare l'architettura `i386`, poi installare Wine, poi usare un prefix a 32 bit, perché AKABAK è un eseguibile `PE32`[^1] e non a 64 bit. Ogni comando aveva risposto bene. L'architettura risultava dichiarata, Wine risultava installato in versione 10.0, e `wine --version` rispondeva senza errori.

Il primo avvio del programma è fallito con una riga sola.

```
wine: '/home/alesop95/.wine' is a 32-bit installation, it cannot support 64-bit applications.
```

Il messaggio va letto al contrario di come si è tentati di leggerlo, e questa inversione è il primo insegnamento della vicenda. Non dice che il prefix sia difettoso, e non dice che AKABAK sia a 64 bit. Dice che il *caricatore* che è stato avviato era quello a 64 bit, e che un caricatore a 64 bit non lavora dentro un prefix a 32 bit. Il soggetto della frase è il programma che sta parlando, non il prefix nominato.

## Le quattro architetture, che sono quattro e non una

La confusione che ha prodotto il difetto nasce dall'aver trattato come una cosa sola quattro proprietà indipendenti. Vale enumerarle, perché ciascuna si imposta con un comando diverso, si verifica con uno strumento diverso, e può essere giusta mentre le altre sono sbagliate.

La prima è l'architettura del sistema operativo, cioè quali architetture di pacchetto il gestore accetta di installare. Su Debian e derivate si dichiara con `dpkg --add-architecture` ed è una proprietà del sistema, non di Wine.

```bash
sudo dpkg --add-architecture i386 && dpkg --print-foreign-architectures
```

```
i386
```

La seconda è la presenza fisica del caricatore a 32 bit e delle sue librerie, cioè se sul disco esiste un eseguibile capace di far girare codice a 32 bit. Si installa con un pacchetto e si verifica con `dpkg -l`.

La terza è l'architettura del *prefix*, cioè della finta installazione di Windows dentro cui il programma vive. È scritta nel registro del prefix e non si cambia dopo la creazione.

```bash
grep -m1 "#arch" ~/.wine/system.reg
```

```
#arch=win32
```

La quarta, che è quella che mancava alla documentazione del progetto, è l'architettura del *comando* che si invoca. Un sistema può avere entrambi i caricatori installati e un prefix a 32 bit perfettamente valido, e fallire comunque, perché il comando digitato ha avviato il caricatore sbagliato.

Le prime tre erano giuste. La quarta era sbagliata, e nessun controllo della procedura la guardava.

## Il primo difetto: `--install-recommends` non installa i suggeriti

Prima di arrivare al comando, va raccontato un difetto precedente, perché è dello stesso genere e perché senza la sua correzione il problema successivo non si sarebbe nemmeno manifestato: sarebbe stato mascherato da un errore diverso.

La procedura prescriveva l'installazione con l'opzione che tira dentro i pacchetti raccomandati.

```bash
sudo apt install --install-recommends wine winetricks
```

L'esecuzione ha installato undici pacchetti e `wine --version` ha risposto `wine-10.0`. Il controllo di uscita che la fase 7 prescriveva era quindi soddisfatto. Ma nell'elenco dei pacchetti installati compariva `wine64` e non `wine32`, che stava invece nella sezione dei suggeriti.

```
Installing dependencies:
  cabextract          libcapi20-3t64  libz-mingw-w64
  fuseiso             libmspack0t64   wine-common
  libasound2-plugins  libwine         wine64

Suggested packages:
  ttf-mscorefonts-installer  dosbox
  q4wine                     wine32
```

La distinzione fra i tre livelli di dipendenza di apt[^2] è la causa, ed è una di quelle cose che si sanno e non si applicano. Le *dipendenze* sono obbligatorie. I *raccomandati* sono installati per impostazione predefinita, e `--install-recommends` li forza dove la configurazione li avesse disattivati. I *suggeriti* non vengono installati mai, se non nominandoli. Il metapacchetto `wine` di Ubuntu raccomanda `wine64` e si limita a suggerire `wine32`, quindi quell'opzione non poteva in nessun caso produrre un ambiente a 32 bit funzionante.

La verifica che lo dimostra, e che il controllo di uscita della fase non faceva.

```bash
dpkg -l wine32:i386 ; apt-cache policy wine32:i386
```

```
wine32:i386:
  Installed: (none)
  Candidate: 10.0~repack-12ubuntu1
```

Va notato che `Candidate` porta una versione mentre `Installed` è vuoto, e la coppia dice due cose diverse: il pacchetto è disponibile, quindi la dichiarazione dell'architettura ha funzionato, e non è installato, quindi il ramo a 32 bit non esiste sul disco. Prima di dichiarare `i386` la stessa interrogazione rispondeva `Candidate: (none)`, che è la conferma pratica dell'ordine imposto da ADR-016: quell'ordine non era una precauzione teorica, era la condizione perché il pacchetto fosse perfino nominabile.

La correzione è nominarlo.

```bash
sudo apt install wine32:i386
```

Il costo di quel comando merita una riga, perché spiega la scelta dei confezionatori invece di farla sembrare arbitraria: 263 pacchetti, 250 MB scaricati, 1,1 GB occupati. Il ramo a 32 bit non è un binario, è un intero albero di librerie parallelo che parte dalla `libc` e arriva a Mesa, GTK e GStreamer, perché un programma Windows a 32 bit sotto Wine finisce per chiamare, attraverso Wine, le librerie grafiche e audio del sistema, e le chiama a 32 bit. Chi installa Wine per programmi a 64 bit non vuole pagare quel gigabyte, e per questo il pacchetto è suggerito e non raccomandato. La conseguenza pratica è che su questa piattaforma un ambiente a 32 bit va chiesto, non ottenuto per inerzia.

## Il secondo difetto: il wrapper che scarta il caricatore che serve

Con il ramo a 32 bit installato, il comando è stato rilanciato e ha prodotto l'errore da cui questa pagina è partita. La spiegazione sta in come Ubuntu confeziona il comando `wine`, e si legge aprendo i file invece di supporli.

```bash
ls -la /usr/bin/wine ; ls -la /etc/alternatives/wine
```

```
/usr/bin/wine -> /etc/alternatives/wine
/etc/alternatives/wine -> /usr/bin/wine-stable
```

Il comando non è un eseguibile ma un collegamento che, attraverso il sistema delle *alternative* di Debian, arriva a uno script. Quello script è il punto in cui la decisione viene presa, ed è breve abbastanza da leggerlo per intero.

```sh
#!/bin/sh -e

wine64=/usr/bin/wine64
wine32=/usr/bin/wine32

if test -x $wine64; then
    wine=$wine64
    if test -z "$WINELOADER"; then
        export WINELOADER=$wine64
    fi
elif test -x $wine32; then
    wine=$wine32
else
    echo "error: unable to find wine executable, this shouldn't happen." >&2
    exit 1
fi

if test -z "$WINEDEBUG"; then
    export WINEDEBUG=fixme-all
fi

exec $wine "$@"
```

La condizione che conta è la prima. Se `wine64` è eseguibile, lo script lo usa e ne esporta il percorso in `WINELOADER`, e il ramo a 32 bit viene considerato soltanto nel caso in cui il primo *manchi*. Non c'è alcuna ispezione del prefix, alcuna lettura di `#arch`, alcun tentativo di indovinare l'architettura dell'eseguibile passato come argomento: la scelta è fatta sulla sola presenza del caricatore a 64 bit.

Ne segue la conseguenza che rende il difetto strutturale e non accidentale. ADR-016 impone di installare il ramo a 32 bit, quindi su questa macchina entrambi i caricatori esistono, quindi il comando `wine` sceglierà *sempre* quello a 64 bit. Su un prefix `win32` fallirà sempre. Non è una configurazione da correggere: è il comportamento previsto del wrapper, e va aggirato usando l'altro comando.

```bash
cat /usr/bin/wine32-stable
```

```sh
#!/bin/sh -e

if test -z "$WINEPREFIX"; then
   export WINEPREFIX="$HOME/.wine32"
fi

exec /usr/lib/i386-linux-gnu/wine/wine "$@"
```

Anche questo è uno script, e porta una trappola propria che va conosciuta prima di incontrarla: se `WINEPREFIX` non è definita, ne impone una sua, `~/.wine32`, che non è il prefix del progetto. Chi lanciasse `wine32` senza dichiarare il prefix si troverebbe dentro un prefix vuoto creato al volo, e concluderebbe che il programma non è installato. Il prefix va quindi sempre passato esplicitamente.

Il binario a cui lo script arriva è quello giusto, e `file` lo conferma.

```bash
file /usr/lib/i386-linux-gnu/wine/wine
```

```
ELF 32-bit LSB pie executable, Intel i386
```

La forma corretta del comando, che è il complemento operativo mancante di ADR-016.

```bash
WINEPREFIX=~/.wine wine32 "C:/Program Files/RDTeam/AKABAK/AKABAK.exe"
```

La prova non distruttiva che la catena regge, eseguita prima di avviare il programma vero.

```bash
WINEPREFIX=~/.wine wine32 --version
```

```
wine-10.0 (Ubuntu 10.0~repack-12ubuntu1)
```

La stessa interrogazione fatta con `wine` invece di `wine32` risponde anch'essa `wine-10.0`, e questo è precisamente il motivo per cui il controllo di uscita della fase 7 era inutile: la versione si legge senza caricare alcun prefix, quindi risponde bene anche su un ambiente incapace di eseguire il programma. Un controllo che passa su un sistema difettoso non è un controllo debole, è un controllo che misura la cosa sbagliata.

## Leggere l'output, e perché usando `wine32` diventa rumoroso

L'avvio riuscito ha prodotto una ventina di righe sul terminale, e vale imparare a classificarle perché a prima vista sembrano una diagnosi di guasto mentre sono il contrario.

```
00b8:err:setupapi:do_file_copyW Unsupported style(s) 0x10
0024:fixme:thread:GetThreadUILanguage : stub, returning default language.
0024:fixme:nls:RtlGetThreadPreferredUILanguages 00000038, 02D7D9DC, 00000000 02D7DA04
0024:fixme:system:NtUserSystemParametersInfo Unknown action: 8220
0024:fixme:wtsapi:WTSRegisterSessionNotification Stub 000300AA 0x00000000
0024:fixme:uxtheme:BufferedPaintInit Stub ()
0024:fixme:explorerframe:taskbar_list_SetProgressValue iface 043CA3F8, hwnd 000400CC, ullCompleted 0, ullTotal 64 stub!
```

Il campo che decide è il secondo, cioè il livello. Le righe `fixme` segnalano una funzione di Windows che Wine non implementa e per cui restituisce un valore plausibile: la lingua dell'interfaccia, l'indicatore di progresso sulla barra delle applicazioni, il disegno con doppio buffer, la registrazione alle notifiche di sessione. Sono informazioni per chi sviluppa Wine, non sintomi, e un programma complesso ne produce a decine senza che nulla vada storto. Le sole righe di livello `err` in questa esecuzione sono due, entrambe da `setupapi`, e riguardano un flag di stile nella copia di un file che Wine non riconosce: vengono dall'aggiornamento del prefix che Wine 10 ha eseguito sul prefix creato da Wine 9, cioè dalla migrazione, e non dal programma.

Il numero in testa a ciascuna riga è l'identificatore del thread, e la sua lettura chiarisce la sequenza: le due righe `err` portano identificatori diversi fra loro e diversi da tutte le altre, `00b8` e `002c` contro il `0024` del resto, quindi appartengono ai processi di servizio della migrazione e non al thread principale del programma.

Resta la domanda più utile, cioè perché queste righe compaiano affatto, dato che una esecuzione con `wine` sarebbe silenziosa. La risposta sta nella differenza fra i due script già letti sopra, in un punto che a prima vista sembra accessorio. Lo script a cui `wine` rimanda contiene anche questo.

```sh
if test -z "$WINEDEBUG"; then
    export WINEDEBUG=fixme-all
fi
```

Quella riga disattiva l'intero canale `fixme` quando l'utente non ha espresso una preferenza, ed è il motivo per cui l'uso normale di Wine su Ubuntu è silenzioso. Lo script `wine32` non la contiene: esegue direttamente il caricatore, quindi lascia il canale attivo. Il rumore non è quindi un sintomo della migrazione né del prefix, è un effetto collaterale del comando corretto, e chi passa da `wine` a `wine32` lo incontra sempre.

Ne segue una comodità operativa che vale scrivere accanto alla prescrizione, così che il rumore non venga letto come un problema in una sessione futura.

```bash
WINEDEBUG=fixme-all WINEPREFIX=~/.wine wine32 "C:/Program Files/RDTeam/AKABAK/AKABAK.exe"
```

La forma opposta serve quando qualcosa non va e si vuole vedere di più, per esempio per accertare quale driver grafico Wine stia usando, che è la maglia inferenziale non misurata della sezione precedente.

```bash
WINEDEBUG=+wayland WINEPREFIX=~/.wine wine32 --version
```

## Il prefix sopravvissuto, e perché la licenza era già dentro

La parte che ha reso questa vicenda un guadagno invece di un costo è indipendente dai due difetti, e discende dalla decisione presa all'inizio della reinstallazione: azzerare la radice e conservare `/home`.

Il prefix Wine di questa macchina vive in `~/.wine`, cioè dentro `/home`. L'azzeramento della radice ha portato via Wine, i suoi pacchetti e i suoi caricatori, e non ha toccato il prefix. Dentro quel prefix ci sono tre cose che sarebbero costate un pomeriggio a ricostruire: AKABAK installato, VACS installato, e la registrazione dell'attivazione, perché la licenza di questi programmi si scrive nel registro del prefix.

```bash
ls ~/.wine/drive_c/Program\ Files/RDTeam/AKABAK/
file ~/.wine/drive_c/Program\ Files/RDTeam/AKABAK/AKABAK.exe
```

```
PE32 executable for MS Windows
```

Prima di aprirlo con Wine 10 il prefix è stato copiato, perché la migrazione che Wine applica a un prefix creato da una versione molto precedente, qui la 9.0, è irreversibile.

```bash
cp -a ~/.wine ~/.wine-prima-di-wine10 && du -sh ~/.wine-prima-di-wine10
```

```
831M    /home/alesop95/.wine-prima-di-wine10
```

La migrazione è andata a buon fine e il programma si è aperto dichiarando `3.2.4 b126 - 32 Professional`. Ne segue che la fase 8 della procedura, che prevedeva di reinstallare i programmi e riattivare la licenza, si riduce a una verifica. Vale però registrare una discrepanza aperta invece di ignorarla: la documentazione del progetto afferma che l'edizione ottenuta sia Standard e non professionale malgrado il nome dell'installer, mentre la finestra dichiara `32 Professional`. Il numero e la lettera potrebbero indicare l'architettura seguita dall'edizione, oppure l'affermazione precedente potrebbe essere sbagliata. Non è verificato, e va accertato leggendo lo stato del release code dal menu di aiuto.

## Il display trovato senza `DISPLAY`, che sembra impossibile

Su questa parte avevo scritto una affermazione sbagliata e l'utente l'ha corretta con un fatto: il comando che apre la finestra è stato lanciato da una sessione remota via SSH[^3], e la finestra è comparsa sullo schermo della macchina. Io avevo scritto che andasse lanciato dal desktop, perché in una sessione SSH non c'è un display.

La misura mostra che l'ambiente della sessione remota è privo di entrambe le variabili che indicano un display.

```bash
ssh studio 'echo "DISPLAY=[$DISPLAY]"; echo "WAYLAND_DISPLAY=[$WAYLAND_DISPLAY]"; echo "XDG_SESSION_TYPE=[$XDG_SESSION_TYPE]"'
```

```
DISPLAY=[]
WAYLAND_DISPLAY=[]
XDG_SESSION_TYPE=[tty]
```

E mostra che il processo del programma, già in esecuzione, non ha ereditato nessuna delle due.

```bash
tr "\0" "\n" < /proc/20822/environ | grep -iE "display|wayland|xdg_runtime"
```

```
XDG_RUNTIME_DIR=/run/user/1000
```

La spiegazione sta nella variabile che *è* presente. La sessione remota eredita `XDG_RUNTIME_DIR`, che il gestore delle sessioni imposta per utente, e in quella cartella vive il socket del compositore grafico.

```bash
ls $XDG_RUNTIME_DIR/wayland-*
ls /tmp/.X11-unix/
```

```
/run/user/1000/wayland-0
/run/user/1000/wayland-0.lock
X0
```

Wine 10 porta due driver grafici, e il prefix non ne dichiara nessuno, quindi Wine li prova nell'ordine previsto dalla propria configurazione.

```bash
ls /usr/lib/i386-linux-gnu/wine/i386-windows/ | grep -iE "wayland|x11"
```

```
winewayland.drv
winex11.drv
```

La catena che ne risulta è questa, e la sua ultima maglia è la parte non ovvia. Il driver X11 chiede una connessione al display indicato da `DISPLAY`, che è vuota, quindi non può aprire nulla e viene scartato malgrado il socket `X0` esista. Il driver Wayland chiede una connessione al display indicato da `WAYLAND_DISPLAY`, che è vuota anch'essa, ma la libreria di Wayland in quel caso non fallisce: ricade sul nome predefinito `wayland-0` cercandolo dentro `XDG_RUNTIME_DIR`. Quel socket esiste, appartiene alla sessione Plasma dell'utente sulla macchina, e la finestra vi si attacca.

Questa ultima maglia è una inferenza fortemente sostenuta e non una misura diretta, e va dichiarata come tale: la prova definitiva sarebbe leggere i descrittori aperti del processo, cosa che richiede privilegi non disponibili nella sessione non interattiva, oppure rilanciare il programma con la tracciatura del driver Wayland attiva. Ciò che è misurato è che le due variabili sono assenti, che `XDG_RUNTIME_DIR` è presente, che il socket `wayland-0` esiste al suo interno e che il processo gira.

La lezione operativa è di portata generale e vale oltre Wine: su un sistema con sessione grafica attiva, una sessione remota che eredita `XDG_RUNTIME_DIR` può aprire finestre sul display dell'utente senza che alcuna variabile di display sia impostata, perché il nome predefinito del socket è una convenzione e non un caso particolare. La conseguenza da tenere presente è simmetrica e meno gradevole: un comando lanciato per errore da remoto può comparire sullo schermo di chi è fisicamente davanti alla macchina.

## I due ritiri, e la causa precisa di ciascuno

Nel corso di questa diagnosi ho scritto due affermazioni false, entrambe registrate e poi corrette, e vanno riportate qui perché la causa di ciascuna è una regola generale.

La prima è quella sul display appena raccontata: avevo dichiarato che una sessione SSH non ha display, che è vero per le variabili d'ambiente e falso per la raggiungibilità del compositore. L'errore è di aver trasformato una condizione tipica in una impossibilità. La regola che ne discende è che l'assenza di una variabile d'ambiente non dimostra l'assenza della risorsa che quella variabile indica, perché quasi ogni protocollo ha un valore predefinito.

La seconda è più istruttiva perché ha prodotto anche una correzione inutile su file reali. Avevo affermato che i due lanciatori sulla scrivania della macchina fossero rotti, in quanto invocavano il programma con il nome `wine-stable`, che credevo inesistente su questo sistema, e li avevo corretti a `wine` registrando la cosa come un difetto risolto.

```
Exec=env WINEPREFIX="/home/alesop95/.wine" wine-stable C:\\\\users\\\\Public\\\\Desktop\\\\AKABAK.lnk
```

Il file `/usr/bin/wine-stable` esiste, è installato dal pacchetto `wine`, ed è esattamente lo script a cui `/usr/bin/wine` rimanda attraverso il sistema delle alternative. I due nomi sono lo stesso programma, quindi la mia correzione non ha cambiato niente, e soprattutto ha lasciato intatto il difetto reale: entrambe le forme finiscono nel caricatore a 64 bit, quindi entrambi i lanciatori avrebbero fallito sul prefix a 32 bit con lo stesso messaggio incontrato a riga di comando. La correzione giusta è `wine32`, ed è quella applicata dopo la diagnosi.

La causa del mio errore è precisa e ripetibile, e per questo vale enunciarla come regola. Avevo verificato l'inesistenza del *pacchetto* `wine-stable` con `apt-cache policy`, che è il controllo giusto per la riga di installazione, e avevo trasferito quella conclusione al *binario* senza rifare la misura con lo strumento adatto. Sono due domande diverse su due oggetti diversi: `apt-cache policy` risponde sui pacchetti, `ls` e `command -v` rispondono sui file eseguibili. In Debian e derivate la distinzione è tutt'altro che accademica, perché il sistema delle alternative fa esistere nomi di comando che non corrispondono ad alcun pacchetto omonimo, ed è precisamente il caso incontrato qui.

## Come estendere il pattern

Tre prescrizioni discendono da questa pagina e valgono per ogni programma Windows a 32 bit che il progetto aggiungerà.

La prima riguarda la forma dei comandi. Ogni comando rivolto a un prefix a 32 bit si scrive con `wine32` e con `WINEPREFIX` dichiarato esplicitamente, senza eccezioni, e questo include `winecfg`, `wineboot` e `winetricks`, che sono anch'essi caricati dal wrapper e soggetti alla stessa scelta. Per un prefix a 64 bit il comando `wine` va bene, e la differenza va scritta accanto a ciascun prefix nella tabella della procedura invece di essere ricordata.

La seconda riguarda i controlli di uscita. Un controllo che interroga la versione di uno strumento non prova che lo strumento sappia fare il lavoro, e questa vicenda ne è il terzo esempio in questo progetto dopo il nome del kernel nella fase 6 e la lettura dei file dei limiti realtime invece di `ulimit`. La forma corretta di un controllo di uscita è eseguire l'operazione che deve funzionare, o interrogare lo stato che la rende possibile, e per il ramo a 32 bit di Wine quello stato è `dpkg -l wine32:i386` uguale a installato.

La terza riguarda l'installazione di pacchetti. Prima di scrivere una riga di installazione in una procedura, i nomi dei pacchetti si verificano sull'archivio della distribuzione di destinazione e non su quello che era attivo sulla macchina precedente, e il livello di dipendenza va guardato: un pacchetto necessario che il metapacchetto si limita a suggerire va nominato esplicitamente, perché nessuna opzione lo tirerà dentro.

[^1]: *PE32*, Portable Executable a 32 bit - il formato degli eseguibili di Windows nella sua variante a 32 bit, riconoscibile con il comando `file`, che lo riporta come `PE32 executable`. La variante a 64 bit si chiama `PE32+`.

[^2]: *apt*, Advanced Package Tool - il gestore di pacchetti di Debian e derivate. Distingue tre livelli di dipendenza fra pacchetti: le dipendenze, obbligatorie; i raccomandati, installati per impostazione predefinita; i suggeriti, mai installati automaticamente.

[^3]: *SSH*, Secure Shell - protocollo per aprire una sessione di comando su una macchina remota attraverso una connessione cifrata, qui usata con autenticazione a chiave e in modo non interattivo.
