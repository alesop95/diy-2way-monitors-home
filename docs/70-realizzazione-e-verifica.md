# Fasi 6, 7 e 8: acquisto, montaggio e verifica finale

> Le tre fasi finali del workflow, raccolte in una pagina perché nel documento sorgente esistono quasi soltanto come intestazioni. Questa pagina dichiara che cosa manca invece di riempirlo, e definisce che cosa ciascuna fase dovrà produrre.

## Lo stato reale di queste tre fasi

Va detto senza attenuazioni: nel documento sorgente le fasi 6, 7 e 8 erano segnaposto. La fase 6 aveva un titolo e un paragrafo di lettere ripetute. La fase 7 aveva un titolo, una sottosezione intitolata ai pannelli di legno e un altro segnaposto. La fase 8 aveva una sola frase di contenuto reale. Anche la sotto-fase 4b, la progettazione meccanica, era in condizioni simili nella parte di ingressi e uscite.

Questa asimmetria non è un difetto della conversione. Riflette lo stato del progetto: la parte simulativa è pensata in profondità, la parte fisica non è ancora iniziata. Registrarla come vuota è più utile che riempirla di contenuto plausibile, perché una pagina inventata verrebbe letta come una decisione presa.

Alle tre fasi si aggiunge un secondo filone appena abbozzato nel sorgente, la personalizzazione di un amplificatore per il basso, che aveva un titolo, una sottosezione sul modello e nessun contenuto. È fuori dallo scopo del progetto dei monitor e resta annotato come possibile lavoro separato.

## Fase 6: acquisto dei driver

Che cosa dovrà produrre: una coppia di woofer e una coppia di tweeter reali, scelti perché i loro parametri Thiele/Small sono quelli su cui la fase 4a ha convalidato il progetto.

Le decisioni che la precedono e che oggi sono aperte. La curva di risposta target va fissata prima, perché è il criterio con cui si giudica un candidato. Il diametro e le caratteristiche del woofer derivano dal volume del box e dall'accordo che la simulazione avrà stabilito; l'ipotesi di partenza registrata negli appunti è quattro pollici. Il tweeter dipende dalla frequenza di incrocio che uscirà dalla fase 4a.

Un vincolo di reperibilità è già noto e va tenuto presente perché può cambiare la scelta: gli appunti registrano che il canale di approvvigionamento professionale usato in passato non è più disponibile, e che l'alternativa ipotizzata è il recupero da magazzino tramite un ex collega. Questo rende la disponibilità un parametro di selezione reale accanto alle specifiche, e suggerisce di verificare che cosa è ottenibile prima di ottimizzare il progetto su un driver che non si può comprare.

## Fase 7: montaggio

Che cosa dovrà produrre: i due cabinet costruiti secondo i disegni della fase 4b.

L'ipotesi di realizzazione registrata negli appunti è il taglio dei pannelli di legno da parte di un artigiano, non una fresatura a controllo numerico. È la ragione per cui il formato `.dxf` è, fra le esportazioni di FreeCAD, quella che conta davvero: sono i pannelli da tagliare a misura.

Le decisioni aperte sono il materiale definitivo, con l'MDF fra 18 e 25 millimetri come ipotesi di partenza già usata come parametro nelle simulazioni, il metodo di assemblaggio e la tenuta d'aria, che in un caricamento bass reflex incide direttamente sull'accordo, e lo smorzamento interno, che nella fase 5 è modellato come schiuma acustica o fibra di poliestere e va scelto in coerenza con quanto simulato.

## Fase 8: verifica finale

Che cosa dovrà produrre: la misura dello scostamento fra il progetto simulato e l'oggetto costruito.

La procedura è la stessa della fase 1, con la stessa catena di misura e nello stesso punto di ascolto, ed è precisamente per questo che la fase 1 va documentata con cura: la ripetibilità del setup di misura è ciò che rende confrontabili le due misure a distanza di mesi. Il file di sessione `.mdat` della prima misura conserva quel contesto, e va conservato per questo motivo.

Il criterio di giudizio è la distanza dal criterio di uscita già dichiarato per le fasi 4 e 5, cioè una risposta lineare entro più o meno 2 dB in asse e fino a più o meno dieci gradi fuori asse, da 60 Hz a circa 20 kHz. Lo scarto fra quel bersaglio e la misura reale è il risultato del progetto.

Un passaggio ulteriore, non presente nel sorgente ma coerente con gli strumenti disponibili, chiude il cerchio: una volta misurato il monitor costruito, quelle misure possono diventare un file GLL tramite EASE SpeakerLab o un software di misura come ARTA. Da quel momento il diffusore autocostruito è simulabile come un prodotto commerciale, e il limite discusso nella pagina della fase 2, cioè l'assenza di un GLL per un progetto DIY, cade.

## Il correttivo, che è l'ultima decisione aperta

Gli appunti registrano una domanda mai risolta, e vale lasciarla come domanda invece di risolverla d'ufficio: se dopo la verifica finale resta uno scostamento, lo si corregge intervenendo sul crossover, oppure con una equalizzazione digitale nella catena di ascolto, oppure accettandolo.

Il progetto ha una posizione implicita, perché la sua premessa è progettare il diffusore in funzione della stanza invece di correggere a posteriori, e questo spinge verso l'intervento sul crossover. La decisione però dipende da quanto grande sia lo scarto e da dove cada in frequenza, quindi non si può prendere prima di avere la misura.
