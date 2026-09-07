# Azioni differite

> Registro delle azioni che non si possono compiere adesso perché dipendono da una condizione esterna, con la condizione di sblocco di ciascuna e il criterio con cui si stabilisce che sono compiute. Serve a un fine preciso: un promemoria che vive solo in una conversazione è perduto, mentre una voce qui sopravvive alla sessione, al riavvio e a un clone del repository.
>
> Lo strumento `tools/check-pending-actions.py` legge le condizioni verificabili in automatico e dice quali azioni sono diventate eseguibili. Conviene lanciarlo a inizio sessione.

## Come si legge una voce

Ogni azione ha un identificativo nella forma `PA-NNN`, una data di apertura, la descrizione di che cosa va fatto, la condizione che ne blocca l'esecuzione, il criterio di completamento e lo stato. Una voce non si cancella quando è compiuta: si marca come compiuta con la data, così che il registro resti la storia di ciò che è stato deciso e non solo di ciò che resta da fare.

## PA-001 - Cancellare la copia del corredo software su SSD esterno

Data di apertura: 2026-09-04. Stato: **aperta, bloccata**.

Che cosa va fatto. Cancellare la cartella `J:\Progetto stanza (software)` dall'SSD esterno, una volta che il corredo utile è stato trasferito sulla macchina Ubuntu Studio e la sua integrità è stata verificata. È l'utente a chiedere questo promemoria, e la ragione è che quella copia è ridondante rispetto a quella sul Desktop della postazione Windows.

Perché è bloccata, e da due cose distinte. La prima è che il disco non era collegato durante questa sessione: `J:` non risulta fra le unità montate, quindi non è stato possibile né verificare il contenuto né cancellarlo. La seconda, più importante, è che non si cancella una copia prima che la copia buona sia al suo posto e verificata: la condizione logica di sblocco è il completamento della fase 1 della procedura di installazione pulita, cioè il trasferimento verso la macchina con il confronto delle impronte.

Le condizioni di sblocco, tutte e tre necessarie. Il disco `J:` deve essere collegato e visibile. Il trasferimento del corredo verso la macchina Ubuntu Studio deve essere completato con le impronte verificate, secondo `docs/TRANSFER-MANIFEST.md`. E la corrispondenza fra la copia su SSD e quella sul Desktop deve essere verificata per impronte e non a occhio: l'utente la dichiara una copia uno a uno, ma quella è una affermazione e non un fatto accertato, e cancellare sulla base di una affermazione è precisamente il modo in cui si perdono i dati.

Il criterio di verifica della corrispondenza. Si confrontano gli elenchi di impronte SHA-256 delle due copie, non i nomi e non le dimensioni. Lo strumento `tools/check-pending-actions.py --confronta` lo fa quando il disco è collegato. È già noto un punto in cui le due copie differiscono, e questo è di per sé la dimostrazione che il confronto serve: nella copia sul Desktop la versione 3.1.10 di EASE Focus non è una cartella ma un collegamento, quindi quel contenuto esiste probabilmente solo sull'SSD. Se la verifica lo conferma, quel materiale va portato via dall'SSD prima della cancellazione, oppure la cancellazione va limitata a ciò che è effettivamente duplicato.

Il criterio di completamento. La cartella non esiste più su `J:`, e sulla macchina Ubuntu Studio il corredo utile è presente con le impronte verificate.

Nota sul perimetro. Questa azione riguarda la copia su SSD, non quella sul Desktop della postazione Windows. Quest'ultima è la copia di lavoro da cui parte il trasferimento, e la sua eventuale rimozione è una decisione separata, da prendere dopo che il materiale è sulla macchina e non insieme a questa.

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

## Azioni compiute

Nessuna, per ora. Le voci compiute si spostano qui con la data e l'esito, e non si cancellano.
