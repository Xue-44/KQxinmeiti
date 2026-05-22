# GitHub Sync Script - Weekly Memory Sync
# Runs every Sunday at 12:30 - syncs memory files only

$ErrorActionPreference = "Stop"
$logFile = "G:\openclaw\data\.openclaw\workspace\logs\github_sync.log"

function Write-Log {
    param($message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp - $message" | Out-File -FilePath $logFile -Append
}

try {
    $logDir = Split-Path $logFile -Parent
    if (!(Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }

    Write-Log "=== Starting GitHub Sync ==="

    $repoPath = "G:\openclaw\data\.openclaw\workspace\xinmeiti"
    $memorySrc = "G:\openclaw\data\.openclaw\workspace"
    $memoryDir = Join-Path $memorySrc "memory"
    $pat = "[已移除]"
    $remoteUrl = "https://github.com/Xue-44/KQxinmeiti.git"

    if (!(Test-Path $repoPath)) {
        Write-Log "Cloning repo..."
        git clone "https://github.com/Xue-44/KQxinmeiti.git" $repoPath
    }

    # Only sync memory/*.md files
    $memoryFiles = Get-ChildItem $memoryDir -Filter "*.md" -ErrorAction SilentlyContinue
    
    if ($memoryFiles) {
        Write-Log "Syncing memory files: $($memoryFiles.Name -join ', ')"
        
        foreach ($file in $memoryFiles) {
            $src = $file.FullName
            $dst = Join-Path $repoPath $file.Name
            Copy-Item $src -Destination $dst -Force
            Write-Log "Copied: $($file.Name)"
        }
    } else {
        Write-Log "No memory files to sync"
    }

    Set-Location $repoPath
    git config user.email "xinmeiti@kaiqi.com" 2>$null
    git config user.name "XinMeiti虾" 2>$null

    $status = git status --porcelain
    if ($status) {
        Write-Log "Changes detected, committing..."
        git add -A
        $commitMsg = "Weekly memory sync " + (Get-Date -Format "yyyy-MM-dd HH:mm")
        git commit -m $commitMsg
        git remote set-url origin $remoteUrl
        git push origin main
        Write-Log "Push successful!"
    } else {
        Write-Log "No changes to sync"
    }

    Write-Log "=== GitHub Sync Complete ==="
} catch {
    Write-Log "ERROR: $($_.Exception.Message)"
    throw
}