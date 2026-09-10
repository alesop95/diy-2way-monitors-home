---
generated-from-commit: 0df04bb7019814cf69b8458e4eaad8eaf71be818
generated-from-branch: main
generated-date: 2026-09-04
covers-paths:
  - docs/**
last-verified-commit: 633c513
---

# Roadmap

> Direzione e priorità del progetto dei due monitor da casa. Tracciata. Non è il work-log: qui sta dove si va, non cosa è già stato fatto, che sta in `docs/OPERATIONS-LOG.md`. Gli impegni con una condizione esterna stanno invece in `docs/PENDING-ACTIONS.md`.

## Direzione

Progettare e costruire una coppia di monitor da studio a due vie, ottimizzati per un punto di ascolto domestico noto e non trattabile acusticamente, portando l'intero flusso di progettazione su una macchina Linux dove i programmi Windows indispensabili girano sotto Wine. L'obiettivo di qualità dichiarato è una risposta lineare entro più o meno 2 dB in asse e fino a più o meno dieci gradi fuori asse, da 60 Hz a circa 20 kHz, misurata al punto di ascolto reale e non in campo libero.

Il progetto ha due esiti, e vale distinguerli perché hanno criteri di successo diversi. Il primo è l'oggetto: due diffusori funzionanti. Il secondo è la comprensione: un percorso documentato che spieghi perché ogni scelta è stata fatta, riutilizzabile su un progetto successivo. La documentazione tecnico-didattica sotto `docs/` è il secondo esito, non un accessorio del primo.

## Lo stato di partenza

La parte simulativa è pensata in profondità: il workflow in otto fasi è definito, gli strumenti sono scelti con le loro motivazioni, l'ambiente Linux è documentato e in parte già collaudato, e la licenza di Akabak è ottenuta. La parte fisica non è iniziata: nessuna misura è stata eseguita, nessun driver è stato acquistato, nessun cabinet è stato disegnato.

Sull'ambiente lo stato è più avanzato di quanto la prima ricognizione lasciasse credere: Akabak e VACS sono installati, licenziati e verificati funzionanti sulla macchina dal 3 settembre 2025, quindi la ricostruzione dell'ambiente non è un primo impianto ma la ripetizione di un percorso già percorso una volta.

Il vincolo che oggi blocca più di ogni altro non è più di infrastruttura, e la differenza rispetto a come questa sezione era scritta fino al 2026-09-09 è il progresso di una settimana. La macchina è stata reinstallata su Ubuntu Studio 26.04.1 LTS conservando `/home`, l'accesso remoto per chiave funziona come `ssh studio` anche in modo non interattivo, la sospensione automatica che la faceva scomparire dalla rete è disattivata, e l'ambiente Wine è ricostruito con Akabak e VACS funzionanti e la licenza verificata valida. Il vincolo che resta è un acquisto: la macchina ha la sola scheda audio integrata, quindi non esiste un ingresso microfonico con alimentazione phantom, e senza di esso non si misura nulla. È PA-012, ed è una decisione condivisa con il progetto gemello di home recording perché l'interfaccia serve a entrambi.

## Priorità

Le prime cinque priorità di questa scheda, come era scritta il 2026-09-04, sono compiute, e restano elencate in forma sintetica perché la loro chiusura è ciò che spiega da dove riparte il resto. L'accesso remoto è aperto con una chiave dedicata. La fotografia della macchina precedente è stata prodotta prima della formattazione, in quattordici file, ed è ciò che ha portato alla scoperta dei 32 bit di ADR-016. I materiali sono stati trasferiti e verificati per impronta, 281 file per 728 MB, con la copia di sicurezza di `/home` fuori dalla macchina. L'installazione pulita della 26.04 LTS è stata eseguita conservando `/home`, ed è verificata. L'ambiente Wine è ricostruito, e nella forma che ADR-016 e ADR-019 prescrivono e non in quella che questa scheda dava per buona: l'architettura `i386` va dichiarata e non evitata, e il comando su un prefix a 32 bit è `wine32` e non `wine`. La cronologia con il razionale di ciascun passo è in `docs/10-ambiente/setup-macchina-2026-09.md`.

La prima priorità aperta è la scelta dell'interfaccia audio, che è PA-012. Viene prima di tutto il resto per una ragione di dipendenza e non di preferenza: da essa dipende la scelta del microfono di misura, e dal microfono dipende la prima misura reale, che è il primo dato vero del progetto. Due parametri non sono ancora stati dichiarati dall'utente e vanno chiesti invece di essere assunti, cioè il numero di ingressi simultanei necessari alla registrazione, che è il vincolo che elimina più modelli di ogni altro, e un eventuale tetto di spesa. I due vincoli già fissati sono dispositivo di classe audio che il kernel veda senza driver proprietari, e capacità di reggere anche le misure e non solo la registrazione.

La seconda priorità è chiudere la fase 8 per la parte che non dipende da acquisti, cioè l'installazione del corredo secondo le sottofasi da 8.3 a 8.9: il limite delle pipeline COM da configurare subito, gli esempi di Akabak, VituixCAD, EASE Focus 3.1.260 con il servizio di database AFMG, e ARTA. Ramsete resta fuori finché PA-002 non è risolta.

La terza priorità è l'acquisto del microfono di misura, cioè il Dayton Audio EMM-6 o la Sonarworks equivalente, con il suo file di calibrazione individuale. Dipende dalla prima e non le si può anteporre.

La quarta priorità è la misura reale della stanza. È il primo dato vero del progetto e va fatta prima di qualunque altra cosa di progettazione, perché fino ad allora ogni simulazione è priva di riscontro. Si può eseguire con un diffusore qualsiasi come sorgente, quindi non attende l'acquisto dei driver.

La quinta priorità è il backup completo della macchina, che è PA-011, e la sua collocazione qui e non più in fondo è una conseguenza di questa settimana: la ricostruzione è costata più di un giorno di lavoro, e il suo scopo è renderla ripetibile in poche ore. Va preso a fase 8 chiusa e verificata, non prima, perché un backup di uno stato intermedio non è uno stato che qualcuno voglia ripristinare.

La sesta priorità è la coppia modellazione e validazione, cioè la geometria in Blender e l'analisi modale in Octave, con il confronto contro la misura. Il criterio di uscita è l'accordo verificato fra modi predetti e picchi misurati, non la produzione di un grafico.

La settima priorità è la definizione della risposta target, che precede la scelta dei driver e oggi è ancora una decisione aperta fra una risposta piatta e una curva con lieve enfasi sui bassi.

L'ottava priorità è la progettazione in VituixCAD, poi l'acquisto dei driver, poi la progettazione meccanica in FreeCAD, poi la simulazione finale in Akabak, poi la costruzione, poi la verifica finale. Da qui in avanti l'ordine è quello del workflow e non richiede argomentazione ulteriore.

## Decisioni aperte

Lo stato di licenza di Ramsete 27b, che decide se il programma entra nel piano e con esso se serve un prefix Wine a 32 bit. Tracciata come PA-002, priorità bassa perché il suo ruolo è coperto da Akabak.

L'architettura del diffusore, cioè attivo o passivo. Non era una decisione aperta finché la sorgente non era definita; ora che lo è, per ADR-012, va anticipata alla fase 4a: con monitor attivi la catena di ascolto è completa così com'è, con monitor passivi serve un amplificatore di potenza interposto, che sarebbe un acquisto. Influisce anche su quali driver convengono.

La risposta target del diffusore. Gli appunti registrano che la scelta di un riferimento consumer con lieve enfasi sui bassi è stata fatta da un collega sul proprio sistema; per un monitor da mixing la scelta di una risposta piatta ha argomenti diversi, e le due strade portano a crossover diversi.

Il diametro del tweeter, che dipende dalla frequenza di incrocio, quindi si decide dentro la fase 4a e non prima.

Il canale di approvvigionamento dei driver, che condiziona quali driver sono realmente selezionabili e va verificato prima di ottimizzare il progetto su un modello.

La strategia di correzione residua dopo la verifica finale, cioè intervento sul crossover, equalizzazione digitale, oppure accettazione dello scarto. La premessa del progetto spinge verso il crossover, ma la decisione dipende da quanto grande sia lo scarto e da dove cada in frequenza.

## Direzioni future, dichiarate non urgenti

Questa sezione raccoglie ciò che l'utente ha indicato come direzione e non come lavoro, e la distinzione va conservata: una voce qui non ha una condizione di sblocco, altrimenti apparterrebbe a `docs/PENDING-ACTIONS.md`, e non ha un criterio di finito, altrimenti apparterrebbe alle priorità. Sta qui perché orienta scelte che si stanno facendo adesso.

*La replica del setup sul secondo portatile.* L'utente ha indicato il 2026-09-10 la replica dello stesso setup di Ubuntu Studio sul proprio secondo portatile, un Asus F550CC-XX698H oggi su Ubuntu 24.04 LTS, dichiarando esplicitamente che non è urgente. La macchina è un portatile consumer del 2013: schermo da 15,6 pollici a 1366 per 768, processore Intel Core i3 di terza generazione, 4 GB di RAM DDR3 espandibili, disco meccanico da 500 GB a 5400 giri, grafica dedicata NVIDIA GeForce GT 720M con 2 GB di VRAM DDR3, raffreddamento a un solo heatpipe con ventola, batteria agli ioni di litio da circa 37 Wh, peso attorno ai 2,3 kg. Le porte sono USB 2.0 e 3.0, HDMI, VGA, lettore di schede SD e jack audio combinato. La rete wireless è una Intel Centrino Wireless-N 2230, che copre 802.11b/g/n sulla sola banda a 2,4 GHz fino a 300 Mbps con WEP, WPA e WPA2 e non ha supporto nativo per i 5 GHz; la rete cablata è un controller Realtek PCIe GBE fino a 1 Gbps con Wake-on-LAN. Il numero di serie e il codice di configurazione sono stati forniti in forma oscurata e restano tali, perché non servono a nessuna decisione tecnica e un identificativo di dispositivo non ha motivo di stare in un repository.

Su questa direzione vanno enunciati i due punti che decidono se valga la pena, e vanno enunciati adesso perché sono il genere di cosa che si scopre dopo aver formattato. Il primo è che quel portatile non può essere una seconda postazione di lavoro equivalente: 4 GB di RAM sono il vincolo dominante, e un processo a 32 bit sotto Wine ne vede al massimo 2047 MByte, numero non desunto dalla teoria ma letto il 2026-09-10 nella finestra di informazioni di AKABAK, che dichiarava `1876 / 2047 MBytes`, e che sul solo Akabak può bastare ma lascia poco margine al resto del sistema; il disco meccanico a 5400 giri è il secondo vincolo, e su un carico di simulazione che scrive risultati intermedi si sente. Il secondo è che la parte del setup che si replica non è la stessa per tutto: la catena Wine con il prefix a 32 bit, gli installer e la procedura sono replicabili integralmente, mentre la licenza di Akabak non lo è, perché il Release Code è legato al Machine Identifier di una macchina sola, come ADR-003 stabilisce e come MS-085 ha ora verificato sperimentalmente. Una seconda macchina richiederebbe quindi una seconda licenza, o l'accettazione di usare là soltanto il software che non ne ha bisogno. La domanda vera da porsi prima di iniziare è dunque a che cosa serva quella macchina: se serve a leggere la documentazione e a lavorare in Octave, FreeCAD e Blender, la replica ha senso e non tocca la licenza; se serve a simulare in Akabak, non è una replica ma una seconda installazione con un proprio costo.

*L'altro dei due progetti che condividono la macchina.* Il Nektar Impact GX49 dichiarato dall'utente il 2026-09-10 è hardware presente e pertinente al progetto gemello di home recording, non a questo: una tastiera di controllo non produce suono da sé e non misura nulla, quindi non entra in alcuna delle otto fasi del flusso di progettazione dei monitor. È inventariato in `docs/10-ambiente/setup-macchina-2026-09.md`, che è il blocco condiviso fra i due progetti, e il suo collaudo va rifatto sul sistema reinstallato perché quello ricordato dall'utente appartiene al sistema precedente.

## Idee e ipotesi da verificare

*Risolta il 2026-09-08.* L'esistenza e la data di rilascio di Ubuntu Studio 26.04 LTS come immagine scaricabile era una ipotesi da confermare: l'immagine esiste, e il punto da prendere è il point release `ubuntustudio-26.04.1-desktop-amd64.iso` e non la 26.04 iniziale. Il sistema installato si dichiara `Ubuntu 26.04.1 LTS` con supporto `Resolute Raccoon` build 20260826.

*Risolta il 2026-09-09.* Il modo in cui la 26.04 fornisce la bassa latenza non è un kernel separato: il kernel installato è `7.0.0-31-generic`, generico e non `lowlatency`, e la bassa latenza viene dai parametri di avvio `preempt=full threadirqs rcu_nocbs=all` che Ubuntu Studio scrive in `/etc/default/grub.d/ubuntustudio.cfg`, più i limiti realtime `rtprio 95` e `memlock unlimited`. Questi ultimi erano scritti e non in vigore, perché l'utente non apparteneva ai gruppi `audio` e `pipewire`, e la correzione è in MS-077: la lezione è che i limiti si verificano con `ulimit` in una sessione di login e non leggendo il file che li dichiara.

Se ITA-Toolbox convenga come complemento a MATAA per il calcolo del RT60 e la visualizzazione, invece di scrivere quelle funzioni da zero.

Quali programmi del corredo condividano le stesse dipendenze e possano quindi condividere un prefix Wine invece di averne uno per uno. La domanda del documento sorgente ha ora una risposta parziale nella mappa dei prefix di `docs/10-ambiente/wine-corredo-progetto-stanza.md`, dove Akabak e VACS condividono un prefix e gli altri no; il resto si risolve solo provando sulla macchina.

Le limitazioni della modalità dimostrativa di ARTA senza registrazione, e se siano compatibili con la produzione di un file GLL.

Il comportamento del servizio di database AFMG sotto Wine, che è un servizio Windows e sotto Wine non gira come servizio di sistema ma come processo dentro il prefix.

Se valga la pena, dopo la costruzione e la misura, produrre un file GLL del monitor autocostruito con EASE SpeakerLab o ARTA. Renderebbe il diffusore simulabile come un prodotto commerciale e chiuderebbe il limite discusso nella pagina della fase 2, ma è lavoro aggiuntivo oltre l'obiettivo dichiarato.

La personalizzazione di un amplificatore per il basso, che nel documento sorgente esisteva come titolo senza contenuto. È fuori dallo scopo dei monitor e resta annotata come possibile progetto separato.
