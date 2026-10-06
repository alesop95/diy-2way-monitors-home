---
tipo: progetto
aggiornato: 2026-10-05
---
# Tassonomia della biblioteca completa delle fonti

> Specifica del 2026-10-05 per PA-027 e ADR-038, confermata dall'utente lo stesso giorno insieme alla cartella del vault e alle note per tutte le voci, anche senza PDF. Descrive come la biblioteca JabRef e il vault delle fonti su `J:` suddividono ogni fonte. Uno strumento genera entrambi dall'indice e dal registro unico, quindi questa pagina è la specifica dello strumento.

## Da dove parte

La libreria JabRef `ELE_Technical_Library.bib` dichiara nel blocco `jabref-meta: grouping` un albero di sette rami: Computer science, Mathematics, Signal processing, Electronics and circuit theory, Physics, Music e Loudspeakers, più Musical Instruments e Amplifiers 2.0. Le sue voci però usano 52 nomi di gruppo, contati sul registro unico `fonti.json` il 2026-10-05. Molti gruppi usati non compaiono nell'albero, per esempio Loudspeaker motor, Sound field analysis, Wave Field Synthesis, Ambisonics, Multizone, Plane wave tube, Gaussian beams ed EMC, e quindi in JabRef restano sparsi. Il suo albero è il punto di partenza e non il limite: ogni gruppo usato trova un posto nell'albero, e i rami nuovi coprono il materiale che la libreria non aveva.

Il registro unico conta 8194 voci: 4986 della libreria, 3338 copie locali su `J:` dopo i lotti 10 e 11, 119 della bibliografia della tesi del 2020, 29 proposte dell'agente e 10 PDF scaricati. Le provenienze si sovrappongono.

## Quattro assi, come quattro alberi di JabRef

JabRef ammette più alberi sotto la radice, e una voce può stare in più gruppi. La biblioteca ne usa quattro, perché rispondono a quattro domande diverse.

### Asse 1, disciplina: che cosa c'è su un argomento

```
Disciplina
  Mathematics
    Analysis
    Algebra
    Geometry
    Probability and statistics
    Numerical mathematics
    Mathematical physics
      Integral asymptotics
      Math tables and functions
      Frames
  Signal processing
    Foundations
    Digital Signal Processing
      Filter design and quantization
      Room response equalization
    Nonlinear Signal Processing
    Statistical Signal Processing
    Audio and acoustics signal processing
  Electronics and circuit theory
    Circuit theory
    Analog electronics
    Digital electronics
    Microelectronics
    Audio electronics
      Amplifiers 2.0
    Electronic measurements
    EMC
  Physics
    Mechanics
      Vibration and structural dynamics
    Thermodynamics
    Electromagnetism
    Optics
      Gaussian beams
    Acoustics
      Acustica classica
      Room acoustics
      Psychoacoustics and spatial perception
      Sound field analysis
        Plane wave representations
        Wave Field Synthesis
        Ambisonics
        Multizone
      Acustica e psicoacustica automotive
      Acoustic simulation (FEM, BEM, ray tracing)
  Loudspeakers
    Transducer modelling (Thiele-Small, lumped parameters)
    Loudspeaker motor
    Nonlinearities and large signal
    Enclosures and cabinet
    Horns and waveguides
      Plane wave tube
    Directivity and baffle diffraction
    Crossover
    Active loudspeakers and DSP
    Measurement
    Studio monitors
    Line arrays and sound reinforcement
    Microspeakers and MEMS
    Manufacturer papers
  Microphones
  Music
  Musical Instruments
  Guitar and effects engineering
    Guitar electronics
    Distortion, overdrive and fuzz
    Modulation and time-based effects
    Guitar amplifiers and cabinets
    Virtual analog modeling
    Guitar pickups
    Guitar body acoustics
    Pedal design and construction
    Schematics and datasheets
  Mechanical design and CAD
  Computer science
    Information theory
    Data structures and algorithms
    Programming languages
    Artificial intelligence
      Machine learning
    Computer architecture
    Computer networks
    Databases
    Computer graphics
  Scientific writing and typesetting
```

I gruppi nuovi, cioè assenti dalla libreria JabRef, sono: Filter design and quantization, Room response equalization, Electronic measurements, Vibration and structural dynamics, Room acoustics, Psychoacoustics and spatial perception, Acoustic simulation, i sottogruppi di Loudspeakers tranne Loudspeaker motor e Plane wave tube, Microphones, Mechanical design and CAD, Machine learning e Scientific writing and typesetting. Gli altri esistono già come nomi nelle voci della libreria e vengono soltanto collocati.

