# Somma acustica su file, specifica e piano MS-322

Base main ea70a7b. Prosecuzione autonoma autorizzata dal proprietario; esecuzione inline con writing-plans ed executing-plans. Commit, push, deploy e installazioni manuali. Due GRC riservati al template, nessun agente parallelo. Verifiche fisiche sospese ADR-055.

## Scopo e scelta

Collegare i dati complessi importati in MS-321 al progetto del crossover: risposta di ciascun driver moltiplicata per filtro elettrico, guadagno, polarità e ritardo espliciti, poi somma dei numeri complessi. Le curve dei due driver devono avere fase disponibile e identica griglia. Il manifesto dichiara stesso livello di eccitazione, riferimento temporale, direzione/distanza e risposta del driver senza il crossover da applicare. Sono dichiarazioni da qualificare in futuro, non proprietà dimostrate dal software.

Alternative considerate: sommare soltanto i moduli perde le cancellazioni; costruire un interprete generale di configurazioni CamillaDSP allargherebbe inutilmente il perimetro. Si usano sezioni digitali del secondo ordine con coefficienti espliciti, senza reinterpretare il servizio installato. Le formule LR4 esistenti in tools/verifica-matematica-crossover.py producono i coefficienti dell'esempio; il nuovo modulo valuta coefficienti, non risceglie il crossover o i driver.

NumPy e libreria standard già presenti. La ricerca nel catalogo per crossover/FRD/fase e altoparlanti/filtri non ha trovato una capacità pertinente. Nessun pacchetto installato. Nessun ricampionamento, fase minima ricavata o spostamento automatico del tempo: rifiutare griglie diverse evita un'interpolazione di fase ambigua. Nessun microfono, periferica o processo audio aperto.

## Task1: calcolo complesso

- [x] Scrivere e vedere rosse le prove analitiche di SOS, somma coerente, cancellazione, guadagno, polarità e segno del ritardo.
- [x] Implementare tools/somma_acustica.py: sos_response(frequency, samplerate, sos) e sum_branches(woofer, tweeter, samplerate, woofer_filter, tweeter_filter), riusando Curve e parsing di caratterizzazione.
- [x] Verificare coefficienti finiti, denominatore non nullo, poli strettamente interni al cerchio unitario, frequenze sotto Nyquist, griglie identiche e fase obbligatoria. Niente normalizzazioni dei singoli driver.

## Task2: manifesto, qualità e consegna

- [x] Provare riferimenti mancanti, banda/coerenza degli input, fase indefinita nei nulli, percorsi esterni e alterazioni di input/codice/output.
- [x] Implementare analyse_manifest(path), build_bundle(path), write_bundle(path, output), check_bundle(path, output) e CLI --manifest/--out/--check. Snapshot dei byte originali; impronte di modulo e dipendenza. Cartella nuova, nessuna sovrascrittura del lavoro umano.
- [x] Esportare CSV con parte reale/immaginaria e fase vuota nei nulli; FRD a tre colonne soltanto se tutte le fasi sono definite, altrimenti due colonne. Il pavimento numerico del modulo è esplicito. Dataset risultante riutilizzabile da caratterizzazione; data_kind simulated e hardware_qualified falso.

## Task3: esempio e integrazione

- [x] Versionare esempio analitico con due driver unitari e coefficienti LR4 digitali a 2kHz/48kHz. Eseguire casi allineato, invertito e ritardato di sei campioni: al taglio moduli attesi 1,0,sqrt(0.5). Nessuna risposta reale dei candidati SB dedotta.
- [x] Reintrodurre la somma dei moduli come mutazione, osservare la prova fallire, ripristinare e confrontare SHA. Documentare metodo, limiti, comandi eseguiti e difetti effettivamente incontrati.
- [x] Integrare i controlli nella chiusura, aggiornare documentazione/memoria/didattica e indici pertinenti, PDF con QA e gate completo. Preparare messaggio e perimetro per la sola chiusura manuale.

## Fuoco della revisione

La fase importata non prova un riferimento temporale comune. Il modulo di una somma non è la somma dei moduli. Un nullo non ha fase zero: il CSV lascia il campo vuoto e il FRD rinuncia alla colonna di fase. La coerenza della somma non si ricava prendendo il minimo delle coerenze dei driver: si riportano separatamente qualità degli input e risultato calcolato. Una banda dichiarata insufficiente non diventa valida perché il filtro attenua quel driver. Un integrità verde non qualifica né la previsione acustica né l'hardware.

## Registro di esecuzione

Specifica e piano scritti prima del codice. Il mandato di prosecuzione permette le scelte ordinarie senza nuove domande; nessuna decisione di spesa o di prodotto è congelata. La revisione resta in prima persona per la regola locale che non delega progettazione e revisione.

Task1 e2 sviluppati:22 test verdi. Tre casi analitici generati e controllati; LR4 confrontato con il modello continuo alla frequenza bilineare, modulo al taglio1/circa0/sqrt(0,5). La mutazione della somma dei moduli fa cadere la prova; SHA ripristinato identico. Ruling: con qualità insufficiente degli input non si esportano dataset.json e system.frd, per impedire al passaggio successivo di perdere il vincolo; restano diagnostici e originali. Il downstream allineato è stato eseguito realmente ed è simulated. Ultimo task ancora da verificare con QA e gate completi.


Consolidamento:22 test, due mutazioni rilevate e ripristini SHA, tre pacchetti e passaggio downstream verificati. Quattro PDF con QA, recap tutte le sette pagine viste; catalogo189 e mappa213 fonti/46 curate, didattica12. Il primo gate ha superato45 dei46 comandi locali e si è fermato sull'ancora deployment; dopo rilettura documentale è stata aggiornata soltanto la firma e il controllo mirato non rileva invarianti rotti. Ultima esecuzione completa dopo questa persistenza nel rapporto privato chiudi-finale.txt: la proposta di chiudi resta subordinata alla sua ultima riga «Controlli verdi». Nessuna guardia esclusa o verifica fisica riaperta.
