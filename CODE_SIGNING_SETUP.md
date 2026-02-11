# Code Signing Setup Complete

Task 15 (Code Signing) has been implemented for OpenLiveCaption. This document summarizes what was created and how to use it.

## What Was Implemented

### Documentation
1. **docs/CODE_SIGNING_README.md** - Overview of code signing across all platforms
2. **docs/CODE_SIGNING_WINDOWS.md** - Comprehensive Windows code signing guide
3. **docs/CODE_SIGNING_MACOS.md** - Comprehensive macOS code signing and notarization guide

### Scripts

#### Windows
- **sign_windows.bat** - Automated Windows executable signing script
  - Signs executables and installers
  - Uses signtool.exe from Windows SDK
  - Includes timestamping for long-term validity

#### macOS
- **sign_macos.sh** - Automated macOS app bundle signing script
  - Signs nested frameworks and libraries
  - Signs main executable with entitlements
  - Signs entire app bundle with hardened runtime
  
- **notarize_macos.sh** - Automated macOS notarization script
  - Submits app to Apple for notarization
  - Waits for notarization completion
  - Staples notarization ticket to app

- **entitlements.plist** - macOS entitlements configuration
  - Microphone access permission
  - Unsigned executable memory (for Python)
  - Library validation disabled (for dynamic libraries)

### Build Integration
- **build.py** - Updated with `--sign` flag
  - Automatically signs executables during build
  - Supports both Windows and macOS
  - Provides helpful next-step instructions

### Security
- **.gitignore** - Updated to prevent certificate commits
  - Blocks .pfx, .p12, .cer, .pvk files
  - Blocks certificate directories
  - Blocks base64-encoded certificates

## How to Use

### Prerequisites

#### Windows
1. Obtain a code signing certificate from a trusted CA (DigiCert, Sectigo, GlobalSign)
2. Install Windows SDK for signtool.exe
3. Set environment variables:
   ```cmd
   setx CODESIGN_CERT_PATH "C:\path\to\certificate.pfx"
   setx CODESIGN_CERT_PASSWORD "your-password"
   ```

#### macOS
1. Join Apple Developer Program ($99/year)
2. Create Developer ID Application certificate
3. Create app-specific password for notarization
4. Install Xcode Command Line Tools
5. Set environment variables:
   ```bash
   export CODESIGN_IDENTITY="Developer ID Application: Your Name (TEAM_ID)"
   export APPLE_ID="your-email@example.com"
   export APPLE_APP_PASSWORD="xxxx-xxxx-xxxx-xxxx"
   export APPLE_TEAM_ID="ABCDEF1234"
   ```

### Quick Start

#### Option 1: Automated (Recommended)
```bash
# Build and sign in one command
python build.py --sign
```

#### Option 2: Manual

**Windows**:
```cmd
# Build
python build.py

# Sign executable
sign_windows.bat dist\OpenLiveCaption.exe

# Build installer
iscc installer_windows.iss

# Sign installer
sign_windows.bat dist\installer\OpenLiveCaption-2.0.0-Windows-Setup.exe
```

**macOS**:
```bash
# Build
python build.py

# Sign app bundle
./sign_macos.sh dist/OpenLiveCaption.app

# Notarize
./notarize_macos.sh dist/OpenLiveCaption.app

# Create DMG
./create_dmg_macos.sh

# Sign DMG
./sign_macos.sh dist/installer/OpenLiveCaption-2.0.0-macOS.dmg
```

## Verification

### Windows
```cmd
# Verify signature
signtool.exe verify /pa /v dist\OpenLiveCaption.exe

# Or right-click → Properties → Digital Signatures tab
```

### macOS
```bash
# Verify signature
codesign --verify --deep --strict --verbose=2 dist/OpenLiveCaption.app

# Verify notarization
spctl --assess --verbose=4 --type execute dist/OpenLiveCaption.app

# Check stapled ticket
stapler validate dist/OpenLiveCaption.app
```

## Benefits

### Windows
- Reduces SmartScreen warnings
- Builds user trust
- Professional appearance
- Better antivirus detection

### macOS
- **Required** for distribution outside Mac App Store
- Eliminates Gatekeeper warnings
- Required for macOS 10.15+ (Catalina and later)
- Professional appearance

## Cost Summary

| Platform | Certificate | Annual Cost | Status |
|----------|------------|-------------|---------|
| Windows | Standard Code Signing | $200-300 | Optional but recommended |
| Windows | EV Code Signing | $400-500 | Highly recommended |
| macOS | Developer ID | $99 | Required for distribution |

## Important Notes

### Security
1. **Never commit certificates** to version control
2. Store certificates securely outside the repository
3. Use strong passwords for certificate files
4. Rotate certificates before expiration
5. Revoke immediately if compromised

### Windows Specific
- Standard certificates require building reputation over time
- EV certificates provide instant SmartScreen reputation
- Timestamping ensures signatures remain valid after certificate expiration

### macOS Specific
- Notarization is **required** for macOS 10.15+ (Catalina and later)
- Stapling allows offline verification
- Hardened runtime is required for notarization
- Entitlements must be specified for system access

## Troubleshooting

### Common Issues

**"Certificate not found"**:
- Check environment variables are set correctly
- Verify certificate file exists at specified path
- Ensure certificate hasn't expired

**"Signing failed"**:
- Check certificate password is correct
- Verify certificate is valid and not expired
- Ensure signing tools are installed

**"Notarization failed" (macOS)**:
- Ensure app is properly signed first
- Check all nested frameworks are signed
- Verify hardened runtime is enabled
- Review entitlements.plist

### Getting Help

1. Read the platform-specific guide in docs/
2. Check certificate validity and installation
3. Test with manual signing commands
4. Review error messages carefully
5. Contact certificate authority support
6. Open issue on project repository

## Next Steps

1. **Obtain Certificates**: Purchase/create certificates for your target platforms
2. **Configure Environment**: Set up environment variables with certificate paths
3. **Test Signing**: Run signing scripts manually to verify setup
4. **Integrate CI/CD**: Add signing to your automated build pipeline
5. **Document Process**: Keep internal documentation for team members

## Resources

- **Windows Guide**: docs/CODE_SIGNING_WINDOWS.md
- **macOS Guide**: docs/CODE_SIGNING_MACOS.md
- **Overview**: docs/CODE_SIGNING_README.md

## Status

✅ Task 15.1: Windows code signing setup - **COMPLETE**
✅ Task 15.2: macOS code signing setup - **COMPLETE**
✅ Task 15: Code signing implementation - **COMPLETE**

All code signing infrastructure is in place and ready to use once certificates are obtained.
