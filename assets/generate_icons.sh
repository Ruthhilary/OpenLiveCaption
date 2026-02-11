#!/bin/bash
# generate_icons.sh
# Script to generate platform-specific icons from SVG sources

set -e  # Exit on error

echo "========================================="
echo "OpenLiveCaption Icon Generation"
echo "========================================="
echo ""

# Check for required tools
echo "Checking for required tools..."

if ! command -v convert &> /dev/null; then
    echo "ERROR: ImageMagick not found."
    echo "Please install ImageMagick:"
    echo "  - macOS: brew install imagemagick"
    echo "  - Ubuntu/Debian: sudo apt install imagemagick"
    echo "  - Fedora: sudo dnf install ImageMagick"
    exit 1
fi

echo "✓ ImageMagick found"
echo ""

# Change to assets directory
cd "$(dirname "$0")"

# Check if SVG files exist
if [ ! -f "icon.svg" ]; then
    echo "ERROR: icon.svg not found in assets directory"
    exit 1
fi

if [ ! -f "tray_icon_active.svg" ]; then
    echo "ERROR: tray_icon_active.svg not found in assets directory"
    exit 1
fi

if [ ! -f "tray_icon_inactive.svg" ]; then
    echo "ERROR: tray_icon_inactive.svg not found in assets directory"
    exit 1
fi

echo "✓ All SVG source files found"
echo ""

# Generate PNGs from SVG
echo "Step 1: Converting SVG to PNG..."
echo "  - Generating icon.png (512x512)..."
convert -background none icon.svg -resize 512x512 icon.png

echo "  - Generating tray_active.png (64x64)..."
convert -background none tray_icon_active.svg -resize 64x64 tray_active.png

echo "  - Generating tray_inactive.png (64x64)..."
convert -background none tray_icon_inactive.svg -resize 64x64 tray_inactive.png

echo "✓ PNG files generated"
echo ""

# Generate Windows ICO
echo "Step 2: Generating Windows ICO..."
echo "  - Creating multiple resolutions..."
convert icon.svg -background none -resize 16x16 icon_16.png
convert icon.svg -background none -resize 32x32 icon_32.png
convert icon.svg -background none -resize 48x48 icon_48.png
convert icon.svg -background none -resize 64x64 icon_64.png
convert icon.svg -background none -resize 128x128 icon_128.png
convert icon.svg -background none -resize 256x256 icon_256.png

echo "  - Combining into icon.ico..."
convert icon_16.png icon_32.png icon_48.png icon_64.png icon_128.png icon_256.png icon.ico

echo "  - Cleaning up temporary files..."
rm icon_16.png icon_32.png icon_48.png icon_64.png icon_128.png icon_256.png

echo "✓ Windows ICO generated"
echo ""

# Generate macOS ICNS (macOS only)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Step 3: Generating macOS ICNS..."
    
    if ! command -v sips &> /dev/null; then
        echo "WARNING: sips not found (macOS only tool)"
        echo "Skipping ICNS generation"
    elif ! command -v iconutil &> /dev/null; then
        echo "WARNING: iconutil not found (macOS only tool)"
        echo "Skipping ICNS generation"
    else
        echo "  - Creating iconset directory..."
        mkdir -p icon.iconset
        
        echo "  - Generating required sizes..."
        sips -z 16 16     icon.png --out icon.iconset/icon_16x16.png > /dev/null 2>&1
        sips -z 32 32     icon.png --out icon.iconset/icon_16x16@2x.png > /dev/null 2>&1
        sips -z 32 32     icon.png --out icon.iconset/icon_32x32.png > /dev/null 2>&1
        sips -z 64 64     icon.png --out icon.iconset/icon_32x32@2x.png > /dev/null 2>&1
        sips -z 128 128   icon.png --out icon.iconset/icon_128x128.png > /dev/null 2>&1
        sips -z 256 256   icon.png --out icon.iconset/icon_128x128@2x.png > /dev/null 2>&1
        sips -z 256 256   icon.png --out icon.iconset/icon_256x256.png > /dev/null 2>&1
        sips -z 512 512   icon.png --out icon.iconset/icon_256x256@2x.png > /dev/null 2>&1
        sips -z 512 512   icon.png --out icon.iconset/icon_512x512.png > /dev/null 2>&1
        sips -z 1024 1024 icon.png --out icon.iconset/icon_512x512@2x.png > /dev/null 2>&1
        
        echo "  - Converting to ICNS..."
        iconutil -c icns icon.iconset
        
        echo "  - Cleaning up iconset directory..."
        rm -rf icon.iconset
        
        echo "✓ macOS ICNS generated"
    fi
else
    echo "Step 3: Skipping macOS ICNS (not on macOS)"
fi
echo ""

# Summary
echo "========================================="
echo "Icon Generation Complete!"
echo "========================================="
echo ""
echo "Generated files:"
echo "  ✓ icon.png (512x512) - Linux/General"
echo "  ✓ icon.ico - Windows"
if [[ "$OSTYPE" == "darwin"* ]] && [ -f "icon.icns" ]; then
    echo "  ✓ icon.icns - macOS"
fi
echo "  ✓ tray_active.png (64x64) - System tray (active)"
echo "  ✓ tray_inactive.png (64x64) - System tray (inactive)"
echo ""
echo "These files are ready to use in the application!"
echo ""
