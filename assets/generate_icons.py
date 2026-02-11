#!/usr/bin/env python3
"""
generate_icons.py
Script to generate platform-specific icons from SVG sources
Requires: Pillow, cairosvg
"""

import os
import sys
from pathlib import Path

try:
    from PIL import Image
    from cairosvg import svg2png
except ImportError as e:
    print("ERROR: Required packages not installed")
    print("Please install: pip install Pillow cairosvg")
    print(f"Missing: {e.name}")
    sys.exit(1)


def print_header():
    """Print script header"""
    print("=" * 50)
    print("OpenLiveCaption Icon Generation")
    print("=" * 50)
    print()


def check_svg_files(assets_dir):
    """Check if all required SVG files exist"""
    print("Checking for SVG source files...")
    
    required_files = [
        "icon.svg",
        "tray_icon_active.svg",
        "tray_icon_inactive.svg"
    ]
    
    missing = []
    for filename in required_files:
        filepath = assets_dir / filename
        if not filepath.exists():
            missing.append(filename)
        else:
            print(f"  ✓ {filename}")
    
    if missing:
        print("\nERROR: Missing SVG files:")
        for filename in missing:
            print(f"  ✗ {filename}")
        return False
    
    print()
    return True


def generate_png_from_svg(svg_path, png_path, width, height):
    """Generate PNG from SVG using cairosvg"""
    try:
        svg2png(
            url=str(svg_path),
            write_to=str(png_path),
            output_width=width,
            output_height=height
        )
        return True
    except Exception as e:
        print(f"  ERROR: Failed to convert {svg_path.name}: {e}")
        return False


def generate_pngs(assets_dir):
    """Generate PNG files from SVG sources"""
    print("Step 1: Converting SVG to PNG...")
    
    conversions = [
        ("icon.svg", "icon.png", 512, 512),
        ("tray_icon_active.svg", "tray_active.png", 64, 64),
        ("tray_icon_inactive.svg", "tray_inactive.png", 64, 64),
    ]
    
    success = True
    for svg_name, png_name, width, height in conversions:
        svg_path = assets_dir / svg_name
        png_path = assets_dir / png_name
        print(f"  - Generating {png_name} ({width}x{height})...")
        if not generate_png_from_svg(svg_path, png_path, width, height):
            success = False
    
    if success:
        print("✓ PNG files generated")
    print()
    return success


def generate_ico(assets_dir):
    """Generate Windows ICO file with multiple resolutions"""
    print("Step 2: Generating Windows ICO...")
    
    try:
        icon_png = assets_dir / "icon.png"
        icon_ico = assets_dir / "icon.ico"
        
        if not icon_png.exists():
            print("  ERROR: icon.png not found")
            return False
        
        print("  - Loading source image...")
        img = Image.open(icon_png)
        
        # Ensure RGBA mode
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        print("  - Creating multiple resolutions...")
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        
        print("  - Saving as ICO...")
        img.save(icon_ico, format='ICO', sizes=sizes)
        
        print("✓ Windows ICO generated")
        print()
        return True
        
    except Exception as e:
        print(f"  ERROR: Failed to generate ICO: {e}")
        print()
        return False


def generate_icns_macos(assets_dir):
    """Generate macOS ICNS file (macOS only)"""
    print("Step 3: Generating macOS ICNS...")
    
    if sys.platform != 'darwin':
        print("  Skipping (not on macOS)")
        print()
        return True
    
    try:
        import subprocess
        
        icon_png = assets_dir / "icon.png"
        iconset_dir = assets_dir / "icon.iconset"
        icon_icns = assets_dir / "icon.icns"
        
        if not icon_png.exists():
            print("  ERROR: icon.png not found")
            return False
        
        # Create iconset directory
        print("  - Creating iconset directory...")
        iconset_dir.mkdir(exist_ok=True)
        
        # Generate required sizes using sips
        print("  - Generating required sizes...")
        sizes = [
            (16, "icon_16x16.png"),
            (32, "icon_16x16@2x.png"),
            (32, "icon_32x32.png"),
            (64, "icon_32x32@2x.png"),
            (128, "icon_128x128.png"),
            (256, "icon_128x128@2x.png"),
            (256, "icon_256x256.png"),
            (512, "icon_256x256@2x.png"),
            (512, "icon_512x512.png"),
            (1024, "icon_512x512@2x.png"),
        ]
        
        for size, filename in sizes:
            output_path = iconset_dir / filename
            subprocess.run(
                ["sips", "-z", str(size), str(size), str(icon_png), "--out", str(output_path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
        
        # Convert to ICNS
        print("  - Converting to ICNS...")
        subprocess.run(
            ["iconutil", "-c", "icns", str(iconset_dir)],
            check=True
        )
        
        # Clean up iconset directory
        print("  - Cleaning up...")
        import shutil
        shutil.rmtree(iconset_dir)
        
        print("✓ macOS ICNS generated")
        print()
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"  ERROR: Command failed: {e}")
        print()
        return False
    except Exception as e:
        print(f"  ERROR: Failed to generate ICNS: {e}")
        print()
        return False


def print_summary(assets_dir):
    """Print summary of generated files"""
    print("=" * 50)
    print("Icon Generation Complete!")
    print("=" * 50)
    print()
    print("Generated files:")
    
    files = [
        ("icon.png", "Linux/General (512x512)"),
        ("icon.ico", "Windows"),
        ("icon.icns", "macOS"),
        ("tray_active.png", "System tray active (64x64)"),
        ("tray_inactive.png", "System tray inactive (64x64)"),
    ]
    
    for filename, description in files:
        filepath = assets_dir / filename
        if filepath.exists():
            print(f"  ✓ {filename} - {description}")
        else:
            print(f"  ✗ {filename} - {description} (not generated)")
    
    print()
    print("These files are ready to use in the application!")
    print()


def main():
    """Main function"""
    print_header()
    
    # Get assets directory
    assets_dir = Path(__file__).parent
    os.chdir(assets_dir)
    
    # Check for SVG files
    if not check_svg_files(assets_dir):
        sys.exit(1)
    
    # Generate PNGs
    if not generate_pngs(assets_dir):
        print("WARNING: Some PNG files failed to generate")
    
    # Generate ICO
    if not generate_ico(assets_dir):
        print("WARNING: Windows ICO failed to generate")
    
    # Generate ICNS (macOS only)
    if not generate_icns_macos(assets_dir):
        print("WARNING: macOS ICNS failed to generate")
    
    # Print summary
    print_summary(assets_dir)


if __name__ == "__main__":
    main()
