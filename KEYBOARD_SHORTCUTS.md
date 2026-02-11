# OpenLiveCaption Keyboard Shortcuts

Complete reference for all keyboard shortcuts in OpenLiveCaption.

## Global Shortcuts

These shortcuts work even when OpenLiveCaption is not in focus (system-wide):

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Ctrl+Shift+S` | Start/Stop Captions | Toggle caption generation on/off |
| `Ctrl+Shift+H` | Show/Hide Overlay | Toggle caption overlay visibility |

**Note**: Global shortcuts require the `keyboard` library. On some Linux distributions with Wayland, global shortcuts may not work due to security restrictions.

## Control Window Shortcuts

These shortcuts work when the Control Window is in focus:

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Alt+S` | Start Captions | Begin caption generation |
| `Alt+T` | Stop Captions | End caption generation |
| `Alt+O` | Show Overlay | Make overlay visible |
| `Alt+H` | Hide Overlay | Hide overlay window |
| `Alt+G` | Settings | Open settings dialog |
| `Ctrl+Q` | Quit | Exit application |
| `Ctrl+M` | Minimize to Tray | Minimize to system tray |

## Settings Dialog Shortcuts

These shortcuts work when the Settings dialog is open:

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Ctrl+Tab` | Next Tab | Switch to next settings tab |
| `Ctrl+Shift+Tab` | Previous Tab | Switch to previous settings tab |
| `Ctrl+S` | Save Settings | Apply and save changes |
| `Esc` | Cancel | Close without saving |
| `Ctrl+R` | Reset to Defaults | Reset all settings to defaults |

## System Tray Shortcuts

When the system tray icon is focused:

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Enter` | Show Menu | Open tray context menu |
| `Double-Click` | Show Window | Show Control Window |

## Customizing Shortcuts

You can customize global shortcuts in the Settings dialog:

1. Click **⚙ Settings** button
2. Go to **Shortcuts** tab
3. Click on the shortcut you want to change
4. Press the new key combination
5. Click **Apply** to save

### Shortcut Format

Shortcuts use the following format:
- **Modifiers**: `Ctrl`, `Shift`, `Alt`, `Meta` (Windows key)
- **Keys**: Any letter, number, or function key
- **Combination**: `Modifier+Modifier+Key`

**Examples**:
- `Ctrl+Shift+S`
- `Alt+F1`
- `Ctrl+Alt+C`
- `Meta+Space`

### Shortcut Restrictions

- Must include at least one modifier key (Ctrl, Shift, Alt, or Meta)
- Cannot use system-reserved shortcuts (e.g., `Ctrl+Alt+Del` on Windows)
- Cannot conflict with other application shortcuts
- Some keys may not work on all platforms

## Platform-Specific Shortcuts

### Windows

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Win+Shift+S` | Start/Stop (Alt) | Alternative if default conflicts with Snipping Tool |
| `Win+Shift+H` | Show/Hide (Alt) | Alternative global shortcut |

### macOS

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Cmd+Shift+S` | Start/Stop | macOS uses Cmd instead of Ctrl |
| `Cmd+Shift+H` | Show/Hide | macOS uses Cmd instead of Ctrl |
| `Cmd+Q` | Quit | Standard macOS quit shortcut |
| `Cmd+M` | Minimize | Standard macOS minimize |
| `Cmd+,` | Settings | Standard macOS settings shortcut |

**Note**: On macOS, `Ctrl` is replaced with `Cmd` (⌘) for most shortcuts.

### Linux

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Super+Shift+S` | Start/Stop (Alt) | Alternative using Super (Windows) key |
| `Super+Shift+H` | Show/Hide (Alt) | Alternative using Super key |

**Note**: On Wayland, global shortcuts may require additional permissions or may not work at all. Use the system tray or Control Window instead.

## Accessibility Shortcuts

For users relying on keyboard navigation:

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Tab` | Next Control | Move to next UI element |
| `Shift+Tab` | Previous Control | Move to previous UI element |
| `Space` | Activate | Activate button or checkbox |
| `Enter` | Confirm | Confirm action or open dropdown |
| `Esc` | Cancel | Close dialog or cancel action |
| `Alt+Letter` | Access Key | Activate control with underlined letter |

## Troubleshooting Shortcuts

### Shortcuts Not Working

**Global shortcuts don't respond**:
1. Check if another application is using the same shortcut
2. On Linux/Wayland: Global shortcuts may not be supported
3. Try customizing to a different key combination
4. Ensure the application has necessary permissions
5. Use Control Window or system tray as alternative

