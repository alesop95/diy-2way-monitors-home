# Azioni differite

> Registro delle azioni che non si possono compiere adesso perché dipendono da una condizione esterna, con la condizione di sblocco di ciascuna e il criterio con cui si stabilisce che sono compiute. Serve a un fine preciso: un promemoria che vive solo in una conversazione è perduto, mentre una voce qui sopravvive alla sessione, al riavvio e a un clone del repository.
>
> Lo strumento `tools/check-pending-actions.py` legge le condizioni verificabili in automatico e dice quali azioni sono diventate eseguibili. Conviene lanciarlo a inizio sessione.

## Come si legge una voce

Ogni azione ha un identificativo nella forma `PA-NNN`, una data di apertura, la descrizione di che cosa va fatto, la condizione che ne blocca l'esecuzione, il criterio di completamento e lo stato. Una voce non si cancella quando è compiuta: si marca come compiuta con la data, così che il registro resti la storia di ciò che è stato deciso e non solo di ciò che resta da fare.

## Sequenza operativa: che cosa deve fare l'utente, e in che ordine

Questa sezione esiste perché il registro per voce risponde alla domanda sbagliata. Dice per ciascuna azione se è eseguibile, ma non dice in che ordine affrontarle né quali appartengono alla procedura di installazione invece che a questo registro, e chi si siede al lavoro ha bisogno esattamente di quell'ordine. Si aggiorna quando cambia, e ogni voce rimanda al posto dove sta il dettaglio.

Le azioni sono numerate e nell'ordine in cui vanno eseguite. Dove una dipende dalla precedente lo dice; dove è indipendente lo dice, così che si possa saltare senza rompere nulla.

**1. Commit e push dei due repository.** Prima di tutto il resto, perché il lavoro documentale in attesa di commit è l'unica cosa che una sessione perduta porterebbe via. Indipendente da tutto ciò che segue.

**2. Cancellare la copia del corredo sul Desktop. Compiuto il 2026-09-08.** È PA-007, chiusa. Riverifica delle impronte e cancellazione eseguite nell'ordine e a distanza di minuti, 2,3 GB recuperati, nessun dato utile perduto.

**3. Leggere lo SMART dell'SSD esterno. Compiuto il 2026-09-08.** È PA-009, chiusa. Il supporto è sano, quindi delle due cause resta la rimozione senza espulsione: il disco non va sostituito e la regola è espellere il volume prima di staccarlo.

**4. Preparare la chiavetta di installazione. Compiuto il 2026-09-08.** È la fase 2 della procedura, chiusa. L'immagine è in `C:\Users\Utente\Desktop\_iso-ubuntu-studio\`, verificata due volte, per somma di controllo e per firma del file delle somme: è la **26.04.1**, cioè il point release, e non la 26.04 iniziale che la procedura nominava. La chiavetta Kingston da 57,7 GB è stata scritta con Rufus 4.15 portabile, verificato per firma Authenticode, in modalità DD e in otto minuti, e porta la tabella GPT dell'immagine con le sue tre partizioni. La verifica del supporto si fa al primo avvio, dal menu della chiavetta alla voce di controllo dei difetti, e **non** con un confronto di impronte contro l'immagine: su Windows quel confronto produce un falso allarme, per le ragioni registrate in MS-069.

**5. Controllare il firmware.** È la fase 3. Quattro voci nel setup UEFI, e una va cambiata adesso perché dopo costa una sessione: il Wake-on-LAN, senza il quale la macchina che si sospende va risvegliata a mano.

**6. Installare, conservando `/home`.** Sono le fasi 4 e 5, ed è il passo irreversibile. Il presidio contro l'unico rischio reale, l'errore umano nella selezione delle partizioni, è già in posizione: la copia di sicurezza di `/home` esiste su una macchina diversa ed è verificata.

**7. Ricostruire l'ambiente.** Sono le fasi da 6 a 9, cioè catena audio, Wine, programmi e licenza, strumenti nativi. Un avviso che vale più della sequenza: le fasi 7 e 8 sono state corrette il 2026-09-07 per ADR-016, e chi eseguisse una versione precedente otterrebbe un ambiente in cui Akabak non parte, perché l'architettura `i386` va dichiarata e non evitata.

**8. Igiene e chiusura.** Sono le fasi 10 e 11, cioè politica di aggiornamento, sospensione e accesso remoto, chiave SSH, indirizzo stabile, e la fotografia finale da confrontare con quella iniziale.

