#!/bin/bash
# Setup script to make packaging scripts executable

echo "Setting up packaging scripts..."

# Make shell scripts executable
chmod +x create_dmg_macos.sh
chmod +x create_appimage_linux.sh

echo "✓ create_dmg_macos.sh is now executable"
echo "✓ create_appimage_linux.sh is now executable"
echo ""
echo "Packaging scripts are ready to use!"
echo ""
echo "Next steps:"
echo "1. Build executable: python build.py"
echo "2. Create installer for your platform:"
echo "   - Windows: Use Inno Setup with installer_windows.iss"
echo "   - macOS: Run ./create_dmg_macos.sh"
echo "   - Linux: Run ./create_appimage_linux.sh"
echo ""
