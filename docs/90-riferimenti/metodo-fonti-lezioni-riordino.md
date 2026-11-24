# Come si conservano fonti, lezioni e prove

Questa procedura attua il mandato del 2026-11-20. Il progetto deve conservare sia il risultato ingegneristico sia il percorso che lo rende controllabile: dati, ipotesi, decisioni, errori, comandi, pipeline e limiti. Riordinare significa rendere reperibile quel percorso e ridurre le copie espanse; le prove di un errore restano parte della documentazione.

## Autorità documentali e metodi riuniti

Il confronto autorizzato ha riguardato soltanto le regole di gestione. Dal progetto personale del libro è ripreso il passaggio da raccolta a staging, inserimento effettivo e bibliografia con la stessa citekey. Dal progetto personale dei giochi è ripreso il collegamento fra fonte, scopo e punto d'uso e il riuso della rigenerazione protetta. Il percorso personale dei giochi disponibile in questa sessione era diverso dal nome breve indicato dall'utente: è stato individuato e letto il progetto corrispondente, senza importarne contenuti.

Dall'ambiente aziendale autorizzato è stata considerata soltanto la disciplina generica di un'unica autorità per stato, decisioni, cronaca e residui, con ricostruzioni retrospettive dichiarate. Non sono stati letti o copiati documenti operativi, dati, esempi o risultati aziendali. Nel progetto privato non entrano nomi, percorsi, casi o allegati aziendali, neppure fra gli ignorati. La tabella seguente descrive il metodo adottato qui, senza riprodurre documenti di altri progetti.

Il controllo finale ha trovato tre riferimenti identificanti già presenti da tempo nei documenti. Sono stati anonimizzati con una correzione dichiarata in MS-297. Restano nelle revisioni Git precedenti, non modificate in questa sessione: PA-042 separa questa valutazione dalla pulizia dell'albero corrente. Non si dichiara bonificato il remoto o l'intera storia.

| Domanda | Autorità nel progetto audio | Regola adottata |
|---|---|---|
| Qual è lo stato corrente? | `docs/STATO-PROGETTO.md` per il proprietario; `.claude/memory/index.md` per la ripresa | Stesse autorità tecniche collegate, nessuna cronologia duplicata negli snapshot o nel catalogo. |
| Perché si è scelto così? | `.claude/memory/decisions.md` | Decisione con motivazione, conseguenze e stato; nessun commit storico inventato. |
| Che cosa è accaduto? | `docs/OPERATIONS-LOG.md` | Microstep numerati, compresi tentativi falliti e ritiri espliciti. |
| Come si rifà? | Pagina prescrittiva sotto `docs/` | Comandi realmente eseguiti, nell'ordine; troubleshooting derivato da casi osservati. |
| Che cosa si impara? | `.claude/context/studio-didattico-master.md` | Racconto evolutivo e approfondimento sul caso locale. |
| Che cosa è riutilizzabile altrove? | `.claude/memory/lezioni-template.md` | Una lezione con identificativo, evidenza locale e campo Template nel work-log. |
| Da dove arriva un'affermazione? | `research-vault/fonti.json` e mappa degli usi | Citekey bibliografica conservata, identità della risorsa/versione e punto d'uso concreto. |

## Pedigree e identificazione delle fonti

La [mappa delle fonti](fonti-progetto.md) si genera dai [metadati curati](../../research-vault/anagrafiche-fonti-web.json) e dai collegamenti nei documenti autorati. Il [JSON completo degli usi](../../research-vault/usi-fonti-progetto.json) conserva file, riga, sezione e contesto. Non è una seconda bibliografia: quando esiste, la citekey del registro storico viene riusata. I libri della biblioteca e i testi di terzi sono esclusi da questa scansione, e restano nel loro registro canonico.

Una fonte curata ha un ID permanente, responsabile, URL canonico o impronta del file locale, versione, alias espliciti, spiegazione del ruolo, copertura della lettura e riscontri. La registrazione non significa lettura; la verifica dei metadati non significa lettura integrale; un uso documentato può essere una proposta o un limite, non una prestazione dimostrata. I prezzi sono osservazioni datate, non dati elettroacustici. Il manuale Marshall possiede un ID anche senza pubblicare la posizione originale sul disco privato.

