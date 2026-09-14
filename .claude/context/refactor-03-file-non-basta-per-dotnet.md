# Come si legge l'architettura di un programma, e perché per .NET il modo ovvio dà la risposta sbagliata

> Approfondimento della voce 3 di `studio-didattico-master.md`. È scritto per essere letto da capo senza conoscenze preliminari: parte da che cos'è un file eseguibile e arriva al motivo per cui un comando corretto ha prodotto una conclusione falsa su VituixCAD. Gli output sono reali, raccolti il 2026-09-14.

## Il problema, in una frase

Abbiamo installato VituixCAD e abbiamo controllato se fosse un programma a 32 o a 64 bit. Il controllo che la documentazione prescriveva ha risposto trentadue. La risposta giusta è sessantaquattro. Il controllo non era rotto e il comando non ha sbagliato: rispondeva a una domanda diversa da quella che stavamo ponendo, e le due domande hanno la stessa risposta per quasi tutti i programmi, ma non per quello.

Se ci fossimo fermati lì avremmo concluso che il prefix a 64 bit fosse un errore, lo avremmo distrutto e rifatto a 32, e avremmo passato il pomeriggio a capire perché il programma non partiva.

## Primo mattone: che cos'è un file eseguibile

Un file eseguibile non contiene soltanto le istruzioni del programma. Comincia con una *intestazione*, cioè una zona iniziale di lunghezza fissa che descrive il resto del file: dove cominciano le istruzioni, quanta memoria serve, quali librerie esterne servono, e per quale tipo di processore il programma è stato compilato. Il sistema operativo legge l'intestazione prima di eseguire qualunque cosa, e se non la riconosce si rifiuta di partire.

Su Windows quel formato si chiama PE[^1]. Ha una particolarità storica che conta qui: esistono due varianti dell'intestazione, una per i programmi a 32 bit e una per quelli a 64. Si chiamano `PE32` e `PE32+`, e il comando `file` di Linux le sa distinguere.

```
AKABAK.exe    PE32 executable for MS Windows 4.00 (GUI), Intel 80386
```

Per AKABAK questa riga è la risposta completa: è un programma a 32 bit, e infatti gira in un prefix a 32 bit, come ADR-016 aveva stabilito. Per un programma compilato in modo tradizionale, l'intestazione e l'architettura di esecuzione sono la stessa cosa, perché le istruzioni dentro il file sono già istruzioni per un processore preciso e non possono essere altro.

## Secondo mattone: che cosa cambia con .NET

Un programma tradizionale contiene istruzioni macchina, cioè numeri che il processore esegue direttamente. Il compilatore le ha prodotte una volta per tutte scegliendo il processore di destinazione, e quella scelta è congelata nel file.

Un programma scritto per .NET[^2] funziona diversamente. Il compilatore non produce istruzioni macchina: produce un *codice intermedio*, cioè istruzioni per una macchina astratta che non esiste in hardware. Quel codice viene tradotto in istruzioni vere soltanto quando il programma parte, da un componente chiamato runtime, che è installato sul sistema e non dentro il programma. È lo stesso principio di Java, se il paragone aiuta.

Da questo discende la cosa che ci ha ingannati. Se le istruzioni vere vengono prodotte al momento dell'avvio, la scelta dell'architettura non deve più essere fatta al momento della compilazione: può essere rimandata all'esecuzione. Un programma .NET può quindi dichiarare "vado bene per entrambe, decidi tu", e quella dichiarazione si chiama *AnyCPU*. Su una macchina a 64 bit il runtime lo esegue a 64 bit; sulla stessa macchina a 32 bit lo eseguirebbe a 32.

Il formato del file, però, è rimasto quello di Windows, che nasce prima di .NET e conosce solo due varianti. Un assembly[^3] AnyCPU viene scritto nella variante `PE32`, cioè quella che per un programma tradizionale significherebbe trentadue bit, perché è la variante predefinita e perché deve poter partire anche su un sistema a 32 bit. L'intestazione dice quindi `PE32` per due categorie di programmi profondamente diverse: quelli che sono davvero a 32 bit e quelli che decidono dopo.

## Che cosa abbiamo visto su VituixCAD

Il comando prescritto ha risposto così.

```
VituixCAD.exe   PE32 executable for MS Windows 4.00 (GUI), Intel i386 Mono/.Net assembly
```

Due informazioni, e chi legge in fretta ne prende una sola. La prima è `PE32`, che per un nativo significherebbe 32 bit. La seconda è `Mono/.Net assembly`, ed è precisamente la clausola che rende la prima non conclusiva: `file` ci sta dicendo che quel file non è un programma tradizionale, quindi che la sua prima affermazione non risponde alla domanda che gli abbiamo posto.

## Dove sta la risposta vera

Un assembly .NET porta, dentro il file, una seconda intestazione che descrive la parte .NET e che il formato Windows non conosce. La si raggiunge attraverso una tabella che il PE contiene proprio per questo, cioè un elenco di puntatori a strutture aggiuntive; la voce numero quattordici di quell'elenco indica l'intestazione del runtime CLI[^4], che è quella che ci interessa.

Dentro quella intestazione c'è un campo di flag, cioè di interruttori acceso e spento, e tre di essi decidono la questione. `ILONLY` dice che il file contiene solo codice intermedio e nessuna istruzione macchina. `32BITREQUIRED` dice che il programma pretende di girare a 32 bit. `32BITPREFERRED` dice che preferisce i 32 bit pur potendo fare altrimenti.

