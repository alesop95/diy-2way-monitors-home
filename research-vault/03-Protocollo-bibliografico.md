---
tipo: protocollo
aggiornato: 2026-10-02
---
# Protocollo bibliografico

**Tipo di studio.** Revisione narrativa mirata al progetto, non sistematica: ogni fonte entra perché fonda una derivazione o una scelta della tesi. Non la si chiama sistematica finché non esistono ricerca documentata per filone, screening con i conteggi e un criterio di arresto dichiarato.

## Le cinque provenienze

Ogni voce di `fonti.json` dichiara da dove viene, e una voce può averne più d'una dopo l'unione.

- `locale`: documento del materiale di studio dell'utente su `J:`, indicizzato per lotto con posizione e impronta in `fonti-locali/lotto-NN-origine.json` (ADR-036).
- `libreria`: voce della libreria JabRef `ELE_Technical_Library.bib`, che è lavoro di terzi. I suoi PDF non esistono: l'utente ha chiarito il 2026-10-02 che è un elenco e che i paper che servono si scaricano.
- `tesi2020`: voce della bibliografia della tesi magistrale dell'utente.
- `proposta`: candidato dell'agente, riscontrato sul web prima di essere consegnato.
- `scaricata`: PDF scaricato dall'utente in `papers/` con il nome uguale alla chiave.

## Gli stati

Lo stato del PDF è `assente`, `su J:` o `scaricato`. Lo stato di verifica è `da_verificare`, `verificata` o `scartata`, come vuole la skill `citation-tracker`. Una fonte diventa verificata soltanto quando il PDF o la pagina dell'editore è stato letto e titolo, autori, sede, anno e pagine coincidono. Solo le verificate entrano in `bibliography.bib`.

## Unione dei doppioni

Lo strumento unisce prima per DOI, poi per titolo normalizzato, con la numerazione romana portata in cifre perché "Part I" e "Part 1" sono lo stesso titolo. Per le sole proposte usa anche un confronto approssimato, che assorbe i refusi della libreria di terzi. Il confronto approssimato non fonde mai due titoli i cui numeri differiscono: senza questa regola la prima versione aveva fuso le due parti di Thiele 1971.

## Che cosa si versiona e che cosa no

Si versionano le note, le schede in `paper/`, la configurazione di `.obsidian`, `fonti.json`, `fonti-proposte.json`, `papers/manifest.json` e `bibliography.bib`. Restano locali i PDF, l'indice del materiale di studio, la libreria di terzi e i plugin comunitari; il materiale stesso non sta nel progetto ma in `J:\MAIN`, per ADR-036. Nessun percorso su `J:` e nessun contenuto dei libri entra nei file versionati, per ADR-028.

## Lezioni apprese nella prima ricerca, 2026-10-02

Prima di proporre candidati dalla propria conoscenza si cerca ciò che esiste già: le cartelle di studio, le bibliografie delle tesi precedenti dell'utente e le librerie bibliografiche. La prima proposta di 24 paper era stata fatta a memoria e dieci erano già in una libreria locale (MS-187).

Una proposta a memoria si riscontra prima di consegnare un collegamento. Il riscontro ha corretto la forma di sette voci su ventiquattro: parti multiple, convention invece di rivista, anno della ripubblicazione (MS-186).

Le pagine della AES E-Library e di ASA rispondono 403 agli strumenti di recupero, quindi i loro metadati si prendono dai risultati di ricerca e lo stato resta `da_verificare` fino al PDF.

Una ricerca per nome di file non vede il contenuto: non trova un PDF rinominato né l'interno di un archivio, e lo si dichiara accanto al risultato.

Torna a [[00-START]]
