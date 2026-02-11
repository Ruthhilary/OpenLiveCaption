#!/bin/bash
# macOS Code Signing Script for OpenLiveCaption
# Signs app bundles and DMG files with Developer ID certificate

set -e

echo "======================================"
echo "OpenLiveCaption macOS Code Signing"
echo "======================================"
echo ""

# Configuration from environment variables
# Set these environment variables:
#   CODESIGN_IDENTITY - Your Developer ID certificate identity
#   Example: "Developer ID Application: Your Name (TEAM_ID)"
IDENTITY="${CODESIGN_IDENTITY}"

# Check if file to sign was provided
if [ -z "$1" ]; then
    echo "Error: No file specified to sign"
    echo ""
    echo "Usage: ./sign_macos.sh <file-to-sign>"
    echo "Example: ./sign_macos.sh dist/OpenLiveCaption.app"
    echo "Example: ./sign_macos.sh dist/installer/OpenLiveCaption-2.0.0-macOS.dmg"
    echo ""
    exit 1
fi

FILE_TO_SIGN="$1"

# Check if file exists
if [ ! -e "$FILE_TO_SIGN" ]; then
    echo "Error: File not found: $FILE_TO_SIGN"
    exit 1
fi

echo "File to sign: $FILE_TO_SIGN"
echo ""

# Check if codesign is available
if ! command -v codesign &> /dev/null; then
    echo "Error: codesign not found"
    echo ""
    echo "Please install Xcode Command Line Tools:"
    echo "  xcode-select --install"
    echo ""
    exit 1
fi

echo "✓ Found codesign: $(which codesign)"

# Check if identity is set
if [ -z "$IDENTITY" ]; then
    echo "Error: Code signing identity not set"
    echo ""
    echo "Please set the CODESIGN_IDENTITY environment variable:"
    echo "  export CODESIGN_IDENTITY=\"Developer ID Application: Your Name (TEAM_ID)\""
    echo ""
    echo "To find your identity, run:"
    echo "  security find-identity -v -p codesigning"
    echo ""
    exit 1
fi

echo "✓ Code signing identity: $IDENTITY"

# Verify identity exists in keychain
if ! security find-identity -v -p codesigning | grep -q "$IDENTITY"; then
    echo "Error: Identity not found in keychain"
    echo ""
    echo "Available identities:"
    security find-identity -v -p codesigning
    echo ""
    echo "Please ensure your Developer ID certificate is installed"
    echo "See docs/CODE_SIGNING_MACOS.md for setup instructions"
    echo ""
    exit 1
fi

echo "✓ Identity verified in keychain"
echo ""

# Determine if signing app bundle or DMG
if [[ "$FILE_TO_SIGN" == *.app ]]; then
    echo "Detected app bundle, performing deep signing..."
    echo ""
    
    # Check for entitlements file
    ENTITLEMENTS_FILE="entitlements.plist"
    if [ ! -f "$ENTITLEMENTS_FILE" ]; then
        echo "Warning: entitlements.plist not found"
        echo "Creating default entitlements file..."
        cat > "$ENTITLEMENTS_FILE" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.device.audio-input</key>
    <true/>
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/>
    <key>com.apple.security.cs.disable-library-validation</key>
    <true/>
</dict>
</plist>
EOF
        echo "✓ Created entitlements.plist"
    fi
    
    echo "✓ Using entitlements: $ENTITLEMENTS_FILE"
    echo ""
    
    # Sign all nested frameworks and libraries first
    echo "Signing nested frameworks and libraries..."
    find "$FILE_TO_SIGN/Contents" -type f \( -name "*.dylib" -o -name "*.so" \) 2>/dev/null | while read -r lib; do
        echo "  Signing: $(basename "$lib")"
        codesign --sign "$IDENTITY" \
            --force \
            --timestamp \
            --options runtime \
            "$lib" 2>&1 | grep -v "replacing existing signature" || true
    done
    
    # Sign frameworks
    find "$FILE_TO_SIGN/Contents/Frameworks" -type d -name "*.framework" 2>/dev/null | while read -r framework; do
        echo "  Signing framework: $(basename "$framework")"
        codesign --sign "$IDENTITY" \
            --force \
            --timestamp \
            --options runtime \
            "$framework" 2>&1 | grep -v "replacing existing signature" || true
    done
    
    echo ""
    echo "Signing main executable..."
    
    # Find and sign the main executable
    MAIN_EXEC="$FILE_TO_SIGN/Contents/MacOS/OpenLiveCaption"
    if [ -f "$MAIN_EXEC" ]; then
        echo "  Signing: $(basename "$MAIN_EXEC")"
        codesign --sign "$IDENTITY" \
            --entitlements "$ENTITLEMENTS_FILE" \
            --force \
            --timestamp \
            --options runtime \
            "$MAIN_EXEC"
    fi
    
    echo ""
    echo "Signing app bundle..."
    
    # Sign the entire app bundle
    codesign --sign "$IDENTITY" \
        --entitlements "$ENTITLEMENTS_FILE" \
        --force \
        --deep \
        --timestamp \
        --options runtime \
        "$FILE_TO_SIGN"
    
elif [[ "$FILE_TO_SIGN" == *.dmg ]]; then
    echo "Detected DMG file, signing..."
    echo ""
    
    # Sign DMG
    codesign --sign "$IDENTITY" \
        --force \
        --timestamp \
        "$FILE_TO_SIGN"
    
else
    echo "Detected generic file, signing..."
    echo ""
    
    # Sign generic file
    codesign --sign "$IDENTITY" \
        --force \
        --timestamp \
        --options runtime \
        "$FILE_TO_SIGN"
fi

if [ $? -ne 0 ]; then
    echo ""
    echo "Error: Signing failed"
    echo ""
    echo "Common issues:"
    echo "  - Certificate expired or not installed"
    echo "  - Identity string incorrect"
    echo "  - Keychain locked"
    echo "  - File already signed with different identity"
    echo ""
    echo "To verify certificate:"
    echo "  security find-identity -v -p codesigning"
    echo ""
    exit 1
fi

echo ""
echo "======================================"
echo "Signing completed successfully!"
echo "======================================"
echo ""

# Verify the signature
echo "Verifying signature..."
codesign --verify --deep --strict --verbose=2 "$FILE_TO_SIGN"

if [ $? -ne 0 ]; then
    echo ""
    echo "Warning: Signature verification failed"
    echo "The file was signed but verification encountered an issue"
    echo ""
    exit 1
fi

echo ""
echo "======================================"
echo "Verification successful!"
echo "======================================"
echo ""
echo "Signed file: $FILE_TO_SIGN"
echo ""

# Display signature details
echo "Signature details:"
codesign -dv --verbose=4 "$FILE_TO_SIGN" 2>&1 | head -20

echo ""
echo "Next steps:"
if [[ "$FILE_TO_SIGN" == *.app ]]; then
    echo "  1. Notarize the app: ./notarize_macos.sh $FILE_TO_SIGN"
    echo "  2. Create DMG: ./create_dmg_macos.sh"
    echo "  3. Sign DMG: ./sign_macos.sh dist/installer/OpenLiveCaption-2.0.0-macOS.dmg"
elif [[ "$FILE_TO_SIGN" == *.dmg ]]; then
    echo "  1. Distribute the signed DMG"
    echo "  2. Users can verify with: spctl --assess --verbose=4 --type open --context context:primary-signature $FILE_TO_SIGN"
fi
echo ""

exit 0
