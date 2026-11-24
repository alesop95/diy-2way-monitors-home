# 6. L'autonomia richiede un percorso, la prova un risultato leggibile

Approfondimento del 2026-11-20. L'utente rende obbligatorio ascoltare da CD o altri riproduttori con PC spento, chiede sviluppo dei componenti e formule leggibili. Le decisioni ADR-051/052 e il documento 63 trasformano il requisito in due percorsi completi; il dossier 62 conserva la matematica generale.

## La premessa corretta cambia la scelta

La prima proposta privilegiava il PC esistente perché evitava un altro processore. Era sensata sotto il requisito limitato alla sorgente PC, ma non soddisfa l'autonomia ora esplicita. Aggiungere il nome Raspberry alla distinta non risolverebbe l'ingresso CD, il clock, il volume o la proprietà dell'interfaccia USB.

Il nuovo percorso riusa l'interfaccia in due modalità alternative. PC e Pi non sono contemporaneamente host della stessa periferica: si commuta fisicamente il collegamento, confrontando uno switch con il cavo diretto. Il costo evitato è un secondo convertitore multicanale; il costo tecnico introdotto è qualificare rilascio, aggancio e ritorno in attesa silenziata. Un uso simultaneo richiederebbe un altro progetto.

Il manuale UMC1820 rivela due vincoli che il conteggio dei canali non mostra: l'ingresso coassiale dipende dalla modalità ottica, e le Line Out non seguono la manopola Main. La stessa scatola può avere abbastanza porte e richiedere comunque un controllo di volume comune distinto. Bit perfect si misura prima del DSP, dove i campioni devono essere conservati; le quattro vie filtrate sono intenzionalmente differenti.

## Il modello produce una decisione e un limite

Il nuovo studio usa parametri di datasheet normalizzati e i volumi geometrici già costruiti. La prova del caso Butterworth è stata scritta prima del codice, insieme al limite di volume grande e alle leggi di scala della pressione. Il modello indica circa -4,44 dB a 60 Hz per SB16/A24 chiuso: è un motivo per studiare compensazione e livello massimo, non per dichiarare raggiunto il target.

Il dato Fs da solo non ordina le alternative: nel secondo driver il Q inferiore produce una f3 più alta anche quando la risonanza del sistema scende. Questa distinzione rende utile spendere più tempo nel modello prima di spendere sui trasduttori. Il candidato economico e l'alternativa stretta hanno conseguenze esplicite su corsa, frontale e costo.

## Il difetto era nella misura che volevamo confrontare

Nel collaudo su file i canali non selezionati contengono un disturbo. Una selezione corretta deve produrre lo stesso segnale della sorgente stereo; la selezione sbagliata deve cambiarlo. Il controllo negativo modifica realmente il mapping e il confronto vede circa 0,02485 di differenza massima nel caso perturbato.

Un primo confronto fra profili usava RMS globale. Nel ramo tweeter a 100 Hz il fondamentale è molto attenuato e le armoniche generate dalla quantizzazione a 16 bit pesano relativamente di più: il rapporto RMS non rappresentava più il solo guadagno alla frequenza voluta. La correzione misura la componente coerente:

```python
amplitude = abs(np.mean(signal * np.exp(-2j*np.pi*frequency*time)))
```

La frequenza, la durata e il tratto a regime sono dichiarati; non si interpreta una differenza di RMS come errore del filtro quando il dato contiene altre frequenze. Separatamente il parser ha respinto un filtro Volume assegnato a Main: nella 4.1.3 Main è già implicito e il filtro aggiuntivo serve ai fader Aux. Entrambi i tentativi sono conservati per spiegare perché la prova corrente è formulata così.

## Il verde del controllo va interpretato dalla causa

Chiudi mostrava in coda stringhe Python da rivedere. Era stato attribuito loro il fallimento, ma il sorgente del correttore dice che quei residui sono solo avvisi. L'intercettazione non mutante del risultato ha trovato un vero accento mancante nella docstring dell'installatore. Correggere quella parola ha portato a zero i cambiamenti richiesti, mantenendo intatto il controllo. Escludere tutti i file Python avrebbe nascosto la causa e ridotto la copertura.

Le altre derive sono state trattate separatamente: hook confrontati con il modello e tabelle con separatori interni esplicitamente escapati. Il test del secret scan usa un git sintetico per evitare stage o commit: distingue contesto, aggiunta da bloccare ed esenzione locale. Anche il wrapper di prova deve propagare il codice di uscita del processo che vuole misurare.

## La consegna esiste nel lettore, oltre che nel sorgente

Il Markdown era ispezionabile ma il lettore dell'utente non mostrava le equazioni. I due capitoli sono ora convertiti con Pandoc e compilati con LuaLaTeX: frazioni, simboli e grafici restano leggibili nel PDF. Questo è un requisito di prodotto, non un dettaglio estetico del sorgente.

Una vecchia anteprima PNG del capitolo 63 sembrava tagliata; il rendering fresco del PDF finale era corretto. La conferma viene dai limiti del testo e dalle anteprime correnti con hash del PDF, non dal nome del PNG. Le tredici pagine sono conservate in un nuovo insieme di preview finali. Il principio riutilizzabile è lo stesso del banco audio: identificare l'oggetto effettivamente osservato prima di attribuirgli l'esito di una prova.
