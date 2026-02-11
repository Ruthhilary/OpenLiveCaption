#!/usr/bin/env python3
"""
Verify package configuration without building
Checks that all build scripts and configurations are properly set up
"""

import os
import sys
from pathlib import Path
import json


class ConfigVerification:
    """Verification result for a configuration"""
    
    def __init__(self, name):
        self.name = name
        self.exists = False
        self.valid = False
        self.errors = []
        self.warnings = []
    
    def to_dict(self):
        return {
            'name': self.name,
            'exists': self.exists,
            'valid': self.valid,
            'errors': self.errors,
            'warnings': self.warnings,
            'passed': self.exists and self.valid and len(self.errors) == 0
        }


def verify_pyinstaller_spec():
    """Verify PyInstaller spec file"""
    print("Verifying PyInstaller spec file...")
    result = ConfigVerification("PyInstaller Spec")
    
    spec_path = Path("openlivecaption.spec")
    if not spec_path.exists():
        result.errors.append("openlivecaption.spec not found")
        print("  ❌ Spec file not found")
        return result
    
    result.exists = True
    
    # Read and check spec file content
    content = spec_path.read_text(encoding='utf-8')
    
    # Check for required sections
    required_sections = [
        "Analysis",
        "PYZ",
        "EXE",
        "hiddenimports",
        "datas",
    ]
    
    for section in required_sections:
        if section in content:
            print(f"  ✓ {section} section found")
        else:
            result.errors.append(f"Missing {section} section")
            print(f"  ❌ {section} section missing")
    
    # Check for size optimization
    if "upx=True" in content:
        print("  ✓ UPX compression enabled")
    else:
        result.warnings.append("UPX compression not enabled")
        print("  ⚠ UPX compression not enabled")
    
    # Check for CUDA exclusion
    if "torch.cuda" in content or "excludes" in content:
        print("  ✓ CUDA exclusion configured")
    else:
        result.warnings.append("CUDA libraries may not be excluded")
        print("  ⚠ CUDA exclusion not found")
    
    # Check for console=False (GUI app)
    if "console=False" in content:
        print("  ✓ GUI mode configured (no console)")
    else:
        result.warnings.append("Console mode may be enabled")
        print("  ⚠ Console mode may be enabled")
    
    result.valid = len(result.errors) == 0
    print()
    return result


def verify_build_script():
    """Verify build.py script"""
    print("Verifying build script...")
    result = ConfigVerification("Build Script")
    
    build_path = Path("build.py")
    if not build_path.exists():
        result.errors.append("build.py not found")
        print("  ❌ Build script not found")
        return result
    
    result.exists = True
    
    # Read and check build script
    content = build_path.read_text(encoding='utf-8')
    
    # Check for required functions
    required_functions = [
        "clean_build_artifacts",
        "check_dependencies",
        "build_executable",
        "get_executable_size",
        "create_platform_package",
    ]
    
    for func in required_functions:
        if f"def {func}" in content:
            print(f"  ✓ {func}() found")
        else:
            result.errors.append(f"Missing {func}() function")
            print(f"  ❌ {func}() missing")
    
    # Check for size verification
    if "500" in content and "MB" in content:
        print("  ✓ 500MB size check implemented")
    else:
        result.warnings.append("500MB size check not found")
        print("  ⚠ 500MB size check not found")
    
    result.valid = len(result.errors) == 0
    print()
    return result


