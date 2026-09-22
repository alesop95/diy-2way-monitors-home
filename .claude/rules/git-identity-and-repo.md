# Identità git e bootstrap del repository

> Regola modulare. Definisce come scegliere l'identità git con cui si commetteranno e pusheranno le modifiche, come collegare il repository locale a GitHub tramite l'alias SSH corretto, e come proteggersi dal commit involontario con l'identità sbagliata su una macchina condivisa. Il commit e il push restano sempre operazioni manuali dell'utente: questa regola e la skill di inizializzazione preparano la configurazione, non committano e non pushano mai.

## Concetto

L'identità git, ovvero la coppia `user.name` e `user.email` con cui git firma i commit, e indipendente dall'account Claude Code e dalla chiave SSH[^1] usata per autenticarsi a GitHub. Su una stessa macchina possono convivere più identità: tipicamente una di lavoro e una personale. Il rischio concreto su un computer aziendale e committare un progetto personale con l'email di lavoro per distrazione, o viceversa. La regola e impostare sempre l'identità a livello locale di repository, così che ogni repo porti la firma giusta a prescindere dal default globale.

## Account Claude Code, un asse a parte e il re-auth silenzioso

L'account con cui Claude Code e autenticato e un terzo asse, distinto sia dall'identità git sia dalla chiave SSH: determina quale abbonamento e quali impostazioni di account si usano nella sessione, non chi firma i commit. Lo si seleziona con la variabile `CLAUDE_CONFIG_DIR`, una directory di configurazione per profilo. Su questa macchina le funzioni PowerShell `claude-account1`, `claude-account2` e `claude-account3`, definite nel profilo `Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1`, puntano rispettivamente a `%USERPROFILE%\.claude-account1`, `%USERPROFILE%\.claude-account2` e `%USERPROFILE%\.claude-account3`, mentre il comando `claude` nudo usa la directory di default `%USERPROFILE%\.claude`. Ogni directory conserva le proprie credenziali nel file `<dir>\.credentials.json`, separato dalle altre, quindi in linea di principio ogni profilo mantiene il proprio account.

Il legame fra una directory e il suo account, pero, non è garantito stabile, ed è la causa di un comportamento che sembra inspiegabile. Quando il token OAuth[^2] di una directory scade e il rinnovo automatico fallisce, cosa che può accadere dopo giorni di inattivita o in seguito a un riavvio, al primo avvio successivo Claude riapre l'autenticazione e adotta in modo silenzioso l'account che in quel momento risulta attivo nel browser su claude.ai, senza chiedere quale. Se il browser e loggato sull'account sbagliato, la directory viene ri-vincolata a quello. E esattamente il meccanismo per cui un riavvio sembra "scombussolare" gli account: una directory che era su un account si ritrova sull'altro perché al momento del re-auth il browser era su quell'altro, non per un guasto del profilo.

Ne discende la regola operativa. Il binding di una directory non va mai dedotto dal suo nome ma verificato a inizio sessione con `/status`, o leggendo il campo `emailAddress` in `<dir>\.claude.json`. La mappatura per convenzione su questa macchina e `.claude-account1` su asopranzi@intrawelt.com, `.claude-account2` su un secondo account non verificato in questa sessione (da leggere con `/status`, non da assumere) e `.claude-account3` su tvezeni@intrawelt.com, ma resta una convenzione, non un invariante. Per riportare o cambiare l'account di una directory si imposta prima il browser su claude.ai sull'account desiderato, e solo dopo, in una sessione avviata con quel `CLAUDE_CONFIG_DIR`, si eseguono `/logout` e `/login`, confermando infine con `/status`. Toccare l'altra directory mentre il browser e ancora sull'account sbagliato la ri-vincolerebbe a sua volta a quello: il browser va sempre allineato prima di ogni `/login`.

Questo asse resta indipendente dall'identità git descritta sotto. Un progetto personale può girare sotto l'account Claude di lavoro e farsi comunque firmare i commit dall'identità git personale: i due assi non devono coincidere e si verificano separatamente, l'account con `/status` e l'identità git con `git log -1 --format="%an <%ae>"`.

[^2]: *OAuth*, Open Authorization - protocollo di autorizzazione con cui Claude Code ottiene e rinnova un token di accesso all'account senza conservare la password; il token ha una scadenza e si rinnova tramite un refresh token, e quando il rinnovo non va a buon fine occorre ri-autenticarsi.

## GitHub CLI, il quarto asse: l'API non passa da SSH

Sezione istanziata su questa postazione il 2026-09-22, con i valori letti e non assunti, e corrisponde alla sezione che il template porta in forma generale. Dove il template dice di rilevare, qui sta il rilevamento già fatto, con la data, perché un valore letto una volta e non scritto va riletto ogni volta.

