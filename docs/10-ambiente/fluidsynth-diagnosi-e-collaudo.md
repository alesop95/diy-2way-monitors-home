# FluidSynth: diagnosi del servizio MIDI e collaudo

Stato del 2026-11-19: causa dell'errore 218/CAPABILITIES individuata, correzione locale installata e servizio verificato anche con un nuovo manager della sessione utente. Prova funzionale MIDI su istanza isolata riuscita con controllo senza note. PA-040 compiuta. Questa pagina distingue la prova dell'avvio da quella della produzione di audio attraverso MIDI; non certifica latenza o periferiche fisiche.

## Causa misurata

L'unità della distribuzione usa PrivateUsers=yes insieme a ProtectKernelModules e ProtectKernelLogs. Sulla macchina systemd è 259.5-0ubuntu3.4, FluidSynth 2.4.8+dfsg-1; kernel.apparmor_restrict_unprivileged_userns vale 1. systemd-detect-virt risponde none. La lettura del journal kernel mostra il passaggio del processo esecutore al profilo AppArmor unprivileged_userns e il rifiuto di setpcap. Il guasto riguarda la preparazione del processo, non il SoundFont o il driver MIDI.

Le unità transitorie della prova eseguono soltanto /usr/bin/true, con nomi nuovi e raccolta automatica al termine. La tabella riporta i processi realmente eseguiti; codice 218 significa che non raggiungono quel programma.

| Proprietà aggiunte al caso base | Codice di uscita |
|---|---|
| Nessuna | 0 |
| PrivateUsers=yes | 0 |
| PrivateUsers e ProtectHostname | 0, con avviso sul namespace UTS |
| PrivateUsers, ProtectSystem=full e ProtectHome=read-only | 0 |
| Tutte le protezioni dell'unità distribuita | 218 |
| PrivateUsers e ProtectKernelTunables | 0 |
| PrivateUsers e ProtectKernelModules | 218 |
| PrivateUsers e ProtectKernelLogs | 218 |
| PrivateUsers e ProtectControlGroups | 0 |
| Protezioni distribuite senza ProtectKernelModules e ProtectKernelLogs | 0, con avviso UTS |
| PrivateUsers e NoNewPrivileges | 0 |

