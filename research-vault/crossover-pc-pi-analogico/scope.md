# Protocollo: PC, Raspberry Pi, analogico e doppio uso dei monitor

Data: 2026-11-20. Richiesta dell'utente: manuale tecnico CamillaDSP, confronto ingegneristico e matematico fra piattaforme e crossover, vantaggi e limiti del doppio uso mix/ascolto; indice della documentazione anche didattica. Ricerca narrativa tecnica mirata, non revisione sistematica. Nessun cambio dell'architettura o acquisto viene deciso da questo studio.

## Domande e ipotesi prima dei calcoli

Separare quattro assi: realizzazione del filtro (analogica o digitale), calcolatore ospite del DSP (PC o Raspberry Pi), interfacce e amplificazione, obiettivo acustico dei profili. Verificare quali scelte sono già registrate in ADR-033, ADR-045, ADR-046 e ADR-049, senza interpretare il collaudo su PC come esclusione definitiva del Raspberry Pi. Distinguere vantaggio pratico del richiamo dei profili dalla possibilità fisica di usare un diffusore per più impieghi.

## Fonti e inventario

Inventario iniziale: documenti 52, 54, 55, 56, 57, 58, 59 e 75, registri delle decisioni e dei collaudi, scheda W3C già presente nel vault e ricerca di Linkwitz/Riley nei metadati fonti.json. Tale ricerca nei metadati non legge tutti i PDF o gli archivi privati e non attesta lettura dei libri. Il nuovo indice documentale è un censimento dei percorsi di progetto, distinto dalla ricerca bibliografica.

Fonti ammesse: autore originale Linkwitz Lab, documentazione e codice CamillaDSP fissati a 4.1.3, W3C Audio EQ Cookbook, note applicative dei produttori analogici, documentazione Raspberry Pi e review scientifica dal sito dell'editore. Niente forum usati come prova, prezzi correnti non oggetto del confronto. Linkwitz Lab è fonte prioritaria per richiesta esplicita dell'utente, senza estendere la qualifica di letto a tutto il sito.

Query esatte eseguite il 2026-11-20: `site.linkwitzlab.com filters Linkwitz Riley crossover sum phase fourth order`; `site.ti.com active low pass filter design Sallen Key Q equal components application report`; `site.raspberrypi.com documentation computers audio USB audio Raspberry Pi`; `site.github.com HEnquist camilladsp v4.1.3 Delay subsample coefficient LinkwitzRiley`. Gli URL iniziali includono il filters.htm fornito dall'utente, il README e backend PipeWire CamillaDSP già usati nel progetto, il cookbook W3C già censito. Le capacità di ricerca e simulazione sono state cercate nel catalogo con due formulazioni; nessuna installazione o collegamento di servizi a consumo.

## Protocollo numerico deterministico

Parametri illustrativi, non scelta dei monitor: fc=2000 Hz, fs=48000 Hz, c=343 m/s ipotizzata, modello lineare tempo-invariante di filtri e due sorgenti coerenti. Griglia di frequenza logaritmica con punti dichiarati nel rapporto, più valutazione esatta a fc. Nessun driver reale, ambiente, consumo o carico DAW misurato da questa simulazione; nessuna inferenza statistica da punti della griglia trattati come repliche sperimentali.

Confronti prespecificati: somma LR4 contro modulo unitario e contro forma allpass derivata; rami digitali da due biquad Butterworth contro proprietà a fc e stabilità dei poli; modello Sallen-Key a componenti uguali con Q, guadagno e tolleranze espliciti; profilo comune ai due rami contro rapporto complesso invariato; controesempi con polarità opposta e differenza di cammino. Tolleranze delle uguaglianze numeriche: 1e-9 sul modulo complesso e 1e-9 sui valori speciali, salvo valore esplicitamente indicato. I controesempi devono produrre l'effetto diverso atteso, non un generico errore di esecuzione.

Conservare codice, parametri, rapporti JSON, CSV della griglia, hash e figure autonome. Esportare figure con strumenti scientifici standard e design di account, senza presentarle come acquisizioni. L'analisi non sostituisce la prova fisica dei driver, la misura della latenza o un confronto energetico PC/Pi sotto lo stesso carico.

## Prodotti previsti

Manuale operativo nel progetto, confronto con derivazioni e risultati, brief e review tracciati nel topic, scheda prioritaria Linkwitz Lab, approfondimento didattico e indice ragionato completo. Fonti e limiti in sources.md; sorgente dei calcoli in tools/verifica-matematica-crossover.py; artefatti derivati sotto build. Non modificare servizio audio, profilo di laboratorio, dati su J o filtri di diffusori reali.
