# Azioni differite

> Registro delle azioni che non si possono compiere adesso perché dipendono da una condizione esterna, con la condizione di sblocco di ciascuna e il criterio con cui si stabilisce che sono compiute. Serve a un fine preciso: un promemoria che vive solo in una conversazione è perduto, mentre una voce qui sopravvive alla sessione, al riavvio e a un clone del repository.
>
> Lo strumento `tools/check-pending-actions.py` legge le condizioni verificabili in automatico e dice quali azioni sono diventate eseguibili. Conviene lanciarlo a inizio sessione.

## Come si legge una voce

Ogni azione ha un identificativo nella forma `PA-NNN`, una data di apertura, la descrizione di che cosa va fatto, la condizione che ne blocca l'esecuzione, il criterio di completamento e lo stato. Una voce non si cancella quando è compiuta: si marca come compiuta con la data, così che il registro resti la storia di ciò che è stato deciso e non solo di ciò che resta da fare.

## Sequenza operativa: che cosa deve fare l'utente, e in che ordine

Questa sezione esiste perché il registro per voce risponde alla domanda sbagliata. Dice per ciascuna azione se è eseguibile, ma non dice in che ordine affrontarle né quali appartengono alla procedura di installazione invece che a questo registro, e chi si siede al lavoro ha bisogno esattamente di quell'ordine. Si aggiorna quando cambia, e ogni voce rimanda al posto dove sta il dettaglio.

Le azioni sono numerate e nell'ordine in cui vanno eseguite. Dove una dipende dalla precedente lo dice; dove è indipendente lo dice, così che si possa saltare senza rompere nulla.

*1. Commit e push dei due repository.* Prima di tutto il resto, perché il lavoro documentale in attesa di commit è l'unica cosa che una sessione perduta porterebbe via. Indipendente da tutto ciò che segue.

*2. Cancellare la copia del corredo sul Desktop. Compiuto il 2026-09-08.* È PA-007, chiusa. Riverifica delle impronte e cancellazione eseguite nell'ordine e a distanza di minuti, 2,3 GB recuperati, nessun dato utile perduto.

*3. Leggere lo SMART dell'SSD esterno. Compiuto il 2026-09-08.* È PA-009, chiusa. Il supporto è sano, quindi delle due cause resta la rimozione senza espulsione: il disco non va sostituito e la regola è espellere il volume prima di staccarlo.

*4. Preparare la chiavetta di installazione. Compiuto il 2026-09-08.* È la fase 2 della procedura, chiusa. L'immagine è in `C:\Users\Utente\Desktop\_iso-ubuntu-studio\`, verificata due volte, per somma di controllo e per firma del file delle somme: è la *26.04.1*, cioè il point release, e non la 26.04 iniziale che la procedura nominava. La chiavetta Kingston da 57,7 GB è stata scritta con Rufus 4.15 portabile, verificato per firma Authenticode, in modalità DD e in otto minuti, e porta la tabella GPT dell'immagine con le sue tre partizioni. La verifica del supporto si fa al primo avvio, dal menu della chiavetta alla voce di controllo dei difetti, e *non* con un confronto di impronte contro l'immagine: su Windows quel confronto produce un falso allarme, per le ragioni registrate in MS-069.

*5. Controllare il firmware.* È la fase 3. Quattro voci nel setup UEFI, e una va cambiata adesso perché dopo costa una sessione: il Wake-on-LAN, senza il quale la macchina che si sospende va risvegliata a mano.

*6. Installare, conservando `/home`.* Sono le fasi 4 e 5, ed è il passo irreversibile. Il presidio contro l'unico rischio reale, l'errore umano nella selezione delle partizioni, è già in posizione: la copia di sicurezza di `/home` esiste su una macchina diversa ed è verificata.

*7. Ricostruire l'ambiente.* Sono le fasi da 6 a 9, cioè catena audio, Wine, programmi e licenza, strumenti nativi. Un avviso che vale più della sequenza: le fasi 7 e 8 sono state corrette il 2026-09-07 per ADR-016, e chi eseguisse una versione precedente otterrebbe un ambiente in cui Akabak non parte, perché l'architettura `i386` va dichiarata e non evitata.

*8. Igiene e chiusura.* Sono le fasi 10 e 11, cioè politica di aggiornamento, sospensione e accesso remoto, chiave SSH, indirizzo stabile, e la fotografia finale da confrontare con quella iniziale.

Restano fuori da questa sequenza le voci a bassa priorità che non dipendono da essa e non la bloccano: PA-002 sulla licenza di Ramsete, PA-003 sulla propagazione al template, PA-004 sul disco `G:`. Si affrontano quando capita l'occasione, non in un ordine.

## PA-010 - Verificare che i file personali siano tutti sulla macchina, prima di cancellarli altrove

Data di apertura: 2026-09-09. Stato: aperta.

Che cosa va fatto. Prima di cancellare qualunque copia di materiale personale che oggi vive fuori dalla macchina Ubuntu Studio, cioè sulla postazione Windows, sull'SSD esterno `J:` o sul disco `G:` non ancora ispezionato, va accertato che il corrispondente sia presente e integro dentro `/home/alesop95`. La verifica riguarda i file di lavoro personali e non il solo corredo software, quindi comprende i progetti Ardour, il materiale di acustica della stanza, i simulatori, i documenti sciolti sulla scrivania e tutto ciò che l'utente riconosce come proprio.

Perché conta, ed è una richiesta esplicita dell'utente. Il 2026-09-09 la reinstallazione ha conservato `/home` e la scrivania si è ripresentata con i suoi contenuti, il che rende naturale concludere che non manchi nulla. Quella conclusione non è verificata: si è osservato che le icone della scrivania ci sono e che `~/electroacoustics` conta 281 file per 728 MB come documentato, che sono due controlli su un perimetro molto più ampio. Cancellare una copia esterna sulla base di una impressione visiva è esattamente il genere di passo che non si può annullare.

Condizione di sblocco. Nessuna condizione esterna impedisce la verifica in sé, che si può fare adesso via SSH. La cancellazione delle copie esterne, invece, dipende da questa verifica e non va anticipata. La voce resta aperta finché l'inventario non è fatto e confrontato.

Criterio di completamento. Esiste un confronto documentato fra il contenuto personale delle copie esterne e quello di `/home/alesop95`, fatto per impronta del contenuto e non per dimensione occupata, dato che il tranello del `du -sh` è già costato una inferenza sbagliata in MS-024. Da quel confronto risulta un elenco esplicito di ciò che esiste solo fuori dalla macchina, e ogni voce di quell'elenco è stata trasferita oppure dichiarata volutamente non trasferita.

Nota sul software. La richiesta dell'utente comprende anche l'utilizzo del software, cioè non soltanto i file di dato ma la loro apribilità: un progetto Ardour o un modello Akabak conservato senza il programma che lo apre è un archivio e non un materiale di lavoro. La verifica va quindi estesa a quali formati restano leggibili sulla macchina dopo la ricostruzione dell'ambiente delle fasi da 6 a 9.

## PA-011 - Backup Veeam della macchina, a ricostruzione finita

Data di apertura: 2026-09-09. Stato: compiuta il 2026-09-17, sette giorni dopo l'apertura. Il racconto sta nei microstep da MS-117 a MS-135, e la procedura replicabile che ne è stata estratta in `docs/10-ambiente/veeam-agent-linux.md`.

Che cosa va fatto. Un backup completo della macchina Ubuntu Studio con Veeam, da eseguire quando la ricostruzione dell'ambiente è finita e verificata, non prima.

Perché conta, e perché è diverso dal backup che già esiste. L'archivio da 4,4 GB prodotto il 2026-09-07 e conservato sulla postazione Windows è una copia di `/home` fatta con `tar`, cioè dei soli dati dell'utente, ed è servito come presidio contro l'errore umano nel partizionamento. Non contiene il sistema, i pacchetti installati, la configurazione della catena audio a bassa latenza, i prefix Wine ricostruiti né le licenze attivate. Un backup di macchina intera ha uno scopo diverso: rendere ripetibile in poche ore il risultato di una ricostruzione che, come questa sessione dimostra, costa più di un giorno.

Condizione di sblocco. Che le fasi da 6 a 9 siano compiute e verificate, cioè catena audio, Wine con l'architettura `i386` dichiarata, programmi reinstallati, licenza Akabak riattivata e corredo installato. Un backup preso prima congelerebbe uno stato intermedio che nessuno vuole ripristinare.

Criterio di completamento. Il backup esiste, il suo supporto di destinazione è dichiarato, e ne è stato provato il ripristino almeno in forma parziale, perché un backup mai riletto è una speranza e non una copia. Va dichiarato anche dove risiede, dato che la regola imparata da PA-009 vale anche qui: un disco rimovibile non è il posto dove tenere l'unica copia di qualcosa.