La cosa da capire prima di usarlo è che `gh` non parla con la piattaforma via SSH, e questo lo rende un asse a sé rispetto agli altri tre. SSH serve a `git push`, cioè a spostare oggetti fra due copie del repository; `gh` usa l'API HTTPS con un token OAuth conservato nel gestore credenziali del sistema operativo. Autenticare `gh` quindi non tocca né la chiave SSH, né l'alias host, né l'identità con cui i commit vengono firmati: gli assi sono quattro e si verificano separatamente. La conseguenza pratica è che `gh auth status` risponde a una domanda diversa da `ssh -T git@github-personal`, e nessuna delle due risposte implica l'altra: si può avere `gh` autenticato sull'account sbagliato mentre i push funzionano perfettamente, e il sintomo sarebbe una pull request aperta sul repository di qualcun altro.

### Lo stato rilevato su questa postazione

L'eseguibile è presente e risponde. È la versione 2.100.0 del 2026-09-03, installata in `C:\Program Files\GitHub CLI\gh.exe`, ed è raggiungibile per nome perché quella cartella è nel PATH.

L'autenticazione esiste e nomina l'account personale. `gh auth status` riporta l'accesso a `github.com` con l'account `alesop95`, il token conservato nel portachiavi del sistema e non in un file, l'account attivo, il protocollo delle operazioni git impostato su `ssh`, e gli ambiti `gist`, `read:org` e `repo`.

Ne segue che su questa postazione i quattro assi coincidono tutti sull'identità personale, cioè `user.name` e `user.email` di `alesop95`, la chiave `id_ed25519_personal` selezionata dall'alias `github-personal`, l'account della GitHub CLI `alesop95`, e l'account Claude Code che resta indipendente e si verifica con `/status`. La coincidenza va letta come un fatto misurato e non come una necessità: è precisamente perché possono divergere che si verificano uno per uno.

Il token vive nel portachiavi del sistema operativo, quindi nessun valore segreto entra in un file del repository, ed è la ragione per cui questa sezione può esistere in un file tracciato. Il repository, verificato lo stesso giorno, è pubblico: la documentazione di questo progetto è quindi leggibile da chiunque, il che non cambia nulla sul piano tecnico e rende il vincolo sui valori segreti nei file tracciati una condizione di riservatezza e non una formalità.

### Il comando non si chiama `gh` finché non si riapre il terminale

Vale anche qui, e va detto perché il messaggio di errore sembra un'installazione fallita mentre l'eseguibile c'è e funziona. Un processo eredita le variabili d'ambiente quando parte e non le rilegge mai più: l'installatore aggiorna il PATH permanente della macchina, non quello del terminale già aperto. Riaprire il terminale risolve, e nella sessione corrente si invoca l'eseguibile per percorso completo. È la quarta causa della sezione sul contesto di shell di `git-commands-format.md`, ed è la stessa forma del gruppo `veeam` mancante in una sessione nata prima dell'installazione del pacchetto.

### L'alias SSH e il riconoscimento del repository, misurato qui e non presunto

Il template avverte che `gh` ricava il repository leggendo il remoto `origin`, e che un remoto costruito su un alias host può non essere riconosciuto, perché l'alias non è un host reale. L'avvertenza è formulata come possibilità e va verificata dove si lavora, non riportata.

Su questa postazione non si verifica. Il remoto di questo repository è `git@github-personal:alesop95/diy-2way-monitors-home.git`, quindi porta l'alias, e `gh repo view` senza alcun flag lo riconosce correttamente come `alesop95/diy-2way-monitors-home`, con codice di uscita zero. Misurato il 2026-09-22 con la versione 2.100.0.

Ne segue che il flag `-R <owner>/<repo>` resta una precauzione e non una necessità, e va usato comunque nei comandi che si consegnano, per due ragioni che non dipendono da questa misura: non costa nulla, e rende il comando indipendente dalla cartella in cui viene incollato, che è la terza causa della sezione sul contesto di shell. Quello che non si fa, e che è la tentazione da evitare, è cambiare il remoto all'host reale: l'alias è ciò che seleziona la chiave giusta fra quelle configurate, quindi toglierlo romperebbe il meccanismo a più identità per risolvere un problema che qui non esiste. Va evitato anche il comando che memorizza il repository nella configurazione git locale, perché aggiungerebbe una seconda fonte di verità su quale sia il repository, destinata a divergere dal remoto.

### Che cosa resta manuale, e perché

`gh` può anche fondere una pull request. Non lo si usa per quello. La regola per cui commit, push e merge restano gesti dell'utente non nasce da un limite tecnico ma da una scelta: l'agente prepara il lavoro, la decisione di farlo atterrare è di una persona. Uno strumento che rende facile automatizzare quella decisione non è una ragione per cambiarla, ed è esattamente il momento in cui conviene ribadirla, perché la comodità è il modo in cui le regole si erodono.

### L'autorizzazione è un legame durevole fra macchina e account

L'autenticazione crea un legame che sopravvive alla sessione e al progetto, quindi va tracciato dove questo progetto registra le operazioni manuali sui pannelli web, cioè in `docs/90-riferimenti/licenze-e-registrazioni.md`, con la data e il luogo in cui si revoca. Un legame che nessuno ha scritto è un legame che nessuno saprà sciogliere il giorno in cui questa macchina non servirà più.

## Profili disponibili su questa macchina

