# Fonti tracciate

> Registro della skill `citation-tracker`, tracciato. Una riga per fonte, con i tre stati: verificata, da verificare, scartata. Solo le verificate passano a `bib-sync` ed entrano in `research-vault/bibliography.bib`. I PDF stanno in `research-vault/papers/`, ignorata da git, con il nome del file uguale alla chiave più `.pdf`.

## Lotto di candidati 01, proposto il 2026-10-02 (MS-185) e riscontrato lo stesso giorno (MS-186)

L'utente ha confermato il piano e ha chiesto i collegamenti. I 24 candidati di MS-185 sono stati riscontrati da tre agenti con accesso al web, e i lavori pubblicati in più parti sono stati divisi, quindi le righe sono 29. I resoconti completi, con le discrepanze, stanno in `_notes/fonti-studio/verifiche-paper/`.

Il limite del riscontro va detto, perché decide lo stato. Le pagine della AES E-Library e di ASA hanno risposto 403 agli strumenti di recupero, quindi i numeri della E-Library e i metadati degli articoli AES vengono dai risultati di ricerca che riportano quelle pagine, non da una pagina AES aperta. Lo stesso vale per i documenti di IEEE Xplore, mentre i DOI di IEEE, ASA e MDPI sono riscontrati su Crossref o su OpenAlex. Per questo nessuna riga è ancora verificata: lo diventa quando l'utente scarica il PDF e se ne controllano titolo, autori e pagine.

Le correzioni rispetto alla proposta sono queste. Thiele 1971 è in due parti e Small 1973 in quattro. Olson è la ripubblicazione JAES del 1969 di un lavoro del 1950-51, e la chiave diventa `olson1969enclosures`. D'Appolito 1983 è un paper di convention, il numero 2000 della 74a. Olive viene da due convention distinte, la 116a e la 117a. La nota di Bristow-Johnson si cita nella versione W3C del 2021, curata da Raymond Toy, perché la data della nota originale non ha trovato una fonte primaria. Cecchi è uscito online nel dicembre 2017 nel volume 8 del 2018, come articolo 16.

Legenda di Dove: AES per la E-Library, IEEE per Xplore, ASA per JASA, OA per l'accesso aperto.

