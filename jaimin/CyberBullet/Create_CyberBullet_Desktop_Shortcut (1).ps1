$appDir = "C:\Users\khatr\OneDrive\Desktop\CyberBullet"
$python = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $python) { Write-Host "Python was not found in PATH."; pause; exit 1 }
$target = Join-Path $appDir "main.py"
$icon = Join-Path $appDir "CyberBullet.ico"
$desktop = [Environment]::GetFolderPath("Desktop")
$link = Join-Path $desktop "CyberBullet Premium.lnk"
$ws = New-Object -ComObject WScript.Shell
$sc = $ws.CreateShortcut($link)
$sc.TargetPath = $python
$sc.Arguments = "`"$target`""
$sc.WorkingDirectory = $appDir
if (Test-Path $icon) { $sc.IconLocation = "$icon,0" }
$sc.Description = "CyberBullet Premium Security Suite"
$sc.Save()
Write-Host "Desktop shortcut created."
pause
