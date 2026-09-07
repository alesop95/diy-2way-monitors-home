# Storico di Akabak e VACS: licenza, installazione, limiti

> Cronologia verificata della messa in opera di Akabak 3 e VACS sulla macchina Ubuntu Studio, ricostruita dalla corrispondenza con l'autore del software. Colma il punto esatto in cui il documento sorgente si interrompeva, e porta alla luce un limite tecnico dell'integrazione fra i due programmi su Linux che nel sorgente non compare affatto e che condiziona il workflow della fase 5.

## Perché questo storico esiste

Il documento sorgente raccontava l'inizio di questa vicenda e poi si fermava. Riportava la domanda inviata il 13 agosto 2025 alle 10:35, riportava per intero la prima risposta dell'autore con i cinque passi per ottenere il codice, e subito dopo, al paragrafo successivo, aveva un segnaposto: una sequenza di lettere ripetute, cioè il promemoria di una sezione da scrivere e mai scritta.

Il seguito, però, è la parte che conta. È lì che l'installazione fallisce, che l'autore rivela un limite del suo software su Linux, che l'installazione riesce, che il codice arriva e che viene verificato funzionante. Ricostruirlo dalla corrispondenza non è archeologia: tre dei fatti emersi cambiano decisioni operative documentate altrove in questo albero.

## La cronologia

Le date e gli orari sono quelli della corrispondenza. I nomi delle versioni e degli eseguibili sono trascritti come compaiono.

**13 agosto 2025, 10:35.** Richiesta inviata all'autore: si chiede se sia possibile usare una licenza per uso non commerciale su una macchina Ubuntu Studio 25 dopo la registrazione, e se ci sia qualcosa da acquistare.

**13 agosto 2025, 11:05.** Risposta dell'autore, Joerg Panzer di R&D-Team. Registra l'utente per una *student-license* e indica cinque passi: scaricare la versione professionale di AKABAK e di VACS dai due link forniti, installare ed eseguire entrambi, aprire in AKABAK il menu di aiuto alla voce del release code, inviare per posta elettronica il Machine Identifier indicato, e ricevere in cambio un Release Code valido per quel computer.

**13 agosto 2025, 11:11.** Si risponde che la macchina non è ancora a disposizione e che non è stata ancora configurata. Si pone inoltre la domanda che si rivelerà decisiva per tutta l'amministrazione successiva della macchina: la licenza è legata strettamente a quell'hardware, e come funziona esattamente. Si precisa per correttezza di non essere più uno studente ma un IT manager, con un passato nel settore dell'elettroacustica per impianti di diffusione sonora.

**13 agosto 2025, 17:00.** Si comunica di aver scaricato `AKABAK_Pro_v324b126.exe`, un installer da 35 MB, e di averlo eseguito con Wine sulla macchina Ubuntu Studio. Si comunica il Machine Identifier ottenuto. E si segnala il primo problema reale: VACS non parte, con l'ipotesi che dipenda dall'aver usato la versione a 64 bit invece di quella a 32.

**14 agosto 2025, 09:12.** Sollecito.

**14 agosto 2025, 19:19.** Risposta dell'autore, ed è la parte tecnicamente più densa di tutto lo scambio. Dichiara di non avere molta esperienza su Linux, e aggiunge l'informazione che segue, testualmente: poiché Linux non supporta le pipeline COM, il trasferimento dei dati fra AKABAK e VACS è possibile soltanto attraverso gli appunti di sistema, e rimanda alle preferenze e alla guida di AKABAK.

**14 agosto 2025, 22:26.** Si comunica che alla fine entrambi i programmi sono stati installati con successo su Ubuntu, e si richiede il Release Code indicando di nuovo il Machine Identifier.

**15 agosto 2025, 12:18.** L'autore invia il Release Code permanente, valido per quel Machine Identifier, con la procedura di inserimento: accedere come amministratore, aprire AKABAK, andare al menu di aiuto alla voce del release code, inserire i numeri e confermare. Nella stessa risposta ripete i link di download e dichiara le versioni correnti: **AKABAK 3.2.4 b126** e **VACS 2.1.3 b33**.

**15 agosto 2025, 13:04.** Si comunica di essere fuori sede dall'inizio di settembre e che il codice verrà provato al ritorno.

**3 settembre 2025, 12:58.** Si comunica l'esito: il codice ha funzionato per AKABAK, eseguito su Ubuntu Studio con Wine. VACS è stato avviato e non ha richiesto un secondo codice.

