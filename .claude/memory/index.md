# Snapshot di sincronizzazione

## Stato corrente, 2026-11-26

Branch main, base dcb5e18. Chiusura di MS-319 eseguita dal proprietario e impronta verificata coerente il 25 novembre. Successivo mandato di completamento: correzione MS-320 sviluppata, piano docs/piani/2026-11-25-ricostruzione-da-sorgenti.md. La milestone attuale non è ancora committata. Un solo albero, nessun agente parallelo, nessun add/commit/push/deploy automatico.

La prova da archivio Git ha isolato risorse cercate soltanto in vecchi build: font nei generatori, CAD/PDF nei test del manifesto. Il verde di MS-319 valeva per quella postazione e non provava il clone. Ora tools/font_intrawelt.py risolve da argomento, ambiente, account o installazione; percorso esplicito incompleto rifiutato. Impronte delle risorse nelle figure, hash della dipendenza nel collaudo CAD. Nessun font installato o pubblicato. Le prove del manifesto usano fixture autonome di soli byte; non qualificano i formati CAD.

Otto suite del blocco: 42 test e nove subtest superati. Quattro prove eseguono davvero generatori e CADCraft da una copia senza vecchi build: quattro PDF scientifici, SVG confrontati, figura basso ricreata, dodici profili per ciascuna variante e contratti del kit senza CAD/PDF preesistenti; risorsa mancante rifiutata. Chiudi in sola verifica con «Controlli verdi», 39 comandi locali. Dopo l'ultima persistenza il rapporto da leggere è _notes/completamento-20261125/chiudi-ms320-finale.txt; proporre chiudi solo se anche quello termina verde.

## Progetto e consegna

Ingresso docs/STATO-PROGETTO.md; architettura e candidati in docs/63, completamento nominale e ricostruzione in docs/64, uso DSP in docs/61. Modelli invariati: 108 casi reflex, 27 angolari, 18 elettrici e tre geometrie. A24 chiusa/SB16 rimane base, SB15/B27 alternativa e C24 confronto. FreeCAD di MS-319 conserva sette solidi per variante, ricomputazione, riapertura e STEP verificati; sorgenti geometriche e nativi non sono stati modificati da MS-320. Tavole CADCraft rigenerate e rilette, prove negative incluse nelle suite.

Quattro PDF correnti con impronte e QA nel manifesto. Relazione64 di sei pagine: prime cinque identiche alla precedente ispezione per hash delle immagini, sesta vista; recap aggiornato e tavola A24 ispezionati. Quattro SVG del completamento e figura del basso correnti. Kit build/consegna-completamento-20261125.zip: 55 file e 2.444.936 byte verificati, manifesto durevole research-vault/completamento-20261125/consegna.json. L'artefatto in build è rigenerabile; non sostituisce i sorgenti e non arriva con un clone.

205 risorse, 38 schede curate, 167 riferimenti storici e catalogo di 177 file. Dieci approfondimenti didattici. Nessuna lettura bibliografica nuova in MS-320; la copertura di Small 1973 resta metadata/abstract. Originali e archivi preservati; 27 artefatti precedenti archiviati con verifica prima della sostituzione, 14 nuovi PNG QA rimossi con ricevuta. Banco sorgenti iniziale rimosso dopo verifica dell'archivio Git di 435 voci; temporaneo Craft e cache di test eliminati dopo autorizzazione e verifica dei percorsi. Non ripetere le pulizie storiche di MS-304/305.

## Residui e vincoli

Pendenze correnti soltanto in docs/PENDING-ACTIONS.md. Nel perimetro sviluppabile senza hardware restano le decisioni esecutive e di spesa, le fonti e le attività di altri progetti/template; non manca un nuovo blocco DSP o un generatore nominale. ADR-055 sospende senza scadenza foto, misure, collegamenti, ascolto, tagli, appoggi e prototipo. Fissaggi, cablaggio, tolleranze e giunzioni esecutive dipendono dai componenti e dai riscontri differiti. Nessuna prestazione acustica o potenza continua dedotta dalle prove software.

Pannello installato/verificato in MS-317: 24 file, HTTP200, zero riavvii; avvio automatico disabled alla prova. Enable al login resta manuale. Nessun runtime audio riconfigurato; non ripetere setup, banco DSP, backup o reboot. PA-042 resta manuale, sette lezioni per il template aperte; ricevuta personale MS-307 solo nella ripresa privata. Nessun contenuto aziendale importato.

Roadmap rigenerata: 26 voci aperte, nessuna chiusa dalla misura. Gate pacchetti ancora senza risposta: template99b13ff, 107 voci mai viste e undici presenze non registrate; nessuna adozione/installazione dedotta, ADR-031 valida. Rapporto vulnerabilità assente, sicurezza non verificata. Quattro ancore di contesto non avanzate senza riesame completo: STACK/deployment/roadmap 0d95d2e, current-work cf17718; struttura senza difetti, avvisi conservati.

Due GRC preesistenti riservati al template, esclusi da COMMIT-SCOPE. Messaggio proposto e ripresa pronti nel livello privato; il proprietario esegue chiudi e conferma il perimetro. Nessuna nuova impronta registrata prima del suo commit/push. Le decisioni e i risultati sono su disco, non affidati alla chat.
