# Revisione e lacune

L'autonomia era stata lasciata opzionale: ADR-051 corregge la premessa per richiesta dell'utente, senza riscrivere gli eventi storici. Le configurazioni sono dimostrative, il Pi non è presente e il controllo d'uso autonomo finale non è ancora implementato. È preparato un modello d'unità di sistema in attesa silenziata e una mappa hardware con verified false; nessuna configurazione PC operativa è stata sostituita.

Le principali lacune misurabili sono mappa e formati ALSA, clock da sorgente, rumore e guadagni, controllo comune delle vie, avvio a freddo/hotplug, carico DAW e misura acustica di driver in cassa. La selezione teorica è motivata da ingombri, modello e costo complessivo; la prestazione sonora superiore di un marchio non è stata dimostrata. Il budget include stime e stock variabile, senza ordini inviati.

Il controllo chiudi aveva un vero accento mancante nella docstring dell'installatore: il precedente addebito alle stringhe Python era errato e viene ritirato nei microstep. Il correttore non è stato indebolito. Le verifiche della consegna comprendono anche rendering effettivo delle formule e controllo della data dei PNG: una vecchia anteprima non prova il PDF corrente.
