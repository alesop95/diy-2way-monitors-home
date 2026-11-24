# Risultato del confronto

La scelta attuale è crossover attivo digitale sul PC disponibile, non esclusione definitiva di Raspberry Pi. PC e Pi possono ospitare lo stesso modello di elaborazione, ma la migrazione richiede I/O, collegamento della DAW, gestione del clock e prova del carico. Il Raspberry non serve per poter usare CamillaDSP; può servire per un requisito futuro di autonomia. Fonti S2/S6 e decisioni P1 del [registro](sources.md).

L'analogico attivo può realizzare il medesimo LR4 ideale. Il modello mostra somma a modulo unitario, ma non fase lineare. Componenti, Q e guadagni devono essere progettati; la forma Sallen-Key con componenti uguali non è Butterworth a guadagno unitario. Fonti S1/S4/S5/S7 e derivazioni del [dossier](../../docs/62-confronto-crossover-e-verifica-matematica.md).

Il doppio uso mix/ascolto è una possibilità del sistema acustico e dei profili, non un'esclusiva del digitale. Un fattore EQ comune ai rami preserva il loro rapporto complesso nelle ipotesi lineari. Il digitale rende pratici richiamo e ripetibilità, ma non aumenta gratuitamente SPL, escursione o risposta in basso. La dimostrazione è sul modello; le prestazioni dei monitor sono ancora da misurare.

Su 8194 frequenze, le uguaglianze ideali passano entro 1e-9; l'errore massimo di modulo della somma digitale è circa 9,11e-15. Le prove con polarità invertita e mezzo periodo di ritardo producono il nullo previsto al crossover. Un ritardo equivalente a 20 mm, a 2 kHz e c=343 m/s, dà -0,596456 dB nel modello a livelli uguali. Questi sono calcoli deterministici, non prove dei driver.

La scelta operativa resta iniziare dal PC già collaudato e decidere sull'eventuale host dedicato dopo requisiti, consumi, latenza e costo della catena completa. Non sono stati installati nuovi servizi o filtri. Fonte Linkwitz Lab promossa a prioritaria per richiesta esplicita dell'utente; letture e limiti nella [scheda](../web/linkwitzlab-active-filters.md).
