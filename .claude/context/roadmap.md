---
generated-from-commit: 0df04bb7019814cf69b8458e4eaad8eaf71be818
generated-from-branch: main
generated-date: 2026-09-04
covers-paths:
  - docs/**
last-verified-commit: 0df04bb7019814cf69b8458e4eaad8eaf71be818
---

# Roadmap

> Direzione e priorità del progetto dei due monitor da casa. Tracciata. Non è il work-log: qui sta dove si va, non cosa è già stato fatto, che sta in `docs/OPERATIONS-LOG.md`. Il commit di riferimento è quello precedente alla sessione di conversione, perché i file di questa sessione non sono ancora committati.

## Direzione

Progettare e costruire una coppia di monitor da studio a due vie, ottimizzati per un punto di ascolto domestico noto e non trattabile acusticamente, portando l'intero flusso di progettazione su una macchina Linux dove i programmi Windows indispensabili girano sotto Wine. L'obiettivo di qualità dichiarato è una risposta lineare entro più o meno 2 dB in asse e fino a più o meno dieci gradi fuori asse, da 60 Hz a circa 20 kHz, misurata al punto di ascolto reale e non in campo libero.

Il progetto ha due esiti, e vale distinguerli perché hanno criteri di successo diversi. Il primo è l'oggetto: due diffusori funzionanti. Il secondo è la comprensione: un percorso documentato che spieghi perché ogni scelta è stata fatta, riutilizzabile su un progetto successivo. La documentazione tecnico-didattica sotto `docs/` è il secondo esito, non un accessorio del primo.

## Lo stato di partenza

La parte simulativa è pensata in profondità: il workflow in otto fasi è definito, gli strumenti sono scelti con le loro motivazioni, l'ambiente Linux è documentato e in parte già collaudato, e la licenza di Akabak è ottenuta. La parte fisica non è iniziata: nessuna misura è stata eseguita, nessun driver è stato acquistato, nessun cabinet è stato disegnato.

Il vincolo che oggi blocca più di ogni altro non è tecnico di progetto ma di infrastruttura: la macchina di lavoro è su una versione di Ubuntu fuori supporto e non raggiungibile in rete dalla postazione corrente.

## Priorità

La prima priorità è rimettere in funzione la macchina, perché tutto il resto vi si appoggia. Concretamente: portarla in rete o raggiungerla fisicamente, confermare la diagnosi del blocco di aggiornamento eseguendo la sequenza di verifica in sola lettura di `docs/10-ambiente/ubuntu-lts-upgrade.md`, e poi eseguire l'installazione pulita di Ubuntu Studio 26.04 LTS conservando `/home`. Viene prima di tutto perché una macchina su un rilascio fuori supporto accumula attrito a ogni intervento successivo, e perché la ricostruzione pulita dell'ambiente Wine risolve nello stesso passaggio i guasti registrati in `docs/10-ambiente/wine-troubleshooting.md`.

La seconda priorità è il trasferimento dei materiali, secondo `docs/TRANSFER-MANIFEST.md`, da eseguire prima della reinstallazione e non dopo. La ragione è di sicurezza dei dati: mettere i file sotto `/home` mentre `/home` non è ancora a rischio è una operazione tranquilla, farlo dopo aver riformattato non sarebbe più possibile.

La terza priorità è la ricostruzione dell'ambiente Wine con un prefix per programma, e la reinstallazione di Akabak, VACS, VituixCAD ed EASE Focus 3.1.260. Il criterio di completamento è che ciascuno dei quattro apra la propria finestra e carichi un file di esempio; per Akabak si aggiunge la verifica che il release code esistente sia ancora accettato, che è la prova pratica dell'affermazione sulla licenza legata alla macchina.

La quarta priorità è l'acquisto del microfono di misura, cioè il Dayton Audio EMM-6 o la Sonarworks equivalente, con il suo file di calibrazione individuale. È il primo acquisto del progetto e sblocca la fase 1, che è la fase da cui dipendono sia il modello della stanza sia la scelta dei driver.

La quinta priorità è la misura reale della stanza. È il primo dato vero del progetto e va fatta prima di qualunque altra cosa, perché fino ad allora ogni simulazione è priva di riscontro. Si può eseguire con un diffusore qualsiasi come sorgente, quindi non attende l'acquisto dei driver.

La sesta priorità è la coppia modellazione e validazione, cioè la geometria in Blender e l'analisi modale in Octave, con il confronto contro la misura. Il criterio di uscita è l'accordo verificato fra modi predetti e picchi misurati, non la produzione di un grafico.

La settima priorità è la definizione della risposta target, che precede la scelta dei driver e oggi è ancora una decisione aperta fra una risposta piatta e una curva con lieve enfasi sui bassi.

L'ottava priorità è la progettazione in VituixCAD, poi l'acquisto dei driver, poi la progettazione meccanica in FreeCAD, poi la simulazione finale in Akabak, poi la costruzione, poi la verifica finale. Da qui in avanti l'ordine è quello del workflow e non richiede argomentazione ulteriore.

## Decisioni aperte

La scelta fra installazione pulita e aggiornamento in posto della macchina. La documentazione raccomanda la prima con quattro motivi, ma la decisione è dell'utente e va presa dopo la conferma della diagnosi.

La risposta target del diffusore. Gli appunti registrano che la scelta di un riferimento consumer con lieve enfasi sui bassi è stata fatta da un collega sul proprio sistema; per un monitor da mixing la scelta di una risposta piatta ha argomenti diversi, e le due strade portano a crossover diversi.

Il diametro del tweeter, che dipende dalla frequenza di incrocio, quindi si decide dentro la fase 4a e non prima.

Il canale di approvvigionamento dei driver, che condiziona quali driver sono realmente selezionabili e va verificato prima di ottimizzare il progetto su un modello.

La strategia di correzione residua dopo la verifica finale, cioè intervento sul crossover, equalizzazione digitale, oppure accettazione dello scarto. La premessa del progetto spinge verso il crossover, ma la decisione dipende da quanto grande sia lo scarto e da dove cada in frequenza.

## Idee e ipotesi da verificare

L'esistenza e la data di rilascio di Ubuntu Studio 26.04 LTS come immagine scaricabile, da confermare dal sito del progetto e non dedurre dal calendario dei rilasci.

Il modo in cui la 26.04 fornisce il kernel a bassa latenza, che è il tipo di dettaglio che cambia fra un rilascio e l'altro.

Se ITA-Toolbox convenga come complemento a MATAA per il calcolo del RT60 e la visualizzazione, invece di scrivere quelle funzioni da zero.

Quali programmi del corredo condividano le stesse dipendenze e possano quindi condividere un prefix Wine invece di averne uno per uno. È la domanda che il documento sorgente aveva lasciato aperta e che si risolve solo provando sulla macchina.

Se valga la pena, dopo la costruzione e la misura, produrre un file GLL del monitor autocostruito con EASE SpeakerLab o ARTA. Renderebbe il diffusore simulabile come un prodotto commerciale e chiuderebbe il limite discusso nella pagina della fase 2, ma è lavoro aggiuntivo oltre l'obiettivo dichiarato.

La personalizzazione di un amplificatore per il basso, che nel documento sorgente esisteva come titolo senza contenuto. È fuori dallo scopo dei monitor e resta annotata come possibile progetto separato.