Restano fuori da questa sequenza le voci a bassa priorità che non dipendono da essa e non la bloccano: PA-002 sulla licenza di Ramsete, PA-003 sulla propagazione al template, PA-004 sul disco `G:`. Si affrontano quando capita l'occasione, non in un ordine.

## PA-010 - Verificare che i file personali siano tutti sulla macchina, prima di cancellarli altrove

Data di apertura: 2026-09-09. Stato: aperta.

Che cosa va fatto. Prima di cancellare qualunque copia di materiale personale che oggi vive fuori dalla macchina Ubuntu Studio, cioè sulla postazione Windows, sull'SSD esterno `J:` o sul disco `G:` non ancora ispezionato, va accertato che il corrispondente sia presente e integro dentro `/home/alesop95`. La verifica riguarda i file di lavoro personali e non il solo corredo software, quindi comprende i progetti Ardour, il materiale di acustica della stanza, i simulatori, i documenti sciolti sulla scrivania e tutto ciò che l'utente riconosce come proprio.

Perché conta, ed è una richiesta esplicita dell'utente. Il 2026-09-09 la reinstallazione ha conservato `/home` e la scrivania si è ripresentata con i suoi contenuti, il che rende naturale concludere che non manchi nulla. Quella conclusione non è verificata: si è osservato che le icone della scrivania ci sono e che `~/electroacoustics` conta 281 file per 728 MB come documentato, che sono due controlli su un perimetro molto più ampio. Cancellare una copia esterna sulla base di una impressione visiva è esattamente il genere di passo che non si può annullare.

Condizione di sblocco. Nessuna condizione esterna impedisce la verifica in sé, che si può fare adesso via SSH. La cancellazione delle copie esterne, invece, dipende da questa verifica e non va anticipata. La voce resta aperta finché l'inventario non è fatto e confrontato.

Criterio di completamento. Esiste un confronto documentato fra il contenuto personale delle copie esterne e quello di `/home/alesop95`, fatto per impronta del contenuto e non per dimensione occupata, dato che il tranello del `du -sh` è già costato una inferenza sbagliata in MS-024. Da quel confronto risulta un elenco esplicito di ciò che esiste solo fuori dalla macchina, e ogni voce di quell'elenco è stata trasferita oppure dichiarata volutamente non trasferita.

Nota sul software. La richiesta dell'utente comprende anche l'utilizzo del software, cioè non soltanto i file di dato ma la loro apribilità: un progetto Ardour o un modello Akabak conservato senza il programma che lo apre è un archivio e non un materiale di lavoro. La verifica va quindi estesa a quali formati restano leggibili sulla macchina dopo la ricostruzione dell'ambiente delle fasi da 6 a 9.

## PA-011 - Backup Veeam della macchina, a ricostruzione finita

Data di apertura: 2026-09-09. Stato: aperta.

Che cosa va fatto. Un backup completo della macchina Ubuntu Studio con Veeam, da eseguire quando la ricostruzione dell'ambiente è finita e verificata, non prima.

Perché conta, e perché è diverso dal backup che già esiste. L'archivio da 4,4 GB prodotto il 2026-09-07 e conservato sulla postazione Windows è una copia di `/home` fatta con `tar`, cioè dei soli dati dell'utente, ed è servito come presidio contro l'errore umano nel partizionamento. Non contiene il sistema, i pacchetti installati, la configurazione della catena audio a bassa latenza, i prefix Wine ricostruiti né le licenze attivate. Un backup di macchina intera ha uno scopo diverso: rendere ripetibile in poche ore il risultato di una ricostruzione che, come questa sessione dimostra, costa più di un giorno.

Condizione di sblocco. Che le fasi da 6 a 9 siano compiute e verificate, cioè catena audio, Wine con l'architettura `i386` dichiarata, programmi reinstallati, licenza Akabak riattivata e corredo installato. Un backup preso prima congelerebbe uno stato intermedio che nessuno vuole ripristinare.

Criterio di completamento. Il backup esiste, il suo supporto di destinazione è dichiarato, e ne è stato provato il ripristino almeno in forma parziale, perché un backup mai riletto è una speranza e non una copia. Va dichiarato anche dove risiede, dato che la regola imparata da PA-009 vale anche qui: un disco rimovibile non è il posto dove tenere l'unica copia di qualcosa.

