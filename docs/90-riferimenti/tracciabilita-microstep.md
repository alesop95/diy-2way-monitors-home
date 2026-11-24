# Perché ogni microstep serve a due monitor: la catena che lega il registro al progetto

> Pagina di raccordo. Il registro dei microstep dice che cosa è stato fatto, come è stato verificato e con quale esito, ma non dice a quale fase del progetto ciascun intervento serva, e a leggerlo di seguito si ha l'impressione di un lavoro di sistemistica che ha perso di vista il proprio scopo. Questa pagina fornisce il legame mancante, per blocchi e non voce per voce, e dichiara la convenzione che lo rende esplicito nei microstep successivi.

## Perché questa pagina esiste, e perché non si è corretto il registro

La lacuna è reale e va nominata invece di essere aggirata: fino a MS-096 la maggior parte delle voci spiega il perché tecnico dell'intervento, cioè perché quel comando e non un altro, e non il perché di progetto, cioè che cosa di due diffusori da costruire dipenda da quell'intervento. Chi legge il registro dall'inizio incontra fini riga, prefix Wine, allineamenti al template e diagnosi di driver grafici, e può legittimamente chiedersi dove siano finiti gli altoparlanti.

La correzione non poteva però essere la riscrittura delle voci passate, per due ragioni. La prima è che la convenzione del registro lo vieta esplicitamente: non si riscrive una voce passata, e se un intervento successivo la corregge si aggiunge una voce nuova che dichiara di superarla. La seconda è che una riscrittura di novantasei voci fatta a posteriori produrrebbe un documento che sembra essere sempre stato giusto, che è precisamente il difetto che questo progetto evita quando ritira una inferenza invece di cancellarla.

La forma corretta è quindi additiva: il legame si fornisce qui, una volta, per blocchi omogenei, e si rende obbligatorio d'ora in avanti.

## La catena, dall'obiettivo all'ambiente

L'obiettivo è una coppia di monitor da studio a due vie per un punto di ascolto domestico noto, con una risposta lineare entro più o meno 2 dB in asse e fino a più o meno dieci gradi fuori asse, da 60 Hz a circa 20 kHz, misurata al punto di ascolto reale e non in campo libero. Da questo obiettivo discende tutto il resto, e conviene percorrere la catena all'indietro perché è così che si capisce perché si passa il tempo su Wine.

La misura al punto di ascolto reale, e non in campo libero, implica che la stanza entri nel progetto come vincolo e non come disturbo: è ADR-002, ed è la scelta che dà forma a tutto. Se la stanza entra nel progetto, serve un modello della stanza validato contro una misura reale, che è il ramo delle fasi 1, 2 e 3. E serve uno strumento capace di mettere insieme il modello della stanza e il modello del diffusore in un solo calcolo, perché il comportamento al punto di ascolto non è la somma di due simulazioni fatte separatamente: è la fase 5.

Quello strumento è Akabak, e la ragione per cui il progetto gli dedica tanta documentazione è che è l'unico gratuito a fare elettroacustica e acustica ambientale insieme. Akabak è un programma Windows, non ha equivalente libero per questo compito, e la stessa cosa vale per VituixCAD nella fase 4a, dove serve il crossover multivia con la direttività. Ne discende che il progetto ha bisogno di Wine, e che la parte fragile del setup non è Linux ma Wine: è la ragione per cui l'ambiente ha una cartella di documentazione propria invece di una nota a margine.

Da qui la conseguenza che spiega la forma del registro. Ogni ora spesa a capire perché il comando `wine` scelga il caricatore sbagliato, o dove un programma scriva le proprie preferenze, non è lavoro di sistemistica che ha sostituito il progetto: è la condizione perché la fase 5 possa essere eseguita. Un ambiente che non parte rende il progetto non eseguibile, non più lento.

## La mappa per blocchi

Aggiornamento del 2026-11-20. La mappa originaria sotto rimane una spiegazione dei blocchi storici; i passaggi recenti si collegano così al progetto. I numeri sono ricercabili nel [registro completo](../OPERATIONS-LOG.md), che conserva comandi, esiti e rettifiche.

