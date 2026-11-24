# Amplificatore EKO per basso: identificazione e sostituzione altoparlante

L'utente dichiara il 2026-11-18 di possedere un vecchio amplificatore EKO per basso che richiede la sostituzione dello speaker. Il 2026-11-20 fornisce il manuale scansionato e precisa di avere la versione da 30 W, con un suono che descrive come rotto. Il lavoro sarà seguito dal contatto già individuato per il progetto dei due vie. L'ipotesi di guasto allo speaker è registrata come sospetto dell'utente, non come diagnosi già eseguita.

## Manuale acquisito e identificazione

La fonte è XL, XB-Series Amplifications Operating Instructions: undici pagine PDF, copertina con copyright 2001 Philipson Research Co., Ltd. La data editoriale non dimostra l'anno di costruzione dell'esemplare. Il manuale comprende più combo per chitarra e basso: la copertina mostra un modello per chitarra, ma non identifica il modello posseduto. Nella tabella dei bassi la versione da 30 W è XB30. Questa è la corrispondenza documentale con la dichiarazione dell'utente; pannello e targhetta fisici restano da riscontrare.

Il sommario rimanda anche alle informazioni di garanzia a pagina stampata 11; il file ricevuto termina con le specifiche alla pagina stampata 10. La lettura copre la scansione disponibile, senza dichiarare completa l'edizione originale. Le pagine necessarie per i dati XB30 sono presenti.

La scansione non conteneva testo estraibile. PdfCraft 0.21.1 ha prodotto l'OCR delle undici pagine, 2555 parole riconosciute; il testo dei controlli è stato letto e le immagini di copertina, comandi XB30/XB50 e specifiche sono state ispezionate. La tabella, ruotata nella scansione, non era leggibile nell'OCR: i valori seguenti provengono dal riscontro dell'immagine, non da quel testo automatico.

| Voce | Dato del manuale per XB30 | Posizione |
|---|---|---|
| Potenza d'uscita | 30 W, condizioni dichiarate 8 Ω, 1 kHz, 1% THD | Pagina PDF 11, stampata 10 |
| Altoparlante previsto | Uno da 10 pollici, 8 Ω | Pagina PDF 11, stampata 10 |
| Quote tabellari | 405 × 300 × 458, ordine larghezza × profondità × altezza; interpretazione in millimetri da riscontrare fisicamente, unità non esplicita nella riga | Pagina PDF 11, stampata 10 |
| Peso dichiarato | 13,5 kg | Pagina PDF 11, stampata 10 |
| Compressione | Interruttore IN/OUT e soglia regolabile | Pagina PDF 10, stampata 9 |
| Controlli principali | Master Volume; Bass, Low Mid, Hi Mid, Treble | Pagina PDF 10, stampata 9 |
| Altri collegamenti | Mic Input e relativo volume, ingresso CD RCA, Line Out e Phones da 1/4″ | Pagine PDF 10 e 11 |
| Uscita cuffie | Il manuale dichiara il silenziamento dello speaker interno quando si usano le cuffie | Pagina PDF 10, stampata 9 |

THD indica la distorsione armonica totale.[^thd] Non si estende la potenza dichiarata a condizioni diverse da quelle scritte. Il testo descrive Line Out con livello circa 0 dB, senza specificare la grandezza di riferimento: non si assume automaticamente dBu o dBV, né si ricostruisce lo schema dal nome del jack. La pagina dei controlli menziona Line Out sia nel pannello sia come connessione posteriore; la posizione effettiva va verificata sul nostro esemplare.

La fonte ha ID permanente `SRC-EKO-XL-XB-USER-PDF`, SHA-256 `deb488a55acd73426ec69a89eb802312ed4ad6640dfc3831e4fdda01dd7e5a21`. Originale acquisito e impronta coincidenti, conservati nel livello privato; il PDF fornito sul disco dell'utente non è stato modificato o eliminato. Il manuale d'uso non fornisce sigla del ricambio originale, parametri di Thiele-Small, volume interno o schema elettrico.

[^thd]: Total Harmonic Distortion; il manuale usa questa condizione per la potenza d'uscita.

## Ripetere la lettura della copia locale

Sequenza eseguita su Windows, nella radice del progetto. La copia originale privata deve già essere stata acquisita e verificata; questi comandi non modificano il PDF esterno. L'output OCR esistente va conservato prima di una nuova corsa oppure si usa una nuova directory di output.