Da definire, e non va inventato adesso. Quale prodotto Veeam si usa su Linux, se l'agente gratuito per Linux basta allo scopo, quale sia la destinazione e con quale frequenza. Sono decisioni che si prendono quando la voce si sblocca, e la loro assenza qui è voluta.

## PA-001 - Cancellare la copia del corredo software su SSD esterno

Data di apertura: 2026-09-04. **Compiuta il 2026-09-07.** Stato: chiusa.

L'esito, con la distinzione fra ciò che è accertato e ciò che non lo è. La cartella `J:\Progetto stanza (software)` **non esiste più sul disco**, verificato con il disco collegato. Le due copie restanti sono intatte: quella sul Desktop della postazione conta 650 file per 2,3 GB, e quella sulla macchina Ubuntu Studio conta 281 file per 728 MB con le impronte verificate. Nessun dato è andato perduto.

Non è invece accertato il momento né il modo della cancellazione, e va detto invece di ricostruirlo. Il comando lanciato dall'utente ha risposto che il percorso non esisteva, e nello stesso momento lo strumento riportava il disco come non collegato: le due cose sono compatibili sia con una cartella già rimossa in precedenza sia con un disco assente al momento del comando. Alle 14 dello stesso giorno la cartella era presente, perché il confronto delle impronte ne ha letto tutti e 650 i file. Fra quel momento e la verifica successiva è scomparsa. Poiché l'obiettivo della voce era che quella copia non ci fosse più e le altre due sì, la voce è compiuta a prescindere da quale delle due spiegazioni sia quella giusta.

Che cosa va fatto. Cancellare la cartella `J:\Progetto stanza (software)` dall'SSD esterno, una volta che il corredo utile è stato trasferito sulla macchina Ubuntu Studio e la sua integrità è stata verificata. È l'utente a chiedere questo promemoria, e la ragione è che quella copia è ridondante rispetto a quella sul Desktop della postazione Windows.

Le tre condizioni di sblocco, e il loro stato al 2026-09-07.

La prima, il disco collegato e visibile, è **soddisfatta**. Il 2026-09-04 `J:` non risultava fra le unità montate; il 2026-09-07 è stato collegato ed è visibile.

La seconda, la corrispondenza fra le due copie verificata per impronte, è **soddisfatta**. Il confronto ha dato 650 file su ciascuna copia, gli stessi nomi, le stesse dimensioni, 2.380.021.546 byte in totale su entrambe, e le impronte SHA-256 di tutti e 650 i file coincidenti, senza alcun file presente su una sola delle due. La dichiarazione dell'utente che si trattasse di una copia uno a uno è quindi confermata come fatto.

La terza, il trasferimento del corredo verso la macchina Ubuntu Studio completato con le impronte verificate secondo `docs/TRANSFER-MANIFEST.md`, è **soddisfatta il 2026-09-07**. Il trasferimento è stato eseguito e verificato: 8 file del manifest e 6 voci del corredo per 273 file, tutte le impronte coincidenti, per 728 MB sotto `~/electroacoustics` con un collegamento sulla scrivania della macchina. Il dettaglio, compresi i due difetti dello strumento trovati durante l'operazione, è in MS-038.

**Le tre condizioni sono quindi tutte soddisfatte e la cancellazione è autorizzata.** Resta un'azione dell'utente e non dell'agente, perché cancellare 2,3 GB da un disco esterno è una operazione distruttiva su materiale personale: il comando è in fondo a questa voce.

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

Data di apertura: 2026-09-04. Stato: **aperta**.

Che cosa va fatto. Accertare dal sito del produttore se la copia di Ramsete 27b presente nel corredo sia una versione dimostrativa liberamente distribuibile oppure una copia completa che richiede licenza.

Perché conta. È la condizione che decide se Ramsete entra nel piano di installazione, e con essa se serve un prefix Wine a 32 bit e la dichiarazione dell'architettura `i386` sul sistema. Il quadro è in `docs/10-ambiente/wine-corredo-progetto-stanza.md` e l'emendamento condizionato alla decisione sui prefix è ADR-009.

Il criterio di completamento. Una risposta documentata con la fonte, e la conseguente installazione oppure l'esclusione dichiarata.

Nota di priorità. Bassa. Il ruolo di Ramsete nel workflow sarebbe l'acustica architettonica, che è già coperta da Akabak, licenziato e funzionante. È un supplemento facoltativo e non un tassello mancante, quindi non blocca nulla.

