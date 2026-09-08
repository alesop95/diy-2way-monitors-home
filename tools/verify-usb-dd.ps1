<#
.SYNOPSIS
    Confronta una copia grezza con l'immagine di origine, byte per byte via SHA-256.

.DESCRIPTION
    Confronta l'impronta SHA-256 dei primi N byte del dispositivo grezzo con quella del
    file immagine, dove N e' la dimensione esatta del file.

    QUANDO NON USARLO, e va letto prima del resto. Questo strumento NON serve a verificare
    una chiavetta di installazione appena scritta su Windows, e la sottofase 2.4 della
    procedura di installazione pulita non lo usa piu'. La ragione e' che Windows monta
    automaticamente i volumi del supporto e ripara la tabella delle partizioni quando la
    copia di sicurezza dell'immagine non si trova in fondo al disco: i byte cambiano per
    scritture legittime del sistema, e il confronto integrale produce un falso allarme su
    una chiavetta perfettamente valida. E' accaduto per davvero il 2026-09-08, ed e'
    documentato in MS-069. Per una chiavetta appena scritta la verifica giusta e' quella
    che il supporto fa su se stesso dal proprio menu di avvio.

    Quando usarlo. Confrontare una immagine con una copia grezza che nessun sistema
    operativo ha montato ne' riparato: per esempio l'archivio di un supporto prodotto con
    una copia diretta, o una scheda di memoria letta da un sistema che non la monta.

    Perche' esiste. Una copia scritta in modalita' DD e' un clone byte per byte del file,
    quindi e' l'unico caso in cui una copia grezza si possa confrontare con l'originale.
    Una scritta in modalita' immagine ISO non e' confrontabile con nulla, perche' il suo
    contenuto e' un filesystem nuovo costruito dallo strumento di scrittura, che nessuna
    impronta pubblicata descrive. Il confronto vale quindi solo per copie DD, e solo dove
    nessun sistema operativo sia intervenuto dopo la scrittura.

    Che cosa dimostra e che cosa no. Dimostra che i byte scritti coincidono con quelli
    del file, quindi che la scrittura non ha introdotto errori e che il supporto li ha
    conservati fino alla rilettura. Non dimostra che l'immagine sia autentica: quella e'
    una domanda diversa, a cui risponde la verifica della somma di controllo firmata
    descritta nella sottofase 2.2, e va fatta prima di questa.

    Richiede privilegi di amministratore, perche' leggere un dispositivo grezzo significa
    aprire \\.\PhysicalDriveN e non un file dentro un filesystem. E' di sola lettura:
    apre il dispositivo in lettura e non scrive un solo byte.

.PARAMETER DiskNumber
    Numero del disco fisico, quello che riporta Get-Disk. Da verificare due volte: il
    parametro identifica il dispositivo da leggere, e leggere il disco sbagliato non fa
    danni ma da' un esito privo di senso.

.PARAMETER ImagePath
    Percorso del file immagine con cui confrontare.

.PARAMETER ExpectedHash
    Facoltativo. Se indicato, si confronta anche l'impronta del file immagine con questo
    valore, cosi' che una sola esecuzione dica se il file e' quello atteso e se la
    chiavetta corrisponde al file.

.EXAMPLE
    powershell -NoProfile -ExecutionPolicy Bypass -File tools\verify-usb-dd.ps1 -DiskNumber 4 -ImagePath "C:\percorso\immagine.iso"
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)] [int]    $DiskNumber,
    [Parameter(Mandatory = $true)] [string] $ImagePath,
    [string] $ExpectedHash
)

$ErrorActionPreference = 'Stop'

function Scrivi-Riga([string]$Stato, [string]$Testo) {
    Write-Host ("  [{0}] {1}" -f $Stato, $Testo)
}

if (-not (Test-Path -LiteralPath $ImagePath)) {
    Write-Host "immagine inesistente: $ImagePath"
    exit 2
}

$immagine = Get-Item -LiteralPath $ImagePath
$dimensione = $immagine.Length

Write-Host "Verifica di una chiavetta scritta in modalita' DD"
Scrivi-Riga " " ("immagine:   {0}" -f $immagine.FullName)
Scrivi-Riga " " ("dimensione: {0:N0} byte" -f $dimensione)

# Un dispositivo grezzo si legge per settori: la dimensione deve essere un multiplo di
# 512, cosa che per una immagine ISO e' sempre vera perche' il suo blocco e' di 2048 byte.
# Se non lo fosse, la lettura dell'ultimo pezzo andrebbe troncata e il confronto diretto
# non sarebbe piu' possibile in questa forma: si dichiara e si esce invece di arrotondare.
if ($dimensione % 512 -ne 0) {
    Scrivi-Riga "!!" "la dimensione non e' un multiplo di 512: confronto non eseguibile per settori"
    exit 2
}

