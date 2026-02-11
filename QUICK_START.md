# OpenLiveCaption Quick Start Guide

Get up and running with OpenLiveCaption in 5 minutes!

## Installation

### Option 1: Run from Source (All Platforms)

```bash
# Clone the repository
git clone https://github.com/yourusername/OpenLiveCaption.git
cd OpenLiveCaption

# Install dependencies
pip install -r requirements.txt

# Run the application
python Main.py
```

### Option 2: Download Installer (Coming Soon)

- **Windows**: Download and run `OpenLiveCaption-Setup.exe`
- **macOS**: Download and open `OpenLiveCaption.dmg`, drag to Applications
- **Linux**: Download `OpenLiveCaption.AppImage`, make executable, and run

## Platform-Specific Setup

### Windows Users
✅ No additional setup needed! System audio capture works out of the box.

### macOS Users
⚠️ **Required**: Install BlackHole for system audio capture

```bash
brew install blackhole-2ch
```

Then configure Multi-Output Device in Audio MIDI Setup. See [docs/MACOS_SETUP.md](docs/MACOS_SETUP.md) for details.

### Linux Users
✅ Works with PulseAudio or PipeWire (usually pre-installed)

Check if PulseAudio is running:
```bash
pactl info
```

## First Launch

1. **Application starts** - You'll see two windows:
   - Control Window (main interface)
   - Caption Overlay (transparent, on top of everything)

2. **Model download** - First time only, Whisper model downloads (1-2 minutes)

3. **Ready to use!**

## Basic Usage

### Step 1: Select Audio Source

In the Control Window:
- Click the **Audio Source** dropdown
- Choose:
  - **Microphone** - To caption your own speech
  - **System Audio** (Windows) or **BlackHole** (macOS) or **Monitor** (Linux) - To caption computer audio

### Step 2: Choose Model Size

- **tiny** - Fastest, good for real-time (recommended for first try)
- **base** - Good balance of speed and accuracy
- **small/medium/large** - More accurate but slower

### Step 3: Start Captions

1. Click **Start Captions** button
2. Speak into your microphone OR play audio from any app
3. Watch captions appear in the overlay!

### Step 4: Customize (Optional)

Click **⚙ Settings** to adjust:
- **Overlay position** (top/bottom/custom)
- **Font size and color**
- **Background opacity**
- **Language** (auto-detect or manual)

## Common Use Cases

### Video Conferencing (Zoom, Teams, Meet)

1. Select **System Audio** as source (or **BlackHole** on macOS)
2. Start captions
3. Join your meeting
4. Captions appear for all speakers!

**Tip**: Position overlay at bottom so it doesn't cover faces

### YouTube/Streaming

1. Select **System Audio** as source
2. Start captions
3. Play your video
4. Enjoy real-time captions!

### Presentations

1. Select **Microphone** as source
2. Start captions before presenting
3. Your speech appears as captions
4. Audience can read along!

**Tip**: Use **large** font size for better visibility

### Accessibility

1. Keep OpenLiveCaption running in background
2. Minimize to system tray
3. Use keyboard shortcuts:
   - `Ctrl+Shift+S` - Start/Stop
   - `Ctrl+Shift+H` - Show/Hide overlay

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Shift+S` | Start/Stop captions |
| `Ctrl+Shift+H` | Show/Hide overlay |

*Customize in Settings > Shortcuts*

## System Tray

When you close the Control Window, the app minimizes to system tray:

- **Double-click tray icon** - Show Control Window
- **Right-click tray icon** - Quick menu
  - Start/Stop Captions
  - Show/Hide Overlay
  - Settings
  - Exit

## Quick Troubleshooting

### "No audio devices found"
- **Windows**: Check microphone is connected
- **macOS**: Install BlackHole
- **Linux**: Run `pactl list sources`

### "Captions not appearing"
- Press `Ctrl+Shift+H` to show overlay
- Check audio level indicator is moving
- Increase microphone volume

### "Model loading failed"
- Check internet connection (first time only)
- Try smaller model (tiny)
- Free up disk space

### "High CPU usage"
- Use smaller model (tiny or base)
- Increase chunk duration in settings

## Tips for Best Results

### Audio Quality
- Use a good quality microphone
- Reduce background noise
- Speak clearly at moderate pace
- Position microphone 6-12 inches from mouth

### Model Selection
- **Real-time conversations**: Use tiny or base
- **Recorded content**: Use medium or large
- **Multiple languages**: Use medium or large

### Overlay Positioning
- **Video calls**: Bottom position
- **Presentations**: Top position
- **Gaming**: Custom position (avoid HUD)

### Performance
- Close unnecessary applications
- Use GPU acceleration if available
- Disable translation if not needed

## Next Steps

### Explore Settings
- Try different fonts and colors
- Adjust overlay opacity
- Enable translation
- Configure subtitle export

### Learn Advanced Features
- Multi-source audio capture
- Custom keyboard shortcuts
- Subtitle export (SRT/VTT)
- Translation to other languages

### Read Full Documentation
- [README.md](README.md) - Complete user guide
- [docs/MACOS_SETUP.md](docs/MACOS_SETUP.md) - macOS audio setup
- [docs/LINUX_SETUP.md](docs/LINUX_SETUP.md) - Linux audio setup
- [RUNNING_THE_APPLICATION.md](RUNNING_THE_APPLICATION.md) - Detailed usage

## Getting Help

- **Documentation**: Check [docs/](docs/) folder
- **Issues**: Report bugs on [GitHub Issues](https://github.com/yourusername/OpenLiveCaption/issues)
- **Questions**: Ask on [GitHub Discussions](https://github.com/yourusername/OpenLiveCaption/discussions)

## Quick Reference Card

```
┌─────────────────────────────────────────────────────┐
│  OpenLiveCaption Quick Reference                    │
├─────────────────────────────────────────────────────┤
│  Start/Stop:        Ctrl+Shift+S                    │
│  Show/Hide:         Ctrl+Shift+H                    │
│  Settings:          Click ⚙ button                  │
│  System Tray:       Right-click tray icon           │
│                                                     │
│  Audio Sources:                                     │
│    • Microphone     - Your voice                    │
│    • System Audio   - Computer audio (Windows)      │
│    • BlackHole      - Computer audio (macOS)        │
│    • Monitor        - Computer audio (Linux)        │
│                                                     │
│  Model Sizes:                                       │
│    • tiny    - Fastest (75MB)                       │
│    • base    - Fast (150MB)                         │
│    • small   - Balanced (500MB)                     │
│    • medium  - Accurate (1.5GB)                     │
│    • large   - Most accurate (3GB)                  │
│                                                     │
│  Config Location:                                   │
│    • Windows: %APPDATA%\OpenLiveCaption             │
│    • macOS:   ~/Library/Application Support/...    │
│    • Linux:   ~/.config/OpenLiveCaption             │
└─────────────────────────────────────────────────────┘
```

---

**Ready to start? Run `python Main.py` and begin captioning!** 🎉
