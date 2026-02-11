# Changelog

All notable changes to OpenLiveCaption will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-02-10

### 🎉 Major Release - Complete Rewrite

OpenLiveCaption v2.0.0 is a complete rewrite transforming the application from a webcam-based subtitle display into a comprehensive system-wide live captioning solution.

### Added

#### Core Features
- **System-wide overlay display** - Always-on-top captions that work across all applications
- **Click-through transparency** - Interact with underlying applications without interference
- **Real-time transcription** - OpenAI Whisper integration with multiple model sizes
- **Audio capture engine** - Capture from microphone or system audio
- **Multi-source audio support** - Simultaneous capture from multiple sources
- **Voice Activity Detection (VAD)** - Pause processing during silence
- **Translation support** - Real-time translation to multiple languages
- **Subtitle export** - Export captions to SRT and VTT formats
- **Dual-language export** - Export both original and translated subtitles

#### User Interface
- **Control window** - Intuitive interface for all settings
- **System tray integration** - Minimize to tray with quick access menu
- **Settings dialog** - Comprehensive configuration with tabbed interface
- **Keyboard shortcuts** - Global hotkeys for start/stop and show/hide
- **Audio level indicator** - Real-time visual feedback of audio input
- **Status indicators** - Clear display of current state (running/stopped)

#### Customization
- **Overlay positioning** - Top, bottom, or custom placement
- **Multi-monitor support** - Works across multiple displays
- **Font customization** - Configurable font family and size
- **Color customization** - Adjustable text and background colors
- **Opacity control** - Configurable background transparency
- **Display modes** - Scroll or replace text modes
- **Auto-clear timeout** - Automatic caption clearing after silence

#### Platform Support
- **Windows audio capture** - WASAPI loopback for system audio (no additional software needed)
- **macOS audio capture** - Core Audio with BlackHole support
- **Linux audio capture** - PulseAudio and PipeWire support
- **Cross-platform packaging** - Standalone installers for Windows, macOS, and Linux

#### Performance
- **Low latency** - Captions appear within 2 seconds of speech
- **Efficient resource usage** - Optimized for minimal CPU and memory usage
- **GPU acceleration** - Optional CUDA support for faster transcription
- **Model caching** - Faster startup with cached models
- **Overlapping chunk processing** - Better word boundary handling

#### Reliability
- **Graceful error handling** - Comprehensive error recovery
- **Automatic device reconnection** - Handle device disconnection/reconnection
- **Overlay recreation** - Automatic recreation on unexpected close
- **Configuration persistence** - Settings saved across sessions
- **Corruption handling** - Recover from corrupted configuration files

#### Testing
- **Property-based testing** - 29 correctness properties with 100+ iterations each
- **Unit testing** - 150+ unit tests covering all components
- **Integration testing** - End-to-end workflow validation
- **Platform-specific testing** - Tests for Windows, macOS, and Linux

#### Documentation
- **Comprehensive README** - Complete user guide with installation and usage
- **Quick start guide** - Get started in 5 minutes
- **Keyboard shortcuts reference** - Complete shortcuts documentation
- **Troubleshooting guide** - Extensive troubleshooting for common issues
- **Platform-specific guides** - Setup instructions for macOS and Linux
- **Packaging guide** - Build and distribution instructions
- **Code signing guides** - Instructions for Windows and macOS code signing

### Changed
- **Architecture** - Complete rewrite with modular design
- **Audio processing** - New audio capture engine with platform-specific implementations
- **Transcription** - Improved Whisper integration with better error handling
- **UI framework** - Migrated from Tkinter to PyQt6 for better cross-platform support
- **Configuration** - JSON-based configuration with platform-specific locations
- **Packaging** - PyInstaller-based packaging with size optimization

### Removed
- **Webcam integration** - Removed webcam-based subtitle display (focus on system-wide captions)
- **Video overlay** - Removed video-specific features (now works with all applications)

### Fixed
- **Timestamp precision** - Fixed SRT/VTT export timestamp rounding issues
- **Memory leaks** - Improved memory management in transcription engine
- **Device switching** - Fixed audio device switching without restart
- **Overlay positioning** - Fixed multi-monitor positioning issues
- **Configuration loading** - Fixed handling of corrupted configuration files

### Security
- **Local processing** - All audio processing happens locally (no data sent to external servers)
- **Configuration validation** - Validate all configuration values to prevent injection
- **File path sanitization** - Sanitize file paths to prevent directory traversal
- **Error message sanitization** - Prevent sensitive information leakage in error messages

### Performance
- **Startup time** - Reduced startup time to < 5 seconds
- **Memory usage** - Optimized memory usage (500MB-1GB depending on model)
- **Package size** - Reduced package size to ~250-280MB
- **Transcription latency** - Achieved < 2 second latency with tiny/base models

### Known Issues
- **macOS fullscreen** - Overlay may not appear in some fullscreen apps (requires accessibility permissions)
- **Linux Wayland** - Global keyboard shortcuts may not work on Wayland (use system tray instead)
- **First launch delay** - Model download takes 1-2 minutes on first launch
- **Large model memory** - Large Whisper models require significant RAM (2-10GB)

## [1.0.0] - 2024-XX-XX

### Initial Release
- Basic webcam-based subtitle display
- Whisper transcription
- Translation to Yoruba and Twi
- Simple Tkinter UI

---

## Version History

- **2.0.0** (2026-02-10) - Complete rewrite with system-wide overlay
- **1.0.0** (2024-XX-XX) - Initial release

## Upgrade Guide

### From v1.x to v2.0.0

OpenLiveCaption v2.0.0 is a complete rewrite and is not compatible with v1.x configurations.

**Migration steps:**
1. Uninstall v1.x
2. Install v2.0.0
3. Reconfigure settings (v1.x settings will not be imported)

**Breaking changes:**
- Configuration file format changed from INI to JSON
- Configuration file location changed to platform-specific directories
- Webcam integration removed (focus on system-wide captions)
- UI completely redesigned (PyQt6 instead of Tkinter)

## Support

For issues, questions, or feature requests:
- **GitHub Issues**: https://github.com/yourusername/OpenLiveCaption/issues
- **GitHub Discussions**: https://github.com/yourusername/OpenLiveCaption/discussions
- **Documentation**: See [README.md](README.md) and [docs/](docs/)

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

OpenLiveCaption is licensed under the MIT License. See [LICENSE.txt](LICENSE.txt) for details.

