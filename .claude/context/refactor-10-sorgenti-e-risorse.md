# 10. Il verde della postazione e la ricostruzione del progetto

## Il difetto che il primo banco non vedeva

In MS-319 i modelli e i formati CAD avevano prove reali: file ricomputati, riaperti e alterazioni rilevate. Anche le figure venivano rigenerate. Ma tutto avveniva nella stessa cartella che conteneva il kit precedente. La prova chiamata «un clone possiede già gli SVG» cambiava la destinazione dei PDF, lasciando disponibili le risorse in build.

L'archivio Git estratto in una cartella nuova ha esercitato un confine diverso. Il codice era presente, i font esistevano sulla macchina, ma i generatori cercavano soltanto la copia nel vecchio kit ignorato. I test del manifesto incontravano inoltre CAD e PDF generati assenti. I verdi precedenti rimangono prove del comportamento locale; non provavano la ricostruzione dai sorgenti.

## La risorsa diventa un input dichiarato

[font_intrawelt.py](../../tools/font_intrawelt.py) risolve la risorsa con una precedenza esplicita: argomento, variabile di ambiente, account attivo e font installati. Un argomento errato produce un errore, anche se sulla macchina esiste una copia alternativa. Sostituirlo in silenzio renderebbe riuscita la procedura usando un input diverso da quello richiesto.

I grafici dichiarano l'impronta dei font, senza pubblicare il percorso di account. Le tavole mantengono il controllo TrueType emesso da CADCraft e dichiarano anche l'hash della dipendenza che seleziona la risorsa. La presenza di un file e la risoluzione del font nel motore CAD sono controlli distinti: la prova CLI ha mostrato che il nome del file viene risolto, mentre un percorso assoluto conservato nello stile non viene riconosciuto come TrueType da CADCraft 0.20.1.

## La fixture deve corrispondere alla domanda del test

[test_consegna_completamento.py](../../tools/test_consegna_completamento.py) costruisce ora byte opachi, impronte e rapporti temporanei. Verifica che il kit conservi i payload attesi, rifiuti uno STEP alterato prima della firma, rifiuti un file modificato dopo l'estrazione e respinga una sorgente PDF superata. Una quinta prova modifica la dipendenza CAD prima della firma. Non vengono simulate le equazioni o le operazioni booleane: il confine di questi test è l'integrità dei file.

Questo permette di eseguire quei contratti senza i prodotti del collaudo precedente. Non permette di chiamare valido un modello CAD costruito nella fixture. La verifica dei volumi, la riapertura del nativo, il reimport dello STEP e la lettura del DXF restano nei collaudi reali. Il comando di consegna continua a consumare soltanto quegli artefatti verificati.

## La prova che chiude il difetto

[test_ricostruzione_sorgenti.py](../../tools/test_ricostruzione_sorgenti.py) copia i sorgenti in una cartella priva del vecchio build, passa la risorsa di account come input ed esegue processi Python e CADCraft reali. Ricostruisce quattro PDF scientifici, confronta gli SVG con le figure correnti e ricrea la figura del basso. Legge dodici profili per ciascuna delle tre varianti e lancia i contratti del kit senza CAD o PDF preesistenti. Il caso negativo imposta una directory font assente e verifica che il generatore fallisca prima di creare la destinazione.

La prima esecuzione ha trovato la figura del basso da rigenerare per la nuova provenienza. La modifica del suo percorso di scrittura ha poi esposto un import sys dimenticato, corretto prima del verde; la prova ora esegue anche la scrittura e non soltanto il check. Le diciassette prove mirate sono passate insieme. La ricostruibilità misurata riguarda il progetto su un ambiente con i programmi e il design system dichiarati, senza installazioni o verifiche fisiche implicite.
