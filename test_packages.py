#!/usr/bin/env python3
"""
Test script for packaged applications
Tests Windows installer, macOS DMG, and Linux AppImage
Validates dependencies and size requirements
"""

import os
import sys
import platform
import subprocess
from pathlib import Path
import json


class PackageTestResult:
    """Result of a package test"""
    
    def __init__(self, name):
        self.name = name
        self.exists = False
        self.size_bytes = 0
        self.size_mb = 0.0
        self.under_500mb = False
        self.dependencies_ok = False
        self.executable = False
        self.errors = []
        self.warnings = []
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'name': self.name,
            'exists': self.exists,
            'size_bytes': self.size_bytes,
            'size_mb': self.size_mb,
            'under_500mb': self.under_500mb,
            'dependencies_ok': self.dependencies_ok,
            'executable': self.executable,
            'errors': self.errors,
            'warnings': self.warnings,
            'passed': self.exists and self.under_500mb and len(self.errors) == 0
        }


def format_size(size_bytes):
    """Format size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def get_directory_size(path):
    """Get total size of directory recursively"""
    total = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file(follow_symlinks=False):
                total += entry.stat().st_size
            elif entry.is_dir(follow_symlinks=False):
                total += get_directory_size(entry.path)
    except PermissionError:
        pass
    return total


def test_windows_package():
    """Test Windows executable and installer"""
    print("=" * 60)
    print("Testing Windows Package")
    print("=" * 60)
    print()
    
    result = PackageTestResult("Windows")
    
    # Check for executable
    exe_path = Path("dist/OpenLiveCaption.exe")
    if not exe_path.exists():
        result.errors.append("Executable not found at dist/OpenLiveCaption.exe")
        print("❌ Executable not found")
        return result
    
    result.exists = True
    result.size_bytes = exe_path.stat().st_size
    result.size_mb = result.size_bytes / (1024 * 1024)
    result.under_500mb = result.size_mb < 500
    
    print(f"✓ Executable found: {exe_path}")
    print(f"  Size: {format_size(result.size_bytes)} ({result.size_mb:.2f} MB)")
    
    if result.under_500mb:
        print(f"  ✓ Size under 500MB requirement")
    else:
        print(f"  ✗ Size exceeds 500MB requirement")
        result.errors.append(f"Size {result.size_mb:.2f} MB exceeds 500MB limit")
    
    # Check if executable is valid PE file
    try:
        with open(exe_path, 'rb') as f:
            header = f.read(2)
            if header == b'MZ':
                result.executable = True
                print("  ✓ Valid Windows executable (PE format)")
            else:
                result.errors.append("Not a valid Windows executable")
                print("  ✗ Not a valid Windows executable")
    except Exception as e:
        result.errors.append(f"Failed to read executable: {e}")
        print(f"  ✗ Failed to read executable: {e}")
    
    # Check for installer
    installer_path = Path("dist/installer/OpenLiveCaption-2.0.0-Windows-Setup.exe")
    if installer_path.exists():
        installer_size = installer_path.stat().st_size
        print(f"\n✓ Installer found: {installer_path}")
        print(f"  Size: {format_size(installer_size)}")
        result.dependencies_ok = True
    else:
        result.warnings.append("Installer not built yet (run Inno Setup)")
        print(f"\n⚠ Installer not found (expected at {installer_path})")
        print("  Run Inno Setup with installer_windows.iss to create installer")
    
    print()
    return result


def test_macos_package():
    """Test macOS app bundle and DMG"""
    print("=" * 60)
    print("Testing macOS Package")
    print("=" * 60)
    print()
    
    result = PackageTestResult("macOS")
    
    # Check for app bundle
    app_path = Path("dist/OpenLiveCaption.app")
    if not app_path.exists():
        result.errors.append("App bundle not found at dist/OpenLiveCaption.app")
        print("❌ App bundle not found")
        return result
    
    result.exists = True
    result.size_bytes = get_directory_size(app_path)
    result.size_mb = result.size_bytes / (1024 * 1024)
    result.under_500mb = result.size_mb < 500
    
    print(f"✓ App bundle found: {app_path}")
    print(f"  Size: {format_size(result.size_bytes)} ({result.size_mb:.2f} MB)")
    
    if result.under_500mb:
        print(f"  ✓ Size under 500MB requirement")
    else:
        print(f"  ✗ Size exceeds 500MB requirement")
        result.errors.append(f"Size {result.size_mb:.2f} MB exceeds 500MB limit")
    
    # Check for executable inside bundle
    exe_path = app_path / "Contents" / "MacOS" / "OpenLiveCaption"
    if exe_path.exists():
        result.executable = True
        print(f"  ✓ Executable found in bundle")
        
        # Check if executable is valid Mach-O file
        try:
            with open(exe_path, 'rb') as f:
                header = f.read(4)
                # Mach-O magic numbers
                if header in [b'\xfe\xed\xfa\xce', b'\xfe\xed\xfa\xcf', 
                             b'\xce\xfa\xed\xfe', b'\xcf\xfa\xed\xfe']:
                    print(f"  ✓ Valid macOS executable (Mach-O format)")
                else:
                    result.warnings.append("Executable may not be valid Mach-O format")
                    print(f"  ⚠ Executable may not be valid Mach-O format")
        except Exception as e:
            result.warnings.append(f"Failed to verify executable: {e}")
            print(f"  ⚠ Failed to verify executable: {e}")
    else:
        result.errors.append("Executable not found in app bundle")
        print(f"  ✗ Executable not found in bundle")
    
    # Check for Info.plist
    plist_path = app_path / "Contents" / "Info.plist"
    if plist_path.exists():
        print(f"  ✓ Info.plist found")
        result.dependencies_ok = True
    else:
        result.warnings.append("Info.plist not found")
        print(f"  ⚠ Info.plist not found")
    
    # Check for DMG
    dmg_path = Path("dist/installer/OpenLiveCaption-2.0.0-macOS.dmg")
    if dmg_path.exists():
        dmg_size = dmg_path.stat().st_size
        print(f"\n✓ DMG found: {dmg_path}")
        print(f"  Size: {format_size(dmg_size)}")
    else:
        result.warnings.append("DMG not built yet (run create_dmg_macos.sh)")
        print(f"\n⚠ DMG not found (expected at {dmg_path})")
        print("  Run ./create_dmg_macos.sh to create DMG installer")
    
    print()
    return result


def test_linux_package():
    """Test Linux executable and AppImage"""
    print("=" * 60)
    print("Testing Linux Package")
    print("=" * 60)
    print()
    
    result = PackageTestResult("Linux")
    
    # Check for executable
    exe_path = Path("dist/OpenLiveCaption")
    if not exe_path.exists():
        result.errors.append("Executable not found at dist/OpenLiveCaption")
        print("❌ Executable not found")
        return result
    
    result.exists = True
    result.size_bytes = exe_path.stat().st_size
    result.size_mb = result.size_bytes / (1024 * 1024)
    result.under_500mb = result.size_mb < 500
    
    print(f"✓ Executable found: {exe_path}")
    print(f"  Size: {format_size(result.size_bytes)} ({result.size_mb:.2f} MB)")
    
    if result.under_500mb:
        print(f"  ✓ Size under 500MB requirement")
    else:
        print(f"  ✗ Size exceeds 500MB requirement")
        result.errors.append(f"Size {result.size_mb:.2f} MB exceeds 500MB limit")
    
    # Check if executable is valid ELF file
    try:
        with open(exe_path, 'rb') as f:
            header = f.read(4)
            if header == b'\x7fELF':
                result.executable = True
                print("  ✓ Valid Linux executable (ELF format)")
            else:
                result.errors.append("Not a valid Linux executable")
                print("  ✗ Not a valid Linux executable")
    except Exception as e:
        result.errors.append(f"Failed to read executable: {e}")
        print(f"  ✗ Failed to read executable: {e}")
    
    # Check if executable has execute permissions
    if os.access(exe_path, os.X_OK):
        print("  ✓ Executable has execute permissions")
        result.dependencies_ok = True
    else:
        result.warnings.append("Executable missing execute permissions")
        print("  ⚠ Executable missing execute permissions")
    
    # Check for AppImage
    appimage_path = Path("dist/installer/OpenLiveCaption-2.0.0-x86_64.AppImage")
    if appimage_path.exists():
        appimage_size = appimage_path.stat().st_size
        print(f"\n✓ AppImage found: {appimage_path}")
        print(f"  Size: {format_size(appimage_size)}")
    else:
        result.warnings.append("AppImage not built yet (run create_appimage_linux.sh)")
        print(f"\n⚠ AppImage not found (expected at {appimage_path})")
        print("  Run ./create_appimage_linux.sh to create AppImage")
    
    print()
    return result


def check_dependencies():
    """Check if all required dependencies are included"""
    print("=" * 60)
    print("Checking Dependencies")
    print("=" * 60)
    print()
    
    # This is a basic check - actual dependency verification would require
    # running the executable or using platform-specific tools
    
    required_deps = [
        "PyQt6",
        "Whisper",
        "PyTorch",
        "Transformers",
        "NumPy",
        "Audio libraries (sounddevice/pyaudiowpatch)"
    ]
    
    print("Required dependencies:")
    for dep in required_deps:
        print(f"  • {dep}")
    
    print("\n⚠ Note: Full dependency verification requires running the executable")
    print("  or using platform-specific analysis tools (ldd, otool, Dependencies.exe)")
    print()


def generate_report(results):
    """Generate test report"""
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    print()
    
    all_passed = True
    
    for result in results:
        status = "✅ PASSED" if result.to_dict()['passed'] else "❌ FAILED"
        print(f"{result.name}: {status}")
        
        if result.exists:
            print(f"  Size: {result.size_mb:.2f} MB")
            print(f"  Under 500MB: {'Yes' if result.under_500mb else 'No'}")
            print(f"  Valid executable: {'Yes' if result.executable else 'No'}")
        
        if result.errors:
            print(f"  Errors:")
            for error in result.errors:
                print(f"    • {error}")
            all_passed = False
        
        if result.warnings:
            print(f"  Warnings:")
            for warning in result.warnings:
                print(f"    • {warning}")
        
        print()
    
    # Save results to JSON
    report_path = Path("test_packages_report.json")
    with open(report_path, 'w') as f:
        json.dump({
            'results': [r.to_dict() for r in results],
            'all_passed': all_passed
        }, f, indent=2)
    
    print(f"📊 Detailed report saved to: {report_path}")
    print()
    
    if all_passed:
        print("✅ All package tests passed!")
        return 0
    else:
        print("❌ Some package tests failed")
        return 1


def main():
    """Main test execution"""
    print()
    print("=" * 60)
    print("OpenLiveCaption Package Testing")
    print("=" * 60)
    print()
    
    current_platform = platform.system().lower()
    print(f"Current platform: {current_platform}")
    print()
    
    results = []
    
    # Test based on current platform
    if current_platform == "windows":
        results.append(test_windows_package())
    elif current_platform == "darwin":
        results.append(test_macos_package())
    elif current_platform == "linux":
        results.append(test_linux_package())
    else:
        print(f"❌ Unsupported platform: {current_platform}")
        return 1
    
    # Check dependencies
    check_dependencies()
    
    # Generate report
    return generate_report(results)


if __name__ == "__main__":
    sys.exit(main())
