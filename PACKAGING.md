# OpenLiveCaption Packaging Guide

This guide explains how to build and package OpenLiveCaption for distribution on Windows, macOS, and Linux.

## Prerequisites

### All Platforms
- Python 3.8 or later
- All dependencies installed: `pip install -r requirements.txt`
- PyInstaller: `pip install pyinstaller`

### Windows
- **Inno Setup 6** or later (for creating installer)
  - Download from: https://jrsoftware.org/isdl.php
  - Install to default location: `C:\Program Files (x86)\Inno Setup 6`

### macOS
- **Xcode Command Line Tools**
  - Install: `xcode-select --install`
- **create-dmg** (optional, for better DMG appearance)
  - Install: `brew install create-dmg`

### Linux
- **appimage-builder**
  - Install: `pip3 install appimage-builder`
- **Required system packages**:
  ```bash
  sudo apt install python3-pip binutils coreutils desktop-file-utils \
    fakeroot fuse libgdk-pixbuf2.0-dev patchelf squashfs-tools strace \
    util-linux zsync
  ```

## Building the Executable

### Step 1: Build with PyInstaller

Run the build script on your target platform:

```bash
python build.py
```

**Options:**
- `--clean`: Remove previous build artifacts before building
- `--no-optimize`: Disable size optimization (includes CUDA, no UPX)
- `--skip-checks`: Skip dependency checks

**Example:**
```bash
python build.py --clean
```

This will create:
- **Windows**: `dist/OpenLiveCaption.exe`
- **macOS**: `dist/OpenLiveCaption.app`
- **Linux**: `dist/OpenLiveCaption`

### Step 2: Verify the Build

Test the executable before packaging:

**Windows:**
```cmd
dist\OpenLiveCaption.exe
```

**macOS:**
```bash
open dist/OpenLiveCaption.app
```

**Linux:**
```bash
./dist/OpenLiveCaption
```

## Creating Platform-Specific Installers

### Windows Installer

1. Ensure the executable is built: `dist/OpenLiveCaption.exe`

2. Open Inno Setup Compiler

3. Load the script: `installer_windows.iss`

4. Click **Build** → **Compile**

5. The installer will be created at:
   ```
   dist/installer/OpenLiveCaption-2.0.0-Windows-Setup.exe
   ```

**Command Line (if ISCC is in PATH):**
```cmd
iscc installer_windows.iss
```

### macOS DMG

1. Ensure the app bundle is built: `dist/OpenLiveCaption.app`

2. Make the script executable (first time only):
   ```bash
   chmod +x create_dmg_macos.sh
   ```

3. Run the DMG creation script:
   ```bash
   ./create_dmg_macos.sh
   ```

4. The DMG will be created at:
   ```
   dist/installer/OpenLiveCaption-2.0.0-macOS.dmg
   ```

### Linux AppImage

1. Ensure the executable is built: `dist/OpenLiveCaption`

2. Make the script executable (first time only):
   ```bash
   chmod +x create_appimage_linux.sh
   ```

3. Run the AppImage creation script:
   ```bash
   ./create_appimage_linux.sh
   ```

4. The AppImage will be created at:
   ```
   dist/installer/OpenLiveCaption-2.0.0-x86_64.AppImage
   ```

## Size Optimization

The build process includes several optimizations to keep the package under 500MB:

1. **UPX Compression**: Compresses the executable (enabled by default)
2. **CUDA Exclusion**: Excludes CUDA libraries for CPU-only builds
3. **Module Exclusion**: Excludes unnecessary Python modules (matplotlib, scipy, etc.)
4. **Model Exclusion**: Whisper models are downloaded on first run, not bundled

### Checking Package Size

After building, the script will display the package size:

```
📊 Executable size: 245.67 MB
  ✓ Size within 500MB requirement (245.67 MB)
```

If the size exceeds 500MB, consider:
- Using a smaller Whisper model by default (tiny instead of base)
- Excluding additional modules in `openlivecaption.spec`
- Using PyTorch CPU-only build

## Code Signing (Optional)

### Windows

1. Obtain a code signing certificate from a trusted CA

2. Sign the executable:
   ```cmd
   signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com dist\OpenLiveCaption.exe
   ```

3. Sign the installer:
   ```cmd
   signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com dist\installer\OpenLiveCaption-2.0.0-Windows-Setup.exe
   ```

### macOS

1. Obtain an Apple Developer certificate

2. Sign the app bundle:
   ```bash
   codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name" dist/OpenLiveCaption.app
   ```

3. Notarize the app (required for macOS 10.15+):
   ```bash
   xcrun notarytool submit dist/installer/OpenLiveCaption-2.0.0-macOS.dmg \
     --apple-id your@email.com \
     --team-id TEAMID \
     --password app-specific-password \
     --wait
   ```

## Testing the Installers

### Windows
1. Run the installer: `OpenLiveCaption-2.0.0-Windows-Setup.exe`
2. Follow installation wizard
3. Launch from Start Menu or Desktop shortcut
4. Test uninstaller from Control Panel

### macOS
1. Open the DMG: `OpenLiveCaption-2.0.0-macOS.dmg`
2. Drag app to Applications folder
3. Launch from Applications
4. Test by dragging to Trash

### Linux
1. Make executable: `chmod +x OpenLiveCaption-2.0.0-x86_64.AppImage`
2. Run: `./OpenLiveCaption-2.0.0-x86_64.AppImage`
3. Test on different distributions (Ubuntu, Fedora, etc.)

## Troubleshooting

### Build Fails with Missing Dependencies

**Solution:** Install all requirements:
```bash
pip install -r requirements.txt
```

### Executable Size Too Large

**Solution:** Check excluded modules in `openlivecaption.spec` and ensure CUDA is excluded.

### Windows: "Application failed to start"

**Solution:** Install Visual C++ Redistributable:
- Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe

### macOS: "App is damaged and can't be opened"

**Solution:** Remove quarantine attribute:
```bash
xattr -cr /Applications/OpenLiveCaption.app
```

### Linux: "No such file or directory" when running AppImage

**Solution:** Install FUSE:
```bash
sudo apt install fuse libfuse2
```

## Distribution Checklist

Before releasing:

- [ ] Build executable on each platform
- [ ] Test executable on clean system
- [ ] Create installer for each platform
- [ ] Test installer on clean system
- [ ] Verify size is under 500MB
- [ ] Sign executables (if applicable)
- [ ] Test on multiple OS versions
- [ ] Update version numbers in all files
- [ ] Create release notes
- [ ] Upload to distribution platform

## File Structure

After building and packaging, you should have:

```
dist/
├── OpenLiveCaption.exe              # Windows executable
├── OpenLiveCaption.app/             # macOS app bundle
├── OpenLiveCaption                  # Linux executable
└── installer/
    ├── OpenLiveCaption-2.0.0-Windows-Setup.exe
    ├── OpenLiveCaption-2.0.0-macOS.dmg
    └── OpenLiveCaption-2.0.0-x86_64.AppImage
```

## Support

For packaging issues, please check:
- PyInstaller documentation: https://pyinstaller.org/
- Inno Setup documentation: https://jrsoftware.org/ishelp/
- AppImage documentation: https://docs.appimage.org/
