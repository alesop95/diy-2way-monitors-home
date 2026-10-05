# Biblioteca e vault delle fonti: sequenza replicabile

> Pagina prescrittiva del fronte della base bibliografica, PA-026 e PA-027, secondo la regola di `CLAUDE.md`. Ogni comando qui sotto è stato eseguito il 2026-10-05 sulla postazione Windows con il disco esterno montato come `J:`, e il suo esito osservato. Il racconto cronologico, con i ritiri, sta nei microstep da MS-189 a MS-201 di `docs/OPERATIONS-LOG.md`. Le scelte che governano il fronte sono ADR-036 e ADR-038.

## Che cosa produce

Il materiale di studio resta sul disco esterno e il progetto ne tiene l'indice per impronta. Il testo convertito sta in una cache locale. Da indice, cache e registro uno strumento genera la biblioteca JabRef `Biblioteca.bib` e il vault Obsidian delle fonti, con una nota per fonte e una per gruppo, in `J:\MAIN\LOUDSPEAKERS & ELECTROACOUSTIC\_VAULT FONTI\`. La tassonomia dei quattro alberi di gruppi è specificata in `research-vault/09-Biblioteca-tassonomia.md`, e le regole che la applicano stanno in `research-vault/biblioteca-regole.yml`.

## Sequenza

I comandi si eseguono dalla radice del repository e sono identici in PowerShell e in bash, perché sono tutti invocazioni di Python con percorsi fra doppi apici. Su `J:` gli strumenti leggono soltanto, tranne `estrai-archivi.py`, che scrive nella destinazione indicata, e `biblioteca.py`, che scrive nel vault: entrambe le scritture sono autorizzate dall'utente, la prima in MS-197 e la seconda in ADR-038.

Il primo passo censisce le cartelle in un lotto nuovo, il secondo calcola le impronte e scarta i doppioni.

```powershell
python tools/censisci-cartelle.py --lotto 12 --prova "J:/MAIN/CARTELLA"
python tools/censisci-cartelle.py --lotto 12 "J:/MAIN/CARTELLA"
python tools/indicizza-lotti.py --lotto 12
```

Gli archivi del lotto si estraggono nella cartella scelta dall'utente.

```powershell
python tools/estrai-archivi.py --dest "J:/MAIN/_ESTRATTI ARCHIVI TESI" --prova
python tools/estrai-archivi.py --dest "J:/MAIN/_ESTRATTI ARCHIVI TESI"
```

La conversione in testo prima, l'OCR delle scansioni poi, sempre un processo alla volta.

```powershell
python tools/converti-fonti.py --lotto 12
python tools/converti-fonti.py --ocr --nomi Dickason Colloms
```

Infine si rigenerano il registro unico e la biblioteca, e si verifica l'indice.

```powershell
python tools/registro-fonti.py
python tools/biblioteca.py --prova
python tools/biblioteca.py
python tools/indicizza-lotti.py --verifica
```

Le voci che nessuna regola assegna finiscono nel gruppo Da classificare. Per ridurle si allargano prima le regole in `biblioteca-regole.yml`. Quello che resta si fa classificare a un agente sul solo titolo, e l'esito va in `_notes/biblioteca/classificazione-agente.json`, con la forma `{"chiave": {"disciplina": [...], "progetto": [...]}}`. Il file è locale, e lo strumento lo applica solo alle voci che le regole non hanno assegnato.

## Esiti attesi, misurati il 2026-10-05

`indicizza-lotti.py --lotto 11`: 2650 indicizzati, 162 doppioni, nessun mancante. `converti-fonti.py --lotto 11`: 2648 nuovi e 2 errori, con 4357 documenti nel manifesto, di cui 431 sotto le 50 parole. `biblioteca.py`: 8194 fonti e 148 gruppi, con 8194 note di fonte e 148 note di gruppo, scritti in circa 40 secondi. La biblioteca ha 8197 blocchi, nessuno con parentesi sbilanciate, e 3300 voci con il campo `file`. `indicizza-lotti.py --verifica`: 7384 posizioni verificate, nessun problema.

## Troubleshooting: sintomo, causa, rimedio

Ogni voce nasce da un caso osservato sulla postazione Windows il 2026-10-05 e non da una previsione.

### A, due gruppi di stato contano zero

Sintomo: in `biblioteca.py --prova` i gruppi `PDF su J:` e `Materiale di studio su J:` contano zero. Causa: in YAML una chiave non quotata che contiene i due punti seguiti da uno spazio viene spezzata, e il gruppo prende il nome `PDF su J`. Rimedio: quotare la chiave nell'albero, `"PDF su J:": {}`.

### B, un gruppo raccoglie quasi tutto

Sintomo: un gruppo raccoglie quasi tutto, per esempio Acustica classica con 1797 voci. Causa: le parole chiave venivano confrontate anche con il percorso, e il nome della cartella ombrello `LOUDSPEAKERS & ELECTROACOUSTIC` contiene "acoustic". Rimedio: le parole chiave guardano titolo e sede, e il percorso solo sotto `z_____UNIVERSITA`, dove le cartelle portano i nomi dei corsi. Per le altre cartelle si usa la tabella `cartelle:` delle regole.

### C, un'espressione con la barra rovesciata non trova nulla

Sintomo: un'espressione con `\b` o `\+` non trova nulla, oppure trova una barra rovesciata letterale. Causa: nelle stringhe YAML fra apici singoli la barra rovesciata è letterale, quindi `'\\b'` diventa l'espressione `\\b`, cioè barra seguita da b. Rimedio: scrivere `'\b'` fra apici singoli, e nei percorsi usare la barra in avanti, che lo strumento normalizza.

### D, il controllo delle fini riga cade su un file illeggibile

Sintomo: `check-eol.py` cade con `PermissionError` su un file sotto `_notes/.tmp-estrazione/`. Causa: il residuo di un pacchetto per macOS estratto a metà contiene collegamenti che Windows rifiuta di leggere. Rimedio: lo strumento corretto in MS-199 filtra per nome prima di interrogare il disco. Il residuo si cancella dal terminale dell'utente con `Remove-Item -LiteralPath <cartella> -Recurse -Force`, perché la cancellazione ricorsiva è vietata all'agente.

### E, il resoconto di un agente non torna con il suo file

Sintomo: un agente di classificazione dichiara di avere scritto più voci di quante ne avesse in ingresso, oppure ne restituisce meno. Causa: il resoconto di un agente è un'affermazione e non una misura. Il 2026-10-05 un lotto da 379 voci è stato dichiarato di 500, e il file ne conteneva 374. Rimedio: prima di usarne l'esito, confrontare le chiavi dell'uscita con quelle dell'ingresso e scartare i nomi di gruppo che non stanno nell'albero, come fa il passo di unione descritto in MS-201.

### F, il diff mostra cambiato l'intero file

Sintomo: dopo una modifica con `sed -i` il diff mostra cambiato l'intero file. Causa: `sed -i` di Git Bash riscrive le fini riga `CRLF` in `LF`. Rimedio: sui file `CRLF` si usa lo strumento di modifica o uno script che scrive i byte, e prima di un commit si confronta la fine riga di ogni file modificato con `HEAD`. Il caso è in MS-199.
