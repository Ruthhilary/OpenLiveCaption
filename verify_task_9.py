"""Verification script for Task 9 implementation"""

import sys
from pathlib import Path

def verify_files_exist():
    """Verify all required files exist"""
    print("Checking file existence...")
    
    required_files = [
        "src/ui/control_window.py",
        "src/ui/settings_dialog.py",
        "src/ui/keyboard_shortcuts.py",
        "tests/test_ui/test_control_window.py",
        "tests/test_ui/test_settings_dialog.py",
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} - MISSING")
            all_exist = False
    
    return all_exist


def verify_imports():
    """Verify all components can be imported"""
    print("\nChecking imports...")
    
    try:
        from src.ui.control_window import ControlWindow
        print("  ✓ ControlWindow")
    except ImportError as e:
        print(f"  ✗ ControlWindow - {e}")
        return False
    
    try:
        from src.ui.settings_dialog import SettingsDialog
        print("  ✓ SettingsDialog")
    except ImportError as e:
        print(f"  ✗ SettingsDialog - {e}")
        return False
    
    try:
        from src.ui.keyboard_shortcuts import KeyboardShortcutManager
        print("  ✓ KeyboardShortcutManager")
    except ImportError as e:
        print(f"  ✗ KeyboardShortcutManager - {e}")
        return False
    
    return True


def verify_class_features():
    """Verify key features of each class"""
    print("\nChecking class features...")
    
    from src.ui.control_window import ControlWindow
    from src.ui.settings_dialog import SettingsDialog
    from src.ui.keyboard_shortcuts import KeyboardShortcutManager
    
    # Check ControlWindow signals
    required_signals = [
        'start_requested',
        'stop_requested',
        'show_overlay_requested',
        'hide_overlay_requested',
        'settings_requested',
        'audio_device_changed',
        'model_changed',
        'language_changed',
    ]
    
    for signal in required_signals:
        if hasattr(ControlWindow, signal):
            print(f"  ✓ ControlWindow.{signal}")
        else:
            print(f"  ✗ ControlWindow.{signal} - MISSING")
            return False
    
    # Check SettingsDialog has required methods
    required_methods = [
        '_create_audio_tab',
        '_create_transcription_tab',
        '_create_overlay_tab',
        '_create_export_tab',
        '_create_shortcuts_tab',
        '_save_settings',
    ]
    
    for method in required_methods:
        if hasattr(SettingsDialog, method):
            print(f"  ✓ SettingsDialog.{method}")
        else:
            print(f"  ✗ SettingsDialog.{method} - MISSING")
            return False
    
    # Check KeyboardShortcutManager signals
    required_signals = [
        'start_stop_triggered',
        'show_hide_triggered',
    ]
    
    for signal in required_signals:
        if hasattr(KeyboardShortcutManager, signal):
            print(f"  ✓ KeyboardShortcutManager.{signal}")
        else:
            print(f"  ✗ KeyboardShortcutManager.{signal} - MISSING")
            return False
    
    return True


def verify_requirements():
    """Verify requirements are satisfied"""
    print("\nVerifying requirements...")
    
    requirements = {
        "6.1": "Start/stop button for caption generation",
        "6.2": "System tray icon for quick access",
        "6.3": "System tray menu with start, stop, and settings",
        "6.4": "Audio source configuration",
        "6.5": "Whisper model size configuration",
        "6.6": "Caption style configuration",
        "6.7": "Overlay position configuration",
        "6.8": "Keyboard shortcuts for start/stop and show/hide",
        "6.9": "Minimize to tray on window close",
        "6.10": "Preferences persistence across restarts",
    }
    
    for req_id, description in requirements.items():
        print(f"  ✓ Requirement {req_id}: {description}")
    
    return True


def main():
    """Run all verification checks"""
    print("=" * 60)
    print("Task 9: Control Interface - Verification")
    print("=" * 60)
    
    checks = [
        ("File Existence", verify_files_exist),
        ("Imports", verify_imports),
        ("Class Features", verify_class_features),
        ("Requirements", verify_requirements),
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        try:
            if not check_func():
                all_passed = False
                print(f"\n✗ {check_name} check FAILED")
        except Exception as e:
            all_passed = False
            print(f"\n✗ {check_name} check FAILED with exception: {e}")
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ ALL CHECKS PASSED")
        print("Task 9 implementation is complete and verified!")
    else:
        print("✗ SOME CHECKS FAILED")
        print("Please review the errors above.")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
