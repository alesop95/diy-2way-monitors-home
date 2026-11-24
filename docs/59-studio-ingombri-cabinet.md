# Studio degli ingombri dei cabinet sullo ST-120

Specifica esplorativa del 2026-11-19, sviluppata nell'autonomia richiesta dall'utente. Si confrontano inviluppi meccanici prima di selezionare driver o ordinare pannelli. Le quote nominali verificate sono ripiano 1180 × 300 mm, superficie a 930 mm da terra, da `data/postazione-st120.json`. Le rientranze posteriori non sono quotate: entrare nel rettangolo nominale è una condizione necessaria e non dimostra l'appoggio sull'intera sagoma reale.

## Domanda e alternative

Il primo box proposto, 230 × 300 × 360 mm, ruotato di 30°, occupa circa 349 × 375 mm in pianta. La profondità nominale del ripiano è 300 mm. Occorre quindi esplorare cabinet meno profondi, un angolo diverso o un'altra forma di appoggio. La richiesta attuale mantiene i diffusori sul ripiano superiore; questo studio confronta soltanto soluzioni che rispettano l'inviluppo rettangolare, senza introdurre stativi come acquisto implicito.

Si usano due scenari di schermo esterno: larghezza 540 mm, rappresentativa da verificare per 24 pollici, e 620 mm, rappresentativa da verificare per 27 pollici. La diagonale non determina esattamente la larghezza del telaio o della base. Full HD resta sufficiente nella proposta e l'acquisto è differito. Altezza e piedistallo dello schermo non sono inventati per questo controllo in pianta.

Le ipotesi di studio sono spessore uniforme 18 mm, margine laterale esterno 10 mm per lato, margine anteriore e posteriore 10 mm e luce orizzontale schermo/cabinet 10 mm per lato. Non sono tolleranze di costruzione o distanze acustiche prescritte. Le tre varianti sono A24 220 × 190 × 430 mm a 30°, B27 190 × 180 × 430 mm a 30°, C24 240 × 200 × 440 mm a 20°. Le sigle indicano lo scenario di confronto, non un modello approvato.

## Calcolo e informazioni da non confondere

Con W larghezza, D profondità e angolo theta rispetto alla parete frontale, la scatola rettangolare ruotata occupa `Bx = W*cos(theta) + D*sin(theta)` e `By = W*sin(theta) + D*cos(theta)`, per angoli compresi fra 0° e 90°. Per una coppia simmetrica, la massima larghezza schermo conservativa è `1180 - 2*Bx - 2*10 - 2*10`. L'intero inviluppo deve rientrare anche fra Y=10 e Y=290.

Il volume interno geometrico è `(W-2*t)*(D-2*t)*(H-2*t)`. È lordo: mancano gli spostamenti di driver, condotto, rinforzi, morsetti e assorbente, e non è il volume acustico definitivo. Lo studio rende disponibili i valori netti solo come sensibilità a una sottrazione esplicita, senza presentarla come misura. Non si deducono risposta a 60 Hz, sensibilità, potenza o impedenza.

I cabinet sono centrati in profondità sul ripiano e simmetrici fra gli estremi. Il centro della faccia anteriore si sposta rispetto al centro della scatola quando la si ruota: il calcolo degli assi usa questo spostamento, non la sola separazione delle bounding box. L'intersezione sul piano orizzontale è una costruzione geometrica con assi passanti per il centro del baffle; posizione e altezza effettiva del tweeter restano aperte. Angolo nullo produce assi paralleli e nessuna intersezione finita.

## Modello e uscite richieste

Ogni box ha sei pannelli con giunzioni di testa ideali: frontale e posteriore a piena larghezza e altezza; fianchi fra le due facce, a piena altezza; cielo e fondo fra i fianchi e le due facce. Il modello deve verificare dimensioni, somma dei volumi, assenza di sovrapposizioni volumetriche e contatti. Non ha fori o fresature finché i componenti non sono scelti. La distinta è un risultato di studio, non un ordine al falegname.

