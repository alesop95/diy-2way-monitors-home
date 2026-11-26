# Sistema con PC e autonomo: componenti, profili e qualificazione

Revisione 2026-11-26, ADR-051/052/057/058. L'ascolto a PC spento da CD o riproduttori esterni è obbligatorio. Questa proposta sviluppa entrambi i percorsi e sceglie una base concreta per interfaccia, driver e finali. Le parti già verificate sono indicate con il relativo risultato; le prove di hardware assente sono un protocollo da eseguire, non un collaudo dichiarato riuscito. La versione di lettura con formule è [il PDF LaTeX](pdf/sistema-autonomo-driver-e-collaudo.pdf); il [dossier sul crossover](62-confronto-crossover-e-verifica-matematica.md) fornisce le dimostrazioni generali. Il [consolidamento della catena, distinta e budget corrente](67-catena-di-riferimento-e-dipendenze-esecutive.md) registra la conferma dei V3 e i collegamenti nominali; le cifre del 20 novembre conservate sotto sono storiche.

## Architettura scelta per proseguire

La base proposta è una coppia attiva, un'interfaccia UMC1820 e quattro canali di potenza condivisi. In registrazione l'interfaccia USB appartiene al PC Ubuntu e CamillaDSP elabora sul PC. In ascolto autonomo appartiene al Raspberry Pi e CamillaDSP elabora sul Pi. Il cavo USB si sposta a finali spenti; uno switch USB può rendere comoda la commutazione solo dopo averne verificato il funzionamento audio. Non occorre comprare un secondo DAC multicanale per questa architettura.

| Modalità | Percorso completo | Disponibilità della registrazione |
|---|---|---|
| Studio PC | DAW/lettore su Ubuntu → PipeWire → CamillaDSP PC → USB UMC1820 → quattro uscite → due finali stereo → driver | Otto ingressi analogici al PC, cuffie su percorso stereo distinto |
| CD digitale autonomo | Uscita PCM S/PDIF del CD → ingresso digitale UMC1820 → USB Pi → CamillaDSP Pi → USB UMC1820 → stessi finali e driver | Il PC può essere spento; interfaccia impegnata dal Pi |
| Sorgente analogica autonoma | RCA di linea → due ingressi line UMC1820 → ADC → USB Pi → DSP → DAC UMC1820 → finali | Non è un trasporto bit perfect; contiene conversione ADC |
| Riproduzione locale/rete autonoma | Lettore sul Pi → dispositivo ALSA loopback → CamillaDSP → USB UMC1820 → finali | Sorgente e DSP sul Pi; loopback/routing da qualificare |

