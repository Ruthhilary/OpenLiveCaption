# OpenLiveCaption

**OpenLiveCaption** is a free, open-source system-wide live captioning application that provides real-time speech-to-text transcription as an always-on-top overlay. Perfect for video conferencing, presentations, streaming, and accessibility.

🎬 OpenLiveCaption v2.1

**Real-time Speech-to-Text Captions for YouTube, Zoom, and More!**

[![Version](https://img.shields.io/badge/version-2.1-blue.svg)](https://github.com/Ruthhilary/OpenLiveCaption/releases)
[![Python](https://img.shields.io/badge/python-3.11+-green.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://github.com/Ruthhilary/OpenLiveCaption)

---

## ✨ Features

- 🎯 **Real-time Captions** - Instant speech-to-text transcription
- 🔊 **System Audio Capture** - Capture audio from YouTube, Zoom, Discord, and any application
- 🎤 **Microphone Support** - Transcribe your own speech
- 🌍 **Multi-language Support** - Auto-detect or select from 90+ languages
- 🔄 **Live Translation** - Translate captions to another language in real-time
- 🎨 **Customizable Overlay** - Adjust position, size, colors, and fonts
- 💾 **Export Subtitles** - Save captions as SRT files
- 🚀 **Beginner-Friendly** - Simple interface with clear instructions
- 🖥️ **Clean GUI** - Professional interface with no command prompt
- ⚡ **Fast & Accurate** - Powered by OpenAI Whisper AI

---

## 🚀 Quick Start

### 1. Download
Download the latest release: [OpenLiveCaption v2.1](https://github.com/Ruthhilary/OpenLiveCaption/releases)

### 2. Install Requirements
- **Python 3.11+** - [Download here](https://www.python.org/downloads/)
- **Visual C++ Redistributables** - [Download here](https://aka.ms/vs/17/release/vc_redist.x64.exe)

### 3. Install Python Packages
Open Command Prompt and run:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install openai-whisper PyQt6 sounddevice PyAudioWPatch numpy opencv-python
```

### 4. Start the Application
Double-click: **START_OPENLIVE_CAPTION.bat**

That's it! The application will start with a clean GUI (no command prompt).

---

## 📖 How to Use

### For YouTube/Zoom (System Audio):
1. **Start playing audio** (YouTube video, Zoom call, etc.)
2. Open OpenLiveCaption
3. Select: **🔊 Speakers [Loopback]** device
4. Click **"▶ Start Captions"**
5. Captions appear automatically!

### For Microphone:
1. Open OpenLiveCaption
2. Select: **🎤 Microphone** device
3. Click **"▶ Start Captions"**
4. Speak into your microphone
5. Your speech appears as captions!

---

## 🎯 Key Improvements in v2.1

### ✅ Beginner-Friendly Interface
- Clear audio device labels with icons (🔊 for system audio, 🎤 for microphones)
- Visual separators showing which device is for what purpose
- Recommended devices marked with ⭐
- Helpful tooltips explaining each option

### ✅ No Command Prompt Window
- Clean professional GUI
- Launches with pythonw (no black console window)
- Simple one-click launcher

### ✅ Improved Audio Capture
- Automatic sample rate detection and conversion
- Support for 48000 Hz, 44100 Hz, and 16000 Hz devices
- Better error handling and reconnection
- Works with USB audio devices and built-in audio

### ✅ Enhanced Stability
- PyTorch DLL loading fix included
- Automatic error recovery
- Device disconnection handling
- Better memory management

### ✅ Better User Experience
- Splash screen on startup
- System tray integration
- Minimize to tray
- Quick settings for common adjustments

---

## 🎨 Features in Detail

### Audio Capture
- **System Audio (Loopback)**: Capture audio from any application
  - YouTube videos
  - Zoom/Teams meetings
  - Discord voice chat
  - Spotify, Netflix, etc.
- **Microphone**: Capture your own speech
  - USB microphones
  - Built-in laptop microphones
  - Bluetooth headsets

### Transcription
- **AI-Powered**: Uses OpenAI Whisper for accurate transcription
- **Multiple Models**: Choose speed vs accuracy
  - `tiny` - Fastest (good for real-time)
  - `base` - Balanced (recommended)
  - `small` - More accurate
  - `medium` - Very accurate
  - `large` - Most accurate (slower)
- **90+ Languages**: Auto-detect or manually select

### Translation
- **Real-time Translation**: Translate captions to another language
- **90+ Target Languages**: Translate to any supported language
- **Preserve Original**: Option to show both original and translated text

### Customization
- **Position**: Top, bottom, or custom position
- **Appearance**: Font, size, colors, transparency
- **Behavior**: Auto-hide, scroll mode, line count
- **Export**: Save captions as SRT subtitle files

---

## 💻 System Requirements

### Minimum:
- **OS**: Windows 10/11
- **CPU**: Intel Core i3 or equivalent
- **RAM**: 4 GB
- **Storage**: 2 GB free space
- **Internet**: Required for first-time model download

### Recommended:
- **OS**: Windows 11
- **CPU**: Intel Core i5 or better
- **RAM**: 8 GB or more
- **Storage**: 5 GB free space
- **Internet**: Stable connection for best performance

---

## 🔧 Troubleshooting

### Application Won't Start
**Solution**: Restart your computer after installing Visual C++ Redistributables, then try again.

### No Audio Devices Showing
**Solution**: 
1. Right-click speaker icon in taskbar
2. Click "Sounds" → "Recording" tab
3. Right-click empty space → "Show Disabled Devices"
4. Enable "Stereo Mix" or loopback devices
5. Restart OpenLiveCaption

### "Invalid Sample Rate" Error
**Solution**:
1. Make sure audio is PLAYING before clicking "Start Captions"
2. Try a different audio device from the dropdown
3. Use microphone instead of loopback device
4. Close other audio applications (Discord, OBS, etc.)

### Captions Not Appearing
**Solution**:
1. Check that correct audio device is selected
2. Make sure audio is actually playing
3. Increase volume
4. Try different accuracy level (tiny/base/small)

### Slow Performance
**Solution**:
1. Use "tiny" or "base" model for faster performance
2. Close other heavy applications
3. Reduce caption overlay size
4. Disable translation if not needed

---

## 📁 Project Structure

```
OpenLiveCaption-v2.1-FIXED/
├── START_OPENLIVE_CAPTION.bat    # Main launcher (no console)
├── Main.py                        # Application entry point
├── fix_pytorch_and_run.py        # PyTorch DLL fix script
├── requirements.txt               # Python dependencies
├── src/                          # Source code
│   ├── application.py            # Main application logic
│   ├── audio/                    # Audio capture modules
│   ├── transcription/            # Whisper transcription
│   ├── translation/              # Translation engine
│   ├── ui/                       # User interface
│   ├── config/                   # Configuration management
│   └── export/                   # Subtitle export
├── assets/                       # Icons and resources
└── docs/                         # Documentation
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### How to Contribute:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OpenAI Whisper** - For the amazing speech recognition model
- **PyQt6** - For the GUI framework
- **PyAudioWPatch** - For WASAPI loopback support on Windows
- All contributors and users who provided feedback

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Ruthhilary/OpenLiveCaption/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Ruthhilary/OpenLiveCaption/discussions)
- **Email**: [Your Email]

---

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

---

## 📊 Version History

### v2.1 (Latest)
- ✅ Beginner-friendly audio device labels
- ✅ No command prompt window
- ✅ Improved audio capture with automatic sample rate conversion
- ✅ PyTorch DLL loading fix
- ✅ Better error handling and recovery
- ✅ Enhanced user interface
- ✅ System tray integration

### v2.0
- Initial release with basic functionality
- Real-time transcription
- Multi-language support
- Basic UI

---

## 🎉 Thank You!

Thank you for using OpenLiveCaption! We hope it makes your content more accessible.

**Made with ❤️ for accessibility**

---

**[⬆ Back to Top](#-openlive-caption-v21)**
