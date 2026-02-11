# Control Interface Implementation

This document describes the implementation of the Control Interface for OpenLiveCaption (Task 9).

## Overview

The Control Interface provides a user-friendly GUI for managing the caption system, including:
- Main control window with start/stop functionality
- System tray integration for background operation
- Comprehensive settings dialog
- Global keyboard shortcuts

## Components

### 1. ControlWindow (`src/ui/control_window.py`)

The main control window provides:

**Features:**
- Start/Stop buttons for caption control
- Audio source selection dropdown
- Model size selection (tiny, base, small, medium, large)
- Language selection (auto-detect or manual)
- Settings button to open configuration dialog
- Show/Hide overlay toggle button
- Status indicator (Running/Stopped)

**Signals:**
- `start_requested` - Emitted when start button is clicked
- `stop_requested` - Emitted when stop button is clicked
- `show_overlay_requested` - Emitted when overlay should be shown
- `hide_overlay_requested` - Emitted when overlay should be hidden
- `settings_requested` - Emitted when settings are changed
- `audio_device_changed(int)` - Emitted when audio device is changed
- `model_changed(str)` - Emitted when model size is changed
- `language_changed(str)` - Emitted when language is changed

**Usage:**
```python
from src.ui.control_window import ControlWindow
from src.config.config_manager import Config, ConfigManager

config_manager = ConfigManager()
config = config_manager.load()

window = ControlWindow(config, config_manager)
window.show()

# Connect signals
window.start_requested.connect(on_start)
window.stop_requested.connect(on_stop)
```

### 2. System Tray Integration

The control window includes system tray functionality:

**Features:**
- Tray icon with status indicator (green when running, gray when stopped)
- Right-click context menu with:
  - Start/Stop Captions
  - Show/Hide Overlay
  - Show Window
  - Settings
  - Exit
- Minimize to tray on window close
- Double-click tray icon to restore window
- Notification when minimized to tray

**Behavior:**
- Closing the window minimizes to tray instead of exiting
- Use "Exit" from tray menu to actually quit the application

### 3. SettingsDialog (`src/ui/settings_dialog.py`)

Comprehensive settings dialog with 5 tabs:

#### Audio Tab
- Sample Rate (Hz)
- Chunk Duration (seconds)
- VAD Threshold (voice activity detection)

#### Transcription Tab
- Model Size (tiny, base, small, medium, large)
- Device (cpu, cuda)
- Enable Translation checkbox
- Target Language selection

#### Overlay Tab
- **Position Group:**
  - Position preset (top, bottom, custom)
  - Custom X/Y coordinates
- **Appearance Group:**
  - Font Family
  - Font Size
  - Text Color (with color picker)
  - Background Color (with color picker)
  - Background Opacity
- **Behavior Group:**
  - Max Lines
  - Scroll Mode (replace, scroll)
  - Clear Timeout

#### Export Tab
- Enable Subtitle Export checkbox
- Format (srt, vtt)
- Output Path (with file browser)

#### Shortcuts Tab
- Start/Stop shortcut
- Show/Hide Overlay shortcut

**Usage:**
```python
from src.ui.settings_dialog import SettingsDialog

dialog = SettingsDialog(config, config_manager, parent_window)
if dialog.exec() == QDialog.DialogCode.Accepted:
    # Settings were saved
    print("Settings updated")
```

### 4. KeyboardShortcutManager (`src/ui/keyboard_shortcuts.py`)

Manages global keyboard shortcuts that work even when the application is not in focus.

**Features:**
- Cross-platform global hotkey support
- Configurable shortcuts
- Start/Stop shortcut (default: Ctrl+Shift+S)
- Show/Hide overlay shortcut (default: Ctrl+Shift+H)

**Signals:**
- `start_stop_triggered` - Emitted when start/stop shortcut is pressed
- `show_hide_triggered` - Emitted when show/hide shortcut is pressed

**Requirements:**
- Requires `keyboard` library for global hotkey support
- If library is not installed, shortcuts are disabled gracefully

**Usage:**
```python
from src.ui.keyboard_shortcuts import KeyboardShortcutManager

manager = KeyboardShortcutManager()
manager.start_stop_triggered.connect(on_start_stop)
manager.show_hide_triggered.connect(on_show_hide)

manager.setup_default_shortcuts("Ctrl+Shift+S", "Ctrl+Shift+H")
```

## Installation

### Required Dependencies

```bash
pip install PyQt6
```

### Optional Dependencies

For global keyboard shortcuts:
```bash
pip install keyboard
```