## PA-003 - Propagare al template le quattro correzioni trovate

Data di apertura: 2026-09-04. Stato: **aperta**.

Che cosa va fatto. Portare in `template-claude-developing` le quattro correzioni individuate lavorando su questo progetto, elencate in `.claude/context/current-work.md` e diagnosticate in MS-004 e MS-014 del registro dei microstep.

Perché è differita. Sono modifiche a un altro repository, e la decisione se farle è dell'utente. Finché non sono propagate, ogni progetto nuovo istanziato dal template eredita i quattro difetti.

Il criterio di completamento. Le quattro correzioni sono nel template e le due divergenze annotate nel `.gitignore` e in `.claude/context/STACK.md` di questo progetto possono essere riscritte come allineamento invece che come divergenza.

## PA-004 - Ispezionare il disco G: e il materiale EASE Focus 3.1.10 del workshop K-array

Data di apertura: 2026-09-07. Stato: **aperta, bloccata**.

Che cosa va fatto. Collegare il disco `G:` e ispezionare il percorso `G:\LIBRARY\LOUDSPEAKERS & ELECTROACOUSTIC\K-ARRAY WORKSHOP\EASE Focus (k-array)`, per stabilire che cosa contenga, se vada trasferito sulla macchina e se contenga materiale non presente altrove.

Da dove viene. In entrambe le copie del corredo, sul Desktop e su `J:`, esiste un collegamento chiamato `EASE_Focus_v3.1.10 (k-array) - collegamento.lnk` al posto della cartella. La lettura del collegamento ha rivelato il percorso di destinazione, che sta su un disco `G:` mai menzionato prima in nessun documento di questo progetto. Il disco non risultava fra le unità montate al momento della verifica, quindi il contenuto non è stato ispezionato.

**Avvertenza sulla lettera, aggiunta il 2026-09-08.** La lettera `G:` non identifica quel disco e non va usata come se lo facesse. Il 2026-09-08 è stata assegnata a una chiavetta Kingston DataTraveler da 57,7 GB collegata per preparare il supporto di installazione, che con il materiale del workshop non ha nulla a che vedere: Windows assegna la prima lettera libera, quindi la stessa lettera indica dispositivi diversi in momenti diversi, e lo stesso dispositivo può presentarsi con lettere diverse. Ne segue che il criterio di riconoscimento del disco cercato è il **contenuto**, cioè la presenza della cartella `LIBRARY` con il percorso completo indicato sopra, e non la lettera. Vale anche per lo strumento di controllo: trovare quel percorso su una lettera è una conferma, non trovarlo significa soltanto che quel dispositivo non è collegato adesso, e la lettera occupata da qualcos'altro non è un indizio di nulla.

Che cosa si sa e che cosa non si sa. Si sa dove punta il collegamento, e si sa dal documento sorgente che il pacchetto della 3.1.10 comprendeva l'installer InstallShield, i due servizi di database AFMG, una cartella di dati, una cartella di configurazione predefinita e una cartella di esempi ed esercitazioni con un progetto di workshop e due GLL, cioè `Concert_v10.gll` e `KS5_v4.gll`. Non si sa se il contenuto su `G:` corrisponda a quella descrizione, né se contenga altro.

Perché la priorità è bassa. La versione da installare è la 3.1.260, per le ragioni discusse in `docs/30-modellazione-e-simulazione.md`: la 3.1.10 e la 3.0.18 sono superate, i file GLL sono retrocompatibili, e tre versioni dello stesso programma in tre prefix sono manutenzione senza ritorno. Il materiale del workshop ha però un valore residuo che vale nominare, cioè i progetti di esempio e i due GLL, che sono materiale didattico e non installazione.

Il criterio di completamento. Un inventario del percorso su `G:`, la decisione se trasferire qualcosa e, se sì, il suo ingresso nel manifest di trasferimento.

Nota metodologica. Questa voce nasce da una inferenza sbagliata corretta: si era concluso che il contenuto della 3.1.10 vivesse sul solo SSD, mentre il collegamento è identico su entrambe le copie e punta a un terzo luogo. La lezione operativa è che un collegamento va letto, non interpretato dal nome: due minuti di lettura del file hanno sostituito una supposizione con un percorso esatto.

## PA-005 - Completare le tre voci privilegiate della fase 0

Data di apertura: 2026-09-07. Stato: **aperta, due voci su tre compiute, e la terza è irrilevante**.

