#!/bin/bash
# Script to create macOS DMG installer for OpenLiveCaption

set -e

# Configuration
APP_NAME="OpenLiveCaption"
APP_VERSION="2.0.0"
DMG_NAME="${APP_NAME}-${APP_VERSION}-macOS"
APP_BUNDLE="dist/${APP_NAME}.app"
DMG_DIR="dist/dmg"
DMG_OUTPUT="dist/installer/${DMG_NAME}.dmg"
VOLUME_NAME="${APP_NAME} ${APP_VERSION}"

echo "======================================"
echo "Creating macOS DMG for ${APP_NAME}"
echo "======================================"
echo ""

# Check if app bundle exists
if [ ! -d "${APP_BUNDLE}" ]; then
    echo "❌ Error: App bundle not found at ${APP_BUNDLE}"
    echo "   Please run build.py first to create the app bundle"
    exit 1
fi

echo "✓ Found app bundle: ${APP_BUNDLE}"

# Create DMG staging directory
echo "📦 Creating DMG staging directory..."
rm -rf "${DMG_DIR}"
mkdir -p "${DMG_DIR}"

# Copy app bundle to staging directory
echo "📋 Copying app bundle..."
cp -R "${APP_BUNDLE}" "${DMG_DIR}/"

# Create Applications symlink
echo "🔗 Creating Applications symlink..."
ln -s /Applications "${DMG_DIR}/Applications"

# Copy additional files
if [ -f "LICENSE.txt" ]; then
    cp "LICENSE.txt" "${DMG_DIR}/"
    echo "✓ Copied LICENSE.txt"
fi

if [ -f "README.md.txt" ]; then
    cp "README.md.txt" "${DMG_DIR}/README.txt"
    echo "✓ Copied README.txt"
fi

# Create installer directory
mkdir -p "dist/installer"

# Remove existing DMG if it exists
if [ -f "${DMG_OUTPUT}" ]; then
    echo "🗑️  Removing existing DMG..."
    rm "${DMG_OUTPUT}"
fi

# Create temporary DMG
echo "🔨 Creating temporary DMG..."
TEMP_DMG="dist/installer/${DMG_NAME}-temp.dmg"
hdiutil create -volname "${VOLUME_NAME}" \
    -srcfolder "${DMG_DIR}" \
    -ov -format UDRW \
    "${TEMP_DMG}"

# Mount temporary DMG
echo "📂 Mounting temporary DMG..."
MOUNT_DIR=$(hdiutil attach -readwrite -noverify -noautoopen "${TEMP_DMG}" | \
    egrep '^/dev/' | sed 1q | awk '{print $3}')

echo "✓ Mounted at: ${MOUNT_DIR}"

# Set DMG window properties using AppleScript
echo "🎨 Configuring DMG appearance..."
cat > /tmp/dmg_setup.applescript << 'EOF'
tell application "Finder"
    tell disk "VOLUME_NAME_PLACEHOLDER"
        open
        set current view of container window to icon view
        set toolbar visible of container window to false
        set statusbar visible of container window to false
        set the bounds of container window to {100, 100, 600, 400}
        set viewOptions to the icon view options of container window
        set arrangement of viewOptions to not arranged
        set icon size of viewOptions to 72
        set position of item "APP_NAME_PLACEHOLDER.app" of container window to {150, 150}
        set position of item "Applications" of container window to {350, 150}
        close
        open
        update without registering applications
        delay 2
    end tell
end tell
EOF

# Replace placeholders
sed -i '' "s/VOLUME_NAME_PLACEHOLDER/${VOLUME_NAME}/g" /tmp/dmg_setup.applescript
sed -i '' "s/APP_NAME_PLACEHOLDER/${APP_NAME}/g" /tmp/dmg_setup.applescript

# Run AppleScript
osascript /tmp/dmg_setup.applescript || echo "⚠️  Warning: Could not set DMG appearance"

# Clean up
rm /tmp/dmg_setup.applescript

# Unmount temporary DMG
echo "📤 Unmounting temporary DMG..."
hdiutil detach "${MOUNT_DIR}" -quiet

# Convert to compressed DMG
echo "🗜️  Compressing DMG..."
hdiutil convert "${TEMP_DMG}" \
    -format UDZO \
    -imagekey zlib-level=9 \
    -o "${DMG_OUTPUT}"

# Remove temporary DMG
rm "${TEMP_DMG}"

# Clean up staging directory
rm -rf "${DMG_DIR}"

# Get DMG size
DMG_SIZE=$(du -h "${DMG_OUTPUT}" | cut -f1)

echo ""
echo "======================================"
echo "✅ DMG created successfully!"
echo "======================================"
echo ""
echo "Output: ${DMG_OUTPUT}"
echo "Size: ${DMG_SIZE}"
echo ""
echo "To install:"
echo "1. Open the DMG file"
echo "2. Drag ${APP_NAME}.app to Applications folder"
echo "3. Eject the DMG"
echo ""
