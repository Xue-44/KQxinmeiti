$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument '-ExecutionPolicy Bypass -WindowStyle Hidden -File "G:\openclaw\data\.openclaw\workspace\scripts\github_sync.ps1"'
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At '12:00'
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
$principal = New-ScheduledTaskPrincipal -UserId 'Administrator' -LogonType Password -RunLevel Highest
$taskName = 'KaiQiJiTuan_GitHub_Sync'

Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description 'KaiQiJiTuan GitHub weekly sync - Every Sunday 12:00'
Write-Host 'Task registered successfully'