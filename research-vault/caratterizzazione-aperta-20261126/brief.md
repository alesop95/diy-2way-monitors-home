# Esito tecnico e limiti

F1 separa acquisizione e authoring: SpeakerLab importa i dati e crea il modello GLL; la pagina corrente lo offre con licenza commerciale. F2 aggiunge l'autorizzazione del modello per Focus. La precedente descrizione di ARTA come semplice via di salvataggio GLL e di SpeakerLab come gratuito va corretta. Non è stata identificata, nel perimetro consultato, una catena libera che garantisca un GLL autorizzato per Focus.

F3 documenta dati testuali, FRD e CSV. F7 documenta il FRD a tre colonne di frequenza, modulo e fase. La via sviluppabile qui è conservarli, verificarli e confrontarli senza trasformare l'assenza del GLL in un blocco dell'analisi. F6 mantiene disponibile la strada GNU Octave/MATAA già prevista; l'acquisizione reale rimane da qualificare.

F4 è una release GPL3 identificata, distinta dai prodotti cui si applicano le condizioni F5. Nel codice v1.5.2 saveFRD e saveCSV scrivono anche la coerenza: sono quattro colonne. Usano la fase memorizzata, mentre phase() applica anche polarità e ritardo. La condizione isnormal esclude inoltre valori zero. È un rilievo statico: non sono stati eseguiti OSM o una misura. L'importatore deve distinguere questo schema e conservare i dati ricevuti, senza promettere che comprendano le correzioni mostrate nell'app.

Si sviluppa un controllo locale su file con NumPy già disponibile. Le decisioni dell'esecutore sono parsing esplicito dei formati, nessuna fase inventata, nessuna normalizzazione automatica delle direzioni e nessuna estrapolazione. Si verifica il bersaglio ai campioni disponibili nella banda e si segnala una griglia troppo rada. Provenienza, calibrazione e validità fisica dei dati rimangono dichiarazioni da verificare nel futuro collaudo: hardware_qualified resta falso anche quando i campioni soddisfano il bersaglio.

Restano aperti l'effetto della catena di acquisizione reale, la copertura angolare completa necessaria a un modello spaziale e l'eventuale percorso proprietario GLL. Il controllo di cinque direzioni non produce una sfera di direttività, un CLF o una misura della stanza. Nessuna licenza o componente viene acquistato o installato.
