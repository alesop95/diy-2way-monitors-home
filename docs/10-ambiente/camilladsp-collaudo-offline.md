# CamillaDSP: collaudo su file prima dell'interfaccia

Stato verificato il 2026-11-18, MS-237. Ubuntu Studio ha eseguito CamillaDSP 4.1.3 in una nuova cartella temporanea, usando soltanto file PCM. Non è un servizio installato né il crossover definitivo dei diffusori. Lo schermo è un acquisto differito e non blocca questa preparazione.

## Che cosa è stato eseguito

Il binario Linux ufficiale è stato scaricato dal [rilascio CamillaDSP 4.1.3](https://github.com/HEnquist/camilladsp/releases/tag/v4.1.3), verificato per SHA-256 e confrontato dopo il trasferimento SSH. Il solo elemento nell'archivio è l'eseguibile. Sono stati trasferiti nella stessa cartella nuova lo script di collaudo e la configurazione JSON, che il motore ha accettato come documento YAML. Il binario ha dichiarato `CamillaDSP 4.1.3 (05e9cfc)`.

I comandi seguenti sono stati eseguiti nella cartella temporanea di prova sulla macchina, dopo il trasferimento dei tre file. I nomi dei file sono quelli realmente usati; la cartella temporanea e i rapporti con i percorsi reali restano nel livello privato del progetto.

```bash
sha256sum camilladsp-linux-amd64-v4.1.3.tar.gz
tar -xzf camilladsp-linux-amd64-v4.1.3.tar.gz
./camilladsp --version
python3 collauda-camilladsp.py --bin ./camilladsp --config ./offline-lr4.json --dest ./rapporti --mutazioni
```

L'impronta attesa dell'archivio è `55f5ec2ed80fcc79a543672f9f89ace4557d290d80584ef31ee0442111bd0b11`. Si confronta prima di eseguire un binario scaricato; una differenza interrompe la procedura. Il collaudo crea una cartella nuova per ciascuna esecuzione e non sovrascrive una precedente misura.

## Risultati e limite della verifica

Tre corse sono riuscite: normale, volume a -6 dB e mute. Sono stati misurati ordine dei quattro canali, separazione delle bande, incrocio elettrico LR4 a 2 kHz e somma ai tre toni di prova. Il mute ha prodotto zero digitale; invertire i lati o sostituire il passa alto ha fatto fallire il controllo. Le misure coincidono con quelle Windows alla precisione del rapporto. Le prove complete e le tolleranze sono nel progetto canonico, pagina `docs/56-collaudo-dsp-offline.md`; sorgenti `tools/collauda-camilladsp.py` e `config/camilladsp/offline-lr4.json`. Questi sorgenti non appartengono al blocco documentale copiato al gemello e restano di proprietà di questo progetto.

Il risultato dimostra il comportamento del motore e della configurazione su file in questo ambiente. Non osserva conversione analogica, mappatura dei jack, latenza USB, rumore degli amplificatori o stabilità durante una registrazione. Il collegamento con PipeWire e l'avvio persistente sono ancora da preparare. Crossover e protezioni finali dipendono dagli altoparlanti e dalle misure in cassa.

## Stato del prossimo intervento

Aggiornamento 2026-11-18: Veeam e stato verificato nella sessione attuale e funziona senza sudo grazie al gruppo veeam. Il nuovo pieno e in corso, con conservazione portata da due a tre per mantenere i punti di settembre; seguire `backup-ottimizzazione-2026-11.md`. Il requisito di sudo manuale riguarda ancora l'aggiornamento APT, non il backup così eseguito.

La ricognizione di oggi conferma il servizio `cpupower-gui` fallito e la correzione della distribuzione candidata. I backup visibili nel deposito sono datati 17 e 21 settembre; la sola presenza non certifica un punto attuale o un ripristino. Prima di cambiare il sistema si verifica il lavoro Veeam e si produce un nuovo punto con rilettura, seguendo `veeam-agent-linux.md`. Il lavoro privilegiato resta manuale; nessun aggiornamento o avvio di servizio è stato eseguito in questo collaudo.

FreeCAD non è stato trovato nel PATH o come pacchetto con candidato negli indici APT locali. Il rilascio ufficiale individuato è [FreeCAD 1.1.4](https://github.com/FreeCAD/FreeCAD/releases/tag/1.1.4), con AppImage Linux x86_64 da circa 821 MB e impronta pubblicata. Non è stato scaricato o collaudato sulla macchina. La disponibilità di un artefatto non dimostra il funzionamento del CAD o la validità di un cabinet; questo resta il prossimo fronte indipendente dallo schermo.

## Troubleshooting osservato

La prova Linux è riuscita al primo avvio del collaudo già corretto su Windows. L'errore incontrato nella preparazione, cioè il parametro negativo di volume passato come argomento separato, è documentato con causa e rimedio nella pagina del collaudo del progetto canonico. Non è stato osservato un guasto Linux da aggiungere come esperienza della macchina.

Aggiornamento 2026-11-19: backup e rotazione esterna riusciti, CPU aggiornata e FreeCAD collaudato. Il [servizio persistente PipeWire](camilladsp-servizio-utente.md) è ora verificato anche sul segnale virtuale e sulla ripartenza dopo guasto; le descrizioni precedenti di questo documento restano riferite alla corsa offline del 18 novembre. Hardware e riavvio del sistema restano da provare.
