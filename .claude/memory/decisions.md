# Registro delle decisioni architetturali

> Convenzione ADR-lite, append-only. Ogni decisione non ovvia entra come voce numerata con data, stato, contesto, decisione, motivazione e conseguenze. Una decisione non si cancella e non si riscrive: quando viene superata, si aggiunge una voce nuova che dichiara di superarla e ne cita il numero. Le inferenze non confermate si marcano come da verificare e si promuovono a decisione solo quando una fonte le conferma.

## ADR-001 - Adozione del sistema di progetto portabile

Data: 2026-09-04. Stato: accettata.

Contesto: il progetto necessita di uno stato interamente recuperabile da un clone e di documentazione che resti allineata senza rilettura integrale a ogni sessione.

Decisione: adottare il sistema descritto in `.claude/PROJECT-SYSTEM.md`, con doppio livello documentale tracciato e ignorato, e mantenerlo allineato a `template-claude-developing` come sorgente.

Motivazione: persistenza strutturale su disco indipendente dalla sessione, e controllo umano sul versionamento.

Conseguenze: ogni passo significativo aggiorna schede, snapshot e work-log; commit e push restano manuali.

## ADR-002 - Progettare a partire dalla stanza e non dal diffusore

Data: 2026-09-04, formalizzazione di una scelta già implicita nel documento sorgente. Stato: accettata.

Contesto: il punto di ascolto è in una stanza irregolare, con soffitto spiovente e una parete vicina alle spalle, e non è trattabile acusticamente né riposizionabile per vincoli di arredamento.

Decisione: invertire l'ordine consueto. Misurare la stanza prima, validare un modello geometrico contro quella misura, progettare il diffusore in campo libero in parallelo, e ottimizzare la posizione solo alla fine con i due modelli insieme.

Motivazione: un monitor progettato per essere neutro in campo libero subisce la stanza; qui la stanza è nota e diventa vincolo di progetto invece di disturbo.

Conseguenze: la fase di misura è un prerequisito e non una verifica finale, e va eseguita prima dell'acquisto dei driver. La ripetibilità del setup di misura diventa un requisito, perché la misura della fase 1 e quella della fase 8 devono essere confrontabili a mesi di distanza. Il criterio di successo del progetto è definito al punto di ascolto reale, non in camera anecoica.

## ADR-003 - Wine invece di una macchina virtuale Windows

Data: 2026-09-04, formalizzazione. Stato: accettata.

Contesto: quattro programmi indispensabili al progetto esistono solo per Windows: Akabak, VACS, VituixCAD ed EASE Focus. La macchina di lavoro è Ubuntu Studio.

Decisione: usare Wine con un prefix per programma, e non una macchina virtuale Windows.

Motivazione: tre argomenti indipendenti, tutti verificabili. La catena audio resta quella nativa di Linux con il kernel a bassa latenza, mentre una macchina virtuale aggiungerebbe latenza proprio nella fase in cui si misura il tempo. L'identificativo hardware esposto è quello reale, quindi la licenza machine-based di Akabak sopravvive a reinstallazioni e ricostruzioni dei prefix, mentre in una macchina virtuale sarebbe diverso e andrebbe richiesta di nuovo. Non serve licenza Windows né la manutenzione delle sue patch, perché nessun codice Windows è in esecuzione.

Conseguenze: i guasti hanno la forma di librerie mancanti invece di problemi di driver, e la cura è installare il runtime giusto nel prefix giusto. Un programma che richiedesse un driver in kernel space non funzionerebbe, e per quello servirebbe tornare a una macchina virtuale; nessuno dei quattro programmi del progetto ricade in quel caso. Il backup di un ambiente configurato è una copia di cartella.

## ADR-004 - Un prefix Wine per programma, e nessun prefix a 32 bit

Data: 2026-09-04. Stato: accettata.

Contesto: il documento sorgente registra sia l'uso di un prefix condiviso, che con Akabak è andato bene, sia la buona pratica del prefix separato. Registra anche un guasto reale su `kernel32.dll`, causato da un prefix creato prima che l'architettura a 32 bit fosse dichiarata.