Che cosa va fatto. Tre controlli della fase 0 che l'accesso via chiave non permette di eseguire, perché `sudo` sulla macchina chiede la password e perché uno dei tre è un controllo in interfaccia grafica.

Il primo, lo stato di salute dell'SSD, è **compiuto il 2026-09-07 con esito positivo**. Il giudizio è `PASSED`, l'usura al 9 per cento, la riserva di blocchi al 100, gli errori di integrità zero, e il valore coincide con il 91 per cento di vita residua misurato nel 2025. Il disco non va sostituito, quindi la scelta resta fra installazione e aggiornamento. Il pacchetto `smartmontools` era già installato, quindi l'avvertenza su una possibile installazione da rete non serviva. Il dettaglio, con la lettura dei due numeri che sembrano allarmanti e non lo sono, è in `docs/10-ambiente/fotografia-macchina-2026-09-07.md` e in MS-033.

Il secondo è la verifica del Machine Identifier di Akabak, ed è **compiuto il 2026-09-07**. Il valore letto nella finestra del release code coincide con quello nella scheda riservata sotto `_notes/`, il release code inserito coincide anch'esso, e il programma dichiara la licenza valida. Il dettaglio, con i tre fatti collaterali che la finestra ha portato in dote, è in MS-052 e in [90-riferimenti/licenze-e-registrazioni.md](90-riferimenti/licenze-e-registrazioni.md).

Il terzo è l'esito reale di `sudo apt update`. Le prove HTTP lo rendono prevedibile, perché archivio, mirror e security rispondono 200, ma prevedibile non è verificato. Va detto però che ADR-013 lo ha reso **irrilevante**: su un sistema che verrà azzerato l'esito di `apt update` non informa nessuna decisione, e la voce resta elencata solo per non dichiarare compiuto ciò che non lo è.

Il criterio di completamento. I due esiti che contano sono registrati e la fotografia della fase 0 è aggiornata di conseguenza; la voce si chiude quando la macchina viene azzerata, perché a quel punto il terzo controllo non ha più oggetto.

## PA-006 - Riconfermare o rivedere la scelta fra installazione pulita e aggiornamento in posto

Data di apertura: 2026-09-07. **Chiusa il 2026-09-07.** Esito: l'utente ha riconfermato l'installazione pulita di Ubuntu Studio 26.04 LTS sulla base corretta, cioè su tre motivi invece di quattro con l'ambiente pulito come dominante, e ha scelto di eseguire il lavoro privilegiato con comandi preparati e lanciati a mano, senza regole `sudoers`. La decisione è registrata come ADR-013, che supera lo stato di attesa di ADR-011.

La conseguenza operativa che ne discende, e che non era ovvia: la pulizia dell'ambiente Wine **non si esegue**, perché pulire un sistema che verrà azzerato è lavoro che si butta. L'ambiente pulito si ottiene per costruzione dalla reinstallazione. Per la stessa ragione non si applicano i 134 pacchetti pendenti e non si esegue il riavvio richiesto.

Il testo che segue è quello originale della voce, conservato perché documenta i termini su cui la decisione è stata presa.

Che cosa va fatto. Riconfermare ADR-006, cioè l'installazione pulita della 26.04 LTS, oppure scegliere l'aggiornamento in posto, sapendo che uno dei quattro motivi originali è venuto meno.

Perché è aperta. La decisione era stata confermata dall'utente il 2026-09-04 sulla base di quattro motivi, e la verifica del 2026-09-07 ne ha smentito il primo: non ci sono due aggiornamenti in cascata attraverso archivi storici da evitare, perché `do-release-upgrade` offre direttamente la 26.04.1 LTS. Tenere una decisione confermata quando una delle sue gambe è caduta significherebbe farla passare per più solida di quanto sia. La revisione è registrata come ADR-011.

Che cosa cambia fra le due strade, in concreto. L'aggiornamento in posto è oggi: applicare 134 pacchetti pendenti, riavviare, disattivare i due repository WineHQ, ed eseguire un solo `do-release-upgrade`. L'installazione pulita è la procedura in undici fasi, e il suo guadagno è un ambiente Wine ricostruito senza la sedimentazione documentata, più la rimozione dell'architettura `i386` e delle sorgenti residue.

Il criterio di completamento. Una scelta dichiarata, e ADR-006 riconfermata oppure superata da una voce nuova.

