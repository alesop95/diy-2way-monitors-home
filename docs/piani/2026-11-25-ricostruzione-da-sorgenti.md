# Ricostruzione dai sorgenti dopo MS-319

Base dcb5e18, chiusura eseguita dal proprietario e impronta coerente. Prosecuzione autonoma autorizzata. I due GRC preesistenti restano esclusi, nessun add/commit/push/deploy. Diagnosi e correzione di capacità già consegnate, senza nuove scelte del prodotto o installazioni.

## Difetto riprodotto e confine

Un archivio Git del commit, estratto in una cartella nuova senza build, non riesce a verificare le quattro figure, la figura del basso o i DXF: i font sono cercati soltanto nella copia di un kit precedente ignorato. Tre dei quattro test del kit falliscono per PDF/CAD generati assenti. I test di MS-319 erano verdi su questa postazione; quella prova non dimostrava il comportamento di un clone. Prova privata prova-sorgenti-prima.json e copia immutata dei sorgenti conservate. La prima esecuzione dei test temporanei nel sandbox ha anche incontrato una negazione Windows; la ripetizione con i permessi appropriati ha isolato il difetto di risorse.

Il catalogo non offre un componente pertinente per risolvere font locali e fixture di questo progetto. Craft e design Intrawelt già presenti vengono riusati. Il generatore del kit continua a richiedere gli artefatti realmente collaudati: una prova con byte costruiti non qualifica il formato CAD.

## Piano inline

- [x] Osservare rosse le prove di selezione dei font da argomento, ambiente o installazione; rifiutare un percorso esplicito incompleto senza sostituire il design system.
- [x] Condividere la risoluzione dei font fra grafici e tavole, conservando opzioni esplicite e dichiarando le impronte delle risorse; nessun font copiato nel repository pubblico.
- [x] Rendere autonome le prove del contratto del kit con fixture temporanee esplicite. Conservare controlli su alterazioni prima/dopo la firma e sul PDF con sorgente superata; il collaudo reale rimane obbligatorio nella chiusura.
- [x] Eseguire realmente grafici e tavole da una copia dei soli sorgenti, senza la vecchia cartella build. Verificare che la prova fallisca con risorsa mancante.
- [x] Rigenerare figure e tavole interessate, aggiornare consegna/PDF e ispezionare le pagine cambiate. Aggiornare istruzioni di ricostruzione, controlli, didattica e memoria; gate completo prima di proporre chiudi.

## Revisione

Prove in prima persona secondo la regola locale. Una directory esplicita sbagliata deve fallire; una risorsa uguale deve produrre la stessa grafica. Le fixture del kit coprono integrità e composizione, non la geometria. La prova da sorgenti deve eseguire processi reali con percorsi isolati e senza ereditare il vecchio build. Verifiche fisiche sempre sospese ADR-055.


## Esito osservato il 26 novembre

Otto suite: 42 test e nove subtest superati; gate completo con «Controlli verdi» e 39 comandi locali. Quattro PDF correnti, QA registrato, kit da 55 file e 2.444.936 byte verificato. Prime cinque pagine della relazione identiche per hash delle immagini, sesta e recap aggiornati ispezionati. Le figure sono ricostruite da processi reali in una copia dei sorgenti, con confronto degli SVG e caso negativo sulla risorsa mancante. Le fixture del manifesto non sostituiscono il collaudo nativo.

Durante il passaggio alla scrittura protetta della figura basso è emerso un import sys mancante, corretto e coperto dalla prova che ora esercita anche la scrittura. La rigenerazione WordCraft ha richiesto esecuzione fuori sandbox per il temporaneo negato; riuscita senza cambiare il template. La sonda CADCraft sul percorso assoluto ha restituito TrueType falso: rimangono nome file e controllo TrueType del motore. Un aggiornamento PowerShell dei metadati si è fermato prima di scrivere per un'ancora non valida; le trasformazioni successive validano tutte le ancore prima di applicarle.

Artefatti precedenti archiviati, 14 PNG QA rimossi con ricevuta e banco iniziale eliminato dopo verifica del suo archivio Git di435 voci. Temporaneo Craft nominato e cache ripuliti con autorizzazione e controllo dei percorsi. Nessuna installazione, scrittura Git, modifica audio o qualifica fisica. Dopo la persistenza finale si ripete chiudi in sola verifica; perimetro manuale esclude i due GRC.
