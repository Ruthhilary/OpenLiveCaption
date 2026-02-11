#!/bin/bash
# macOS Notarization Script for OpenLiveCaption
# Submits app bundle to Apple for notarization

set -e

echo "======================================"
echo "OpenLiveCaption macOS Notarization"
echo "======================================"
echo ""

# Configuration from environment variables
# Set these environment variables:
#   APPLE_ID - Your Apple ID email
#   APPLE_APP_PASSWORD - App-specific password for notarization
#   APPLE_TEAM_ID - Your Apple Developer Team ID (10 characters)
APPLE_ID="${APPLE_ID}"
APP_PASSWORD="${APPLE_APP_PASSWORD}"
TEAM_ID="${APPLE_TEAM_ID}"

# Check if file to notarize was provided
if [ -z "$1" ]; then
    echo "Error: No file specified to notarize"
    echo ""
    echo "Usage: ./notarize_macos.sh <app-bundle>"
    echo "Example: ./notarize_macos.sh dist/OpenLiveCaption.app"
    echo ""
    exit 1
fi

APP_BUNDLE="$1"

# Check if app bundle exists
if [ ! -d "$APP_BUNDLE" ]; then
    echo "Error: App bundle not found: $APP_BUNDLE"
    exit 1
fi

echo "App bundle: $APP_BUNDLE"
echo ""

# Check if notarytool is available
if ! command -v xcrun &> /dev/null; then
    echo "Error: xcrun not found"
    echo ""
    echo "Please install Xcode Command Line Tools:"
    echo "  xcode-select --install"
    echo ""
    exit 1
fi

echo "✓ Found xcrun: $(which xcrun)"

# Check if credentials are set
if [ -z "$APPLE_ID" ]; then
    echo "Error: Apple ID not set"
    echo ""
    echo "Please set the APPLE_ID environment variable:"
    echo "  export APPLE_ID=\"your-email@example.com\""
    echo ""
    exit 1
fi

if [ -z "$APP_PASSWORD" ]; then
    echo "Error: App-specific password not set"
    echo ""
    echo "Please set the APPLE_APP_PASSWORD environment variable:"
    echo "  export APPLE_APP_PASSWORD=\"xxxx-xxxx-xxxx-xxxx\""
    echo ""
    echo "To create an app-specific password:"
    echo "  1. Go to https://appleid.apple.com/account/manage"
    echo "  2. Sign in with your Apple ID"
    echo "  3. In Security section, generate an app-specific password"
    echo ""
    exit 1
fi

if [ -z "$TEAM_ID" ]; then
    echo "Error: Team ID not set"
    echo ""
    echo "Please set the APPLE_TEAM_ID environment variable:"
    echo "  export APPLE_TEAM_ID=\"ABCDEF1234\""
    echo ""
    echo "To find your Team ID:"
    echo "  1. Go to https://developer.apple.com/account"
    echo "  2. Look for 'Team ID' in your membership details"
    echo ""
    exit 1
fi

echo "✓ Apple ID: $APPLE_ID"
echo "✓ Team ID: $TEAM_ID"
echo "✓ App password: [HIDDEN]"
echo ""

# Verify app is signed
echo "Verifying app signature..."
if ! codesign --verify --deep --strict "$APP_BUNDLE" 2>/dev/null; then
    echo "Error: App bundle is not properly signed"
    echo ""
    echo "Please sign the app first:"
    echo "  ./sign_macos.sh $APP_BUNDLE"
    echo ""
    exit 1
fi

echo "✓ App is properly signed"
echo ""

# Create ZIP archive for notarization
ZIP_FILE="${APP_BUNDLE%.app}.zip"
echo "Creating ZIP archive for notarization..."
echo "  Output: $ZIP_FILE"

# Remove existing ZIP if present
if [ -f "$ZIP_FILE" ]; then
    rm "$ZIP_FILE"
fi

# Create ZIP using ditto (preserves code signatures)
ditto -c -k --keepParent "$APP_BUNDLE" "$ZIP_FILE"

if [ ! -f "$ZIP_FILE" ]; then
    echo "Error: Failed to create ZIP archive"
    exit 1
fi

