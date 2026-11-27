# Fasi 6, 7 e 8: acquisto, montaggio e verifica finale

Procedura di progetto aggiornata il 27 novembre 2026, MS-328. Riunisce acquisto, giunzioni, cablaggio e taratura. La [scheda di collaudo](70a-scheda-collaudo-a24.md) conserva esiti e prove per esemplare. Il protocollo è pronto per la revisione. ADR-055 mantiene sospesi acquisti, costruzione e verifiche fisiche fino a riapertura esplicita.

## Sequenza corrente per A24

| Fase | Che cosa si approva per avanzare | Dove si registra |
|---|---|---|
| A. Scelta e preventivo | Variante del retro compatibile con spazio e manutenzione, sigle effettive, proposta di spesa approvata | Scheda A e distinta 67-69a |
| B. Prova a secco e montaggio | Incastri e appoggi conformi alla tavola esecutiva, tenuta e percorso accessibile | Scheda B e quote riscontrate |
| C. Cablaggio scollegato | Continuità e isolamento delle quattro vie, sigle e polarità coerenti | Scheda C e continuità |
| D. Banco con carichi fittizi | Routing, protezione, guadagno e limiti verificati in PC e Pi | Scheda D, tracce ed esito del pannello |
| E. Misura e crossover | Dati con riferimenti comuni, filtri candidati provati su file e verificati a basso livello | Scheda E, acquisizioni e profili |
| F. Verifica finale | Risposta misurata, avvio e guasti controllati, consegna riproducibile | Scheda F e rapporto di accettazione |

Si avanza con evidenza registrata e firma di chi ha eseguito o revisionato la verifica. Un esito fuori criterio ferma la fase. Si annota la misura, si corregge la causa e si ripetono la prova fallita e quelle che dipendono dall'intervento. Una verifica su PC non compila la riga Pi. Una prova su file vale per il calcolo, con evidenza distinta dal banco.

### A. Prima di ordinare o autorizzare tagli

Usare quantità e sigle del [capitolo67](67-catena-di-riferimento-e-dipendenze-esecutive.md). Verificare apertura, flange e fissaggi contro i disegni della variante esatta. Confrontare stock, prezzo e resi prima dell'approvazione. Una sostituzione di driver riapre geometria, modello e filtro. Annotare ordine e lavorazioni soltanto dopo decisione del proprietario.

Il [confronto 69a](69a-discesa-cavi-st120.md) distingue circa 80 mm con la piastra centrale, 54 mm con centrale arretrata e 33 mm con la compatta per la manovra modellata. La scelta richiede luce effettiva dal bordo del ripiano alla parete, sagoma di appoggio e possibilità di innesto e sgancio. Tenere la piastra centrale se questi riscontri la ammettono. Una variante arretrata richiede tavola ed esame della tenuta del vano prima dei tagli. Per la prequalifica si può usare un provino e una sagoma, con revisione e acquisti autorizzati separatamente dal lotto definitivo.

### B. Prova a secco, poi montaggio

Presentare al supporto il [modello nominale](64-reflex-direttivita-e-cabinet-nominale.md), la [tavola del retro](69-retro-a24-e-passaggio-cavi.md) e l'elenco dei punti ancora da verificare. Il disegno per la lavorazione porta revisione, facce di riferimento, spessori, giochi, fissaggi, giunzioni e passaggio posteriore. Registrare le tolleranze concordate dal supporto prima del pezzo definitivo.

Montare a secco sei pannelli e rinforzo a finestra. Riscontrare diagonali e profondità dell'assieme, appoggio dei telai e della piastra, accesso agli inserti e corridoio HF. Saggiare tenuta, fissaggio e possibilità di estrarre la piastra senza tirare i faston. Approvare il percorso dell'ansa prima di chiudere il cabinet. Dopo l'incollaggio e la sigillatura ricontrollare giunzioni, guarnizioni e appoggio. Conservare revisione del mobile e riscontro di tenuta con metodo e condizioni. Una perdita cambia la risposta di un cabinet chiuso e va risolta prima della taratura.

### C. Continuità e isolamento a banco spento

Con finale disalimentato e cavo scollegato ai due lati, verificare ogni conduttore da capo a capo, poi ogni coppia distinta di contatti e la separazione dal telaio. Registrare resistenza dei puntali e lettura a puntali aperti. Verificare i quattro contatti sul cabinet sinistro e destro. Sul diretto TRS-RCA il ring deve risultare isolato secondo il [capitolo68](68-cablaggio-quattro-vie.md). La variante isolata ha invece TRS a tre conduttori lato UMC1820 e RCA separato dopo il trasformatore. Confrontare il verso di tutte le etichette con la scheda C. Una coppia invertita o comune va corretta prima di collegare il carico fittizio.

