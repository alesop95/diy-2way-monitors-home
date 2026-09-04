# diy-2way-monitors-home

Progettazione e costruzione di una coppia di monitor da studio a due vie per un punto di ascolto domestico, con l'intero flusso di lavoro su Linux. Il progetto è nella fase in cui la parte simulativa è documentata in profondità e la parte fisica non è ancora iniziata: nessuna misura eseguita, nessun driver acquistato, nessun cabinet disegnato. Va letto come un percorso di progettazione documentato con cura, non come una realizzazione finita.

## L'impostazione, che è la cosa che distingue questo progetto

Il progetto non parte dal diffusore ma dalla stanza. Il punto di ascolto è in un ambiente irregolare, con soffitto spiovente e una parete vicina alle spalle, che non è trattabile acusticamente né riposizionabile per vincoli di arredamento. Invece di progettare un diffusore neutro in campo libero e poi lasciargli subire la stanza, si misura la stanza per prima, si valida un modello geometrico contro quella misura, si progetta il diffusore in parallelo, e si ottimizza la posizione soltanto alla fine con i due modelli insieme.

Il criterio di successo è di conseguenza definito al punto di ascolto reale e non in camera anecoica: una risposta lineare entro più o meno 2 dB in asse e fino a più o meno dieci gradi fuori asse, da 60 Hz a circa 20 kHz.

## Il workflow in otto fasi

Misura reale della stanza con REW e microfono calibrato. Modellazione geometrica dell'ambiente in Blender. Analisi modale e calcolo dei tempi di riverberazione in GNU Octave con il toolbox MATAA. Progettazione acustica del diffusore in VituixCAD e progettazione meccanica del cabinet in FreeCAD. Simulazione finale in Akabak 3, che mette insieme il diffusore progettato e la stanza validata. Acquisto dei driver, montaggio, e verifica finale con una nuova misura nello stesso punto di ascolto.

## La toolchain, e perché è composta così

La regola di composizione è nativo Linux dove possibile, Wine dove non esiste alternativa seria. Nativi sono REW, Blender, Octave con MATAA e FreeCAD, e su Ubuntu Studio hanno il vantaggio della gestione a bassa latenza della catena audio. Sotto Wine restano quattro programmi, ciascuno nel proprio prefix a 64 bit: Akabak 3, che è l'unico gratuito a fare elettroacustica e acustica ambientale in un solo passaggio, il suo strumento di visualizzazione VACS, VituixCAD 2 per crossover e direttività, ed EASE Focus 3 per la verifica di copertura.

Wine e non una macchina virtuale, per tre motivi indipendenti: la catena audio resta quella nativa, mentre una macchina virtuale aggiungerebbe latenza proprio nella fase in cui si misura il tempo; l'identificativo hardware esposto è quello reale, quindi la licenza di Akabak, che è legata alla macchina, sopravvive a reinstallazioni e ricostruzioni dell'ambiente; e non serve alcuna licenza Windows, perché nessun codice Windows è in esecuzione.

## La macchina

Un desktop riconvertito con processore Intel i7-6700, 16 GB di RAM e un SSD da 500 GB, escluso da Windows 11 per requisiti e riformattato su Ubuntu Studio con kernel a bassa latenza. L'interfaccia audio è una Focusrite Scarlett 2i2 di seconda generazione con alimentazione phantom. Il partizionamento tiene `/home` su una partizione separata, scelta che oggi rende una reinstallazione pulita del sistema una operazione a basso rischio.

## Documentazione

Il punto d'ingresso è [docs/README.md](docs/README.md), che indicizza l'intero albero. Vale segnalare quattro pagine che stanno da sole.

Il [workflow completo](docs/00-workflow.md) mostra le otto fasi insieme, con ingressi, uscite e strumento di ciascuna.

La pagina su [Wine, un emulatore e una macchina virtuale](docs/10-ambiente/wine-vs-emulatore.md) chiarisce una distinzione da cui dipendono quasi tutte le decisioni pratiche dell'ambiente, e non è una digressione teorica.

La pagina sull'[aggiornamento alla LTS successiva](docs/10-ambiente/ubuntu-lts-upgrade.md) ricostruisce perché la macchina non si aggiorna, con la procedura di verifica e le due strade possibili. È dichiaratamente una ipotesi in attesa di conferma sulla macchina.

Il [registro dei microstep](docs/OPERATIONS-LOG.md) traccia ogni intervento con il comando che lo ha verificato e il suo esito, inclusi i microstep bloccati e da che cosa dipendono.

La direzione del progetto, con le priorità motivate e le decisioni ancora aperte, sta in [.claude/context/roadmap.md](.claude/context/roadmap.md).

## Materiali

Gli installer dei programmi Windows, il pacchetto degli esempi di Akabak e il documento sorgente della documentazione non sono versionati, per un totale di circa 166 megabyte. Vivono sul disco di sviluppo solo in transito verso la macchina di lavoro; l'elenco di che cosa sono, dove vanno e come si verifica l'integrità del travaso è in [docs/TRANSFER-MANIFEST.md](docs/TRANSFER-MANIFEST.md).

Il documento sorgente `full_electroacoustics.docx`, da cui proviene la maggior parte di questa documentazione, è stato convertito integralmente e archiviato fuori dal versionamento. La prova che la copertura è completa, sezione per sezione, è in [docs/90-riferimenti/copertura-sorgente.md](docs/90-riferimenti/copertura-sorgente.md).

## Progetto gemello

Il blocco di documentazione sull'ambiente, cioè [docs/10-ambiente/](docs/10-ambiente/README.md), è condiviso con `home-recording-training-mixing-setup`, perché la stessa macchina serve a entrambi i progetti. La copia canonica è quella di questo repository e la propagazione è unidirezionale, con `tools/sync-ambiente.py`.

## Stato

Fase di progettazione documentata. Il prossimo passo concreto non è di progetto ma di infrastruttura: rimettere in servizio la macchina di lavoro, che è su un rilascio di Ubuntu fuori supporto, prima di iniziare le misure.
