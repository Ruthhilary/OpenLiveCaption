# macOS Code Signing Guide

This guide explains how to set up code signing and notarization for OpenLiveCaption on macOS to avoid Gatekeeper warnings and distribute your app outside the Mac App Store.

## Overview

macOS requires apps to be signed and notarized to run without security warnings. Code signing proves the app's authenticity, while notarization is Apple's automated security scan that checks for malicious content.

## Prerequisites

### 1. Apple Developer Account

You need an active Apple Developer Program membership ($99/year).

**Sign up**:
1. Visit: https://developer.apple.com/programs/
2. Enroll in the Apple Developer Program
3. Complete identity verification (may take 1-2 days)

**Account Types**:
- **Individual**: Personal developer account
- **Organization**: Company account (requires D-U-N-S number)

### 2. Install Xcode Command Line Tools

The command line tools include `codesign`, `productbuild`, and `notarytool`.

**Installation**:
```bash
xcode-select --install
```

**Verify Installation**:
```bash
codesign --version
# Should output: codesign version...

xcrun notarytool --version
# Should output: notarytool version...
```

### 3. Create Certificates

You need two certificates from Apple:

#### Developer ID Application Certificate

Used to sign the app bundle.

**Create Certificate**:
1. Go to: https://developer.apple.com/account/resources/certificates/list
2. Click "+" to create a new certificate
3. Select "Developer ID Application"
4. Follow the instructions to create a Certificate Signing Request (CSR):
   - Open "Keychain Access" app
   - Menu: Keychain Access > Certificate Assistant > Request a Certificate from a Certificate Authority
   - Enter your email address
   - Select "Saved to disk"
   - Save the CSR file
5. Upload the CSR file
6. Download the certificate (.cer file)
7. Double-click to install in Keychain Access

**Verify Installation**:
```bash
security find-identity -v -p codesigning
```

You should see an entry like:
```
1) ABCDEF1234567890 "Developer ID Application: Your Name (TEAM_ID)"
```

#### Developer ID Installer Certificate (Optional)

Used to sign PKG installers. For DMG distribution, this is optional.

**Create Certificate**:
1. Follow same steps as above
2. Select "Developer ID Installer" instead
3. Install the certificate

### 4. Create App-Specific Password

Required for notarization.

**Create Password**:
1. Go to: https://appleid.apple.com/account/manage
2. Sign in with your Apple ID
3. In "Security" section, click "Generate Password" under "App-Specific Passwords"
4. Enter a label: "OpenLiveCaption Notarization"
5. Copy the generated password (format: xxxx-xxxx-xxxx-xxxx)
6. Save it securely - you won't be able to see it again

## Setup Instructions

### Step 1: Store Credentials Securely

**Set Environment Variables**:
```bash
# Your Apple Developer Team ID (10 characters)
export APPLE_TEAM_ID="ABCDEF1234"

# Your Apple ID email
export APPLE_ID="your-email@example.com"

# App-specific password for notarization
export APPLE_APP_PASSWORD="xxxx-xxxx-xxxx-xxxx"

# Certificate identity (from security find-identity)
export CODESIGN_IDENTITY="Developer ID Application: Your Name (ABCDEF1234)"
```

**Make Permanent** (add to `~/.zshrc` or `~/.bash_profile`):
```bash
echo 'export APPLE_TEAM_ID="ABCDEF1234"' >> ~/.zshrc
echo 'export APPLE_ID="your-email@example.com"' >> ~/.zshrc
echo 'export APPLE_APP_PASSWORD="xxxx-xxxx-xxxx-xxxx"' >> ~/.zshrc
echo 'export CODESIGN_IDENTITY="Developer ID Application: Your Name (ABCDEF1234)"' >> ~/.zshrc
source ~/.zshrc
```

**Security Note**: For production, use Keychain or a secure credential manager instead of environment variables.

### Step 2: Configure Entitlements

Entitlements specify what system resources your app can access.

The project includes `entitlements.plist` with required permissions:
- Microphone access (for audio capture)
- Audio input (for system audio)
- Hardened runtime (required for notarization)

**Review entitlements.plist**:
```xml
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
```

### Step 3: Sign the App Bundle

**Manual Signing**:
```bash
./sign_macos.sh dist/OpenLiveCaption.app
```

**Automated Signing** (integrated with build):
```bash
python build.py --sign
```

