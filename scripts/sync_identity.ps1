$repoPath = "G:\openclaw\data\.openclaw\workspace\KaiQiJiTuan"
$memorySrc = "G:\openclaw\data\.openclaw\workspace"
$pat = "[已移除]"
$remoteUrl = "https://github.com/Xue-44/KaiQiJiTuan.git"

# Clone if not exists
if (!(Test-Path $repoPath)) {
    git clone "https://github.com/Xue-44/KaiQiJiTuan.git" $repoPath
}

# Copy identity.md as identity-newmedia.md
$src = Join-Path $memorySrc "IDENTITY.md"
$dst = Join-Path $repoPath "identity-newmedia.md"
Copy-Item $src -Destination $dst -Force

Set-Location $repoPath
git config user.email "xinmeiti@kaiqi.com" 2>$null
git config user.name "XinMeiti虾" 2>$null
git add identity-newmedia.md
$commitMsg = "Sync identity-newmedia.md " + (Get-Date -Format "yyyy-MM-dd HH:mm")
git commit -m $commitMsg
git remote set-url origin $remoteUrl
git push origin main
Write-Host "Pushed identity-newmedia.md successfully"
