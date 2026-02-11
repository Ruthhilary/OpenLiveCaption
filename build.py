#!/usr/bin/env python3
"""
Build script for OpenLiveCaption
Automates building executables for Windows, macOS, and Linux
"""

import os
import sys
import shutil
import subprocess
import platform
import argparse
from pathlib import Path


class BuildConfig:
    """Build configuration for different platforms"""
    
    def __init__(self):
        self.platform = platform.system().lower()
        self.project_root = Path(__file__).parent
        self.dist_dir = self.project_root / "dist"
        self.build_dir = self.project_root / "build"
        self.spec_file = self.project_root / "openlivecaption.spec"
        
    def get_platform_name(self):
        """Get platform-specific name"""
        if self.platform == "windows":
            return "windows"
        elif self.platform == "darwin":
            return "macos"
        elif self.platform == "linux":
            return "linux"
        else:
            return "unknown"


def clean_build_artifacts(config):
    """Remove previous build artifacts"""
    print("🧹 Cleaning build artifacts...")
    
    if config.dist_dir.exists():
        shutil.rmtree(config.dist_dir)
        print(f"  ✓ Removed {config.dist_dir}")
    
    if config.build_dir.exists():
        shutil.rmtree(config.build_dir)
        print(f"  ✓ Removed {config.build_dir}")
    
    # Remove spec file cache
    spec_cache = config.project_root / "__pycache__"
    if spec_cache.exists():
        shutil.rmtree(spec_cache)
        print(f"  ✓ Removed {spec_cache}")


def check_dependencies(config):
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        "PyInstaller",
        "PyQt6",
        "whisper",
        "torch",
        "transformers",
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
        print(f"\n❌ Missing dependencies: {', '.join(missing)}")
        print("   Install with: pip install -r requirements.txt")
        return False
    
    return True


def create_assets_directory(config):
    """Create assets directory with placeholder icons if needed"""
    print("📦 Preparing assets...")
    
    assets_dir = config.project_root / "assets"
    assets_dir.mkdir(exist_ok=True)
    
    # Check for icon files
    icon_files = {
        "windows": assets_dir / "icon.ico",
        "macos": assets_dir / "icon.icns",
        "linux": assets_dir / "icon.png",
    }
    
    platform_icon = icon_files.get(config.get_platform_name())
    if platform_icon and not platform_icon.exists():
        print(f"  ⚠ Warning: {platform_icon.name} not found")
        print(f"    Build will continue without custom icon")
    else:
        print(f"  ✓ Icon file ready")


def build_executable(config, optimize=True):
    """Build executable using PyInstaller"""
    print(f"🔨 Building executable for {config.get_platform_name()}...")
    
    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        str(config.spec_file),
        "--clean",
        "--noconfirm",
    ]
    
    if optimize:
        print("  ℹ Size optimization enabled (UPX compression, CUDA excluded)")
    
    try:
        result = subprocess.run(
            cmd,
            cwd=config.project_root,
            check=True,
            capture_output=True,
            text=True
        )
        print("  ✓ Build completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Build failed")
        print(f"\nError output:\n{e.stderr}")
        return False


def get_executable_size(config):
    """Get size of built executable"""
    if config.platform == "darwin":
        # macOS app bundle
        app_path = config.dist_dir / "OpenLiveCaption.app"
        if app_path.exists():
            size = sum(f.stat().st_size for f in app_path.rglob('*') if f.is_file())
            return size
    else:
        # Windows/Linux executable
        exe_name = "OpenLiveCaption.exe" if config.platform == "windows" else "OpenLiveCaption"
        exe_path = config.dist_dir / exe_name
        if exe_path.exists():
            return exe_path.stat().st_size
    
    return 0


