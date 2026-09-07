# Inventario del software

> Che cosa esiste materialmente sui dischi, dove sta e a che serve. La distinzione utile non è fra software gratuito e a pagamento ma fra ciò che entra nel workflow, ciò che resta come archivio e ciò che non va installato.
>
> Questa pagina è la vista d'insieme. L'inventario verificato del corredo `Progetto stanza (software)`, con il formato reale di ogni installer letto dai file invece che dedotto dal nome, il prefix di destinazione e le dipendenze, sta in [../10-ambiente/wine-corredo-progetto-stanza.md](../10-ambiente/wine-corredo-progetto-stanza.md). Dove le due pagine sembrano divergere, quella vale come fonte, perché nasce dall'ispezione diretta.

## Il corredo che entra nel workflow

Nativi Linux, già presenti o installabili dai repository di Ubuntu Studio: REW per la misura, Blender per la modellazione geometrica, GNU Octave con MATAA per l'analisi, FreeCAD per la progettazione meccanica. Nessuno di questi richiede Wine e nessuno richiede licenza.

Sotto Wine, con installer conservati nella cartella dei materiali del progetto: Akabak Pro versione 3.2.4 build 126 e VACS versione 2.1.3 build 33 nelle varianti a 32 e a 64 bit, numeri di versione confermati dall'autore nella corrispondenza, entrambi coperti dalla student license descritta nella pagina delle licenze, e VituixCAD 2. Il pacchetto degli esempi di Akabak, che pesa circa novanta megabyte, è il file più grande del corredo ed è materiale di lavoro, non documentazione, perché la fase 5 comincia adattando un esempio.

EASE Focus 3, nella versione 3.1.260, con il servizio di database AFMG e il database dei file GLL. Come discusso nella pagina della fase 2, il suo ruolo nel progetto è la verifica rapida di copertura, non la simulazione ambientale.

ARTA, nella versione 1.7.1. È shareware, e la cartella contiene soltanto l'installer ufficiale senza modifiche. Non era nel piano originale ed è stato promosso al gruppo da installare, perché è la via più diretta per produrre un file GLL da un diffusore misurato e quindi serve alla fase 8, quando il monitor autocostruito esiste e va caratterizzato. Fino a quel momento la misura la fa REW, nativo.

## Il materiale che resta come archivio

Le due versioni precedenti di EASE Focus, la 3.0.18 e la 3.1.10, con i rispettivi database di GLL e, per la 3.1.10, i progetti di esempio di un workshop. Non vanno installate: tre versioni dello stesso programma in tre prefix sono manutenzione senza ritorno, e la 3.1.260 le copre entrambe grazie alla retrocompatibilità dei GLL.

Il database di GLL del 2016, che contiene qualche centinaio di modelli di diffusori professionali di molti costruttori. È materiale di valore perché evita di cercare i file sui siti dei produttori uno per uno, e va conservato. Un dettaglio operativo importante: alcuni costruttori accompagnano il `.gll` con file `.dll` e `.bin`, e i tre devono restare nella stessa cartella o il modulo non si carica.

WinISD, distribuito solo a 32 bit. Come discusso nella pagina della fase 4, è ridondante rispetto a VituixCAD e Akabak, e non installarlo elimina il solo prefix Wine a 32 bit necessario al progetto. Resta archiviato.

Ramsete 27b, per l'acustica degli ambienti. L'ispezione ha accertato che è una applicazione Visual Basic 6, quindi a 32 bit e con bisogno del runtime `vb6run` in un prefix a 32 bit. Lo stato di licenza non è accertato: la cartella non mostra indizi di manomissione, ma è un prodotto commerciale e va verificato prima di installarlo, verifica tracciata come PA-002. La priorità è bassa, perché il suo ruolo è già coperto da Akabak.

## Il materiale che non va installato

Otto voci del corredo, per circa 1,7 GB, cioè quasi tre quarti del suo peso. Sette portano protezioni rimosse e una porta il file di provenienza da un servizio di condivisione: FineCone 2.1 con una cartella di modifica e una cartella `HASP`, che è l'emulazione della chiave hardware; FineMotor 2.5 con una cartella di modifica; LSPCad 5.25 e 6.32; Grenander Loudspeaker Lab 3.13; AmpliTube 3 con uno sbloccatore separato accanto all'installer; Guitar Rig 5 Pro dichiarato sbloccato nel nome; e POD Farm, che richiede in ogni caso una licenza Line 6.

Va corretta una affermazione che una versione precedente di questa pagina conteneva. Grenander Loudspeaker Lab era descritto come privo di cartella di modifica: l'ispezione diretta ha mostrato che accanto al suo installer c'è il file descrittivo di un gruppo di distribuzione illecita, quindi la voce appartiene a questo gruppo e non al precedente.

Non fanno parte del workflow documentato, non compaiono nel manifest di trasferimento e non esiste alcuna procedura di installazione per esse in questa documentazione. Vale notare che non ne serve nessuna: il ruolo di FineCone e FineMotor, cioè la simulazione a elementi finiti del cono e del motore magnetico, sta a monte del progetto di un diffusore e riguarda chi costruisce gli altoparlanti, non chi li assembla in un sistema partendo da driver finiti; il ruolo di LSPCad e di Grenander è coperto da VituixCAD, che è gratuito, molto più recente e gestisce direttività e risposta in potenza; gli emulatori di amplificatori non hanno relazione con la progettazione elettroacustica, e per il progetto gemello di home recording esistono equivalenti nativi liberi su Linux come Guitarix e Rakarrack.

La decisione è registrata come ADR-010.

## Hardware

Il processore è un Intel i7-6700 a 3.40 GHz, con 16 GB di RAM DDR4 e un SSD Crucial CT500P25SD8 da 500 GB, dato al 91 per cento di vita residua.

L'interfaccia audio è una Focusrite Scarlett 2i2 di seconda generazione, con alimentazione phantom a 48 V.

Il microfono di misura non è ancora acquistato. La scelta è il Dayton Audio EMM-6, con la Sonarworks SoundID Reference Mic come alternativa equivalente, per le ragioni discusse nella pagina della fase 1.

I driver non sono ancora acquistati, e la fase 6 discute i vincoli che ne condizionano la scelta.