### D. Banco elettrico con quattro carichi fittizi

Qualificare prima il percorso di linea C-01 sui dispositivi effettivi. Controllare mappa, polarità, livello ricevuto, clipping e fondo di rumore del banco. Confrontare risposta D/I al medesimo livello in ingresso al V3. Come budget preliminare il capitolo68 assegna ±0,2 dB al solo collegamento sulla banda 60 Hz-20 kHz, con riferimento a 1 kHz. Registrare limite di rumore, incertezza dello strumento e margini prima della prova. Se il diretto eccede il limite, motivare il passaggio alla riserva isolata e ricontrollare la spesa.

Il carico di prova va fra `+` e `-` di ciascun finale. I finali a ponte richiedono misura differenziale idonea alla tensione di modo comune e ai residui di commutazione. Verificare portata, banda e isolamento dell'ingresso di misura. Il filtro dello strumento deve permettere il confronto nella banda scelta. Tenere i trasduttori scollegati e le pinze a massa lontane dai morsetti. [Nota TI SLOA068A, §3.1](https://www.ti.com/lit/an/sloa068a/sloa068a.pdf).

Per ciascuna coppia registrare resistenza, dissipazione ammessa nella configurazione reale e durata del segnale. Concordare il limite di banco prima di aumentare il livello. Per carichi resistivi la potenza media si ricava da `V_RMS²/R`; i limiti di picco e di durata si annotano separatamente. Provare entro il più restrittivo dei limiti di carico e strumento, fermandosi se compaiono clip, sovratemperatura o anomalie. Conservare il massimo verificato, il guadagno per via e la posizione delle due manopole. Il limite di esercizio dei driver è un limite ulteriore, da motivare con dati e protezioni, e può essere più basso di quello verificato sul resistore.

Percorrere una via per volta, confrontando la fondamentale sulla coppia designata e il residuo sulle altre tre con il fondo strumentale e il limite concordati. Ripetere a 44,1 e 48 kHz sui percorsi applicabili PC/Pi. Verificare cuffie a banda intera su 3/4, protezione passa-alto e guadagno HF, mute, livello di partenza e perdita di clock. Per il dettaglio del controllo comune usare il [manuale CamillaDSP](61-camilladsp-manuale-tecnico.md). Un guasto invalida la preparazione e richiede riabilitazione esplicita. Misurare separatamente il transitorio del mute e il regime. Disalimentare i finali prima di cambiare i collegamenti o il proprietario USB.

### E. Acquisizione, somma e taratura

Collegare una via alla volta dopo il banco. Per il tweeter verificare passa-alto, protezioni e limite di livello prima di emettere il segnale. La prima misura procede a livello contenuto e nella banda autorizzata. Annotare file di calibrazione del microfono, orientamento, eventuale riferimento assoluto, eccitazione ai morsetti, temperatura, distanza, angolo, finestra e banda valida. A parità di direzione e posizione mantenere riferimento temporale ed eccitazione comuni fra le due vie.

