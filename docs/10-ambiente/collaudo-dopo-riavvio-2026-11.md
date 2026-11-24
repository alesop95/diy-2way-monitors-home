# Collaudo dopo il riavvio del 19 novembre

L'utente ha eseguito da PowerShell `ssh -t studio "sudo reboot"`. La chiusura della connessione non bastava a provare il nuovo avvio: la successiva lettura SSH osserva inizio del boot il 2026-11-19 alle 14:21:33 CET, mentre prima era il 17 novembre. Kernel rimasto 7.0.0-43-generic. Due connessioni iniziali si chiudono prima dell'accesso; il successivo tentativo autorizzato fuori sandbox riesce. Questo non dimostra da solo se la causa dei primi tentativi fosse il riavvio ancora in corso o il confinamento locale.

## Esiti verificati

| Perimetro | Risultato dopo il nuovo avvio |
|---|---|
| CPU | cpupower-gui enabled, Type=oneshot, Result=success, ExecMainStatus=0; esecuzione alle 14:21:40 |
| Policy CPU | Otto thread coperti, powersave, limiti configurati 800000 e 4000000 kHz |
| Audio della sessione | PipeWire, compatibilità PulseAudio e WirePlumber active/running |
| DSP prima delle prove | Servizio utente enabled/running, pipeline Inactive, mute true, -60 dB e configurazione null |
| Esposizione DSP | Unico ascolto API su 127.0.0.1:12341 |
| Clock PipeWire | Forzature 48000 Hz e quantum 1024 conservate |
| Kit del progetto | Tutte le 82 impronte del manifesto coincidenti |
| FreeCAD console | Versione 1.1.4, tre FCStd con vista riaperti e ricomputati, dodici pannelli validi e volumi corretti per variante |
| FreeCAD GUI | A24 aperto con Xvfb e configurazioni nuove; dodici pannelli visibili, immagine ispezionata, pianta lungo -Z, processo terminato 0 |
| Banco DSP | Normale, volume -6 dB, mute e lati scambiati ripetuti sul grafo virtuale; rapporto passed true |
| Ripristino del banco | Default audio invariati durante la prova, nessun nodo del banco residuo; DSP riportato Inactive, mute true, -60 dB e configurazione null |
| Unità di sistema fallite | Nessuna nella lettura eseguita |
| Unità utente fallite | FluidSynth, da correggere separatamente: PA-040 |

Il profilo CPU è applicato al boot: lo stato inactive/dead segue il completamento riuscito del servizio oneshot. Non è un blocco di frequenza a 800 MHz e non misura consumo, rumore o stabilità sotto DAW.

I servizi audio sono servizi della sessione utente. La proprietà Linger è no; nella lettura prima del banco il nuovo manager li aveva avviati alle 14:24:41, durante l'accesso utente. Questo prova la disponibilità dopo riavvio e accesso, non l'esecuzione senza login. Non è stato abilitato il linger o un accesso grafico automatico.

## Letture eseguite e criteri

Le seguenti letture sono state eseguite sulla macchina via SSH. Le configurazioni di collaudo sono in una cartella nuova restituita da `mktemp -d /tmp/diy-postboot-20261119-XXXXXXXX`; percorsi compilati, identificativo di boot, processi e log integrali restano nelle prove private.

```bash
date -Iseconds
uptime -s
cat /proc/sys/kernel/random/boot_id
uname -r
systemctl show cpupower-gui.service -p Type -p ActiveState -p SubState -p Result -p ExecMainStatus -p ExecMainStartTimestamp -p UnitFileState
systemctl --user show pipewire.service pipewire-pulse.service wireplumber.service diy-monitor-dsp.service -p Id -p ActiveState -p SubState -p MainPID -p NRestarts -p ExecMainStartTimestamp -p UnitFileState
journalctl -b -u cpupower-gui.service --no-pager -n 30
loginctl show-user "$(id -u)" -p Linger -p State -p Sessions
systemctl --failed --no-pager
systemctl --user --failed --no-pager
"$HOME/.local/bin/diy-monitor-dsp" stato
```

La lettura delle policy ha confrontato i file affected_cpus, scaling_governor, scaling_min_freq e scaling_max_freq di tutte le cartelle policy sotto `/sys/devices/system/cpu/cpufreq/`; la loro unione copre CPU da 0 a 7. Il controllo API ha letto anche GetConfigJson e richiesto null, prima di caricare qualsiasi banco. Il dump PipeWire completo ha misurato le due forzature del clock e l'assenza di nodi di prova. La disponibilità del servizio non viene dedotta dalla sola abilitazione.

