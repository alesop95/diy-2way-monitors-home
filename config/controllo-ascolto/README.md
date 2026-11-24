# Pannello di ascolto: consegna e avvio

Software del progetto, con motore CamillaDSP 4.1.3 già disponibile. Il collaudo su Ubuntu ha usato istanze temporanee e file PCM; il servizio principale è rimasto Inactive, mute true, -60 dB. Questa consegna non installa o abilita automaticamente il pannello persistente. La regola AGENTS.md del progetto riserva il deploy all'utente.

Aggiornamento del 23 novembre, MS-317: il proprietario ha installato e avviato il pannello. Verifica SSH successiva: 24 file integri, servizio active/running senza riavvii, pagina/API/font raggiungibili e DSP in attesa silenziata. Il rapporto di installazione nel vault identifica il manifesto effettivamente trasferito. I comandi sotto restano la procedura per una nuova installazione: sulla macchina già installata non si ripetono estrazione e copia. Rimane da abilitare l'avvio automatico al login. Le successive correzioni documentali del kit non richiedono di reinstallare il runtime già verificato.

## Dipendenze e modi

Python 3, websockets 15.0.1, CamillaDSP 4.1.3. Per PC anche PipeWire, pw-dump e pw-link; per la qualifica ALSA anche amixer, procfs e sysfs. Il Pi richiede la propria compilazione ARM e la qualifica locale: il binario Ubuntu x86 non viene trasferito sul Pi. Edge e Node sono strumenti di QA Windows, non dipendenze del pannello. Nessuna nuova libreria è stata installata durante questo lavoro.

| Configurazione | Funzione e condizione |
|---|---|
| pannello-file.example.json | Banco isolato RawFile/File; deve essere presente un flusso di prova. Usare il collaudo per creare automaticamente FIFO, istanza e pulizia. |
| pannello-pipewire.example.json | Laboratorio virtuale. L'avvio del segnale richiede esattamente generatore → DSP → registratore del banco; i collegamenti all'hardware vengono respinti. |
| pannello-pc.example.json | PC qualificato PipeWire: grafo a due ingressi e quattro uscite, sink legato alla card osservata. L'esempio verified false viene respinto prima di aprire i profili mancanti. |
| pannello-alsa.example.json | Pi/host ALSA diretto: interfaccia completa e selezione delle quattro destinazioni fisiche. L'esempio non è qualificato. |

Le mappe example sono specifiche incomplete, non rilevamenti della UMC1820. Numeri di canale, formati, controlli clock, identità, nodi e porte devono provenire dalla qualifica differita. Non cambiare soltanto verified in true: servono prova coerente, hash dei profili normalizzati, routing fisico e catena del volume attestati. Gli hash rilevano modifiche; non costituiscono una firma o una protezione contro chi può riscrivere tutti i file.

## Riproduzione già collaudata dalla postazione

```powershell
python tools/test_controllo_ascolto.py
python tools/test_ascolto_alsa.py
python tools/test_ascolto_pipewire.py
python tools/test_pannello_ascolto.py
python tools/collauda-controllo-ascolto.py --ssh studio
python tools/collauda-controllo-ascolto.py --check
python tools/collauda-pannello-browser.py --check
```

La prova via SSH usa Python e il motore già presenti sulla macchina: invia un bundle temporaneo, misura quattro canali a 44,1 e 48 kHz e rimuove FIFO, PCM e processi propri. Non sostituisce la configurazione del servizio 12341. Un clock mancante è iniettato come condizione software; non viene staccato un dispositivo reale.

## Installazione persistente preparata, da eseguire manualmente

Il kit locale viene prodotto e verificato con `python tools/consegna_controllo.py`; contiene runtime, configurazioni, pagina, font locali e unità utente. Nessun binario DSP e nessuna prova privata di identità. La destinazione deve essere nuova: se esiste già, fermarsi e confrontare prima di aggiornare. Dalla radice del progetto su Windows:

```powershell
python tools/consegna_controllo.py --check
scp build/controllo-ascolto/controllo-ascolto.zip studio:controllo-ascolto.zip
ssh -t studio
```

Nella shell Ubuntu aperta con SSH, questi sono i comandi di installazione proposti, non dichiarati eseguiti:

```bash
set -e
test ! -e "$HOME/.local/opt/diy-listening-control" || exit 1
mkdir -p "$HOME/.local/opt/diy-listening-control"
python3 -m zipfile -e "$HOME/controllo-ascolto.zip" "$HOME/.local/opt/diy-listening-control"
cd "$HOME/.local/opt/diy-listening-control"
python3 tools/consegna_controllo.py --verify-installed .
python3 -c 'import websockets; assert websockets.__version__ == "15.0.1"; print(websockets.__version__)'
systemd-analyze --user verify config/systemd/user/diy-listening-control.service
mkdir -p "$HOME/.config/systemd/user"
test ! -e "$HOME/.config/systemd/user/diy-listening-control.service" || exit 1
cp config/systemd/user/diy-listening-control.service "$HOME/.config/systemd/user/"
systemctl --user daemon-reload
systemctl --user start diy-listening-control.service
systemctl --user status diy-listening-control.service --no-pager
```

Non serve sudo. Il servizio preparato avvia soltanto il pannello di laboratorio: nessun profilo viene preparato o abilitato al boot. La validazione systemd è una precondizione sul computer destinatario, non una prova di funzionamento dei diffusori. L'abilitazione permanente al login, dopo la verifica manuale, è `systemctl --user enable diy-listening-control.service`. Per arrestarlo: `systemctl --user stop diy-listening-control.service`; prova a lasciare muta la sola configurazione gestita. In assenza di RPC il silenzio non è garantito dal software.

Il percorso qualificato si avvia con lo stesso comando Python e un file di sessione proprio, mode pipewire-qualified sul PC oppure alsa sul Pi. Quel file punta a profili normalizzati, manifest e prova della relativa macchina. L'unità di laboratorio non viene convertita cambiando solo un flag: dopo la qualifica si prepara un override ExecStart verso il file di sessione effettivo. Sul Pi si usa il servizio DSP ALSA previsto in config/pi, senza dipendenza dal desktop PipeWire; pannello e API rimangono su loopback e l'accesso avviene sul Pi o tramite SSH. Finché mancano le prove fisiche, gli esempi qualificati sono deliberatamente respinti.

## Accesso e uso quotidiano

Sul PC Ubuntu aprire http://127.0.0.1:12342. Per consultarlo da Windows aprire un tunnel separato e poi lo stesso URL nel browser locale:

```powershell
ssh -N -L 12342:127.0.0.1:12342 studio
```

1. Scegliere Mix o Ascolto e premere Prepara il profilo: ritorno in mute a -60 dB, normalizzazione e rilettura della configurazione, collegamenti qualificati sul PC.
2. Impostare il livello richiesto e premere Avvia ascolto. Il livello effettivo è letto dal motore; il cursore da solo non disattiva il mute.
3. Silenzia porta mute e -60 dB. È possibile riabilitare esplicitamente una preparazione ancora valida. Un errore di clock, rate, identità o routing invece revoca la preparazione: occorre preparare nuovamente, anche se il dispositivo torna disponibile.

Il limite -6 dB è una policy di sviluppo, non una calibrazione SPL. La sorveglianza ogni 250 ms e le RPC con timeout non sono una protezione elettrica a tempo garantito. Per spegnimento improvviso, blocco del processo e transitori restano necessari il progetto delle protezioni e le prove hardware sospese. Sorgenti, decisioni, misure e limiti completi nel [manuale tecnico](../../docs/61-camilladsp-manuale-tecnico.md).
