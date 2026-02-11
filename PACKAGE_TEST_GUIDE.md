# Package Testing Guide - Task 14.4

This guide documents the testing process for packaged applications across all platforms.

## Prerequisites

Before testing packages, ensure they are built:

### Windows
```bash
# Install dependencies
pip install -r requirements.txt

# Build executable
python build.py --clean

# Create installer (requires Inno Setup)
iscc installer_windows.iss
```

### macOS
```bash
# Install dependencies
pip install -r requirements.txt

# Build app bundle
python build.py --clean

# Create DMG
./create_dmg_macos.sh
```

### Linux
```bash
# Install dependencies
pip install -r requirements.txt

# Build executable
python build.py --clean

# Create AppImage (requires appimage-builder)
./create_appimage_linux.sh
```

## Test Execution

Run the automated test script:
```bash
python test_packages.py
```

## Test Criteria

### 1. Build and Test Windows Installer

**Expected Outputs:**
- `dist/OpenLiveCaption.exe` - Main executable
- `dist/installer/OpenLiveCaption-2.0.0-Windows-Setup.exe` - Installer

**Tests:**
- ✓ Executable exists and is valid PE format
- ✓ Size under 500MB
- ✓ Installer can be created with Inno Setup
- ✓ Installer includes all dependencies
- ✓ Installer creates start menu shortcuts
- ✓ Installer creates uninstaller

**Manual Verification:**
1. Run the installer
2. Launch OpenLiveCaption from Start Menu
3. Verify application starts without errors
4. Test basic functionality (audio capture, transcription)
5. Uninstall and verify clean removal

### 2. Build and Test macOS DMG

**Expected Outputs:**
- `dist/OpenLiveCaption.app` - App bundle
- `dist/installer/OpenLiveCaption-2.0.0-macOS.dmg` - DMG installer

**Tests:**
- ✓ App bundle exists and is valid Mach-O format
- ✓ Size under 500MB
- ✓ Info.plist is present and valid
- ✓ DMG can be created
- ✓ DMG includes Applications symlink
- ✓ All dependencies bundled

**Manual Verification:**
1. Mount the DMG
2. Drag app to Applications folder
3. Launch OpenLiveCaption
4. Verify application starts without errors
5. Test basic functionality
6. Check for code signing warnings (expected without certificate)

### 3. Build and Test Linux AppImage

**Expected Outputs:**
- `dist/OpenLiveCaption` - Main executable
- `dist/installer/OpenLiveCaption-2.0.0-x86_64.AppImage` - AppImage

**Tests:**
- ✓ Executable exists and is valid ELF format
- ✓ Size under 500MB
- ✓ Executable has execute permissions
- ✓ AppImage can be created
- ✓ AppImage includes all dependencies
- ✓ Desktop integration files present

**Manual Verification:**
1. Make AppImage executable: `chmod +x OpenLiveCaption-2.0.0-x86_64.AppImage`
2. Run AppImage: `./OpenLiveCaption-2.0.0-x86_64.AppImage`
3. Verify application starts without errors
4. Test basic functionality
5. Check system integration (tray icon, etc.)

### 4. Verify All Dependencies Included

**Required Dependencies:**
- PyQt6 (GUI framework)
- OpenAI Whisper (transcription)
- PyTorch (ML backend)
- Transformers (translation)
- NumPy (numerical operations)
- sounddevice/pyaudiowpatch (audio capture)
- soundfile (audio file handling)

**Verification Methods:**

**Windows:**
```bash
# Use Dependencies.exe or similar tool
Dependencies.exe dist\OpenLiveCaption.exe
```

**macOS:**
```bash
# Check dynamic libraries
otool -L dist/OpenLiveCaption.app/Contents/MacOS/OpenLiveCaption
```

**Linux:**
```bash
# Check shared libraries
ldd dist/OpenLiveCaption
```

**Runtime Test:**
- Launch application
- Attempt to start audio capture
- Attempt to transcribe audio
- Check for missing dependency errors

### 5. Verify Size Under 500MB

**Automated Check:**
The `test_packages.py` script automatically checks size requirements.

**Manual Check:**

**Windows:**
```bash
dir dist\OpenLiveCaption.exe
```

**macOS:**
```bash
du -sh dist/OpenLiveCaption.app
```

**Linux:**
```bash
du -h dist/OpenLiveCaption
```

**Size Optimization Tips:**
- Exclude CUDA libraries (CPU-only build)
- Use UPX compression
- Exclude unnecessary Python packages
- Strip debug symbols

## Test Results

### Current Platform Test Results

Run `python test_packages.py` to generate `test_packages_report.json` with detailed results.

### Expected Results

All tests should pass with:
- ✅ Package exists
- ✅ Valid executable format
- ✅ Size under 500MB
- ✅ Dependencies included
- ✅ Manual functionality test passes

## Troubleshooting

### Build Fails
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Check Python version (3.8+)
- Verify disk space available

### Size Exceeds 500MB
- Enable UPX compression in spec file
- Exclude CUDA libraries
- Remove unnecessary packages from excludes list
- Consider using smaller Whisper model as default

### Missing Dependencies
- Check PyInstaller hidden imports
- Add missing modules to spec file
- Use `--collect-all` flag for problematic packages

### Installer Creation Fails

**Windows:**
- Install Inno Setup from https://jrsoftware.org/isdown.php
- Verify paths in installer_windows.iss

**macOS:**
- Ensure hdiutil is available (built-in)
- Check disk space for DMG creation

**Linux:**
- Install appimage-builder: `pip install appimage-builder`
- Install system dependencies: `sudo apt install libfuse2`

## Requirements Validation

This task validates:
- **Requirement 5.4**: Application package includes all required dependencies
- **Requirement 5.7**: Application package is under 500MB in size

## Completion Checklist

- [ ] Windows executable built and tested
- [ ] Windows installer created and tested
- [ ] macOS app bundle built and tested
- [ ] macOS DMG created and tested
- [ ] Linux executable built and tested
- [ ] Linux AppImage created and tested
- [ ] All packages under 500MB
- [ ] All dependencies verified
- [ ] Manual functionality tests passed
- [ ] Test report generated

## Notes

- Code signing (Requirement 5.6) is handled in Task 15 (optional for MVP)
- Full manual testing on all platforms is covered in Task 17.3
- This task focuses on build verification and basic package validation