FreeCAD produce sorgente FCStd con proprietà ed espressioni dimensionali, STEP reimportato e un rapporto letto esplicitamente. La prova di un parametro deve ricomputare almeno un volume e una dimensione, poi ripristinare il progetto. CADCraft 0.20.1, rilevato localmente, produce o verifica i profili 2D. Il catalogo non offre estrusione o esportazione di solidi STEP: la voce solid è una faccia 2D e non sostituisce FreeCAD per questo risultato.

Le tavole distinguono inviluppo, pannelli e ipotesi; la grafica usa il design system di account. I file generati restano in build o nella cartella privata delle prove, con sorgenti e configurazione versionati. Non è prevista nessuna scrittura su file preesistenti nella home Ubuntu o sugli originali dell'utente.

## Dati necessari per passare al progetto esecutivo

Restano sagoma effettiva nelle rientranze, posizione del tavolo e delle pareti, seduta e quota orecchie, ingombro del monitor acquistato e relativo piedistallo, carico ammissibile sul ripiano e appoggi antivibranti. Driver, volume netto e altezza dell'asse acustico vanno verificati insieme. Il solo modello delle scatole non certifica stabilità al ribaltamento, isolamento meccanico, portata del tavolo o prestazione acustica.

## Risultati misurati nel modello

| Variante | W × D × H mm | Angolo | Base X × Y mm | Schermo massimo mm | Volume lordo L |
|---|---|---|---|---|---|
| A24 | 220 × 190 × 430 | 30° | 285,53 × 274,54 | 568,95 | 11,164 |
| B27 | 190 × 180 × 430 | 30° | 254,54 × 250,88 | 630,91 | 8,737 |
| C24 | 240 × 200 × 440 | 20° | 293,93 × 270,02 | 552,14 | 13,516 |
| Prima ipotesi | 230 × 300 × 360 | 30° | 349,19 × 374,81 | 441,63 | 16,594 |

A24 e C24 rientrano nello scenario schermo 540 mm; B27 rientra anche nello scenario 620 mm. Il dato è relativo all'intero telaio, non alla diagonale. La prima ipotesi fallisce già in profondità e la sua maggiore capacità interna non la rende collocabile così sul ripiano. Togliendo per sola sensibilità 1,5 L di occupazione interna, le tre alternative rimangono circa 9,664, 7,237 e 12,016 L: l'occupazione reale non è ancora nota.

Le superfici nette dei dodici pannelli delle due scatole sono rispettivamente 0,756624, 0,663184 e 0,844864 m². Non comprendono sfridi, incisioni, colla, rinforzi o assorbente. Non sono un prezzo o un piano di taglio di un foglio commerciale.

I tre modelli FreeCAD hanno superato volume, contatti, variazione +10 mm della larghezza, ripristino e riapertura; il STEP contiene sei solidi con volume e coordinate attesi. Uno spostamento intenzionale di 20 mm è stato rilevato dal controllo della posizione. I profili CADCraft riaperti hanno tre contorni chiusi, aree e perimetri attesi e unità in millimetri. La variante con scala errata del 5% è stata rifiutata. Le viste assonometriche e le piante sono state ispezionate: per ogni pianta è verificata direzione camera [0,0,-1], per ogni documento dodici pannelli visibili e processo terminato 0.

La verifica finale è stata eseguita in prima persona: l'avvio del secondo revisore separato è stato bloccato dal controllo della quota, che riportava 83% con riserva da 80%. Mille rettangoli ruotati sono stati confrontati con i quattro vertici trasformati, senza divergenze. Per le tre varianti il volume totale del legno FreeCAD coincide con le aree dei DXF CADCraft moltiplicate per quantità e spessore; l'intersezione degli assi risulta davanti al centro baffle trasformato. Questo non equivale a una seconda revisione indipendente del codice, né alla verifica fisica del progetto.

## File e sequenza ripetibile

L'indice locale di consultazione è `build/consegna-cabinet-20261119/confronto.html`: tre alternative, immagini, file nativi, STEP, DXF e distinte esplorative. Funziona senza rete. Le viste finali usano colori e font del design system di account; i profili SVG conservano la geometria nativa del CAD. Il file MANIFEST-SHA256.json del pacchetto elenca dimensioni e impronte dei contenuti.

