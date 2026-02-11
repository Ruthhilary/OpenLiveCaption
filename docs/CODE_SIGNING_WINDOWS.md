# Windows Code Signing Guide

This guide explains how to set up code signing for OpenLiveCaption on Windows to avoid security warnings and build user trust.

## Overview

Code signing digitally signs your executable with a certificate, proving its authenticity and integrity. Windows SmartScreen and antivirus software trust signed executables more than unsigned ones.

## Prerequisites

### 1. Obtain a Code Signing Certificate

You need a valid code signing certificate from a trusted Certificate Authority (CA). Options include:

**Commercial CAs** (Recommended for production):
- **DigiCert**: Industry standard, ~$474/year
  - Website: https://www.digicert.com/signing/code-signing-certificates
  - Supports EV (Extended Validation) certificates for instant SmartScreen reputation
- **Sectigo (formerly Comodo)**: ~$200/year
  - Website: https://sectigo.com/ssl-certificates-tls/code-signing
- **GlobalSign**: ~$250/year
  - Website: https://www.globalsign.com/en/code-signing-certificate

**Certificate Types**:
- **Standard Code Signing**: Basic signing, requires building reputation over time
- **EV Code Signing**: Extended validation, provides instant SmartScreen reputation (recommended)

**What You'll Receive**:
- `.pfx` or `.p12` file containing your certificate and private key
- Password to protect the certificate file

### 2. Install Windows SDK

The Windows SDK includes `signtool.exe`, the command-line tool for signing executables.

**Installation Options**:

**Option A: Install Full Windows SDK**
1. Download from: https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/
2. Run installer and select "Windows SDK Signing Tools for Desktop Apps"
3. Default location: `C:\Program Files (x86)\Windows Kits\10\bin\<version>\x64\signtool.exe`

**Option B: Install via Visual Studio**
1. Install Visual Studio (Community edition is free)
2. In installer, select "Desktop development with C++"
3. signtool.exe will be included

**Verify Installation**:
```cmd
signtool.exe /?
```

## Setup Instructions

### Step 1: Store Certificate Securely

1. **Save Certificate File**:
   - Place your `.pfx` file in a secure location
   - Recommended: `C:\Certificates\openlivecaption-codesign.pfx`
   - **Never commit this file to version control**

2. **Add to .gitignore**:
   ```
   # Code signing certificates
   *.pfx
   *.p12
   /certificates/
   ```

3. **Set Environment Variables** (for automation):
   ```cmd
   setx CODESIGN_CERT_PATH "C:\Certificates\openlivecaption-codesign.pfx"
   setx CODESIGN_CERT_PASSWORD "your-certificate-password"
   ```

   **Security Note**: For production builds, use a secure credential manager instead of environment variables.

### Step 2: Configure Signing Script

The project includes `sign_windows.bat` for automated signing. Configure it:

1. Edit `sign_windows.bat`
2. Update paths if needed:
   ```batch
   set SIGNTOOL_PATH=C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\signtool.exe
   set CERT_PATH=%CODESIGN_CERT_PATH%
   set CERT_PASSWORD=%CODESIGN_CERT_PASSWORD%
   ```

### Step 3: Sign the Executable

**Manual Signing**:
```cmd
sign_windows.bat dist\OpenLiveCaption.exe
```

**Automated Signing** (integrated with build):
```cmd
python build.py --sign
```

### Step 4: Sign the Installer

After creating the installer with Inno Setup:
```cmd
sign_windows.bat dist\installer\OpenLiveCaption-2.0.0-Windows-Setup.exe
```

## Verification

### Verify Signature

**Using signtool**:
```cmd
signtool.exe verify /pa /v dist\OpenLiveCaption.exe
```

Expected output:
```
Successfully verified: dist\OpenLiveCaption.exe
```

**Using Windows Explorer**:
1. Right-click the executable
2. Select "Properties"
3. Go to "Digital Signatures" tab
4. You should see your certificate listed

### Test SmartScreen

1. Copy signed executable to a different machine
2. Try to run it
3. With EV certificate: Should run without warnings
4. With standard certificate: May show warning initially, but builds reputation over time

## Timestamping

Timestamping ensures your signature remains valid even after your certificate expires.

**Timestamp Servers** (free):
- DigiCert: `http://timestamp.digicert.com`
- Sectigo: `http://timestamp.sectigo.com`
- GlobalSign: `http://timestamp.globalsign.com`

The signing script automatically uses DigiCert's timestamp server. To change:

Edit `sign_windows.bat`:
```batch
set TIMESTAMP_URL=http://timestamp.sectigo.com
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Build and Sign Windows

on:
  push:
    tags:
      - 'v*'

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Build executable
        run: python build.py
      
      - name: Import certificate
        run: |
          echo "${{ secrets.CODESIGN_CERT_BASE64 }}" | base64 -d > cert.pfx
        shell: bash
      
      - name: Sign executable
        env:
          CODESIGN_CERT_PATH: cert.pfx
          CODESIGN_CERT_PASSWORD: ${{ secrets.CODESIGN_CERT_PASSWORD }}
        run: sign_windows.bat dist\OpenLiveCaption.exe
      
      - name: Build installer
        run: iscc installer_windows.iss
      
      - name: Sign installer
        env:
          CODESIGN_CERT_PATH: cert.pfx
          CODESIGN_CERT_PASSWORD: ${{ secrets.CODESIGN_CERT_PASSWORD }}
        run: sign_windows.bat dist\installer\OpenLiveCaption-2.0.0-Windows-Setup.exe
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: windows-installer
          path: dist/installer/*.exe
```

**Required Secrets**:
- `CODESIGN_CERT_BASE64`: Base64-encoded certificate file
- `CODESIGN_CERT_PASSWORD`: Certificate password

**Create Base64 Certificate**:
```cmd
certutil -encode openlivecaption-codesign.pfx cert-base64.txt
```

## Troubleshooting

### Error: "SignTool Error: No certificates were found that met all the given criteria"

**Cause**: Certificate file not found or password incorrect

**Solution**:
1. Verify certificate path is correct
2. Verify password is correct
3. Check certificate hasn't expired: `certutil -dump cert.pfx`

### Error: "SignTool Error: The specified timestamp server either could not be reached or returned an invalid response"

**Cause**: Timestamp server is down or unreachable

**Solution**:
1. Check internet connection
2. Try alternative timestamp server
3. Retry after a few minutes

### Warning: "Windows protected your PC" (SmartScreen)

**Cause**: New executable without established reputation

**Solution**:
- **With EV Certificate**: Should not occur
- **With Standard Certificate**: 
  - Reputation builds over time as users download and run your app
  - Typically takes a few weeks and hundreds of downloads
  - Consider upgrading to EV certificate for instant reputation

### Error: "The file is not signed"

**Cause**: Signing failed silently

**Solution**:
1. Run signing command manually to see error details
2. Check signtool.exe is in PATH
3. Verify certificate is valid: `certutil -dump cert.pfx`

## Best Practices

1. **Use EV Certificates for Production**: Provides instant SmartScreen reputation
2. **Always Timestamp**: Ensures signatures remain valid after certificate expiration
3. **Sign All Executables**: Sign both the main executable and installer
4. **Secure Certificate Storage**: Never commit certificates to version control
5. **Use Hardware Security Modules (HSM)**: For maximum security in production
6. **Automate Signing**: Integrate into build pipeline to avoid manual steps
7. **Test on Clean Systems**: Verify signed executables work on fresh Windows installations
8. **Monitor Certificate Expiration**: Renew certificates before they expire
9. **Keep Private Keys Secure**: Treat certificate files like passwords
10. **Document the Process**: Ensure team members can sign releases

## Cost Considerations

**Annual Costs**:
- Standard Code Signing: $200-$300/year
- EV Code Signing: $400-$500/year

**ROI Benefits**:
- Reduced support costs (fewer "can't install" issues)
- Increased user trust and download rates
- Better antivirus detection rates
- Professional appearance

## Alternative: Self-Signed Certificates (Development Only)

For testing purposes only, you can create a self-signed certificate:

```cmd
# Create self-signed certificate
makecert -r -pe -n "CN=OpenLiveCaption Dev" -ss My -sr CurrentUser ^
  -sky signature -eku 1.3.6.1.5.5.7.3.3 -a sha256 -len 2048 ^
  openlivecaption-dev.cer

# Export to PFX
pvk2pfx -pvk openlivecaption-dev.pvk -spc openlivecaption-dev.cer ^
  -pfx openlivecaption-dev.pfx -po "password"

# Sign executable
signtool.exe sign /f openlivecaption-dev.pfx /p "password" /fd SHA256 ^
  /tr http://timestamp.digicert.com /td SHA256 dist\OpenLiveCaption.exe
```

**Important**: Self-signed certificates will trigger SmartScreen warnings. Only use for internal testing.

## Resources

- [Microsoft Code Signing Documentation](https://docs.microsoft.com/en-us/windows/win32/seccrypto/cryptography-tools)
- [SignTool.exe Reference](https://docs.microsoft.com/en-us/windows/win32/seccrypto/signtool)
- [Windows SmartScreen](https://docs.microsoft.com/en-us/windows/security/threat-protection/microsoft-defender-smartscreen/microsoft-defender-smartscreen-overview)
- [Code Signing Best Practices](https://docs.microsoft.com/en-us/windows-hardware/drivers/dashboard/code-signing-best-practices)

## Support

For issues with code signing:
1. Check this documentation
2. Verify certificate validity
3. Test with manual signtool commands
4. Contact your CA's support team
5. Open an issue on the project repository