Il ramo Guitar and effects engineering è stato aggiunto il 2026-10-06, su richiesta dell'utente, perché il materiale sull'ingegnerizzazione dei pedali e della chitarra elettrica è un'area di ricerca a sé e non un dettaglio dell'elettronica audio. I sottogruppi sono ricavati dal materiale presente: paper e tesi su distorsori e fuzz, modulazioni, simulazione di amplificatori e casse, modellazione virtuale analogica, pickup, acustica del corpo della chitarra, progetto dei pedali e schemi. Guitar electronics, che prima stava sotto Audio electronics, ne è il sottogruppo generale.

### Asse 2, progetto: che cosa sostiene un punto della tesi

```
Progetto monitor
  Capitoli
    00 Introduzione
    01 Misura della stanza
    02 Modello della stanza
    03 Simulazione acustica
    04 Crossover
    05 Progetto acustico
    06 Progetto meccanico
    07 Simulazione finale
    08 Costruzione e verifica
  Appendici
    A1 Notazione
    A2 Matematica
    A3 Elettrotecnica ed elettronica
    A4 Fisica ed elettromagnetismo
    A5 Acustica
    A6 Elettroacustica
    A7 Elaborazione numerica del segnale
  Filoni di ricerca
    R1 Correzione su più punti
    R2 Misura in stanza
    R3 Interferenza con i confini
    R4 Bassi in stanza piccola
    R5 Simulazione di stanze piccole
    R6 Crossover misti FIR e IIR
    R7 Quantizzazione dei biquad
    R8 Ritardi e centro acustico
    R9 Guida d'onda e direttività
    R10 Diffrazione del pannello
    R11 Cabinet
    R12 Monitor attivi oggi
  Decisioni
    ADR-033 Attivo con processore digitale
```

I capitoli sono quelli di `report/main.tex`, le appendici quelle di ADR-034, i filoni quelli di `08-Piano-ricerca-online.md`. Il ramo delle decisioni raccoglie le fonti citate per motivare una scelta, e cresce con le decisioni.

### Asse 3, provenienza: da dove viene la voce

```
Provenienza
  Libreria JabRef ELE
  Bibliografia della tesi 2020
  Appunti propri (lezioni Polimi)
  Materiale dei corsi universitari
  Libri
  Paper e preprint
  Proposte dell'agente
  Scaricati per la tesi
```

### Asse 4, stato: a che punto è la lettura

```
Stato
  PDF su J:
  PDF scaricato
  Senza PDF
  Testo convertito
  Scansione da OCR
  Letto
  Verificato
```

## Come si assegna una fonte ai gruppi

L'assegnazione è deterministica prima che linguistica, secondo `token-economy.md`.
- Le voci della libreria portano già i loro gruppi, e una tabella li colloca nell'albero.
- Le copie locali prendono il gruppo dalla cartella in cui stanno, con una tabella di corrispondenza fra cartelle di `J:` e gruppi. Per esempio `Biblioteca speaker\Horns` va in Horns and waveguides, `TLC, SIGNAL PROCESSING and DIGITAL FILTERS` va in Digital Signal Processing, e `KLIPPEL` va in Measurement.
- Parole chiave del titolo e delle intestazioni del testo convertito aggiungono gruppi di disciplina e di progetto, con regole scritte in un file di configurazione versionato.
- Le fonti che dopo i primi tre passi restano senza gruppo vanno in Da classificare. Le classifica un agente a lotti, con il modello economico, leggendo il solo scheletro di Livello 1. L'esito torna su disco come stato intermedio correggibile a mano.

## Che cosa si genera, e dove

Sul disco `J:`, in `J:\MAIN\LOUDSPEAKERS & ELECTROACOUSTIC\_VAULT FONTI\`:
- `Biblioteca.bib`, la biblioteca JabRef con i quattro alberi, il campo `groups` per ogni voce e il campo `file` verso la posizione su `J:`;
- `00-INDICE.md`, il punto d'ingresso del vault Obsidian;
- `Gruppi/`, una nota per gruppo con l'elenco delle sue fonti;
- `Fonti/`, una nota per fonte con metadati, gruppi, collegamento al PDF e al testo convertito, e una sezione di note di lettura che lo strumento non tocca mai;
- `.obsidian/`, la configurazione minima del vault.

Nel repository restano il registro, il protocollo e questa specifica. I percorsi su `J:` non entrano nei file tracciati, per ADR-028.

Lo strumento scrive soltanto dentro `_VAULT FONTI\`, non cancella nulla, e quando rigenera una nota riscrive la parte generata e conserva la sezione delle note di lettura.

Torna a [[00-START]]
