# Catena di riferimento, piano MS-323

Base main ac01f66, chiusura MS-322 verificata. Il proprietario autorizza il prossimo passo: consolidare documentalmente i componenti e i collegamenti per sbloccare il progetto esecutivo. È una proposta tecnica da rivedere, senza ordini, installazioni, deploy o riapertura delle verifiche fisiche ADR-055. Due GRC preesistenti riservati al template; nessun agente parallelo.

## Specifica e alternative

Riordinare la base già sviluppata nel capitolo63: UMC1820 condivisa fra PC e Pi, uscite5-8 per le quattro vie, cuffie separate3/4, SB16PFCR25-8 e SB26STCN-C000-4 in A24 chiusa, due finali stereo V3 con alimentatori finiti, EMM-6 come catena di misura candidata. Non ricominciare la scelta da zero. Le alternative SB15/B27, amplificazione bilanciata e processore separato restano confronti motivati, non acquisti cumulativi.

Verificare manuali e datasheet ufficiali, inclusi i limiti contrari alla proposta. Separare specifica del produttore, inferenza di progetto e prova dell'esemplare. Prezzi del 20 novembre restano storici; aggiornare soltanto le righe realmente lette, con data/IVA/spedizione/stock e variante esatta. Non congelare filtri, guadagni o fresature come se fossero già tarati.

## Passi e risultati

- [x] Inventario mirato: capitoli20/55/63/64/65/66, dati driver/geometria, mappe PC/Pi, budget e fonti canoniche; nessuna lettura di dischi esterni.
- [x] Ricerca narrativa mirata in research-vault/catena-riferimento-20261126: scope/sources/brief, query esatte e coperture. Recuperare le fonti che servono davvero, marcando ciò che non è leggibile.
- [x] Produrre docs/67-catena-di-riferimento-e-dipendenze-esecutive.md: componenti/quantità, percorso completo PC e Pi, mappa canali, collegamenti di linea/potenza e dipendenze per CAD/DSP. Una scelta di sviluppo esplicita, senza qualifiche hardware presunte.
- [x] Preparare distinta e budget tracciabile, distinguendo prezzo osservato, stima, variante e condizione. Esporre il residuo decisionale reale prima di una scelta di spesa.
- [x] Aggiornare capitolo63 e registri correnti senza duplicare due fonti di verità. Preservare storia, simulazioni e quattro PDF correnti; rigenerare solo i documenti effettivamente superati, QA sulle pagine cambiate.
- [x] Aggiornare memoria/ripresa, indici e roadmap; eseguire i controlli pertinenti e la chiusura completa prima di proporre il perimetro manuale. Nessun nuovo test per semplici modifiche documentali; eventuali calcoli devono conservare input e risultato.

## Revisione

Il Main della UMC1820 non governa le Line Out3-10. Il passaggio USB cambia host e richiede una sequenza silenziata. Le prese cuffie non sono quattro vie di monitor. Un finale RCA richiede un collegamento ammesso dalle uscite bilanciate: la specifica TRS non basta a scegliere il cablaggio. I120W del tweeter hanno una condizione di filtro e non sono potenza a banda intera. Un chip da300W non rende300W continui un finale con alimentatore32V/5A. Quote e compatibilità nominali non sono un ordine di taglio.

Scelta ricevuta nel giro: mantenere V3 per priorità al costo, registrata in ADR-058 e nel JSON. C-01 non è risolto da questa conferma. Distinta e somme controllate con Decimal; mappa e variante confrontate con i dati canonici senza qualificare l’hardware. Fonte Dayton fallita marcata non letta, portale calibrazione separato. Indici e due PDF rigenerati; QA sulle 16 pagine correnti, originali e ricevute conservati. Primo gate completo verde con tutti i 46 comandi locali; memoria e perimetro consolidati. Ripetere il gate dopo l’ultima scrittura e proporre chiudi soltanto se chiudi-finale.txt termina «Controlli verdi».
