# Trasferisce i materiali pesanti del progetto sulla macchina Ubuntu Studio.
# Equivalente PowerShell di transfer-to-studio.sh, per chi lavora dalla postazione
# Windows senza Git Bash. Non cancella nulla sull'origine: la rimozione resta una
# decisione manuale, da prendere dopo che il confronto delle impronte e' riuscito.
#
# Uso:
#   powershell -NoProfile -ExecutionPolicy Bypass -File tools\transfer-to-studio.ps1 -SoloVerifica
#   powershell -NoProfile -ExecutionPolicy Bypass -File tools\transfer-to-studio.ps1

[CmdletBinding()]
param(
    [string]$StudioHost = 'alesop95@192.168.10.204',
    [string]$StudioBase = 'electroacoustics',
    [switch]$SoloVerifica
)

# Deliberatamente 'Continue' e non 'Stop': ssh e scp scrivono diagnostica su stderr
# anche quando il messaggio non e' fatale, e con 'Stop' PowerShell la promuove a
# errore terminante abortendo lo script prima dei suoi percorsi d'errore puliti.
# Il controllo di correttezza qui e' esplicito: ogni comando nativo viene seguito
# dalla verifica di $LASTEXITCODE, e ogni percorso viene verificato con Test-Path.
$ErrorActionPreference = 'Continue'

function Write-Nota   { param([string]$Testo) Write-Host "  $Testo" }
function Write-Titolo { param([string]$Testo) Write-Host "`n== $Testo ==" }
function Write-Errore { param([string]$Testo) Write-Host "ERRORE: $Testo" -ForegroundColor Red }

$Radice    = Split-Path -Parent $PSScriptRoot
$Materiali = Join-Path $Radice 'Akabak + VACS'
$Docx      = 'full_electroacoustics.docx'
$DocxSotto = '_notes'   # il sorgente e' archiviato sotto _notes/, ignorato da git

# Mappa origine -> sottocartella di destinazione.
$Mappa = @(
    @{ Nome = 'AKABAK_Pro_v324b126.exe';                                Sotto = 'installers' }
    @{ Nome = 'VACS_64_v213b33.exe';                                    Sotto = 'installers' }
    @{ Nome = 'VACS_32_v213b33.exe';                                    Sotto = 'installers' }
    @{ Nome = 'AKABAK-Examples.zip';                                    Sotto = 'examples'   }
    @{ Nome = 'Gmail - Akabak 3 license.pdf';                           Sotto = 'licenze'    }
    @{ Nome = 'update AKABAK (Joerg Panzer)_2026-03-19_10-18-32.jpg';   Sotto = 'licenze'    }
    @{ Nome = 'randteam.url';                                           Sotto = 'licenze'    }
)

Write-Titolo 'Controlli preliminari'

foreach ($strumento in @('ssh', 'scp')) {
    if (Get-Command $strumento -ErrorAction SilentlyContinue) {
        Write-Nota "$strumento presente"
    } else {
        Write-Errore "$strumento non trovato: installare la funzionalita' OpenSSH Client di Windows"
        exit 1
    }
}

if (-not (Test-Path -LiteralPath $Materiali -PathType Container)) {
    Write-Errore "cartella dei materiali non trovata: $Materiali"
    exit 1
}
Write-Nota 'cartella dei materiali trovata'

$daCopiare = @()
$assenti = $false
foreach ($voce in $Mappa) {
    $percorso = Join-Path $Materiali $voce.Nome
    if (Test-Path -LiteralPath $percorso -PathType Leaf) {
        $daCopiare += @{ Percorso = $percorso; Nome = $voce.Nome; Sotto = $voce.Sotto }
    } else {
        Write-Errore "file di origine assente: $($voce.Nome)"
        $assenti = $true
    }
}
$percorsoDocx = Join-Path (Join-Path $Radice $DocxSotto) $Docx
if (Test-Path -LiteralPath $percorsoDocx -PathType Leaf) {
    $daCopiare += @{ Percorso = $percorsoDocx; Nome = $Docx; Sotto = 'sorgenti' }
} else {
    Write-Nota "avviso: $Docx non presente sotto $DocxSotto/, verra' saltato"
}
if ($assenti) {
    Write-Errore 'manifest e disco non coincidono, controllare prima di trasferire'
    exit 1
}
Write-Nota 'tutti i file del manifest sono presenti'

