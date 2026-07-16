$ErrorActionPreference = 'Stop'
$Project = Split-Path -Parent $MyInvocation.MyCommand.Path
$BundledPython = 'C:\Users\jiang\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$Python = if (Test-Path -LiteralPath $BundledPython) { $BundledPython } else { (Get-Command python).Source }

Push-Location $Project
try {
    $SourceFiles = Get-ChildItem -LiteralPath $Project -Recurse -File | Where-Object {
        $_.FullName -notmatch '\\(build|dist|release|__pycache__|qa)\\' -and $_.Extension -in '.py', '.ps1', '.json', '.md', '.txt'
    }
    $SecretHit = $SourceFiles | Select-String -Pattern 'sk-[A-Za-z0-9_-]{20,}' -List
    if ($SecretHit) { throw "Share safety check failed: an API-key-like value exists in source files." }
    $PackagedState = Get-ChildItem -LiteralPath $Project -Recurse -Filter 'state.json' -File | Where-Object { $_.FullName -notmatch '\\(build|dist|release)\\' }
    if ($PackagedState) { throw "Share safety check failed: state.json must never be packaged." }
    & $Python -m pip install --disable-pip-version-check -r requirements.txt
    & $Python make_icon.py
    & $Python -m PyInstaller --noconfirm --clean --onefile --windowed `
        --name 'TingtingHeartbeat' `
        --icon 'assets\tingting.ico' `
        --add-data 'assets;assets' `
        --collect-all pystray `
        --hidden-import PIL._tkinter_finder `
        main.py
    if ($LASTEXITCODE -ne 0) { throw "PyInstaller failed with exit code $LASTEXITCODE" }
    Write-Host "Built: $Project\dist\TingtingHeartbeat.exe"
}
finally {
    Pop-Location
}
