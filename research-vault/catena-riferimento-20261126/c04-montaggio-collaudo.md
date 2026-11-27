# Fonti per montaggio e collaudo, MS-328

Ricerca mirata il 27 novembre 2026. Quesito: quali precondizioni di misura preservano le quattro uscite indipendenti e il riferimento comune richiesto dalla somma? Perimetro: manuale del produttore per uscite a ponte e aiuto ufficiale REW per acquisizione ed export. Le note servono al protocollo, senza misure di apparecchi.

Query: `site:ti.com guidelines measuring audio power amplifier performance BTL differential input class D low pass measurement filter ground differential`, `site:roomeqwizard.com REW help acoustic timing reference same reference speaker phase impulse measurements time reference`, `site:roomeqwizard.com room eq wizard export measurement frequency response phase file mdat export`. Preferiti URL canonici senza parametri temporali o percorso beta.

| Fonte primaria | Copertura | Limite |
|---|---|---|
| [TI SLOA068A, Richard Palmer, revisione 2019](https://www.ti.com/lit/an/sloa068a/sloa068a.pdf) | Sezione 3.1, figura 2 e misura del rumore in figura 11. Il carico va fra i due terminali BTL e la lettura è differenziale. | Nota per amplificatori e moduli di valutazione. Non specifica un banco completo o un limite strumentale per i V3. Il filtraggio per le misure in classe D va scelto in funzione dello strumento e dell'uscita. |
| [REW, Making Measurements](https://www.roomeqwizard.com/help/help_en-GB/html/makingmeasurements.html) | Timing reference, loopback o riferimento acustico con posizione e offset espliciti. Richiede calibrazione e livelli adeguati. | Le misure differenziali dei V3 appartengono al banco elettrico. Un loopback temporale di linea non si collega ai morsetti di potenza. |
| [REW, File Menu](https://www.roomeqwizard.com/help/help_en-GB/html/file.html) | Salvataggio `.mdat`, Export measurement as text e Export impulse response as WAV. L'help descrive anche lo zero di fase per dati privi di quella misura. | Controllare versione usata, origine della fase, finestra, smoothing e griglia. Una colonna di zeri in un export può contenere segnaposto. |

Le scelte di progetto associabili a queste fonti sono nel [capitolo70](../../docs/70-realizzazione-e-verifica.md) e nella [scheda 70a](../../docs/70a-scheda-collaudo-a24.md). Volt, picchi e tempi vengono lasciati vuoti finché non esiste una lettura in condizioni dichiarate. I casi numerici precedenti verificano la pipeline, non le apparecchiature.