Il normalizzatore già presente nel template elimina tracking e differenze di schema senza perdere identificativi come il numero di un articolo. Per le risorse non ancora curate, il generatore deriva un ID dall'impronta della chiave normalizzata. Aggiungere una fonte non rinumera le altre. Versioni e alias richiedono una decisione esplicita: due pagine simili non vengono fuse perché condividono un dominio. Le righe sono coordinate della ricognizione e possono spostarsi; ID e percorso sono i riferimenti durevoli.

Le fonti storiche rilevate automaticamente conservano il contesto del documento, ma sono marcate da riconciliare. Questa etichetta non nega le letture passate: evita di dichiararle controllate oggi senza risalire al microstep o alla scheda. Il pedigree approfondito parte dalle fonti effettivamente usate nella progettazione corrente. Linkwitz Lab e OpenCV hanno priorità esplicita; la lettura parziale e i limiti dell'omografia rimangono visibili.

## Sequenza ripetibile per la mappa

I comandi seguenti sono stati eseguiti su questa postazione. Non aprono rete, macchina Ubuntu, periferiche audio, biblioteca privata o altri repository.

```powershell
cd E:\diy-2way-monitors-home
python tools/test_mappa_fonti.py
python tools/mappa_fonti_progetto.py
python tools/mappa_fonti_progetto.py --check
python .claude/templates/tools/lezioni-template.py controlla --rigoroso
```

Per aggiungere o correggere una fonte si modifica `research-vault/anagrafiche-fonti-web.json`, conservando l'ID. Le note scientifiche e i claim appartengono alle schede di ricerca, non alla tabella generata. L'output usa `rigenera_sicuro.py`: una perdita di struttura viene fermata e deve essere valutata, senza forzare la sovrascrittura. Il controllo di aggiornamento e i test sono registrati anche in `tools/controlli-progetto.txt`, eseguito da chiudi.

## Pulizia con conservazione integrale delle prove

Il censimento è stato eseguito prima di cancellare alcunché. I confronti per impronta separano uguaglianza dei byte da equivalenza del ruolo: due rapporti identici possono attestare due corse differenti. I run superati e le vecchie anteprime vengono perciò compressi integralmente, con i percorsi originali, senza sostituire i file con hardlink modificabili.

Il 20 novembre sono stati archiviati 340 file di quattordici cartelle: dodici corse precedenti e due raccolte di anteprime. L'archivio è stato riaperto, l'elenco confrontato esattamente e ogni membro verificato per dimensione e SHA-256 prima della rimozione degli espansi. Lo script PowerShell ha ricontrollato archivio, originali, contenimento in build e assenza di reparse point prima di rimuovere le sole cartelle approvate dal manifesto. La ricevuta conferma che i percorsi espansi non esistono più. Le due relazioni PDF correnti hanno mantenuto le impronte precedenti.

Gli originali occupavano 236.967.020 byte; il ZIP occupa 37.323.781 byte. La riduzione lorda è 199.643.239 byte, circa 190,39 MiB, prima del piccolo costo di manifesti e ricevute. Si tratta di riordino sullo stesso disco, non di una nuova copia di sicurezza. Nessun manuale, microstep, decisione o dato sorgente è stato eliminato. Cache TeX e kit CAD restano disponibili. Due cartelle temporanee, inizialmente non leggibili nella sandbox, sono risultate vuote nella successiva lettura autorizzata; non sono state rimosse.

| Artefatto locale privato | Percorso relativo alla radice del progetto |
|---|---|
| Censimento documentale iniziale | `_notes/censimento-documenti-20261120.json` |
| Inventario completo di build con impronte | `_notes/pulizia-build-conservativa-20261120.json` |
| Archivio delle prove precedenti | `_notes/archivio-prove/20261120/prove-superate.zip` |
| Manifesto con i 340 percorsi e le impronte | `_notes/archivio-prove/20261120/manifest.json` |
| Ricevuta della rimozione degli espansi | `_notes/archivio-prove/20261120/ricevuta-riordino.json` |
| Script di creazione e verifica, senza cancellazione | `_notes/archivia-prove-20261120.py` |
| Script PowerShell di rimozione verificata | `_notes/rimuovi-espansi-20261120.ps1` |

