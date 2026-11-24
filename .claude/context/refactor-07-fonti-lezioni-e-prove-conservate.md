# Dalla raccolta di link a una catena di evidenze

Data: 2026-11-20. Evidenze locali: MS-292/294, `tools/mappa_fonti_progetto.py`, `tools/test_mappa_fonti.py`, mappa degli usi e ricevuta del riordino privato. Questo approfondimento spiega la scelta di metodo; lo stato corrente rimane nello snapshot.

## Il problema prima del riordino

Le fonti erano presenti in molti documenti: manuale CamillaDSP, ricerca LR4, proposta autonoma, schede degli strumenti e cronologia. Il registro bibliografico storico già esisteva, perciò crearne un altro avrebbe dato due autorità per la stessa opera. Mancava invece una domanda diversa: dove viene usata ogni risorsa, quale versione è stata letta e quale parte sostiene la decisione?

Anche i risultati erano distribuiti fra più run. Un rapporto identico in due cartelle non era necessariamente immondizia: poteva dimostrare che una modifica del runner aveva lasciato invariato il risultato. Le prime prove fallite spiegavano il passaggio dall'RMS alla fondamentale coerente o la correzione della sintassi del motore. Eliminarle solo perché una corsa successiva era verde avrebbe indebolito la documentazione richiesta dall'utente.

## Il salto: identità, lettura e uso separati

Si mantiene la biblioteca canonica e si aggiunge una mappa degli usi. Le fonti curate hanno ID esplicito; gli altri riferimenti ricevono un identificativo stabile dalla chiave normalizzata del template. Gli alias vengono dichiarati, non dedotti dalla somiglianza di due pagine. La citekey esistente rimane la chiave bibliografica, mentre l'ID distingue la risorsa e la versione usate nel progetto.

```python
def seed_index(records):
    result = {}
    for source in records:
        if source['id'] in result:
            raise ValueError(f"Identità duplicata: {source['id']}")
        result[source['id']] = dict(source, usi=list(source.get('usi_dichiarati', [])))
    return result
```

Il rifiuto precede la costruzione del dizionario. Contare gli ID alla fine sarebbe inutile: l'assegnazione avrebbe già sovrascritto la prima voce. La regressione locale aggiunta durante il lavoro ha fallito prima dell'introduzione di `seed_index`, quindi è diventata verde. Un'altra regressione ha riprodotto il `KeyError: usi` realmente incontrato sul primo riferimento non curato. La prova completa sul corpus è necessaria anche quando le funzioni più piccole passano.

La mappa non trasforma una fonte censita in una fonte letta. Per il Marshall si conserva il riscontro del manuale scansionato e delle immagini, senza inventare uno schema elettrico. Per OpenCV si dichiara la lettura pertinente all'omografia, senza pretendere di ricavare da un solo piano l'altezza delle orecchie. Per i vecchi collegamenti si mantiene il contesto locale e lo stato da riconciliare. L'output è un elenco controllabile di lacune, oltre che delle evidenze già disponibili.

## Una pulizia che lascia visibile il passato

La ricognizione meccanica ha trovato duplicati esatti e corse di generazioni precedenti. La scelta è stata conservare ogni file dei run superati in un archivio compresso, con percorsi originali e manifesto. Il verificatore ha aperto ogni membro e ricalcolato SHA-256; il passo successivo ha ricontrollato gli originali, escluso collegamenti e verificato il contenimento in build prima della rimozione degli espansi.

Il risultato è una riduzione lorda di 199.643.239 byte e la conservazione di tutti i 340 file selezionati. Le relazioni correnti, i profili finali, il modello v5 e il kit CAD rimangono disponibili. I riferimenti nei microstep storici sono risolti dal manifesto, che indica dove ritrovare il percorso originale nel ZIP. La compressione sullo stesso disco non crea un backup: conserva e rende meno dispersivo il materiale esistente.

## Come una lezione diventa riutilizzabile

Le sette lezioni del registro locale hanno un'evidenza audio e non importano casi di altri progetti. Il confronto autorizzato ha riunito principi di autorità documentale, passaggio dalla raccolta all'uso e rigenerazione protetta. Il confine sui dati aziendali è parte del metodo: una regola generica si può applicare senza copiare l'episodio o i documenti da cui è nata altrove.

Il nuovo controllo dell'output e le regressioni sono dentro `tools/controlli-progetto.txt`, perché una capacità che chiudi non verifica rimarrebbe affidata alla memoria di chi lavora. Il registro lezioni non sostituisce la cronologia né il racconto didattico: raccoglie soltanto ciò che può valere oltre il progetto. La ricezione nel template sarà un'attività distinta, non dichiarata già avvenuta.

## Il passo successivo: il PDF corretto deve derivare dal sorgente corrente

In MS-300/305 la sola impronta del PDF non bastava: un vecchio PDF può essere integro e descrivere un Markdown ormai cambiato. tools/verifica_documenti.py controlla sia il binario consegnato sia tutti gli input elencati nel manifesto. La regressione cambia il testo sorgente lasciando identici i byte del PDF: il controllo diventa rosso. Aggiornando il record alla nuova sorgente torna verde soltanto nel caso costruito; nel lavoro reale il manifesto si aggiorna dopo la nuova compilazione ed ispezione, non per aggirare il controllo.

La prova visiva e la conservazione del suo bitmap sono due esigenze distinte. Le anteprime per pagina erano utili per trovare tabelle e formule tagliate, ma la loro permanenza moltiplicava file derivati e confondeva le consegne con il laboratorio. Ora si ispeziona l'immagine corrente, si conserva nel manifesto il PDF cui si riferiva il controllo e si elimina l'immagine. Le viste CAD restano perché spiegano la geometria del progetto. Il risultato leggibile sta in docs/pdf e build conserva gli intermedi necessari a riprodurlo.

Anche uno snapshot può diventare duplicazione: decine di aggiornamenti successivi in testa alla memoria fanno leggere come attuali i vecchi esiti. La copia integrale viene archiviata prima del consolidamento; la ripresa conserva soltanto stato e riferimenti, mentre OPS e progress mantengono la cronaca. La pulizia preserva così sia un presente leggibile sia il percorso delle correzioni.