Esito del 2026-09-17, criterio per criterio. Il backup esiste: è `backup-file-sistema_2026-09-17T154511.vbk` da 17 627 570 176 byte, prodotto in sette minuti da un lavoro a livello di file con Veeam Agent for Linux nella variante senza modulo del kernel, accompagnato dal descrittore `backup-file-sistema.vbm` da 10 831 byte. Il supporto di destinazione è dichiarato: `J:\backup-macchine\alessio-ubuntustudio\`, e la copia è stata verificata confrontando le impronte `sha256` alle due estremità. Il ripristino è stato provato e non rimandato: il punto è stato montato, sei file confrontati per impronta fra sistema vivo e archivio e quattro conteggi di file nei prefix di Wine trovati coincidenti, ed è stato verificato per assenza che il deposito non si sia copiato dentro sé stesso. Dove risiede è dichiarato qui e verificato a ogni corsa da `tools/check-pending-actions.py`, che controlla l'esistenza del file al percorso di destinazione, perché il disco è rimovibile e una chiusura che non si rimisura è una dichiarazione e non un fatto.

Tre cose che la chiusura non risolve, dichiarate perché una voce chiusa non sembri risolvere più di quanto risolva. La destinazione resta provvisoria e il NAS domestico la sostituirà, e con essa va ripresa la decisione sulla cifratura, qui rinviata con motivazione in MS-131: l'archivio contiene l'intero sistema, quindi anche le impronte delle password, e su un filesystem che non conserva i permessi POSIX la protezione che sulla macchina viene dalla cartella del deposito non esiste. L'archivio non è una immagine avviabile e non può esserlo su questa macchina, per quanto accertato in MS-120, MS-121 e MS-122, quindi il ripristino passa da una installazione nuova seguita dal riversamento, e l'immagine avviabile resta quella da prendere con Clonezilla a macchina spenta. E una copia sola su un disco solo non è una strategia di backup ma il primo esemplare di una, che lo diventa quando il NAS esiste: vale anche qui la regola imparata da PA-009.

Sull'esperienza precedente dell'utente va registrato un accertamento fatto il 2026-09-09, perché ridimensiona quanto sia riutilizzabile. Il progetto `home-lab-cybersec-networking` contiene una strategia di backup con Veeam sotto `docs/03-spunti-di-sviluppo/05-strategia-di-backup/`, ma la sua unica pagina è `01-veeam-agent-for-windows.md` e il README della cartella elenca soltanto quella: una ricerca di `linux` e `ubuntu` in quel blocco non restituisce nulla. Trasferibili sono quindi i concetti, cioè la scelta della destinazione, il criterio di ritenzione e la prova di ripristino, mentre l'agente per Linux è un prodotto diverso, con un proprio modulo del kernel per gli snapshot e un proprio servizio, e va documentato da zero. Su Ubuntu Studio non cambia nulla rispetto a Ubuntu, e questa è una delle poche affermazioni che si possono fare senza verificarle su questa macchina, perché l'abbiamo misurata: kernel generico, stessi archivi, stesso `apt`, con la sola differenza della selezione di pacchetti.

Da definire, e non va inventato adesso. Se l'agente gratuito per Linux basti allo scopo, quale sia la destinazione e con quale frequenza. Sono decisioni che si prendono quando la voce si sblocca, e la loro assenza qui è voluta.

Aggiunta del 2026-09-15, che chiude la destinazione in forma dichiaratamente provvisoria. L'utente ha scelto l'SSD esterno T7, cioè il volume `J:` della postazione, scrivendo alla sua radice, e ha dichiarato il motivo per cui la scelta è temporanea: il consolidamento di un NAS per la macchina privata è un progetto in corso tracciato altrove, sotto `E:\home-lab-cybersec-networking\nas-consolidation`, e i backup organizzati partiranno quando quel NAS esisterà. Fino ad allora queste sono copie di cautela, il cui scopo dichiarato è ripartire da una macchina con tutto installato se qualcosa va storto, non una politica di ritenzione.

La scelta va letta insieme a due fatti già registrati qui, e non li contraddice: PA-009 dice che un disco rimovibile non è il posto dove tenere l'unica copia, e resta vero, ma una copia di cautela su disco rimovibile è comunque incomparabilmente meglio di nessuna copia, e la sua provvisorietà è dichiarata invece che dimenticata. Lo spazio disponibile su quel volume era di 78,2 GB al 2026-09-15, contro circa 31 GB occupati sulla macchina fra radice e `/home`, quindi basta per una copia e non per molte, il che è coerente con lo scopo dichiarato.

Le alternative scartate e il perché, così che la decisione non vada rifatta da zero. Le due condivisioni di rete `\\NAS-INTRA\Backup` e `\\NAS-INTRA3\Public`, con 2952 e 1529 GB liberi, sono NAS aziendali e il progetto è personale. Un disco interno della postazione, tipicamente `E:`, è stato scartato per una ragione tecnica precisa e non per preferenza, ed è il motivo per cui esiste PA-013.

L'utente ha inoltre fissato l'ordine: il backup si prende dopo avere finito di installare il corredo, ARTA compreso, e non prima. È la stessa condizione di sblocco già scritta qui sopra, ribadita esplicitamente il 2026-09-15.

Aggiunta del 2026-09-16 sulla forma dell'accesso, decisa dall'utente. Il T7 resta collegato alla postazione Windows e non viene spostato sulla macchina, quindi Veeam scrive su un percorso locale della macchina e il risultato viene poi trasferito su `J:` attraverso la rete. La scelta ha due conseguenze che vanno scritte perché non sono evidenti e perché nessuna delle due la rende sbagliata, ma entrambe vanno conosciute prima del ripristino.

La prima è che la copia transita sul disco interno della macchina, cioè proprio il disco che il backup esiste per proteggere: finché il trasferimento non è compiuto, quel backup non protegge da un guasto del disco, e l'unico stato che conta come raggiunto è quello in cui i file sono su `J:`. La seconda è che al momento del ripristino il T7 andrà comunque collegato alla macchina, oppure il backup andrà riportato su di essa attraverso la rete, perché il supporto di avvio di Veeam deve poter leggere l'archivio: lo spostamento fisico non è evitato, è rimandato al momento peggiore per farlo. Se questo diventasse scomodo, l'alternativa resta collegare il T7 direttamente alla macchina, che era la via più breve.

Accertamento del 2026-09-16 che cambia la natura della copia, e va letto prima di ogni altra cosa. Su questa macchina il backup a livello di volume con Veeam non è disponibile: la variante senza modulo del kernel non lo sa fare su partizioni semplici, e i due moduli esistenti, `veeamsnap` e `blksnap`, non compilano contro il kernel `7.0.0-31-generic` perché appartengono a una generazione precedente. Il racconto è in MS-120, MS-121 e MS-122, e la pagina prescrittiva che ne è stata estratta è `docs/10-ambiente/veeam-agent-linux.md`.

Ne discende che questa voce si soddisfa con un backup a livello di file dell'intero sistema, che conserva i file con permessi e proprietà ma non produce una immagine avviabile. La differenza va dichiarata perché cambia il criterio di completamento: il ripristino non è l'avvio di un supporto che riscrive i volumi, ma una installazione nuova del sistema seguita dal riversamento dei file. Per questo progetto la perdita si misura in un'ora di reinstallazione e non in contenuto, perché ciò che costa ricostruire, cioè i quattro prefix Wine, le licenze attivate e la configurazione della catena audio, vive interamente in file.

Resta aperta e consigliata una seconda via per l'immagine avviabile vera, che non passa da Veeam e non dipende dal kernel installato: Clonezilla avviato da chiavetta a macchina spenta, che copia le partizioni così come sono. Richiede la presenza fisica davanti alla macchina e il disco di destinazione collegato a lei, quindi non sostituisce la copia da remoto ma la completa, ed è il modo ragionevole di avere entrambe.

Un fatto misurato il 2026-09-16 sul supporto: il T7 è formattato exFAT, 500 GB complessivi e 78 GB liberi. Non è un impedimento, perché Veeam vi deposita file e l'exFAT non pone limiti di dimensione che contino a questa scala, ma è il motivo per cui l'archivio non porta con sé permessi e proprietà dei file: quelli vivono dentro l'archivio di Veeam e non nel filesystem che lo ospita, il che è esattamente il comportamento voluto.

Aggiunta del 2026-09-10, che apre una discrepanza invece di chiuderla. L'utente ha riconfermato l'intenzione e ha aggiunto di avere già sperimentato Veeam da Ubuntu proprio nel progetto `home-lab-cybersec-networking`. L'affermazione non coincide con l'accertamento riportato nel paragrafo precedente, che in quel repository ha trovato una sola pagina di strategia di backup, dedicata all'agente per Windows, e nessuna occorrenza di `linux` o `ubuntu` nel blocco. Le due si conciliano in due modi con conseguenze diverse, quindi la discrepanza si dichiara. Se l'esperimento su Linux è stato eseguito e non documentato, esiste esperienza riutilizzabile da recuperare, e la sua assenza da quel repository è un difetto di tracciamento di quel progetto e non di questo. Se invece riguardava l'agente per Windows, come la sola pagina esistente suggerisce, l'agente per Linux resta da documentare da zero e la conclusione qui sopra non cambia. La verifica costa una domanda e va fatta quando la voce si sblocca; fino ad allora nessuna delle due versioni va scritta come fatto.

Chiusura del 2026-09-16, per lettura e non per domanda. La discrepanza si risolve nel primo dei due rami: l'esperienza su Linux esiste ed è documentata, ma non nella cartella della strategia di backup, dove era stata cercata. Sta nel censimento hardware del sottoprogetto di consolidamento, dove una delle due macchine Linux porta installati `veeam-libs` e `veeam-nosnap` alla versione `6.3.2.1307` insieme al pacchetto del repository ufficiale, e sta nel documento di passaggio dello stesso sottoprogetto, che dichiara il backup delle due macchine Linux eseguito e collaudato con un ripristino reale, con le macchine riavviate e verificate dall'interno. Il dettaglio riutilizzabile che conta è la variante `nosnap`, cioè quella che non compila alcun modulo del kernel, ed è la scelta giusta anche qui perché Ubuntu Studio porta un kernel proprio. Il racconto, con il compromesso che quella variante comporta, è in MS-117.

## PA-012 - Scegliere l'interfaccia audio, che serve a due progetti e non a uno

Data di apertura: 2026-09-09. Stato: aperta.

Che cosa va fatto. Scegliere e acquisire una interfaccia audio per la macchina Ubuntu Studio. La valutazione appartiene al progetto gemello `home-recording-training-mixing-setup`, perché l'esigenza primaria è la registrazione multitraccia con Ardour, ma la scelta vincola anche questo progetto, quindi la voce esiste in entrambi.

Perché conta qui. La fase 8 di questo progetto misura i diffusori costruiti, e una misura acustica richiede un ingresso microfonico con alimentazione phantom per un microfono XLR calibrato, che la scheda integrata `ALC887-VD` non ha. Senza interfaccia la fase 8 non è eseguibile in quella forma, e la scelta del microfono resta bloccata a monte: `docs/20-misura-stanza.md` conclude a favore di un XLR calibrato individualmente soltanto sotto la condizione che l'interfaccia esista, e dichiara che in sua assenza l'UMIK-1 USB sarebbe la scelta giusta senza discussione. Le due decisioni sono quindi in sequenza e non in parallelo.

I due vincoli fissati dall'utente il 2026-09-09, e vanno trattati come requisiti e non come preferenze. Il primo è che l'interfaccia funzioni come dispositivo di classe audio, cioè che il kernel Linux la riconosca senza driver proprietari: elimina la classe di problemi peggiore su questa piattaforma, dove un produttore che rilascia driver solo per Windows e macOS rende l'hardware inutilizzabile a ogni aggiornamento di kernel. Il secondo è che la stessa interfaccia regga anche le misure di questo progetto, non solo la registrazione, quindi serve almeno un ingresso microfonico con phantom a 48 V e una qualità di conversione dichiarata dal produttore.

Due vincoli che l'utente ha esplicitamente non fissato, e la loro assenza va registrata perché altrimenti verrebbe riempita per ipotesi: il numero di ingressi simultanei necessari, che è il parametro che elimina più modelli di ogni altro, e un tetto di spesa. Nessuno dei due va assunto: vanno chiesti quando la valutazione si apre.

Un fatto storico da non ripetere. Le versioni precedenti della documentazione dichiaravano come dato di fatto che la macchina possedesse una Focusrite Scarlett 2i2 di seconda generazione, e l'affermazione derivava da un file alla radice contenente il solo indirizzo della pagina di download dei driver. L'utente possiede quella interfaccia ma non la impiega in questo progetto. Il ritiro è in MS-079, e la lezione operativa per questa voce è che l'inventario dell'hardware si scrive da ciò che si osserva sul bus, non da un segnalibro.

Condizione di sblocco. Nessuna condizione esterna impedisce la valutazione, che si può fare adesso; l'acquisto dipende dai due parametri mancanti, che sono dell'utente. La voce resta aperta finché l'interfaccia non è scelta.

Criterio di completamento. Esiste un documento nel progetto gemello che confronta un numero limitato di candidati sui due vincoli dichiarati, con la verifica esplicita del supporto di classe audio su Linux fatta su fonte primaria e non su un forum, e la scelta è registrata come decisione architetturale in entrambi i progetti. Dopo l'acquisto, il controllo di uscita della fase 6 di `docs/10-ambiente/installazione-pulita-26-04.md` va riscritto nominando il dispositivo reale, e la scelta del microfono in `docs/20-misura-stanza.md` va promossa da condizionale a decisa.

## PA-001 - Cancellare la copia del corredo software su SSD esterno

Data di apertura: 2026-09-04. *Compiuta il 2026-09-07.* Stato: chiusa.

L'esito, con la distinzione fra ciò che è accertato e ciò che non lo è. La cartella `J:\Progetto stanza (software)` *non esiste più sul disco*, verificato con il disco collegato. Le due copie restanti sono intatte: quella sul Desktop della postazione conta 650 file per 2,3 GB, e quella sulla macchina Ubuntu Studio conta 281 file per 728 MB con le impronte verificate. Nessun dato è andato perduto.

Non è invece accertato il momento né il modo della cancellazione, e va detto invece di ricostruirlo. Il comando lanciato dall'utente ha risposto che il percorso non esisteva, e nello stesso momento lo strumento riportava il disco come non collegato: le due cose sono compatibili sia con una cartella già rimossa in precedenza sia con un disco assente al momento del comando. Alle 14 dello stesso giorno la cartella era presente, perché il confronto delle impronte ne ha letto tutti e 650 i file. Fra quel momento e la verifica successiva è scomparsa. Poiché l'obiettivo della voce era che quella copia non ci fosse più e le altre due sì, la voce è compiuta a prescindere da quale delle due spiegazioni sia quella giusta.

Che cosa va fatto. Cancellare la cartella `J:\Progetto stanza (software)` dall'SSD esterno, una volta che il corredo utile è stato trasferito sulla macchina Ubuntu Studio e la sua integrità è stata verificata. È l'utente a chiedere questo promemoria, e la ragione è che quella copia è ridondante rispetto a quella sul Desktop della postazione Windows.

Le tre condizioni di sblocco, e il loro stato al 2026-09-07.

La prima, il disco collegato e visibile, è *soddisfatta*. Il 2026-09-04 `J:` non risultava fra le unità montate; il 2026-09-07 è stato collegato ed è visibile.

La seconda, la corrispondenza fra le due copie verificata per impronte, è *soddisfatta*. Il confronto ha dato 650 file su ciascuna copia, gli stessi nomi, le stesse dimensioni, 2.380.021.546 byte in totale su entrambe, e le impronte SHA-256 di tutti e 650 i file coincidenti, senza alcun file presente su una sola delle due. La dichiarazione dell'utente che si trattasse di una copia uno a uno è quindi confermata come fatto.

La terza, il trasferimento del corredo verso la macchina Ubuntu Studio completato con le impronte verificate secondo `docs/TRANSFER-MANIFEST.md`, è *soddisfatta il 2026-09-07*. Il trasferimento è stato eseguito e verificato: 8 file del manifest e 6 voci del corredo per 273 file, tutte le impronte coincidenti, per 728 MB sotto `~/electroacoustics` con un collegamento sulla scrivania della macchina. Il dettaglio, compresi i due difetti dello strumento trovati durante l'operazione, è in MS-038.

*Le tre condizioni sono quindi tutte soddisfatte e la cancellazione è autorizzata.* Resta un'azione dell'utente e non dell'agente, perché cancellare 2,3 GB da un disco esterno è una operazione distruttiva su materiale personale: il comando è in fondo a questa voce.

Il tranello nel metodo di verifica, che vale registrare perché avrebbe portato a una conclusione sbagliata. Il comando `du -sh` riportava dimensioni sensibilmente diverse fra le due copie, per esempio 14 MB contro 5,9 MB su LSPCad 5.25 e 36 MB contro 15 MB su LSPCad 6.32, e a prima vista sembrava una divergenza di contenuto. Non lo era: `du` misura lo spazio occupato, che dipende dalla dimensione dei cluster del filesystem e arrotonda per eccesso ogni file, e i due dischi hanno cluster di dimensione diversa. Il conteggio dei byte reali e le impronte hanno mostrato copie identiche. È la dimostrazione pratica del perché il criterio di confronto deve essere l'impronta del contenuto e non lo spazio occupato.

Una inferenza sbagliata da ritirare, registrata qui perché una versione precedente di questa voce la dava per probabile. Si era osservato che nella copia sul Desktop la versione 3.1.10 di EASE Focus era un collegamento e non una cartella, e concluso che quel contenuto esistesse presumibilmente sul solo SSD, quindi che la cancellazione dovesse essere limitata a ciò che era effettivamente duplicato. È falso: il collegamento è presente e identico su entrambe le copie. La lettura del collegamento ha però rivelato dove punta davvero, e questo ha aperto PA-004.

Il criterio di completamento. La cartella non esiste più su `J:`, e sulla macchina Ubuntu Studio il corredo utile è presente con le impronte verificate.

Nota sul perimetro. Questa azione riguarda la copia su SSD, non quella sul Desktop della postazione Windows. Quest'ultima è la copia di lavoro da cui parte il trasferimento, e la sua eventuale rimozione è una decisione separata, da prendere dopo che il materiale è sulla macchina e non insieme a questa.

Il comando di cancellazione, da eseguire dall'utente sulla postazione Windows. Prima di lanciarlo conviene rilanciare il controllo, che conferma le tre condizioni.

```powershell
python tools/check-pending-actions.py
Remove-Item -LiteralPath "J:\Progetto stanza (software)" -Recurse -Force
```

```bash
python tools/check-pending-actions.py
rm -rf "/j/Progetto stanza (software)"
```

Nota sul perimetro di installazione, aggiunta il 2026-09-07 a fronte di una domanda dell'utente. Il percorso indicato per la messa in opera sotto Wine era la sola copia sul Desktop; `J:` era stato nominato soltanto come la copia da cancellare. L'utente ha poi chiesto che anche il contenuto di `J:` fosse fatto funzionare sulla macchina. La verifica per impronte rende la richiesta priva di conseguenze pratiche: essendo le due copie identiche file per file, il piano di installazione già scritto le copre entrambe, e non c'è alcun programma su `J:` che non sia già nel piano. Il perimetro di installazione resta quindi quello di ADR-010, e nessuna voce va aggiunta.

## PA-002 - Verificare lo stato di licenza di Ramsete 27b

Data di apertura: 2026-09-04. Stato: *aperta*.

Che cosa va fatto. Accertare dal sito del produttore se la copia di Ramsete 27b presente nel corredo sia una versione dimostrativa liberamente distribuibile oppure una copia completa che richiede licenza.

Perché conta. È la condizione che decide se Ramsete entra nel piano di installazione, e con essa se serve un prefix Wine a 32 bit e la dichiarazione dell'architettura `i386` sul sistema. Il quadro è in `docs/10-ambiente/wine-corredo-progetto-stanza.md` e l'emendamento condizionato alla decisione sui prefix è ADR-009.

Il criterio di completamento. Una risposta documentata con la fonte, e la conseguente installazione oppure l'esclusione dichiarata.

Nota di priorità. Bassa. Il ruolo di Ramsete nel workflow sarebbe l'acustica architettonica, che è già coperta da Akabak, licenziato e funzionante. È un supplemento facoltativo e non un tassello mancante, quindi non blocca nulla.

## PA-003 - Propagare al template le correzioni trovate qui

Data di apertura: 2026-09-04. Stato: aperta su due voci su cinque, riscritta sui fatti il 2026-09-12.

Che cosa va fatto. Portare al progetto `template-claude-developing` le correzioni nate qui, così che non vadano perdute alla prossima istanziazione. La voce è stata riscritta il 2026-09-12 perché tre delle quattro correzioni originali erano già state fatte nel template da una sessione che ha lavorato là, e continuare a elencarle come aperte avrebbe fatto rifare lavoro fatto.

Chiusa il 2026-09-09, nel template e non qui. La ripropagazione degli strumenti tipografici nel pacchetto `fix-typography`, che era rimasto indietro rispetto alle copie in `tools/`: il confronto del 2026-09-12 mostra che nel template la copia alla radice e quella nel pacchetto sono ora identiche per tutti e cinque i file, quindi lo sfasamento non esiste più. Chiusa anche l'incoerenza fra le regole di prudenza di `fix-accents.py` e `fix-missing-accents.py`, che corrompeva le forme elise nei file di codice: la versione nuova di `fix-accents.py` porta una funzione dedicata, `togli_residuo`, che rimuove l'apostrofo rimasto dopo una vocale già accentata e lo conta in una voce propria delle statistiche, cioè dichiara quante volte ha riparato invece di quante volte ha convertito.

Conseguenza per questo progetto, ed è il motivo per cui la voce ha prodotto lavoro invece di essere solo aggiornata. Il progetto era rimasto indietro rispetto al template su quattro strumenti su cinque, e le sue copie portavano ventidue apostrofi orfani prodotti proprio dal difetto che il template ha poi corretto: nove in `tools/fix-dashes.py`, due in `tools/md-unwrap.py` e gli undici corrispondenti nelle copie sotto `.claude/templates/`. Adottando le versioni del template le ventidue occorrenze sono sparite, verificato con una ricerca dedicata. Il racconto è in MS-091.

Compiuta sul disco del template il 2026-09-17, e riscritta perché poggiava su un fatto falso. La negazione nel `.gitignore` che rende versionabili i modelli `_notes` sotto `.claude/templates/` è stata aggiunta al template, ma la motivazione con cui questa voce la chiedeva era sbagliata: diceva che chi clona il template non riceve `DIARIO.md`, `RESOCONTO.md`, `RESUME-PROMPT.md` e `TEST-CHECKLIST.md`, mentre `git ls-files` li elenca tutti e quattro come tracciati, perché un pattern del `.gitignore` governa i soli file non tracciati e quei modelli erano entrati nella storia prima che la regola esistesse. La negazione resta giusta con una motivazione diversa, cioè prevenire il caso futuro: un modello aggiunto domani sotto quel percorso sparirebbe in silenzio e `git add` lo rifiuterebbe senza `-f`. Il ritiro e la misura sono in MS-130.

Chiusa il 2026-09-17, e non da questo progetto. La correzione di stile nella skill `studio-didattico` è caduta da sé: il template ha risolto la stessa questione togliendo l'enfasi invece di convertirla in corsivo, il che rispetta la regola allo stesso modo, e la copia qui è stata allineata a quella forma. Non resta nulla da propagare su questa voce.

Compiuta sul disco del template il 2026-09-17, nata lo stesso giorno. La quinta causa nella sezione sul contesto di shell di `git-commands-format.md`, cioè la macchina. Le quattro cause che il template elenca riguardano tutte lo stato di una shell su un computer dato, e nessuna copre il caso in cui il blocco venga incollato su un computer diverso da quello per cui è stato scritto: un alias SSH è una riga nel file di configurazione di una singola macchina e non una proprietà della rete, quindi un blocco che lo nomina è eseguibile su una macchina sola e il suo nome non lo dice. Il caso è stato osservato qui il 2026-09-17 ed è registrato in MS-126; il paragrafo è già scritto nella copia di questo progetto e va portato là. Nel passaggio l'alias concreto è diventato un segnaposto, perché il template non deve nominare la macchina di un singolo progetto e un esempio con un nome reale invita a copiarlo invece che a sostituirlo. Come le altre due voci, resta da committare e da unire: il template è sul ramo `pacchetto-allineamento`.

Non aperta e non chiusa, perché il confronto non l'ha decisa. La gestione dei percorsi cross-disco nei tre strumenti tipografici, diagnosticata in MS-014: il confronto per occorrenze degli idiomi rilevanti dà lo stesso numero nelle due versioni, quindi l'aggiornamento non l'ha né introdotta né tolta. Va verificata con un caso minimo su due lettere di unità diverse prima di dichiararla in un verso o nell'altro, e il caso minimo è già descritto in MS-014.

In corso, e va verso il template, aggiunta il 2026-09-14 ed eseguita in parte lo stesso giorno. Il registro dei microstep, cioè `docs/OPERATIONS-LOG.md` con la sua convenzione, non esisteva nel template: una ricerca su `PROJECT-SYSTEM.md` non trova alcuna occorrenza né di `OPERATIONS-LOG` né di `microstep`, mentre la forma `append-only` vi compare per `memory/progress.md` e per il registro delle decisioni. È quindi un pattern nato qui, e risolve un problema che i file di memoria del template non coprono, cioè il tracciamento dell'intervento singolo con la sua verifica e il suo esito. È stato quindi creato nel template come pacchetto opzionale `operations-log`, con README, modello del registro, modello della pagina di tracciabilità e riga nel catalogo `PACKAGES.md`, comprese le due regole aggiunte lo stesso giorno, cioè la dichiarazione del legame con lo scopo del progetto e l'indice delle voci superate. È MS-098.

Resta aperta la parte che non dipende da questo progetto: il commit nel template. Il `git status` di quel repository, letto il 2026-09-14, riporta ventuno file modificati e quattro non tracciati, tutti non committati, e fra essi ci sono proprio i file da cui MS-091 ha preso le versioni nuove. Ne discende una correzione di lettura di MS-091: il template è avanti sul disco e non nella storia di git, quindi chi lo clonasse oggi non riceverebbe né la regola `chat-non-e-memoria.md`, né la riparazione degli apostrofi orfani, né i due pacchetti, né il registro dei microstep. Il quadro è stato precisato il 2026-09-14 in MS-099, leggendo il `git status` completo: il template non è su `main` ma sul ramo `pacchetto-allineamento`, allineato con il proprio remoto. Ne segue che la propagazione non si chiude con un commit ma con una unione, perché anche una volta committati quei file resterebbero su un ramo di lavoro e non raggiungerebbero chi clona il template.

Criterio di completamento. Le voci aperte risultano presenti nel template, verificate con un confronto e non con un ricordo, e questa voce si chiude dichiarando la data. La verifica non decisa produce invece un microstep con il suo esito.

Perché non si fa da qui e subito. È una modifica a un altro repository, quindi è una decisione dell'utente su quel progetto, e va fatta aprendo una sessione là invece di scrivere da qui: la direzione di propagazione del blocco dell'ambiente è unidirezionale per scelta, e lo stesso principio vale a maggior ragione fra un progetto e il template da cui discende.
## PA-004 - Ispezionare il disco G: e il materiale EASE Focus 3.1.10 del workshop K-array

Data di apertura: 2026-09-07. Stato: *aperta, bloccata*.

Che cosa va fatto. Collegare il disco `G:` e ispezionare il percorso `G:\LIBRARY\LOUDSPEAKERS & ELECTROACOUSTIC\K-ARRAY WORKSHOP\EASE Focus (k-array)`, per stabilire che cosa contenga, se vada trasferito sulla macchina e se contenga materiale non presente altrove.

Da dove viene. In entrambe le copie del corredo, sul Desktop e su `J:`, esiste un collegamento chiamato `EASE_Focus_v3.1.10 (k-array) - collegamento.lnk` al posto della cartella. La lettura del collegamento ha rivelato il percorso di destinazione, che sta su un disco `G:` mai menzionato prima in nessun documento di questo progetto. Il disco non risultava fra le unità montate al momento della verifica, quindi il contenuto non è stato ispezionato.

*Avvertenza sulla lettera, aggiunta il 2026-09-08.* La lettera `G:` non identifica quel disco e non va usata come se lo facesse. Il 2026-09-08 è stata assegnata a una chiavetta Kingston DataTraveler da 57,7 GB collegata per preparare il supporto di installazione, che con il materiale del workshop non ha nulla a che vedere: Windows assegna la prima lettera libera, quindi la stessa lettera indica dispositivi diversi in momenti diversi, e lo stesso dispositivo può presentarsi con lettere diverse. Ne segue che il criterio di riconoscimento del disco cercato è il *contenuto*, cioè la presenza della cartella `LIBRARY` con il percorso completo indicato sopra, e non la lettera. Vale anche per lo strumento di controllo: trovare quel percorso su una lettera è una conferma, non trovarlo significa soltanto che quel dispositivo non è collegato adesso, e la lettera occupata da qualcos'altro non è un indizio di nulla.

Che cosa si sa e che cosa non si sa. Si sa dove punta il collegamento, e si sa dal documento sorgente che il pacchetto della 3.1.10 comprendeva l'installer InstallShield, i due servizi di database AFMG, una cartella di dati, una cartella di configurazione predefinita e una cartella di esempi ed esercitazioni con un progetto di workshop e due GLL, cioè `Concert_v10.gll` e `KS5_v4.gll`. Non si sa se il contenuto su `G:` corrisponda a quella descrizione, né se contenga altro.

Perché la priorità è bassa. La versione da installare è la 3.1.260, per le ragioni discusse in `docs/30-modellazione-e-simulazione.md`: la 3.1.10 e la 3.0.18 sono superate, i file GLL sono retrocompatibili, e tre versioni dello stesso programma in tre prefix sono manutenzione senza ritorno. Il materiale del workshop ha però un valore residuo che vale nominare, cioè i progetti di esempio e i due GLL, che sono materiale didattico e non installazione.

Il criterio di completamento. Un inventario del percorso su `G:`, la decisione se trasferire qualcosa e, se sì, il suo ingresso nel manifest di trasferimento.

Nota metodologica. Questa voce nasce da una inferenza sbagliata corretta: si era concluso che il contenuto della 3.1.10 vivesse sul solo SSD, mentre il collegamento è identico su entrambe le copie e punta a un terzo luogo. La lezione operativa è che un collegamento va letto, non interpretato dal nome: due minuti di lettura del file hanno sostituito una supposizione con un percorso esatto.

## PA-005 - Completare le tre voci privilegiate della fase 0

Data di apertura: 2026-09-07. Stato: *aperta, due voci su tre compiute, e la terza è irrilevante*.

Che cosa va fatto. Tre controlli della fase 0 che l'accesso via chiave non permette di eseguire, perché `sudo` sulla macchina chiede la password e perché uno dei tre è un controllo in interfaccia grafica.

Il primo, lo stato di salute dell'SSD, è *compiuto il 2026-09-07 con esito positivo*. Il giudizio è `PASSED`, l'usura al 9 per cento, la riserva di blocchi al 100, gli errori di integrità zero, e il valore coincide con il 91 per cento di vita residua misurato nel 2025. Il disco non va sostituito, quindi la scelta resta fra installazione e aggiornamento. Il pacchetto `smartmontools` era già installato, quindi l'avvertenza su una possibile installazione da rete non serviva. Il dettaglio, con la lettura dei due numeri che sembrano allarmanti e non lo sono, è in `docs/10-ambiente/fotografia-macchina-2026-09-07.md` e in MS-033.

Il secondo è la verifica del Machine Identifier di Akabak, ed è *compiuto il 2026-09-07*. Il valore letto nella finestra del release code coincide con quello nella scheda riservata sotto `_notes/`, il release code inserito coincide anch'esso, e il programma dichiara la licenza valida. Il dettaglio, con i tre fatti collaterali che la finestra ha portato in dote, è in MS-052 e in [90-riferimenti/licenze-e-registrazioni.md](90-riferimenti/licenze-e-registrazioni.md).

Il terzo è l'esito reale di `sudo apt update`. Le prove HTTP lo rendono prevedibile, perché archivio, mirror e security rispondono 200, ma prevedibile non è verificato. Va detto però che ADR-013 lo ha reso *irrilevante*: su un sistema che verrà azzerato l'esito di `apt update` non informa nessuna decisione, e la voce resta elencata solo per non dichiarare compiuto ciò che non lo è.

Il criterio di completamento. I due esiti che contano sono registrati e la fotografia della fase 0 è aggiornata di conseguenza; la voce si chiude quando la macchina viene azzerata, perché a quel punto il terzo controllo non ha più oggetto.

## PA-006 - Riconfermare o rivedere la scelta fra installazione pulita e aggiornamento in posto

Data di apertura: 2026-09-07. *Chiusa il 2026-09-07.* Esito: l'utente ha riconfermato l'installazione pulita di Ubuntu Studio 26.04 LTS sulla base corretta, cioè su tre motivi invece di quattro con l'ambiente pulito come dominante, e ha scelto di eseguire il lavoro privilegiato con comandi preparati e lanciati a mano, senza regole `sudoers`. La decisione è registrata come ADR-013, che supera lo stato di attesa di ADR-011.

La conseguenza operativa che ne discende, e che non era ovvia: la pulizia dell'ambiente Wine *non si esegue*, perché pulire un sistema che verrà azzerato è lavoro che si butta. L'ambiente pulito si ottiene per costruzione dalla reinstallazione. Per la stessa ragione non si applicano i 134 pacchetti pendenti e non si esegue il riavvio richiesto.

Il testo che segue è quello originale della voce, conservato perché documenta i termini su cui la decisione è stata presa.

Che cosa va fatto. Riconfermare ADR-006, cioè l'installazione pulita della 26.04 LTS, oppure scegliere l'aggiornamento in posto, sapendo che uno dei quattro motivi originali è venuto meno.

Perché è aperta. La decisione era stata confermata dall'utente il 2026-09-04 sulla base di quattro motivi, e la verifica del 2026-09-07 ne ha smentito il primo: non ci sono due aggiornamenti in cascata attraverso archivi storici da evitare, perché `do-release-upgrade` offre direttamente la 26.04.1 LTS. Tenere una decisione confermata quando una delle sue gambe è caduta significherebbe farla passare per più solida di quanto sia. La revisione è registrata come ADR-011.

Che cosa cambia fra le due strade, in concreto. L'aggiornamento in posto è oggi: applicare 134 pacchetti pendenti, riavviare, disattivare i due repository WineHQ, ed eseguire un solo `do-release-upgrade`. L'installazione pulita è la procedura in undici fasi, e il suo guadagno è un ambiente Wine ricostruito senza la sedimentazione documentata, più la rimozione dell'architettura `i386` e delle sorgenti residue.

Il criterio di completamento. Una scelta dichiarata, e ADR-006 riconfermata oppure superata da una voce nuova.

## PA-007 - Cancellare la copia del corredo sul Desktop della postazione

Data di apertura: 2026-09-07. *Compiuta il 2026-09-08.* Stato: chiusa.

L'esito. La cartella `C:\Users\Utente\Desktop\Progetto stanza (software)`, 650 file per 2,3 GB, è stata cancellata dall'utente e non esiste più, verificato. Nell'ordine prescritto: prima la riverifica delle impronte sulla macchina, che ha dato 8 file del manifest e 273 file del corredo tutti coincidenti, e subito dopo la cancellazione. Le voci utili del corredo restano in due copie indipendenti, quella sulla macchina e quella dentro l'archivio di `/home`; delle otto voci scartate dal censimento si è perduta l'unica copia, come previsto e voluto, perché per ciascuna esiste una sostituzione nativa o gratuita già disponibile.

Il testo che segue documenta i termini su cui la voce era stata sbloccata, ed è *superato dall'esecuzione*.

Detto senza giri di parole, perché la domanda è stata posta due volte: *la cartella si può cancellare, oggi, e l'unica cosa che si perde è quella che il censimento ha deciso di non tenere.* Non c'è nessuna condizione residua da attendere.

La condizione che c'era è la copia di sicurezza di `/home` fuori dalla macchina, ed è soddisfatta: archivio `tar` di 4,4 GB, verificato con 13.498 file nell'archivio contro 13.498 sulla macchina e i permessi conservati. Si veda MS-049. L'archivio è stato spostato dall'utente da `E:\_backup-ubuntu-studio\` a `C:\Users\Utente\Desktop\_backup-ubuntu-studio\`, con dimensione identica al byte, quindi la verifica di MS-049 vale ancora per quel file; lo strumento di controllo cerca l'archivio per nome in entrambe le posizioni proprio perché un file si sposta e un controllo che inchioda una cartella dichiara assente ciò che è soltanto altrove.

Va corretto in meglio il ragionamento con cui la voce era stata aperta. Avevo scritto che cancellare il Desktop di Windows avrebbe portato le voci utili a una copia sola: non era vero, perché sulla macchina ne esistono due indipendenti, cioè l'albero organizzato sotto `~/electroacoustics` e il materiale grezzo già presente sulla scrivania della macchina, scoperto in MS-048. La ragione valida che resta è diversa e più precisa: quelle due copie vivono sulla stessa partizione dello stesso disco, quindi rispetto al rischio che il backup deve coprire non sono due copie ma una. Il backup su un supporto diverso è ciò che le rende due, e adesso c'è.

Che cosa va fatto. Cancellare `C:\Users\Utente\Desktop\Progetto stanza (software)`, 650 file per 2,3 GB.

Il testo che segue, in questi due paragrafi, è quello con cui la voce era stata aperta ed è *superato*: si conserva perché documenta la condizione che allora mancava e che oggi è soddisfatta, non perché descriva lo stato attuale.

Perché non ora, ed è la risposta a una domanda diretta dell'utente. Il ragionamento "se abbiamo tutto quello che serve possiamo cancellare anche il Desktop" è corretto sul contenuto e sbagliato sul momento. Oggi le voci utili del corredo esistono in due copie, una sul Desktop e una sulla macchina. Cancellare il Desktop le porta a *una copia sola*, e quella copia vive su una macchina che sta per subire una reinstallazione con riformattazione di una partizione. Ridurre a una copia proprio prima di una operazione che tocca le partizioni è il momento peggiore possibile.

La condizione di sblocco è quindi una sola: *la copia di sicurezza di `/home` fuori dalla macchina*, cioè la fase 1.3 della procedura di installazione pulita. Fatta quella, le copie tornano a essere due, una sulla macchina e una nel backup, e il Desktop diventa la terza: a quel punto è ridondante e può andare.

Che cosa si perde davvero, distinto con precisione. Delle sei voci trasferite non si perde nulla, perché sono sulla macchina con le impronte verificate. Delle otto voci scartate dal censimento si perde l'unica copia esistente, perché non sono state trasferite di proposito. Il censimento stabilisce che nessuna serve al progetto e che per ciascuna esiste una sostituzione nativa o gratuita già disponibile, quindi la perdita è voluta e non accidentale; ma va detta, perché è irreversibile.

Il criterio di completamento. La cartella non esiste più sul Desktop, e sulla macchina il corredo è presente con le impronte verificate più una copia di sicurezza di `/home` fuori dalla macchina.

Il comando. La condizione della fase 1.3 è soddisfatta, quindi si può lanciare.

```powershell
bash tools/transfer-to-studio.sh --impronte
Remove-Item -LiteralPath "C:\Users\Utente\Desktop\Progetto stanza (software)" -Recurse -Force
```

Il primo comando non è decorativo: riverifica che il materiale sulla macchina corrisponda ancora, e va lanciato subito prima della cancellazione e non ore prima.

## PA-014 - Decidere la via verso il GLL del monitor, dato che ARTA in modalità dimostrativa non salva

Data di apertura: 2026-09-15. Stato: aperta.

Che cosa va fatto. Decidere come si produrrà il file GLL del monitor autocostruito, sapendo che la via attribuita finora a questo compito non è percorribile senza spesa.

Perché esiste. ARTA è shareware, e il limite della modalità dimostrativa è stato misurato il 2026-09-15 invece di essere rimandato: il programma è pienamente funzionante tranne che per il caricamento e il salvataggio dei file, come dichiarano concordi la finestra di avvio e il file `Readme.txt`. Produrre un GLL è esattamente un salvataggio, quindi il ruolo che la documentazione di questo progetto assegna ad ARTA non è esercitabile senza licenza. Non è una limitazione aggirabile con un accorgimento, perché non riguarda che cosa il programma sappia fare ma che cosa gli sia permesso conservare. Il racconto è in MS-116.

Condizione di sblocco. Nessuna condizione esterna la blocca in senso stretto, ma non ha senso deciderla adesso: la fase 8 richiede un diffusore costruito e misurato, che non esiste. La voce si sblocca quando il progetto arriva alla caratterizzazione del prototipo.

Direttiva dell'utente del 2026-09-16, che restringe il campo e va rispettata invece di essere riaperta. La via da cercare è un sostituto gratuito e open source che copra quella funzione, non l'acquisto della licenza. L'acquisto resta l'ultima risorsa, da considerare soltanto se la ricerca dimostra che un sostituto non esiste, e quella dimostrazione va fatta e scritta, non assunta.

Criterio di completamento. La via è scelta e motivata, e le alternative scartate sono nominate. La ricerca parte dagli strumenti liberi che misurano una risposta e ne esportano i dati, e deve chiarire un punto che oggi non è chiaro: se il formato GLL sia producibile soltanto con gli strumenti del suo autore, nel qual caso il sostituto non riguarda la produzione del GLL ma il modo di fare il confronto senza di esso. Distinguere le due cose è la prima cosa da fare, perché cercare un sostituto per una funzione che nessuno strumento libero può svolgere sarebbe tempo perso.

Che cosa non va fatto adesso. Comprare la licenza in anticipo perché sembra la via più semplice. Il programma serve alla fine del progetto, i prezzi e le versioni cambiano, e una licenza acquistata oggi per un uso fra molti mesi è denaro immobilizzato su una scelta non ancora istruita.

## PA-015 - Impedire meccanicamente agli strumenti tipografici di scrivere sotto .claude/templates/

Data di apertura: 2026-09-16. Stato: compiuta. Costruita nel template il 2026-09-16 con MS-124, arrivata qui il 2026-09-17 con il riallineamento di MS-129, dove la sua efficacia è stata anche misurata.

Che cosa va fatto. Aggiungere agli strumenti `fix-accents.py`, `fix-missing-accents.py` e `fix-dashes.py` un rifiuto esplicito a scrivere qualunque file che si trovi sotto `.claude/templates/`, con un messaggio che ne spieghi la ragione invece di fallire in silenzio.

Perché esiste. `CLAUDE.md` vieta di correggere in questo repository i file che sono copie del template, perché farlo allarga la divergenza che PA-003 esiste per chiudere. Il divieto è oggi affidato all'attenzione di chi lancia il comando, ed è stato violato due volte nella stessa sessione del 2026-09-15 e 2026-09-16, la seconda meno di un'ora dopo averlo scritto come regola in MS-115. Il racconto della ripetizione e della conseguenza che se ne trae è in MS-123.

Il principio non è nuovo in questo progetto ed è precisamente quello che rende affidabile `md-unwrap`, che si rifiuta di scrivere un file il cui rendering cambierebbe invece di fidarsi di chi lo lancia. Una convenzione che un comando può violare per distrazione va difesa dal comando.

Condizione di sblocco. Nessuna condizione esterna la blocca, ma la modifica non va fatta in questo repository: quegli strumenti sono condivisi con `template-claude-developing` e una modifica locale allargherebbe proprio la divergenza in questione. Appartiene quindi alla propagazione all'indietro tracciata in PA-003, ed è una ragione in più per eseguirla.

Criterio di completamento. I tre strumenti rifiutano un percorso sotto `.claude/templates/` con un messaggio esplicito, il rifiuto è coperto da un caso nella suite `tools/test-tipografia.py`, e la modifica è nel template e non soltanto qui.

Esito del 2026-09-16. Tutti e tre i criteri sono soddisfatti nel template, con una aggiunta che la prova ha reso necessaria: il rifiuto ha un interruttore esplicito, `--includi-modelli`, perché dentro il template quei file sono gli originali e una guardia senza scavalcamento avrebbe impedito la manutenzione tipografica del template stesso. La prova nuova lancia gli strumenti come processi, perché la guardia vive nella raccolta dei file e non nella funzione di trasformazione, ed è stata sottoposta alla verifica di non vacuità prescritta da `prove-che-misurano.md`.

## PA-013 - Escludere i backup Veeam dalla sincronizzazione giornaliera di sync-dev

Data di apertura: 2026-09-15. Stato: aperta, e da compiere prima del primo backup se la destinazione cambiasse.

Che cosa va fatto. Dichiarare allo script `C:\Scripts\sync-dev` della postazione di ignorare i backup Veeam, sia quello di questa macchina sia gli altri che vi si accumuleranno suddivisi per macchina, finché il NAS domestico non sarà disponibile.

Perché esiste, e perché non è un dettaglio. Lo script copia ogni giorno il contenuto di `E:` verso l'SSD esterno T7, cioè il volume `J:`. Un backup di macchina intera collocato sotto `E:` verrebbe quindi ricopiato integralmente ogni giorno verso `J:`, che è circa 30 GB di traffico e di scrittura quotidiani su un disco a stato solido, per duplicare una copia che non cambia. È il motivo per cui la destinazione scelta in PA-011 è la radice di `J:` e non una cartella di `E:`: si evita il problema invece di risolverlo.

La voce resta aperta lo stesso, e non è una precauzione oziosa. La destinazione attuale è dichiaratamente provvisoria e cambierà quando il NAS esisterà; nel momento in cui un backup finisse sotto `E:`, anche solo di passaggio, l'esclusione diventerebbe necessaria e nessuno se ne ricorderebbe. La conoscenza che serve a scriverla, cioè che lo script esiste e che cosa copia, è disponibile adesso e va fissata adesso.

Condizione di sblocco. Nessuna condizione esterna la blocca: è eseguibile in qualunque momento sulla postazione. Diventa obbligatoria quando una destinazione di backup cade sotto un percorso che `sync-dev` copia.

Criterio di completamento. Lo script porta una regola di esclusione che nomina i backup Veeam per percorso o per estensione, la regola è verificata con una corsa a vuoto che mostra il backup non fra i file da copiare, e il comportamento è documentato nel repository che possiede lo script, che non è questo.

Dove vive la decisione di fondo. Il consolidamento del NAS per la macchina privata è tracciato in `E:\home-lab-cybersec-networking\nas-consolidation`, ed è quello il progetto che chiuderà sia questa voce sia la provvisorietà della destinazione di PA-011. Qui resta il legame, perché una voce che dipende da un altro progetto senza nominarlo è una voce che nessuno sa chiudere.

## PA-008 - Recuperare 1,2 GiB di cartelle di servizio su J:

Data di apertura: 2026-09-07. Stato: *aperta, eseguibile adesso*.

Che cosa va fatto. Cancellare da `J:` le tre cartelle di servizio che contengono lo spazio recuperabile, verificate presenti il 2026-09-07.

Va chiarito un equivoco emerso in sessione: l'agente non ha cancellato nulla su quel disco. La cartella `Progetto stanza (software)` risultava già assente quando è stata verificata, e le tre cartelle di servizio ci sono ancora tutte.

| Voce | Peso | Natura |
|---|---|---|
| `J:\FOUND.002` | 429 MiB | 77 frammenti orfani di chkdsk, del 27 luglio |
| `J:\FOUND.000` | 412 MiB | 90 frammenti orfani di chkdsk, del 30 giugno |
| `J:\.Spotlight-V100` | 371 MiB | 76 file di indice di ricerca di macOS |

Le altre sei voci di servizio, cioè `FOUND.001`, `FOUND.003`, `FOUND.004`, `.Trashes`, `.fseventsd` e `.TemporaryItems`, esistono ma sommate non arrivano a un megabyte: cancellarle non cambia niente e non vale il gesto. `$RECYCLE.BIN` si svuota dal cestino e `System Volume Information` va lasciata al sistema.

Una precauzione sulle due `FOUND` grandi. Contengono 167 file di dati che il filesystem aveva perso e che `chkdsk` ha recuperato senza il loro nome, quindi con nomi del tipo `file0001.chk`. Nella grande maggioranza dei casi sono inservibili, ma la maggioranza non è la totalità: guardarli prima costa un minuto.

```powershell
Get-ChildItem "J:\FOUND.000", "J:\FOUND.002" -Recurse -File | Sort-Object Length -Descending | Select-Object -First 20 Length, FullName
```

Il comando di cancellazione, dopo aver guardato.

```powershell
Remove-Item -LiteralPath "J:\FOUND.000", "J:\FOUND.001", "J:\FOUND.002", "J:\FOUND.003", "J:\FOUND.004", "J:\.Spotlight-V100" -Recurse -Force
```

Il criterio di completamento. Le tre voci non esistono più e `python tools/analisi-ssd-esterno.py` riporta un recuperabile prossimo a zero.

Nota su ciò che *non* va cancellato, perché è la parte contro-intuitiva. I due archivi di backup da 25,8 e 19,4 GiB restano: il confronto dei loro indici, fatto il 2026-09-07, dimostra che nessuno dei due contiene l'altro, e cancellare il più vecchio costerebbe 145.478 versioni di file che non esistono altrove in forma archiviata. Il dettaglio è in `docs/90-riferimenti/pulizia-ssd-esterno.md`.

## PA-009 - Leggere lo SMART dell'SSD esterno

Data di apertura: 2026-09-07. *Compiuta il 2026-09-08.* Stato: chiusa.

L'esito, e risponde alla domanda che la voce poneva. Il *supporto è sano*: usura a zero, riserva disponibile al 100 per cento su una soglia di 10, zero errori di integrità dei dati, zero voci nel registro errori, giudizio complessivo 100 per cento dopo 2795 ore. Il disco non va sostituito e può continuare a ospitare materiale, con l'avvertenza generale che un disco rimovibile non è il posto dove tenere l'unica copia di qualcosa.

Delle due cause possibili cade quindi la seconda, cioè il difetto del supporto, e resta la prima, cioè la rimozione senza espulsione sicura, coerente con i *122 spegnimenti non protetti su 742 cicli* di alimentazione. Su quel numero va applicato un correttivo prima di usarlo come prova, perché su un disco USB il contatore si incrementa ogni volta che il ponte non inoltra al controller la notifica di spegnimento, cosa che molti ponti non fanno mai: una parte dei 122 è fisiologica dell'involucro. Le cinque cartelle `FOUND` non hanno invece spiegazioni fisiologiche, e restano la prova che il volume è stato staccato con scritture in sospeso.

La regola operativa che ne discende è una sola: espellere il volume prima di staccarlo, sempre. La misura completa, il confronto con il disco di sistema della postazione e l'ostacolo dei privilegi su Windows sono in [90-riferimenti/pulizia-ssd-esterno.md](90-riferimenti/pulizia-ssd-esterno.md) e in MS-058.

Il testo che segue è quello originale della voce, conservato perché documenta i termini su cui la verifica è stata impostata.

Che cosa va fatto. Leggere lo stato di salute del disco `J:` con CrystalDiskInfo da Windows, oppure con `smartctl` collegandolo alla macchina Ubuntu Studio.

Perché conta. Sul volume ci sono cinque cartelle `FOUND`, dal 30 giugno al 3 settembre, cioè cinque riparazioni del filesystem in poco più di due mesi. Le cause possibili sono due e portano a rimedi opposti: la rimozione senza espulsione sicura, che si corregge con una abitudine, oppure un difetto del supporto, che si corregge sostituendolo. Solo lo SMART distingue le due.

L'elemento di contesto che rende la prima ipotesi meno rassicurante: il disco interno della macchina ha 24 spegnimenti non puliti su 135 accensioni. Due dischi con sintomi diversi che puntano nella stessa direzione sono un indizio più forte di due sintomi isolati.

Gli indicatori da guardare sono gli stessi usati per il disco interno: percentuale di usura, riserva di blocchi disponibili e conteggio degli errori di integrità dei dati.

Il criterio di completamento. Un esito registrato, e la conseguente decisione se quel disco possa continuare a ospitare backup oppure vada sostituito.

Nota di priorità. Media, e più alta di quanto sembri: su quel disco vivono 371 GiB di materiale personale e due archivi di backup che il confronto ha dimostrato non ridondanti. Se il supporto è malato, quello è il posto sbagliato dove tenerli.

## PA-016 - Riallineare il progetto al template dopo i sei commit dal 2026-09-15

Data di apertura: 2026-09-17. Stato: compiuta lo stesso giorno per la parte documentale, aperta sulla sola decisione relativa a `hooks-starter`. La misura dello scarto è in MS-127, l'esecuzione in MS-129.

Che cosa va fatto. Portare qui dal template `E:\template-claude-developing` quattro cose, in quest'ordine, che è quello di quanto pesano. La regola `.claude/rules/prove-che-misurano.md`, che qui non esiste. Il paragrafo aggiunto oggi a `interaction-style.md` sull'unica eccezione al divieto di grassetto, cioè l'etichetta di campo nei documenti a record fissi. Le versioni aggiornate dei quattro strumenti tipografici, cioè `fix-accents.py`, `fix-dashes.py`, `fix-missing-accents.py` e `test-tipografia.py`, che qui sono indietro rispettivamente di 56, 50, 165 e 219 righe e che contengono la guardia di PA-015. E la valutazione, che è una decisione e non un travaso, se istanziare qui il pacchetto `hooks-starter` con i suoi quattro hook di ciclo e i due strumenti nuovi `check-catalogo.py` e `check-copie-modelli.py`.

Perché esiste, e perché una delle voci pesa più delle altre. Due delle quattro riguardano file che questo progetto carica a ogni sessione, e una divergenza su un file caricato sempre si applica sempre, in silenzio, senza che nessuno la veda: è il caso di `interaction-style.md`. La terza riguarda la catena di verifica che si esegue prima di ogni commit, e dentro quello scarto c'è la guardia nata da un errore commesso in questo repository e costruita nel template con MS-124, che finché non torna indietro lascia possibile proprio qui l'errore che impedisce altrove.

Il motivo per cui lo scarto si riapre, invece, non è una dimenticanza e va scritto perché si ripeterà. Il verso discendente, cioè dal template ai progetti, non ha alcun automatismo e dipende da qualcuno che se ne ricordi, mentre il verso ascendente è un atto deliberato che si compie quando una cosa nasce quaggiù. Nei cinque giorni fra il 2026-09-12 e il 2026-09-17 il verso ascendente è stato percorso due volte, con MS-124 e MS-125, e quello discendente nessuna.

Condizione di sblocco. Nessuna. Va però eseguita dopo la chiusura di PA-011 e non durante, perché tocca la regola di stile e gli strumenti della catena di verifica mentre un lavoro operativo è aperto, e mescolare i due giri renderebbe ambiguo quale dei due abbia causato un eventuale problema.

Criterio di completamento. La regola nuova è presente sotto `.claude/rules/` e nominata in `CLAUDE.md` fra i satelliti tracciati; `interaction-style.md` porta il paragrafo dell'eccezione; i quattro strumenti coincidono con quelli del template, verificato con un confronto file per file e non a occhio; la catena di verifica prima di un commit passa per intero; e la decisione su `hooks-starter` è registrata, qualunque sia, perché una decisione di non adottare è un esito e non un vuoto. Quando il criterio è soddisfatto, PA-015 si chiude insieme a questa, perché la guardia sarà finalmente presente dove serviva.

Voce discendente aggiunta il 2026-09-17 mentre la propagazione ascendente era in corso, ed è la conferma sul campo di ciò che MS-127 diceva in astratto. Il commit `4b7411d` del template, dello stesso giorno, aggiunge a `git-identity-and-repo.md` un quarto asse di identità, cioè la GitHub CLI con il proprio token OAuth su HTTPS distinto dalla chiave SSH, e nello stesso atto de-istanzia quel file portandolo da un elenco di profili concreti a una procedura di rilevamento. Qui quel file è nella forma istanziata con gli alias, le chiavi e le due identità reali di questa postazione, quindi allinearlo non è una copia ma una re-istanziazione, ed è lavoro diverso da quello già fatto. Va eseguito con il resto di questa voce.

Esito del 2026-09-17, poche ore dopo l'apertura, su istruzione esplicita dell'utente che ha superato la mia proposta di rimandare. Quattro criteri su cinque sono soddisfatti e verificati: la regola nuova è presente e nominata in `CLAUDE.md`, `interaction-style.md` porta il paragrafo dell'eccezione, i quattro strumenti coincidono con quelli del template per confronto byte per byte tramite `check-copie-modelli.py`, e la catena di verifica passa per intero. Sono arrivati inoltre due controlli che l'apertura non prevedeva, cioè `check-copie-modelli.py`, entrato nella sequenza obbligatoria, e `check-catalogo.py`, e i sei pacchetti di modelli che mancavano. PA-015 si chiude con questa, perché la guardia è ora presente qui e la sua efficacia è stata misurata e non solo dichiarata. Resta aperto il quinto criterio, cioè la decisione su `hooks-starter`, che è una scelta e non un travaso: va posta all'utente quando il fronte operativo sarà chiuso.

## PA-017 - Secondo backup a setup finito, e la decisione se renderlo incrementale

Data di apertura: 2026-09-17. Stato: aperta, con condizione di sblocco non ancora soddisfatta.

Che cosa va fatto. Prendere un secondo backup della macchina quando la ricostruzione sarà davvero finita, cioè a sottofase 8.6 chiusa e fase 8 superata in tutti e cinque i criteri di uscita, e decidere in quella occasione se il secondo punto debba essere una copia completa nuova oppure un incrementale sul primo.

Perché esiste. L'archivio del 2026-09-17 che chiude PA-011 fotografa una macchina il cui allestimento è superato in quattro criteri su cinque: manca l'import GLL di EASE Focus, e se quel criterio si chiuderà cambiando la provenienza dei pacchetti di Wine, come MS-137 misura, lo stato del sistema sarà sensibilmente diverso da quello fotografato. Un archivio che non contiene l'ultima parte del lavoro protegge dal guasto del disco e non dal rifare il passo che è costato di più.

La richiesta dell'utente del 2026-09-17 parla di un backup manuale incrementale, e la parola incrementale porta con sé una decisione che conviene prendere consapevolmente invece di ereditarla dal comando. Il lavoro è già creato con `--maxPoints 2`, quindi una seconda corsa produce per costruzione un secondo punto di ripristino sulla stessa catena e non una copia indipendente: è il comportamento predefinito e non va chiesto. Il punto è che una catena lega i punti fra loro, quindi il secondo dipende dal primo, e un archivio danneggiato porta con sé entrambi. Una copia piena indipendente costa altri 17 GiB e non ha quella dipendenza.

Condizione di sblocco. Che la fase 8 sia chiusa in tutti e cinque i criteri di uscita, oppure che la sottofase 8.6 sia dichiarata chiusa in altro modo, per esempio rinunciando a EASE Focus. Un backup preso prima ripeterebbe l'errore che PA-011 evitava, cioè congelare uno stato intermedio che nessuno vuole ripristinare.

Criterio di completamento. Il secondo punto esiste, il suo esito è `Success`, è stato riletto con la stessa procedura del primo, cioè montandolo e confrontando impronte e conteggi, ed è stato portato fuori dalla macchina e verificato per impronta. La decisione fra catena incrementale e copia piena indipendente è registrata con il suo motivo, qualunque sia, perché una scelta ereditata da un valore predefinito non è una scelta. Vanno inoltre riprese in quella occasione le due cose che PA-011 ha rinviato dichiarandole, cioè la cifratura e la destinazione definitiva.

Un prerequisito nato il 2026-09-17 e da non dimenticare, perché costerebbe trentacinque gigabyte di archivio inutile. Sulla macchina restano due residui del tentativo di sostituzione di Wine, cioè l'archivio `~/prefix-prima-di-winehq-2026-09-17.tar` da 28 GiB e la copia danneggiata `~/wineprefixes.rotto-winehq` da 7,6 GiB. Sono entrambi sotto `/home`, quindi entrerebbero nel backup. Vanno cancellati prima della seconda corsa, e non prima di aver verificato che il corredo funzioni, il che è stato fatto in MS-142.

La procedura da seguire è quella di `docs/10-ambiente/veeam-agent-linux.md`, che dalla fase 5 in avanti vale identica per una corsa successiva.

## PA-018 - Decidere che fare del repository WineHQ rimasto sulla macchina

Data di apertura: 2026-09-21. Stato: aperta, senza condizione di sblocco. La misura che la apre è MS-145.

Che cosa va fatto. Decidere se rimuovere il file `/etc/apt/sources.list.d/winehq-resolute.sources` con la sua chiave in `/etc/apt/keyrings/winehq-archive.asc`, se lasciarlo dove è, oppure se conservarlo disattivato, ed eseguire la decisione presa.

Perché esiste. Il repository è il residuo del tentativo di sostituzione di Wine del 2026-09-17: MS-142 rimosse i pacchetti con purga e rimise quelli della distribuzione, ma il repository restò, e nessuno se ne accorse fino alla fotografia finale della fase 11. Non è una voce urgente, perché nessun pacchetto di quella provenienza è installato e `apt upgrade` non installa ciò che non c'è. È però uno stato dichiarato del sistema che nessuno ha deciso di lasciare, e la ragione per cui merita una decisione esplicita è che la prossima persona che legga quel file concluderà che il progetto usa WineHQ, che è esattamente il contrario di quanto MS-141, MS-142 e MS-145 hanno stabilito.

Le tre opzioni, con il loro costo. Rimuovere il file e la chiave è la scelta che lascia la macchina nello stato che i documenti descrivono, costa due comandi privilegiati e perde soltanto la comodità di riprovare, che oggi non serve a nulla perché MS-145 ha accertato che per Ubuntu 26.04 quel repository non pubblica alcuna metà a 32 bit. Lasciarlo dove è non costa nulla e conserva la divergenza fra documento e macchina, che è il difetto da cui questa voce nasce. Conservarlo disattivato, cioè rinominandolo in modo che apt lo ignori, è la via di mezzo e ha senso soltanto se si prevede di riprovare quando WineHQ pubblicherà di nuovo i386, cosa che nessuno ha annunciato.

La mia raccomandazione, che resta una raccomandazione. Rimuovere entrambi, perché il valore di una configurazione conservata sta nel poterla riusare, e qui la misura dice che non è riusabile su questa versione di Ubuntu. Se la decisione fosse invece di conservarla, va scritta qui con il motivo, perché una configurazione lasciata per scelta e una lasciata per dimenticanza hanno lo stesso aspetto.

Condizione di sblocco. Nessuna. Va eseguita sulla macchina con `sudo`, quindi in un terminale interattivo, secondo la prassi del progetto per cui il lavoro privilegiato si esegue a mano su comandi preparati.

Criterio di completamento. Lo stato delle sorgenti di apt sulla macchina coincide con quanto i documenti dichiarano, verificato rileggendo `/etc/apt/sources.list.d/` e non a memoria, e la decisione presa è scritta qui con il suo motivo qualunque essa sia.

## PA-019 - Verificare la catena audio da una sessione grafica attiva sulla console

Data di apertura: 2026-09-21. Stato: aperta, con una condizione di sblocco che dipende dalla presenza fisica dell'utente. L'accertamento che la apre è MS-146.

Che cosa va fatto. Rifare la verifica della catena audio della fase 6 da una sessione grafica attiva sulla console della macchina, e non da SSH, leggendo che PipeWire veda la scheda integrata, che esistano una uscita e un ingresso reali al posto del dispositivo fittizio, e che una riproduzione di prova si senta.

Perché esiste. La fotografia della fase 11 ha raccolto `pactl info` da una sessione SSH e ha riportato `Default Sink: auto_null`, cioè l'assenza di qualunque scheda, mentre ALSA vede regolarmente la `ALC887-VD`. MS-146 ha isolato due cause indipendenti, e nessuna delle due è un difetto di configurazione: la sessione grafica dell'utente non è la sessione attiva del posto, quindi `systemd-logind` ha assegnato allo schermo di accesso la lista di controllo di accesso sui nodi di `/dev/snd/`, e per giunta il processo `wireplumber` di quella sessione, iniziata il 2026-09-09, non ha i gruppi `audio` e `pipewire` che MS-077 aggiunse lo stesso giorno più tardi. Entrambe cadono con un accesso nuovo alla console.

Il punto che rende questa voce diversa da una semplice verifica rimandata è che l'esito raccolto finora non vale né in positivo né in negativo. Una misura fatta nel contesto sbagliato non dice che la catena audio sia guasta e non dice che funzioni, e trattarla come una delle due cose sarebbe il difetto che la regola sulle prove che misurano chiama vacuità: un risultato che si legge senza esercitare ciò che dichiara di esercitare.

Condizione di sblocco. Che l'utente si trovi davanti alla macchina e faccia un accesso nuovo alla sessione grafica. Non è automatizzabile e non va simulata da remoto, perché è precisamente il contesto a essere oggetto della verifica.

Criterio di completamento. Da una sessione attiva sulla console, `pactl list short cards` riporta la scheda integrata, `pactl info` riporta una uscita reale al posto di `auto_null`, il processo `wireplumber` di quella sessione porta i gruppi 29 e 982, e una riproduzione di prova si sente. L'esito va scritto in un microstep, anche se positivo, perché è la chiusura misurata di una domanda che oggi è aperta.

## Azioni compiute

Nessuna, per ora. Le voci compiute si spostano qui con la data e l'esito, e non si cancellano.