$disco = Get-Disk -Number $DiskNumber
Scrivi-Riga " " ("dispositivo: disco {0}, {1}, {2}, {3:N1} GB" -f `
    $disco.Number, $disco.FriendlyName, $disco.BusType, ($disco.Size / 1GB))

if ($disco.Size -lt $dimensione) {
    Scrivi-Riga "!!" "il dispositivo e' piu' piccolo dell'immagine: non puo' contenerla"
    exit 2
}

Write-Host ""
Write-Host "Impronta del file immagine"
$impronta_file = (Get-FileHash -LiteralPath $ImagePath -Algorithm SHA256).Hash.ToLower()
Scrivi-Riga "ok" $impronta_file

if ($ExpectedHash) {
    $atteso = $ExpectedHash.ToLower()
    if ($impronta_file -eq $atteso) {
        Scrivi-Riga "ok" "coincide con l'impronta attesa passata come parametro"
    } else {
        Scrivi-Riga "!!" "NON coincide con l'impronta attesa: l'immagine non e' quella giusta"
        exit 1
    }
}

Write-Host ""
Write-Host "Impronta dei primi $($dimensione.ToString('N0')) byte del dispositivo grezzo"

$percorso_grezzo = "\\.\PhysicalDrive$DiskNumber"
$blocco = 1MB
$sha = [System.Security.Cryptography.SHA256]::Create()
$flusso = $null
try {
    # FileShare ReadWrite perche' i volumi della chiavetta sono montati: senza questo
    # l'apertura fallirebbe con un errore di condivisione.
    $flusso = New-Object System.IO.FileStream(
        $percorso_grezzo,
        [System.IO.FileMode]::Open,
        [System.IO.FileAccess]::Read,
        [System.IO.FileShare]::ReadWrite)

    $buffer = New-Object byte[] $blocco
    [long]$letti = 0
    $ultima_percentuale = -1
    while ($letti -lt $dimensione) {
        $da_leggere = [int][Math]::Min([long]$blocco, $dimensione - $letti)
        $n = $flusso.Read($buffer, 0, $da_leggere)
        if ($n -le 0) {
            Scrivi-Riga "!!" ("lettura interrotta a {0:N0} byte" -f $letti)
            exit 1
        }
        $sha.TransformBlock($buffer, 0, $n, $null, 0) | Out-Null
        $letti += $n
        $percentuale = [int](100 * $letti / $dimensione)
        if ($percentuale -ne $ultima_percentuale -and $percentuale % 10 -eq 0) {
            Write-Host ("    {0}%" -f $percentuale)
            $ultima_percentuale = $percentuale
        }
    }
    $sha.TransformFinalBlock((New-Object byte[] 0), 0, 0) | Out-Null
} catch [System.UnauthorizedAccessException] {
    Scrivi-Riga "!!" "accesso negato: serve una sessione con privilegi di amministratore"
    exit 2
} finally {
    if ($flusso) { $flusso.Dispose() }
}

$impronta_disco = -join ($sha.Hash | ForEach-Object { $_.ToString('x2') })
$sha.Dispose()
Scrivi-Riga "ok" $impronta_disco

Write-Host ""
if ($impronta_disco -eq $impronta_file) {
    Write-Host "ESITO: la chiavetta e' identica all'immagine, byte per byte."
    Write-Host "La scrittura in modalita' DD e' riuscita e il supporto rilegge cio' che vi e' stato scritto."
    exit 0
} else {
    Write-Host "ESITO: le impronte NON coincidono."
    Write-Host "Le cause possibili, in ordine di probabilita'."
    Write-Host "  1. Il sistema operativo ha scritto sul supporto dopo la copia: monta i volumi,"
    Write-Host "     ripara la tabella delle partizioni, crea cartelle di servizio. Su Windows e'"
    Write-Host "     la causa piu' frequente, NON e' un guasto, e rende questo confronto inadatto"
    Write-Host "     a una chiavetta di installazione appena scritta. Vedi MS-069."
    Write-Host "  2. La scrittura e' avvenuta in modalita' immagine ISO invece che DD, quindi il"
    Write-Host "     contenuto e' una ricostruzione e non una copia."
    Write-Host "  3. E' stato indicato il disco sbagliato."
    Write-Host "  4. Il supporto non conserva cio' che scrive. E' l'ultima ipotesi, non la prima."
    exit 1
}
