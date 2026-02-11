"""Verification script for project setup"""

import sys
from pathlib import Path

def verify_structure():
    """Verify project directory structure"""
    print("Verifying project structure...")
    
    required_dirs = [
        "src",
        "src/audio",
        "src/transcription",
        "src/ui",
        "src/config",
        "src/export",
        "tests",
        "tests/test_audio",
        "tests/test_transcription",
        "tests/test_ui",
        "tests/test_config",
        "tests/test_export",
    ]
    
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists() and path.is_dir():
            print(f"  ✓ {dir_path}")
        else:
            print(f"  ✗ {dir_path} - MISSING")
            return False
    
    return True

def verify_files():
    """Verify required files exist"""
    print("\nVerifying required files...")
    
    required_files = [
        "requirements.txt",
        "pytest.ini",
        "setup.py",
        "src/__init__.py",
        "src/config/config_manager.py",
        "tests/conftest.py",
        "tests/test_config/test_config_manager.py",
    ]
    
    for file_path in required_files:
        path = Path(file_path)
        if path.exists() and path.is_file():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} - MISSING")
            return False
    
    return True

def verify_imports():
    """Verify key imports work"""
    print("\nVerifying imports...")
    
    sys.path.insert(0, 'src')
    
    try:
        from config import ConfigManager, Config
        print("  ✓ config module imports")
    except ImportError as e:
        print(f"  ✗ config module import failed: {e}")
        return False
    
    try:
        import pytest
        print("  ✓ pytest installed")
    except ImportError:
        print("  ✗ pytest not installed")
        return False
    
    try:
        import hypothesis
        print("  ✓ hypothesis installed")
    except ImportError:
        print("  ✗ hypothesis not installed")
        return False
    
    return True

def verify_config():
    """Verify configuration system works"""
    print("\nVerifying configuration system...")
    
    sys.path.insert(0, 'src')
    from config import ConfigManager
    
    try:
        cm = ConfigManager()
        config = cm.get_default()
        
        assert config.audio.sample_rate == 16000
        assert config.transcription.model_name == "tiny"
        assert config.overlay.position == "bottom"
        
        print("  ✓ Configuration system working")
        return True
    except Exception as e:
        print(f"  ✗ Configuration system failed: {e}")
        return False

def main():
    """Run all verification checks"""
    print("=" * 60)
    print("OpenLiveCaption Project Setup Verification")
    print("=" * 60)
    
    checks = [
        verify_structure(),
        verify_files(),
        verify_imports(),
        verify_config(),
    ]
    
    print("\n" + "=" * 60)
    if all(checks):
        print("✅ All verification checks passed!")
        print("=" * 60)
        print("\nProject setup complete. Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run tests: pytest")
        print("3. Follow tasks in .kiro/specs/system-wide-live-captions/tasks.md")
        return 0
    else:
        print("❌ Some verification checks failed!")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