**Note:** The `keyboard` library requires administrator/root privileges on some platforms. If not installed, the application will work without global shortcuts.

## Testing

All components have comprehensive unit tests:

```bash
# Run all UI tests
python -m pytest tests/test_ui/ -v

# Run specific test files
python -m pytest tests/test_ui/test_control_window.py -v
python -m pytest tests/test_ui/test_settings_dialog.py -v
```

**Test Coverage:**
- ControlWindow: 11 tests
- SettingsDialog: 11 tests
- CaptionOverlay: 23 tests (from previous tasks)

Total: 45 UI tests, all passing

## Demo

Run the demo script to see the control window in action:

```bash
python demo_control_window.py
```

The demo shows:
- Control window with all UI elements
- Audio device population
- Signal connections
- System tray integration
- Settings dialog access

## Architecture

```
┌─────────────────────────────────────┐
│       ControlWindow                 │
│  ┌───────────────────────────────┐  │
│  │  Start/Stop Buttons           │  │
│  │  Audio Device Dropdown        │  │
│  │  Model Size Dropdown          │  │
│  │  Language Dropdown            │  │
│  │  Settings Button              │  │
│  │  Show/Hide Overlay Button     │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  System Tray Icon             │  │
│  │  - Context Menu               │  │
│  │  - Status Indicator           │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  KeyboardShortcutManager      │  │
│  │  - Global Hotkeys             │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
            │
            │ Opens
            ▼
┌─────────────────────────────────────┐
│       SettingsDialog                │
│  ┌───────────────────────────────┐  │
│  │  Tab 1: Audio Settings        │  │
│  │  Tab 2: Transcription         │  │
│  │  Tab 3: Overlay               │  │
│  │  Tab 4: Export                │  │
│  │  Tab 5: Shortcuts             │  │
│  └───────────────────────────────┘  │
│                                     │
│  [Cancel] [Apply] [OK]              │
└─────────────────────────────────────┘
```

## Integration with Other Components

The Control Interface integrates with:

1. **ConfigManager** - Loads and saves all settings
2. **AudioCaptureEngine** - Lists available audio devices
3. **CaptionOverlay** - Controls overlay visibility
4. **TranscriptionEngine** - Changes model size and language
5. **TranslationEngine** - Enables/disables translation

## Requirements Validation

This implementation satisfies the following requirements:

### Requirement 6.1: Control Interface
✅ Provides start/stop button for caption generation

### Requirement 6.2: System Tray Icon
✅ Provides system tray icon for quick access

### Requirement 6.3: System Tray Menu
✅ Displays menu with start, stop, and settings options on tray icon click

### Requirement 6.4: Audio Source Configuration
✅ Allows configuration of audio source

### Requirement 6.5: Model Size Configuration
✅ Allows configuration of Whisper model size

### Requirement 6.6: Caption Style Configuration
✅ Allows configuration of caption style properties

### Requirement 6.7: Overlay Position Configuration
✅ Allows configuration of overlay position

### Requirement 6.8: Keyboard Shortcuts
✅ Provides keyboard shortcuts for start/stop and show/hide overlay

### Requirement 6.9: Minimize to Tray
✅ Minimizes to system tray rather than exit when main window is closed

### Requirement 6.10: Preferences Persistence
✅ Persists all user preferences across application restarts

## Future Enhancements

Potential improvements for future versions:

1. **Preset Management** - Save and load configuration presets
2. **Device Monitoring** - Auto-detect when audio devices are added/removed
3. **Quick Actions** - Add quick action buttons for common tasks
4. **Themes** - Support for light/dark themes
5. **Compact Mode** - Minimal UI mode for smaller screen footprint
6. **Multi-Language UI** - Localization support for the interface
7. **Tooltips** - Add helpful tooltips to all controls
8. **Keyboard Navigation** - Full keyboard navigation support
9. **Accessibility** - Enhanced screen reader support
10. **Custom Icons** - Professional icon set for tray and window

## Troubleshooting

### Global Shortcuts Not Working

If keyboard shortcuts don't work:
1. Install the `keyboard` library: `pip install keyboard`
2. On Linux, you may need to run with sudo for global hotkeys
3. On macOS, grant accessibility permissions in System Preferences
4. On Windows, run as administrator if needed

### System Tray Icon Not Showing

If the tray icon doesn't appear:
1. Check if your desktop environment supports system tray
2. On Linux, ensure you have a system tray applet running
3. Try restarting the application

### Settings Not Saving

If settings don't persist:
1. Check file permissions for the config directory
2. Verify the config path is writable
3. Check logs for any error messages

## License

This implementation is part of the OpenLiveCaption project.