The script will:
1. Sign all frameworks and libraries
2. Sign the main executable
3. Sign the app bundle
4. Verify the signature

### Step 4: Notarize the App

After signing, submit to Apple for notarization:

```bash
./notarize_macos.sh dist/OpenLiveCaption.app
```

The script will:
1. Create a ZIP archive of the app
2. Submit to Apple's notarization service
3. Wait for notarization to complete (usually 1-5 minutes)
4. Staple the notarization ticket to the app

### Step 5: Create and Sign DMG

After notarization, create the DMG installer:

```bash
./create_dmg_macos.sh
```

Then sign the DMG:
```bash
./sign_macos.sh dist/installer/OpenLiveCaption-2.0.0-macOS.dmg
```

## Verification

### Verify Code Signature

**Check app bundle signature**:
```bash
codesign --verify --deep --strict --verbose=2 dist/OpenLiveCaption.app
```

Expected output:
```
dist/OpenLiveCaption.app: valid on disk
dist/OpenLiveCaption.app: satisfies its Designated Requirement
```

**Display signature details**:
```bash
codesign -dv --verbose=4 dist/OpenLiveCaption.app
```

### Verify Notarization

**Check notarization status**:
```bash
spctl --assess --verbose=4 --type execute dist/OpenLiveCaption.app
```

Expected output:
```
dist/OpenLiveCaption.app: accepted
source=Notarized Developer ID
```

**Check stapled ticket**:
```bash
stapler validate dist/OpenLiveCaption.app
```

Expected output:
```
The validate action worked!
```

### Test Gatekeeper

1. Copy the signed and notarized app to a different Mac
2. Try to open it
3. Should open without warnings
4. If warnings appear, check signature and notarization status

## Troubleshooting

### Error: "No identity found"

**Cause**: Certificate not installed or expired

**Solution**:
1. Check installed certificates:
   ```bash
   security find-identity -v -p codesigning
   ```
2. If missing, download and install from Apple Developer portal
3. Verify certificate hasn't expired

### Error: "The specified item could not be found in the keychain"

**Cause**: Certificate in wrong keychain or not accessible

**Solution**:
1. Open Keychain Access app
2. Ensure certificate is in "login" keychain
3. Right-click certificate > Get Info > Access Control
4. Add `codesign` to allowed applications

### Error: "code object is not signed at all"

**Cause**: Signing failed or incomplete

**Solution**:
1. Check for error messages during signing
2. Ensure all nested frameworks are signed first
3. Try signing with `--force` flag:
   ```bash
   codesign --force --sign "$CODESIGN_IDENTITY" dist/OpenLiveCaption.app
   ```

### Error: "Invalid Signature" during notarization

**Cause**: Missing entitlements or hardened runtime

**Solution**:
1. Ensure entitlements.plist is used during signing
2. Enable hardened runtime:
   ```bash
   codesign --sign "$CODESIGN_IDENTITY" \
     --entitlements entitlements.plist \
     --options runtime \
     --force \
     dist/OpenLiveCaption.app
   ```

### Error: "The software is damaged and can't be opened"

**Cause**: Gatekeeper quarantine attribute on unsigned/unnotarized app

**Solution**:
1. Remove quarantine attribute (for testing only):
   ```bash
   xattr -cr dist/OpenLiveCaption.app
   ```
2. For distribution, properly sign and notarize the app

### Notarization Fails with "Invalid Bundle"

**Cause**: Missing Info.plist or incorrect bundle structure

**Solution**:
1. Verify Info.plist exists in app bundle
2. Check bundle structure:
   ```bash
   ls -la dist/OpenLiveCaption.app/Contents/
   ```
3. Ensure PyInstaller created proper app bundle

### Notarization Takes Too Long

**Cause**: Apple's servers are busy

**Solution**:
1. Wait patiently (can take up to 1 hour in rare cases)
2. Check status manually:
   ```bash
   xcrun notarytool history --apple-id "$APPLE_ID" --team-id "$APPLE_TEAM_ID"
   ```
3. If stuck, cancel and resubmit

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Build and Sign macOS

on:
  push:
    tags:
      - 'v*'