Il [manuale systemd 259](https://www.freedesktop.org/software/systemd/man/259/systemd.exec.html) conferma che le due opzioni intervengono anche sull'insieme delle capability. La [documentazione Ubuntu su AppArmor](https://documentation.ubuntu.com/security/security-features/privilege-restriction/apparmor/) descrive le restrizioni applicabili ai namespace non privilegiati. La [segnalazione upstream AppArmor 585](https://gitlab.com/apparmor/apparmor/-/issues/585) descrive un'interazione analoga con l'esecutore systemd; è un riferimento di contesto, mentre la bisezione e il journal della macchina sono le prove del caso presente.

Il codice 0 di una prova non dimostra da solo l'efficacia di ogni isolamento. In particolare ProtectHostname rimane configurato ma il namespace UTS viene ignorato con un avviso. Non viene attribuito il problema a un contenitore, che non è stato rilevato, né viene dichiarata una protezione operante soltanto perché la relativa proprietà è presente.

## Comandi diagnostici eseguiti

Eseguire sulla macchina Ubuntu. Le prove dettagliate usano cartelle nuove sotto /tmp e nomi di unità unici, conservati nel livello privato con comandi completi e journal. Il primo tentativo di leggere la versione con systemd --version è fallito perché quel nome non è nel PATH; systemctl --version ha fornito la versione richiesta.

```bash
systemctl --version
uname -r
systemd-detect-virt
cat /proc/self/attr/current
sysctl kernel.unprivileged_userns_clone
sysctl kernel.apparmor_restrict_unprivileged_userns
sysctl user.max_user_namespaces
systemctl --user show fluidsynth.service -p ActiveState -p Result -p ExecMainStartTimestamp -p ExecMainStatus -p FragmentPath -p DropInPaths
systemctl --user cat fluidsynth.service
apt-cache policy fluidsynth systemd apparmor
cat /etc/default/fluidsynth
fluidsynth -a help
fluidsynth -m help
```

Le unità isolate sono lanciate con systemd-run --user --wait --pipe --collect, Type=oneshot e TimeoutStartSec=5s, aggiungendo una proprietà alla volta. Non hanno modificato l'unità originale. Sono disponibili i backend audio ALSA, file, JACK, OSS, PipeWire, PulseAudio e SDL3; i backend MIDI includono alsa_seq. Il SoundFont configurato è /usr/share/sounds/sf3/default-GM.sf3, con opzioni -r 48000 -z 512. Sono dati letti, non ancora una prova del percorso audio.

## Passi di correzione e criterio di riuscita

Prima della modifica persistente va provata un'istanza isolata con le due sole opzioni incompatibili disattivate. Il test deve inviare un MIDI noto, osservare un segnale audio in una destinazione virtuale e confrontarlo con un controllo senza note, senza inviare il segnale ai diffusori. Solo dopo si prepara un nuovo drop-in dell'utente, lasciando intatta l'unità distribuita. Non si disabilita AppArmor e non si modifica il sysctl globale.

La correzione è un adattamento locale dell'unità: rinuncia a due restrizioni supplementari del servizio e mantiene i permessi dell'utente ordinario e le policy globali. Non equivale a conservare tutte le protezioni originariamente richieste.

## Prova funzionale eseguita

Istanza transitoria con Type=notify, stesse protezioni salvo le due incompatibili, MIDI alsa_seq e uscita PulseAudio indirizzata esplicitamente a un sink virtuale dedicato. Inviato con aplaymidi un file MIDI costruito: programma 80, nota 69, velocità 80, durata un secondo; secondo file identico con velocità zero. Cattura del monitor con parec in float32 stereo a 48000 Hz. I due file contengono ciascuno 229376 frame: nel caso con nota picco 0,0324892178 e valore efficace 0,0047515780, nel controllo picco e valore efficace zero. Non inviato MIDI al servizio originale o ai diffusori fisici.

La prima corsa produceva già i segnali attesi ma il controllo dei predefiniti falliva: il sink iniziale era auto_null, ancora provvisorio durante l'avvio del manager audio. Un tentativo di ripristino si ferma prima di cambiare preferenze, perché quel dispositivo non esiste più. La prova corretta attende due predefiniti non provvisori stabili per cinque osservazioni a distanza di 0,2 secondi; se non si stabilizzano entro quindici secondi termina senza creare il laboratorio. Ripetuta: segnale e controllo riusciti, predefiniti invariati, istanza fermata e sink rimosso. Il primo fallimento resta conservato, non viene contato come collaudo riuscito.

## Installazione eseguita e verifica

Creato il solo file prima assente `~/.config/systemd/user/fluidsynth.service.d/20-userns-compat.conf`, il cui modello vive nel repository sotto config/systemd/fluidsynth.service.d/. L'installazione usa apertura esclusiva e rifiuta file o collegamenti già presenti; non sovrascrive personalizzazioni. Il contenuto operativo è:

```ini
[Service]
ProtectKernelModules=no
ProtectKernelLogs=no
```

Il seguente blocco Python riporta la creazione esclusiva eseguita nel programma di installazione, compresi i commenti del modello verificati per impronta. Rifiuta la ripetizione quando il file esiste già.

```python
import pathlib
content = '''# Compatibilità locale verificata su Ubuntu Studio, 2026-11-19.
# Il profilo AppArmor unprivileged_userns nega setpcap durante
# la preparazione di queste due opzioni: errore 218/CAPABILITIES.
# Si mantengono unità distribuita, PrivateUsers e policy globali.
# Diagnosi, limiti e ripristino: docs/10-ambiente/fluidsynth-diagnosi-e-collaudo.md
[Service]
ProtectKernelModules=no
ProtectKernelLogs=no
'''
target = pathlib.Path.home() / '.config/systemd/user/fluidsynth.service.d/20-userns-compat.conf'
if target.exists() or target.is_symlink():
    raise RuntimeError('Existing drop-in will not be overwritten: ' + str(target))
target.parent.mkdir(parents=True, exist_ok=True)
with target.open('x', encoding='utf-8', newline='\n') as handle:
    handle.write(content)
```

Comandi successivi eseguiti sulla macchina Ubuntu:

```bash
systemctl --user daemon-reload
systemctl --user start fluidsynth.service
systemctl --user show fluidsynth.service -p ActiveState -p SubState -p Result -p MainPID -p ExecMainStartTimestamp -p UnitFileState -p DropInPaths
systemctl --user --failed --no-pager
systemctl --failed --no-pager
```

Il primo avvio riesce alle 17:36:00 CET. Nell'accesso successivo, nuovo manager utente e nuovo processo FluidSynth avviati alle 17:36:55: active/running, Result=success, enabled, timestamp non vuoto. Zero unità fallite sia utente sia sistema. PipeWire e DSP attivi, pipeline DSP Inactive, mute true e -60 dB. Linger rimane no: l'avvio è con la sessione utente.

L'unità della distribuzione conserva SHA-256 75f0035be01c7ba5ea0d63fdc288468b4c7e3edb513ec60d9be0cd8d0c267730 prima e dopo. Modello locale e drop-in installato coincidono: 4c5814524d0d9814ad8e2e974d073169dd92f992530f3e5fe6f7cc40fc31efcb. Sysctl AppArmor ancora a 1; nel processo osservato identità ordinaria, capability effettive, permesse, ereditabili e ambientali a zero, NoNewPrivs pari a 1. Questa lettura del processo non va confusa con la proprietà esplicita NoNewPrivileges dell'unità, che è no.

Per annullare la correzione, l'utente può rimuovere esattamente il nuovo drop-in indicato, poi ricaricare le unità e riavviare il servizio. Il rollback è preparato ma non eseguito: ripristina la richiesta delle due protezioni incompatibili e quindi il difetto già riprodotto. Non rimuovere l'intera cartella degli override, che potrebbe contenere altre personalizzazioni.

## Evidenze e limiti residui

Prove persistenti in `~/electroacoustics/collaudi/fluidsynth-20261119`: 91 file verificati, 7401517 byte prima del manifesto aggiuntivo; copia nel livello privato della postazione. Comprendono la corsa fallita del banco, quella corretta, bisezione, installazione, nuova sessione e copia del drop-in. Non sostituiscono il backup finale Veeam e non alterano il kit CAD precedente.

Il journal conserva l'avviso UTS e quattro avvisi GLib g_param_spec/validate_pspec già visibili nell'istanza isolata; non bloccano l'avvio o il segnale misurato, ma non sono dichiarati risolti. Non è stata fatta una misura di rumore, latenza o stabilità sotto carico DAW; il backend PulseAudio della prova isolata è una scelta del banco, non una nuova preferenza del servizio originale.

## Troubleshooting osservato

Sintomo: unità fallita con ExecMainStatus 0. Causa dell'interpretazione errata: il processo principale non è stato avviato, come dimostra ExecMainStartTimestamp vuoto, mentre il risultato dell'unità è exit-code. Rimedio diagnostico: leggere insieme risultato, timestamp e journal, senza usare lo zero del processo non eseguito come prova di successo.

Sintomo: 218/CAPABILITIES anche con /usr/bin/true. Causa misurata: tentativo di modificare le capability da un processo soggetto al profilo unprivileged_userns, attivato dalle due proprietà isolate. Rimedio collaudato: drop-in locale limitato a quelle due opzioni; nessuna protezione globale cambiata. Mantenere la verifica di avvio e del segnale quando un aggiornamento di distribuzione permetterà di riesaminare il workaround.