def verify_windows_installer():
    """Verify Windows installer configuration"""
    print("Verifying Windows installer configuration...")
    result = ConfigVerification("Windows Installer")
    
    iss_path = Path("installer_windows.iss")
    if not iss_path.exists():
        result.errors.append("installer_windows.iss not found")
        print("  ❌ Inno Setup script not found")
        return result
    
    result.exists = True
    
    # Read and check installer script
    content = iss_path.read_text(encoding='utf-8')
    
    # Check for required sections
    required_sections = [
        "[Setup]",
        "[Files]",
        "[Icons]",
        "[Run]",
        "[UninstallDelete]",
    ]
    
    for section in required_sections:
        if section in content:
            print(f"  ✓ {section} section found")
        else:
            result.errors.append(f"Missing {section} section")
            print(f"  ❌ {section} section missing")
    
    # Check for app name and version
    if "MyAppName" in content and "MyAppVersion" in content:
        print("  ✓ App name and version configured")
    else:
        result.warnings.append("App name/version not configured")
        print("  ⚠ App name/version not configured")
    
    # Check for uninstaller
    if "UninstallDelete" in content:
        print("  ✓ Uninstaller configured")
    else:
        result.warnings.append("Uninstaller not configured")
        print("  ⚠ Uninstaller not configured")
    
    result.valid = len(result.errors) == 0
    print()
    return result


def verify_macos_dmg():
    """Verify macOS DMG creation script"""
    print("Verifying macOS DMG script...")
    result = ConfigVerification("macOS DMG")
    
    dmg_path = Path("create_dmg_macos.sh")
    if not dmg_path.exists():
        result.errors.append("create_dmg_macos.sh not found")
        print("  ❌ DMG creation script not found")
        return result
    
    result.exists = True
    
    # Read and check DMG script
    content = dmg_path.read_text(encoding='utf-8')
    
    # Check for required commands
    required_commands = [
        "hdiutil create",
        "hdiutil attach",
        "hdiutil detach",
        "hdiutil convert",
    ]
    
    for cmd in required_commands:
        if cmd in content:
            print(f"  ✓ {cmd} found")
        else:
            result.errors.append(f"Missing {cmd} command")
            print(f"  ❌ {cmd} missing")
    
    # Check for Applications symlink
    if "ln -s /Applications" in content:
        print("  ✓ Applications symlink creation found")
    else:
        result.warnings.append("Applications symlink not created")
        print("  ⚠ Applications symlink not found")
    
    # Check for compression
    if "UDZO" in content or "zlib" in content:
        print("  ✓ DMG compression configured")
    else:
        result.warnings.append("DMG compression not configured")
        print("  ⚠ DMG compression not configured")
    
    result.valid = len(result.errors) == 0
    print()
    return result


def verify_linux_appimage():
    """Verify Linux AppImage configuration"""
    print("Verifying Linux AppImage configuration...")
    result = ConfigVerification("Linux AppImage")
    
    # Check for shell script
    script_path = Path("create_appimage_linux.sh")
    if not script_path.exists():
        result.errors.append("create_appimage_linux.sh not found")
        print("  ❌ AppImage creation script not found")
        return result
    
    result.exists = True
    
    # Check for AppImageBuilder.yml
    yml_path = Path("AppImageBuilder.yml")
    if yml_path.exists():
        print("  ✓ AppImageBuilder.yml found")
        
        # Read and check YAML content
        content = yml_path.read_text(encoding='utf-8')
        
        # Check for required sections
        if "AppDir:" in content:
            print("  ✓ AppDir configuration found")
        else:
            result.errors.append("AppDir configuration missing")
            print("  ❌ AppDir configuration missing")
        
        if "app_info:" in content:
            print("  ✓ App info configured")
        else:
            result.errors.append("App info missing")
            print("  ❌ App info missing")
        
        if "apt:" in content:
            print("  ✓ APT dependencies configured")
        else:
            result.warnings.append("APT dependencies not configured")
            print("  ⚠ APT dependencies not configured")
        
    else:
        result.errors.append("AppImageBuilder.yml not found")
        print("  ❌ AppImageBuilder.yml not found")
    
    # Check shell script content
    script_content = script_path.read_text(encoding='utf-8')
    
    if "appimage-builder" in script_content:
        print("  ✓ appimage-builder command found")
    else:
        result.errors.append("appimage-builder command missing")
        print("  ❌ appimage-builder command missing")
    
    if "AppRun" in script_content:
        print("  ✓ AppRun script creation found")
    else:
        result.warnings.append("AppRun script not created")
        print("  ⚠ AppRun script not created")
    
    result.valid = len(result.errors) == 0
    print()
    return result