## PA-007 - Cancellare la copia del corredo sul Desktop della postazione

Data di apertura: 2026-09-07. **Compiuta il 2026-09-08.** Stato: chiusa.

L'esito. La cartella `C:\Users\Utente\Desktop\Progetto stanza (software)`, 650 file per 2,3 GB, è stata cancellata dall'utente e non esiste più, verificato. Nell'ordine prescritto: prima la riverifica delle impronte sulla macchina, che ha dato 8 file del manifest e 273 file del corredo tutti coincidenti, e subito dopo la cancellazione. Le voci utili del corredo restano in due copie indipendenti, quella sulla macchina e quella dentro l'archivio di `/home`; delle otto voci scartate dal censimento si è perduta l'unica copia, come previsto e voluto, perché per ciascuna esiste una sostituzione nativa o gratuita già disponibile.

Il testo che segue documenta i termini su cui la voce era stata sbloccata, ed è **superato dall'esecuzione**.

Detto senza giri di parole, perché la domanda è stata posta due volte: **la cartella si può cancellare, oggi, e l'unica cosa che si perde è quella che il censimento ha deciso di non tenere.** Non c'è nessuna condizione residua da attendere.

La condizione che c'era è la copia di sicurezza di `/home` fuori dalla macchina, ed è soddisfatta: archivio `tar` di 4,4 GB, verificato con 13.498 file nell'archivio contro 13.498 sulla macchina e i permessi conservati. Si veda MS-049. L'archivio è stato spostato dall'utente da `E:\_backup-ubuntu-studio\` a `C:\Users\Utente\Desktop\_backup-ubuntu-studio\`, con dimensione identica al byte, quindi la verifica di MS-049 vale ancora per quel file; lo strumento di controllo cerca l'archivio per nome in entrambe le posizioni proprio perché un file si sposta e un controllo che inchioda una cartella dichiara assente ciò che è soltanto altrove.

Va corretto in meglio il ragionamento con cui la voce era stata aperta. Avevo scritto che cancellare il Desktop di Windows avrebbe portato le voci utili a una copia sola: non era vero, perché sulla macchina ne esistono due indipendenti, cioè l'albero organizzato sotto `~/electroacoustics` e il materiale grezzo già presente sulla scrivania della macchina, scoperto in MS-048. La ragione valida che resta è diversa e più precisa: quelle due copie vivono sulla stessa partizione dello stesso disco, quindi rispetto al rischio che il backup deve coprire non sono due copie ma una. Il backup su un supporto diverso è ciò che le rende due, e adesso c'è.

Che cosa va fatto. Cancellare `C:\Users\Utente\Desktop\Progetto stanza (software)`, 650 file per 2,3 GB.

Il testo che segue, in questi due paragrafi, è quello con cui la voce era stata aperta ed è **superato**: si conserva perché documenta la condizione che allora mancava e che oggi è soddisfatta, non perché descriva lo stato attuale.

Perché non ora, ed è la risposta a una domanda diretta dell'utente. Il ragionamento "se abbiamo tutto quello che serve possiamo cancellare anche il Desktop" è corretto sul contenuto e sbagliato sul momento. Oggi le voci utili del corredo esistono in due copie, una sul Desktop e una sulla macchina. Cancellare il Desktop le porta a **una copia sola**, e quella copia vive su una macchina che sta per subire una reinstallazione con riformattazione di una partizione. Ridurre a una copia proprio prima di una operazione che tocca le partizioni è il momento peggiore possibile.

La condizione di sblocco è quindi una sola: **la copia di sicurezza di `/home` fuori dalla macchina**, cioè la fase 1.3 della procedura di installazione pulita. Fatta quella, le copie tornano a essere due, una sulla macchina e una nel backup, e il Desktop diventa la terza: a quel punto è ridondante e può andare.

Che cosa si perde davvero, distinto con precisione. Delle sei voci trasferite non si perde nulla, perché sono sulla macchina con le impronte verificate. Delle otto voci scartate dal censimento si perde l'unica copia esistente, perché non sono state trasferite di proposito. Il censimento stabilisce che nessuna serve al progetto e che per ciascuna esiste una sostituzione nativa o gratuita già disponibile, quindi la perdita è voluta e non accidentale; ma va detta, perché è irreversibile.

Il criterio di completamento. La cartella non esiste più sul Desktop, e sulla macchina il corredo è presente con le impronte verificate più una copia di sicurezza di `/home` fuori dalla macchina.

Il comando. La condizione della fase 1.3 è soddisfatta, quindi si può lanciare.

```powershell
bash tools/transfer-to-studio.sh --impronte
Remove-Item -LiteralPath "C:\Users\Utente\Desktop\Progetto stanza (software)" -Recurse -Force
```

Il primo comando non è decorativo: riverifica che il materiale sulla macchina corrisponda ancora, e va lanciato subito prima della cancellazione e non ore prima.

## PA-008 - Recuperare 1,2 GiB di cartelle di servizio su J:

Data di apertura: 2026-09-07. Stato: **aperta, eseguibile adesso**.

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

Nota su ciò che **non** va cancellato, perché è la parte contro-intuitiva. I due archivi di backup da 25,8 e 19,4 GiB restano: il confronto dei loro indici, fatto il 2026-09-07, dimostra che nessuno dei due contiene l'altro, e cancellare il più vecchio costerebbe 145.478 versioni di file che non esistono altrove in forma archiviata. Il dettaglio è in `docs/90-riferimenti/pulizia-ssd-esterno.md`.

## PA-009 - Leggere lo SMART dell'SSD esterno

Data di apertura: 2026-09-07. **Compiuta il 2026-09-08.** Stato: chiusa.

L'esito, e risponde alla domanda che la voce poneva. Il **supporto è sano**: usura a zero, riserva disponibile al 100 per cento su una soglia di 10, zero errori di integrità dei dati, zero voci nel registro errori, giudizio complessivo 100 per cento dopo 2795 ore. Il disco non va sostituito e può continuare a ospitare materiale, con l'avvertenza generale che un disco rimovibile non è il posto dove tenere l'unica copia di qualcosa.

Delle due cause possibili cade quindi la seconda, cioè il difetto del supporto, e resta la prima, cioè la rimozione senza espulsione sicura, coerente con i **122 spegnimenti non protetti su 742 cicli** di alimentazione. Su quel numero va applicato un correttivo prima di usarlo come prova, perché su un disco USB il contatore si incrementa ogni volta che il ponte non inoltra al controller la notifica di spegnimento, cosa che molti ponti non fanno mai: una parte dei 122 è fisiologica dell'involucro. Le cinque cartelle `FOUND` non hanno invece spiegazioni fisiologiche, e restano la prova che il volume è stato staccato con scritture in sospeso.

La regola operativa che ne discende è una sola: espellere il volume prima di staccarlo, sempre. La misura completa, il confronto con il disco di sistema della postazione e l'ostacolo dei privilegi su Windows sono in [90-riferimenti/pulizia-ssd-esterno.md](90-riferimenti/pulizia-ssd-esterno.md) e in MS-058.

Il testo che segue è quello originale della voce, conservato perché documenta i termini su cui la verifica è stata impostata.

Che cosa va fatto. Leggere lo stato di salute del disco `J:` con CrystalDiskInfo da Windows, oppure con `smartctl` collegandolo alla macchina Ubuntu Studio.

Perché conta. Sul volume ci sono cinque cartelle `FOUND`, dal 30 giugno al 3 settembre, cioè cinque riparazioni del filesystem in poco più di due mesi. Le cause possibili sono due e portano a rimedi opposti: la rimozione senza espulsione sicura, che si corregge con una abitudine, oppure un difetto del supporto, che si corregge sostituendolo. Solo lo SMART distingue le due.

L'elemento di contesto che rende la prima ipotesi meno rassicurante: il disco interno della macchina ha 24 spegnimenti non puliti su 135 accensioni. Due dischi con sintomi diversi che puntano nella stessa direzione sono un indizio più forte di due sintomi isolati.

Gli indicatori da guardare sono gli stessi usati per il disco interno: percentuale di usura, riserva di blocchi disponibili e conteggio degli errori di integrità dei dati.

Il criterio di completamento. Un esito registrato, e la conseguente decisione se quel disco possa continuare a ospitare backup oppure vada sostituito.

Nota di priorità. Media, e più alta di quanto sembri: su quel disco vivono 371 GiB di materiale personale e due archivi di backup che il confronto ha dimostrato non ridondanti. Se il supporto è malato, quello è il posto sbagliato dove tenerli.

## Azioni compiute

Nessuna, per ora. Le voci compiute si spostano qui con la data e l'esito, e non si cancellano.
