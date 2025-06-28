Add-Type @"
using System;
using System.Runtime.InteropServices;

public class MouseSimulator {
    [DllImport("user32.dll")]
    public static extern bool SetCursorPos(int X, int Y);

    [DllImport("user32.dll")]
    public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint dwData, UIntPtr dwExtraInfo);

    public const uint MOUSEEVENTF_LEFTDOWN = 0x02;
    public const uint MOUSEEVENTF_LEFTUP = 0x04;
}
"@

param (
    [int]$X,
    [int]$Y
)

# Move cursor to X, Y
[MouseSimulator]::SetCursorPos($X, $Y)

Start-Sleep -Milliseconds 100  # Small delay before clicking

# Simulate mouse left click
[MouseSimulator]::mouse_event([MouseSimulator]::MOUSEEVENTF_LEFTDOWN, 0, 0, 0, [UIntPtr]::Zero)
Start-Sleep -Milliseconds 50
[MouseSimulator]::mouse_event([MouseSimulator]::MOUSEEVENTF_LEFTUP, 0, 0, 0, [UIntPtr]::Zero)

Write-Host "Clicked at ($X, $Y)"
