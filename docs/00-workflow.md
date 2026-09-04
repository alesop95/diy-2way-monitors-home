# Il workflow in otto fasi

> Inquadramento architetturale dell'intero progetto. Descrive che cosa entra e che cosa esce da ogni fase, con quale strumento, e perché quella fase esiste. Le pagine numerate successive entrano nel dettaglio operativo di ciascuna.

## L'idea di fondo

Il progetto non parte dal diffusore ma dalla stanza, e questa è la scelta che ne determina tutta la forma. Un monitor da studio commerciale è progettato per essere neutro in campo libero e poi subisce la stanza dell'utente; qui l'ordine si inverte, perché la stanza è nota, non è trattabile acusticamente e non è modificabile nell'arredo, quindi diventa un vincolo di progetto invece di un disturbo. Si misura la stanza, si costruisce un modello geometrico che riproduce le misure reali, si progetta il diffusore in campo libero, e solo alla fine si rimettono insieme i due blocchi per ottimizzare il posizionamento.

Da questa impostazione discende la divisione del lavoro fra i due rami. Il ramo della stanza produce un modello validato: misura reale in REW[^1], geometria in Blender, analisi modale in Octave, e il confronto fra modo predetto e picco misurato è il criterio di validazione. Il ramo del diffusore produce una firma acustica: parametri Thiele/Small[^2] dei driver, volume e accordo del box, crossover e direttività in VituixCAD. I due rami convergono in Akabak, che è l'unico strumento gratuito capace di simulare in un solo passaggio la parte elettroacustica e quella ambientale.

## La sequenza

La tabella riassume le otto fasi nella forma ingresso, uscita, strumento e tecnica, così come erano state fissate nel documento sorgente.

| Fase | Ingresso | Uscita | Strumento | Tecnica |
|---|---|---|---|---|
| 1. Misura reale | microfono calibrato, scheda audio | IR `.wav`, FR `.txt`, sessione `.mdat` | REW | sweep logaritmico 20 Hz - 20 kHz, deconvoluzione IR, RT60, C50/C80, EDT |
| 2. Modellazione CAD | misure della stanza in centimetri | modello 3D `.blend`, `.obj`, `.dae` | Blender | geometria di pareti, mobili, schermo e punto di ascolto |
| 3. Simulazione acustica | dimensioni stanza, IR dei driver | frequenze modali, mappe SPL | MATAA su Octave | image-source, ray tracing, modali |
| 4a. Progettazione acustica | parametri T/S, IR misurata, risposta target | volume box, accordo, SPL, direttività | VituixCAD, WinISD sotto Wine | simulazione box e crossover |
| 4b. Progettazione meccanica | volume e accordo dalla 4a | `.fcstd`, `.stl`, `.step`, `.dxf` | FreeCAD | pannelli, spessori, fori, sede dei driver |
| 5. Simulazione finale | modello stanza più modello monitor | SPL al punto di ascolto, mappe di comb filtering | Akabak 3 sotto Wine | integrazione diffusore e stanza, verifica delle angolazioni |
| 6. Acquisto driver | specifiche dalla 4a | woofer e tweeter reali | - | selezione su parametri T/S convalidati in simulazione |
| 7. Montaggio | pannelli dalla 4b | cabinet costruito | - | taglio del legno e assemblaggio |
| 8. Verifica finale | monitor costruiti | scostamento fra progetto e realizzazione | REW | nuova misura al punto di ascolto |

## Perché questo insieme di strumenti

La regola di scelta è stata prendere nativo Linux tutto ciò che si può, e ricorrere a Wine soltanto dove non esiste un equivalente serio. Nativi sono REW, Blender, Octave con MATAA e FreeCAD, e su Ubuntu Studio hanno il vantaggio della gestione a bassa latenza di JACK[^3], PulseAudio e PipeWire, che per la catena di misura conta. Sotto Wine restano tre programmi: VituixCAD, che non ha equivalente libero per il crossover multivia con direttività, Akabak, che è l'unico gratuito a fare elettroacustica e acustica ambientale insieme, e WinISD, che è comodo per l'accordo bass reflex ma è in buona parte ridondante se si usano già gli altri due.

Questa divisione ha una conseguenza pratica sul carico di lavoro dell'ambiente: la parte fragile del setup non è Linux, è Wine, e per questo l'ambiente ha una cartella di documentazione propria invece di una nota a margine.

## Lo stato di avanzamento

Il documento sorgente era ricco sulle fasi da 1 a 5 e povero sulle fasi da 6 a 8, che restavano quasi interamente in forma di segnaposto. Questa asimmetria non è un difetto della conversione ma lo stato reale del progetto: la parte simulativa è pensata, la parte di acquisto e costruzione non ancora. La roadmap in `.claude/context/roadmap.md` riprende questo punto e lo trasforma in ordine di priorità.

[^1]: *REW*, Room EQ Wizard - software gratuito di misura acustica che ricava la risposta all'impulso di un ambiente da uno sweep sinusoidale e ne deriva i parametri di riverberazione e chiarezza.

[^2]: *T/S*, Thiele/Small - insieme di parametri elettromeccanici che descrivono il comportamento di un altoparlante a bassa frequenza e permettono di simularlo come circuito equivalente.

[^3]: *JACK*, JACK Audio Connection Kit - server audio a bassa latenza tipico dell'audio professionale su Linux, che instrada i segnali fra applicazioni con un ritardo deterministico.
