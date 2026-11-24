# Verifica di Ubuntu Studio prima del trasferimento a casa

Ricognizione del 2026-11-17, MS-233. Questa pagina appartiene al blocco canonico condiviso con il progetto di home recording. Descrive comandi di sola lettura effettivamente eseguiti via SSH e distingue lo stato osservato dalle prove ancora da fare. Non certifica prestazioni audio, sicurezza o ripristino della macchina.

## Sequenza replicabile della ricognizione

Aprire la sessione SSH con l'alias `studio`, la cui destinazione è conservata nella configurazione privata della postazione. I comandi seguenti sono stati eseguiti sul sistema remoto, nell'ordine delle due ricognizioni; ogni blocco si può eseguire separatamente. Non richiedono `sudo`.

```bash
uname -r
cat /etc/os-release
lscpu
free -h
df -h / /home
cat /proc/cmdline
systemctl --failed --no-pager
systemctl status cpupower-gui --no-pager -l
journalctl -u cpupower-gui -n 18 --no-pager
lspci
cat /usr/lib/systemd/system/cpupower-gui.service
sed -n 1,90p /usr/bin/cpupower-gui
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_driver
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
cat /sys/devices/system/cpu/intel_pstate/no_turbo
systemctl --user show pipewire -p LimitRTPRIO -p LimitMEMLOCK
ps -C pipewire -C wireplumber -Lo comm,cls,rtprio
wpctl status
apt-cache policy cpupower-gui freecad
apt-get -s install --only-upgrade cpupower-gui
```

L'elenco APT è quello locale: non è stato eseguito `apt update`, quindi candidati e simulazione vanno riletti dopo l'aggiornamento degli indici e prima di installare. La simulazione osservata aggiorna il solo `cpupower-gui` da 1.0.0-6 a 1.0.0-6ubuntu0.26.04.3, senza installazioni o rimozioni aggiuntive. Per `freecad` gli indici locali non offrono un candidato: non si propone quindi `apt install freecad` come comando già verificato.

## Fotografia e criteri ancora aperti

Aggiornamento del 2026-11-18: collaudo CamillaDSP temporaneo su file riuscito, descritto in `camilladsp-collaudo-offline.md`; servizio CPU ancora fallito e backup visibili di settembre. Nessuna installazione persistente o modifica della configurazione audio.

Il sistema osservato è Ubuntu 26.04.1 con kernel 7.0.0-43-generic. CPU i7-6700, 16 GB di RAM, grafica Intel HD 530; circa 49 GiB disponibili su radice e 303 GiB su home. Blender 5.0.1, Ardour 9.0 e Wine 10.0 risultano nei pacchetti. Il kernel riceve già `preempt=full threadirqs rcu_nocbs=all`; PipeWire e WirePlumber sono attivi. I limiti del servizio PipeWire sono 95 e illimitato. La lettura dei soli processi non è una verifica completa della priorità dei thread audio durante il carico.

La lettura interattiva di `pw-metadata -n settings`, eseguita separatamente e poi interrotta perché resta in ascolto, ha mostrato frequenza forzata 48000 e quantum forzato 1024. Il rapporto 1024/48000 corrisponde a 21,33 ms, non alla latenza totale. Il solo dispositivo audio osservato è quello integrato, con uscita digitale selezionata nella sessione corrente. L'accesso SSH non prova la riproduzione udita, la corretta mappatura di un'interfaccia futura o l'assenza di interruzioni in registrazione.

La proposta completa di profili, macchina, interfaccia, misure e cabinet vive nel progetto canonico in `docs/55-proposta-sistema-home-recording.md`. Il trasferimento del software si chiude soltanto dopo correzione del servizio CPU, verifica di apertura e salvataggio dei progetti CAD/audio/Wine, prova del routing DSP e backup riletto. La prestazione audio finale richiede l'interfaccia e il carico di home recording; la risposta dei monitor richiede i prototipi. Non si rinnova una vecchia verifica per il solo fatto che la macchina risponde su SSH.

