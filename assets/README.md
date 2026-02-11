# OpenLiveCaption Assets

This directory contains application assets including icons and images for OpenLiveCaption.

## Files

### Source Files (SVG)
- `icon.svg` - Main application icon (512x512)
- `tray_icon_active.svg` - System tray icon for active state (64x64)
- `tray_icon_inactive.svg` - System tray icon for inactive state (64x64)

### Generated Files (Platform-Specific)
These files are generated from the SVG sources:
- `icon.ico` - Windows application icon (multi-resolution)
- `icon.icns` - macOS application icon (multi-resolution)
- `icon.png` - Linux application icon (512x512)
- `tray_active.png` - System tray active icon (64x64)
- `tray_inactive.png` - System tray inactive icon (64x64)

## Icon Design

### Main Application Icon (`icon.svg`)
- **Design**: Speech bubble with caption lines and microphone
- **Colors**: 
  - Primary: Blue (#2196F3)
  - Accent: Amber (#FFC107)
  - Background: White
- **Symbolism**: 
  - Speech bubble represents captions/subtitles
  - Caption lines represent text transcription
  - Microphone represents audio input
- **Size**: 512x512 pixels (scalable SVG)

### System Tray Icons
- **Active State** (`tray_icon_active.svg`):
  - Blue background (#2196F3)
  - Green indicator dot (#4CAF50)
  - Indicates captions are running
  
- **Inactive State** (`tray_icon_inactive.svg`):
  - Gray background (#757575)
  - Gray indicator dot (#9E9E9E)
  - Indicates captions are stopped

## Generating Platform-Specific Icons

### Prerequisites

Install required tools:

**Windows**:
```bash
pip install Pillow
# For ICO generation, use ImageMagick or online converter
```

**macOS**:
```bash
brew install imagemagick
# For ICNS, use iconutil (built-in) or img2icns
```

**Linux**:
```bash
sudo apt install imagemagick  # Ubuntu/Debian
sudo dnf install ImageMagick  # Fedora
```

### Conversion Commands

#### 1. Generate PNG from SVG

Using Inkscape (recommended for best quality):
```bash
# Main icon
inkscape icon.svg --export-type=png --export-filename=icon.png -w 512 -h 512

# Tray icons
inkscape tray_icon_active.svg --export-type=png --export-filename=tray_active.png -w 64 -h 64
inkscape tray_icon_inactive.svg --export-type=png --export-filename=tray_inactive.png -w 64 -h 64
```

Using ImageMagick (alternative):
```bash
# Main icon
convert -background none icon.svg -resize 512x512 icon.png

# Tray icons
convert -background none tray_icon_active.svg -resize 64x64 tray_active.png
convert -background none tray_icon_inactive.svg -resize 64x64 tray_inactive.png
```

Using Python (Pillow + cairosvg):
```python
from cairosvg import svg2png

# Main icon
svg2png(url='icon.svg', write_to='icon.png', output_width=512, output_height=512)

# Tray icons
svg2png(url='tray_icon_active.svg', write_to='tray_active.png', output_width=64, output_height=64)
svg2png(url='tray_icon_inactive.svg', write_to='tray_inactive.png', output_width=64, output_height=64)
```

#### 2. Generate Windows ICO (Multi-Resolution)

Using ImageMagick:
```bash
# Generate multiple sizes
convert icon.svg -resize 16x16 icon_16.png
convert icon.svg -resize 32x32 icon_32.png
convert icon.svg -resize 48x48 icon_48.png
convert icon.svg -resize 64x64 icon_64.png
convert icon.svg -resize 128x128 icon_128.png
convert icon.svg -resize 256x256 icon_256.png

# Combine into ICO
convert icon_16.png icon_32.png icon_48.png icon_64.png icon_128.png icon_256.png icon.ico

# Clean up
rm icon_16.png icon_32.png icon_48.png icon_64.png icon_128.png icon_256.png
```

Using Python (Pillow):
```python
from PIL import Image

# Load SVG as PNG first
img = Image.open('icon.png')

# Generate ICO with multiple sizes
img.save('icon.ico', format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])
```

#### 3. Generate macOS ICNS

Using iconutil (macOS built-in):
```bash
# Create iconset directory
mkdir icon.iconset

# Generate required sizes
sips -z 16 16     icon.png --out icon.iconset/icon_16x16.png
sips -z 32 32     icon.png --out icon.iconset/icon_16x16@2x.png
sips -z 32 32     icon.png --out icon.iconset/icon_32x32.png
sips -z 64 64     icon.png --out icon.iconset/icon_32x32@2x.png
sips -z 128 128   icon.png --out icon.iconset/icon_128x128.png
sips -z 256 256   icon.png --out icon.iconset/icon_128x128@2x.png
sips -z 256 256   icon.png --out icon.iconset/icon_256x256.png
sips -z 512 512   icon.png --out icon.iconset/icon_256x256@2x.png
sips -z 512 512   icon.png --out icon.iconset/icon_512x512.png
sips -z 1024 1024 icon.png --out icon.iconset/icon_512x512@2x.png

# Convert to ICNS
iconutil -c icns icon.iconset

# Clean up
rm -rf icon.iconset
```

Using img2icns (alternative):
```bash
brew install img2icns
img2icns icon.png icon.icns
```

#### 4. Generate Linux PNG (Already Done)

Linux typically uses PNG files directly. The 512x512 PNG generated in step 1 is sufficient.

### Automated Generation Script

Create a script to generate all formats:

```bash
#!/bin/bash
# generate_icons.sh

echo "Generating OpenLiveCaption icons..."

# Check for required tools
if ! command -v convert &> /dev/null; then
    echo "ImageMagick not found. Please install it first."
    exit 1
fi

# Generate PNGs from SVG
echo "Converting SVG to PNG..."
convert -background none icon.svg -resize 512x512 icon.png
convert -background none tray_icon_active.svg -resize 64x64 tray_active.png
convert -background none tray_icon_inactive.svg -resize 64x64 tray_inactive.png

# Generate Windows ICO
echo "Generating Windows ICO..."
convert icon.svg -resize 16x16 icon_16.png
convert icon.svg -resize 32x32 icon_32.png
convert icon.svg -resize 48x48 icon_48.png
convert icon.svg -resize 64x64 icon_64.png
convert icon.svg -resize 128x128 icon_128.png
convert icon.svg -resize 256x256 icon_256.png
convert icon_16.png icon_32.png icon_48.png icon_64.png icon_128.png icon_256.png icon.ico
rm icon_16.png icon_32.png icon_48.png icon_64.png icon_128.png icon_256.png

# Generate macOS ICNS (macOS only)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Generating macOS ICNS..."
    mkdir -p icon.iconset
    sips -z 16 16     icon.png --out icon.iconset/icon_16x16.png
    sips -z 32 32     icon.png --out icon.iconset/icon_16x16@2x.png
    sips -z 32 32     icon.png --out icon.iconset/icon_32x32.png
    sips -z 64 64     icon.png --out icon.iconset/icon_32x32@2x.png
    sips -z 128 128   icon.png --out icon.iconset/icon_128x128.png
    sips -z 256 256   icon.png --out icon.iconset/icon_128x128@2x.png
    sips -z 256 256   icon.png --out icon.iconset/icon_256x256.png
    sips -z 512 512   icon.png --out icon.iconset/icon_256x256@2x.png
    sips -z 512 512   icon.png --out icon.iconset/icon_512x512.png
    sips -z 1024 1024 icon.png --out icon.iconset/icon_512x512@2x.png
    iconutil -c icns icon.iconset
    rm -rf icon.iconset
fi

echo "Icon generation complete!"
echo "Generated files:"
echo "  - icon.png (512x512)"
echo "  - icon.ico (Windows)"
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "  - icon.icns (macOS)"
fi
echo "  - tray_active.png (64x64)"
echo "  - tray_inactive.png (64x64)"
```

Make it executable:
```bash
chmod +x generate_icons.sh
./generate_icons.sh
```

## Using Icons in the Application

### PyQt6 Integration

```python
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon
import os

# Get assets directory
assets_dir = os.path.join(os.path.dirname(__file__), 'assets')

# Set application icon
app = QApplication([])
app.setWindowIcon(QIcon(os.path.join(assets_dir, 'icon.png')))

# Set system tray icons
tray = QSystemTrayIcon()
active_icon = QIcon(os.path.join(assets_dir, 'tray_active.png'))
inactive_icon = QIcon(os.path.join(assets_dir, 'tray_inactive.png'))

# Switch based on state
if captions_running:
    tray.setIcon(active_icon)
else:
    tray.setIcon(inactive_icon)
```

### PyInstaller Integration

In your `.spec` file:

```python
# Windows
a = Analysis(
    ...
    datas=[('assets/icon.ico', 'assets')],
    ...
)

# macOS
app = BUNDLE(
    ...
    icon='assets/icon.icns',
    ...
)

# Linux
a = Analysis(
    ...
    datas=[('assets/icon.png', 'assets')],
    ...
)
```

## Icon Guidelines

### Design Principles
- **Simple**: Clear and recognizable at small sizes
- **Consistent**: Matches application purpose (captions/subtitles)
- **Scalable**: Works from 16x16 to 512x512
- **Accessible**: High contrast, colorblind-friendly

### Color Palette
- **Primary Blue**: #2196F3 (Material Design Blue 500)
- **Dark Blue**: #1976D2 (Material Design Blue 700)
- **Amber**: #FFC107 (Material Design Amber 500)
- **Orange**: #FF9800 (Material Design Orange 500)
- **Green**: #4CAF50 (Material Design Green 500)
- **Gray**: #757575 (Material Design Gray 600)

### Size Requirements
- **Windows ICO**: 16, 32, 48, 64, 128, 256 pixels
- **macOS ICNS**: 16, 32, 128, 256, 512, 1024 pixels (with @2x variants)
- **Linux PNG**: 512x512 pixels (scalable)
- **System Tray**: 16x16, 32x32, 64x64 pixels

## Modifying Icons

To modify the icons:

1. Edit the SVG files using:
   - Inkscape (free, cross-platform)
   - Adobe Illustrator
   - Figma
   - Any SVG editor

2. Maintain the same canvas size (512x512 for main, 64x64 for tray)

3. Keep the design simple and recognizable

4. Test at small sizes (16x16, 32x32) to ensure clarity

5. Regenerate platform-specific formats using the commands above

## License

These icons are part of OpenLiveCaption and are licensed under the MIT License. See [LICENSE.txt](../LICENSE.txt) for details.

## Credits

Icon design inspired by:
- Material Design icons
- Accessibility symbols
- Speech and caption metaphors
