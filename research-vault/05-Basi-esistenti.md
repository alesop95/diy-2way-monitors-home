---
tipo: mappa
aggiornato: 2026-10-02
---
# Il lavoro già fatto

Tre basi esistevano prima di questa ricerca, e il registro parte da esse invece che da una proposta.

## La tesi magistrale del 2020

*Feature-based characterization of loudspeakers*, tesi magistrale dell'utente in Sound and Music Engineering. Il PDF su `J:` e quello del repository `E:\feature-based_characterization_loudspeakers` hanno la stessa impronta. Quattro woofer e quattro tweeter, test d'ascolto su intensità, bilanciamento timbrico e preferenza, tredici descrittori spettrali dalle misure anecoiche in asse, e un modello di regressione che predice i giudizi dalle misure. È il filone di Olive e di Toole che questo progetto riprende per giustificare l'obiettivo di direttività regolare.

La bibliografia ha 119 voci, estratte con `pdftotext` in `basi/tesi-2020-bibliografia.txt`. Il repository porta anche gli script MATLAB di estrazione delle feature e gli script di validazione statistica con ANOVA, riusabili nella fase di verifica.

## La libreria JabRef

`ELE_Technical_Library.bib`, trovata in `J:\_____da sistemare ancora`, ha 5676 voci inserite fra il 2013 e il 2016, con due proprietari dichiarati, per 1927 e 116 voci. È un elenco: i PDF che le voci richiamano non esistono su questa macchina, e l'utente ha confermato di non averli. I gruppi più numerosi sono Loudspeakers con 1066 voci, Signal processing con 916, Physics con 500, Acoustics con 267 e Mathematics con 215, mentre circa 2486 voci non hanno alcun gruppo. Il registro ne tiene 4986, cioè tutte tranne quelle con gruppi soltanto estranei al progetto. Diciassette delle 29 proposte dell'agente vi erano già.

## Il materiale di studio su J:

Censito in sola lettura il 2026-10-02 in tre file, `fonti-locali/censimento-A.md`, `censimento-B.md` e `censimento-C.md`, e ordinato in nove lotti nel piano `fonti-locali/piano-lotti.md`. Tutti e nove i lotti sono indicizzati dove stanno, con `tools/indicizza-lotti.py`, e i dieci archivi sono estratti in `J:\MAIN\_ESTRATTI ARCHIVI TESI` con `tools/estrai-archivi.py` (MS-189, MS-190, ADR-036). Il testo si converte da `J:` con `tools/converti-fonti.py`.

Torna a [[00-START]]