Per ritrovare una vecchia prova si cerca il percorso originale nel manifesto e nel ZIP. I riferimenti storici nei microstep non vengono riscritti: il manifesto è la mappa della ricollocazione. Un'eventuale estrazione va fatta in una nuova cartella, evitando di sovrascrivere i risultati correnti.

Lo stato nel manifesto descrive il momento della creazione, quando gli originali espansi esistevano ancora. La ricevuta separata registra il passo successivo di rimozione. Il manifesto storico non viene riscritto per nascondere questa sequenza.

## Troubleshooting osservato

Il primo censimento con una fonte non curata terminava con `KeyError: usi`: il record generato non inizializzava l'elenco degli usi. Una regressione ha riprodotto l'errore, quindi l'inizializzazione è stata corretta. Un secondo controllo rifiuta ID duplicati prima dell'unione in dizionario, dove altrimenti una voce verrebbe persa. Le dieci prove verificano questi casi e normalizzazione, alias, stabilità, separazione degli stati e trattamento dei collegamenti nel contesto.

La prima verifica dei collegamenti ha rilevato tre rimandi relativi non validi nella mappa generata. Il testo di contesto era stato riportato da un'altra cartella mantenendo la sintassi del suo link. Ora la visualizzazione conserva l'etichetta come testo, mentre il punto d'uso resta collegato al documento originale e il JSON conserva il contesto completo. La regressione è stata prima rossa e poi verde; il controllo su 703 link locali non trova più destinazioni mancanti.

Le due cartelle temporanee di build davano accesso negato nella sandbox. Il primo comando PowerShell non aveva ErrorAction Stop e ha proseguito: la sua uscita zero non provava una lettura riuscita. La ripetizione autorizzata con errore bloccante le ha elencate senza contenuto. Non sono stati cambiati permessi o ACL. La distinzione fra esito del processo e contenuto del rapporto resta una lezione da applicare ai controlli futuri.

Il controllo rigoroso delle lezioni ha segnalato sei voci del work-log della stessa data precedenti all'adozione senza il campo Template. È stato aggiunto un campo dichiaratamente retrospettivo: non altera gli esiti né pretende che il registro esistesse al momento del lavoro. Le lezioni riconciliate appartengono al nuovo consolidamento. Le sette lezioni restano aperte fino alla ricezione nel template; aperta non significa collegamento rotto o prova fallita.

## Riprodurre il recap del progetto

Il recap per il proprietario è `docs/STATO-PROGETTO.md`, una vista collegata alle fonti canoniche. È esportato con WordCraft 0.18.1 già installato e lo stile di account esistente; le due relazioni matematiche rimangono in LaTeX. Comando eseguito su Windows dalla radice del progetto:

```powershell
cd E:\diy-2way-monitors-home
python .claude/templates/craft-apps/tools/craft-documento.py documento docs/STATO-PROGETTO.md --out docs/pdf/recap-progetto.pdf --stile config/documenti/intrawelt-tecnico.json
```

L'esportazione iniziale nella sandbox è fallita con accesso negato alla cartella temporanea di WordCraft; la ripetizione autorizzata fuori sandbox è riuscita. Non sono stati installati pacchetti o usata la rete. PdfCraft 0.21.1 legge metadati e testo; le eventuali anteprime sono temporanee e si eliminano subito dopo l'ispezione. Il manifesto `docs/pdf/manifest.json` lega i tre PDF ai sorgenti con SHA-256, pagine e controlli effettivi. I rapporti QA precedenti rimangono soltanto come storia nell'archivio privato. L'export PDF non conserva i collegamenti navigabili: è dichiarato copia di lettura, mentre per i rimandi si usa il Markdown con il catalogo.

## Politica corrente degli artefatti e pulizia ripetibile

ADR-056 distingue le consegne dagli intermedi. `docs/pdf/` contiene soltanto i tre PDF correnti e il manifesto di provenienza. Il Markdown tecnico e il TeX restano i sorgenti; `build/` è il posto di compilazioni, simulazioni e kit CAD locali. I PNG del CAD descrivono il progetto, mentre i PNG di ogni pagina PDF erano anteprime QA: non erano una necessità della consegna ed erano stati lasciati troppo a lungo. Si eliminano dopo il controllo, senza farne una seconda raccolta permanente.

