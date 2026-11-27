# Scheda di montaggio e collaudo A24

Modello da compilare nel livello privato dopo la riapertura delle verifiche fisiche. La [sequenza di montaggio e collaudo](70-realizzazione-e-verifica.md) definisce i passi e i criteri. Lasciare «non eseguita» fino a una prova con data, condizioni, criterio ed evidenza. Nella copia privata si possono annotare identificativi degli esemplari e dei dispositivi.

| Fase | Esito | Revisione o evidenza | Responsabile e data |
|---|---|---|---|
| A. Scelta e preventivo | Non eseguita | | |
| B. Prova a secco e montaggio | Non eseguita | | |
| C. Cablaggio scollegato | Non eseguita | | |
| D. Banco elettrico | Non eseguita | | |
| E. Acquisizione e taratura | Non eseguita | | |
| F. Verifica finale | Non eseguita | | |

## A-B. Dalla distinta al mobile

| Campo | Dato o prova |
|---|---|
| Variante del retro, luce fra bordo e parete, modalità di sgancio | |
| Spazio di appoggio reale, sagoma del ripiano, larghezza disponibile per lo schermo | |
| Sigle effettive di driver, connettori, finali e alimentatori | |
| Tavola approvata, revisione, data, tolleranze e autorizzazione | |
| Sezione, guaina e lunghezza dei cavi, percorso e ansa di servizio | |
| Misure a secco: diagonali, profondità, incassi e punti di appoggio | |
| Fissaggi, tenuta, giunzioni, estrazione della piastra e corridoio HF | |

## C. Continuità delle coppie indipendenti

| Via | Uscita UMC1820 | Ingresso finale | Coppia e poli | Continuità e polarità |
|---|---|---|---|---|
| Woofer L | L05 | V3 LF L | P05 → cassa L 1+/1- | |
| Tweeter L | L06 | V3 HF L | P06 → cassa L 2+/2- | |
| Woofer R | L07 | V3 LF R | P07 → cassa R 1+/1- | |
| Tweeter R | L08 | V3 HF R | P08 → cassa R 2+/2- | |

Registrare prova dei sei abbinamenti fra contatti distinti per cassa e verifica dal telaio. Allegare lettura a puntali corti, fondo a puntali aperti e stato dei due capi. Per le linee TRS-RCA indicare D/I, terminazione, esito dei tre contatti e riferimenti ai file di prova.

## D. Banco elettrico

Compilare una copia della tabella per ogni combinazione di host, ingresso e frequenza di campionamento. Allegare matrice quattro per quattro delle tensioni sulle quattro uscite a ogni stimolo. Annotare stimolo, banda, impostazioni dello strumento, portate differenziale e di modo comune, risoluzione, limiti termici, durata e rumore di fondo.

| Coppia | Carico e potenza ammessa | Livello rilevato e guadagno | Limite operativo concordato e relativo fondamento | Traccia |
|---|---|---|---|---|
| P05 | | | | |
| P06 | | | | |
| P07 | | | | |
| P08 | | | | |

| Prova | Evidenza e criterio di passaggio | Esito |
|---|---|---|
| C-01 D/I | Risposta a pari livello ricevuto, rumore, eventuale ronzio e margine prima del clip | |
| Identità e clock | Host USB attivo, linea selezionata, rate e rilettura della mappa | |
| Cuffie 3/4 | Percorso a banda intera indipendente e livello annotato | |
| Protezioni | Passa-alto HF, margine elettrico e protezione locali coerenti con la catena | |
| Mute e arresto | Transitorio, livello a regime, volume iniziale e segnali sulle quattro coppie | |
| Guasti | Perdita clock, sorgente o servizio e nuova preparazione esplicita | |

## E-F. Acquisizione e consegna

Per ogni direzione o posizione riportare due curve acquisite con riferimenti comuni. Duplicare la riga per gli esemplari e le direzioni effettive. Allegare `.mdat`, calibrazione, curve e impostazioni REW. Indicare quali elementi e filtri fossero già inseriti nella catena. Una curva simulata va riconoscibile dal relativo rapporto.

| Esemplare e direzione | Distanza e finestra | Eccitazione e riferimento di tempo | Banda e qualità valide | File e impronte |
|---|---|---|---|---|
| Woofer e tweeter a pari posizione | | | | |
| Misura diretta combinata | | | | |
| Punto di ascolto | | | | |

| Voce finale | Dato o prova |
|---|---|
| Profilo approvato, hash, frequenza, latenza e margine per via | |
| Destinazione dei due preset, limiti e protezione HF | |
| Autonomia con PC spento e stati di arresto/ripartenza | |
| Bersaglio, riferimento comune, direzioni, scostamento e banda coperta | |
| Esiti fuori specifica, interventi e prova da ripetere | |
| Cartella della consegna con disegni, distinta, misure, profili e rapporti | |
