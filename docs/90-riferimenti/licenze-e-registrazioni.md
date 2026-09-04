# Licenze e registrazioni

> Stato delle autorizzazioni all'uso del software del progetto, con la cronaca della richiesta ad Akabak, che è l'unica che ha richiesto un contatto con l'autore. Serve a sapere, prima di reinstallare qualcosa, se si perde un diritto d'uso o soltanto una configurazione.

## Akabak 3 e VACS

Il software si scarica dal sito dell'autore, R&D-Team di Joerg Panzer. La versione scaricabile non è una demo limitata nel tempo o nelle funzioni: è la versione completa. Richiede licenza per uso commerciale ed è gratuita per uso privato, hobbistico o di ricerca senza scopo di lucro, previa registrazione di un account e download dal link che appare nel profilo dopo l'accesso.

La richiesta è stata inviata il 13 agosto 2025, chiedendo se fosse possibile usare una licenza per uso non commerciale su una macchina Ubuntu Studio dopo la registrazione, e se ci fosse qualcosa da acquistare. La risposta dell'autore è arrivata registrando l'utente per una student license, con quattro passi: scaricare la versione professionale di Akabak e di VACS dai link forniti, installare ed eseguire entrambi, aprire nel menu di aiuto la voce del release code, e inviare per posta elettronica il Machine Identifier indicato, in cambio del quale l'autore restituisce un release code valido per quel computer.

Ne segue la proprietà pratica che conta per tutta l'amministrazione della macchina: la licenza è machine-based. Il release code vale per quella macchina e non ha nulla a che vedere con il prefix di Wine né con l'installazione di Wine. Cancellare e ricreare i prefix, reinstallare Wine, o reinstallare interamente Ubuntu Studio non invalida la licenza, perché dal punto di vista del programma la macchina è sempre la stessa: basterà reinstallare Akabak e reinserire lo stesso codice.

I due casi che invaliderebbero la licenza sono un cambio significativo di hardware, per esempio una nuova scheda madre, e lo spostamento del programma dentro una macchina virtuale, dove l'identificativo esposto sarebbe quello virtuale e quindi diverso. Il secondo caso è la ragione tecnica per cui, in questo progetto, Wine è preferibile a una macchina virtuale anche a prescindere dalle prestazioni, come discusso nella pagina sulla differenza fra i due.

La copia della corrispondenza con l'autore, che contiene il release code, è materiale sensibile e va conservata fuori dal repository. Sta insieme ai materiali locali del progetto in un file PDF, ignorato da git per estensione, e va inclusa nel trasferimento verso la macchina di destinazione perché serve alla reinstallazione.

## VituixCAD 2

Gratuito per l'uso previsto in questo progetto, senza registrazione né codice di attivazione. Nessuna licenza da conservare.

## EASE Focus 3 e i file GLL

EASE Focus 3 è gratuito per l'utente finale, con licenza inclusa nel programma e nessuna attivazione da richiedere. La versione corrente della linea gratuita è la 3.1.x, scaricabile dal sito di AFMG e dai distributori autorizzati.

I file GLL hanno uno stato che vale chiarire perché è controintuitivo. Ogni GLL è un modello licenziato dal costruttore del diffusore e non richiede attivazione ulteriore: si usa così com'è, e lo stesso file funziona indistintamente in EASE Focus 3 e nelle versioni JR, Standard e Advanced della famiglia. Sono gratuiti ma specifici per modello, quindi il vincolo non è di licenza ma di corrispondenza: per simulare un diffusore serve il GLL di quel diffusore, e per un progetto autocostruito il GLL non esiste finché non lo si crea da misure reali.

Se un GLL è stato prodotto con funzioni non supportate dalle API della versione di EASE Focus in uso, il programma può segnalare un errore o caricarlo in modalità limitata. È uno dei motivi che favoriscono la versione più recente.

## REW, Blender, Octave, MATAA, FreeCAD, ARTA

REW è gratuito. Blender, Octave, MATAA e FreeCAD sono software libero. ARTA nella versione non registrata ha limitazioni funzionali che per l'uso previsto, cioè produrre misure da convertire in GLL, vanno verificate al momento dell'uso e non sono state accertate qui.

## Il resto del pacchetto ereditato

Come registrato nell'inventario, una parte del pacchetto software ereditato è costituita da copie con protezione rimossa, e quel materiale non ha una posizione di licenza da documentare perché non rientra nel workflow, non viene installato e non viene trasferito.
