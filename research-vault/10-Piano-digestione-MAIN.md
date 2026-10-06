# Piano di digestione di J:/MAIN nella wiki: la decisione da prendere

> Aperto il 2026-10-06 con MS-210, dalla voce 25 della roadmap e dalla proposta di MS-209. Stato: in attesa della risposta dell'utente a ciascuna delle sette domande. Le cifre di costo sono stime, dichiarate come tali, e vanno sostituite dalla misura del primo lotto di ciascun livello.

## Perché serve una decisione

L'utente vuole che tutto ciò che di utile c'è in `J:\MAIN` entri nella wiki. La misura di MS-209 dice che cosa vuol dire. In testo ci sono 3958 documenti per 91,2 milioni di parole. I tre appunti EEASE, cioè circa 197 000 parole, sono costati circa 1,02 milioni di token, quindi circa 5 token per parola. Alla stessa profondità tutto il corpus costerebbe oltre 450 milioni di token, cioè decine di sessioni piene e settimane di quota. Leggere tutto con la stessa cura non è quindi un'opzione realistica, e va deciso che cosa leggere a quale profondità.

La proposta divide il materiale in tre livelli. Il livello 1 è la lettura profonda come per EEASE: pagine di concetto con le formule, gli errori verificati e i collegamenti, riservata al nucleo, nell'ordine di un milione di parole e di circa 5 milioni di token. Il livello 2 è una scheda di fonte per documento: che cosa contiene, a che cosa serve per la tesi, quali capitoli sono pertinenti. La scrive il modello economico leggendo solo l'indice e le prime pagine, quindi senza verifica dei conti. Con circa 2500 documenti a circa 3000 token ciascuno sono circa 7,5 milioni di token del modello economico. Il livello 3 è tutto il resto, che resta una voce della biblioteca e del vault su `J:`, ricercabile ma non letto, come è già oggi.

La conseguenza pratica: con il livello 2 la wiki sa che un documento esiste e a che cosa serve, e quando un capitolo della tesi ne ha bisogno lo si promuove al livello 1. È lo stesso principio della disclosure progressiva di `token-economy.md`.

## Le domande

D1. Struttura. Accetti la divisione in tre livelli? Le alternative sono due. La prima è fare solo il livello 1 e il livello 3, senza schede: costa meno, ma la wiki non sa che cosa c'è nel resto. La seconda è la lettura profonda di tutto, che non è fattibile per le cifre sopra. Raccomandazione: tre livelli.

D2. Il nucleo del livello 1. La proposta comprende tre categorie. La prima sono i tuoi appunti dei corsi pertinenti: EEASE, già fatto, poi Fundamentals of Acoustics, Musical Acoustics e gli appunti di elettronica analogica. La seconda sono i manuali cardine della tesi: Colloms, Borwick, Beranek e Mellow, Kleiner, Toole, Kuttruff, Dickason e, per la parte digitale, Oppenheim e Schafer, Lyons e Diniz. La terza sono i paper centrali, scelti con il criterio dello stadio per stadio del piano di ricerca. La risposta attesa: se confermi le tre categorie, e quali titoli aggiungi o togli, sapendo che ogni manuale vale da 150 000 a 400 000 parole, cioè da circa 1 a circa 2 milioni di token.

D3. I pedali. Il materiale del ramo Guitar and effects engineering lo leggiamo al livello 1 qui, oppure lo rimandiamo al progetto della pedaliera di PA-030, che avrà la sua wiki? Raccomandazione: rimandarlo. Qui resta voce di biblioteca, e i token si spendono nel progetto che li usa.

D4. Il perimetro del livello 2, cartella per cartella. Le cartelle sono sei, con i documenti in testo misurati in MS-209.

| Cartella | In testo | Proposta |
|---|---|---|
| LOUDSPEAKERS & ELECTROACOUSTIC | 576 | tutta al livello 2 |
| ANALOG (AUDIO) ELECTRONICS | 229 | tutta, tranne il ramo dei pedali se D3 lo rimanda |
| TLC, SIGNAL PROCESSING and DIGITAL FILTERS | 168 | tutta |
| MATH and CALCULUS | 104 | solo i testi che servono alle dimostrazioni della tesi |
| z_____UNIVERSITA | 2415 | solo i corsi pertinenti, da elencare |
| _ESTRATTI ARCHIVI TESI | 316 | solo la tesi magistrale e il suo materiale |

La risposta attesa è un sì o un no per ciascuna riga. Per z_____UNIVERSITA serve anche l'elenco dei corsi da includere. La proposta di partenza comprende i corsi di acustica, elettronica, segnali e controlli, ed esclude gli esami vecchi, informatica, fisica generale e tutto ciò che non è materiale di studio.

D5. I documenti personali. Nelle cartelle ci sono documenti amministrativi: contratti, pratiche di borsa di studio, documenti d'identità, certificati, ricevute. Confermi che non devono mai essere letti da un agente, a nessun livello, e che lo strumento li deve escludere con una regola esplicita, invece che caso per caso? Raccomandazione: sì, con la regola nello strumento e l'elenco dei pattern nel file locale dei termini, che non si pubblica.

D6. Ritmo e budget. Il limite della quota è su una finestra mobile, e la stessa spesa concentrata in una sola sessione la esaurisce, mentre distribuita no. La proposta è misurare prima un lotto per livello, cioè una fonte del livello 1 e 50 schede del livello 2, poi fissare il ritmo sui numeri veri: per esempio un lotto di livello 2 e una fonte di livello 1 per sessione. La risposta attesa: se approvi il lotto di misura, e se vuoi un tetto di token per sessione o preferisci decidere lotto per lotto.

D7. La forma del livello 1 per i manuali. Per gli appunti la forma è quella di EEASE, con pagine di concetto nella wiki. Per i manuali c'è anche `book-digest`, che produce una skill `libro-` caricabile su richiesta, con un capitolo per file. Raccomandazione: wiki per gli appunti, `book-digest` per i manuali cardine, perché un manuale si consulta per capitolo e non si legge per intero a ogni domanda. Tutto resta locale, per ADR-028.

## Le risposte

Date dall'utente il 2026-10-06, registrate come ADR-041 e ADR-042.

D1. Struttura a tre livelli accettata.

D2. I tre gruppi del nucleo sono confermati. Ogni lancio di lettura chiede prima il permesso dell'utente. Le fonti non lette restano note all'agente: a ogni domanda l'agente sa che oltre alla wiki esistono la biblioteca, il vault su `J:`, le schede del livello 2 e la cache convertita, e può leggerle.

D3. Il materiale sui pedali va al progetto della pedaliera, con la sua wiki. Gli strumenti del template per convertire i libri in skill restano tutti disponibili.

D4. Il perimetro proposto è accettato per ogni riga, compreso l'elenco di partenza dei corsi di z_____UNIVERSITA.

D5. I documenti personali non si leggono mai, a nessun livello, se non su richiesta espressa dell'utente, e la regola diventa generale nel template. È ADR-042 con `.claude/rules/documenti-personali.md`.

D6. Il lotto di prova è approvato, e il ritmo si decide lotto per lotto.

D7. Proposta approvata: wiki per gli appunti, `book-digest` per i manuali cardine.
