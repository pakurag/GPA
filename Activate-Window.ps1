param (
    [string]$Title,
    [ValidateSet("like", "eq")]
    [string]$MatchType = "like"
)

Add-Type @"
using System;
using System.Runtime.InteropServices;

public class WinAPI {
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
}
"@

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$found = $false

$windows = Get-Process | Where-Object {
    if ($_.MainWindowHandle -eq 0) { return $false }

    switch ($MatchType) {
        "like" { return $_.MainWindowTitle -like "*$Title*" }
        "eq"   { return $_.MainWindowTitle -eq $Title }
    }
}

foreach ($window in $windows) {
    $null = [WinAPI]::SetForegroundWindow($window.MainWindowHandle)
    Write-Host "Activated window: $($window.MainWindowTitle)"
    $found = $true
    break
}

if (-not $found) {
    Write-Error "Window with title match ($MatchType) '$Title' not found."
    exit 1
}
