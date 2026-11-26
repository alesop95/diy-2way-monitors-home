# Fonti della ricognizione

Accesso del 26 novembre 2026. Le letture sono mirate ai passaggi indicati, senza promozione dell'intero sito o manuale. Le prove grezze dei repository e gli hash dei file consultati restano nel livello privato.

| ID | Tipo, autore e titolo | Versione e URL canonico | Passaggio letto e stato | Uso e limite |
|---|---|---|---|---|
| F1 | Prodotto ufficiale, AFMG, EASE SpeakerLab | Pagina corrente, [SpeakerLab](https://www.afmg.eu/en/ease-speakerlab) | Descrizione, importazione e licenze; contenuto-verificato | Authoring distinto dalla misura; nessuna prova di installazione |
| F2 | FAQ ufficiale, AFMG, installer Focus con propri GLL | [Autorizzazioni](https://www.afmg.eu/en/we-are-loudspeaker-manufacturer-can-we-get-installer-ease-focus-only-our-own-glls-it) | Note 1-2; contenuto-verificato | Vincolo per modello, non solo estensione del file |
| F3 | Manuale ufficiale, Ivo Mateljan, ARTA User Manual | 1.9.8, dicembre 2024, [PDF](https://www.artalabs.hr/download/ARTA-user-manual.pdf) | Sezione 9.16, pagine164-165; contenuto-verificato | Esportazione testuale, lettura parziale; non prova di exporter GLL |
| F4 | Sorgenti e release ufficiali, progetto Open Sound Meter | v1.5.2, commit1e08de2322f5e8849e1ba39e1d3993187a7cc75c, [release](https://github.com/psmokotnin/osm/releases/tag/v1.5.2) | LICENSE e src/source/stored.cpp, saveFRD/saveCSV/phase; contenuto-verificato | GPL3 e schema esportato; analisi statica, non esecuzione dell'app |
| F5 | Condizioni ufficiali, Open Sound Meter, EULA | 25 settembre 2026, [EULA](https://opensoundmeter.com/en/eula) | Sezioni2-4, distinzione versioni GPL precedenti; contenuto-verificato | Non estendere la licenza della release ai prodotti correnti |
| F6 | Repository del manutentore, Matthias S. Brennwald, MATAA | [Repository](https://github.com/mbrennwa/mataa) | README.txt e metadati licenza GPL2; contenuto-verificato | Alternativa GNU Octave prevista dal progetto; nessuna nuova acquisizione provata |
| F7 | Manuale del manutentore, Kimmo Saunisto, VituixCAD | 2.0.135.2, 25 aprile 2026, [manuale](https://kimmosaunisto.net/Software/VituixCAD/VituixCAD_help_20.html) | Supported response file types e Convert IR to FR; contenuto-verificato | Tre colonne FRD, unità; non attestazione della GUI installata |

Il recupero web della homepage ARTA e di alcuni URL raw/API ha avuto timeout o cache miss. Il PDF ufficiale ARTA è stato letto con lo strumento web. Per OSM e MATAA i file pubblici sono stati letti via HTTPS dal repository ufficiale; il primo tentativo nel sandbox era bloccato dal proxy, la ripetizione autorizzata è riuscita. Non si qualificano come letti i risultati di ricerca non aperti.

La scheda F7 conserva l'identificativo storico SRC-7E426029EF155B01 dello stesso URL nel registro canonico. La prima rigenerazione protetta ha segnalato che assegnare un nuovo ID eliminava il vecchio titolo; è stato mantenuto l'ID, senza forzare la guardia o perdere i rimandi. La lettura corrente resta limitata alle sezioni dichiarate, non promuove tutti gli usi storici a claim verificati.
