# Due driver unitari, esempio analitico del crossover

I file sono sintetici: due risposte di modulo unitario e fase zero sulla stessa griglia di 242 frequenze tra50 e20000Hz, includendo esattamente2000Hz. Non rappresentano i driver SB, la cassa o la stanza. Lo zero della fase è parte della costruzione analitica, non una fase ricavata da una misura incompleta.

I coefficienti provengono da digital_biquad in tools/verifica-matematica-crossover.py, già usato nel capitolo62: due sezioni Butterworth identiche per ciascun ramo, frequenza2000Hz e campionamento48000Hz. Sono coefficienti elettrici di prova, non una configurazione calibrata per i monitor. Nessun servizio CamillaDSP viene modificato o interpretato dal nuovo modulo.

manifest.json mantiene i rami allineati. invertito.json cambia soltanto la polarità del tweeter; ritardo-6-campioni.json aggiunge0,125ms al tweeter, equivalenti a sei campioni alla frequenza dichiarata. Al taglio i moduli analitici della somma sono rispettivamente1,0 e sqrt(0,5). Il calcolo in virgola mobile può lasciare un residuo presso il nullo: la fase viene dichiarata indefinita, senza assegnarle zero gradi.

Il bersaglio100-10000Hz entro±0,5dB serve alle prove. I riferimenti comuni sono dichiarati perché la fixture li costruisce; per future misure dovranno essere dimostrati nella catena di acquisizione. La somma resta un dato simulato e non qualifica l'hardware. Metodo e comandi nel [capitolo66](../../docs/66-somma-acustica-e-crossover-su-file.md).