Per la fase usare loopback di linea o riferimento acustico fisso qualificato, con offset annotato. Conservare lo stesso zero temporale per i due driver. [REW, Making Measurements](https://www.roomeqwizard.com/help/help_en-GB/html/makingmeasurements.html).

Conservare sessione `.mdat`, curve con modulo e fase ed eventuali impulsi. Confrontare segno, unità, griglia e fase con la sessione. L'export REW può contenere zeri quando manca la fase. [REW, File Menu](https://www.roomeqwizard.com/help/help_en-GB/html/file.html).

Registrare crossover e protezioni presenti durante ogni sweep. Il [modulo del capitolo66](66-somma-acustica-e-crossover-su-file.md) applica il filtro candidato a risposte che lo precedono. Se era attivo un filtro di protezione, conservarne il contributo nella catena di riferimento o rimuoverlo dai dati soltanto con una correzione complessa qualificata nella banda valida. Una misura già passata attraverso il crossover candidato serve al confronto finale e non va filtrata nuovamente. Stabilità dei filtri, risposta in banda, fase, livello e ritardo devono tornare prima di applicare il candidato. Non si rimuove la protezione del tweeter per produrre un file pre-crossover.

La [caratterizzazione su file](65-caratterizzazione-aperta-e-dati-di-misura.md) verifica ingressi, unità, copertura e riferimento di livello. Blocca l'uso di dati insufficienti. Il confronto complesso produce una previsione, da confrontare poi con una misura diretta delle due vie insieme. Rettificare prima la causa di cancellazioni o incongruenze. Provare i profili candidati su file e sui carichi fittizi per entrambi i campionamenti prima di affidare il segnale ai driver.

### F. Verifica finale e restituzione

Acquisire una misura diretta per cabinet con profilo approvato, in asse e alle direzioni dichiarate, quindi verificare separatamente al punto di ascolto. Fissare bersaglio e livello di riferimento prima del confronto. Il target storico è ±2 dB da 60 Hz a 20 kHz, in asse e fino a ±10°. Riportare configurazione e posizioni usate, ripetibilità e banda realmente valida. Una finestra che taglia la validità del basso lascia la banda scoperta e va dichiarata. Se lo scostamento eccede il bersaglio resta fuori specifica anche quando i file passano i controlli di integrità.

Registrare prova a basso livello, ronzio e rumore, comportamento a spegnimento e perdita della sorgente, modalità Mix/Ascolto e autonomia Pi con PC spento. Separare taratura dei driver e interventi sul punto di ascolto. Una variante di EQ per ascolto va verificata con i suoi livelli e il proprio margine. Consegnare foto soltanto se autorizzate, tavole, distinta, `.mdat`, export, profili identificati, rapporto e condizioni di arresto. La scheda distingue dati misurati, dati simulati e punti rimasti aperti.

### Riscontro su file del criterio di avanzamento

Sulla postazione Windows con i pacchetti MS-322 già generati, i controlli seguenti ricalcolano allineato, polarità invertita e passaggio a caratterizzazione. I dati sono sintetici. L'allineato rientra nel bersaglio, l'invertito è fuori specifica a integrità verde. Entrambi mantengono la qualifica hardware falsa.

```powershell
cd "E:/diy-2way-monitors-home"
python tools/somma_acustica.py --manifest data/somma-acustica-demo/manifest.json --out build/somma-acustica-20261126/allineato --check
python tools/somma_acustica.py --manifest data/somma-acustica-demo/invertito.json --out build/somma-acustica-20261126/invertito --check
python tools/caratterizzazione.py --manifest build/somma-acustica-20261126/allineato/dataset.json --out build/caratterizzazione-somma-20261126 --check
```

## Note storiche delle fasi 6, 7 e 8

Le sezioni seguenti conservano l'origine del workflow e le ipotesi precedenti. La sequenza corrente, sopra, usa A24, driver e amplificazione della distinta consolidata.

## Lo stato reale di queste tre fasi

Va detto senza attenuazioni: nel documento sorgente le fasi 6, 7 e 8 erano segnaposto. La fase 6 aveva un titolo e un paragrafo di lettere ripetute. La fase 7 aveva un titolo, una sottosezione intitolata ai pannelli di legno e un altro segnaposto. La fase 8 aveva una sola frase di contenuto reale. Anche la sotto-fase 4b, la progettazione meccanica, era in condizioni simili nella parte di ingressi e uscite.

Questa asimmetria non è un difetto della conversione. Riflette lo stato del progetto: la parte simulativa è pensata in profondità, la parte fisica non è ancora iniziata. Registrarla come vuota è più utile che riempirla di contenuto plausibile, perché una pagina inventata verrebbe letta come una decisione presa.

Alle tre fasi si aggiunge un secondo filone appena abbozzato nel sorgente, la personalizzazione di un amplificatore per il basso, che aveva un titolo, una sottosezione sul modello e nessun contenuto. È fuori dallo scopo del progetto dei monitor e resta annotato come possibile lavoro separato.

## Fase 6: acquisto dei driver

Che cosa dovrà produrre: una coppia di woofer e una coppia di tweeter reali, scelti perché i loro parametri Thiele/Small sono quelli su cui la fase 4a ha convalidato il progetto.

Le decisioni che la precedono e che oggi sono aperte. La curva di risposta target va fissata prima, perché è il criterio con cui si giudica un candidato. Il diametro e le caratteristiche del woofer derivano dal volume del box e dall'accordo che la simulazione avrà stabilito; l'ipotesi di partenza registrata negli appunti è quattro pollici. Il tweeter dipende dalla frequenza di incrocio che uscirà dalla fase 4a.

Un vincolo di reperibilità è già noto e va tenuto presente perché può cambiare la scelta: gli appunti registrano che il canale di approvvigionamento professionale usato in passato non è più disponibile, e che l'alternativa ipotizzata è il recupero da magazzino tramite un ex collega. Questo rende la disponibilità un parametro di selezione reale accanto alle specifiche, e suggerisce di verificare che cosa è ottenibile prima di ottimizzare il progetto su un driver che non si può comprare.

## Fase 7: montaggio

Aggiornamento del 2026-11-18, MS-236. L'utente dispone di un contatto che lo aiuterà sia con il progetto dei due vie sia con un falegname per la realizzazione, una volta completato il progetto teorico. Il passaggio pratico ha quindi un supporto già individuato. Nomi e recapiti restano nel livello privato del progetto. Per il confronto si preparano disegni del cabinet, distinta dei pannelli, fresature, materiali, tolleranze, assemblaggio e collegamenti, dopo la verifica teorica.

Che cosa dovrà produrre: i due cabinet costruiti secondo i disegni della fase 4b.

L'ipotesi di realizzazione registrata negli appunti è il taglio dei pannelli di legno da parte di un artigiano, non una fresatura a controllo numerico. È la ragione per cui il formato `.dxf` è, fra le esportazioni di FreeCAD, quella che conta davvero: sono i pannelli da tagliare a misura.

Le decisioni aperte sono il materiale definitivo, con l'MDF fra 18 e 25 millimetri come ipotesi di partenza già usata come parametro nelle simulazioni, il metodo di assemblaggio e la tenuta d'aria, che in un caricamento bass reflex incide direttamente sull'accordo, e lo smorzamento interno, che nella fase 5 è modellato come schiuma acustica o fibra di poliestere e va scelto in coerenza con quanto simulato.

## Fase 8: verifica finale

Che cosa dovrà produrre: la misura dello scostamento fra il progetto simulato e l'oggetto costruito.

La procedura è la stessa della fase 1, con la stessa catena di misura e nello stesso punto di ascolto, ed è precisamente per questo che la fase 1 va documentata con cura: la ripetibilità del setup di misura è ciò che rende confrontabili le due misure a distanza di mesi. Il file di sessione `.mdat` della prima misura conserva quel contesto, e va conservato per questo motivo.

Il criterio di giudizio è la distanza dal criterio di uscita già dichiarato per le fasi 4 e 5, cioè una risposta lineare entro più o meno 2 dB in asse e fino a più o meno dieci gradi fuori asse, da 60 Hz a circa 20 kHz. Lo scarto fra quel bersaglio e la misura reale è il risultato del progetto.

Rettifica del 26 novembre 2026: l’export del programma di misura non crea automaticamente un GLL autorizzato. Il [capitolo65](65-caratterizzazione-aperta-e-dati-di-misura.md) separa acquisizione, confronto dei dati e authoring eventuale. La pipeline su file è sviluppata; l’uso futuro di SpeakerLab e l’autorizzazione per Focus restano una decisione distinta, senza acquisti anticipati.

## Il correttivo, che è l'ultima decisione aperta

Gli appunti registrano una domanda mai risolta, e vale lasciarla come domanda invece di risolverla d'ufficio: se dopo la verifica finale resta uno scostamento, lo si corregge intervenendo sul crossover, oppure con una equalizzazione digitale nella catena di ascolto, oppure accettandolo.

Il progetto ha una posizione implicita, perché la sua premessa è progettare il diffusore in funzione della stanza invece di correggere a posteriori, e questo spinge verso l'intervento sul crossover. La decisione però dipende da quanto grande sia lo scarto e da dove cada in frequenza, quindi non si può prendere prima di avere la misura.

## Intervento sull'amplificatore EKO già posseduto

L'utente dichiara nel giro del 18/19 novembre che lo stesso contatto lo aiuterà anche con la sostituzione dello speaker del suo amplificatore EKO per basso. È PA-039: prima del ricambio servono identificazione del modello, carico, quote e cabinet. Il supporto è disponibile per dichiarazione dell'utente; nessun ricambio o incarico è stato deciso dall'agente. La scheda è [EKO per basso](80-strumenti-posseduti/eko-basso.md).

## Dettaglio nominale completato il 25 novembre

Il [capitolo 64](64-reflex-direttivita-e-cabinet-nominale.md) completa frontali, incassi, rinforzo e distinta per A24/B27/C24, con nativi FreeCAD, STEP e DXF effettivamente riletti. Il modello mantiene le battute incollate dei sei pannelli e aggiunge un rinforzo a finestra. I cerchi di fissaggio sono centri nominali, senza inventare il diametro pilota di una vite ancora da scegliere.

La [consegna locale](../build/consegna-completamento-20261125/README.md) permette di aprire l'assieme e discutere quote e lavorazioni col supporto già individuato. Non è un ordine di taglio: restano da confermare processo, giochi, fissaggi, sigillatura, assorbente, connettori e appoggi reali. Il confronto fisico e la costruzione rimangono sospesi. Le verifiche numeriche dei solidi non dichiarano una verifica strutturale della colla o del mobile.
