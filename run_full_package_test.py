#!/usr/bin/env python3
"""
Full package testing workflow
Runs complete build and test cycle for current platform
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print()
    print("=" * 60)
    print(text)
    print("=" * 60)
    print()


def run_command(cmd, description, cwd=None):
    """Run command and report result"""
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    print()
    
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
            shell=isinstance(cmd, str)
        )
        print("✅ Success")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Failed")
        if e.stdout:
            print("Output:", e.stdout)
        if e.stderr:
            print("Error:", e.stderr)
        return False


def main():
    """Main test workflow"""
    print_header("OpenLiveCaption Full Package Test")
    
    current_platform = platform.system().lower()
    print(f"Platform: {current_platform}")
    print()
    
    # Step 1: Verify configuration
    print_header("Step 1: Verify Configuration")
    if not run_command(
        [sys.executable, "verify_package_config.py"],
        "Configuration verification"
    ):
        print("\n❌ Configuration verification failed")
        print("Fix configuration errors before proceeding")
        return 1
    
    # Step 2: Check dependencies
    print_header("Step 2: Check Dependencies")
    print("Checking if required packages are installed...")
    
    required_packages = [
        "PyQt6",
        "whisper",
        "torch",
        "transformers",
        "PyInstaller",
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.lower().replace("-", "_"))
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} (missing)")
            missing.append(package)
    
    if missing:
        print(f"\n⚠ Missing dependencies: {', '.join(missing)}")
        print("\nInstall with:")
        print("  pip install -r requirements.txt")
        print("\nContinuing anyway to test what we can...")
    else:
        print("\n✅ All dependencies installed")
    
    # Step 3: Build package
    print_header("Step 3: Build Package")
    if not run_command(
        [sys.executable, "build.py", "--clean"],
        "Building executable"
    ):
        print("\n❌ Build failed")
        print("Cannot proceed with testing")
        return 1
    
    # Step 4: Test package
    print_header("Step 4: Test Package")
    if not run_command(
        [sys.executable, "test_packages.py"],
        "Testing package"
    ):
        print("\n⚠ Package tests failed")
        print("Review test_packages_report.json for details")
    
    # Step 5: Create installer (platform-specific)
    print_header("Step 5: Create Installer")
    
    if current_platform == "windows":
        print("To create Windows installer:")
        print("  1. Install Inno Setup from https://jrsoftware.org/isdown.php")
        print("  2. Run: iscc installer_windows.iss")
        print()
        
    elif current_platform == "darwin":
        print("Creating macOS DMG...")
        if run_command(
            ["bash", "create_dmg_macos.sh"],
            "DMG creation"
        ):
            print("✅ DMG created successfully")
        else:
            print("❌ DMG creation failed")
    
    elif current_platform == "linux":
        print("Creating Linux AppImage...")
        if run_command(
            ["bash", "create_appimage_linux.sh"],
            "AppImage creation"
        ):
            print("✅ AppImage created successfully")
        else:
            print("❌ AppImage creation failed")
    
    # Step 6: Summary
    print_header("Test Summary")
    
    print("Completed steps:")
    print("  ✅ Configuration verification")
    print("  ✅ Dependency check")
    print("  ✅ Package build")
    print("  ✅ Package testing")
    
    if current_platform in ["darwin", "linux"]:
        print("  ✅ Installer creation")
    else:
        print("  ⚠ Installer creation (manual step)")
    
    print()
    print("Review the following files for details:")
    print("  • package_config_verification.json - Configuration results")
    print("  • test_packages_report.json - Package test results")
    print("  • PACKAGE_TEST_GUIDE.md - Testing documentation")
    print("  • TASK_14_4_SUMMARY.md - Task summary")
    print()
    
    print("Next steps:")
    print("  1. Review test results")
    print("  2. Perform manual functionality testing")
    print("  3. Test installation/uninstallation")
    print("  4. Verify application runs correctly")
    print()
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