def format_size(size_bytes):
    """Format size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def create_platform_package(config):
    """Create platform-specific package"""
    print(f"📦 Creating {config.get_platform_name()} package...")
    
    if config.platform == "windows":
        # Windows: Executable is ready in dist/
        exe_path = config.dist_dir / "OpenLiveCaption.exe"
        if exe_path.exists():
            print(f"  ✓ Executable: {exe_path}")
            print(f"  ℹ Run installer script to create Windows installer")
            return True
    
    elif config.platform == "darwin":
        # macOS: App bundle is ready in dist/
        app_path = config.dist_dir / "OpenLiveCaption.app"
        if app_path.exists():
            print(f"  ✓ App bundle: {app_path}")
            print(f"  ℹ Run DMG creation script to create macOS installer")
            return True
    
    elif config.platform == "linux":
        # Linux: Executable is ready in dist/
        exe_path = config.dist_dir / "OpenLiveCaption"
        if exe_path.exists():
            print(f"  ✓ Executable: {exe_path}")
            print(f"  ℹ Run AppImage builder to create Linux package")
            return True
    
    print(f"  ✗ Package creation failed")
    return False


def sign_executable(config):
    """Sign executable with code signing certificate"""
    if config.platform == "windows":
        print("🔐 Signing Windows executable...")
        
        exe_path = config.dist_dir / "OpenLiveCaption.exe"
        if not exe_path.exists():
            print(f"  ✗ Executable not found: {exe_path}")
            return False
        
        sign_script = config.project_root / "sign_windows.bat"
        if not sign_script.exists():
            print(f"  ✗ Signing script not found: {sign_script}")
            return False
        
        try:
            result = subprocess.run(
                [str(sign_script), str(exe_path)],
                cwd=config.project_root,
                check=True,
                capture_output=True,
                text=True
            )
            print("  ✓ Executable signed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"  ✗ Signing failed")
            print(f"\nError output:\n{e.stderr}")
            print(f"\nPlease check docs/CODE_SIGNING_WINDOWS.md for setup instructions")
            return False
    
    elif config.platform == "darwin":
        print("🔐 Signing macOS app bundle...")
        
        app_path = config.dist_dir / "OpenLiveCaption.app"
        if not app_path.exists():
            print(f"  ✗ App bundle not found: {app_path}")
            return False
        
        sign_script = config.project_root / "sign_macos.sh"
        if not sign_script.exists():
            print(f"  ✗ Signing script not found: {sign_script}")
            return False
        
        try:
            result = subprocess.run(
                ["bash", str(sign_script), str(app_path)],
                cwd=config.project_root,
                check=True,
                capture_output=True,
                text=True
            )
            print("  ✓ App bundle signed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"  ✗ Signing failed")
            print(f"\nError output:\n{e.stderr}")
            print(f"\nPlease check docs/CODE_SIGNING_MACOS.md for setup instructions")
            return False
    
    else:
        print(f"  ℹ Code signing not implemented for {config.platform}")
        return True


def main():
    """Main build process"""
    parser = argparse.ArgumentParser(description="Build OpenLiveCaption executable")
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean build artifacts before building"
    )
    parser.add_argument(
        "--no-optimize",
        action="store_true",
        help="Disable size optimization (include CUDA, no UPX)"
    )
    parser.add_argument(
        "--skip-checks",
        action="store_true",
        help="Skip dependency checks"
    )
    parser.add_argument(
        "--sign",
        action="store_true",
        help="Sign executable with code signing certificate (Windows only)"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("OpenLiveCaption Build Script")
    print("=" * 60)
    print()
    
    config = BuildConfig()
    
    # Clean if requested
    if args.clean:
        clean_build_artifacts(config)
        print()
    
    # Check dependencies
    if not args.skip_checks:
        if not check_dependencies(config):
            return 1
        print()
    
    # Prepare assets
    create_assets_directory(config)
    print()
    
    # Build executable
    if not build_executable(config, optimize=not args.no_optimize):
        return 1
    print()
    
    # Get executable size
    size = get_executable_size(config)
    if size > 0:
        print(f"📊 Executable size: {format_size(size)}")
        
        # Check if under 500MB requirement
        size_mb = size / (1024 * 1024)
        if size_mb > 500:
            print(f"  ⚠ Warning: Size exceeds 500MB requirement ({size_mb:.2f} MB)")
        else:
            print(f"  ✓ Size within 500MB requirement ({size_mb:.2f} MB)")
        print()
    
    # Sign executable if requested
    if args.sign:
        if not sign_executable(config):
            print("⚠️  Warning: Signing failed, but build completed")
            if config.platform == "windows":
                print("   See docs/CODE_SIGNING_WINDOWS.md for setup instructions")
            elif config.platform == "darwin":
                print("   See docs/CODE_SIGNING_MACOS.md for setup instructions")
        print()
    
    # Create platform package
    if not create_platform_package(config):
        return 1
    print()
    
    print("=" * 60)
    print("✅ Build completed successfully!")
    print("=" * 60)
    print()
    print(f"Output directory: {config.dist_dir}")
    
    if args.sign:
        if config.platform == "windows":
            print()
            print("Note: Executable has been signed")
            print("      To sign the installer, run:")
            print("      sign_windows.bat dist\\installer\\OpenLiveCaption-2.0.0-Windows-Setup.exe")
        elif config.platform == "darwin":
            print()
            print("Note: App bundle has been signed")
            print("      Next steps:")
            print("      1. Notarize: ./notarize_macos.sh dist/OpenLiveCaption.app")
            print("      2. Create DMG: ./create_dmg_macos.sh")
            print("      3. Sign DMG: ./sign_macos.sh dist/installer/OpenLiveCaption-2.0.0-macOS.dmg")
    
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