def verify_requirements():
    """Verify requirements.txt"""
    print("Verifying requirements.txt...")
    result = ConfigVerification("Requirements")
    
    req_path = Path("requirements.txt")
    if not req_path.exists():
        result.errors.append("requirements.txt not found")
        print("  ❌ requirements.txt not found")
        return result
    
    result.exists = True
    
    # Read and check requirements
    content = req_path.read_text(encoding='utf-8')
    
    # Check for required packages
    required_packages = [
        "PyQt6",
        "openai-whisper",
        "torch",
        "transformers",
        "sounddevice",
        "pyinstaller",
        "pytest",
        "hypothesis",
    ]
    
    for package in required_packages:
        if package.lower() in content.lower():
            print(f"  ✓ {package} found")
        else:
            result.errors.append(f"Missing {package} package")
            print(f"  ❌ {package} missing")
    
    # Check for platform-specific packages
    if "pyaudiowpatch" in content and "sys_platform" in content:
        print("  ✓ Platform-specific packages configured")
    else:
        result.warnings.append("Platform-specific packages not configured")
        print("  ⚠ Platform-specific packages not configured")
    
    result.valid = len(result.errors) == 0
    print()
    return result


def verify_assets():
    """Verify assets directory"""
    print("Verifying assets directory...")
    result = ConfigVerification("Assets")
    
    assets_dir = Path("assets")
    if not assets_dir.exists():
        result.warnings.append("assets directory not found")
        print("  ⚠ assets directory not found (will be created)")
        result.exists = True
        result.valid = True
        print()
        return result
    
    result.exists = True
    
    # Check for icon files
    icon_files = {
        "icon.ico": "Windows",
        "icon.icns": "macOS",
        "icon.png": "Linux",
    }
    
    for icon_file, platform in icon_files.items():
        icon_path = assets_dir / icon_file
        if icon_path.exists():
            print(f"  ✓ {icon_file} found ({platform})")
        else:
            result.warnings.append(f"{icon_file} not found ({platform})")
            print(f"  ⚠ {icon_file} not found ({platform})")
    
    result.valid = True  # Assets are optional
    print()
    return result


def generate_report(results):
    """Generate verification report"""
    print("=" * 60)
    print("Configuration Verification Summary")
    print("=" * 60)
    print()
    
    all_passed = True
    
    for result in results:
        status = "✅ PASSED" if result.to_dict()['passed'] else "❌ FAILED"
        print(f"{result.name}: {status}")
        
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
    report_path = Path("package_config_verification.json")
    with open(report_path, 'w') as f:
        json.dump({
            'results': [r.to_dict() for r in results],
            'all_passed': all_passed
        }, f, indent=2)
    
    print(f"📊 Detailed report saved to: {report_path}")
    print()
    
    if all_passed:
        print("✅ All package configurations are valid!")
        print()
        print("Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Build packages: python build.py --clean")
        print("3. Test packages: python test_packages.py")
        return 0
    else:
        print("❌ Some package configurations have errors")
        print()
        print("Fix the errors above before building packages")
        return 1


def main():
    """Main verification execution"""
    print()
    print("=" * 60)
    print("OpenLiveCaption Package Configuration Verification")
    print("=" * 60)
    print()
    
    results = []
    
    # Verify all configurations
    results.append(verify_requirements())
    results.append(verify_pyinstaller_spec())
    results.append(verify_build_script())
    results.append(verify_windows_installer())
    results.append(verify_macos_dmg())
    results.append(verify_linux_appimage())
    results.append(verify_assets())
    
    # Generate report
    return generate_report(results)


if __name__ == "__main__":
    sys.exit(main())
