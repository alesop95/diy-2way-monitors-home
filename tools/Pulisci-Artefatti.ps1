param([switch]$Applica, [switch]$ArchiviaSessioni)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$receiptPath = Join-Path $root '_notes/archivio-prove/riordino-corrente.json'
$previousReceipt = if (Test-Path -LiteralPath $receiptPath) { Get-Content -LiteralPath $receiptPath -Raw -Encoding UTF8 | ConvertFrom-Json } else { $null }
function Controlla-Percorso([string]$path) {
    $resolved = (Resolve-Path -LiteralPath $path).Path
    if (-not $resolved.StartsWith($root + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Percorso esterno al progetto' }
    if ((Get-Item -LiteralPath $resolved -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Collegamento non consentito' }
    return $resolved
}
$candidates = @()
$emptyDirs = @()
$manifestPath=Join-Path $root 'docs/pdf/manifest.json'
$published=$false
if (Test-Path -LiteralPath $manifestPath) {
    $manifest=Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
    foreach ($document in $manifest.documenti) {
        $path=Controlla-Percorso (Join-Path $root $document.pdf)
        if ((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $document.sha256) { throw 'PDF consegnato diverso dal manifesto' }
        foreach ($source in $document.sorgenti.PSObject.Properties) {
            $path=Controlla-Percorso (Join-Path $root $source.Name)
            if ((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $source.Value) { throw 'Sorgente cambiato dopo la consegna PDF' }
        }
    }
    $published=($manifest.documenti.Count -eq 3)
}
foreach ($relative in @('build/relazione-audio-20261120','build/recap-progetto-20261120')) {
    $folder = Join-Path $root $relative
    if (Test-Path -LiteralPath $folder) {
        $candidates += @(Get-ChildItem -LiteralPath $folder -File -Recurse -Force | Where-Object { $_.Extension -eq '.png' })
        if ($published) { $candidates += @(Get-ChildItem -LiteralPath $folder -File -Filter '*.pdf' | Where-Object { $_.Name -in @('recap-progetto.pdf','crossover-pc-pi-analogico.pdf','sistema-autonomo-driver-e-collaudo.pdf') }) }
    }
}
foreach ($dir in @(Get-ChildItem -LiteralPath (Join-Path $root 'build') -Directory | Where-Object { $_.Name -match '^(tmp|basso-)' })) {
    $checked=Controlla-Percorso $dir.FullName
    if (@(Get-ChildItem -LiteralPath $checked -Force).Count -eq 0) { $emptyDirs+=$checked }
}
$browser=Join-Path $root '_notes/edge-cabinet-20261119'
if (Test-Path -LiteralPath $browser) {
    $checked=Controlla-Percorso $browser
    $children=@(Get-ChildItem -LiteralPath $checked -Recurse -Force)
    if (@($children | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }).Count -gt 0) { throw 'Collegamento nel profilo temporaneo CAD' }
    $candidates+=@($children | Where-Object { -not $_.PSIsContainer })
}
$manuals = Join-Path $root '_notes/fonti-amplificatori'
if (Test-Path -LiteralPath $manuals) {
    $candidates += @(Get-ChildItem -LiteralPath $manuals -File -Recurse | Where-Object {
        ($_.Extension -eq '.png' -and $_.Name -match '^(marshall|eko-basso)-pagina-') -or
        ($_.Extension -eq '.pdf' -and $_.DirectoryName -ne $manuals -and $_.Name -in @('marshall-mg15-manuale-originale.pdf','eko-basso-manuale-originale.pdf'))
    })
}
$bank = Join-Path $root 'build/collaudo-profili-autonomi-20261120-finale-v5'
if (Test-Path -LiteralPath $bank) { $candidates += @(Get-ChildItem -LiteralPath $bank -File -Recurse -Filter '*.pcm') }
$records = @()
foreach ($file in @($candidates | Sort-Object FullName -Unique)) {
    $path = Controlla-Percorso $file.FullName
    $records += [ordered]@{ path = $path.Substring($root.Length+1).Replace('\','/'); bytes = $file.Length; sha256 = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant(); motivo = 'Derivato rigenerabile: QA, PDF intermedio/OCR, PCM sintetico o cache del browser di collaudo CAD' }
}
$archiveRecords = @()
$archiveInfo = $null
if ($ArchiviaSessioni) {
    $keep = @('RESUME-PROMPT.md','COMMIT-MSG.txt','.md-unwrap-ignore','chiudi-autonomia-20261120.py','chiudi-autonomia-20261120.txt','verifica-studio-crossover-20261120.py','verifica-studio-crossover-20261120.json')
    $archiveFiles = @(Get-ChildItem -LiteralPath (Join-Path $root '_notes') -File | Where-Object { $_.Name -notin $keep -and $_.Extension -in @('.py','.ps1','.sh','.md','.txt','.json','.log','.csv') })
    $historicDirs = @(Get-ChildItem -LiteralPath (Join-Path $root '_notes') -Directory | Where-Object { $_.Name -match '^(dsp-|fluidsynth-|postboot-|cabinet-collaudo-|collaudi-|esecuzioni-|fotografia-|backup-finale-collaudo-)' })
    foreach ($dir in $historicDirs) {
        $checked = Controlla-Percorso $dir.FullName
        $children = @(Get-ChildItem -LiteralPath $checked -Recurse -Force)
        if (@($children | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }).Count -gt 0) { throw 'Collegamento in una prova storica' }
        $archiveFiles += @($children | Where-Object { -not $_.PSIsContainer })
    }
    $archiveFiles = @($archiveFiles | Sort-Object FullName -Unique)
    if ($Applica -and $archiveFiles.Count -gt 0) {
        Add-Type -AssemblyName System.IO.Compression
        Add-Type -AssemblyName System.IO.Compression.FileSystem
        $zipPath = Join-Path $root '_notes/archivio-prove/sessioni-storiche.zip'
        if (Test-Path -LiteralPath $zipPath) { throw 'Archivio sessioni esistente: non sovrascrivo' }
        $zip = [IO.Compression.ZipFile]::Open($zipPath, [IO.Compression.ZipArchiveMode]::Create)
        try {
            foreach ($file in $archiveFiles) {
                $path = Controlla-Percorso $file.FullName
                $rel = $path.Substring($root.Length+1).Replace('\','/')
                $hash = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
                [IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip,$path,$rel,[IO.Compression.CompressionLevel]::Optimal) | Out-Null
                $archiveRecords += [ordered]@{ path=$rel; bytes=$file.Length; sha256=$hash }
            }
        } finally { $zip.Dispose() }
        $archiveInfo=[ordered]@{ path='_notes/archivio-prove/sessioni-storiche.zip'; bytes=(Get-Item -LiteralPath $zipPath).Length; sha256=(Get-FileHash -LiteralPath $zipPath -Algorithm SHA256).Hash.ToLowerInvariant(); membri_verificati=$archiveRecords.Count }
        $zip = [IO.Compression.ZipFile]::OpenRead($zipPath)
        try {
            if ($zip.Entries.Count -ne $archiveRecords.Count) { throw 'Conteggio ZIP diverso' }
            foreach ($record in $archiveRecords) {
                $entry = $zip.GetEntry($record.path)
                if (-not $entry -or $entry.Length -ne $record.bytes) { throw 'Voce ZIP diversa' }
                $stream = $entry.Open(); $algorithm = [Security.Cryptography.SHA256]::Create()
                try { $digest = [BitConverter]::ToString($algorithm.ComputeHash($stream)).Replace('-','').ToLowerInvariant() } finally { $stream.Dispose(); $algorithm.Dispose() }
                if ($digest -ne $record.sha256) { throw 'Impronta ZIP diversa' }
            }
        } finally { $zip.Dispose() }
    }
}
$sumBytes = [long]0
foreach ($record in $records) { $sumBytes += [long]$record.bytes }
if ($Applica -and $records.Count -eq 0 -and $archiveRecords.Count -eq 0 -and $emptyDirs.Count -eq 0) {
    [pscustomobject]@{ applicato=$false; nessuna_modifica=$true; derivati=0; bytes_derivati=0; ricevuta='_notes/archivio-prove/riordino-corrente.json' } | ConvertTo-Json
    return
}
$receipt = [ordered]@{ data = (Get-Date).ToString('o'); applicato=[bool]$Applica; cancellazioni=$records; cartelle_vuote=@($emptyDirs | ForEach-Object { $_.Substring($root.Length+1).Replace('\','/') }); archiviate=$archiveRecords; bytes_derivati=$sumBytes; stato='piano' }
if ($archiveInfo) { $receipt['archivio']=$archiveInfo }
if ($previousReceipt) {
    $history=@()
    $cursor=$previousReceipt
    while ($cursor) {
        if ($cursor.PSObject.Properties.Name -contains 'storico') { $history+=@($cursor.storico) }
        $prior=if ($cursor.PSObject.Properties.Name -contains 'precedente') { $cursor.precedente } else { $null }
        $copy=[ordered]@{}
        foreach ($property in $cursor.PSObject.Properties) {
            if ($property.Name -notin @('precedente','storico')) { $copy[$property.Name]=$property.Value }
        }
        $history+=,$copy
        $cursor=$prior
    }
    $receipt['storico']=$history
}
if ($Applica) {
    $receipt.stato='rimozione_in_corso'
    $receipt | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $receiptPath -Encoding UTF8
    foreach ($record in @($records)+@($archiveRecords)) {
        $path = Controlla-Percorso (Join-Path $root $record.path)
        if ((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $record.sha256) { throw 'File cambiato prima della rimozione' }
        Remove-Item -LiteralPath $path -Force
    }
    if ($ArchiviaSessioni) {
        foreach ($dir in $historicDirs) {
            $checked=Controlla-Percorso $dir.FullName
            if (@(Get-ChildItem -LiteralPath $checked -Recurse -File -Force).Count -ne 0) { throw 'File rimasti dopo archiviazione' }
            Remove-Item -LiteralPath $checked -Recurse -Force
        }
    }
    foreach ($checked in $emptyDirs) { Controlla-Percorso $checked | Out-Null; Remove-Item -LiteralPath $checked }
    foreach ($relative in @('build/relazione-audio-20261120','build/recap-progetto-20261120','_notes/fonti-amplificatori','_notes/edge-cabinet-20261119')) {
        $parent=Join-Path $root $relative
        if (Test-Path -LiteralPath $parent) {
            foreach ($dir in @(Get-ChildItem -LiteralPath $parent -Directory -Recurse | Sort-Object { $_.FullName.Length } -Descending)) {
                $checked=Controlla-Percorso $dir.FullName
                if (@(Get-ChildItem -LiteralPath $checked -Force).Count -eq 0) { Remove-Item -LiteralPath $checked }
            }
        }
    }
    if ((Test-Path -LiteralPath $browser) -and @(Get-ChildItem -LiteralPath $browser -Force).Count -eq 0) { $checked=Controlla-Percorso $browser; Remove-Item -LiteralPath $checked }
    $receipt.stato='compiuto'
    $receipt | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $receiptPath -Encoding UTF8
}
[pscustomobject]@{ applicato=[bool]$Applica; derivati=$records.Count; bytes_derivati=$receipt.bytes_derivati; file_sessione_archiviati=$archiveRecords.Count; ricevuta='_notes/archivio-prove/riordino-corrente.json' } | ConvertTo-Json
