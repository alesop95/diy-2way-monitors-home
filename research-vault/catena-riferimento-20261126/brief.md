# Sintesi tecnica della catena, MS-323

Il proprietario conferma i V3 per priorità al costo, ADR-058. La base esistente rimane coerente per proseguire: una UMC1820 a host alternativo PC/Pi, due SB16 e due SB26 in A24 chiusa, due finali stereo esterni e microfono XLR candidato. Il numero di ingressi soddisfa il requisito nominale degli otto ingressi di home recording; cuffie e quattro vie hanno percorsi distinti. È una scelta di sviluppo, non una qualifica degli apparecchi. Fonti e coperture in [sources.md](sources.md), proposta operativa nel [capitolo67](../../docs/67-catena-di-riferimento-e-dipendenze-esecutive.md).

## Evidenze e decisioni motivate

T1/T2 confermano nominalmente cuffie su playback3/4 e linee separate. La mappa di progetto5/6/7/8 coincide con gli indici simulati4/5/6/7 delle configurazioni, ma l'associazione ALSA fisica non è misurata. Il Main analogico non è il volume comune di queste quattro vie. Il cambio host e il cambio clock restano sequenze distinte, con attesa silenziata; nessun ramo bypassa il DSP.

T3/T4 mantengono i due driver della base A24 e i relativi ingombri. Non emerge una ragione documentale per cambiare le fresature nominali. Il prezzo basso dello SB16 e il maggiore prodotto area/corsa rispetto all'alternativa già modellata sostengono il mantenimento della base; non provano qualità sonora o target nella stanza. La potenza del tweeter ha una condizione di filtro di prova e non è un limite operativo direttamente applicabile.

T5 mantiene il V3 stereo come base economica; i collegamenti RCA sono un vincolo distinto dalla compatibilità di carico nominale. Un cavo TRS-RCA non viene congelato senza stabilire come terminare l'uscita bilanciata e senza qualificare livello/rumore. T7 offre un'alternativa con ingresso bilanciato: due A800 costano160 euro in più ai prezzi visualizzati e richiedono più spazio. Non si deduce un vantaggio acustico o una protezione del tweeter dal solo connettore.

T6 consente di specificare Pi4 con alimentazione ufficiale e accessori; la scelta2GB è di risorse, non un benchmark. T8 conferma il portale del microfono; file individuale e riferimento SPL assoluto restano da qualificare. Nessuna lettura riuscita del PDF Dayton viene dichiarata.

## Budget e lacune

I prezzi P1-P5 producono un subtotale di587,25 euro per interfaccia, quattro driver, due V3 completi e microfono. Aggiungendo i lotti stimati si ottiene867,25-1087,25 euro senza switch. È una somma di osservazioni con regimi IVA visualizzati diversi e stime, non il prezzo di un ordine italiano. Con A800 al posto dei V3:1027,25-1247,25 euro. Pi, legno, cavi/protezioni/supporti e accessori microfonici restano stime, non offerte nuove.

Il tweeter è in backorder e il microfono in preordine. La pagina V3 non consente di garantire due unità e consegna italiana. Le lacune non motivano una sostituzione automatica: cambiare tweeter riapre geometria, filtri e confronto acustico. La scelta di spesa resta al proprietario e i riscontri fisici sono sospesi. Il risultato utile ora è la distinta, la mappa dei collegamenti e l'elenco esatto dei criteri che sbloccano CAD e taratura.
