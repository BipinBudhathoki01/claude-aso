param(
    [ValidateSet('claude', 'codex')]
    [string]$Runtime = 'claude',
    [string]$DestinationRoot
)
$ErrorActionPreference = 'Stop'
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $DestinationRoot) {
    if ($Runtime -eq 'codex') {
        $ConfigRoot = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE '.codex' }
    } else { $ConfigRoot = Join-Path $env:USERPROFILE '.claude' }
    $DestinationRoot = Join-Path $ConfigRoot 'skills'
}
$Name = if ($Runtime -eq 'codex') { 'claude-aeo' } else { 'aeo' }
$Target = Join-Path $DestinationRoot $Name
if (Test-Path -LiteralPath $Target) { throw "Destination already exists: $Target. Back it up or remove it before reinstalling." }
New-Item -ItemType Directory -Path $Target -Force | Out-Null
foreach ($Entry in @('SKILL.md', 'CLAUDE.md', 'AGENTS.md', 'LICENSE', 'skills', 'agents', 'data', 'scripts', 'templates', 'extensions', 'docs', 'examples')) {
    Copy-Item -LiteralPath (Join-Path $Here $Entry) -Destination $Target -Recurse
}
if ($Runtime -eq 'claude') {
    Copy-Item -LiteralPath (Join-Path $Here 'skills/aeo/SKILL.md') -Destination (Join-Path $Target 'SKILL.md') -Force
}
Write-Host "Installed to $Target. Restart your AI runtime to discover the skill."
