# 9. Conservare fase, volume e provenienza nello stesso progetto

## Il punto di partenza

Il modello della cassa chiusa in [studio_sistema_audio.py](../../tools/studio_sistema_audio.py) era corretto nel suo perimetro. La funzione esprime un passa-alto del secondo ordine:

```python
scale = math.sqrt(1 + vas/vb)
z = 1j * np.asarray(frequency) / (fs*scale)
return z*z / (z*z + z/(qts*scale) + 1)
```

Questa forma non contiene un condotto. Aggiungere una seconda curva al grafico non basta a estenderla al reflex: cono e aria nel tubo sono accoppiati dalla pressione della cavità. Anche il volume occupato dal tubo cambia la cavità che ne determina l'accordo.

Il fronte geometrico aveva un limite analogo. Sei pannelli con il volume corretto dimostravano il contenitore esplorativo; non dimostravano tagli, incassi, rinforzo o spazio per i driver. Per proseguire serviva una rappresentazione che facesse incontrare il circuito, i dati di targa e il solido.

## La fase non è un accessorio del grafico

[acustica_cabinet.py](../../tools/acustica_cabinet.py) risolve il circuito per ammettenza. La scelta evita di dividere per un'impedenza infinita all'accordo ideale e restituisce contributi complessi, conservando la somma:

```python
cone = s*enclosure_admittance / denominator
port = -s*vent_admittance / denominator
return {'cone': cone, 'port': port, 'total': s*s/denominator}
```

Quel meno non descrive una diminuzione di livello. Descrive il verso della radiazione del condotto rispetto al movimento del cono. Sommando soltanto i moduli si perderebbe la cancellazione sotto accordo e si potrebbe scambiare per utile un'emissione che non esiste.

La prova che lo sorveglia è stata osservata rossa prima dell'implementazione. Dopo il verde è stata mutata la sola riga del condotto, invertendo il segno; la prova di somma è caduta. Il sorgente è poi tornato all'impronta precedente. Il caso Butterworth del quarto ordine fornisce un secondo controllo indipendente: l'atteso è una funzione analitica, non un altro passaggio nel medesimo circuito.

## Il condotto cambia il volume che lo fa accordare

Una lunghezza calcolata sul volume prima del tubo può non essere coerente col volume finale. Il programma risolve il sistema fra accordo e occupazione, sottraendo soltanto il tratto nella cavità. Il tratto nel pannello appartiene già al volume del legno e non viene contato due volte.

Questo lega una scelta acustica a un vincolo di fabbricazione. Una soluzione con buona estensione resta nel rapporto anche quando il tubo non entra, con la condizione geometrica negativa. Eliminarla dal calcolo prima di mostrarla toglierebbe al proprietario il motivo del rifiuto. I 108 scenari restano leggibili, compresi quelli sfavorevoli.

## Due motori per due domande

[progetto_cabinet.py](../../tools/progetto_cabinet.py) calcola analiticamente le sottrazioni di volume del frontale e del rinforzo. Il generatore FreeCAD costruisce invece i solidi con operazioni booleane e ne misura il risultato. I due metodi condividono gli input, ma non il procedimento con cui ottengono il volume.

La variazione della larghezza di 10 mm verifica che i parametri governino anche tagli e rinforzo. La riapertura del nativo controlla ciò che è stato salvato; la reimportazione STEP controlla il formato di scambio. Un raggio aumentato del due per cento produce un volume diverso e viene respinto. Il successo del processo FreeCAD da solo rimane insufficiente: nel primo tentativo il programma aveva conservato un errore di alias nel rapporto anche se il launcher non restituiva un fallimento utile.

Il disegno SB distingue inoltre diametro del cestello, telaio e cerchio dei fissaggi. La tabella unica in data/driver-geometria.json conserva questa distinzione: un centro di montaggio non viene trasformato nel foro pilota di una vite ancora da scegliere.

## La prova deve arrivare fino al file consegnato

Un manifesto creato dopo il collaudo può firmare un file cambiato nel frattempo. Il [generatore del kit](../../tools/consegna_completamento.py) controlla perciò gli hash registrati dal collaudo prima di costruire il nuovo manifesto. La prova altera una copia dello STEP e osserva il rifiuto prima della firma.

Lo stesso confine vale per il PDF: avere i byte del PDF non dimostra che rappresenti il Markdown corrente. Il kit riusa inspect_document per verificare anche le sorgenti dichiarate. La prova cambia l'impronta della sorgente e ottiene il rifiuto, pur lasciando intatto il PDF.

Questo pattern si estende ad altri risultati del progetto: conservare l'input, verificare l'uscita con un metodo indipendente e controllare che la copia consegnata sia ancora quella della prova. Non trasforma un modello in una misura fisica. È proprio la distinzione mantenuta fino al manifesto a permettere di proseguire lo sviluppo senza pretendere hardware o tagli già qualificati.
