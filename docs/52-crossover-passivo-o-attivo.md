# Crossover passivo o attivo: il confronto per questo progetto

> Decisione del 2026-10-02: attivo, con il crossover in un processore digitale, registrata come ADR-033. La scelta del modulo e la verifica del suo software su Linux sono PA-024. Il confronto che segue è quello su cui la decisione è stata presa, e resta com'era.

> Documento di confronto scritto il 2026-10-01 su richiesta dell'utente, che aveva dato per scontato un crossover passivo e ha chiesto di vedere le due strade prima di decidere. Non prende la decisione: la prepara. Le affermazioni generali vengono dalle fonti elencate in fondo, ciascuna con il suo stato di lettura; quelle sul progetto vengono dai documenti del repository. La trattazione matematica sta nel report LaTeX, capitolo sul crossover.

## Che cosa cambia fra le due architetture

Un diffusore a due vie divide il segnale fra un woofer, che riproduce le frequenze basse e medie, e un tweeter, che riproduce le alte. Il crossover è il filtro che fa la divisione, e la differenza fra le due architetture è dove sta rispetto all'amplificazione.

Nel passivo il filtro sta dopo l'amplificatore. Un amplificatore di potenza stereo alimenta ciascun cabinet con un solo cavo, e dentro il cabinet una rete di induttanze, condensatori e resistenze manda le basse al woofer e le alte al tweeter. Il filtro lavora a livello di potenza, con le correnti che muovono gli altoparlanti.

Nell'attivo il filtro sta prima dell'amplificazione, sul segnale di linea. Ogni altoparlante ha il proprio canale di amplificazione, collegato direttamente alla bobina, quindi ogni cabinet ospita due amplificatori e il filtro che li precede. Il filtro si realizza in due modi: con circuiti analogici ad amplificatori operazionali, oppure con un processore digitale di segnale[^1] che calcola filtri ricorsivi in forma di biquad[^2] e può aggiungere ritardi ed equalizzazione.

Il lavoro di progettazione acustica è lo stesso nei due casi: si misurano gli altoparlanti, si simulano le risposte nel programma di progetto e si scelgono pendenze e frequenza di incrocio. Cambia ciò che il progetto produce. Nel passivo sono valori di componenti da saldare, nell'attivo sono parametri di filtri analogici oppure coefficienti da caricare nel processore. VituixCAD, il programma di questo progetto per la fase 4a, supporta entrambe le strade: il suo manuale elenca resistenze, condensatori e induttanze passivi con le loro perdite, blocchi di filtro attivo Butterworth, Bessel e Linkwitz-Riley, e blocchi biquad digitali i cui coefficienti si esportano per processori di più costruttori.

## Il passivo, che è l'ipotesi da cui l'utente partiva

Il suo vantaggio principale è la semplicità d'uso: il cabinet finito è un oggetto che si collega a qualunque amplificatore, senza alimentazione propria, senza software e senza un apparecchio da configurare. È la forma più diffusa nei progetti fatti in casa, ed è quella su cui la documentazione pratica è più abbondante.

Il suo limite tecnico è che il filtro vede come carico l'altoparlante, e l'impedenza di un altoparlante non è una resistenza: varia con la frequenza, ha un picco alla risonanza e sale con l'induttanza della bobina alle frequenze alte. Una rete calcolata su un carico nominale da 8 ohm non incrocia dove dovrebbe; per questo il progetto passivo si fa sull'impedenza misurata di ciascun altoparlante, e spesso chiede reti di compensazione dell'impedenza che aggiungono componenti e perdite. Rod Elliott aggiunge due effetti da conoscere: la rete presuppone un amplificatore con impedenza d'uscita prossima a zero, e la resistenza della bobina cresce con la temperatura quando si suona forte, spostando il comportamento del filtro. I componenti hanno tolleranze, che si pagano in precisione o in costo, e le induttanze in serie al woofer hanno una resistenza che si somma a quella dell'altoparlante.

Per questo progetto il passivo ha una conseguenza già scritta in ADR-012: la sorgente della catena di ascolto è un'uscita di linea a circa 2 Vrms, che non può pilotare un altoparlante. Serve quindi un amplificatore di potenza stereo esterno, che oggi non c'è e diventerebbe una voce degli acquisti di fine percorso secondo ADR-027.

## L'attivo

Il suo vantaggio tecnico principale è che il filtro non dipende più dall'impedenza dell'altoparlante: lavora su un segnale di linea, con carichi definiti, e l'amplificatore è collegato direttamente alla bobina. Linkwitz lo dice in una frase: l'amplificatore prende il massimo controllo sul moto del cono. Ne seguono, secondo Elliott, l'assenza delle perdite di inserzione della rete passiva, la riduzione dell'intermodulazione fra le due vie, perché basse e alte vengono separate prima di essere amplificate, e filtri che si accoppiano con precisione fra i due canali.

La variante con processore digitale porta un secondo vantaggio che pesa molto in questo progetto. La premessa del progetto è un punto di ascolto in una stanza nota e non trattabile acusticamente, e la fase 8 confronta la risposta misurata al punto di ascolto con il progetto. In un sistema con processore lo scarto trovato in misura si corregge cambiando coefficienti, compresa una equalizzazione dei modi della stanza alle basse frequenze, senza ricostruire nulla; in un passivo ogni correzione è un componente da cambiare, e i problemi della stanza alle basse frequenze non si correggono nella rete.

