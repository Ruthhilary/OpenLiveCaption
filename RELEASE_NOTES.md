# OpenLiveCaption v2.0.0 Release Notes

**Release Date:** February 10, 2026

## Overview

OpenLiveCaption v2.0.0 is a complete rewrite transforming the application from a webcam-based subtitle display into a comprehensive system-wide live captioning solution. This release provides real-time speech-to-text transcription as an always-on-top overlay that works across all applications.

## 🎉 Major Features

### System-Wide Overlay
- **Always-on-top display**: Captions appear above all applications including fullscreen apps
- **Click-through transparency**: Interact with underlying applications without interference
- **Customizable positioning**: Top, bottom, or custom placement with multi-monitor support
- **Configurable styling**: Adjust font, colors, opacity, and display modes

### Real-Time Transcription
- **OpenAI Whisper integration**: State-of-the-art speech recognition
- **Multiple model sizes**: Choose from tiny (fast) to large (accurate)
- **Auto language detection**: Supports 99+ languages
- **Low latency**: Captions appear within 2 seconds of speech

### Audio Capture
- **System audio capture**: Transcribe audio from Zoom, Teams, YouTube, and more
- **Microphone input**: Caption your own speech
- **Multi-source support**: Capture from multiple sources simultaneously
- **Voice Activity Detection**: Pause processing during silence to save resources

### Translation Support
- **Real-time translation**: Translate captions to other languages
- **Dual-language display**: Show both original and translated text
- **Multiple languages**: Support for Yoruba, Twi, and more

### Subtitle Export
- **SRT format**: Export captions with timestamps
- **VTT format**: WebVTT format support
- **Dual-language export**: Export both original and translated subtitles

### User Interface
- **Control window**: Easy-to-use interface for all settings
- **System tray integration**: Minimize to tray with quick access menu
- **Keyboard shortcuts**: Global hotkeys for start/stop and show/hide
- **Settings dialog**: Comprehensive configuration options

## 🆕 What's New in v2.0.0

### Core Functionality
- Complete rewrite with modular architecture
- System-wide overlay instead of webcam-only display
- Platform-specific audio capture (WASAPI on Windows, Core Audio on macOS, PulseAudio/PipeWire on Linux)
- Overlapping chunk processing for better word boundary handling
- Configuration persistence across sessions

### User Experience
- Intuitive control window with status indicators
- System tray integration for background operation
- Customizable keyboard shortcuts
- Comprehensive settings dialog with tabbed interface
- Real-time audio level indicator

### Performance
- Optimized for low latency (< 2 seconds)
- Efficient resource usage with VAD
- GPU acceleration support (optional)
- Model caching for faster startup

### Reliability
- Graceful error handling and recovery
- Automatic device reconnection
- Overlay recreation on unexpected close
- Configuration file corruption handling

## 📦 Installation

### Windows
1. Download `OpenLiveCaption-2.0.0-Windows-Setup.exe`
2. Run the installer
3. Launch from Start Menu or Desktop shortcut

### macOS
1. Download `OpenLiveCaption-2.0.0-macOS.dmg`
2. Open the DMG and drag to Applications
3. Install BlackHole for system audio: `brew install blackhole-2ch`
4. Launch from Applications folder

### Linux
1. Download `OpenLiveCaption-2.0.0-x86_64.AppImage`
2. Make executable: `chmod +x OpenLiveCaption-2.0.0-x86_64.AppImage`
3. Run: `./OpenLiveCaption-2.0.0-x86_64.AppImage`

### From Source
```bash
git clone https://github.com/yourusername/OpenLiveCaption.git
cd OpenLiveCaption
pip install -r requirements.txt
python Main.py
```

## 🔧 System Requirements

### Minimum
- **OS**: Windows 10, macOS 11, or Ubuntu 20.04
- **RAM**: 2GB (4GB recommended)
- **Disk**: 500MB for application and models
- **CPU**: Dual-core processor

### Recommended
- **RAM**: 8GB or more
- **GPU**: NVIDIA GPU with CUDA support (optional)
- **Internet**: Required for first-time model download

## 🚀 Quick Start

1. Launch OpenLiveCaption
2. Select audio source (microphone or system audio)
3. Choose model size (tiny for speed, large for accuracy)
4. Click "Start Captions"
5. Speak or play audio - captions appear in overlay!

See [QUICK_START.md](QUICK_START.md) for detailed instructions.

## 📝 Configuration

