# OpenLiveCaption

**OpenLiveCaption** is a free, open-source system-wide live captioning application that provides real-time speech-to-text transcription as an always-on-top overlay. Perfect for video conferencing, presentations, streaming, and accessibility.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## Features

- **System-Wide Overlay**: Captions appear on top of all applications
- **Real-Time Transcription**: Powered by OpenAI Whisper for accurate speech-to-text
- **Multiple Audio Sources**: Capture from microphone or system audio (Zoom, Teams, YouTube, etc.)
- **Customizable Display**: Configure font, colors, position, and opacity
- **Translation Support**: Translate captions to 47 languages (Spanish, French, German, Chinese, Arabic, and more)
- **Subtitle Export**: Save captions as SRT or VTT files
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Privacy-Focused**: All processing happens locally on your device
- **Keyboard Shortcuts**: Quick access to start/stop and show/hide functions

## Quick Start

### Installation

#### From Source

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/OpenLiveCaption.git
   cd OpenLiveCaption
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python Main.py
   ```

#### From Package (Coming Soon)

Download the installer for your platform:
- **Windows**: `OpenLiveCaption-Setup.exe`
- **macOS**: `OpenLiveCaption.dmg`
- **Linux**: `OpenLiveCaption.AppImage`

### First Run

On first launch:
1. The application will download the Whisper model (this may take a few minutes)
2. A configuration file will be created in your system's config directory
3. The control window and caption overlay will appear

### Basic Usage

1. **Select Audio Source**: Choose your microphone or system audio from the dropdown
2. **Choose Model Size**: Select a Whisper model (tiny = fast, large = accurate)
3. **Click "Start Captions"**: Begin transcription
4. **Speak or play audio**: Captions will appear in the overlay window

## System Requirements

### Minimum Requirements
- **OS**: Windows 10, macOS 11, or Ubuntu 20.04 (or equivalent)
- **RAM**: 2GB (4GB recommended for larger models)
- **Disk Space**: 500MB for application and models
- **Processor**: Dual-core CPU (quad-core recommended)

### Recommended Requirements
- **RAM**: 8GB or more
- **GPU**: NVIDIA GPU with CUDA support (optional, for faster transcription)
- **Internet**: Required for first-time model download only

## Platform-Specific Setup

### Windows

OpenLiveCaption works out of the box on Windows 10 and 11:
- **System Audio Capture**: Uses WASAPI loopback (no additional software needed)
- **Microphone**: Standard microphone input supported
- **Compatibility**: Works with Zoom, Teams, Discord, YouTube, and more

### macOS

For system audio capture on macOS, you need a virtual audio device:

1. **Install BlackHole** (recommended):
   ```bash
   brew install blackhole-2ch
   ```
   Or download from: https://existential.audio/blackhole/

2. **Configure Audio Routing**:
   - Open Audio MIDI Setup
   - Create a Multi-Output Device
   - Add both your speakers and BlackHole
   - Set as system output

See [docs/MACOS_SETUP.md](docs/MACOS_SETUP.md) for detailed instructions.

### Linux

OpenLiveCaption supports PulseAudio and PipeWire:

1. **Check your audio system**:
   ```bash
   pactl info  # For PulseAudio
   pw-cli info # For PipeWire
   ```

2. **Find monitor sources**:
   ```bash
   pactl list sources | grep monitor
   ```

3. **Select monitor source** in OpenLiveCaption to capture system audio

See [docs/LINUX_SETUP.md](docs/LINUX_SETUP.md) for detailed instructions.

## User Guide

### Control Window

The main control window provides:
- **Start/Stop Captions**: Begin or end transcription
- **Audio Source Selection**: Choose input device
- **Model Size**: Select Whisper model (tiny, base, small, medium, large)
- **Language**: Auto-detect or manual selection
- **Settings**: Configure all application options
- **Show/Hide Overlay**: Toggle caption display

### Caption Overlay

The overlay window displays captions on top of all applications:
- **Always on Top**: Stays visible over fullscreen apps
- **Click-Through**: Doesn't interfere with mouse clicks
- **Customizable**: Adjust position, font, colors, and opacity
- **Multi-Monitor**: Works across multiple displays

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Shift+S` | Start/Stop captions |
| `Ctrl+Shift+H` | Show/Hide overlay |

