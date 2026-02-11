# Code Signing Overview

This document provides an overview of code signing for OpenLiveCaption across all platforms.

## Why Code Signing?

Code signing is essential for distributing applications to end users:

1. **Security**: Proves the application comes from a verified developer
2. **Trust**: Eliminates security warnings during installation
3. **Integrity**: Ensures the application hasn't been tampered with
4. **Requirements**: Required by modern operating systems (macOS 10.15+, Windows SmartScreen)

## Platform-Specific Guides

### Windows
- **Guide**: [CODE_SIGNING_WINDOWS.md](CODE_SIGNING_WINDOWS.md)
- **Certificate**: Code Signing Certificate from trusted CA
- **Cost**: $200-500/year
- **Tools**: signtool.exe (Windows SDK)
- **Process**: Sign executable → Sign installer
- **Benefit**: Reduces SmartScreen warnings

### macOS
- **Guide**: [CODE_SIGNING_MACOS.md](CODE_SIGNING_MACOS.md)
- **Certificate**: Developer ID Application certificate
- **Cost**: $99/year (Apple Developer Program)
- **Tools**: codesign, notarytool (Xcode Command Line Tools)
- **Process**: Sign app → Notarize → Staple → Create DMG → Sign DMG
- **Benefit**: Required for distribution outside Mac App Store

### Linux
- **Status**: Not required for Linux distributions
- **Alternative**: Package signing for repositories (GPG)
- **Distribution**: AppImage, Flatpak, or repository packages

## Quick Start

### Prerequisites

**Windows**:
1. Obtain code signing certificate (.pfx file)
2. Install Windows SDK
3. Set environment variables:
   ```cmd
   setx CODESIGN_CERT_PATH "C:\path\to\cert.pfx"
   setx CODESIGN_CERT_PASSWORD "your-password"
   ```

**macOS**:
1. Join Apple Developer Program ($99/year)
2. Create Developer ID Application certificate
3. Install Xcode Command Line Tools
4. Set environment variables:
   ```bash
   export CODESIGN_IDENTITY="Developer ID Application: Your Name (TEAM_ID)"
   export APPLE_ID="your-email@example.com"
   export APPLE_APP_PASSWORD="xxxx-xxxx-xxxx-xxxx"
   export APPLE_TEAM_ID="ABCDEF1234"
   ```

### Build and Sign

**Automated** (recommended):
```bash
# Build and sign in one step
python build.py --sign
```

**Manual**:
```bash
# Build first
python build.py

# Then sign
# Windows:
sign_windows.bat dist\OpenLiveCaption.exe

# macOS:
./sign_macos.sh dist/OpenLiveCaption.app
./notarize_macos.sh dist/OpenLiveCaption.app
```

## Verification

### Windows
```cmd
# Verify signature
signtool.exe verify /pa /v dist\OpenLiveCaption.exe

# View signature in Windows Explorer
# Right-click → Properties → Digital Signatures tab
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

## CI/CD Integration

Both Windows and macOS signing can be automated in CI/CD pipelines:

- **GitHub Actions**: See platform-specific guides for examples
- **GitLab CI**: Similar setup with secure variables
- **Jenkins**: Use credential plugins for certificate storage

**Security Best Practices**:
1. Store certificates as encrypted secrets
2. Use base64 encoding for binary certificates
3. Rotate passwords regularly
4. Limit access to signing credentials
5. Use separate certificates for development and production

## Troubleshooting

### Common Issues

**"Certificate not found"**:
- Verify certificate is installed
- Check environment variables
- Ensure certificate hasn't expired

**"Signature verification failed"**:
- Check certificate validity
- Ensure all nested components are signed
- Verify timestamp server is accessible

**"SmartScreen/Gatekeeper warning"**:
- Windows: Build reputation over time or use EV certificate
- macOS: Ensure app is notarized and stapled

### Getting Help

1. Check platform-specific guide
2. Verify certificate installation
3. Test with manual commands
4. Check error logs
5. Contact certificate authority support
6. Open issue on project repository

## Cost Summary

| Platform | Certificate Type | Annual Cost | Required? |
|----------|-----------------|-------------|-----------|
| Windows | Standard Code Signing | $200-300 | Recommended |
| Windows | EV Code Signing | $400-500 | Highly Recommended |
| macOS | Developer ID | $99 | Required for distribution |
| Linux | N/A | Free | Not required |

**Total Annual Cost**: $299-599 for full cross-platform signing

## Best Practices

1. **Automate**: Integrate signing into build pipeline
2. **Secure**: Never commit certificates to version control
3. **Test**: Verify signatures on clean systems
4. **Monitor**: Track certificate expiration dates
5. **Document**: Keep signing procedures documented
6. **Backup**: Maintain secure backups of certificates
7. **Rotate**: Update certificates before expiration
8. **Audit**: Log all signing operations

## Security Considerations

### Certificate Storage

**Development**:
- Store in secure location outside repository
- Use environment variables for paths
- Encrypt certificate files

**Production**:
- Use hardware security modules (HSM)
- Implement access controls
- Enable audit logging
- Use separate certificates per environment

### Private Key Protection

1. **Never commit** private keys to version control
2. **Encrypt** certificate files with strong passwords
3. **Limit access** to authorized personnel only
4. **Rotate regularly** to minimize exposure
5. **Revoke immediately** if compromised

## Resources

### Official Documentation
- [Microsoft Code Signing](https://docs.microsoft.com/en-us/windows/win32/seccrypto/cryptography-tools)
- [Apple Code Signing Guide](https://developer.apple.com/library/archive/documentation/Security/Conceptual/CodeSigningGuide/)
- [Notarizing macOS Software](https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution)

### Certificate Authorities
- [DigiCert](https://www.digicert.com/signing/code-signing-certificates)
- [Sectigo](https://sectigo.com/ssl-certificates-tls/code-signing)
- [GlobalSign](https://www.globalsign.com/en/code-signing-certificate)

### Tools
- [Windows SDK](https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/)
- [Xcode Command Line Tools](https://developer.apple.com/xcode/)
- [Apple Developer Portal](https://developer.apple.com/account/)

## Support

For code signing issues:
1. Review platform-specific documentation
2. Check certificate validity and installation
3. Test with manual signing commands
4. Consult certificate authority support
5. Open issue on project repository with details

## License

This documentation is part of the OpenLiveCaption project and follows the same license.