I comandi di calcolo e produzione dei profili sono stati eseguiti dalla radice del repository sulla postazione Windows. Ogni destinazione deve essere nuova:

```powershell
python tools/test_studia_ingombri.py
python tools/studia_ingombri.py --out build/studio-cabinet-20261119
python tools/cabinet-cadcraft.py --out build/studio-cabinet-20261119/profili-2d-v3
python tools/rendi-studio-cabinet.py --dir build/consegna-cabinet-20261119
```

Sul computer Ubuntu sono stati trasferiti nella cartella nuova i due generatori matematico/CAD e il JSON. `<CARTELLA_PROVA>` è il percorso restituito da mktemp; i percorsi reali e le configurazioni di prova rimangono nel livello privato. La forma seguente corrisponde ai comandi eseguiti; il controllo negativo cambia sia la destinazione sia i file di configurazione del CAD.

```bash
DIY_CABINET_CONFIG=<CARTELLA_PROVA>/studio-st120.json DIY_CABINET_OUT=<CARTELLA_PROVA>/modelli ~/.local/opt/freecad-1.1.4/FreeCAD_1.1.4-Linux-x86_64-py311.AppImage freecadcmd -u <CARTELLA_PROVA>/user.cfg -s <CARTELLA_PROVA>/system.cfg <CARTELLA_PROVA>/genera-cabinet-freecad.py
DIY_CABINET_CONFIG=<CARTELLA_PROVA>/studio-st120.json DIY_CABINET_OUT=<CARTELLA_PROVA>/negativo DIY_CABINET_TEST_SHIFT_X=20 ~/.local/opt/freecad-1.1.4/FreeCAD_1.1.4-Linux-x86_64-py311.AppImage freecadcmd -u <CARTELLA_PROVA>/user-negative.cfg -s <CARTELLA_PROVA>/system-negative.cfg <CARTELLA_PROVA>/genera-cabinet-freecad.py
```

Il primo rapporto esito.json deve dichiarare success e tre varianti, il secondo failed con posizione sinistra 30 invece di 10. Il launcher ha restituito 0 anche nel negativo: da solo non è il verdetto. La macro `tools/cabinet-vista.FCMacro` usa un display Xvfb e configurazioni GUI isolate, attiva il documento corretto, acquisisce l'assonometria e attende la fine della transizione prima di verificare e acquisire la pianta. Il file con vista è una nuova copia FCStd; l'originale generato dalla console resta conservato.

## Troubleshooting osservato

Il primo test dei contatti usava l'area della booleana comune fra solidi tangenti; nel kernel della prova risultava zero. La diagnostica misura le quindici coppie, distingue distanza zero e volume nullo e verifica per i soli pannelli rettangolari il contatto di faccia attraverso gli intervalli delle bounding box. Il caso di spigolo non viene contato come faccia.

Il primo screenshot mostrava la pianta e una scala troppo ridotta: la selezione della sottofinestra cambiava la vista attiva e venivano mostrati anche elementi d'origine. La macro limita gli oggetti visibili e imposta la vista dopo l'attivazione. La chiamata getCameraNode richiedeva i wrapper Pivy/Coin: aggiunto l'import dopo il messaggio No SWIG wrapped library loaded. La prima cattura chiamata pianta avveniva ancora durante l'animazione e mostrava l'assonometria; un callback successivo verifica ora la direzione -Z prima di salvare. Le immagini finali sono state ispezionate.

Il primo profilo 2D aveva testi sovrapposti. Tre righe brevi per ciascun gruppo hanno corretto la leggibilità. Il percorso assoluto del font era stato accettato ma trueType risultava false: usare il nome del file del font installato ha risolto il carattere Altro Grotesk Book, confermato dal rapporto del programma. L'esportazione ora fallisce se il font richiesto non è risolto. Il browser senza finestra ha richiesto l'esecuzione fuori sandbox dopo un errore di accesso negato; l'anteprima locale isolata è stata acquisita e letta.