Il riordino ha eliminato 81 derivati per 239.238.929 byte: anteprime, copie OCR del PDF con testo già estratto e PCM sintetici. Gli originali Marshall/EKO, gli OCR testuali e i risultati numerici restano. Tre cartelle temporanee vuote sono state rimosse, comprese le due indicate dall'utente. Le sessioni storiche e i vecchi script ad uso singolo confluiscono in `_notes/archivio-prove/sessioni-storiche.zip`; i percorsi originali e ogni impronta sono nella ricevuta unica `_notes/archivio-prove/riordino-corrente.json`, con la ricevuta precedente incorporata. Il ZIP è riletto integralmente prima di cancellare gli espansi. L'archivio delle 340 prove precedenti resta separato perché già verificato e documentato.

Comandi eseguiti dalla radice del progetto, da ripetere in questo ordine quando serve un nuovo riordino:

```powershell
.\tools\Pulisci-Artefatti.ps1
.\tools\Pulisci-Artefatti.ps1 -Applica
python tools/test_verifica_documenti.py
python tools/verifica_documenti.py
```

La modalità `-ArchiviaSessioni` serve al consolidamento storico corrente e rifiuta un ZIP omonimo esistente: non si sovrascrive la storia ad ogni pulizia. Lo strumento controlla il contenimento nella radice e rifiuta collegamenti; non cambia permessi, non tocca J, altri repository o la biblioteca. La sola scansione senza `-Applica` non scrive ricevute. Il controllo dei documenti entra nei diciannove comandi locali di chiudi e fallisce se un sorgente è cambiato senza rigenerare il PDF, anche quando quest'ultimo ha ancora la vecchia impronta corretta.

Una ripetizione con `-Applica` senza candidati o cartelle vuote non scrive nulla, nemmeno una nuova generazione della ricevuta. L'idempotenza è verificata sul file reale: due invocazioni consecutive senza lavoro lasciano invariato lo SHA-256 della ricevuta corrente. In questo modo una pulizia già conclusa non produce a sua volta una catena inutile di copie e cronache vuote.

Il completamento del medesimo consolidamento ha trovato dodici vecchi backup con suffissi non inclusi nella prima selezione e prove ad uso singolo. Sono stati aggiunti allo stesso ZIP, ricontrollando integralmente tutti i 1004 membri prima di rimuovere gli ultimi espansi; impronta precedente e impronta finale del ZIP sono nella ricevuta. Non è una seconda copia parallela dell'archivio. Il risultato finale è 335 derivati eliminati e circa 433 MiB recuperati, con cinque originali ricollocati in cartelle di fonte e sette soli file nella radice degli appunti. Sono eliminate anche le due PNG derivate dalle pagine del manuale ST-120, il cui PDF originale rimane disponibile.

In MS-305 sono stati archiviati altri sei vecchi rapporti QA rimasti nelle directory di build e la prima chiusura fallita sul trattino en della roadmap. Il medesimo ZIP arriva a 1011 membri, tutti ricalcolati e verificati, poi sono rimossi gli espansi QA e le cartelle recap/preview ormai vuote. La prima chiusura fallita resta consultabile nel ZIP al percorso originale `_notes/chiudi-autonomia-20261120.txt`; il file omonimo attivo conserva soltanto l'ultima corsa. La normalizzazione mirata `python tools/fix-dashes.py .claude/context/roadmap.md` ha sostituito il solo carattere introdotto qui, senza nuove esclusioni.

Troubleshooting di questa sessione: il primo tentativo di conteggio dei byte usava Measure-Object su dizionari e si è fermato prima delle rimozioni; sostituito con somma esplicita. I temporanei Python possono fallire nella sandbox e lasciare una cartella vuota: la ripetizione autorizzata riesce e la cartella abbandonata si rimuove dopo averla verificata. Il warning di locale di Perl su stderr non è l'esito di latexmk: si registra il codice reale del processo e si controlla il PDF. Il modulo Python WebSocket manca su Windows; questo non invalida le dieci prove del nucleo ma lascia aperta l'integrazione con il motore reale, senza inventare un collaudo o installare dipendenze non necessarie alla pulizia.