La condivisione riguarda due modalità alternative. Se in futuro si volesse registrare sul PC mentre un altro contenuto suona autonomamente, servirebbero un'interfaccia aggiuntiva o il Pi come processore permanente con collegamento digitale dal PC. Quest'ultima soluzione aggiunge gestione dei clock e latenza al monitoring; non è necessaria per il requisito espresso di ascolto a PC spento. Il [DAC8x](https://www.hifiberry.com/docs/data-sheets/datasheet-dac8x/) rimane un confronto per un processore dedicato separato, non un acquisto da sommare automaticamente alla UMC1820.

Per il Pi propongo un Raspberry Pi 4 Model B da 1 o 2 GB, alimentatore ufficiale compatibile, microSD affidabile e contenitore passivo ventilato. È una scelta di risorse per un crossover IIR, da verificare con CPU, temperatura e xrun; non una prestazione già misurata. La [documentazione ufficiale](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/) descrive la piattaforma. RAM maggiore e Pi 5 non sono requisiti di questo carico preliminare. I prezzi della RAM sono cambiati anche nel 2026: si confrontano offerte attuali del kit completo, compreso un Pi 4 usato verificato, invece di riusare il vecchio prezzo storico della sola scheda.

Un [Delock 87482](https://www.delock.com/produkt/87482/pdf.html?sprache=en) è un riferimento di switch due host/un dispositivo: il datasheet documenta questa topologia, non il collaudo di una UMC1820 in trasferimento isocrono. Il collegamento diretto resta il riferimento della prova. Si controllano enumerazione, stabilità, alimentazione e ritorno dopo commutazione; uno switch che fallisce si elimina dalla catena, mantenendo le due modalità con spostamento del cavo. Un cavo USB a Y non svolge questo compito.

## Ingressi digitali, clock e significato di bit perfect

Il [manuale UMC1820 ufficiale](https://cdn-media.empowertribe.com/2b9a46d7e1104b78b8881f726c18a4d0/QSG_BE_0805-AAN_UMC1820_WW.pdf), sezioni controlli e Digital I/O Routing, impone una distinzione decisiva: con OPT I/O in S/PDIF l'ingresso è ottico e il coassiale è disabilitato; in modalità ADAT il coassiale riceve S/PDIF. I canali digitali sono indicati come 9-10 nel manuale. Gli indici e il numero di canali esposti da ALSA vanno rilevati sull'esemplare; il modello di laboratorio usa indici zero-based 8/9 in un flusso simulato da 18 canali.

Si parte da PCM stereo a 44,1 kHz per CD, oppure 48 kHz per le sorgenti che lo richiedono. Non si inviano Dolby/DTS ai driver. L'interfaccia deve seguire il clock della sorgente digitale, oppure occorre una conversione asincrona deliberata. Il protocollo legge i controlli ALSA effettivamente esposti, seleziona la sorgente disponibile e verifica validità/aggancio con il dispositivo reale. Non si scrive un numid fisso ricavato da un'altra macchina. La documentazione del produttore non basta a dichiarare qualificati questi controlli su Linux.

La politica iniziale è due configurazioni del DSP, a 44,1 e 48 kHz, generate con la stessa frequenza di crossover in hertz. Il cambio richiede mute, chiusura del flusso, nuovo clock, caricamento della configurazione corrispondente, verifica del lock e riabilitazione controllata. Commutare OPT I/O durante il funzionamento provoca un riavvio dell'interfaccia secondo il manuale: si fermano prima le applicazioni. Una sorgente che cambia frequenza non viene trattata come se il vecchio flusso fosse ancora valido.

Bit perfect significa conservare i campioni decodificati fra sorgente e ingresso del processore. Volume, EQ, crossover e ricampionamento li modificano intenzionalmente; non si promette identità bit per bit ai quattro canali d'uscita. Per la prova si usa una sequenza PCM nota non protetta, si acquisisce prima dei filtri, si allineano i campioni e si confrontano gli interi dopo aver normalizzato contenitore e padding 16/24/32 bit. Un hash del WAV intero confronta anche header e metadati e non misura da solo questa proprietà. Risultato richiesto: zero campioni diversi sul tratto sincronizzato, senza guadagni o conversioni di frequenza attivi.

## Interfaccia, canali e volume

UMC1820 è la candidata di sistema per gli otto ingressi richiesti dall'home recording e per le uscite/digitali; sostituisce nella proposta corrente la precedente candidata a quattro ingressi, senza fingere un acquisto già compiuto. [Produttore](https://behringer.com/en/products/0805-AAN) e manuale documentano connettività e risoluzione; Linux, rumore e riaggancio restano prove dell'esemplare. La mappa seguente è di progetto e si verifica su carichi di prova prima dei tweeter.

| Funzione | Connessione proposta | Vincolo |
|---|---|---|
| Cuffie del musicista | Percorso stereo dedicato, playback 3/4 se qualificato | Deve restare a banda intera, senza ricevere woofer/tweeter separati |
| Woofer L / tweeter L / woofer R / tweeter R | Line Out 5 / 6 / 7 / 8 | Quattro vie; indice USB fisico da verificare |
| Finale woofer stereo | Segnali destinati a woofer L e R | Guadagni fissati e misurati sui due lati |
| Finale tweeter stereo | Segnali destinati a tweeter L e R | Attenuazione/protezione dimensionate sul tweeter |
| Main 1/2 e altre uscite | Riserva/stereo separato, se necessario | Non collegate in modo da aggirare il crossover |

Le Line Out 3-10 non seguono la manopola Main, come dichiara il manuale. Il volume di ascolto agisce insieme sulle quattro vie attraverso il fader Main implicito di CamillaDSP; due potenziometri dei finali servono alla taratura, non al volume quotidiano. Il comando comune è il pannello locale sviluppato per PC/Pi, con mute e livello iniziale riletti. Un encoder fisico rimane opzionale. API e pannello restano su localhost; l'accesso remoto previsto usa tunnel SSH, senza esposizione automatica del WebSocket sulla rete. I valori dei livelli sono collaudati su file; la catena fisica del volume resta da qualificare.

La prima versione autonoma usa Raspberry Pi OS Lite 64 bit e CamillaDSP 4.1.3 ALSA, con unità di sistema dedicata e utente audio. L'avvio non dipende dal desktop. Si riusa la regola di attesa silenziata a -60 dB; il supervisore abilita l'ascolto soltanto dopo identità della scheda, clock, quattro canali e profilo verificati. Sono requisiti d'installazione e accettazione del Pi, non servizi già installati. Overlay in sola lettura e log volatili si valutano dopo aggiornamento e collaudo, seguendo la [documentazione Raspberry Pi](https://www.raspberrypi.com/documentation/computers/configuration.html), conservando un'immagine ripristinabile della configurazione funzionante.

## Driver e cabinet: una base concreta e un'alternativa

Propongo di sviluppare prima SB16PFCR25-8 e SB26STCN-C000-4 nel cabinet A24, MDF 18 mm e cassa chiusa, con C24 come confronto di maggiore volume. Il diametro esterno del woofer è 176 mm e quello del tweeter 72 mm. A24 è 220 × 190 × 430 mm; lascia circa 22 mm per lato al telaio del woofer e ammette l'orientamento esplorato a 30°. La cassa chiusa evita in questa prima iterazione un condotto lungo in un mobile poco profondo. Il [confronto reflex del 25 novembre](64-reflex-direttivita-e-cabinet-nominale.md) è ora sviluppato con perdite ipotetiche, velocità e ingombri del condotto; non cambia automaticamente la base chiusa o il target.

L'alternativa SB15NRX2C30-8 nel B27 permette un frontale più stretto: diametro esterno 150 mm, 190 mm di larghezza del cabinet e spazio maggiore per lo schermo. Costa di più e ha minore prodotto area/corsa. Le dichiarazioni del produttore su motore e bassa induttanza motivano un confronto in gamma media; la qualità sonora sul nostro frontale richiede le misure. Fonti dei dati: [SB16](https://sbacoustics.com/wp-content/uploads/2024/01/6in-SB16PFCR25-8.pdf), [SB15](https://sbacoustics.com/wp-content/uploads/2020/02/5in-SB15NRX2C30-8.pdf), [tweeter](https://sbacoustics.com/wp-content/uploads/2020/02/SB26STCN-C000-4.pdf). Dati normalizzati in [driver-candidati.json](../data/driver-candidati.json).

Il modello preliminare a piccoli segnali assume 1,5 litri occupati da driver, rinforzi e accessori in ciascun cabinet; il volume netto vero sarà misurato dal CAD. Per una cassa chiusa ideale:

$$\alpha=V_{as}/V_b,\quad f_c=f_s\sqrt{1+\alpha},\quad Q_{tc}=Q_{ts}\sqrt{1+\alpha},\quad H(s)=\frac{(s/\omega_c)^2}{(s/\omega_c)^2+(s/\omega_c)/Q_{tc}+1}.$$

| Woofer / cabinet | Netto ipotizzato L | fc Hz | Qtc | f3 Hz | Risposta a 60 Hz dB |
|---|---|---|---|---|---|
| SB16 / A24 | 9,664 | 74,01 | 0,779 | 67,80 | -4,44 |
| SB16 / B27 | 7,237 | 82,65 | 0,870 | 69,97 | -5,20 |
| SB16 / C24 | 12,016 | 68,47 | 0,721 | 67,20 | -4,15 |
| SB15 / A24 | 9,664 | 63,95 | 0,596 | 78,05 | -5,08 |
| SB15 / B27 | 7,237 | 70,81 | 0,660 | 76,28 | -5,26 |
| SB15 / C24 | 12,016 | 59,58 | 0,555 | 79,97 | -5,05 |

I valori spiegano perché una risonanza più bassa non garantisca una f3 più bassa: conta anche il Q. Nessuna riga soddisfa da sola il target storico entro ±2 dB da 60 Hz. Servirà confrontare EQ moderata, risposta nella stanza e limite di emissione; non si dichiara rispettato il target solo perché il software contiene uno shelving. Il modello trascura perdite aggiuntive, induttanza, effetto del materiale assorbente, diffrazione e compressione termica.

![Modello dei driver in cassa chiusa](../build/sistema-autonomo-20261120-v5/confronto-driver.pdf)

Con Xmax inteso come picco in una direzione, il limite di escursione di un monopolo ideale nello spazio intero è:

$$p_{rms}=\frac{\rho(2\pi f)^2S_dX_{pk}}{4\pi r\sqrt2},\qquad L_p=20\log_{10}(p_{rms}/20\,\mu Pa).$$

A 60 Hz e 1 m, con densità dell'aria ipotizzata 1,204 kg/m³, dà 88,58 dB per SB16 e 85,91 dB per SB15. Sono limiti del solo spostamento sinusoidale ideale, senza potenza/riscaldamento/direttività/ambiente. Il semispazio cambierebbe il conto di 6 dB; la stanza reale non viene identificata con nessuno dei due casi. Non si somma automaticamente un guadagno stereo. Il margine inferiore a 40 Hz cala di circa 7 dB: conferma il costo fisico dell'estensione ottenuta con EQ.

Come punto iniziale per studiare il frontale A24 propongo centro woofer a 115 mm dal fondo e tweeter a 247 mm, allineati orizzontalmente a 110 mm dal lato. Interasse 132 mm, distanza fra telai circa 8 mm, quota tweeter nominale da terra 1177 mm prima dei supporti. È una geometria di studio da confrontare con la foto e le orecchie. Nel solo modello di due contributi uguali all'incrocio a 2,6 kHz, un angolo verticale di 10° produce circa -1,37 dB per il cammino differenziale. Driver, centri acustici e direttività possono cambiare il risultato: non è la verifica del vincolo fuori asse.

## Finali, livelli e protezioni

La base economica proposta è due Fosi V3 stereo con alimentatore 32 V/5 A ciascuno: quattro canali completi, nessuna scheda nuda o alimentazione di rete da costruire. Il [manuale del produttore](https://fosiaudio.com/pages/user-instruction-v3) documenta ingresso RCA, carichi e alimentazione; le potenze commerciali massime non sono la potenza continua garantita di questa configurazione. Il [datasheet TI](https://www.ti.com/lit/ds/symlink/tpa3255.pdf) distingue tensione, carico e distorsione: il nome TPA3255 non qualifica automaticamente ogni scheda.

Un finale stereo alimenta i due woofer, l'altro i due tweeter; si misurano guadagni e corrispondenza L/R. I cavi dall'interfaccia ai finali sono corti e cablati secondo le uscite bilanciate e gli ingressi sbilanciati effettivi: non si presume di poter cortocircuitare qualunque ramo freddo. Prima dell'acquisto vanno riscontrati cablaggio ammesso, rumore a riposo e possibilità di reso; ronzio o fruscio non vengono dedotti dai dati del solo chip. Due A800 restano un'alternativa finita con ingressi bilanciati, più ingombrante e cara, da confrontare se la conversione verso RCA rende la prima soluzione poco conveniente.

Il livello massimo pubblicato delle uscite UMC1820 è +16 dBu, pari a circa 4,89 Vrms: può superare il livello necessario a molti finali. Si parte da guadagno software basso e carico di prova, si misura il guadagno elettrico del finale e si fissa la taratura prima dei driver. La relazione $P=V_{rms}^2/R$ vale per il carico resistivo di prova; l'impedenza del diffusore è complessa e dipendente dalla frequenza. La potenza IEC dichiarata sul tweeter non è un'autorizzazione a inviargli un segnale a banda intera.

Studiamo un condensatore non polarizzato in serie al tweeter, per esempio 47 µF, come protezione parziale da continua e basse frequenze. Nel modello resistivo con Re=3,2 ohm il polo è circa 1058 Hz; a 2,6 kHz introduce circa -0,67 dB e +22° di fase. Deve quindi entrare nella misura e nel progetto del crossover. Non basta da solo contro sovratensione, transitori o potenza eccessiva. Valore, tensione, ingombro e costo definitivi seguono taratura e misure. Le uscite BTL dei finali non condividono i negativi; un eventuale relè/protezione deve essere adatto a tale topologia. Il mute software non sostituisce il disinserimento dei quattro canali durante cablaggio e commutazione USB.

## Profili sviluppati e prova già eseguita

Sono generati dodici profili dimostrativi: PC stereo, Pi digitale e Pi analogico, ciascuno a 44,1/48 kHz e in modalità mix/ascolto. Usano esclusivamente RawFile/File. Contengono LR4 elettrico a 2600 Hz, passa-alto comune a 35 Hz, margine -12 dB e trim tweeter -5,5 dB; ascolto aggiunge uno shelving comune +2 dB centrato a 120 Hz con pendenza 1 dB/ottava. Il trim deriva solo dalla differenza nominale di sensibilità, non dalla taratura del sistema montato. Il profilo mix non è ancora un monitor calibrato, e questi valori non sono un crossover acustico esecutivo.

La selezione degli ingressi Pi è stata provata con disturbi negli altri canali simulati. CamillaDSP 4.1.3 ha elaborato realmente le dodici configurazioni su Windows: a pari frequenza/profilo, i quattro segnali risultano identici fra i tre trasporti logici nel tratto confrontato. Il controllo negativo seleziona la sorgente sbagliata e produce un segnale differente, rilevato dalla misura. Non dimostra driver Linux, ALSA, Raspberry o clock hardware.

Per il confronto della curva comune si misura la fondamentale sinusoidale, anziché il solo RMS globale: nel ramo fortemente attenuato le armoniche della quantizzazione dell'ingresso a 16 bit falsavano il confronto RMS. La rampa Main è distinta dalla risposta a regime. Un tentativo di filtro Volume con fader Main è stato rifiutato dal validatore: nella 4.1.3 Main è implicito, mentre il filtro Volume aggiuntivo è per Aux. I tentativi e le correzioni rimangono nei microstep.

I comandi eseguiti dalla radice sono:

```powershell
cd E:\diy-2way-monitors-home
python tools/test_studio_sistema.py
python tools/studio_sistema_audio.py --dest build/sistema-autonomo-20261120-v5
python tools/collauda-profili-autonomi.py --bin _notes/camilladsp-v4.1.3-win/camilladsp.exe --profiles build/sistema-autonomo-20261120-v5 --dest build/collaudo-profili-autonomi-20261120-finale-v5
```

Le destinazioni sono create nuove; per ripetere scegliere nomi nuovi. I tre casi fisici indipendenti verificano il punto Butterworth, il limite di volume grande e le leggi di scala dell'emissione. [Dati e ipotesi](../data/driver-candidati.json), [sorgente](../tools/studio_sistema_audio.py) e [collaudo dei profili](../tools/collauda-profili-autonomi.py) rendono riproducibile la prova. Nessuna configurazione operativa del PC è stata sostituita. La trasformazione dei file in configurazioni ALSA/PipeWire richiede la mappa misurata: quattro uscite logiche non significano aprire soltanto i primi quattro canali della UMC1820.

Il collaudo rifiuta backend diversi da RawFile/File, nomi PCM estranei, rate/canali/formati inattesi e filtri fuori dal sottoinsieme di prova prima di avviare il motore. La guardia è stata verificata con backend hardware e percorso di uscita alterati: i casi vengono respinti senza invocare il processo esterno. Questo vincolo rende esplicito il perimetro del comando anche se un profilo viene modificato.

## Protocollo DAW e autonomia da eseguire sull'hardware

### Controllo comune sviluppato il 23 novembre

Il software mancante è implementato: pannello Mix/Ascolto, volume comune e mute, API WebSocket, osservatore ALSA/clock e percorso PC PipeWire con grafo attestato. Il [manuale 61](61-camilladsp-manuale-tecnico.md) descrive stati, condizioni e codice; la [procedura di consegna](../config/controllo-ascolto/README.md) contiene comandi di prova e attivazione manuale. Le mappe example restano non qualificate. Il Pi richiede binario ARM e propria prova di interfaccia; non si presume che il test Ubuntu qualifichi ARM/USB.

| Prova | Evidenza e criterio |
|---|---|
| Motore reale Ubuntu | Due rate 44,1/48 kHz, quattro canali, HTTP e WebSocket reali su istanza FIFO/file separata. |
| Volume | Passo richiesto 6 dB; tutte le vie devono risultare entro 0,1 dB e avere segnale utile. |
| Mute e perdita condizioni | RMS inferiore a 0,00000001 dopo mute, guasto software e SIGTERM; nessun ripristino automatico. |
| Canonicalizzazione hardware | Candidati ALSA e PC letti dal parser reale senza caricarli, nessun jack aperto dalla prova. |
| Interfaccia grafica | Pagina reale in Edge desktop/mobile, profili e controlli verificati, immagini QA eliminate. |
| Stato del PC | Servizio principale riletto prima/dopo: Inactive, mute true, -60 dB. |

Il [rapporto corrente](../research-vault/sistema-autonomo-20261120/risultati-controllo.json) lega valori e ambiente alle impronte delle sorgenti. Clock mancante e grafi hardware errati sono esercitati con condizioni software e fixture; non sono prove elettriche. Il watchdog non garantisce un tempo massimo di silenziamento e non sostituisce le protezioni dei driver. Le cuffie restano su un percorso full range separato: il binder del PC non modifica i link delle altre applicazioni.

Questo è il progetto del collaudo futuro. La scheda e il Pi non sono presenti: non si dichiara una latenza o un numero di dropout misurato. Ogni sessione conserva versioni, configurazioni, hash, durata e acquisizioni.

| Prova | Configurazione/contrasto | Criterio e significato |
|---|---|---|
| Mappa fisica | Toni distinti su ogni uscita, inizialmente su carichi di prova | Corrispondenza completa fra USB/PipeWire/ALSA e jack; nessun ramo a banda intera sul tweeter |
| Registrazione e DSP | Otto ingressi simultanei, riproduzione multitraccia e quattro vie DSP; 44,1 e 48 kHz | Per ciascun punto 30 minuti senza xrun nel campione, canali corretti e file senza discontinuità; nessuna garanzia su carichi diversi |
| Buffer e carico | 1024, 512, 256 e 128 campioni, un valore alla volta | Conservare il minimo stabile sul carico scelto, registrando CPU, temperatura e picchi; non applicare ottimizzazioni globali senza confronto |
| Latenza elettrica | Loopback con segnale noto, confronto con bypass del solo DSP | Ritardo da correlazione e confronto per distinguere interfaccia, buffer e filtri; il numero del buffer non basta |
| Cuffie | Cue stereo e direct monitoring separati dalle quattro vie | Musicista sente segnale completo; registrare sia latenza sia presenza/assenza degli effetti software |
| CD e clock | Sequenza nota a 44,1 kHz, lock digitale e confronto pre-DSP | Zero campioni diversi sul tratto allineato; perdita sorgente o cambio rate porta a mute/stop controllato |
| Cambio host | Prima cavo diretto, poi switch candidato, finali disinseriti | Enumerazione e routing corretti, ritorno in attesa silenziata; nessuna pretesa di passaggio senza interruzione |
| Pi senza PC | Avvio a freddo, sorgente digitale e analogica, PC fisicamente spento | Audio solo dopo controlli e volume comune funzionante; log e ripartenza verificati |
| Guasti controllati | Profilo mancante, USB scollegato, servizio interrotto | Attesa/mute e riabilitazione esplicita, senza avvio a livello precedente; poi verifica transitori su carico |
| Diffusore e stanza | Driver montati, polarità, asse e ±10°, distorsione e SPL richiesti | Progettare crossover acustico e profili definitivi; il risultato software non chiude questa prova |

## Fotografia e quote: cosa possiamo stimare

Una foto con il tavolo intero può fornire una prima stima di ingombri e collocazione. Sul piano del ripiano, quattro punti riconoscibili e le dimensioni 1180 × 300 mm consentono una rettifica prospettica. La [documentazione OpenCV sull'omografia](https://docs.opencv.org/4.13.0/d9/dab/tutorial_homography.html), teoria e rettifica, descrive la relazione planare $s\mathbf{x}'=H\mathbf{x}$. Dimensioni nominali esatte non eliminano gli errori di identificazione dei bordi o della lente.

Le orecchie, lo schienale e le pareti non appartengono tutti al piano del ripiano: da una sola omografia non si ricavano le loro coordinate 3D. Una foto frontale e una laterale con pavimento, tavolo e seduta visibili aiutano a costruire intervalli plausibili; per l'altezza delle orecchie deve essere visibile l'ascoltatore nella posizione abituale. Senza quella vista il campo resta ignoto. Una foto grandangolare o un punto fuori piano può introdurre un errore sistematico non stimabile dai soli pixel.

Per esempio 1180 mm distribuiti su 900 pixel danno 1,31 mm/pixel nella sola scala locale semplificata; un errore di due pixel vale 2,62 mm, senza contare prospettiva, distorsione o punto fuori piano. Non è l'incertezza totale né un intervallo statistico. Distingueremo quote ufficiali, stime da immagine e controlli fisici necessari prima di fresare o ordinare i tagli. La foto non è ancora arrivata e non sono state inventate misure della stanza.

## Basso protetto, trasformazione e sensibilità: risultati verificati

Il nuovo [rapporto di fattibilità](../research-vault/sistema-autonomo-20261120/fattibilita-basso.json) include HP35, già previsto nei profili. Il passa alto LR4 a 35 Hz attenua ancora 0,952 dB a 60 Hz: SB16/A24 passa da -4,439 a -5,391 dB. Per arrivare a -2 dB al bordo servono +3,391 dB, circa 2,18 volte la potenza a quella frequenza, a parità di carico e segnale iniziale. L'EQ non aumenta lo spostamento d'aria massimo disponibile.

La trasformazione di Linkwitz viene sviluppata come confronto nominale. [Linkwitz Lab, sezione 9](https://www.linkwitzlab.com/filters.htm#9) descrive la sostituzione delle coppie di poli del sistema chiuso. Il [README CamillaDSP 4.1.3, IIR](https://github.com/HEnquist/camilladsp/blob/v4.1.3/README.md#iir) documenta LinkwitzTransform e i quattro parametri freq_act, q_act, freq_target e q_target. Queste sezioni sono state lette; non si dichiara letto l'intero sito o manuale.

$$ H_{\mathrm{LT}}(s)=\frac{s^2+s\omega_c/Q_c+\omega_c^2}{s^2+s\omega_t/Q_t+\omega_t^2}, \qquad |H_{\mathrm{HP35}}(f)|=\frac{1}{1+(35/f)^4}. $$

Il target chiuso Butterworth calcolato affinché il prodotto con HP35 sia -2 dB a 60 Hz ha frequenza 43,371 Hz e Q pari a uno diviso radice di due. È una cancellazione dei poli del modello, non di quelli misurati dell'esemplare o della stanza. Su A24 la sola trasformazione tende a +9,285 dB in continua; insieme a HP35 ha massimo spettrale di circa +3,281 dB. Il margine iniziale -12 dB resta di laboratorio: il massimo di una risposta in frequenza non garantisce assenza di picchi per ogni segnale o transitorio.

| Combinazione | Livello a 60 Hz con HP35 | Correzione per -2 dB | Rapporto di potenza | Risposta a 60 Hz perturbando i parametri, EQ nominale fissa |
|---|---|---|---|---|
| SB16/A24 | -5,391 dB | +3,391 dB | 2,18 | da -4,50 a +0,17 dB |
| SB16/C24 | -5,099 dB | +3,099 dB | 2,04 | da -4,21 a -0,10 dB |
| SB15/B27 | -6,209 dB | +4,209 dB | 2,64 | da -4,30 a -0,05 dB |

La sensibilità comprende 486 casi: sei abbinamenti matematici driver/volume, ciascuno con 81 combinazioni di Fs/Qts/Vas al 90/100/110% e occupazione interna 0,8/1,5/2,2 L. Sono scenari ipotetici, non tolleranze del produttore. L'EQ rimane quella nominale, senza ritararla per nascondere la variazione. I risultati che scendono sotto -2 dB dimostrano che la correzione nominale non garantisce il target sugli esemplari non misurati.

Nello scenario illustrativo di 85 dB RMS sinusoidali a 60 Hz, un metro e un solo woofer ideale in spazio intero, lo SB16 richiede circa 2,98 mm di corsa di picco contro 4,5 mm nominali; lo SB15 circa 4,50 contro 5 mm. Non è un livello richiesto dall'utente o una potenza termicamente ammissibile; non si sommano stanza o seconda cassa. Un volume maggiore riduce la correzione necessaria ma non il volume d'aria richiesto per lo stesso livello e frequenza.

Cinque prove verificano identità complessa, cancellazione dei poli, target comprensivo di HP35, rifiuto di un target impossibile e corsa. Il motore reale ha superato dodici casi, sei abbinamenti a due rate: massimo errore del guadagno elettrico a 60 Hz circa 0,000022 dB. Un target alterato del 20% provoca circa -0,900 dB di differenza ed è rilevato. Il test negativo produce audio: non accetta un errore di processo come prova della misura. I PCM sono temporanei ed eliminati; restano rapporto, risultati e hash. Non è una taratura dei monitor.

Comandi eseguiti dalla radice Windows:

```powershell
python tools/test_fattibilita_basso.py
python tools/fattibilita_basso.py --binary _notes/camilladsp-v4.1.3-win/camilladsp.exe
python tools/fattibilita_basso.py --check
```

Si mantiene SB16/A24 come base, C24 come confronto di volume e SB15/B27 come alternativa per lo schermo. Driver, fresature e prestazioni reali restano da qualificare. Il report rende esplicito il costo elettrico dell'estensione prima dell'acquisto.

## Spesa del 20 novembre, conservata come riferimento storico

Aggiornamento corrente: [capitolo67](67-catena-di-riferimento-e-dipendenze-esecutive.md), revisione commerciale del 26 novembre. La tabella seguente conserva la rilevazione2026-11-20 e non governa più la distinta corrente. Prezzi visualizzati dei negozi, non ordini o preventivi per la consegna italiana; IVA locale, spedizione, stock e fornitore vanno riscontrati. Le stime sono budget di progetto e non prezzi verificati.

| Voce | Quantità | Costo di riferimento o budget |
|---|---|---|
| UMC1820 | 1 | 175 € IVA inclusa, [Thomann Italia](https://www.thomann.it/behringer_umc1820.htm), disponibile nella pagina letta |
| SB16PFCR25-8 | 2 | 31,45 € ciascuno, [SoundImports](https://www.soundimports.eu/en/sb-acoustics-sb16pfcr25-8.html), 62,90 € visualizzati |
| SB26STCN-C000-4 | 2 | 36,45 € ciascuno, [SoundImports](https://www.soundimports.eu/en/sb-acoustics-sb26stcn-c000-4.html), 72,90 €, esaurito/backorder |
| Due Fosi V3 con alimentatori | 2 | 99 € ciascuno IVA francese inclusa, [Audiophonics](https://www.audiophonics.fr/fr/amplificateurs-integre/fosi-audio-v3-32v-p-21697.html), riferimento 198 €, disponibilità da confermare |
| Pi completo di alimentatore, microSD e contenitore | 1 | 100-160 € stimati; confrontare kit nuovo/usato verificato e prezzo attuale della RAM |
| Switch USB opzionale | 1 | 0 € con spostamento del cavo; 20-40 € stimati per comodità, solo dopo prova |
| MDF, rinforzi, colla, tagli e ferramenta | Lotto | 80-140 € stimati; preventivo del falegname con disegni esecutivi |
| Collegamenti, morsetti, protezioni parziali e supporti | Lotto | 80-140 € stimati; conteggio finale dopo taratura e layout |
| Misura: microfono calibrato, cavo e asta | Lotto | 100-140 € stimati; riuso dell'interfaccia e confronto con disponibilità effettiva |

La somma delle righe è 868,80-1088,80 € senza switch oppure 888,80-1128,80 € con switch: come budget arrotondato circa 870-1090 € oppure 890-1130 €. Esclude schermo, tavolo già comprato, trasporti, finitura e utensili. È un intervallo con voci stimate, non un preventivo chiuso. I due SB15 al posto degli SB16 aggiungono circa 65 € ai prezzi visualizzati di 63,95 € ciascuno; il vantaggio richiesto deve giustificarli. Non si comprano entrambi i tipi di woofer o due coppie di casse per eseguire il primo confronto teorico.

Il prossimo risultato costruttivo è confrontare foto/quote e target con questa base, fissare il candidato e misurare il prototipo. La disponibilità del tweeter e il preventivo dei finali possono motivare un'alternativa verificata; non si sostituisce una sigla mantenendo arbitrariamente filtri o fresature. Fonti, calcoli, tentativi e limiti sono registrati nei microstep successivi a MS-282.