Configuration is stored in:
- **Windows**: `%APPDATA%\OpenLiveCaption\config.json`
- **macOS**: `~/Library/Application Support/OpenLiveCaption/config.json`
- **Linux**: `~/.config/OpenLiveCaption/config.json`

All settings can be configured through the Settings dialog (⚙ button).

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Shift+S` | Start/Stop captions |
| `Ctrl+Shift+H` | Show/Hide overlay |

Shortcuts can be customized in Settings > Shortcuts.

## 🐛 Known Issues

### All Platforms
- First launch may take 1-2 minutes to download Whisper model
- Large models (medium, large) require significant RAM (2-10GB)
- Translation requires additional model downloads on first use

### Windows
- Some antivirus software may flag the executable (false positive)
- WASAPI loopback may not work on very old audio drivers

### macOS
- System audio capture requires BlackHole installation
- Overlay may not appear in fullscreen apps without accessibility permissions
- First launch requires right-click > Open to bypass Gatekeeper

### Linux
- Global keyboard shortcuts may not work on Wayland
- Some window managers may not support always-on-top
- AppImage requires FUSE to be installed

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for solutions.

## 🔄 Upgrading from v1.x

OpenLiveCaption v2.0.0 is a complete rewrite and is not compatible with v1.x configurations. 

**Migration steps:**
1. Uninstall v1.x
2. Install v2.0.0
3. Reconfigure settings (v1.x settings will not be imported)

## 🛠️ Technical Details

### Architecture
- **GUI Framework**: PyQt6
- **Audio Capture**: PyAudioWPatch (Windows), sounddevice (macOS/Linux)
- **Transcription**: OpenAI Whisper
- **Translation**: MarianMT (Hugging Face Transformers)
- **Packaging**: PyInstaller

### Dependencies
- Python 3.8+
- PyQt6 6.0+
- openai-whisper 20230314+
- torch 2.0+
- transformers 4.30+

### File Structure
```
OpenLiveCaption/
├── src/
│   ├── audio/          # Audio capture engine
│   ├── transcription/  # Whisper integration
│   ├── translation/    # Translation engine
│   ├── ui/             # PyQt6 UI components
│   ├── config/         # Configuration management
│   └── export/         # Subtitle export
├── tests/              # Test suite
├── docs/               # Documentation
└── Main.py             # Application entry point
```

## 📚 Documentation

- [README.md](README.md) - Complete user guide
- [QUICK_START.md](QUICK_START.md) - Quick start guide
- [KEYBOARD_SHORTCUTS.md](KEYBOARD_SHORTCUTS.md) - Keyboard shortcuts reference
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Troubleshooting guide
- [docs/MACOS_SETUP.md](docs/MACOS_SETUP.md) - macOS audio setup
- [docs/LINUX_SETUP.md](docs/LINUX_SETUP.md) - Linux audio setup
- [PACKAGING.md](PACKAGING.md) - Build and packaging guide

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup
```bash
git clone https://github.com/yourusername/OpenLiveCaption.git
cd OpenLiveCaption
pip install -r requirements.txt
pytest  # Run tests
python Main.py  # Run application
```

## 📄 License

OpenLiveCaption is licensed under the MIT License. See [LICENSE.txt](LICENSE.txt) for details.

## 🙏 Acknowledgments

- **OpenAI Whisper**: Excellent speech recognition model
- **PyQt6**: Robust cross-platform GUI framework
- **PyAudioWPatch**: Windows WASAPI loopback support
- **Hugging Face**: Translation models and transformers library
- **Community contributors**: Thank you for bug reports and feature requests!

## 🔮 Roadmap

### Planned for v2.1.0
- Additional translation languages
- Custom vocabulary support
- Improved GPU acceleration
- Cloud-based transcription option (optional)

### Future Releases
- Mobile companion app
- Browser extension
- Speaker diarization
- Real-time collaboration features
- Custom model training

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/yourusername/OpenLiveCaption/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/OpenLiveCaption/discussions)
- **Email**: support@openlivecaption.com

## 🔐 Security

OpenLiveCaption processes all audio locally on your device. No audio data is sent to external servers. For security issues, please email security@openlivecaption.com.

## 📊 Statistics

- **Lines of Code**: ~5,000
- **Test Coverage**: 85%+
- **Property-Based Tests**: 29 properties
- **Unit Tests**: 150+ tests
- **Supported Languages**: 99+ (via Whisper)
- **Package Size**: ~250MB (Windows), ~280MB (macOS), ~260MB (Linux)

---

**Made with ❤️ for accessibility and inclusion**

Thank you for using OpenLiveCaption! We hope it makes your digital experience more accessible and enjoyable.

