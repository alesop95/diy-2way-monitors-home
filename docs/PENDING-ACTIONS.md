# Azioni differite

> Registro delle azioni che non si possono compiere adesso perché dipendono da una condizione esterna, con la condizione di sblocco di ciascuna e il criterio con cui si stabilisce che sono compiute. Serve a un fine preciso: un promemoria che vive solo in una conversazione è perduto, mentre una voce qui sopravvive alla sessione, al riavvio e a un clone del repository.
>
> Lo strumento `tools/check-pending-actions.py` legge le condizioni verificabili in automatico e dice quali azioni sono diventate eseguibili. Conviene lanciarlo a inizio sessione.

## Come si legge una voce

Ogni azione ha un identificativo nella forma `PA-NNN`, una data di apertura, la descrizione di che cosa va fatto, la condizione che ne blocca l'esecuzione, il criterio di completamento e lo stato. Una voce non si cancella quando è compiuta: si marca come compiuta con la data, così che il registro resti la storia di ciò che è stato deciso e non solo di ciò che resta da fare.

## PA-001 - Cancellare la copia del corredo software su SSD esterno

Data di apertura: 2026-09-04. Ultimo aggiornamento: 2026-09-07. Stato: **sbloccata, in attesa dell'esecuzione da parte dell'utente**.

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

Che cosa si sa e che cosa non si sa. Si sa dove punta il collegamento, e si sa dal documento sorgente che il pacchetto della 3.1.10 comprendeva l'installer InstallShield, i due servizi di database AFMG, una cartella di dati, una cartella di configurazione predefinita e una cartella di esempi ed esercitazioni con un progetto di workshop e due GLL, cioè `Concert_v10.gll` e `KS5_v4.gll`. Non si sa se il contenuto su `G:` corrisponda a quella descrizione, né se contenga altro.

Perché la priorità è bassa. La versione da installare è la 3.1.260, per le ragioni discusse in `docs/30-modellazione-e-simulazione.md`: la 3.1.10 e la 3.0.18 sono superate, i file GLL sono retrocompatibili, e tre versioni dello stesso programma in tre prefix sono manutenzione senza ritorno. Il materiale del workshop ha però un valore residuo che vale nominare, cioè i progetti di esempio e i due GLL, che sono materiale didattico e non installazione.

Il criterio di completamento. Un inventario del percorso su `G:`, la decisione se trasferire qualcosa e, se sì, il suo ingresso nel manifest di trasferimento.

Nota metodologica. Questa voce nasce da una inferenza sbagliata corretta: si era concluso che il contenuto della 3.1.10 vivesse sul solo SSD, mentre il collegamento è identico su entrambe le copie e punta a un terzo luogo. La lezione operativa è che un collegamento va letto, non interpretato dal nome: due minuti di lettura del file hanno sostituito una supposizione con un percorso esatto.

## PA-005 - Completare le tre voci privilegiate della fase 0

Data di apertura: 2026-09-07. Stato: **aperta, una voce su tre compiuta**.

Che cosa va fatto. Tre controlli della fase 0 che l'accesso via chiave non permette di eseguire, perché `sudo` sulla macchina chiede la password e perché uno dei tre è un controllo in interfaccia grafica.

Il primo, lo stato di salute dell'SSD, è **compiuto il 2026-09-07 con esito positivo**. Il giudizio è `PASSED`, l'usura al 9 per cento, la riserva di blocchi al 100, gli errori di integrità zero, e il valore coincide con il 91 per cento di vita residua misurato nel 2025. Il disco non va sostituito, quindi la scelta resta fra installazione e aggiornamento. Il pacchetto `smartmontools` era già installato, quindi l'avvertenza su una possibile installazione da rete non serviva. Il dettaglio, con la lettura dei due numeri che sembrano allarmanti e non lo sono, è in `docs/10-ambiente/fotografia-macchina-2026-09-07.md` e in MS-033.

Il secondo è l'esito reale di `sudo apt update`. Le prove HTTP lo rendono prevedibile, perché archivio, mirror e security rispondono 200, ma prevedibile non è verificato.

Il terzo è la verifica del Machine Identifier di Akabak, che si legge dal menu di aiuto del programma alla voce del release code, con la cattura di uno screenshot della finestra. Va fatto prima di azzerare la macchina, perché dopo non sarebbe più confrontabile, e il valore atteso è quello nella scheda riservata sotto `_notes/`.

Il criterio di completamento. I tre esiti registrati, e la fotografia della fase 0 aggiornata di conseguenza.

## PA-006 - Riconfermare o rivedere la scelta fra installazione pulita e aggiornamento in posto

Data di apertura: 2026-09-07. **Chiusa il 2026-09-07.** Esito: l'utente ha riconfermato l'installazione pulita di Ubuntu Studio 26.04 LTS sulla base corretta, cioè su tre motivi invece di quattro con l'ambiente pulito come dominante, e ha scelto di eseguire il lavoro privilegiato con comandi preparati e lanciati a mano, senza regole `sudoers`. La decisione è registrata come ADR-013, che supera lo stato di attesa di ADR-011.

La conseguenza operativa che ne discende, e che non era ovvia: la pulizia dell'ambiente Wine **non si esegue**, perché pulire un sistema che verrà azzerato è lavoro che si butta. L'ambiente pulito si ottiene per costruzione dalla reinstallazione. Per la stessa ragione non si applicano i 134 pacchetti pendenti e non si esegue il riavvio richiesto.

Il testo che segue è quello originale della voce, conservato perché documenta i termini su cui la decisione è stata presa.

Che cosa va fatto. Riconfermare ADR-006, cioè l'installazione pulita della 26.04 LTS, oppure scegliere l'aggiornamento in posto, sapendo che uno dei quattro motivi originali è venuto meno.

Perché è aperta. La decisione era stata confermata dall'utente il 2026-09-04 sulla base di quattro motivi, e la verifica del 2026-09-07 ne ha smentito il primo: non ci sono due aggiornamenti in cascata attraverso archivi storici da evitare, perché `do-release-upgrade` offre direttamente la 26.04.1 LTS. Tenere una decisione confermata quando una delle sue gambe è caduta significherebbe farla passare per più solida di quanto sia. La revisione è registrata come ADR-011.

Che cosa cambia fra le due strade, in concreto. L'aggiornamento in posto è oggi: applicare 134 pacchetti pendenti, riavviare, disattivare i due repository WineHQ, ed eseguire un solo `do-release-upgrade`. L'installazione pulita è la procedura in undici fasi, e il suo guadagno è un ambiente Wine ricostruito senza la sedimentazione documentata, più la rimozione dell'architettura `i386` e delle sorgenti residue.

Il criterio di completamento. Una scelta dichiarata, e ADR-006 riconfermata oppure superata da una voce nuova.

## Azioni compiute

Nessuna, per ora. Le voci compiute si spostano qui con la data e l'esito, e non si cancellano.
