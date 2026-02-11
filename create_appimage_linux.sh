#!/bin/bash
# Script to create Linux AppImage for OpenLiveCaption

set -e

# Configuration
APP_NAME="OpenLiveCaption"
APP_VERSION="2.0.0"
APPIMAGE_NAME="${APP_NAME}-${APP_VERSION}-x86_64.AppImage"
EXECUTABLE="dist/OpenLiveCaption"
APPDIR="AppDir"
OUTPUT_DIR="dist/installer"

echo "======================================"
echo "Creating Linux AppImage for ${APP_NAME}"
echo "======================================"
echo ""

# Check if executable exists
if [ ! -f "${EXECUTABLE}" ]; then
    echo "❌ Error: Executable not found at ${EXECUTABLE}"
    echo "   Please run build.py first to create the executable"
    exit 1
fi

echo "✓ Found executable: ${EXECUTABLE}"

# Check if appimage-builder is installed
if ! command -v appimage-builder &> /dev/null; then
    echo "❌ Error: appimage-builder not found"
    echo ""
    echo "Install with:"
    echo "  sudo apt install python3-pip"
    echo "  pip3 install appimage-builder"
    echo ""
    exit 1
fi

echo "✓ appimage-builder is installed"

# Create AppDir structure
echo "📦 Creating AppDir structure..."
rm -rf "${APPDIR}"
mkdir -p "${APPDIR}/usr/bin"
mkdir -p "${APPDIR}/usr/share/applications"
mkdir -p "${APPDIR}/usr/share/icons/hicolor/256x256/apps"

# Copy executable
echo "📋 Copying executable..."
cp "${EXECUTABLE}" "${APPDIR}/usr/bin/openlivecaption"
chmod +x "${APPDIR}/usr/bin/openlivecaption"

# Create desktop entry
echo "📝 Creating desktop entry..."
cat > "${APPDIR}/usr/share/applications/openlivecaption.desktop" << EOF
[Desktop Entry]
Type=Application
Name=OpenLiveCaption
Comment=System-wide live captions with real-time transcription
Exec=openlivecaption
Icon=openlivecaption
Categories=AudioVideo;Audio;Utility;
Terminal=false
StartupNotify=true
EOF

# Copy icon (or create placeholder)
if [ -f "assets/icon.png" ]; then
    cp "assets/icon.png" "${APPDIR}/usr/share/icons/hicolor/256x256/apps/openlivecaption.png"
    echo "✓ Copied icon"
else
    echo "⚠️  Warning: Icon not found, creating placeholder"
    # Create a simple placeholder icon (1x1 transparent PNG)
    echo "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==" | base64 -d > "${APPDIR}/usr/share/icons/hicolor/256x256/apps/openlivecaption.png"
fi

# Create AppRun script
echo "📝 Creating AppRun script..."
cat > "${APPDIR}/AppRun" << 'EOF'
#!/bin/bash
# AppRun script for OpenLiveCaption

APPDIR="$(dirname "$(readlink -f "$0")")"

# Set environment variables
export LD_LIBRARY_PATH="${APPDIR}/usr/lib:${APPDIR}/usr/lib/x86_64-linux-gnu:${LD_LIBRARY_PATH}"
export PYTHONHOME="${APPDIR}/usr"
export QT_PLUGIN_PATH="${APPDIR}/usr/lib/x86_64-linux-gnu/qt6/plugins"
export QT_QPA_PLATFORM_PLUGIN_PATH="${APPDIR}/usr/lib/x86_64-linux-gnu/qt6/plugins/platforms"

# Run the application
exec "${APPDIR}/usr/bin/openlivecaption" "$@"
EOF

chmod +x "${APPDIR}/AppRun"

# Create output directory
mkdir -p "${OUTPUT_DIR}"

# Build AppImage using appimage-builder
echo "🔨 Building AppImage..."
echo "   This may take several minutes..."
echo ""

if appimage-builder --recipe AppImageBuilder.yml --skip-test; then
    # Move AppImage to output directory
    if [ -f "${APPIMAGE_NAME}" ]; then
        mv "${APPIMAGE_NAME}" "${OUTPUT_DIR}/"
        
        # Get AppImage size
        APPIMAGE_SIZE=$(du -h "${OUTPUT_DIR}/${APPIMAGE_NAME}" | cut -f1)
        
        echo ""
        echo "======================================"
        echo "✅ AppImage created successfully!"
        echo "======================================"
        echo ""
        echo "Output: ${OUTPUT_DIR}/${APPIMAGE_NAME}"
        echo "Size: ${APPIMAGE_SIZE}"
        echo ""
        echo "To install:"
        echo "1. Make executable: chmod +x ${APPIMAGE_NAME}"
        echo "2. Run: ./${APPIMAGE_NAME}"
        echo ""
    else
        echo "❌ Error: AppImage file not found after build"
        exit 1
    fi
else
    echo "❌ Error: AppImage build failed"
    exit 1
fi

# Clean up
echo "🧹 Cleaning up..."
rm -rf "${APPDIR}"

echo "✅ Done!"