*Shortcuts can be customized in Settings*

### System Tray

The application minimizes to the system tray:
- **Double-click**: Show control window
- **Right-click**: Access quick menu
  - Start/Stop Captions
  - Show/Hide Overlay
  - Settings
  - Exit

### Settings

Access settings by clicking the ⚙ Settings button:

#### Audio Tab
- **Device Selection**: Choose audio input device
- **Sample Rate**: Audio sample rate (default: 16000 Hz)
- **Chunk Duration**: Audio processing interval (default: 1.0 seconds)
- **VAD Threshold**: Voice activity detection sensitivity

#### Transcription Tab
- **Model Size**: Whisper model selection
  - `tiny`: Fastest, least accurate (~75MB)
  - `base`: Fast, good accuracy (~150MB)
  - `small`: Balanced (~500MB)
  - `medium`: Accurate, slower (~1.5GB)
  - `large`: Most accurate, slowest (~3GB)
- **Device**: CPU or GPU processing
- **Language**: Auto-detect or manual selection
- **Translation**: Enable translation to target language

#### Overlay Tab
- **Position**: Top, Bottom, or Custom
- **Font Family**: Choose display font
- **Font Size**: Text size (default: 24)
- **Text Color**: Caption text color
- **Background Color**: Overlay background color
- **Background Opacity**: Transparency level (0-100%)
- **Max Lines**: Maximum lines displayed (default: 3)
- **Display Mode**: Scroll or Replace
- **Auto-Clear Timeout**: Clear captions after silence (seconds)

#### Export Tab
- **Enable Export**: Save captions to file
- **Format**: SRT or VTT
- **Output Path**: File save location

#### Shortcuts Tab
- **Start/Stop**: Customize start/stop shortcut
- **Show/Hide**: Customize overlay toggle shortcut

## Troubleshooting

### No Audio Devices Found

**Problem**: Audio device dropdown is empty

**Solutions**:
- Check that your microphone or audio device is connected
- On macOS: Install BlackHole for system audio capture
- On Linux: Ensure PulseAudio or PipeWire is running
- Restart the application after connecting devices

### Captions Not Appearing

**Problem**: No captions display when speaking

**Solutions**:
- Verify the overlay is not hidden (press `Ctrl+Shift+H`)
- Check audio level indicator shows activity
- Increase microphone volume in system settings
- Try speaking louder or closer to the microphone
- Select a different audio device

### Model Loading Fails

**Problem**: Error loading Whisper model

**Solutions**:
- Ensure internet connection for first-time download
- Check available disk space (models: 75MB - 3GB)
- Try a smaller model size (tiny or base)
- Clear model cache and re-download:
  - Windows: `%USERPROFILE%\.cache\whisper`
  - macOS/Linux: `~/.cache/whisper`

### High CPU Usage

**Problem**: Application uses too much CPU

**Solutions**:
- Use a smaller Whisper model (tiny or base)
- Increase chunk duration in settings (reduces processing frequency)
- Disable translation if not needed
- Close other resource-intensive applications

### Overlay Not Visible in Fullscreen

**Problem**: Overlay disappears in fullscreen apps

**Solutions**:
- Try different overlay position (Top instead of Bottom)
- On macOS: Grant accessibility permissions in System Preferences
- On Linux: Check window manager settings for always-on-top support
- Use windowed mode instead of fullscreen

### Application Crashes

**Problem**: Application closes unexpectedly

**Solutions**:
- Check console output for error messages
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Delete config file and restart:
  - Windows: `%APPDATA%\OpenLiveCaption\config.json`
  - macOS: `~/Library/Application Support/OpenLiveCaption/config.json`
  - Linux: `~/.config/OpenLiveCaption/config.json`
- Update to the latest version
- Report the issue on GitHub with error logs

### Poor Transcription Accuracy

**Problem**: Captions are inaccurate or garbled