| Chiave e file | Fonte riscontrata | Dove | Collegamento | Stato |
|---|---|---|---|---|
| thiele1971vented1 | A. N. Thiele, Loudspeakers in Vented Boxes: Part 1, JAES 19(5), pp. 382-392, maggio 1971 | AES | elib 2173, nessun DOI: https://aes.org/publications/elibrary-page/?id=2173 | da verificare sul PDF |
| thiele1971vented2 | A. N. Thiele, Loudspeakers in Vented Boxes: Part 2, JAES 19(6), pp. 471-483, giugno 1971 | AES | elib 2163, nessun DOI: https://aes.org/publications/elibrary-page/?id=2163 | da verificare sul PDF |
| small1973vented1 | R. H. Small, Vented-Box Loudspeaker Systems Part 1: Small-Signal Analysis, JAES 21, pp. 363-372, 1973 (fascicolo non visto) | AES | elib 1967, nessun DOI: https://aes.org/publications/elibrary-page/?id=1967 | da verificare sul PDF |
| small1973vented2 | R. H. Small, Vented-Box Loudspeaker Systems Part 2: Large-Signal Analysis, JAES 21(6), pp. 438-444, agosto 1973 | AES | elib 1959, nessun DOI: https://aes.org/publications/elibrary-page/?id=1959 | da verificare sul PDF |
| small1973vented3 | R. H. Small, Vented-Box Loudspeaker Systems Part 3: Synthesis, JAES 21(7), pp. 549-554, settembre 1973 | AES | elib 1951, nessun DOI: https://aes.org/publications/elibrary-page/?id=1951 | da verificare sul PDF |
| small1973vented4 | R. H. Small, Vented-Box Loudspeaker Systems Part 4: Appendices, JAES 21, pp. 635-639, ottobre 1973 | AES | elib 1941, nessun DOI: https://aes.org/publications/elibrary-page/?id=1941 | da verificare sul PDF |
| leach2002inductance | W. M. Leach Jr., Loudspeaker Voice-Coil Inductance Losses: Circuit Models, Parameter Estimation, and Effect on Frequency Response, JAES 50(6), pp. 442-450, giugno 2002 | AES; manoscritto dell'autore | elib 11074, nessun DOI: https://aes.org/publications/elibrary-page/?id=11074 (copia libera: https://leachlegacy.ece.gatech.edu/papers/vcinduc.pdf) | da verificare sul PDF |
| vanderkooy1991diffraction | J. Vanderkooy, A Simple Theory of Cabinet Edge Diffraction, JAES 39(12), pp. 923-933, 1991 | AES | elib 5952, nessun DOI: https://aes.org/publications/elibrary-page/?id=5952 | da verificare, collegamento mancante |
| olson1969enclosures | H. F. Olson, Direct Radiator Loudspeaker Enclosures, JAES 17(1), pp. 22-29, gennaio 1969 | AES | elib 1609, nessun DOI: https://aes.org/publications/elibrary-page/?id=1609 | da verificare sul PDF |
| dappolito1983lobing | J. A. D'Appolito, A Geometric Approach to Eliminating Lobing Error in Multiway Loudspeakers, 74th AES Convention, paper 2000, ottobre 1983 | AES | elib 11762, nessun DOI: https://aes.org/publications/elibrary-page/?id=11762 | da verificare sul PDF |
| vanderkooy1984phase | J. Vanderkooy e S. P. Lipshitz, Is Phase Linearization of Loudspeaker Crossover Networks Possible by Time Offset and Equalization?, JAES 32, dicembre 1984; preprint alla 70th Convention, 1981, paper 1857 | AES | elib 11899, nessun DOI: https://aes.org/publications/elibrary-page/?id=11899; elib 11899 è il preprint della 70th Convention 1981, paper 1857; il numero della versione JAES 32(12) 1984 non è confermato | da verificare, collegamento incerto |
| regalia1987tunable | P. A. Regalia e S. K. Mitra, Tunable Digital Frequency Response Equalization Filters, IEEE Trans. ASSP 35(1), pp. 118-120, 1987 | IEEE | DOI 10.1109/TASSP.1987.1165037: https://doi.org/10.1109/TASSP.1987.1165037 | da verificare sul PDF |
| w3c2021eqcookbook | R. Bristow-Johnson, Audio EQ Cookbook, a cura di R. Toy, W3C Working Group Note, 8 giugno 2021 | OA | https://www.w3.org/TR/audio-eq-cookbook/ | da verificare sul PDF, stampando la pagina |
| bank2008parallel | B. Bank, Perceptually Motivated Audio Equalization Using Fixed-Pole Parallel Second-Order Filters, IEEE Signal Processing Letters 15, pp. 477-480, 2008 | IEEE; copia dell'autore | DOI 10.1109/LSP.2008.921473: https://doi.org/10.1109/LSP.2008.921473 (copia libera: http://www.mit.bme.hu/~bank/publist/spl08.pdf) | da verificare sul PDF |
| kirkeby1999inversion | O. Kirkeby e P. A. Nelson, Digital Filter Design for Inversion Problems in Sound Reproduction, JAES 47(7), pp. 583-595, 1999 | AES | elib 12098, nessun DOI: https://aes.org/publications/elibrary-page/?id=12098 | da verificare sul PDF |
| norcross2004inverse | S. G. Norcross, G. A. Soulodre e M. C. Lavoie, Subjective Investigations of Inverse Filtering, JAES 52(10), pp. 1003-1028, ottobre 2004 | AES | elib 13022, nessun DOI: https://aes.org/publications/elibrary-page/?id=13022 | da verificare sul PDF |
| radlovic2000robustness | B. D. Radlović, R. C. Williamson e R. A. Kennedy, Equalization in an Acoustic Reverberant Environment: Robustness Results, IEEE Trans. Speech and Audio Processing 8(3), pp. 311-319, maggio 2000 | IEEE | DOI 10.1109/89.841213: https://doi.org/10.1109/89.841213 | da verificare sul PDF |
| hatziantoniou2000smoothing | P. D. Hatziantoniou e J. N. Mourjopoulos, Generalized Fractional-Octave Smoothing of Audio and Acoustic Responses, JAES 48(4), pp. 259-280, aprile 2000 | AES | elib 12070, nessun DOI: https://aes.org/publications/elibrary-page/?id=12070 | da verificare sul PDF |
| cecchi2018review | S. Cecchi, A. Carini e S. Spors, Room Response Equalization: A Review, Applied Sciences 8(1), articolo 16, 2018 (online dicembre 2017) | OA | DOI 10.3390/app8010016: https://doi.org/10.3390/app8010016 | da verificare sul PDF |
| allen1979image | J. B. Allen e D. A. Berkley, Image Method for Efficiently Simulating Small-Room Acoustics, JASA 65(4), pp. 943-950, aprile 1979 | ASA; copia dell'autore | DOI 10.1121/1.382599: https://doi.org/10.1121/1.382599 (copia libera: https://jontalle.web.engr.illinois.edu/Public/Allen-pdf/AllenBerkley79.pdf) | da verificare sul PDF |
| toole2006review | F. E. Toole, Loudspeakers and Rooms for Sound Reproduction: A Scientific Review, JAES 54(6), pp. 451-476, giugno 2006 | AES | elib 13686, nessun DOI: https://aes.org/publications/elibrary-page/?id=13686 | da verificare sul PDF |
| olive2004preference1 | S. E. Olive, A Multiple Regression Model for Predicting Loudspeaker Preference Using Objective Measurements: Part I, Listening Test Results, 116th AES Convention, paper 6113, 2004 | AES | elib 12794, nessun DOI: https://aes.org/publications/elibrary-page/?id=12794 | da verificare sul PDF |
| olive2004preference2 | S. E. Olive, A Multiple Regression Model for Predicting Loudspeaker Preference Using Objective Measurements: Part II, Development of the Model, 117th AES Convention, paper 6190, 2004 | AES | elib 12847, nessun DOI: https://aes.org/publications/elibrary-page/?id=12847 | da verificare sul PDF |
| blauert1978groupdelay | J. Blauert e P. Laws, Group Delay Distortions in Electroacoustical Systems, JASA 63(5), pp. 1478-1483, 1978 | ASA | DOI 10.1121/1.381841: https://doi.org/10.1121/1.381841 | da verificare sul PDF |
| lipshitz1982audibility | S. P. Lipshitz, M. Pocock e J. Vanderkooy, On the Audibility of Midrange Phase Distortion in Audio Systems, JAES 30(9), pp. 580-595, settembre 1982 | AES | elib 3824, nessun DOI: https://aes.org/publications/elibrary-page/?id=3824 | da verificare sul PDF |
| rife1989mls | D. D. Rife e J. Vanderkooy, Transfer-Function Measurement with Maximum-Length Sequences, JAES 37(6), pp. 419-444, giugno 1989 | AES | elib 6086, nessun DOI: https://aes.org/publications/elibrary-page/?id=6086 | da verificare sul PDF |
| mueller2001sweeps | S. Müller e P. Massarani, Transfer-Function Measurement with Sweeps, JAES 49(6), pp. 443-471, giugno 2001 | AES | elib 10189, nessun DOI: https://aes.org/publications/elibrary-page/?id=10189 | da verificare sul PDF |
| struck1994freefield | C. J. Struck e S. F. Temme, Simulated Free Field Measurements, JAES, giugno 1994 (volume e pagine non riscontrati) | AES | elib 6937, nessun DOI: https://aes.org/publications/elibrary-page/?id=6937 | da verificare sul PDF |
| putzeys2005classd | B. Putzeys, Simple Self-Oscillating Class D Amplifier with Full Output Filter Control, 118th AES Convention, Barcellona, paper 6453, maggio 2005 | AES; copia dell'autore su Hypex, letta | elib 13169, nessun DOI: https://aes.org/publications/elibrary-page/?id=13169 (copia libera: https://www.hypex.nl/media/5c/19/2e/1682341812/Simple%20self-oscillating%20class%20D%20amplifier.pdf) | da verificare sul PDF |

Collegamenti riscritti il 2026-10-05 (MS-193): un solo collegamento canonico per fonte. Il formato `aes2.org/publications/elibrary-page/?id=` usato in MS-186 risponde 404, quindi per la AES vale `https://aes.org/publications/elibrary-page/?id=N`, che esiste ma è protetto da un controllo anti-bot.

## Verificate

Nessuna, al 2026-10-02.

## Scartate

Nessuna, al 2026-10-02.