ZIP_SIZE=$(du -h "$ZIP_FILE" | cut -f1)
echo "✓ Created ZIP archive ($ZIP_SIZE)"
echo ""

# Submit for notarization
echo "Submitting to Apple for notarization..."
echo "This may take 1-5 minutes..."
echo ""

SUBMIT_OUTPUT=$(xcrun notarytool submit "$ZIP_FILE" \
    --apple-id "$APPLE_ID" \
    --password "$APP_PASSWORD" \
    --team-id "$TEAM_ID" \
    --wait 2>&1)

echo "$SUBMIT_OUTPUT"
echo ""

# Check if notarization succeeded
if echo "$SUBMIT_OUTPUT" | grep -q "status: Accepted"; then
    echo "✓ Notarization succeeded!"
    
    # Extract submission ID
    SUBMISSION_ID=$(echo "$SUBMIT_OUTPUT" | grep "id:" | head -1 | awk '{print $2}')
    echo "  Submission ID: $SUBMISSION_ID"
    
elif echo "$SUBMIT_OUTPUT" | grep -q "status: Invalid"; then
    echo "✗ Notarization failed: Invalid submission"
    echo ""
    echo "Getting detailed error log..."
    
    # Extract submission ID
    SUBMISSION_ID=$(echo "$SUBMIT_OUTPUT" | grep "id:" | head -1 | awk '{print $2}')
    
    if [ -n "$SUBMISSION_ID" ]; then
        xcrun notarytool log "$SUBMISSION_ID" \
            --apple-id "$APPLE_ID" \
            --password "$APP_PASSWORD" \
            --team-id "$TEAM_ID"
    fi
    
    echo ""
    echo "Common issues:"
    echo "  - Missing or invalid entitlements"
    echo "  - Unsigned nested frameworks"
    echo "  - Hardened runtime not enabled"
    echo "  - Invalid bundle structure"
    echo ""
    echo "See docs/CODE_SIGNING_MACOS.md for troubleshooting"
    echo ""
    
    # Clean up ZIP
    rm "$ZIP_FILE"
    exit 1
    
else
    echo "✗ Notarization failed or timed out"
    echo ""
    echo "You can check the status manually:"
    echo "  xcrun notarytool history --apple-id \"$APPLE_ID\" --team-id \"$TEAM_ID\""
    echo ""
    
    # Clean up ZIP
    rm "$ZIP_FILE"
    exit 1
fi

echo ""

# Staple the notarization ticket to the app
echo "Stapling notarization ticket to app..."
xcrun stapler staple "$APP_BUNDLE"

if [ $? -ne 0 ]; then
    echo "Warning: Failed to staple notarization ticket"
    echo "The app is notarized but the ticket is not stapled"
    echo "Users will need internet connection to verify notarization"
    echo ""
else
    echo "✓ Notarization ticket stapled successfully"
    echo ""
fi

# Verify stapling
echo "Verifying stapled ticket..."
xcrun stapler validate "$APP_BUNDLE"

if [ $? -ne 0 ]; then
    echo "Warning: Staple validation failed"
    echo ""
else
    echo "✓ Staple validation successful"
    echo ""
fi

# Clean up ZIP file
rm "$ZIP_FILE"
echo "✓ Cleaned up temporary ZIP file"
echo ""

# Verify with spctl
echo "Verifying with Gatekeeper..."
spctl --assess --verbose=4 --type execute "$APP_BUNDLE"

if [ $? -ne 0 ]; then
    echo "Warning: Gatekeeper assessment failed"
    echo ""
else
    echo "✓ Gatekeeper assessment passed"
    echo ""
fi

echo "======================================"
echo "Notarization completed successfully!"
echo "======================================"
echo ""
echo "Notarized app: $APP_BUNDLE"
echo ""
echo "Next steps:"
echo "  1. Create DMG: ./create_dmg_macos.sh"
echo "  2. Sign DMG: ./sign_macos.sh dist/installer/OpenLiveCaption-2.0.0-macOS.dmg"
echo "  3. Distribute the DMG"
echo ""
echo "The app will now run without Gatekeeper warnings on macOS 10.15+"
echo ""

exit 0