$byteTotali = ($daCopiare | ForEach-Object { (Get-Item -LiteralPath $_.Percorso).Length } | Measure-Object -Sum).Sum
Write-Nota "da trasferire: $([math]::Round($byteTotali / 1MB)) MiB in $($daCopiare.Count) file"

Write-Titolo "Raggiungibilita' dell'host"

$null = & ssh -o BatchMode=yes -o ConnectTimeout=10 $StudioHost 'echo raggiungibile' 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Errore "$StudioHost non risponde"
    Write-Errore 'verificare che la macchina sia accesa, sullo stesso segmento di rete, e con sshd attivo'
    Write-Errore 'diagnostica: ping dell indirizzo, presenza in tabella ARP, ascolto sulla porta 22'
    exit 2
}
Write-Nota "$StudioHost risponde"

$spazioKib = (& ssh -o BatchMode=yes $StudioHost 'df -Pk "$HOME" | awk ''NR==2 {print $4}''').Trim()
Write-Nota "spazio disponibile in home sulla destinazione: $([math]::Round([int64]$spazioKib / 1024)) MiB"
if (([int64]$spazioKib * 1024) -lt ($byteTotali * 2)) {
    Write-Errore 'spazio insufficiente: serve almeno il doppio dei byte da trasferire per lavorare con margine'
    exit 3
}

if ($SoloVerifica) {
    Write-Titolo 'Solo verifica: nessun file copiato'
    exit 0
}

Write-Titolo 'Creazione dell albero di destinazione'
& ssh -o BatchMode=yes $StudioHost "mkdir -p `"`$HOME/$StudioBase`"/{installers,examples,licenze,sorgenti}"
Write-Nota "albero creato sotto `$HOME/$StudioBase"

Write-Titolo 'Trasferimento con scp'
foreach ($voce in $daCopiare) {
    Write-Nota "$($voce.Nome) -> $($voce.Sotto)/"
    & scp -p $voce.Percorso "${StudioHost}:`$HOME/$StudioBase/$($voce.Sotto)/"
    if ($LASTEXITCODE -ne 0) {
        Write-Errore "copia fallita su $($voce.Nome), interrotto"
        exit 4
    }
}

Write-Titolo 'Verifica delle impronte'

$atteso = @{}
foreach ($voce in $daCopiare) {
    $atteso[$voce.Nome] = (Get-FileHash -LiteralPath $voce.Percorso -Algorithm SHA256).Hash.ToLower()
}

$righe = & ssh -o BatchMode=yes $StudioHost "cd `"`$HOME/$StudioBase`" && find . -type f -exec sha256sum {} +"
$ottenuto = @{}
foreach ($riga in $righe) {
    if ($riga -match '^([0-9a-f]{64})\s+\./[^/]+/(.+)$') {
        $ottenuto[$Matches[2]] = $Matches[1].ToLower()
    }
}

$differenze = 0
foreach ($nome in $atteso.Keys) {
    if (-not $ottenuto.ContainsKey($nome)) {
        Write-Errore "assente sulla destinazione: $nome"
        $differenze++
    } elseif ($ottenuto[$nome] -ne $atteso[$nome]) {
        Write-Errore "impronta diversa: $nome"
        $differenze++
    } else {
        Write-Nota "ok $nome"
    }
}

if ($differenze -eq 0) {
    Write-Titolo 'Trasferimento verificato: tutte le impronte coincidono'
    Write-Nota 'la rimozione dei file dall origine resta manuale e deliberata'
    exit 0
} else {
    Write-Errore "$differenze differenze rilevate: non rimuovere nulla dall origine"
    exit 4
}