```powershell
cd E:\diy-2way-monitors-home
& 'C:\Program Files\PdfCraft\pdfcraft-cli.exe' info '_notes/fonti-amplificatori/eko-basso-manuale-originale.pdf'
& 'C:\Program Files\PdfCraft\pdfcraft-cli.exe' batch '_notes/fonti-amplificatori/eko-basso-manuale-originale.pdf' --steps ocr --out-dir '_notes/fonti-amplificatori/eko-ocr-20261120' --dpi 80 --language en --ocr-all-pages --stop-on-error
& 'C:\Program Files\PdfCraft\pdfcraft-cli.exe' text '_notes/fonti-amplificatori/eko-ocr-20261120/eko-basso-manuale-originale.pdf'
& 'C:\Program Files\PdfCraft\pdfcraft-cli.exe' render '_notes/fonti-amplificatori/eko-basso-manuale-originale.pdf' --page 11 --dpi 45 --out '_notes/fonti-amplificatori/eko-basso-pagina-11-lettura.png'
```

Caso osservato il 2026-11-20: l'estrazione iniziale restituiva soltanto separatori di pagina perché la scansione era priva di livello testuale. L'OCR con lingua it è stato rifiutato: questa CLI supporta en, appropriata al manuale inglese. L'OCR completato ha comunque fallito semanticamente sulla tabella ruotata: il rimedio è la lettura dell'immagine, non l'adozione dei numeri riconosciuti automaticamente. Il rapporto privato `eko-basso-acquisizione-20261120.json` conserva provenienza, impronta ed evidenze.

## Diagnosi prima del ricambio

Il sintomo è descritto dall'utente; nessuna prova sul combo è stata ancora eseguita. Non si deduce il componente guasto dalla sola età o dalla distorsione udita. La sequenza seguente è un piano per il tecnico, non una procedura già collaudata. Va conservato lo speaker rimosso finché la diagnosi non è conclusa, per poter distinguere guasto originale e incompatibilità del ricambio.

| Passaggio da eseguire | Che cosa distingue | Limite dell'inferenza |
|---|---|---|
| Riscontro di targhetta, pannello e sigla dello speaker | XB30 effettivo, revisioni e possibili sostituzioni precedenti | Il manuale da solo non identifica ciò che è montato oggi. |
| Ispezione a macchina scollegata di cono, sospensioni, griglia, fissaggi e cabinet | Danni visibili e vibrazioni meccaniche estranee al trasduttore | Non esclude un difetto del finale o della bobina. |
| Sorgente e cavo noti, livello basso, equalizzazione senza enfasi e compressore escluso | Distorsione presente già in condizioni di piccolo segnale o legata alla sorgente | Non identifica da sola preamplificatore, finale o speaker. |
| Confronto con cuffie e Line Out, a livelli compatibili da verificare | Possibile localizzazione del sintomo lungo la catena | Una linea pulita non assolve il finale; una cuffia pulita non prova da sola il guasto dello speaker senza schema del prelievo. |
| Prova incrociata controllata dal tecnico di amplificatore e trasduttore | Se il difetto segue lo speaker oppure rimane nell'elettronica/cabinet | Richiede carico corretto, connessioni e protezioni; nessun collegamento dello speaker all'ingresso della scheda audio. |

L'acquisto dello speaker viene dopo la diagnosi. Per lo XB30 documentato si parte da un 10″ nominale 8 Ω, verificando sull'esemplare impedenza, fissaggi, foro e profondità. Non si passa a 4 Ω per aumentare la potenza: il manuale fornito non qualifica quel carico. La potenza sopportata dal ricambio non basta per decidere; occorrono sensibilità, escursione e comportamento nel cabinet. Un trasduttore con watt dichiarati maggiori può comunque dare meno livello o una risposta peggiore nell'involucro esistente.

## Dati ancora necessari

| Dato da acquisire | Perché serve |
|---|---|
| Targhetta e modello dell'amplificatore | Confermare XB30 e revisione, quindi cercare lo schema corrispondente |
| Sigla e impedenza nominale dello speaker | Scegliere il carico elettrico compatibile; la sola resistenza continua non identifica tutta l'impedenza |
| Diametro esterno, foro, fissaggi e profondità utile | Verificare la sostituzione meccanica prima dell'acquisto |
| Tipo e volume del cabinet, eventuale condotto | Valutare il comportamento del trasduttore nell'involucro esistente |
| Uso e risultato desiderato | Stabilire risposta, livello utile e compromesso fra costo e prestazione |
| Stato del cono e verifica del guasto con il tecnico | Definire l'intervento effettivo e confrontare sostituzione e riparazione |

Il preventivo confronterà diagnosi/riparazione e sostituzione compatibile, prima dell'ordine. Nessun ricambio è stato scelto, nessun prezzo attribuito e nessuna misura eseguita. Il fronte rimane PA-039: identificazione fisica, diagnosi, quote del mobile e poi confronto dei ricambi. L'integrazione home recording potrà studiare microfono e Line Out come risposte di sottosistemi differenti, senza confondere l'uscita di linea con l'uscita di potenza.
