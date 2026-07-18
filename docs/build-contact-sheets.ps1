param(
  [string]$Source = 'C:\Users\James\Downloads\my-projects',
  [string]$Output = 'C:\Users\James\Downloads\my-projects-contact-sheets'
)

Add-Type -AssemblyName System.Drawing
New-Item -ItemType Directory -Force -Path $Output | Out-Null

$files = @(Get-ChildItem $Source -File | Where-Object { $_.Extension -match '^\.(jpg|jpeg|png)$' } | Sort-Object Name)
$columns = 5
$rows = 5
$cellWidth = 320
$cellHeight = 230
$labelHeight = 32

for ($sheetIndex = 0; $sheetIndex -lt [Math]::Ceiling($files.Count / 25); $sheetIndex++) {
  $canvas = New-Object System.Drawing.Bitmap ($columns * $cellWidth), ($rows * ($cellHeight + $labelHeight))
  $graphics = [System.Drawing.Graphics]::FromImage($canvas)
  $graphics.Clear([System.Drawing.Color]::FromArgb(242, 240, 232))
  $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
  $font = New-Object System.Drawing.Font('Consolas', 10)
  $brush = [System.Drawing.Brushes]::Black

  for ($index = 0; $index -lt 25; $index++) {
    $fileIndex = ($sheetIndex * 25) + $index
    if ($fileIndex -ge $files.Count) { break }

    $column = $index % $columns
    $row = [Math]::Floor($index / $columns)
    $x = $column * $cellWidth
    $y = $row * ($cellHeight + $labelHeight)
    $image = [System.Drawing.Image]::FromFile($files[$fileIndex].FullName)

    if ($image.PropertyIdList -contains 274) {
      $orientation = $image.GetPropertyItem(274).Value[0]
      if ($orientation -eq 3) { $image.RotateFlip([System.Drawing.RotateFlipType]::Rotate180FlipNone) }
      if ($orientation -eq 6) { $image.RotateFlip([System.Drawing.RotateFlipType]::Rotate90FlipNone) }
      if ($orientation -eq 8) { $image.RotateFlip([System.Drawing.RotateFlipType]::Rotate270FlipNone) }
    }

    $scale = [Math]::Max($cellWidth / $image.Width, $cellHeight / $image.Height)
    $sourceWidth = $cellWidth / $scale
    $sourceHeight = $cellHeight / $scale
    $sourceX = ($image.Width - $sourceWidth) / 2
    $sourceY = ($image.Height - $sourceHeight) / 2
    $destination = New-Object System.Drawing.RectangleF($x, $y, $cellWidth, $cellHeight)
    $sourceRect = New-Object System.Drawing.RectangleF($sourceX, $sourceY, $sourceWidth, $sourceHeight)
    $graphics.DrawImage($image, $destination, $sourceRect, [System.Drawing.GraphicsUnit]::Pixel)
    $graphics.DrawString($files[$fileIndex].Name, $font, $brush, $x + 6, $y + $cellHeight + 6)
    $image.Dispose()
  }

  $path = Join-Path $Output ('sheet-{0:D2}.jpg' -f ($sheetIndex + 1))
  $canvas.Save($path, [System.Drawing.Imaging.ImageFormat]::Jpeg)
  $font.Dispose()
  $graphics.Dispose()
  $canvas.Dispose()
}

$sheets = @(Get-ChildItem $Output -Filter 'sheet-*.jpg' | Sort-Object Name)
if ($sheets.Count -gt 0) {
  $first = [System.Drawing.Image]::FromFile($sheets[0].FullName)
  $combined = New-Object System.Drawing.Bitmap($first.Width, ($first.Height * $sheets.Count))
  $first.Dispose()
  $combinedGraphics = [System.Drawing.Graphics]::FromImage($combined)
  $combinedGraphics.Clear([System.Drawing.Color]::White)
  for ($index = 0; $index -lt $sheets.Count; $index++) {
    $sheet = [System.Drawing.Image]::FromFile($sheets[$index].FullName)
    $combinedGraphics.DrawImageUnscaled($sheet, 0, ($sheet.Height * $index))
    $sheet.Dispose()
  }
  $combinedPath = Join-Path $Output 'all-photos.jpg'
  $combined.Save($combinedPath, [System.Drawing.Imaging.ImageFormat]::Jpeg)
  $combinedGraphics.Dispose()
  $combined.Dispose()
}
