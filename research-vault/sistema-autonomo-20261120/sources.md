# Fonti dello sviluppo autonomo e dei componenti

Accesso 2026-11-20. Contenuti tecnici su fonti primarie, prezzi sui venditori del prodotto. Le schede sono state lette per i punti dichiarati; nessuna prova dell'hardware deriva da un datasheet.

| Fonte | Contenuto letto e uso |
|---|---|
| [UMC1820 produttore](https://behringer.com/en/products/0805-AAN) e [manuale ufficiale](https://cdn-media.empowertribe.com/2b9a46d7e1104b78b8881f726c18a4d0/QSG_BE_0805-AAN_UMC1820_WW.pdf) | Controlli, routing digitale e specifiche. Ottico/coassiale dipendono da OPT I/O; Line Out 3-10 indipendenti da Main. Nessuna certificazione Linux, clock o mappa ALSA dell'esemplare. |
| [SB16PFCR25-8](https://sbacoustics.com/wp-content/uploads/2024/01/6in-SB16PFCR25-8.pdf) | Una pagina: parametri T/S, escursione picco-picco e disegno quotato. Dati del modello in data/driver-candidati.json; non curve misurate sul nostro baffle. |
| [SB15NRX2C30-8](https://sbacoustics.com/wp-content/uploads/2020/02/5in-SB15NRX2C30-8.pdf) | Una pagina: parametri e diametri per alternativa più stretta, dati di progetto distinti dalle dichiarazioni qualitative sul motore. |
| [SB26STCN-C000-4](https://sbacoustics.com/wp-content/uploads/2020/02/SB26STCN-C000-4.pdf) | Una pagina: diametro, risonanza, Re e sensibilità. Nessuna autorizzazione al segnale a banda intera dedotta dalla potenza IEC. |
| [Fosi V3 manuale](https://fosiaudio.com/pages/user-instruction-v3) | Ingressi RCA, stereo, alimentazioni, carichi e collegamento. Non misura indipendente di rumore/potenza del nostro esemplare. |
| [TI TPA3255](https://www.ti.com/lit/ds/symlink/tpa3255.pdf) | Condizioni di potenza/carico e topologia per distinguere chip e oggetto finito; nessuna analisi completa del PCB Fosi. |
| [Raspberry Pi 4](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/), [configurazione](https://www.raspberrypi.com/documentation/computers/configuration.html) | Piattaforma, sistema Lite e configurazione; consumo e carico DSP da misurare. Prezzo del kit nel budget è una stima. |
| [Delock 87482 datasheet](https://www.delock.com/produkt/87482/pdf.html?sprache=en) | Topologia due host/un dispositivo e alimentazione; HTML rifiutato, PDF diretto leggibile. Nessuna garanzia isocrona con UMC1820. |
| [HiFiBerry DAC8x](https://www.hifiberry.com/docs/data-sheets/datasheet-dac8x/) | Confronto di un convertitore separato; evitato nella base con interfaccia condivisa. |
| [OpenCV 4.13, omografia](https://docs.opencv.org/4.13.0/d9/dab/tutorial_homography.html) | Teoria, punti coplanari e rettifica prospettica, sezioni iniziali; non lettura dei libri collegati. Limiti della stima da foto. |
| [UMC1820 Thomann](https://www.thomann.it/behringer_umc1820.htm) | Prezzo 175 € IVA inclusa e disponibilità della pagina italiana. |
| [SB16](https://www.soundimports.eu/en/sb-acoustics-sb16pfcr25-8.html), [SB15](https://www.soundimports.eu/en/sb-acoustics-sb15nrx2c30-8.html), [SB26](https://www.soundimports.eu/en/sb-acoustics-sb26stcn-c000-4.html), SoundImports | 31,45 / 63,95 / 36,45 € visualizzati; tweeter esaurito. Distinti prezzi imponibili/lordi, IVA di destinazione e trasporto da verificare. |
| [V3 32V Audiophonics](https://www.audiophonics.fr/fr/amplificateurs-integre/fosi-audio-v3-32v-p-21697.html) | Riferimento 99 € con IVA francese e alimentatore, disponibilità da confermare; non prezzo finale italiano o prova prestazionale. |

CamillaDSP 4.1.3: README ufficiale già conservato e verificato nel topic crossover; riletti Main implicito, Volume per fader Aux e Lowshelf con slope in dB/ottava. Il parser e il motore su file costituiscono una prova distinta dal testo.
