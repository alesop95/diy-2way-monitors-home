# La catena di riproduzione: dal computer ai monitor

> Che cosa sta fra il computer e i due monitor, e perché questa scelta vincola una decisione di progetto che il documento sorgente aveva lasciato aperta. Il convertitore è già in casa e già studiato in un progetto proprio, quindi questa pagina non lo descrive da capo: lo colloca nel workflow e ne ricava le conseguenze.

## Il convertitore scelto

La sorgente digitale è l'unità etichettata Rod Rain audio, oggetto di uno studio di reverse engineering che vive nel progetto `rodrainaudio-reverse-eng` e che è la fonte canonica per ogni dettaglio del dispositivo. È un amplificatore per cuffie su telaio di tipo Beyerdynamic A1 in cui è stato integrato un modulo DAC[^1] USB.

La catena interna, come documentata in quel progetto, è la seguente: ingresso USB, ricevitore USB-audio SA9023, collegamento I²S[^2], convertitore ES9023 con driver di uscita integrato a 2 Vrms, filtro RC, uscita a livello di linea, e da lì lo stadio cuffie discreto su dissipatore. L'alimentazione è lineare, con toroide da due volte 12 V. Il pannello posteriore espone AUDIO IN, AUDIO OUT su RCA, USB-B e la rete.

Ciò che di questo elenco conta per il progetto dei monitor è un solo dato: esiste una **uscita a livello di linea su RCA, a circa 2 Vrms**. È il livello di linea consumer standard, ed è esattamente ciò che serve come sorgente.

## La conseguenza che vincola il progetto, e va capita prima di comprare i driver

Due Vrms su RCA sono un segnale, non una potenza. Lo stadio cuffie che segue nella catena interna è dimensionato per carichi da decine o centinaia di ohm e per potenze nell'ordine dei milliwatt o di qualche centinaio di milliwatt; un altoparlante da 4 o 8 ohm che chiede decine di watt è un carico di natura diversa, che quello stadio non può pilotare e a cui non va collegato.

Ne segue che la scelta del convertitore non è indipendente dall'architettura del diffusore, e le due strade sono queste.

Se i monitor sono **attivi**, cioè con amplificazione a bordo e crossover attivo, l'uscita RCA del Rod Rain va direttamente ai loro ingressi e la catena è completa. Un due vie attivo ha un amplificatore per via, quindi due canali di potenza per cassa, e il crossover lavora a livello di linea prima degli amplificatori.

Se i monitor sono **passivi**, cioè con crossover a componenti fra l'amplificatore e i driver, serve un amplificatore di potenza stereo fra il Rod Rain e le casse. Quell'amplificatore diventa un elemento della catena da scegliere, con la sua potenza, la sua impedenza di carico ammessa e il suo rumore, e non esiste al momento fra le cose disponibili.

Il documento sorgente lasciava questa scelta aperta, scrivendo che il crossover potesse essere passivo o attivo e che entrambi si potessero simulare in VituixCAD. Era una posizione legittima quando la sorgente non era decisa. Ora che lo è, la scelta va anticipata, perché determina se occorre un acquisto in più e perché cambia la fase 4a: un crossover passivo si progetta con componenti reali e le loro tolleranze, uno attivo si progetta come filtro a livello di linea e si realizza in analogico o in digitale.

Non la decido io. La registro come decisione aperta con i suoi termini, e il posto naturale dove risolverla è la fase 4a, prima dell'acquisto dei driver, perché la scelta influisce anche su quali driver convengono.

## L'uso condiviso con un'altra macchina

Il convertitore è usato anche da un altro computer. Non è un problema di progetto, ma ha due conseguenze pratiche che vale annotare adesso invece di scoprirle dopo.

La prima è banale e riguarda l'ergonomia: una sola porta USB-B significa scollegare e ricollegare, oppure interporre un commutatore USB. Nulla di tecnico, ma è il tipo di attrito che scoraggia le misure ripetute, e le misure ripetute sono il metodo di questo progetto.

La seconda è più sottile e riguarda la validità delle misure. La catena di **misura** usa la Focusrite Scarlett 2i2, perché serve un ingresso microfonico con alimentazione phantom, mentre la catena di **ascolto** userà il Rod Rain. Sono due convertitori diversi con due uscite diverse. Per la fase 1, cioè la caratterizzazione della stanza, questo è irrilevante: si misura come la stanza risponde, e la sorgente è uno strumento provvisorio. Per la fase 8, cioè la verifica finale del monitor costruito, non è irrilevante: se si vuole misurare ciò che si ascolterà, il segnale di prova deve uscire dalla catena di ascolto reale. REW permette di usare dispositivi diversi in ingresso e in uscita, quindi la configurazione corretta per la fase 8 è microfono sulla Scarlett e generazione del segnale sul Rod Rain.

## Che cosa resta da verificare

Tre punti, tutti da accertare sul dispositivo o dalla trattazione del progetto dedicato, e nessuno da assumere.

Se l'uscita AUDIO OUT sia a livello fisso oppure segua il controllo di volume dello stadio cuffie. La differenza è sostanziale per la struttura dei guadagni: con un'uscita fissa a 2 Vrms e monitor attivi il controllo di volume deve stare altrove, cioè nei monitor stessi o in un attenuatore passivo interposto, mentre con un'uscita controllata il volume è già dove serve.

Quale sia la funzione di AUDIO IN, cioè se sia un ingresso analogico che alimenta lo stadio cuffie bypassando il DAC, e se in quel caso l'uscita RCA riporti quel segnale. Serve a sapere se il dispositivo può funzionare anche come semplice amplificatore o commutatore.

Il rumore e la distorsione dell'uscita di linea nelle condizioni d'uso previste. La trattazione del progetto dedicato affronta rumore e impedenza d'uscita per i carichi cuffia; l'uso come sorgente verso un amplificatore o verso monitor attivi è un caso diverso, con un carico di ingresso molto più alto, e va verificato che i valori dichiarati coprano anche quello.

[^1]: *DAC*, Digital to Analog Converter - convertitore che trasforma il flusso numerico proveniente dal computer in un segnale elettrico analogico; qui è il chip ES9023, con driver di uscita integrato che fornisce direttamente il livello di linea senza stadio amplificatore aggiuntivo.

[^2]: *I²S*, Inter-IC Sound - interfaccia digitale seriale con cui il ricevitore USB passa i campioni audio al convertitore, con linee separate per clock, dato e selezione del canale.