Decisione: un prefix dedicato per ciascuno dei quattro programmi, tutti a 64 bit, e non installare WinISD.

Motivazione: l'isolamento evita che un programma che pretende una versione diversa di .NET o di una DLL rompa gli altri, e permette il backup indipendente di ciascun ambiente. WinISD è il solo programma che richiederebbe un prefix a 32 bit, ed è ridondante rispetto a VituixCAD e Akabak: rinunciarvi elimina un prefix, l'architettura `i386` da mantenere e la classe di guasti che ne deriva.

Conseguenze: qualche comando più lungo e più spazio su disco. L'architettura `i386` non va aggiunta sulla macchina nuova, il che rimuove anche uno dei fattori di attrito degli aggiornamenti di rilascio. Se in futuro servisse un programma a 32 bit, la decisione va rivista con una voce nuova.

## ADR-005 - Blocco documentale sull'ambiente condiviso fra due progetti, con propagazione unidirezionale

Data: 2026-09-04. Stato: accettata.

Contesto: la stessa macchina Ubuntu Studio serve alla progettazione elettroacustica di questo progetto e all'home recording di `home-recording-training-mixing-setup`. La documentazione dell'ambiente serve a entrambi.

Decisione: tenere il blocco `docs/10-ambiente/` come copia canonica in questo progetto e propagarlo al gemello con `tools/sync-ambiente.py`, in una sola direzione, marcando ogni copia con una intestazione che ne dichiara la provenienza.

Motivazione: le alternative sono peggiori. Duplicare a mano garantisce la divergenza silenziosa. Un submodule git aggiungerebbe una dipendenza fra due repository personali per otto file di testo. Una sincronizzazione bidirezionale richiederebbe risoluzione dei conflitti, che a due copie non vale il costo.

Conseguenze: il blocco si modifica solo qui. Lo strumento rileva i file orfani nel gemello ma non li rimuove, perché una rimozione automatica su un altro repository è un rischio che non compensa. Il controllo `python tools/sync-ambiente.py --check` entra nella sequenza di verifica prima di un commit.

## ADR-006 - Installazione pulita di Ubuntu Studio 26.04 LTS invece dell'aggiornamento in posto

Data: 2026-09-04. Stato: proposta, in attesa della conferma della diagnosi sulla macchina.

Contesto: la macchina è su Ubuntu Studio 25.04, una versione intermedia fuori supporto, e la LTS successiva non è raggiungibile con un salto singolo. La ricostruzione della diagnosi è in `docs/10-ambiente/ubuntu-lts-upgrade.md` e non è ancora verificata sulla macchina.

Decisione proposta: installazione pulita della 26.04 LTS riformattando la sola partizione root e conservando `/home` senza formattarla.

Motivazione: quattro argomenti. È più corta e più prevedibile di due aggiornamenti di rilascio in cascata attraverso archivi storici. Coincide con l'obiettivo dichiarato di un setup pulito, e ricostruire l'ambiente Wine da zero elimina la sedimentazione che ha generato i guasti registrati. Non mette a rischio la licenza di Akabak, che è legata alla macchina e non all'installazione, per ADR-003. Porta su una base con supporto fino al 2031, da cui gli aggiornamenti futuri procedono da LTS a LTS.

Conseguenze se accettata: il trasferimento dei materiali va eseguito prima della reinstallazione e non dopo, perché la destinazione è sotto `/home`. Tutti i programmi Windows vanno reinstallati secondo `docs/10-ambiente/wine-configurazione.md`. Il release code di Akabak va reinserito, e la sua accettazione è la prova pratica di ADR-003. Il partizionamento con `/home` separato, scelto all'installazione originaria, è ciò che rende l'operazione a basso rischio.

Resta proposta e non accettata perché la diagnosi non è verificata: la macchina non era raggiungibile, quindi nessuno dei comandi di verifica è stato eseguito su di essa.
