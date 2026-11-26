# Caratterizzazione aperta: dai file al confronto verificabile

Stato del 26 novembre 2026. Il nuovo modulo [caratterizzazione.py](../tools/caratterizzazione.py) importa risposte numeriche, conserva gli input e confronta una banda e direzioni dichiarate. Non acquisisce audio, non modifica CamillaDSP e non qualifica l'hardware. Le verifiche fisiche restano sospese per ADR-055. La ricerca che istruisce PA-014 è nel [brief](../research-vault/caratterizzazione-aperta-20261126/brief.md), con [fonti e copertura](../research-vault/caratterizzazione-aperta-20261126/sources.md).

## Misura, file di confronto e modello GLL

Alla verifica odierna [AFMG presenta SpeakerLab](https://www.afmg.eu/en/ease-speakerlab) come authoring GLL a licenza commerciale. Per Focus i modelli richiedono [autorizzazione](https://www.afmg.eu/en/we-are-loudspeaker-manufacturer-can-we-get-installer-ease-focus-only-our-own-glls-it). Il limite non si risolve acquistando una licenza di misura: acquisizione e compilazione sono passaggi distinti.

Il [manuale ARTA 1.9.8](https://www.artalabs.hr/download/ARTA-user-manual.pdf), sezione 9.16, documenta export testuali. Qui si usa questa possibilità come punto di ingresso, senza attribuire ad ARTA un exporter GLL non dimostrato. GNU Octave e [MATAA](https://github.com/mbrennwa/mataa) restano una strada libera prevista dal progetto; nessuna nuova installazione o acquisizione è stata eseguita.

L'analisi locale dei file non richiede GLL. Non produce però una sfera di direttività, un CLF, un modello EASE autorizzato o la risposta della stanza. Le cinque direzioni dell'esempio servono al controllo dei dati; non coprono un modello spaziale completo.

## Formati ammessi e fase

| Formato nel manifesto | Colonne e delimitatore | Comportamento |
|---|---|---|
| frd | Frequenza Hz, modulo dB, fase opzionale in gradi; spazio, tab o punto e virgola | Due o tre colonne coerenti in tutto il file; decimale punto |
| osm_frd | Frequenza, modulo, fase in gradi, coerenza; spazio o tab | Quattro colonne, senza scartare quella della coerenza |
| osm_csv | Gli stessi quattro campi, separati da virgola | Decimale punto; valori mancanti o asterischi rifiutati |

Sono ammessi BOM UTF-8, righe vuote e commenti iniziali con cancelletto, asterisco o punto e virgola. Frequenze non positive, non finite, duplicate o disordinate sono rifiutate; anche colonne incoerenti e coerenza fuori [0,1]. Non vengono indovinati separatori locali, riordinate righe o sostituiti valori mancanti.

Il [manuale VituixCAD 2.0.135.2](https://kimmosaunisto.net/Software/VituixCAD/VituixCAD_help_20.html) documenta il FRD a tre colonne. L'export canonico del modulo segue quella struttura quando la fase esiste. Senza fase produce soltanto il CSV di analisi, lasciando il campo vuoto: zero gradi sarebbe un dato diverso. Il CSV conserva anche la coerenza; gli input originali rimangono nel pacchetto. La compatibilità verificata è strutturale e tramite roundtrip del parser locale, non una prova della GUI di VituixCAD.

Per OSM si è esaminato il [sorgente v1.5.2](https://github.com/psmokotnin/osm/blob/1e08de2322f5e8849e1ba39e1d3993187a7cc75c/src/source/stored.cpp). Gli export usano la fase memorizzata e possono omettere valori zero; non si assume che includano le correzioni di fase dell'app. È analisi statica, non collaudo runtime. La [release GPL3](https://github.com/psmokotnin/osm/releases/tag/v1.5.2) è distinta dalle offerte cui si applicano le [condizioni del settembre 2026](https://opensoundmeter.com/en/eula).

## Che cosa significa il confronto

Il manifesto dichiara unità, provenienza, riferimento di livello comune, banda, tolleranza, salto massimo della griglia in ottave e direzioni richieste. Il riferimento non viene ricavato separatamente da ogni curva: così una perdita fuori asse rimane visibile. La fase è conservata, senza ricavare fase minima o modificare ritardo e polarità.

Agli estremi della banda si interpola il modulo rispetto al logaritmo della frequenza, soltanto quando i dati li comprendono. Si controllano tutti i campioni interni e gli intervalli originali che intersecano la banda, compresi quelli che la attraversano ai bordi. Una griglia troppo rada produce insufficient_coverage. La soglia di 1/12 di ottava dell'esempio è una scelta dell'esecutore modificabile nel manifesto, non una garanzia metrologica.

Se è dichiarata valid_range_hz, il bersaglio deve ricadervi. La presenza di bin numerici non prova da sola la validità fisica: vanno documentati catena di misura, calibrazione, finestra e riferimento temporale. Anche un dataset etichettato measured mantiene hardware_qualified falso. La coerenza è controllata quando disponibile; se manca il rapporto restituisce null, non una qualità presunta.

| Stato della curva | Significato |
|---|---|
| within_bounds | I campioni e gli estremi interpolati soddisfano i limiti numerici dichiarati |
| outside_bounds | Almeno un punto supera il limite |
| insufficient_coverage | Banda, intervalli o validità dichiarata insufficienti |
| low_coherence | Dati disponibili sotto la soglia di coerenza dichiarata |

Lo stato complessivo è incomplete se manca una direzione richiesta o la copertura è insufficiente. Direzioni aggiuntive vengono analizzate ma non ridefiniscono la finestra richiesta. Non viene garantito il comportamento tra campioni o nella stanza.

## Esempio sintetico e risultato osservato

Il [dataset versionato](../data/caratterizzazione-demo/README.md) contiene cinque curve da 241 campioni ciascuna. Sono formule di prova, non simulazioni dei candidati SB né misure del prototipo. Il [rapporto versionato](../research-vault/caratterizzazione-aperta-20261126/risultati-esempio.json) permette di confrontare input, codice e risultato. L'ultima direzione contiene una valle intenzionale.

| Curva | Direzione | Massimo scostamento assoluto dB | Esito |
|---|---|---:|---|
| axial | In asse | 0,25000 | within_bounds |
| h_neg10 | Orizzontale -10° | 1,20000 | within_bounds |
| h_pos10 | Orizzontale +10° | 1,40000 | within_bounds |
| v_neg10 | Verticale -10° | 1,25000 | within_bounds |
| v_pos10 | Verticale +10° | 3,29644 | outside_bounds |

Il pacchetto osservato conserva 17 file firmati più il manifesto: copie degli input, rapporto, cinque CSV e cinque FRD. L'esecuzione è riuscita; il bersaglio sintetico complessivo non è rispettato. Sono due verdetti diversi, mostrati separatamente anche da --check.

## Sequenza replicabile eseguita

Su Windows con Python e NumPy già disponibili, dalla radice del repository. La prima generazione richiede una cartella nuova. Nel workspace consegnato esiste già: per ripetere la verifica si usa il secondo comando, senza sovrascriverla.

```powershell
cd "E:/diy-2way-monitors-home"
python tools/caratterizzazione.py --manifest data/caratterizzazione-demo/manifest.json --out build/caratterizzazione-20261126
python tools/caratterizzazione.py --manifest data/caratterizzazione-demo/manifest.json --out build/caratterizzazione-20261126 --check
python tools/test_caratterizzazione.py
```

Il codice di uscita zero indica generazione riuscita o pacchetto coerente, non conformità del diffusore. Il comando di check mostra anche data_status e hardware_qualified. Una firma diversa, un file inatteso o modificato fanno fallire il check. Una nuova generazione in una cartella esistente è rifiutata per conservare il lavoro umano.

Il manifesto e le curve devono stare nello stesso albero del dataset. I percorsi vengono risolti e verificati prima della lettura; non possono uscire tramite parent directory o collegamenti. Per il confronto si usano gli stessi byte di cui si registra l'hash, conservati in inputs. Anche codice e versione NumPy sono dichiarati nel rapporto.

## Errori incontrati e corretti

La prima implementazione considerava soltanto i segmenti dopo il taglio agli estremi: un intervallo grande che attraversava il bordo poteva risultare nascosto. Le prove con lacuna al limite inferiore e superiore hanno riprodotto il falso within_bounds; ora si controllano gli intervalli originali interessati.

Un percorso con prefisso punto veniva scritto correttamente dal filesystem ma confrontato con una chiave diversa nel manifesto. La prova ha riprodotto il fallimento del proprio check; i percorsi relativi sono ora normalizzati, senza rendere lecita una risalita o un collegamento esterno. Manifesti con forma errata sono rifiutati prima di generare output.

La mutazione che normalizzava ogni curva alla propria media ha fatto fallire la prova dell'attenuazione fuori asse. Il sorgente è stato ripristinato all'hash precedente. Le altre prove esercitano parsing, fase, coerenza, copertura, direzioni, conservazione del lavoro umano e alterazioni prima del check. Nessuna di esse apre hardware audio.