## I fatti che ne discendono, e cosa cambiano

Sette fatti, con la conseguenza operativa di ciascuno.

**Akabak e VACS sono già installati, licenziati e funzionanti** sulla macchina dal 3 settembre 2025. Il documento sorgente lasciava intendere una configurazione in corso; la corrispondenza dimostra un impianto concluso e verificato. Questo cambia il punto di partenza: l'installazione pulita del sistema non è un primo impianto ma una ricostruzione di qualcosa che ha già funzionato una volta su questa stessa macchina, e questo abbassa il rischio dell'operazione perché il percorso è già stato percorso.

**La licenza è machine-based e il codice è permanente.** Il Release Code è valido per quel Machine Identifier e non ha scadenza. Ne segue che azzerare i prefix Wine, reinstallare Wine, o reinstallare interamente Ubuntu Studio non fa perdere la licenza: dal punto di vista del programma la macchina è la stessa. È la conferma, dall'autore stesso, dell'affermazione su cui poggia la raccomandazione dell'installazione pulita.

**Un solo Release Code copre entrambi i programmi.** L'autore lo dichiara esplicitamente scrivendo che il codice abilita AKABAK e VACS, e la verifica del 3 settembre lo conferma: VACS, avviato dopo l'attivazione di AKABAK, non ha chiesto nulla. Alla reinstallazione, quindi, il codice va inserito una volta sola, da AKABAK.

**L'inserimento del codice richiede privilegi di amministratore.** L'autore indica di accedere come amministratore prima di aprire AKABAK. È una istruzione pensata per Windows, dove significa eseguire il programma con elevazione; sotto Wine non esiste un vero controllo degli account utente, e il programma gira con i privilegi dell'utente Linux che lo lancia. Il punto pratico è che l'attivazione scrive nel registro del prefix, quindi va eseguita con lo stesso utente Linux che userà poi il programma, altrimenti l'attivazione finisce in un prefix diverso da quello di lavoro. Questo è il motivo per cui il prefix va sempre indicato esplicitamente e non lasciato al default.

**Le versioni corrette sono AKABAK 3.2.4 b126 e VACS 2.1.3 b33.** Coincidono con i nomi degli installer conservati, cioè `AKABAK_Pro_v324b126.exe` e `VACS_32_v213b33.exe` con la sua variante a 64 bit. È anche la conferma esterna che chiude l'incoerenza 2 del documento sorgente, dove Akabak era descritto in un punto come software a 16 bit: un programma alla versione 3.2.4 distribuito nel 2025 non lo è.

**VACS inizialmente non partiva, e l'ipotesi dei 32 bit era plausibile ma non è quella che ha risolto.** La corrispondenza registra il problema il 13 agosto e la sua soluzione il 14, senza dire quale intervento lo abbia risolto. Questo va dichiarato come lacuna e non riempito per ipotesi: non si sa se la risoluzione sia venuta dall'installazione della variante a 32 bit, da una dipendenza aggiunta con winetricks, o dalla ricreazione del prefix. È una informazione che si recupera soltanto ispezionando la macchina, e la sezione finale di questa pagina indica come.

**Il trasferimento dati fra AKABAK e VACS su Linux passa dagli appunti, non dalle pipeline COM.** È il fatto più importante dei sette, e ha una sezione propria.

## Il limite delle pipeline COM, spiegato

COM[^1] è il meccanismo con cui, su Windows, due applicazioni distinte si parlano: un programma espone oggetti e metodi, un altro li invoca, e i dati passano da un processo all'altro senza che l'utente faccia nulla. AKABAK e VACS sono pensati per lavorare in coppia, il primo come simulatore e il secondo come strumento di visualizzazione e analisi, e su Windows il primo consegna i risultati al secondo attraverso questo canale.

Wine implementa una parte di COM, ma non tutto, e in particolare l'infrastruttura che serve alla comunicazione fra processi distinti attraverso questo canale non è completa. L'autore lo constata sul suo software e indica la via alternativa: gli appunti di sistema. Si copia il dato da AKABAK e si incolla in VACS, con un passaggio manuale al posto di uno automatico. Le preferenze di AKABAK contengono l'impostazione relativa, e la guida del programma la documenta.

Questo non è un difetto di configurazione da risolvere: è una proprietà dell'ambiente, dichiarata dall'autore del software. Va quindi accettata e pianificata, non inseguita. La conseguenza sul workflow della fase 5 è concreta: il passaggio dei risultati di simulazione dal solutore allo strumento di analisi è un passo manuale, quindi va tenuto in conto nel tempo di ogni iterazione, e le iterazioni della fase 5 sono molte, perché il ciclo consiste nel modificare parametri e materiali finché la risposta non rientra nella tolleranza dichiarata.

