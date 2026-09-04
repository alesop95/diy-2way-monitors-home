# Fase 4: progettazione completa del monitor

> Quarta fase operativa, articolata in tre sotto-fasi. È il ramo del workflow che lavora in campo libero, cioè senza la stanza, e che produce la firma acustica del diffusore. Procede in parallelo al ramo della stanza e converge con esso nella fase 5.

## Perché qui la stanza non c'è

La separazione fra questa fase e quelle sulla stanza è deliberata e va tenuta ferma, perché mescolarle è l'errore che rende una progettazione non interpretabile. Qui si lavora sui parametri Thiele/Small dei driver, sulla direttività e sul crossover, e l'uscita attesa è la risposta del diffusore ideale in condizioni controllate. Solo quando quella risposta è nota si può chiedere che cosa la stanza le fa: se si progettasse direttamente dentro la stanza, non si potrebbe distinguere un difetto del diffusore da un effetto dell'ambiente.

## 4a: progettazione acustica in VituixCAD 2

VituixCAD è lo strumento centrale di questa fase. È completo, gestisce sistemi multivia, simula in camera anecoica virtuale e supporta direttività e risposta in potenza.

Il punto cruciale è la definizione congiunta del volume del box e del crossover, e l'approccio è ibrido fra dati di targa e misure reali. Si importano i parametri Thiele/Small dei driver e la risposta misurata dell'altoparlante in campo vicino, che si ottiene con REW; si definisce il volume del box e il tipo, cioè chiuso oppure bass reflex; si simula la risposta totale su pannello infinito insieme alla direttività; si simula il crossover, passivo o attivo, con la possibilità di importare la risposta reale del driver già montato in cassa. Le uscite sono la curva SPL e i diagrammi polari.

L'uso della risposta reale del driver in cassa, invece dei soli dati di targa, è la differenza fra una simulazione plausibile e una utile, perché il pannello frontale e il volume interno modificano la risposta del driver in modo che i parametri Thiele/Small da soli non catturano.

## 4b: progettazione meccanica in FreeCAD

La progettazione meccanica non è un passaggio di documentazione a valle: materiale, spessore e posizione dei driver influenzano risonanze e direttività, quindi retroagiscono sul risultato acustico.

Il lavoro consiste nel costruire il box con gli spessori dettati dal materiale scelto, inserire i fori del bass reflex o le eventuali guide d'onda secondo quanto stabilito in VituixCAD, e posizionare i driver sul pannello frontale. Le esportazioni servono a tre destinazioni diverse: il formato `.fcstd` è il progetto nativo che rimane la fonte modificabile, i formati `.stl` e `.step` servono al taglio a controllo numerico o alla stampa, e il formato `.dxf` serve ai pannelli da tagliare manualmente.

Il formato `.dxf` è quello che conta davvero per questo progetto, perché l'ipotesi di realizzazione registrata negli appunti è il taglio del legno da parte di un artigiano, non una fresatura a controllo numerico.

## 4c: ottimizzazione dell'accordo, e perché è opzionale

WinISD è più semplice di VituixCAD ed è ottimo per la progettazione del volume e dell'accordo bass reflex. Va però registrata la conclusione del documento sorgente, che è un giudizio di ridondanza: se si usano già VituixCAD e Akabak, WinISD è in buona parte superfluo, e quindi non serve propriamente in un workflow ottimizzato.

Questa conclusione ha una conseguenza sull'ambiente e vale renderla esplicita, perché è il tipo di semplificazione che si perde per inerzia. WinISD è il solo programma del corredo che richiede un prefix Wine a 32 bit, con i suoi runtime datati. Rinunciarvi elimina un prefix, una architettura da mantenere e una classe di problemi, cioè esattamente gli errori su `kernel32.dll` documentati nella pagina di troubleshooting. Su una installazione pulita conviene non installarlo, e aggiungerlo soltanto se emerge un bisogno concreto che gli altri due strumenti non coprono.

## Le decisioni di progetto già prese

Dagli appunti del progetto emergono alcune scelte che non sono ancora verificate in simulazione ma che orientano la fase, e vanno registrate come ipotesi di partenza e non come risultati.

La configurazione ipotizzata è a due vie con caricamento bass reflex, con un woofer da quattro pollici. Sulla dimensione del tweeter l'appunto originale dice quattro pollici come il woofer, che per un tweeter è una misura fuori scala e va letta come un errore di trascrizione: un tweeter a cupola per un due vie da nearfield sta tipicamente fra i tre quarti di pollice e l'oncia. La misura effettiva è una decisione ancora da prendere, e dipende dalla frequenza di incrocio che uscirà dalla fase 4a.

La definizione di una risposta target precede la scelta dei driver. Negli appunti la sequenza è dichiarata in questo ordine, e ha senso mantenerlo: prima si stabilisce dove si vuole arrivare, poi si cerca il woofer che permette di arrivarci. La scelta della curva target è a sua volta una decisione aperta, fra una risposta piatta e una curva con lieve enfasi sui bassi del tipo usato in ambito consumer.

Il materiale ipotizzato è MDF, con densità fra 700 e 750 chilogrammi per metro cubo e spessore dei pannelli fra 18 e 25 millimetri, valori che nella fase 5 servono direttamente come parametri di simulazione.

## Il criterio di uscita

Il traguardo quantitativo dichiarato per il diffusore, che vale come definizione di finito per questa fase e per la successiva, è una risposta lineare entro più o meno 2 dB in asse e fino a più o meno 10 gradi fuori asse, nell'intervallo da 60 Hz a circa 20 kHz.