| Microstep | Fase e dipendenza costruttiva |
|---|---|
| MS-233-236 | Requisiti e postazione: proposta condivisa, quote ufficiali del ripiano, schermo economico e supporto del falegname. Alimentano gli ingombri della fase 4. |
| MS-237-242 | Quattro vie software, backup e CPU: capacità e reversibilità dell'ambiente che esegue simulazioni e DSP. Nessuna prestazione acustica dimostrata. |
| MS-243-245 | Strumenti posseduti, CAD e autonomia documentata: inventario della catena e strumenti della fase 4b. |
| MS-246-258 | DSP persistente, guasti osservati, controlli negativi e ripristino: rendono ripetibile il banco della fase 4a e distinguono servizio disponibile da audio effettivo. |
| MS-259-263 | Cabinet parametrici, viste, profili e trasferimento: confronto degli ingombri prima del CAD esecutivo e dei tagli. |
| MS-264-269 | Consegna, riavvio e ripetizione dei collaudi: verifica di persistenza prima di portare a casa la macchina; guasto MIDI separato. |
| MS-270-274 | Diagnosi e correzione FluidSynth con controllo senza note: recupero della funzione musicale condivisa con l'home recording e preparazione del backup. |
| MS-275-277 | Backup riletto, copia esterna e pulizia autorizzata: conservazione del setup e dei modelli, con impronte e spazio recuperato. |
| MS-278 | Uso quotidiano CamillaDSP: collega stereo, quattro uscite e quattro canali di potenza, lasciando esplicite le parti hardware mancanti. |
| MS-279-281 | Fonti primarie, modello LR4 e manuale esteso: motivano la scelta PC/Pi/analogico, dimostrano le proprietà ideali e mostrano perché la fase 8 richiederà misure reali. La mappa documentale collega cronaca, procedure e didattica. |
| MS-282 | Copertura dell'indice, link, PDF e controlli finali: conserva prove e limiti della consegna, distinguendo i rilievi generali di chiusura dalle misure acustiche ancora mancanti. |
| MS-283-285 | Requisito di autonomia obbligatorio, ritiro della diagnosi errata del KO e progetto dei due host: collegano sorgenti esterne, clock, canali e volume alla catena condivisa. |
| MS-286-287 | Modelli dei driver e dodici elaborazioni con controesempio: sviluppano la base di componenti e profili per la fase 4, mantenendo aperta la qualificazione fisica della fase 8. |
| MS-288-289 | LaTeX/PDF leggibili, artefatti identificati e controlli di chiusura riparati: rendono riutilizzabile il progetto teorico e verificabile la sua consegna. |

La mappa è per blocchi omogenei e non voce per voce, perché molti microstep servono lo stesso scopo e ripeterlo novantasei volte sarebbe rumore. Per ogni blocco si dichiara a quale fase del workflow serve e che cosa sarebbe impossibile senza di esso.

*Impianto documentale, indicativamente da MS-001 a MS-014 e da MS-017 a MS-020.* Conversione del documento sorgente in un albero navigabile, verifica che la copertura sia integrale, impianto degli strumenti di verifica e delle regole. Serve tutte le fasi e, soprattutto, serve il secondo esito dichiarato del progetto, che non è l'oggetto ma la comprensione: un percorso documentato che spieghi perché ogni scelta è stata fatta, riutilizzabile su un progetto successivo. Senza questo blocco il progetto avrebbe un documento sorgente in formato binario, non diffabile e non verificabile, e la catena delle decisioni vivrebbe nella memoria di una persona sola.

*Accesso alla macchina e sua fotografia, indicativamente MS-008, MS-015, MS-016 e da MS-027 a MS-033.* La macchina Ubuntu Studio è il luogo dove girano le fasi da 1 a 5. Senza accesso remoto amministrarla costa una sessione fisica per ogni comando; senza la fotografia dello stato iniziale la decisione fra aggiornare e reinstallare sarebbe stata presa al buio, e dopo la formattazione quelle informazioni non sarebbero più state recuperabili. Questo blocco ha inoltre prodotto la scoperta che ha corretto tre decisioni successive, cioè che Akabak è a 32 bit.

*Corredo software e trasferimento, indicativamente da MS-021 a MS-026, MS-034 e da MS-039 a MS-048.* Il corredo contiene gli installer di VituixCAD per la fase 4a, di EASE Focus con il database dei GLL, di ARTA per la fase 8, e il database dei GLL è materiale della fase 5 quando si confronta il proprio diffusore con modelli commerciali. Il trasferimento verificato per impronta è ciò che consente di cancellare le copie esterne senza perdere nulla, ed è la ragione per cui esiste PA-010.

*Licenza di Akabak, indicativamente MS-050, da MS-051 a MS-053, MS-085, MS-089 e MS-094.* Akabak è lo strumento della fase 5 e la sua licenza è legata all'identificativo della macchina. Verificare che il codice sopravviva alla reinstallazione non è pignoleria amministrativa: se non fosse sopravvissuto, la fase 5 sarebbe stata bloccata da una trattativa con l'autore del software invece che da un problema tecnico, e la reinstallazione stessa sarebbe stata una scelta da rivedere.

