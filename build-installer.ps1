param(
    [string]$Version = '1.6.2',
    [switch]$SkipAppBuild
)

$ErrorActionPreference = 'Stop'
$Project = Split-Path -Parent $MyInvocation.MyCommand.Path

Push-Location $Project
try {
    if (-not $SkipAppBuild) {
        & (Join-Path $Project 'build.ps1')
        if ($LASTEXITCODE -ne 0) { throw "Application build failed with exit code $LASTEXITCODE" }
    }

    $CompilerCandidates = @(
        (Join-Path $env:LOCALAPPDATA 'Programs\Inno Setup 6\ISCC.exe'),
        'C:\Program Files (x86)\Inno Setup 6\ISCC.exe',
        'C:\Program Files\Inno Setup 6\ISCC.exe'
    )
    $Compiler = $CompilerCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
    if (-not $Compiler) {
        throw 'Inno Setup 6 compiler was not found. Install JRSoftware.InnoSetup first.'
    }
    $Binary = Join-Path $Project 'dist\TingtingHeartbeat.exe'
    if (-not (Test-Path -LiteralPath $Binary)) { throw "Missing application binary: $Binary" }

    & $Compiler "/DMyAppVersion=$Version" (Join-Path $Project 'installer.iss')
    if ($LASTEXITCODE -ne 0) { throw "Installer build failed with exit code $LASTEXITCODE" }

    $Installer = Join-Path $Project "release\TingtingHeartbeat-Setup-v$Version.exe"
    if (-not (Test-Path -LiteralPath $Installer)) { throw "Installer output was not created: $Installer" }
    Write-Host "Built installer: $Installer"
}
finally {
    Pop-Location
}