I tre nativi sono stati letti dalla copia persistente `~/electroacoustics/progetti/cabinet-st120-20261119/viste/`. Per ciascuno il controllo ricomputa il documento, conta i dodici Part::Box dei due cabinet e confronta il volume con `2*(W*D*H - (W-2*t)*(D-2*t)*(H-2*t))`, senza salvare sul file originale. Configurazioni FreeCAD e nuovi output sono separati dal kit. La successiva prova GUI usa la macro versionata cabinet-vista.FCMacro e produce una nuova copia, mai una sovrascrittura dell'originale.

Il comando del banco è stato eseguito nella forma seguente, con postboot_stage già impostata alla cartella nuova. Il servizio viene riportato alle condizioni iniziali anche se la prova fallisce; un semplice codice del launcher CAD non sostituisce il rapporto.

```bash
python3 "$HOME/.local/share/diy-2way-monitors/releases/pipewire-bench-1.0.1/collauda-dsp-pipewire.py" --dest "$postboot_stage/dsp" --mutazioni
systemctl --user restart diy-monitor-dsp.service
```

Ogni acquisizione positiva contiene 288000 frame a 48 kHz. Le sei somme normali differiscono da 0 dB al massimo di 0,0005 dB; le sei attenuate da -6 dB al massimo di 0,0005 dB. Il mute ha picco iniziale `5.877299145140569e-7` e zero a regime dal secondo 1. Lo scambio dei lati produce RoutingMismatch sul tono a 100 Hz. Rimane applicata l'eccezione verificata per il codice 1 del registratore pw-cat 1.6.2 al limite dei campioni, con lunghezza esatta e log vuoto; il generatore termina 0. La [procedura del banco](camilladsp-servizio-utente.md) descrive soglie e limiti.

## Conservazione e limiti

Le prove complete sono copiate su un percorso prima assente, `~/electroacoustics/collaudi/postboot-20261119`: 70 file verificati contro le sorgenti e un manifesto aggiuntivo, 20867112 byte prima del manifesto. Una copia è nel livello privato del repository. Contengono stato precedente alle prove, rapporti, sorgenti dei controlli, log, immagini e acquisizioni; il kit con le 82 impronte è rimasto invariato.

Questo collaudo chiude la verifica di persistenza di CPU e della disponibilità CAD/DSP dopo riavvio e accesso utente. Non chiude PA-036 nel suo insieme: mancano catena hardware, carico di home recording, risposta dei diffusori, backup finale dopo le modifiche e la correzione del servizio MIDI rilevato. Prima di un nuovo pieno Veeam va rivalutata la conservazione dei tre Full locali; non è stato avviato un backup in questo intervento.

## Troubleshooting: FluidSynth non raggiunge il processo principale

La lettura delle unità utente fallite ha trovato fluidsynth.service, abilitata e fornita da `/usr/lib/systemd/user/fluidsynth.service`, pacchetto 2.4.8+dfsg-1. Le letture di diagnosi eseguite sono:

```bash
systemctl --user show fluidsynth.service -p FragmentPath -p UnitFileState -p Result -p ExecMainStatus -p ExecStart -p ExecMainStartTimestamp
systemctl --user cat fluidsynth.service
journalctl --user -b -u fluidsynth.service --no-pager -n 70
apt-cache policy fluidsynth libfluidsynth3
```

Il journal mostra 218/CAPABILITIES prima di eseguire touch in ExecStartPre e rm in ExecStopPost, con Operation not permitted e un avviso sul namespace UTS richiesto da ProtectHostname. Il processo principale FluidSynth non parte: il suo ExecMainStatus pari a 0 non è prova di successo, perché ExecMainStartTimestamp è vuoto e Result è exit-code. Le opzioni di protezione dell'unità, comprese PrivateUsers e quelle che richiedono namespace, vanno diagnosticate nel contesto della distribuzione. Il journal non dimostra da solo quale impostazione sia la causa iniziale.

Nella ricognizione qui descritta non sono state alterate protezioni globali, file della distribuzione o impostazioni dell'utente. Aggiornamento successivo del 2026-11-19, MS-270/273: [causa isolata e correzione locale collaudata](fluidsynth-diagnosi-e-collaudo.md), con prova MIDI e nuovo manager utente. PA-040 è compiuta. CPU, CAD e banco CamillaDSP hanno gli esiti positivi riportati sopra; restano i collaudi hardware e sotto carico DAW.