*Reinstallazione del sistema, indicativamente da MS-059 a MS-077.* Il sistema precedente era su un rilascio fuori supporto, quindi ogni intervento successivo avrebbe accumulato attrito, e la ricostruzione pulita dell'ambiente Wine risolveva nello stesso passaggio i guasti registrati. La conservazione di `/home` è la parte che si è rivelata decisiva per il progetto, perché ha fatto sopravvivere il prefix Wine con i programmi installati e la licenza attiva, riducendo le sottofasi 8.1, 8.2 e 8.4 a verifiche.

*Ambiente Wine, indicativamente MS-050, da MS-081 a MS-087, MS-090 e da MS-093 a MS-096.* È il blocco che a leggerlo sembra più lontano dagli altoparlanti ed è quello senza il quale le fasi 4a e 5 non esistono. Le scoperte di questo blocco hanno una conseguenza diretta sul lavoro di progettazione: il comando corretto per un prefix a 32 bit decide se Akabak parte, il modo di trasferimento verso VACS decide come si guardano i risultati di ogni iterazione della fase 5, e la cartella di lavoro decide dove si accumulano i dati spettrali di quelle iterazioni.

*Catena audio e interfaccia, indicativamente MS-030, MS-035, MS-036 e MS-079.* La fase 1 è la misura reale della stanza con microfono calibrato, e la fase 8 è la verifica finale con lo stesso strumento. Entrambe richiedono un ingresso microfonico con alimentazione phantom, che questa macchina non ha: è il solo blocco del progetto che non dipende da lavoro ma da un acquisto, tracciato come PA-012, e da esso dipende la scelta del microfono in un ordine non invertibile. I parametri di avvio e i limiti realtime verificati in questo blocco servono perché una misura acustica con buffer sottodimensionati produce artefatti che si scambiano per comportamento della stanza.

*Igiene documentale e strumenti, indicativamente MS-014, MS-056, MS-062, MS-063, MS-071, MS-078, MS-088, MS-091 e MS-092.* Questo blocco non serve alcuna fase del progetto, e dirlo è più onesto che forzare un legame. Serve il secondo esito dichiarato, cioè che la documentazione resti affidabile: uno strumento tipografico che corrompe i file che deve correggere, o un registro che mescola fini riga, degradano il documento che dovrà spiegare fra un anno perché il crossover è quello e non un altro.

## La convenzione, valida dai microstep successivi

Dal 2026-09-14 ogni microstep nuovo dichiara in apertura, subito dopo il perimetro, a quale fase del workflow serve e che cosa del progetto dipenda da esso. La forma è una frase, non una sezione, e quando l'intervento non serve alcuna fase lo dichiara, come fa il blocco dell'igiene documentale qui sopra: un legame inventato è peggio di un legame assente, perché fa credere che tutto sia giustificato.

La convenzione è scritta anche nella sezione `Convenzione` del registro, così che chi scrive una voce nuova la trovi dove la cerca invece che in questa pagina.

## Riordino con conservazione, MS-292/294

Il nuovo blocco serve il secondo esito del progetto, cioè poter ricostruire e imparare ogni scelta, e trasversalmente le fasi che dipendono da manuali e dati. MS-292 collega identità delle fonti e usi senza sostituire la bibliografia; MS-293 comprime le prove superate mantenendo percorsi e impronte; MS-294 riunisce metodo, lezioni e catalogo. I percorsi storici `build/...` ricollocati si ritrovano nel manifesto `_notes/archivio-prove/20261120/manifest.json` e nel corrispondente ZIP. Nessuna voce cronologica precedente viene corretta per far sembrare che l'archivio esistesse già.

## Controllo quotidiano e accesso ai report, MS-308 e successivi

Serve le fasi DSP/integrazione PC e autonomia, con qualifica fisica sospesa. MS-308 definisce il piano e riusa le dipendenze disponibili; MS-309/311 documentano normalizzazione, FIFO, pannello, prove e figura del basso; MS-312 chiude la guardia del grafo e la perdita di identità. I passi successivi registrano la correzione delle finestre PCM, la consegna documentale e il gate. Il manuale 61 contiene procedure e limiti, il deep dive 8 le motivazioni e STATO-PROGETTO i collegamenti a tutti i report tematici e alle simulazioni. Non esiste un nuovo registro concorrente di pendenze.
