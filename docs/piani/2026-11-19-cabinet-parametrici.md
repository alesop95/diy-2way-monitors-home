# Piano dei cabinet parametrici esplorativi

Esecuzione inline con executing-plans nell'autonomia esplicita dell'utente; nessun commit o push automatico.

Obiettivo: confrontare tre inviluppi plausibili sul ripiano nominale e produrre solidi a sei pannelli e distinte verificabili, senza congelare la scelta acustica. Architettura: configurazione JSON, matematica indipendente dal CAD, solidi nativi FreeCAD e profili 2D in CADCraft. Specifica: `docs/59-studio-ingombri-cabinet.md`.

## Vincoli

Ripiano nominale 1180 × 300 mm a quota 930 mm, rientranze non misurate. Pannelli ipotizzati 18 mm, margini 10 mm dichiarati; schermi esterni ipotizzati 540/620 mm. Nessun driver, foro o volume netto presentato come approvato. Ogni output nasce in una cartella nuova. Metodo di confronto e dimensioni devono essere leggibili da un clone senza dipendere da una chat.

## Task 1: configurazione e controllo geometrico

File: `config/cabinet/studio-st120.json`, `tools/studia_ingombri.py`, `tools/test_studia_ingombri.py`.

- [x] Provare prima i casi di riferimento: 0°, 90°, vecchio box fuori profondità, margini esatti e angolo negativo rifiutato.
- [x] Implementare footprint, pannelli, volume e posizione simmetrica delle facce; controllare l'intersezione degli assi dalle coordinate trasformate.
- [x] Generare rapporti JSON/CSV e tabella con larghezza schermo massima e volume lordo, senza una scelta automatica dei driver.

## Task 2: solidi e profili

File: `tools/genera-cabinet-freecad.py`; artefatti e prove in una cartella nuova.

- [x] Creare sei pannelli parametrici, verificare volumi e contatti e salvare FCStd.
- [x] Variare un parametro, osservare la ricomputazione, ripristinare e riaprire il documento.
- [x] Esportare e reimportare STEP verificando sei solidi, bounding box e volumi.
- [x] Generare profili 2D con CADCraft e misurare dimensioni e aree; indicare che mancano fresature e dettagli costruttivi.
- [x] Acquisire una vista del modello, ispezionarla e conservare anche il codice di uscita del processo.

## Task 3: consegna del risultato e revisione

- [x] Aggiungere risultati e limiti alla pagina 59, con comando replicabile e troubleshooting realmente incontrato.
- [x] Consolidare revisione e tracciamento: revisore separato bloccato dalla quota, verifica in prima persona dichiarata; kit copiato e verificato su Ubuntu, registro e ripresa aggiornati. I rilievi generali dei controlli restano distinti.

## Rischi da esercitare nelle prove

Angoli scambiati fra gradi e radianti devono essere rilevati dal riferimento a 30°. Un box che entra senza margine ma viola il margine dichiarato deve essere rifiutato. Il volume dei pannelli deve coincidere con esterno meno cavità; non basta contare sei oggetti. La posizione del centro baffle deve essere trasformata insieme alla scatola; usare solo il centro della bounding box falsa la distanza d'intersezione. Le tre scatole possono superare il rettangolo teorico senza dimostrare un appoggio sulle rientranze reali.

## Registro operativo

Ruling: usare FreeCAD per i solidi parametrici e CADCraft per i profili 2D. Motivo: capacità locali effettivamente interrogate e CAD FreeCAD già collaudato. Costo se errato: confronto fra due formati incoerenti; le dimensioni vengono controllate sulle uscite reimportate. La domanda di confronto della proposta resta aperta e non viene trasformata in approvazione dei componenti.

Ruling: revisione finale in prima persona perché l'avvio del secondo revisore è stato rifiutato dal controllo della quota (83%, riserva da 80%). Si aggiungono mille confronti dei vertici trasformati, incrocio volume FreeCAD/aree CADCraft e direzione delle viste. Costo: manca la seconda lettura indipendente del codice; questo limite resta esplicito nella consegna e non viene coperto dal numero delle prove.
