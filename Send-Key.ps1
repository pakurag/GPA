param (
    [string]$Key
)

Add-Type -AssemblyName System.Windows.Forms

try {
    [System.Windows.Forms.SendKeys]::SendWait($Key)
    Start-Sleep -Milliseconds 100
} catch {
    Write-Error "Failed to send key: $Key"
    exit 1
}