I profili si ricavano dagli alias host definiti in `C:\Users\Utente\.ssh\config`. Ogni alias fissa quale chiave usare verso `github.com`, e va abbinato all'identità corrispondente.

Profilo di lavoro: alias SSH `github-corp`, chiave `id_ed25519_corp`, identità `user.name` asopranzi e `user.email` asopranzi@intrawelt.com, organizzazione Intrawelt-SaaS.

Profilo personale: alias SSH `github-personal`, chiave `id_ed25519_personal`, identità `user.name` alesop95 e `user.email` alessio.sopranzi.95@gmail.com, utente GitHub alesop95. E il profilo con cui questo repository e già configurato, verificato con `git config --local --list`.

L'alias nudo `github.com` punta alla chiave di lavoro. La convenzione dei nomi degli alias, `github-personal` per l'identità personale e `github-corp` per quella di lavoro, e generale e si può adottare identica su qualsiasi macchina, così che la stessa logica di selezione del profilo valga ovunque. I valori concreti dietro ogni alias, cioè il percorso della chiave, lo `user.name` e lo `user.email`, sono invece specifici della macchina e su un altro ambiente vanno riletti dal relativo `~/.ssh/config` senza inventarli.

## Protezione globale dal commit con identità sbagliata

Una sola impostazione globale, da fare una volta per macchina, fa si che git rifiuti di committare in un repository dove non è stata impostata l'identità locale.

```bash
git config --global user.useConfigOnly true
```

Con questa impostazione git non ripiega mai sull'email globale: se il repo non ha `user.email` locale, il commit viene rifiutato finché non lo si imposta esplicitamente. Questo elimina il commit accidentale con l'email di lavoro mentre si sviluppa con identità personale. Essendo una modifica globale, va eseguita solo dopo conferma dell'utente.

## Bootstrap di un repository nuovo

Dalla cartella del progetto, l'inizializzazione di un repo nuovo e l'aggancio al remoto GitHub seguono questa sequenza. La parte di identità e remoto e quella che la skill prepara; il primo commit e il push li esegue l'utente.

```bash
cd "<path cartella>"

# Inizializza il repo e nomina main il branch di default
git init
git branch -M main

# Forza l'OpenSSH di sistema e l'identita SOLO per questo repo (Windows)
git config --local core.sshCommand "C:/Windows/System32/OpenSSH/ssh.exe"
git config --local user.name "alesop95"
git config --local user.email "alessio.sopranzi.95@gmail.com"

# Collega il remoto tramite l'alias SSH personale
git remote add origin git@github-personal:alesop95/<nome repo>.git
```

L'alias `github-personal` e definito in `C:\Users\Utente\.ssh\config` e usa la chiave personale `id_ed25519_personal`, quindi il remoto `git@github-personal:alesop95/<nome repo>.git` punta a `github.com/alesop95/<nome repo>` con quella chiave. Per il profilo di lavoro si sostituiscono identità e alias con quelli `github-corp` e l'owner con l'organizzazione di destinazione.

Differenza per sistema operativo: su Windows si forza `core.sshCommand` all'eseguibile OpenSSH indicato perché git per Windows porta un proprio `ssh` che potrebbe non leggere lo stesso config; su Linux questo passaggio e di norma superfluo, perché `ssh` di sistema e già sul PATH e legge `~/.ssh/config`, quindi si omette `core.sshCommand` oppure lo si imposta a `ssh`.

## Verifica della configurazione

Dopo aver impostato identità e remoto, verificare che tutto sia coerente.

```powershell
# Windows PowerShell
git config --local --list | Select-String "user\.|remote\.|core\.ssh"
```

```bash
# Linux / bash
git config --local --list | grep -E "user\.|remote\.|core\.ssh"
```

Test opzionale della connessione SSH verso l'alias scelto.

```bash
ssh -T git@github-personal
```

## Primo commit, push e caso del repo con README

Le operazioni seguenti sono dell'utente, non dell'agente.

```bash
git add .
git commit -m "Initial commit: <note del primo commit>"
git push -u origin main
```

Subito dopo il primo commit conviene confermare con quale identità e stato firmato.

```bash
git log -1 --format="%an <%ae>"
```

Se il repository su GitHub e stato creato con un README o una licenza automatica, esiste già un commit remoto e il push diretto verrebbe rifiutato. Si allinea con un rebase prima di pushare.

```bash
git pull origin main --rebase
git push -u origin main
```

Il rebase prende il commit già presente su GitHub, ad esempio il README generato alla creazione del repo, e vi colloca sotto il commit iniziale locale, producendo una storia lineare senza commit di merge e senza modificare alcun file di lavoro. Dalle volte successive il push e semplicemente `git push`.

## Vincolo

L'identità locale, il `core.sshCommand` e il remoto si preparano automaticamente; la protezione globale `user.useConfigOnly` si imposta solo su conferma. Commit e push restano sempre manuali.

[^1]: *SSH*, Secure Shell - protocollo con cui git si autentica a GitHub tramite una coppia di chiavi; l'alias host nel file di configurazione SSH seleziona quale chiave usare.