**Solutions**:
- Use a larger Whisper model (medium or large)
- Manually select the correct language instead of auto-detect
- Improve audio quality (reduce background noise)
- Speak more clearly and at a moderate pace
- Check microphone positioning and volume

### Translation Not Working

**Problem**: Translation feature doesn't work

**Solutions**:
- Ensure internet connection for first-time model download
- Check available disk space for translation models
- Verify target language is supported
- Disable and re-enable translation in settings
- Check console for error messages

### Keyboard Shortcuts Not Working

**Problem**: Global shortcuts don't respond

**Solutions**:
- On Linux/Wayland: Global shortcuts may not be supported
- Use the control window or system tray instead
- Check if another application is using the same shortcut
- Customize shortcuts in Settings to avoid conflicts
- Ensure the application has necessary permissions

## Advanced Usage

### GPU Acceleration

To use GPU acceleration for faster transcription:

1. Install CUDA-enabled PyTorch:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

2. In Settings > Transcription, select "cuda" as device

3. Restart the application

### Custom Model Path

To use a custom Whisper model:

1. Download the model to a local directory
2. Edit the config file and set `model_path` to your model location
3. Restart the application

### Batch Processing

To transcribe pre-recorded audio files:

```python
from src.transcription.transcription_engine import TranscriptionEngine
import numpy as np

engine = TranscriptionEngine(model_name="base")
# Load your audio file as numpy array
audio = np.load("audio.npy")
result = engine.transcribe(audio)
print(result.text)
```

### API Integration

OpenLiveCaption can be integrated into other applications:

```python
from src.application import Application

app = Application()
app.start_captions()
# Your code here
app.stop_captions()
```

## Configuration File

The configuration file is stored in JSON format:

**Location**:
- Windows: `%APPDATA%\OpenLiveCaption\config.json`
- macOS: `~/Library/Application Support/OpenLiveCaption/config.json`
- Linux: `~/.config/OpenLiveCaption/config.json`

**Example**:
```json
{
  "audio": {
    "device_id": -1,
    "sample_rate": 16000,
    "chunk_duration": 1.0,
    "vad_threshold": 0.01
  },
  "transcription": {
    "model_name": "tiny",
    "device": "cpu",
    "language": null,
    "enable_translation": false,
    "target_language": null
  },
  "overlay": {
    "position": "bottom",
    "custom_x": 0,
    "custom_y": 0,
    "width": 0,
    "height": 150,
    "font_family": "Arial",
    "font_size": 24,
    "text_color": "#FFFFFF",
    "background_color": "#000000",
    "background_opacity": 0.7,
    "max_lines": 3,
    "scroll_mode": "replace",
    "clear_timeout": 5.0
  },
  "export": {
    "enabled": true,
    "format": "srt",
    "output_path": "subtitles.srt"
  },
  "shortcuts": {
    "start_stop": "Ctrl+Shift+S",
    "show_hide": "Ctrl+Shift+H"
  }
}
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/OpenLiveCaption.git`
3. Create a branch: `git checkout -b feature/your-feature`
4. Install dev dependencies: `pip install -r requirements.txt`
5. Make your changes
6. Run tests: `pytest`
7. Submit a pull request

## License

OpenLiveCaption is licensed under the MIT License. See [LICENSE.txt](LICENSE.txt) for details.

## Acknowledgments

- **OpenAI Whisper**: Speech recognition model
- **PyQt6**: GUI framework
- **PyAudioWPatch**: Windows audio capture
- **sounddevice**: Cross-platform audio I/O
- **MarianMT**: Translation models

## Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/yourusername/OpenLiveCaption/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/OpenLiveCaption/discussions)

## Roadmap

- [ ] Additional translation languages
- [ ] Cloud-based transcription options
- [ ] Mobile companion app
- [ ] Browser extension
- [ ] Custom vocabulary support
- [ ] Speaker diarization
- [ ] Real-time collaboration features

## Privacy Policy

OpenLiveCaption processes all audio locally on your device. No audio data is sent to external servers unless you explicitly enable cloud-based features (not currently available). Configuration and subtitle files are stored locally on your device.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and release notes.

---

**Made with ❤️ for accessibility and inclusion**