jobs:
  build-macos:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Build app bundle
        run: python build.py
      
      - name: Import certificate
        env:
          CERTIFICATE_BASE64: ${{ secrets.MACOS_CERTIFICATE_BASE64 }}
          CERTIFICATE_PASSWORD: ${{ secrets.MACOS_CERTIFICATE_PASSWORD }}
        run: |
          echo "$CERTIFICATE_BASE64" | base64 --decode > certificate.p12
          security create-keychain -p actions build.keychain
          security default-keychain -s build.keychain
          security unlock-keychain -p actions build.keychain
          security import certificate.p12 -k build.keychain -P "$CERTIFICATE_PASSWORD" -T /usr/bin/codesign
          security set-key-partition-list -S apple-tool:,apple:,codesign: -s -k actions build.keychain
      
      - name: Sign app bundle
        env:
          CODESIGN_IDENTITY: ${{ secrets.CODESIGN_IDENTITY }}
        run: ./sign_macos.sh dist/OpenLiveCaption.app
      
      - name: Notarize app
        env:
          APPLE_ID: ${{ secrets.APPLE_ID }}
          APPLE_APP_PASSWORD: ${{ secrets.APPLE_APP_PASSWORD }}
          APPLE_TEAM_ID: ${{ secrets.APPLE_TEAM_ID }}
        run: ./notarize_macos.sh dist/OpenLiveCaption.app
      
      - name: Create DMG
        run: ./create_dmg_macos.sh
      
      - name: Sign DMG
        env:
          CODESIGN_IDENTITY: ${{ secrets.CODESIGN_IDENTITY }}
        run: ./sign_macos.sh dist/installer/OpenLiveCaption-2.0.0-macOS.dmg
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: macos-dmg
          path: dist/installer/*.dmg
```

**Required Secrets**:
- `MACOS_CERTIFICATE_BASE64`: Base64-encoded certificate (.p12)
- `MACOS_CERTIFICATE_PASSWORD`: Certificate password
- `CODESIGN_IDENTITY`: Certificate identity string
- `APPLE_ID`: Your Apple ID email
- `APPLE_APP_PASSWORD`: App-specific password
- `APPLE_TEAM_ID`: Your team ID

**Export Certificate**:
1. Open Keychain Access
2. Find your Developer ID Application certificate
3. Right-click > Export
4. Save as .p12 with password
5. Convert to base64:
   ```bash
   base64 -i certificate.p12 -o certificate-base64.txt
   ```

## Best Practices

1. **Sign Everything**: Sign all executables, frameworks, and libraries in the bundle
2. **Use Hardened Runtime**: Required for notarization
3. **Include Entitlements**: Specify all required permissions
4. **Notarize Before Distribution**: Required for apps distributed outside Mac App Store
5. **Staple Notarization Ticket**: Allows offline verification
6. **Test on Clean Systems**: Verify signed apps work on fresh macOS installations
7. **Automate the Process**: Integrate into build pipeline
8. **Monitor Certificate Expiration**: Renew before expiration
9. **Keep Certificates Secure**: Never commit to version control
10. **Document Team Access**: Ensure team members can sign releases

## Cost Considerations

**Annual Costs**:
- Apple Developer Program: $99/year

**ROI Benefits**:
- Required for distribution outside Mac App Store
- Eliminates Gatekeeper warnings
- Builds user trust
- Professional appearance
- Required for macOS 10.15+ (Catalina and later)

## Alternative: Ad-Hoc Signing (Development Only)

For local testing only, you can use ad-hoc signing:

```bash
codesign --sign - --force --deep dist/OpenLiveCaption.app
```

**Important**: Ad-hoc signed apps:
- Will trigger Gatekeeper warnings
- Cannot be notarized
- Only suitable for personal testing
- Will not work on other Macs without disabling Gatekeeper

## Resources

- [Apple Code Signing Guide](https://developer.apple.com/library/archive/documentation/Security/Conceptual/CodeSigningGuide/)
- [Notarizing macOS Software](https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution)
- [codesign Manual](https://www.manpagez.com/man/1/codesign/)
- [notarytool Documentation](https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution/customizing_the_notarization_workflow)
- [Hardened Runtime](https://developer.apple.com/documentation/security/hardened_runtime)

## Support

For issues with code signing:
1. Check this documentation
2. Verify certificate validity and installation
3. Test with manual codesign commands
4. Check Apple Developer forums
5. Contact Apple Developer Support
6. Open an issue on the project repository
