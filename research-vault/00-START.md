---
tipo: indice
aggiornato: 2026-10-02
---
# Vault di ricerca dei monitor a due vie

Aprire questa cartella, `research-vault/`, come vault Obsidian. È il centro della ricerca bibliografica della tesi di ADR-034: domanda, protocollo, registro delle fonti, schede dei paper. La configurazione e i plugin riprendono il vault `whitepaper-vault` del progetto `D:\intralino-benchmark`, come ha chiesto l'utente il 2026-10-02 (ADR-035).

## Percorso breve

1. [[scope]]: la domanda di ricerca, i sette filoni e le risposte alle domande di gate.
2. [[03-Protocollo-bibliografico]]: provenienze, stati, unione dei doppioni, che cosa resta locale e che cosa si versiona.
3. [[05-Basi-esistenti]]: il lavoro già fatto, cioè la tesi magistrale del 2020, la libreria JabRef e il materiale di studio su `J:`.
4. [[04-Paper-da-scaricare]]: i collegamenti dei paper da scaricare in `papers/`, con il nome uguale alla chiave.
5. [[06-Registro-fonti]]: conteggi e fonti selezionate, generati da `tools/registro-fonti.py`.
6. [[tracked-sources]]: il registro della skill `citation-tracker` con lo stato di verifica di ogni candidato.
7. [[07-Analisi-corpus]]: che cosa sostiene ciascun capitolo della tesi, le lacune e le scansioni da leggere.
8. [[08-Piano-ricerca-online]]: i dodici filoni e le query del primo giro della ricerca online.

## Che cosa c'è nella cartella

| Percorso | Contenuto | Versionato |
|---|---|---|
| `paper/` | una scheda per fonte selezionata: riferimento, collegamenti, perché serve, che cosa è stato letto | sì |
| `papers/` | i PDF scaricati dall'utente; `manifest.json` ne registra impronta e dimensione | solo il manifest |
| `fonti.json` | il registro completo, una voce per fonte con le provenienze | sì |
| `fonti-proposte.json` | i candidati dell'agente, riscontrati in MS-186 | sì |
| `bibliography.bib` | le sole fonti verificate, per la tesi | sì, quando esisterà |
| `fonti-locali/` | l'indice del materiale di studio, che resta su `J:` (ADR-036): `lotto-NN-origine.json` con posizione e impronta di ogni file, i manifesti dei lotti, il piano e i tre censimenti | no, ADR-028 |
| `basi/` | la libreria JabRef di terzi, la bibliografia estratta della tesi e i resoconti di verifica | no |
| `reference/` | il documento di riferimento del pacchetto `academic-researcher` | sì |
| `.obsidian/` | configurazione; i plugin comunitari e lo stato dell'interfaccia restano locali | solo la configurazione |

I plugin comunitari sono tre, come in intralino: `new-3d-graph` 2.5.0 per il grafo tridimensionale, `embed-html` 1.1.9 e `obsidian42-brat` 2.0.4, che serve a reinstallare gli altri due su un clone, perché la loro cartella non si versiona.

## Stato al 2026-10-02

Il registro conta 6145 voci dopo l'unione dei doppioni:
- 29 proposte dell'agente, di cui 17 già nella libreria JabRef e una già su `J:`;
- 5124 voci lette dalla libreria;
- 119 dalla bibliografia della tesi del 2020;
- 1153 documenti indicizzati su `J:`, dai nove lotti e dai dieci archivi.

1135 voci hanno un documento su `J:`. L'indice conta 4039 file indicizzati, per 5,62 GiB, con 1889 doppioni scartati per impronta (MS-189); i file restano in `J:\MAIN`, e quelli estratti dagli archivi in `J:\MAIN\_ESTRATTI ARCHIVI TESI` (MS-190, ADR-036). Il testo convertito sta in `_notes/.tmp-doc-cache/fonti/`, con l'indice `_INDEX.md`. Nessun PDF è ancora scaricato in `papers/`, quindi nessuna fonte è verificata.