C'è anche una conseguenza sul metodo, che vale enunciare. Un passo manuale ripetuto molte volte è un punto in cui si commettono errori silenziosi, per esempio incollare in VACS il risultato di una simulazione precedente credendo che sia quella appena eseguita. Conviene quindi adottare una disciplina di denominazione dei risultati e verificare, a ogni incollaggio, che il dato sia quello atteso.

Va infine osservato che questo limite è un argomento in più a favore di Wine e non contro, per una ragione che a prima vista sfugge: se il progetto girasse in una macchina virtuale Windows, le pipeline COM funzionerebbero, ma si pagherebbero le latenze della catena audio virtualizzata e la licenza andrebbe richiesta di nuovo per l'identificativo virtuale. Il confronto corretto è fra un passaggio manuale di copia e incolla nella fase di simulazione, e una penalizzazione permanente della fase di misura più la perdita della licenza. Il primo costo è chiaramente il minore, e questa è la ragione per cui il limite non riapre la decisione registrata come ADR-003.

## Rapporto con il documento sorgente

La tabella mette in chiaro dove il sorgente era completo, dove era incompleto e dove era sbagliato, così che si veda che cosa la corrispondenza ha effettivamente aggiunto.

| Fatto | Documento sorgente | Corrispondenza |
|---|---|---|
| Richiesta del 13 agosto e prima risposta | presente e integrale | conferma |
| Natura della licenza, machine-based | affermato correttamente, senza fonte | confermato dall'autore |
| Machine Identifier della macchina | non riportato | riportato |
| Release Code | non riportato | riportato, permanente |
| Un solo codice per entrambi i programmi | non menzionato | dichiarato e verificato |
| Versioni corrette dei due programmi | implicite nei nomi degli installer | dichiarate dall'autore |
| Akabak a 16 bit | affermato, ed è falso | smentito dal numero di versione |
| Fallimento iniziale di VACS | non menzionato | riportato, con esito ma senza causa |
| Limite delle pipeline COM su Linux | assente del tutto | dichiarato dall'autore |
| Esito finale dell'attivazione | segnaposto vuoto | verificato il 3 settembre 2025 |

## Dove stanno i dati riservati

Il Machine Identifier e il Release Code non sono in questo file e non sono in nessun file tracciato di questo repository, perché il repository è ospitato su GitHub e un codice di attivazione non va pubblicato. Vivono in due posti, entrambi fuori dal versionamento.

Il primo è il PDF della corrispondenza, che sta fra i materiali della cartella `Akabak + VACS/`, ignorata da git, ed è incluso nel manifest di trasferimento verso la macchina proprio perché serve alla riattivazione.

Il secondo è una scheda sotto `_notes/`, anch'essa ignorata, che riporta i due valori in forma direttamente utilizzabile insieme alla procedura di inserimento, così che al momento della reinstallazione non si debba rileggere un PDF di posta elettronica.

## Che cosa resta da verificare sulla macchina

Tre cose non sono deducibili dalla corrispondenza e vanno lette sulla macchina prima di azzerarla, perché dopo non sarebbero più recuperabili. Sono parte della fotografia dello stato attuale che precede l'installazione pulita.

In quale prefix Wine sono effettivamente installati AKABAK e VACS, e se condividono lo stesso prefix o ne hanno uno per ciascuno. La corrispondenza non lo dice e il documento sorgente descriveva sia l'uso del prefix di default sia la buona pratica del prefix separato.

Quale variante di VACS è installata, a 32 o a 64 bit, e con quali dipendenze nel prefix. È la risposta alla lacuna sul come il fallimento iniziale sia stato risolto.

Se il Machine Identifier attuale sia ancora quello a cui il Release Code è legato. È un controllo di dieci secondi che vale la pena fare prima di reinstallare, perché se per qualche motivo fosse cambiato, per esempio per una sostituzione di componente avvenuta nel frattempo, lo si scoprirebbe adesso e non a reinstallazione compiuta.

[^1]: *COM*, Component Object Model - infrastruttura di Windows che permette a processi distinti di esporre e invocare oggetti fra loro, usata dalle applicazioni per scambiarsi dati senza passare da file o dagli appunti; Wine la implementa solo in parte.
