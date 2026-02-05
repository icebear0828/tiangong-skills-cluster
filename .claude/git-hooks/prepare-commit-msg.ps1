# TianGong Git Hook: prepare-commit-msg
# Pre-fill commit message template with branch info

param([string]$msgFile, [string]$source)

if (-not $msgFile) {
    $msgFile = $args[0]
}
if (-not $source) {
    $source = $args[1]
}

# Only modify for new commits (not amend, merge, etc.)
if ($source) { exit 0 }

if (-not (Test-Path $msgFile)) { exit 0 }

$branch = git symbolic-ref --short HEAD 2>$null
if (-not $branch) { exit 0 }

# Extract type and scope from branch name
# Pattern: feature/auth-login → feat(auth):
# Pattern: fix/user-service-null → fix(user-service):
$branchPattern = "^(feature|fix|hotfix|release|chore)/(.+)$"

if ($branch -match $branchPattern) {
    $branchType = $Matches[1]
    $branchScope = $Matches[2]

    # Map branch prefix to commit type
    $typeMap = @{
        "feature" = "feat"
        "fix" = "fix"
        "hotfix" = "fix"
        "release" = "chore"
        "chore" = "chore"
    }

    $commitType = $typeMap[$branchType]
    if (-not $commitType) { $commitType = "chore" }

    # Extract scope (first segment before -)
    $scope = ($branchScope -split "-")[0]

    # Check if ticket number exists (e.g., PROJ-123)
    $ticketPattern = "([A-Z]+-\d+)"
    $ticket = ""
    if ($branchScope -match $ticketPattern) {
        $ticket = $Matches[1]
    }

    $currentMsg = Get-Content $msgFile -Raw
    if ($currentMsg -notmatch "^(feat|fix|docs|style|refactor|test|chore|ci)") {
        $template = "${commitType}(${scope}): "
        if ($ticket) {
            $template += "`n`n$ticket"
        }
        $template += "`n" + $currentMsg
        Set-Content $msgFile $template -NoNewline
    }
}

exit 0
