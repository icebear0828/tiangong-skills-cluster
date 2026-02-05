# TianGong Git Hook: pre-commit
# Lightweight sensitive file detection (no Claude dependency)
# Full detection available via: /git-commander commit

$configPath = Join-Path $PSScriptRoot "..\git-config.json"
if (Test-Path $configPath) {
    $config = Get-Content $configPath -Raw | ConvertFrom-Json
    $patterns = $config.sensitive_patterns
    $whitelist = $config.sensitive_whitelist
} else {
    $patterns = @("\.env$", "\.env\..+$", "credentials\.json$", "secrets\.ya?ml$", ".*\.pem$", ".*\.key$", "id_rsa", ".*\.p12$")
    $whitelist = @(".env.example", "*.test.*", "*.spec.*")
}

$stagedFiles = git diff --staged --name-only
$violations = @()

foreach ($file in $stagedFiles) {
    if (-not $file) { continue }

    # Check whitelist
    $whitelisted = $false
    foreach ($wl in $whitelist) {
        if ($file -like $wl) {
            $whitelisted = $true
            break
        }
    }
    if ($whitelisted) { continue }

    # Check sensitive patterns
    foreach ($pattern in $patterns) {
        if ($file -match $pattern) {
            $violations += $file
            break
        }
    }
}

if ($violations.Count -gt 0) {
    Write-Host "`n[TianGong] BLOCKED: Sensitive files detected in staging area:" -ForegroundColor Red
    foreach ($v in $violations) {
        Write-Host "  - $v" -ForegroundColor Yellow
    }
    Write-Host "`nSuggestions:" -ForegroundColor Cyan
    Write-Host "  1. Add to .gitignore: $($violations -join ', ')"
    Write-Host "  2. Use 'git reset HEAD <file>' to unstage"
    Write-Host "  3. Use '/git-commander commit' for smart commit with full detection"
    Write-Host ""
    exit 1
}

exit 0
