Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Set output path
$OutputPath = "$PSScriptRoot\screenshot.png"

# Get screen dimensions
$screenWidth = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width
$screenHeight = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height

# Create bitmap and graphics objects
$bitmap = New-Object System.Drawing.Bitmap $screenWidth, $screenHeight
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)

# Copy screen content to bitmap
$graphics.CopyFromScreen(0, 0, 0, 0, $bitmap.Size)

# Save bitmap to PNG
$bitmap.Save($OutputPath, [System.Drawing.Imaging.ImageFormat]::Png)

# Clean up
$graphics.Dispose()
$bitmap.Dispose()

Write-Host "Screenshot saved to: $OutputPath"
