# Inventario del software

> Che cosa esiste materialmente sui dischi, dove sta e a che serve. La distinzione utile non è fra software gratuito e a pagamento ma fra ciò che entra nel workflow, ciò che resta come archivio e ciò che non va installato.

## Il corredo che entra nel workflow

Nativi Linux, già presenti o installabili dai repository di Ubuntu Studio: REW per la misura, Blender per la modellazione geometrica, GNU Octave con MATAA per l'analisi, FreeCAD per la progettazione meccanica. Nessuno di questi richiede Wine e nessuno richiede licenza.

Sotto Wine, con installer conservati nella cartella dei materiali del progetto: Akabak Pro versione 3.24 build 126 e VACS versione 2.13 build 33 nelle varianti a 32 e a 64 bit, entrambi coperti dalla student license descritta nella pagina delle licenze, e VituixCAD 2. Il pacchetto degli esempi di Akabak, che pesa circa novanta megabyte, è il file più grande del corredo ed è materiale di lavoro, non documentazione, perché la fase 5 comincia adattando un esempio.

EASE Focus 3, nella versione 3.1.260, con il database dei file GLL. Come discusso nella pagina della fase 2, il suo ruolo nel progetto è la verifica rapida di copertura, non la simulazione ambientale.

## Il materiale che resta come archivio

Le due versioni precedenti di EASE Focus, la 3.0.18 e la 3.1.10, con i rispettivi database di GLL e, per la 3.1.10, i progetti di esempio di un workshop. Non vanno installate: tre versioni dello stesso programma in tre prefix sono manutenzione senza ritorno, e la 3.1.260 le copre entrambe grazie alla retrocompatibilità dei GLL.

Il database di GLL del 2016, che contiene qualche centinaio di modelli di diffusori professionali di molti costruttori. È materiale di valore perché evita di cercare i file sui siti dei produttori uno per uno, e va conservato. Un dettaglio operativo importante: alcuni costruttori accompagnano il `.gll` con file `.dll` e `.bin`, e i tre devono restare nella stessa cartella o il modulo non si carica.

ARTA, nella versione 1.71, come software di misura alternativo a REW. Non è nel workflow principale, ma è la via più diretta per produrre un file GLL da un diffusore misurato, quindi diventa pertinente alla fase 8.

WinISD, distribuito solo a 32 bit. Come discusso nella pagina della fase 4, è ridondante rispetto a VituixCAD e Akabak, e non installarlo elimina il solo prefix Wine a 32 bit necessario al progetto. Resta archiviato.

Ramsete 27b, per l'acustica degli ambienti, mai valutato. Resta archiviato senza alcuna affermazione sulla sua idoneità.

## Il materiale che non va installato

Una parte del pacchetto ereditato di software per diffusori è costituita da copie con protezione rimossa. Riguarda FineCone 2.1 e FineMotor 2.5 di Loudsoft, LSPCad nelle versioni 5.25 e 6.32, e tre emulatori di amplificatori per chitarra, cioè AmpliTube 3, Guitar Rig 5 Pro e POD Farm, in versioni distribuite come sbloccate.

Non fanno parte del workflow documentato, non compaiono nel manifest di trasferimento verso la macchina Ubuntu e non c'è alcuna procedura di installazione per essi in questa documentazione. Vale notare che non ne serve nessuno: il ruolo di FineCone e FineMotor, cioè la simulazione a elementi finiti del cono e del motore magnetico, sta a monte del progetto di un diffusore e riguarda chi costruisce gli altoparlanti, non chi li assembla in un sistema; il ruolo di LSPCad è coperto da VituixCAD, che è gratuito e più recente; gli emulatori di amplificatori non hanno relazione con la progettazione elettroacustica.

Grenander Loudspeaker Lab 3.13 compare nello stesso pacchetto senza cartella di crack. Non è stato valutato e non serve al workflow.

## Hardware

Il processore è un Intel i7-6700 a 3.40 GHz, con 16 GB di RAM DDR4 e un SSD Crucial CT500P25SD8 da 500 GB, dato al 91 per cento di vita residua.

L'interfaccia audio è una Focusrite Scarlett 2i2 di seconda generazione, con alimentazione phantom a 48 V.

Il microfono di misura non è ancora acquistato. La scelta è il Dayton Audio EMM-6, con la Sonarworks SoundID Reference Mic come alternativa equivalente, per le ragioni discusse nella pagina della fase 1.

I driver non sono ancora acquistati, e la fase 6 discute i vincoli che ne condizionano la scelta.
