param(
  [string]$Source = 'C:\Users\James\Downloads\my-projects',
  [string]$Output = (Join-Path $PSScriptRoot '..\public\projects')
)

Add-Type -AssemblyName System.Drawing
New-Item -ItemType Directory -Force -Path $Output | Out-Null

$assets = @(
  @{ source = 'IMG_20260708_141408312.jpg'; output = 'robodog.jpg'; focalX = 0.58; focalY = 0.52 },
  @{ source = 'IMG_20241111_122352651.jpg'; output = 'robodog-rev-a.jpg'; focalX = 0.50; focalY = 0.52 },
  @{ source = 'IMG_20250505_114508245.jpg'; output = 'robodog-rev-b.jpg'; focalX = 0.52; focalY = 0.52 },
  @{ source = 'IMG_20260417_221157940.jpg'; output = 'robodog-pair.jpg'; focalX = 0.50; focalY = 0.50 },
  @{ source = 'IMG_20260708_141350321.jpg'; output = 'robodog-controllers.jpg'; focalX = 0.52; focalY = 0.52 },
  @{ source = 'IMG_20250622_235128196.jpg'; output = 'moon-lamp.jpg'; focalX = 0.61; focalY = 0.48 },
  @{ source = 'IMG_20250505_114716565.jpg'; output = 'sand-table.jpg'; focalX = 0.43; focalY = 0.48 },
  @{ source = 'IMG_20250505_114708888.jpg'; output = 'sand-table-mechanism.jpg'; focalX = 0.48; focalY = 0.48 },
  @{ source = 'IMG_20250430_224614575.jpg'; output = 'wallet.jpg'; focalX = 0.54; focalY = 0.50 },
  @{ source = '20220316_174504.jpg'; output = 'brother-cartridge.jpg'; focalX = 0.53; focalY = 0.50 },
  @{ source = 'IMG_20230829_014051610.jpg'; output = 'single-key-keyboard.jpg'; focalX = 0.52; focalY = 0.54 },
  @{ source = 'IMG_20260708_172104100.jpg'; output = 'motor-controller.jpg'; focalX = 0.50; focalY = 0.52 },
  @{ source = 'IMG_20260712_192907966.jpg'; output = 'epaper-watch-front.jpg'; focalX = 0.50; focalY = 0.50 },
  @{ source = 'IMG_20260712_192957692.jpg'; output = 'epaper-watch-back.jpg'; focalX = 0.50; focalY = 0.50 },
  @{ source = 'IMG_20250820_163442058.jpg'; output = 'light-gun-side.jpg'; focalX = 0.52; focalY = 0.52 },
  @{ source = 'IMG_20250820_163454397.jpg'; output = 'light-gun-screen.jpg'; focalX = 0.50; focalY = 0.52 },
  @{ source = 'IMG_20250820_163458670.jpg'; output = 'light-gun-profile.jpg'; focalX = 0.50; focalY = 0.50 },
  @{ source = 'IMG_20250205_194546494.jpg'; output = 'flare-on.jpg'; focalX = 0.49; focalY = 0.44 },
  @{ source = 'IMG_20240104_115228831.jpg'; output = 'epaper-frame.jpg'; focalX = 0.50; focalY = 0.48 }
)

$targetWidth = 1440
$targetHeight = 960
$jpegCodec = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object MimeType -eq 'image/jpeg'
$quality = [System.Drawing.Imaging.Encoder]::Quality
$encoderParameters = New-Object System.Drawing.Imaging.EncoderParameters(1)
$encoderParameters.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter($quality, [long]86)

foreach ($asset in $assets) {
  $sourcePath = Join-Path $Source $asset.source
  $outputPath = Join-Path $Output $asset.output
  $image = [System.Drawing.Image]::FromFile($sourcePath)

  if ($image.PropertyIdList -contains 274) {
    $orientation = $image.GetPropertyItem(274).Value[0]
    if ($orientation -eq 3) { $image.RotateFlip([System.Drawing.RotateFlipType]::Rotate180FlipNone) }
    if ($orientation -eq 6) { $image.RotateFlip([System.Drawing.RotateFlipType]::Rotate90FlipNone) }
    if ($orientation -eq 8) { $image.RotateFlip([System.Drawing.RotateFlipType]::Rotate270FlipNone) }
  }

  $targetRatio = $targetWidth / $targetHeight
  $sourceRatio = $image.Width / $image.Height
  if ($sourceRatio -gt $targetRatio) {
    $cropHeight = $image.Height
    $cropWidth = $cropHeight * $targetRatio
  } else {
    $cropWidth = $image.Width
    $cropHeight = $cropWidth / $targetRatio
  }

  $cropX = [Math]::Max(0, [Math]::Min($image.Width - $cropWidth, ($asset.focalX * $image.Width) - ($cropWidth / 2)))
  $cropY = [Math]::Max(0, [Math]::Min($image.Height - $cropHeight, ($asset.focalY * $image.Height) - ($cropHeight / 2)))

  $canvas = New-Object System.Drawing.Bitmap($targetWidth, $targetHeight)
  $canvas.SetResolution(72, 72)
  $graphics = [System.Drawing.Graphics]::FromImage($canvas)
  $graphics.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
  $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
  $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
  $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
  $destination = New-Object System.Drawing.Rectangle(0, 0, $targetWidth, $targetHeight)
  $sourceRectangle = New-Object System.Drawing.Rectangle(
    [int][Math]::Round($cropX),
    [int][Math]::Round($cropY),
    [int][Math]::Round($cropWidth),
    [int][Math]::Round($cropHeight)
  )
  $graphics.DrawImage($image, $destination, $sourceRectangle, [System.Drawing.GraphicsUnit]::Pixel)
  $canvas.Save($outputPath, $jpegCodec, $encoderParameters)

  $graphics.Dispose()
  $canvas.Dispose()
  $image.Dispose()
}

$encoderParameters.Dispose()
