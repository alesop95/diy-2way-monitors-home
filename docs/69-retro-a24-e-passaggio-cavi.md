# Retro A24 e passaggio delle quattro vie

Revisione del 27 novembre 2026, MS-326. La piastra rimovibile porta le due coppie di potenza in ciascun cabinet chiuso. Lo [schema del cablaggio](68-cablaggio-quattro-vie.md) assegna le coppie ai finali V3. Qui si definiscono geometria, servizio e ingombro sullo Stagecaptain ST-120. Le quote sono candidati di progetto con rilascio costruttivo sospeso.

La [tavola PDF](figure/retro-a24-20261127/retro-a24.pdf) mostra retro, dettaglio della piastra e sezione laterale. Il [DXF in millimetri](figure/retro-a24-20261127/retro-a24.dxf) è modificabile. I [dati](../config/cabinet/retro-a24.json) mantengono separati quote del costruttore e riserve nominali. Il [rapporto](figure/retro-a24-20261127/riscontro.json) lega la rilettura CAD alle impronte dei file.

## Connettore e coppie di potenza

Il candidato è Neutrik NL4MPXX, flangia D con quattro contatti e linguette piatte per capicorda. La spina candidata NL4FXX-W-S ammette, secondo il costruttore, guaina da 6 a 12 mm e conduttori da 1,5 a 4 mm². Si prevede un cavo a quattro conduttori per cassa e una diramazione nei pressi dei finali. Guaina, sezione effettiva, lunghezza e capicorda si scelgono sul layout. [NL4MPXX](https://www.neutrik.com/en/product/nl4mpxx), [NL4FXX-W-S](https://www.neutrik.com/en/product/nl4fxx-w-s).

| Contatto | Coppia interna | Cabinet L | Cabinet R |
|---|---|---|---|
| 1+ | LF+ | P05+ | P07+ |
| 1- | LF- | P05- | P07- |
| 2+ | HF+ | P06+ | P08+ |
| 2- | HF- | P06- | P08- |

Le marcature dei contatti distinguono le due coppie, isolate l'una dall'altra e dal telaio. Etichettare le estremità dei cavi con L/R e LF/HF e confermare la continuità verso ciascun V3 prima di alimentare. Il connettore porta potenza audio ai driver. [Istruzioni BDA 594](https://www.neutrik.com/media/14195/download/BDA%20594%20V1%20-%20speakON%20NL4MPXX%20%26%20NL4MPXX-3.pdf?v=2).

## Piastra, giunzioni e tenuta

Il pannello posteriore rimane MDF 220 × 430 × 18 mm nel modello A24. Coordinate della tavola: `u` da sinistra guardando il retro, `z` dal fondo, `y` dal frontale verso il posteriore. L'asse `x` del modello guarda il mobile dal fronte e vale `220-u`. Tutte le coordinate sono in millimetri. Nel modello `y=172-190` appartiene alla parete posteriore.

| Parte | Specifica di studio per cassa | Verifica da fare |
|---|---|---|
| Apertura MDF | Ø50 passante, centro `u=110`, `z=75` | Permette accesso a corpo e connessioni. Rilevare il passaggio dei capicorda e lo spazio per estrarre la piastra. |
| Piastra | Alluminio piano 80 × 70 × 3, centrato sul foro | Prova di rigidezza all'inserimento e presa per la manutenzione. |
| Flangia | Foro Ø24,2, 2 passaggi M3 Ø3,4 | Il costruttore indica minimi Ø24 e Ø3,2. Centri su diagonale, interassi 19 ±0,1 e 24 ±0,1. |
| Piastra su MDF | 4 passaggi M4 Ø4,5 nella piastra, centri a `u±31`, `z±26` dal centro | Inserti ciechi candidati. Lunghezza, utensile e diametro pilota dal fissaggio reale. |
| Guarnizioni | Anello continuo Ø50/60 tra piastra e MDF, guarnizione flangia compatibile | Controllare appoggio piano, compressione e tenuta anche con la spina scollegata. |

La diagonale M3 è in alto a sinistra e in basso a destra nella vista dall'esterno del cabinet. Il disegno Neutrik della foratura è riferito al lato morsetti, quindi va specchiato orizzontalmente per questa vista. Il montaggio qui previsto è frontale sulla piastra, con viti svasate e dado verificato per accesso. Il massimo di 0,6 N·m del produttore riguarda il montaggio frontale del NL4MPXX. Il serraggio dei quattro fissaggi nel legno richiede una scelta distinta. [Disegno 20002406](https://www.neutrik.com/media/14283/download/20002406.pdf?v=2), [istruzioni di montaggio](https://www.neutrik.com/media/14195/download/BDA%20594%20V1%20-%20speakON%20NL4MPXX%20%26%20NL4MPXX-3.pdf?v=2).

Il foro nel MDF lascia 32 mm rispetto alla giunzione più vicina, al fondo. Rimane circa 1,50 mm di materiale fra foro centrale e passaggi M3. È un margine nominale piccolo, da controllare con dima e tolleranze reali. L'anello di tenuta ha 5 mm di margine minimo fino al bordo della piastra. I fissaggi M4 stanno oltre l'anello. Si mantiene la giunzione di testa incollata del nominale con contatto continuo sui bordi del retro. I quattro inserti vanno verificati in un provino di MDF da 18 mm, con profondità utile e riserva verso l'interno. La tavola indica soltanto i centri nel legno. Il volume geometrico dell'apertura vuota è 0,035 L, prima dell'occupazione del connettore. La tenuta e il volume netto effettivi richiedono il montaggio.

## Passaggio interno e spazio sul tavolo

Il connettore e le linguette nude sporgono nominalmente 27,3 mm dietro il piano di montaggio. Si riserva per terminali e curva una zona interna di 50 × 65 × 50 mm dalla faccia esterna della piastra, che arriva fino a `y=128`. L'inviluppo resta 39,7 mm oltre la profondità massima dei driver nel modello e 101 mm sotto il rinforzo. La coppia LF rimane sotto il rinforzo. La coppia HF risale attraverso la finestra esistente con asse candidato `u=150`, `y=130`, raggio di riserva 8 mm e margine nominale di 14 mm dal bordo della finestra. Fissare la guaina e lasciare un'ansa per estrarre la piastra. Staffette, lunghezze, accesso e curva dei conduttori restano da dimensionare sul campione.

Il ripiano superiore noto dello Stagecaptain ST-120 misura 1.180 × 300 mm e ha superficie a 930 mm dal pavimento. Il piano principale misura 1.180 × 600 mm. Le due viste della postazione mostrano una parete dietro il ripiano e il bordo posteriore in parte coperto. Il confronto usa le quote nominali già verificate del tavolo. La distanza parete-mobile rimane un dato aperto. [Quote ST-120](../data/postazione-st120.json).

Il disegno della spina indica fino a 82,5 mm complessivi. Si riservano 110 mm dalla faccia esterna della piastra, includendo il terminale montato e uno spazio di progetto per il cavo. È una riserva da verificare in funzione della curva ammessa dal cavo scelto. A 30° la profondità proiettata del cabinet da solo vale `220 sin(30°) + 190 cos(30°) = 274,5 mm`. Con la piastra da 3 mm e il punto terminale della riserva sull'asse centrale la proiezione arriva a `110 sin(30°) + (190+3+110) cos(30°) = 317,4 mm`. L'asse da solo supera di 17,4 mm l'inviluppo rettangolare del ripiano, prima di margini o spessore del cavo. Il risultato riguarda il contenimento di cabinet e cavo sul ripiano. Resta possibile valutare una discesa del cavo oltre il bordo se il retro è libero. [Disegno spina 20003841](https://www.neutrik.com/media/17072/download/NL4FXX-W-S.pdf?v=1).

## Verifica e rilascio

CADCraft ha riaperto 13 profili e ne ha confrontato centri, aree e perimetri. Il DXF con diagonale M3 specchiata ha stessi diametri e superfici, ma centri sbagliati, ed è stato rifiutato. Il PDF è stato visto dopo il controllo. [Copertura delle fonti](../research-vault/catena-riferimento-20261126/c02-retro-a24.md).

La distinta per la coppia comprende due piastre, due prese, due spine, quattro fissaggi M3 e otto punti di ancoraggio M4, più guarnizioni e otto terminazioni interne sui contatti. I fissaggi dei driver mantengono i centri nominali del capitolo 64. Prima di autorizzare il taglio servono il riscontro sul campione della piastra, la tenuta, la verifica dei percorsi interni e lo spazio per innesto, sgancio e curva dei cavi sullo ST-120. Se la riserva posteriore manca, si confronta prima un'uscita a ingombro ridotto o orientata al basso. Le verifiche fisiche restano differite per ADR-055.