Aggiornamento 2026-11-18, MS-241 e MS-242: il [nuovo backup](backup-ottimizzazione-2026-11.md) è concluso, riletto e copiato sul disco esterno con entrambe le impronte verificate. I due vecchi archivi esterni e il loro descrittore sono stati rimossi dopo autorizzazione; i punti locali restano tre. L'utente ha aggiornato soltanto cpupower-gui alla 1.0.0-6ubuntu0.26.04.3: unità con config -a, servizio abilitato e terminato correttamente. Versione, journal e codice 0 verificati via SSH. La prova dopo riavvio resta aperta; il prossimo lavoro software è il CAD. La sequenza e il perché sono nella [procedura del lavoro remoto](lavoro-remoto-e-tracciabilita.md).

Aggiornamento del giro 18/19 novembre, MS-244: [FreeCAD 1.1.4 preparato e collaudato](freecad-collaudo-native.md), con geometria parametrica, riapertura FCStd, STEP e DXF reimportati, controllo negativo e GUI terminata correttamente. Comando utente, voce menu e campione persistente creati. Il prossimo lavoro software è il DSP persistente; la verifica dopo riavvio rimane aperta. Gli amplificatori posseduti sono inventariati nel repository canonico e non cambiano automaticamente il percorso hardware dei monitor.

## Troubleshooting osservato

### Il profilo CPU non viene applicato all'avvio

Osservato sulla macchina Ubuntu Studio il 2026-11-17. Sintomo: `cpupower-gui.service` è fallito e il journal riporta `cannot open display`. Il servizio installato esegue `/usr/bin/cpupower-gui config`; la versione è 1.0.0-6. Il [changelog Ubuntu della versione candidata](https://lists.ubuntu.com/archives/resolute-changes/2026-September/029924.html) documenta correzioni del servizio e dei flag per applicare i profili. Rimedio proposto, non eseguito: prendere un punto di ripristino, aggiornare gli indici e simulare nuovamente il solo aggiornamento del pacchetto; installarlo manualmente e verificare servizio, policy CPU e persistenza dopo riavvio. Non si presenta questo rimedio come già collaudato.

### Un comando di lettura non termina

Osservato dalla postazione Windows il 2026-11-17. `pw-metadata -n settings` stampa lo stato e resta a osservare i cambiamenti: una ricognizione che lo tratta come comando istantaneo non arriva ai comandi seguenti. Il processo è stato interrotto; i comandi successivi necessari sono stati rieseguiti separatamente. Non usare l'esito della pipeline come prova del loro completamento. Il secondo tentativo di raccolta con un intero script su stdin è stato interrotto e ha lasciato una cattura privata parziale; non è una prova completa della sequenza.

### Una espressione con alternative viene spezzata da PowerShell

Osservato sulla postazione Windows il 2026-11-17. Nel primo tentativo il filtro di `lspci` con alternative e virgolette interne è arrivato alla shell remota spezzato, producendo `3d: command not found` e `audio: command not found`. La ricognizione è stata ripetuta con `lspci` senza filtro, che ha mostrato la grafica Intel HD 530. L'errore del comando non descriveva l'assenza dell'hardware. La sequenza sopra usa il comando effettivamente riuscito.

Aggiornamento 2026-11-19, MS-246/256: [DSP persistente e banco PipeWire collaudati](camilladsp-servizio-utente.md), con segnale virtuale 2/4, volume, mute a regime, controllo negativo e ripartenza dopo guasto. Installatore verificato e copia persistente nella home. I timeout audio sono stati ripristinati nel campione riavviando il solo WirePlumber; la causa interna resta aperta. Il prossimo lavoro indipendente è lo studio degli ingombri, mentre la prova CPU/CAD/DSP dopo riavvio resta da eseguire.

Aggiornamento dopo il riavvio eseguito dall'utente il 2026-11-19: [collaudo CPU/CAD/DSP concluso](collaudo-dopo-riavvio-2026-11.md). Nuovo boot alle 14:21:33 CET, profilo CPU applicato, tre modelli e GUI riaperti, 82 impronte del kit coincidenti e banco DSP nuovamente riuscito. Il servizio DSP parte nella sessione utente, con Linger=no. L'unità FluidSynth allora fallita è stata [corretta e collaudata nella sessione successiva](fluidsynth-diagnosi-e-collaudo.md), PA-040 compiuta. Non occorre richiedere un altro riavvio per ripetere questa stessa verifica. Restano carico DAW, hardware, progetto acustico, backup finale e rete dopo il trasferimento.