La lettura si fa così. Se `32BITREQUIRED` è spento, il programma è AnyCPU e gira alla larghezza della macchina, quindi a 64 bit qui. Se è acceso e `32BITPREFERRED` è spento, il programma è a 32 bit e basta. Se sono accesi entrambi, è AnyCPU ma preferisce i 32 bit e li userà dove può.

Su VituixCAD il valore misurato è questo.

```
flag CLI:              0x00000001
  ILONLY:              True
  32BITREQUIRED:       False
  32BITPREFERRED:      False
architettura reale:    AnyCPU, gira a 64 bit su una macchina a 64 bit
```

Solo `ILONLY` acceso. Il programma è AnyCPU, gira a 64 bit, il prefix a 64 bit è giusto, e la documentazione che lo affermava aveva ragione. Ciò che era sbagliato non era l'affermazione ma il modo prescritto per verificarla.

## Perché lo abbiamo trasformato in uno strumento

La lettura di quei flag non è memorizzabile e non si improvvisa: richiede di sapere dove sta la tabella delle directory, che la voce è la quattordicesima, che l'indirizzo lì scritto è virtuale e va tradotto in posizione nel file attraverso la tabella delle sezioni, e quali tre bit guardare. È esattamente il genere di conoscenza che si perde fra una sessione e l'altra, e che rifatta a mano produce errori.

Per questo è diventata `tools/arch-dotnet.py`. Lo strumento fa quella lettura e dichiara l'esito in parole; se l'intestazione CLI manca dichiara che il file è nativo e riporta l'architettura del formato, che per un nativo è la risposta corretta. È stato provato su tre casi e non su uno, perché uno strumento provato sul solo caso che lo ha motivato non è provato: su VituixCAD risponde AnyCPU a 64 bit, su AKABAK risponde nativo a 32 bit, e su un file che non è un eseguibile risponde che manca la firma iniziale ed esce con un codice di errore.

## Il principio generale, che vale oltre questo caso

È la quarta volta che questo progetto incontra la stessa forma di difetto, e le quattro occorrenze messe in fila la rendono riconoscibile.

La prima è stata il controllo di uscita della fase 7, che era `wine --version`: risponde con la versione di Wine senza caricare alcun prefix, quindi rispondeva correttamente anche su un sistema incapace di eseguire il programma. La seconda è stata la verifica dei limiti realtime leggendo i file che li dichiarano invece di `ulimit`: i file erano scritti correttamente e i limiti non erano in vigore, perché l'utente non apparteneva ai gruppi necessari. La terza è stata il nome del kernel come prova della bassa latenza, quando la bassa latenza viene dai parametri di avvio e non dal nome. La quarta è questa.

Le quattro hanno in comune una struttura precisa: il controllo misura una proprietà correlata a quella che interessa, la correlazione regge nella maggior parte dei casi, e quando non regge il controllo non fallisce ma risponde con sicurezza la cosa sbagliata. È la ragione per cui un controllo che passa non è mai, di per sé, una notizia: la domanda da porsi è se quel controllo potrebbe passare anche nel caso che deve escludere.

La forma difendibile, e la regola che il progetto adotta, è che un controllo di uscita deve fare una di due cose. O esegue l'operazione che deve funzionare, e allora la sua riuscita è la prova cercata. Oppure interroga direttamente la condizione che abilita quell'operazione, e allora va verificato che la condizione sia davvero quella e non una che le somiglia. Nel caso di oggi la seconda via esisteva ed è quella che abbiamo costruito: i flag CLI sono la condizione vera, mentre la variante dell'intestazione PE è quella che le somiglia.

## Che cosa c'entra tutto questo con due diffusori

Vale ricordarlo perché in un documento su intestazioni di file si perde di vista. VituixCAD serve alla fase 4a, cioè a progettare il crossover, che è la rete di filtri che divide il segnale fra woofer e tweeter. Il punto delicato di un crossover è la regione attorno alla frequenza di incrocio, dove entrambi i driver suonano insieme: se le loro risposte non si sommano in fase, là si apre un buco, e in un monitor da nearfield è il difetto più udibile di tutti. VituixCAD è lo strumento che permette di vedere quella somma prima di costruire, tenendo conto anche di come cambia fuori asse.

Se avessimo creduto al controllo sbagliato, avremmo distrutto il prefix corretto per rifarlo a 32 bit, e il programma non sarebbe partito. Mezza giornata per una lettura fatta con lo strumento giusto ma con la domanda sbagliata.

[^1]: *PE*, Portable Executable - il formato dei file eseguibili di Windows; comincia con una intestazione che descrive il resto del file e dichiara fra l'altro per quale tipo di processore il programma è stato compilato.

[^2]: *.NET* - piattaforma di Microsoft in cui il compilatore non produce istruzioni per un processore ma un codice intermedio, tradotto in istruzioni vere al momento dell'avvio da un componente chiamato runtime, installato sul sistema e non dentro il programma.

[^3]: *assembly* - il nome che .NET dà a un proprio file compilato, sia esso un programma o una libreria; non ha relazione con il linguaggio assembly, ed è un caso di omonimia che confonde spesso.

[^4]: *CLI*, Common Language Infrastructure - la specifica standardizzata su cui .NET poggia; l'intestazione CLI dentro un file PE descrive la parte .NET del file, ed è raggiunta attraverso la quattordicesima voce della tabella delle directory del PE.
