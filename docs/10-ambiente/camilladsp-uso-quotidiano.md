# CamillaDSP nella catena dei due monitor

Stato verificato il 2026-11-20: CamillaDSP 4.1.3 risponde al comando di controllo sulla macchina Ubuntu. La pipeline è Inactive, mute true e volume -60 dB: il motore è disponibile, ma non sta elaborando un profilo finale o pilotando automaticamente i connettori fisici. Il banco stereo verso quattro vie virtuali è stato collaudato il 19 novembre, anche dopo riavvio e nuovo accesso utente. Driver, taratura acustica e catena hardware restano da definire e misurare.

## Che cosa fa nel nostro progetto

CamillaDSP è il processore digitale che prepara il segnale per i monitor attivi. Il [progetto ufficiale, versione 4.1.3](https://github.com/HEnquist/camilladsp/blob/v4.1.3/README.md), documenta crossover attivi, equalizzazione e altri filtri. Qui useremo il motore sulla macchina Ubuntu Studio; è una scelta software con il PC nel percorso audio, distinta da un processore hardware autonomo.

Il punto di partenza è lo stereo prodotto dalla DAW o da un lettore musicale. Ogni lato deve alimentare due altoparlanti: il woofer e il tweeter. Il crossover divide lo spettro fra i due e tiene conto delle loro risposte; equalizzazione, ritardi e livelli serviranno a farli lavorare insieme sulla base delle misure. La frequenza di incrocio non si sceglie dal solo diametro del cono e non è ancora congelata.

```text
DAW o lettore musicale: stereo
              |
       PipeWire su Ubuntu
              |
          CamillaDSP
              |
scheda audio: quattro uscite analogiche indipendenti
              |
quattro canali di amplificazione
              |
woofer L, tweeter L, woofer R, tweeter R
```

La mappa logica del banco è la seguente. La corrispondenza con i jack fisici verrà provata con l'interfaccia scelta: questi numeri non sono un cablaggio hardware già qualificato.

| Via logica | Segnale destinato a |
|---|---|
| 1 | Woofer della cassa sinistra |
| 2 | Tweeter della cassa sinistra |
| 3 | Woofer della cassa destra |
| 4 | Tweeter della cassa destra |

Due casse a due vie richiedono quindi quattro canali di amplificazione nella soluzione attiva scelta. Il processore produce dati audio; l'interfaccia li converte in segnali analogici e i finali forniscono la potenza agli altoparlanti. Un'interfaccia con molte prese non garantisce da sola che siano tutte uscite indipendenti utilizzabili dal sistema: questo va riscontrato e collaudato. La scelta dell'interfaccia resta condivisa con gli ingressi necessari all'home recording.

## Come servirà nell'uso quotidiano

Il collegamento previsto farà passare il mix della DAW o la musica dal processore prima dei diffusori. Il [backend PipeWire ufficiale](https://github.com/HEnquist/camilladsp/blob/v4.1.3/backend_pipewire.md) crea nodi da collegare nel grafo audio; installare il servizio non instrada automaticamente ogni programma attraverso il DSP. Quella configurazione operativa e la selezione delle uscite fisiche sono ancora da realizzare.

Il progetto prevede una coppia sola con due profili da validare. Il profilo mix deve essere un riferimento coerente con il target di progetto. Il profilo ascolto può avere una diversa preferenza timbrica e di livello, restando entro i limiti degli stessi altoparlanti, cabinet e amplificatori. La divisione delle bande e le condizioni necessarie al funzionamento dei driver rimangono valide in entrambi; cambiare preferenza non significa alimentare il tweeter a banda intera.

Il profilo di laboratorio LR4 a 2 kHz dimostra soltanto il funzionamento del banco. Non è il crossover dei monitor e non va collegato agli altoparlanti come taratura finale. Per il profilo reale servono driver identificati, risposta in cassa, livelli e ordine dei jack verificati. Non è stato collaudato un limitatore hardware o un sistema completo di protezione dei tweeter; mute e -60 dB iniziali sono condizioni del banco.

Per controllare il sistema quotidianamente sono previsti selezione del profilo e volume comune, mentre i filtri di progetto saranno preparati e verificati prima. Il client attuale espone soltanto stato, silenzio, laboratorio e attesa: non offre ancora un selettore dei profili finali. L'ecosistema ufficiale comprende CamillaGUI, un'interfaccia web, ma non è stata installata o collaudata in questo setup. Una schermata utente pronta non viene dedotta dalla presenza del motore.

Con questa architettura il computer Ubuntu deve essere acceso e la sessione utente disponibile; Linger è no. Il DSP non è promesso prima del login o con il PC spento. Se l'ascolto futuro richiederà una sorgente autonoma dal computer, quel requisito dovrà entrare nella scelta della catena prima degli acquisti.

## Home recording e ascolto durante la registrazione

Il percorso dei monitor serve a sentire il mix. L'ingresso di microfoni e strumenti nella DAW rimane un percorso distinto, progettato con l'interfaccia comune. L'ascolto del musicista in registrazione, soprattutto in cuffia, richiede una scelta di monitoraggio e una misura della latenza; non si assume che debba fare il giro completo dei monitor a quattro vie. L'eventuale monitoraggio diretto dipenderà dalle funzioni realmente disponibili e verificate dell'interfaccia.

Il sistema è stato osservato con 48 kHz e quantum 1024. Questi valori non certificano bassa latenza per suonare o cantare. Prima di ridurre i buffer si confronteranno stabilità e carico reale: cambiare un numero senza una prova non completa l'ottimizzazione. I collaudi virtuali non misurano ritardo dei convertitori, rumore elettronico o risposta della stanza.

## Cosa possiamo già usare e cosa resta da costruire

Sono disponibili il motore, il controllo locale, il banco verificato, i sorgenti versionabili e i tre modelli CAD esplorativi. Il backup finale del 19 novembre è stato riletto e copiato su supporto esterno. Il progetto esecutivo richiede ancora posizione e appoggi reali sul tavolo, target, confronto dei driver e scelta di interfaccia e finali. Poi vengono misure in cassa, filtri definitivi e verifica dei profili mix/ascolto.

Per verificare lo stato da qui è stato eseguito sulla macchina Windows il seguente comando con l'alias SSH già configurato. È una lettura e non attiva un profilo:

```powershell
cd E:\diy-2way-monitors-home
& 'C:/Windows/System32/OpenSSH/ssh.exe' -o BatchMode=yes -o ConnectTimeout=6 -o ConnectionAttempts=1 studio '.local/bin/diy-monitor-dsp stato'
```

L'output osservato riporta versione 4.1.3, Inactive, mute true, volume_db -60.0 e stop_reason None. Per installazione, percorsi e prove ripetibili vedere [servizio utente e banco PipeWire](camilladsp-servizio-utente.md); per il confronto con le misure acustiche, [progettazione dei monitor](../50-progettazione-monitor.md).
