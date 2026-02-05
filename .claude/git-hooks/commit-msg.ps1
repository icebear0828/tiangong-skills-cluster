# TianGong Git Hook: commit-msg
# Lightweight Conventional Commits format validation
# Full validation available via: /git-commander commit

param([string]$msgFile)

if (-not $msgFile) {
    $msgFile = $args[0]
}

if (-not (Test-Path $msgFile)) {
    Write-Host "[TianGong] Warning: Cannot read commit message file" -ForegroundColor Yellow
    exit 0
}

$message = Get-Content $msgFile -Raw
$firstLine = ($message -split "`n")[0].Trim()

# Skip merge commits
if ($firstLine -match "^Merge ") { exit 0 }

# Conventional Commits pattern: type(scope): subject
$pattern = "^(feat|fix|docs|style|refactor|test|chore|ci)(\([a-zA-Z0-9_-]+\))?: .+"

if ($firstLine -notmatch $pattern) {
    Write-Host "`n[TianGong] INVALID: Commit message does not follow Conventional Commits format." -ForegroundColor Red
    Write-Host "`nExpected: <type>(<scope>): <subject>" -ForegroundColor Cyan
    Write-Host "Types: feat, fix, docs, style, refactor, test, chore, ci"
    Write-Host "`nExamples:" -ForegroundColor Green
    Write-Host "  feat(auth): add OAuth2 login support"
    Write-Host "  fix: resolve null pointer in user service"
    Write-Host "  docs(readme): update installation guide"
    Write-Host "`nTip: Use '/git-commander commit' for auto-generated commit messages"
    Write-Host ""
    exit 1
}

# Check subject length
if ($firstLine.Length -gt 72) {
    Write-Host "`n[TianGong] WARNING: Subject line exceeds 72 characters ($($firstLine.Length) chars)" -ForegroundColor Yellow
    Write-Host "Consider shortening the subject line."
    Write-Host ""
    # Warning only, don't block
}

exit 0
