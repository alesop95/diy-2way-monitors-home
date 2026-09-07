# Azioni differite

> Registro delle azioni che non si possono compiere adesso perché dipendono da una condizione esterna, con la condizione di sblocco di ciascuna e il criterio con cui si stabilisce che sono compiute. Serve a un fine preciso: un promemoria che vive solo in una conversazione è perduto, mentre una voce qui sopravvive alla sessione, al riavvio e a un clone del repository.
>
> Lo strumento `tools/check-pending-actions.py` legge le condizioni verificabili in automatico e dice quali azioni sono diventate eseguibili. Conviene lanciarlo a inizio sessione.

## Come si legge una voce

Ogni azione ha un identificativo nella forma `PA-NNN`, una data di apertura, la descrizione di che cosa va fatto, la condizione che ne blocca l'esecuzione, il criterio di completamento e lo stato. Una voce non si cancella quando è compiuta: si marca come compiuta con la data, così che il registro resti la storia di ciò che è stato deciso e non solo di ciò che resta da fare.

## PA-001 - Cancellare la copia del corredo software su SSD esterno

Data di apertura: 2026-09-04. Ultimo aggiornamento: 2026-09-07. Stato: **aperta, una sola condizione residua**.

Che cosa va fatto. Cancellare la cartella `J:\Progetto stanza (software)` dall'SSD esterno, una volta che il corredo utile è stato trasferito sulla macchina Ubuntu Studio e la sua integrità è stata verificata. È l'utente a chiedere questo promemoria, e la ragione è che quella copia è ridondante rispetto a quella sul Desktop della postazione Windows.

Le tre condizioni di sblocco, e il loro stato al 2026-09-07.

La prima, il disco collegato e visibile, è **soddisfatta**. Il 2026-09-04 `J:` non risultava fra le unità montate; il 2026-09-07 è stato collegato ed è visibile.

La seconda, la corrispondenza fra le due copie verificata per impronte, è **soddisfatta**. Il confronto ha dato 650 file su ciascuna copia, gli stessi nomi, le stesse dimensioni, 2.380.021.546 byte in totale su entrambe, e le impronte SHA-256 di tutti e 650 i file coincidenti, senza alcun file presente su una sola delle due. La dichiarazione dell'utente che si trattasse di una copia uno a uno è quindi confermata come fatto.

La terza, il trasferimento del corredo verso la macchina Ubuntu Studio completato con le impronte verificate secondo `docs/TRANSFER-MANIFEST.md`, è **non soddisfatta** e resta l'unica a bloccare. La ragione per cui non si salta è la più semplice possibile: non si cancella una copia prima che la copia buona sia al suo posto e verificata.

Il tranello nel metodo di verifica, che vale registrare perché avrebbe portato a una conclusione sbagliata. Il comando `du -sh` riportava dimensioni sensibilmente diverse fra le due copie, per esempio 14 MB contro 5,9 MB su LSPCad 5.25 e 36 MB contro 15 MB su LSPCad 6.32, e a prima vista sembrava una divergenza di contenuto. Non lo era: `du` misura lo spazio occupato, che dipende dalla dimensione dei cluster del filesystem e arrotonda per eccesso ogni file, e i due dischi hanno cluster di dimensione diversa. Il conteggio dei byte reali e le impronte hanno mostrato copie identiche. È la dimostrazione pratica del perché il criterio di confronto deve essere l'impronta del contenuto e non lo spazio occupato.

Una inferenza sbagliata da ritirare, registrata qui perché una versione precedente di questa voce la dava per probabile. Si era osservato che nella copia sul Desktop la versione 3.1.10 di EASE Focus era un collegamento e non una cartella, e concluso che quel contenuto esistesse presumibilmente sul solo SSD, quindi che la cancellazione dovesse essere limitata a ciò che era effettivamente duplicato. È falso: il collegamento è presente e identico su entrambe le copie. La lettura del collegamento ha però rivelato dove punta davvero, e questo ha aperto PA-004.

Il criterio di completamento. La cartella non esiste più su `J:`, e sulla macchina Ubuntu Studio il corredo utile è presente con le impronte verificate.

Nota sul perimetro. Questa azione riguarda la copia su SSD, non quella sul Desktop della postazione Windows. Quest'ultima è la copia di lavoro da cui parte il trasferimento, e la sua eventuale rimozione è una decisione separata, da prendere dopo che il materiale è sulla macchina e non insieme a questa.

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

Che cosa si sa e che cosa non si sa. Si sa dove punta il collegamento, e si sa dal documento sorgente che il pacchetto della 3.1.10 comprendeva l'installer InstallShield, i due servizi di database AFMG, una cartella di dati, una cartella di configurazione predefinita e una cartella di esempi ed esercitazioni con un progetto di workshop e due GLL, cioè `Concert_v10.gll` e `KS5_v4.gll`. Non si sa se il contenuto su `G:` corrisponda a quella descrizione, né se contenga altro.

Perché la priorità è bassa. La versione da installare è la 3.1.260, per le ragioni discusse in `docs/30-modellazione-e-simulazione.md`: la 3.1.10 e la 3.0.18 sono superate, i file GLL sono retrocompatibili, e tre versioni dello stesso programma in tre prefix sono manutenzione senza ritorno. Il materiale del workshop ha però un valore residuo che vale nominare, cioè i progetti di esempio e i due GLL, che sono materiale didattico e non installazione.

Il criterio di completamento. Un inventario del percorso su `G:`, la decisione se trasferire qualcosa e, se sì, il suo ingresso nel manifest di trasferimento.

Nota metodologica. Questa voce nasce da una inferenza sbagliata corretta: si era concluso che il contenuto della 3.1.10 vivesse sul solo SSD, mentre il collegamento è identico su entrambe le copie e punta a un terzo luogo. La lezione operativa è che un collegamento va letto, non interpretato dal nome: due minuti di lettura del file hanno sostituito una supposizione con un percorso esatto.

## Azioni compiute

Nessuna, per ora. Le voci compiute si spostano qui con la data e l'esito, e non si cancellano.