**Control Window shortcuts don't work**:
1. Ensure the Control Window is in focus
2. Check if the shortcut conflicts with system shortcuts
3. Try clicking on the window first, then use shortcut

**Settings dialog shortcuts don't work**:
1. Ensure the Settings dialog is open and in focus
2. Some shortcuts may be disabled while editing fields

### Shortcut Conflicts

If a shortcut conflicts with another application:

1. **Identify the conflict**: Check which application is using the shortcut
2. **Change in OpenLiveCaption**: Go to Settings > Shortcuts and customize
3. **Change in other app**: Modify the conflicting application's shortcut
4. **Use alternative**: Use system tray or Control Window instead

### Platform-Specific Issues

**Windows**:
- Some shortcuts may conflict with Windows system shortcuts
- Try using `Win` key instead of `Ctrl` for global shortcuts
- Check Windows Settings > Keyboard for conflicts

**macOS**:
- Use `Cmd` instead of `Ctrl` for most shortcuts
- Check System Preferences > Keyboard > Shortcuts for conflicts
- Grant accessibility permissions if shortcuts don't work

**Linux**:
- Wayland may block global shortcuts for security
- Check desktop environment keyboard settings
- Use `Super` (Windows key) for global shortcuts
- Some window managers may require additional configuration

## Quick Reference Card

Print this card for easy reference:

```
┌──────────────────────────────────────────────────────┐
│  OpenLiveCaption Keyboard Shortcuts                  │
├──────────────────────────────────────────────────────┤
│  GLOBAL SHORTCUTS (work anywhere)                    │
│    Ctrl+Shift+S    Start/Stop captions               │
│    Ctrl+Shift+H    Show/Hide overlay                 │
│                                                      │
│  CONTROL WINDOW (when window is focused)             │
│    Alt+S           Start captions                    │
│    Alt+T           Stop captions                     │
│    Alt+G           Open settings                     │
│    Ctrl+Q          Quit application                  │
│    Ctrl+M          Minimize to tray                  │
│                                                      │
│  SETTINGS DIALOG (when dialog is open)               │
│    Ctrl+Tab        Next tab                          │
│    Ctrl+Shift+Tab  Previous tab                      │
│    Ctrl+S          Save settings                     │
│    Esc             Cancel                            │
│                                                      │
│  NAVIGATION (all windows)                            │
│    Tab             Next control                      │
│    Shift+Tab       Previous control                  │
│    Space           Activate button                   │
│    Enter           Confirm action                    │
│    Esc             Cancel/Close                      │
│                                                      │
│  PLATFORM NOTES                                      │
│    macOS: Use Cmd (⌘) instead of Ctrl               │
│    Linux: Global shortcuts may not work on Wayland   │
│    Windows: All shortcuts work as documented         │
└──────────────────────────────────────────────────────┘
```

## Default Shortcut Configuration

The default shortcuts are defined in the configuration file:

```json
{
  "shortcuts": {
    "start_stop": "Ctrl+Shift+S",
    "show_hide": "Ctrl+Shift+H"
  }
}
```

You can manually edit this file to change shortcuts:
- **Windows**: `%APPDATA%\OpenLiveCaption\config.json`
- **macOS**: `~/Library/Application Support/OpenLiveCaption/config.json`
- **Linux**: `~/.config/OpenLiveCaption/config.json`

## Tips for Effective Shortcut Use

1. **Memorize the essentials**: Focus on `Ctrl+Shift+S` and `Ctrl+Shift+H`
2. **Customize for your workflow**: Change shortcuts to match your habits
3. **Avoid conflicts**: Check for conflicts with other applications
4. **Use system tray**: When shortcuts don't work, use the tray menu
5. **Practice**: Use shortcuts regularly to build muscle memory

## Accessibility Features

OpenLiveCaption supports full keyboard navigation:
- All controls are accessible via keyboard
- Tab order follows logical flow
- Access keys (Alt+Letter) for quick access
- Screen reader compatible
- High contrast mode support

For users with motor disabilities:
- Shortcuts can be customized to single-key combinations (with modifiers)
- System tray provides mouse-free access
- Voice control software can trigger shortcuts

---

**Need help?** See [README.md](README.md) for full documentation or visit [GitHub Issues](https://github.com/yourusername/OpenLiveCaption/issues).
