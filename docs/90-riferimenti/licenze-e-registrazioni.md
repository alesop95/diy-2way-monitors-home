# Licenze e registrazioni

> Stato delle autorizzazioni all'uso del software del progetto, con la cronaca della richiesta ad Akabak, che è l'unica che ha richiesto un contatto con l'autore. Serve a sapere, prima di reinstallare qualcosa, se si perde un diritto d'uso o soltanto una configurazione.

## Akabak 3 e VACS

Il software si scarica dal sito dell'autore, R&D-Team di Joerg Panzer. La versione scaricabile non è una demo limitata nel tempo o nelle funzioni: è la versione completa. Richiede licenza per uso commerciale ed è gratuita per uso privato, hobbistico o di ricerca senza scopo di lucro, previa registrazione di un account e download dal link che appare nel profilo dopo l'accesso.

La richiesta è stata inviata il 13 agosto 2025, chiedendo se fosse possibile usare una licenza per uso non commerciale su una macchina Ubuntu Studio dopo la registrazione, e se ci fosse qualcosa da acquistare. La risposta dell'autore è arrivata registrando l'utente per una student license, con cinque passi: scaricare la versione professionale di Akabak e di VACS dai link forniti, installare ed eseguire entrambi, aprire nel menu di aiuto la voce del release code, inviare per posta elettronica il Machine Identifier indicato, e ricevere in cambio un release code valido per quel computer.

La cronologia completa dello scambio, che prosegue fino alla verifica del codice il 3 settembre 2025 e porta alla luce un limite tecnico dell'integrazione fra i due programmi su Linux, sta in [timeline-akabak-vacs.md](timeline-akabak-vacs.md). Il documento sorgente si interrompeva subito dopo questa prima risposta, con un segnaposto al paragrafo successivo, quindi tutto il seguito è ricostruito dalla corrispondenza e non da esso.

Ne segue la proprietà pratica che conta per tutta l'amministrazione della macchina: la licenza è machine-based. Il release code vale per quella macchina e non ha nulla a che vedere con il prefix di Wine né con l'installazione di Wine. Cancellare e ricreare i prefix, reinstallare Wine, o reinstallare interamente Ubuntu Studio non invalida la licenza, perché dal punto di vista del programma la macchina è sempre la stessa: basterà reinstallare Akabak e reinserire lo stesso codice.

I due casi che invaliderebbero la licenza sono un cambio significativo di hardware, per esempio una nuova scheda madre, e lo spostamento del programma dentro una macchina virtuale, dove l'identificativo esposto sarebbe quello virtuale e quindi diverso. Il secondo caso è la ragione tecnica per cui, in questo progetto, Wine è preferibile a una macchina virtuale anche a prescindere dalle prestazioni, come discusso nella pagina sulla differenza fra i due.

La copia della corrispondenza con l'autore, che contiene il release code, è materiale sensibile e va conservata fuori dal repository. Sta insieme ai materiali locali del progetto in un file PDF, ignorato da git, ed è inclusa nel manifest di trasferimento verso la macchina perché serve alla reinstallazione. Accanto a essa, sotto `_notes/` e anch'essa ignorata, vive una scheda che riporta Machine Identifier e Release Code in forma direttamente utilizzabile insieme alla procedura di inserimento, così che al momento della riattivazione non si debba rileggere un PDF di posta elettronica. Nessuno dei due valori compare in alcun file tracciato di questo repository, e la ragione è che il repository è ospitato su GitHub.

Le versioni a cui la licenza si riferisce, dichiarate dall'autore, sono AKABAK 3.2.4 build 126 e VACS 2.1.3 build 33. Un solo Release Code copre entrambi i programmi: si inserisce una volta da Akabak, e VACS non ne chiede un secondo.

### Lo stato verificato in interfaccia il 2026-09-07

Il controllo in interfaccia grafica previsto dalla fase 0 è stato eseguito davanti alla macchina, aprendo la finestra del release code e quella delle informazioni sul programma. Serviva a una cosa sola, cioè confrontare il Machine Identifier mostrato dal programma con quello conservato nella scheda riservata, prima di azzerare la macchina e perdere il termine di confronto. *Coincidono*, coincide anche il release code inserito, e il programma dichiara la licenza valida con l'indicatore verde e la scritta `Release Code valid`. Nessuno dei due valori viene riportato qui, per la ragione detta sopra: questo repository è pubblico.

Il confronto vale più di una spunta, perché stabilisce che l'identificativo hardware calcolato da Akabak sotto Wine è *stabile nel tempo*: è lo stesso di agosto 2025, dopo un anno di uso, aggiornamenti di sistema e la sedimentazione dell'ambiente Wine documentata nella fotografia della macchina. È la prova sperimentale di ciò che la pagina sui prefix afferma per costruzione, cioè che una licenza machine-based sopravvive alla ricostruzione dell'ambiente, e quindi la conferma che la reinstallazione pulita non mette a rischio la licenza.

La stessa finestra ha portato in dote tre fatti che nessun documento aveva registrato, e vanno detti perché due di essi correggono un'aspettativa.

Il primo è l'edizione, e su di essa esiste ora una conferma post-reinstallazione del 2026-09-10, registrata in MS-089, che è la sola raccolta dopo l'azzeramento della radice e quindi la sola che provi che l'edizione non dipenda da nulla che quell'azzeramento tocchi; nella stessa finestra si leggono `Valid Release Code`, il profilo `NT 10.0 (Build 19043)` e la memoria `1876 / 2047 MBytes`. Il programma si dichiara *Standard Edition*, non professionale, malgrado l'installer conservato si chiami `AKABAK_Pro_v324b126.exe` e malgrado l'autore avesse scritto di scaricare la versione professionale. La contraddizione è solo apparente e si risolve così: l'installer è uno, e l'edizione che si ottiene la determina il release code, non il file scaricato. L'autore aveva registrato l'utente per una *student license*, e Standard Edition è ciò che quella registrazione concede. Quali funzioni distinguano la Standard dalla professionale non è accertato qui e non va supposto: se una simulazione dovesse urtare un limite di edizione, la verifica è il listino delle funzioni sul sito dell'autore, non l'inferenza dal nome dell'installer.

Il secondo è il profilo di Windows dichiarato dal prefix, che il programma riporta come `NT 10.0 (Build 19043)`. È la conferma misurata che il prefix funzionante è impostato su *Windows 10*, quindi la prescrizione di impostare quel profilo, che la pagina di configurazione dava per uniformità e non per necessità dimostrata, risulta essere anche ciò che l'ambiente funzionante fa davvero.

Il terzo è la memoria, riportata come `1897 / 2047 MBytes` su una macchina che ha 16 GB di RAM installata. Non è un difetto ed è la firma inconfondibile di un processo a 32 bit, che dispone di 2 GB di spazio di indirizzamento in modo utente indipendentemente da quanta memoria fisica esista. È una conferma indipendente di ADR-016, e il suo aspetto scomodo è trattato in MS-053: era visibile in uno screenshot esistente prima dell'indagine che ha stabilito quel fatto per altra via.

Una nota finale sul meccanismo di licenza, che la finestra rende visibile. Sotto il release code compare la scritta `Security key not connected to the USB port`, cioè Akabak prevede anche una chiave hardware come portatore alternativo del diritto d'uso. Non è in uso in questo progetto e non serve procurarsela: la scritta non è un errore, è la constatazione che quella via non è quella scelta. Vale saperlo perché in caso di cambio di hardware, l'unico caso che invaliderebbe il release code, la chiave USB sarebbe l'alternativa tecnica da valutare invece di ricontattare l'autore.

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