I suoi costi sono tre. Il primo è l'elettronica: due canali di amplificazione per cabinet, il processore o il filtro analogico, l'alimentazione, quindi ogni cabinet diventa un apparecchio alimentato. Il secondo è la complessità di integrazione e di sicurezza elettrica. Il terzo riguarda questo progetto in modo specifico, ed è da verificare caso per caso: molti processori per diffusori si configurano con un programma del costruttore, e la macchina di progetto è Linux, quindi un programma solo per Windows andrebbe fatto girare sotto Wine o su un'altra macchina. Per il processore scelto la compatibilità va accertata prima dell'acquisto, come per l'interfaccia audio di PA-012.

Sulla catena di ascolto, l'attivo completa ADR-012 senza un amplificatore esterno: l'uscita di linea va direttamente ai cabinet. Non è un acquisto in meno, perché gli amplificatori stanno dentro i cabinet, ma è un apparecchio in meno da collocare.

## Una avvertenza sulle fonti

Linkwitz ed Elliott, le due fonti tecniche lette, sono apertamente favorevoli all'attivo: Linkwitz scrive che l'unica scusa per il crossover passivo è il basso costo. Sono fonti autorevoli sul comportamento fisico, e le loro affermazioni tecniche sono coerenti con la teoria dei filtri, ma la loro preferenza non va presa come un giudizio neutro sul rapporto fra benefici e complessità per un progetto fatto in casa. Il confronto che segue tiene distinte le due cose.

## Che cosa decide, per questo progetto

La scelta dipende da tre domande, ciascuna dell'utente.

Se si vuole poter correggere dopo la misura in stanza senza ricostruire nulla. Se sì, l'attivo con processore è la strada naturale, ed è il punto in cui la premessa del progetto, cioè una stanza che non si tratta, pesa di più.

Quanto si vuole costruire e mantenere: un cabinet passivo è finito quando è chiuso; un cabinet attivo porta elettronica alimentata, e il processore porta un programma di configurazione la cui compatibilità con Linux va verificata.

Che cosa si preferisce acquistare alla fine: un amplificatore stereo esterno e i componenti delle reti, oppure moduli di amplificazione con processore, uno per cabinet.

Una inclinazione motivata, dichiarata come tale e non come decisione: in un progetto che parte da una stanza non trattabile e che chiude con una misura al punto di ascolto, la possibilità di correggere in un processore è il vantaggio più legato alla premessa del progetto. Il passivo resta una scelta pienamente legittima, più semplice da costruire, al prezzo di correzioni più costose dopo la misura.

## Che cosa segue alla scelta

Con il passivo: ADR sulla scelta, amplificatore di potenza stereo nella lista degli acquisti finali, e progetto della rete in VituixCAD sull'impedenza misurata dei driver. Con l'attivo: ADR sulla scelta, scelta della forma del filtro, analogica o digitale, verifica della compatibilità Linux del processore, e moduli di amplificazione nella lista degli acquisti. In entrambi i casi il capitolo del report sul crossover passa dalla teoria comune alle equazioni della forma scelta.

## Fonti

Siegfried Linkwitz, "Crossovers", Linkwitz Lab, revisione del 2023-02-15: `https://www.linkwitzlab.com/crossovers.htm`. Letta il 2026-10-01. Autorevole sul criterio di progetto di un crossover, cioè la risposta polare mantenuta attraverso l'incrocio, sugli allineamenti Linkwitz-Riley e sui limiti del passivo; dichiaratamente favorevole all'attivo.

Rod Elliott, "Benefits of Bi-Amping (Not Quite Magic, But Close) - Part 1", Elliott Sound Products, pubblicato nel 1998 e aggiornato il 2017-07-07: `https://sound-au.com/bi-amp.htm`. Letta il 2026-10-01 da questo indirizzo, dopo che l'indirizzo `sound.whsites.net` non risolveva il nome. Autorevole su perdite di inserzione, intermodulazione, dipendenza dall'impedenza d'uscita dell'amplificatore, riscaldamento della bobina e tolleranze; favorevole all'attivo.

VituixCAD help 2.0, versione 2.0.135.2 del 2026-04-25, di Kimmo Saunisto: `https://kimmosaunisto.net/Software/VituixCAD/VituixCAD_help_20.html`. Letta il 2026-10-01. Autorevole su che cosa il programma di progetto supporta: componenti passivi con le loro perdite, filtri attivi, biquad digitali con esportazione dei coefficienti, ritardi e filtri a fase lineare.

Douglas Self, "Small Signal Audio Design", terza edizione, Focal Press, 2020, dal materiale di studio dell'utente, letto nella conversione locale per ADR-028: tratta i filtri attivi usati nei crossover elettronici e rimanda per il dettaglio ai due testi seguenti, che non fanno parte del materiale dell'utente e non sono stati letti.

Douglas Self, "The Design of Active Crossovers", seconda edizione, Focal Press, 2018. Citato da Self 2020, non letto: il riferimento monografico sul crossover attivo, da procurare se si sceglie l'attivo.

Siegfried Linkwitz, "Active Crossover Networks for Non-Coincident Drivers", Journal of the Audio Engineering Society, gennaio-febbraio 1976, data verificata nei riferimenti di Self 2020. Citato da Self 2020, non letto: l'articolo che introduce l'allineamento Linkwitz-Riley.

[^1]: *DSP*, Digital Signal Processor - processore che elabora il segnale in forma numerica; in un diffusore attivo calcola i filtri del crossover, i ritardi e l'equalizzazione.

[^2]: *Biquad* - filtro digitale ricorsivo del secondo ordine, descritto da cinque coefficienti; i filtri di ordine più alto si ottengono mettendone più di uno in cascata.
