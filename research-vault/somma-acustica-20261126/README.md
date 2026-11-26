# Prova della somma complessa, MS-322

Questo archivio conserva risultati di un modello analitico, non una nuova ricerca bibliografica o una campagna di misura. Metodo, comandi eseguiti e limiti nel [capitolo66](../../docs/66-somma-acustica-e-crossover-su-file.md); input costruiti in [data/somma-acustica-demo](../../data/somma-acustica-demo/README.md). Le formule elettriche LR4 provengono dal modulo già usato nel capitolo62.

risultati.json registra tre manifesti: allineato, polarità del tweeter invertita e ritardo di sei campioni. Ogni rapporto include hash dei byte originali e dei due moduli, qualità degli input, soglie dei nulli e confronto del risultato. I coefficienti vengono confrontati con la trasformazione bilineare del modello continuo; al taglio i moduli attesi sono1,0 e sqrt(0,5). Tutti i risultati restano simulated, hardware_qualified falso.

I tre pacchetti locali sono in build/somma-acustica-20261126; ciascuno contiene sette file firmati più il manifesto. La prova di caratterizzazione downstream usa il dataset allineato senza convertirlo in dato misurato. Il vault conserva i rapporti durevoli, mentre i pacchetti di lavoro si rigenerano dai file versionati. Non sono stati consultati nuovi paper, aperti servizi audio o letti dischi esterni.
