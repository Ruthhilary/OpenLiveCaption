# OpenLiveCaption Troubleshooting Guide

Complete troubleshooting guide for common issues and their solutions.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Audio Capture Issues](#audio-capture-issues)
- [Transcription Issues](#transcription-issues)
- [Overlay Display Issues](#overlay-display-issues)
- [Performance Issues](#performance-issues)
- [Translation Issues](#translation-issues)
- [Keyboard Shortcut Issues](#keyboard-shortcut-issues)
- [Export Issues](#export-issues)
- [Platform-Specific Issues](#platform-specific-issues)
- [Error Messages](#error-messages)
- [Getting Help](#getting-help)

---

## Installation Issues

### Dependencies Installation Fails

**Problem**: `pip install -r requirements.txt` fails with errors

**Solutions**:
1. **Update pip**:
   ```bash
   python -m pip install --upgrade pip
   ```

2. **Install build tools**:
   - **Windows**: Install Visual Studio Build Tools
   - **macOS**: Install Xcode Command Line Tools: `xcode-select --install`
   - **Linux**: Install build essentials: `sudo apt install build-essential python3-dev`

3. **Use virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Install dependencies individually**:
   ```bash
   pip install PyQt6
   pip install openai-whisper
   pip install pyaudiowpatch  # Windows only
   pip install sounddevice
   ```

### Python Version Incompatibility

**Problem**: Application doesn't run, Python version errors

**Solutions**:
1. **Check Python version**:
   ```bash
   python --version
   ```
   Required: Python 3.8 or higher

2. **Install correct Python version**:
   - Download from https://www.python.org/downloads/
   - Or use pyenv: `pyenv install 3.10`

3. **Use correct Python command**:
   - Try `python3` instead of `python`
   - Try `py` on Windows

### Module Not Found Errors

**Problem**: `ModuleNotFoundError: No module named 'xxx'`

**Solutions**:
1. **Verify installation**:
   ```bash
   pip list | grep xxx
   ```

2. **Reinstall the module**:
   ```bash
   pip install --force-reinstall xxx
   ```

3. **Check Python path**:
   ```bash
   python -c "import sys; print(sys.path)"
   ```

4. **Use absolute imports**:
   ```bash
   python -m src.application
   ```

---

## Audio Capture Issues

### No Audio Devices Found

**Problem**: Audio device dropdown is empty or shows no devices

**Solutions**:

**Windows**:
1. Check Device Manager for audio devices
2. Update audio drivers
3. Restart Windows Audio service:
   ```cmd
   net stop audiosrv
   net start audiosrv
   ```
4. Run as administrator

**macOS**:
1. Install BlackHole:
   ```bash
   brew install blackhole-2ch
   ```
2. Check Audio MIDI Setup for devices
3. Grant microphone permissions:
   - System Preferences > Security & Privacy > Microphone
   - Add OpenLiveCaption

**Linux**:
1. Check PulseAudio is running:
   ```bash
   pulseaudio --check
   echo $?  # Should output 0
   ```
2. Restart PulseAudio:
   ```bash
   pulseaudio -k
   pulseaudio --start
   ```
3. List devices:
   ```bash
   pactl list sources short
   ```
4. Add user to audio group:
   ```bash
   sudo usermod -a -G audio $USER
   ```
   Then log out and back in

### No Audio Being Captured

**Problem**: Audio level indicator doesn't move, no captions appear

**Solutions**:
1. **Check device selection**: Ensure correct device is selected
2. **Test microphone**: Use system sound recorder to verify microphone works
3. **Check volume**: Increase microphone volume in system settings
4. **Check mute**: Ensure microphone is not muted
5. **Test with different device**: Try another microphone or audio source
6. **Check permissions**: Grant microphone access to the application

**Verify audio capture**:
```bash
# Windows
python -c "import pyaudiowpatch as pyaudio; p = pyaudio.PyAudio(); print(p.get_device_count())"

# macOS/Linux
python -c "import sounddevice as sd; print(sd.query_devices())"
```

### System Audio Not Capturing

**Problem**: Microphone works but system audio doesn't capture

**Solutions**:

**Windows**:
1. Enable Stereo Mix:
   - Right-click speaker icon > Sounds > Recording
   - Right-click empty space > Show Disabled Devices
   - Enable Stereo Mix
2. Use WASAPI loopback device (should appear as [Loopback] in dropdown)
3. Update audio drivers

**macOS**:
1. Install BlackHole (required):
   ```bash
   brew install blackhole-2ch
   ```
2. Create Multi-Output Device:
   - Open Audio MIDI Setup
   - Click + > Create Multi-Output Device
   - Check Built-in Output and BlackHole
3. Set Multi-Output as system output
4. Select BlackHole in OpenLiveCaption
5. See [docs/MACOS_SETUP.md](docs/MACOS_SETUP.md) for detailed instructions

**Linux**:
1. Find monitor sources:
   ```bash
   pactl list sources | grep -E "Name:|Description:" | grep monitor
   ```
2. Select monitor source in OpenLiveCaption
3. If no monitors, load loopback module:
   ```bash
   pactl load-module module-loopback
   ```

### Audio Cutting Out

**Problem**: Audio capture stops intermittently

**Solutions**:
1. **Disable VAD**: Set VAD threshold to 0 in settings
2. **Increase buffer size**: Increase chunk duration in settings
3. **Check CPU usage**: Close other applications
4. **Update audio drivers**: Install latest drivers
5. **Disable power saving**: Prevent USB devices from sleeping
6. **Use wired connection**: Avoid Bluetooth audio devices

### Device Disconnection

**Problem**: "Audio device disconnected" error

**Solutions**:
1. **Reconnect device**: Unplug and replug USB device
2. **Wait for reconnection**: Application will attempt to reconnect automatically
3. **Select different device**: Choose another device from dropdown
4. **Check USB port**: Try different USB port
5. **Restart application**: Close and reopen OpenLiveCaption

---

## Transcription Issues

### Model Loading Fails

**Problem**: "Failed to load Whisper model" error

**Solutions**:
1. **Check internet connection**: Required for first-time download
2. **Check disk space**: Models require 75MB - 3GB
3. **Clear model cache**:
   - Windows: Delete `%USERPROFILE%\.cache\whisper`
   - macOS/Linux: Delete `~/.cache/whisper`
4. **Try smaller model**: Use "tiny" or "base" instead of "large"
5. **Manual download**:
   ```bash
   python -c "import whisper; whisper.load_model('tiny')"
   ```
6. **Check firewall**: Ensure Python can access internet

### Poor Transcription Accuracy

**Problem**: Captions are inaccurate, garbled, or nonsensical

**Solutions**:
1. **Use larger model**: Switch to "medium" or "large" in settings
2. **Set language manually**: Disable auto-detect, select specific language
3. **Improve audio quality**:
   - Reduce background noise
   - Use better microphone
   - Speak clearly and at moderate pace
   - Position microphone 6-12 inches from mouth
4. **Check audio levels**: Ensure audio is not too quiet or distorted
5. **Increase chunk duration**: Gives model more context
6. **Update Whisper**: `pip install --upgrade openai-whisper`

### Transcription Lag

**Problem**: Captions appear several seconds after speech

**Solutions**:
1. **Use smaller model**: Switch to "tiny" or "base"
2. **Reduce chunk duration**: Decrease to 0.5 seconds in settings
3. **Enable GPU**: Use CUDA if available (see GPU Acceleration below)
4. **Close other applications**: Free up CPU/RAM
5. **Disable translation**: Turn off translation if not needed
6. **Check CPU usage**: Ensure CPU is not throttling

### Wrong Language Detected

**Problem**: Transcription is in wrong language

**Solutions**:
1. **Set language manually**: Go to Settings > Transcription > Language
2. **Use larger model**: Better language detection
3. **Speak more**: Give model more audio to detect language
4. **Check audio quality**: Poor audio can confuse language detection

### Transcription Stops

**Problem**: Transcription stops working, no new captions

**Solutions**:
1. **Check audio capture**: Verify audio level indicator is moving
2. **Restart transcription**: Click Stop, then Start
3. **Check console for errors**: Look for error messages
4. **Restart application**: Close and reopen
5. **Check memory**: Ensure sufficient RAM available
6. **Update dependencies**: `pip install --upgrade openai-whisper torch`

---

## Overlay Display Issues

### Overlay Not Visible

**Problem**: Caption overlay doesn't appear

**Solutions**:
1. **Toggle visibility**: Press `Ctrl+Shift+H` or click "Show Overlay"
2. **Check position**: Overlay may be off-screen
   - Go to Settings > Overlay > Position
   - Try "Top" or "Bottom" position
3. **Check opacity**: Ensure opacity is not 0%
4. **Check multi-monitor**: Overlay may be on different monitor
5. **Restart overlay**: Click "Hide Overlay" then "Show Overlay"
6. **Check window manager**: Some tiling WMs may hide overlay

### Overlay Not Staying on Top

**Problem**: Other windows cover the overlay

**Solutions**:
1. **Check window flags**: Restart application to reset flags
2. **Grant permissions**:
   - **macOS**: System Preferences > Security & Privacy > Accessibility
   - **Linux**: Check window manager settings
3. **Try different position**: Some positions work better on certain systems
4. **Check desktop environment**: Some DEs may override always-on-top
5. **Use fullscreen workaround**: Set overlay to custom position

### Overlay Not Click-Through

**Problem**: Can't click through overlay to underlying windows

**Solutions**:
1. **Restart application**: Resets window flags
2. **Check Qt version**: Update PyQt6: `pip install --upgrade PyQt6`
3. **Platform limitation**: Some platforms may not support click-through
4. **Use keyboard**: Navigate underlying app with keyboard
5. **Reposition overlay**: Move to edge of screen

### Overlay Text Not Readable

**Problem**: Text is too small, wrong color, or hard to read

**Solutions**:
1. **Increase font size**: Settings > Overlay > Font Size (try 32 or 48)
2. **Change colors**:
   - Use high contrast: White text on black background
   - Or black text on white background
3. **Adjust opacity**: Increase background opacity for better contrast
4. **Enable text shadow**: Improves readability over any background
5. **Change font**: Try different font family (Arial, Helvetica, etc.)
6. **Increase overlay height**: More space for larger text

### Overlay Disappears in Fullscreen

**Problem**: Overlay not visible when app is fullscreen

**Solutions**:

**macOS**:
1. Grant accessibility permissions
2. Use "Top" position instead of "Bottom"
3. Try custom position
4. Use windowed mode instead of fullscreen

**Linux**:
1. Check window manager settings for always-on-top
2. Add window rule for OpenLiveCaption overlay
3. Use different desktop environment
4. Try X11 instead of Wayland

**Windows**:
1. Should work by default
2. Try running as administrator
3. Update graphics drivers

---

## Performance Issues

### High CPU Usage

**Problem**: Application uses too much CPU (>50%)

**Solutions**:
1. **Use smaller model**: Switch to "tiny" (fastest)
2. **Increase chunk duration**: Process less frequently (try 2.0 seconds)
3. **Disable translation**: Turn off if not needed
4. **Close other apps**: Free up CPU resources
5. **Check for updates**: Update to latest version
6. **Limit background processes**: Disable unnecessary startup programs

### High Memory Usage

**Problem**: Application uses too much RAM (>2GB)

**Solutions**:
1. **Use smaller model**:
   - tiny: ~500MB
   - base: ~1GB
   - small: ~2GB
   - medium: ~5GB
   - large: ~10GB
2. **Disable translation**: Saves ~500MB per language
3. **Restart application**: Clears memory leaks
4. **Close other apps**: Free up RAM
5. **Upgrade RAM**: Consider adding more RAM to system

### Slow Startup

**Problem**: Application takes long time to start (>30 seconds)

**Solutions**:
1. **First run is slower**: Model download takes time
2. **Use smaller model**: Loads faster
3. **Check disk speed**: Use SSD instead of HDD
4. **Disable antivirus**: Temporarily disable for testing
5. **Check startup programs**: Reduce system load
6. **Preload model**: Run once to cache model

### Application Freezes

**Problem**: Application becomes unresponsive

**Solutions**:
1. **Wait**: Large models may cause temporary freeze during loading
2. **Check CPU**: Ensure CPU is not overheating
3. **Check memory**: Ensure sufficient RAM available
4. **Force quit and restart**:
   - Windows: Task Manager > End Task
   - macOS: Force Quit (Cmd+Option+Esc)
   - Linux: `killall python`
5. **Check logs**: Look for error messages in console
6. **Update dependencies**: `pip install --upgrade -r requirements.txt`

### GPU Acceleration

**Problem**: Want to use GPU for faster transcription

**Solutions**:
1. **Check GPU compatibility**: NVIDIA GPU with CUDA support required
2. **Install CUDA toolkit**: Download from NVIDIA website
3. **Install PyTorch with CUDA**:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```
4. **Select CUDA in settings**: Settings > Transcription > Device > cuda
5. **Verify GPU usage**:
   ```bash
   nvidia-smi
   ```
6. **Troubleshoot**:
   - Update GPU drivers
   - Check CUDA version compatibility
   - Ensure sufficient VRAM (4GB+ recommended)

---

## Translation Issues

### Translation Not Working

**Problem**: Translation feature doesn't produce translated text

**Solutions**:
1. **Enable translation**: Settings > Transcription > Enable Translation
2. **Select target language**: Choose from dropdown
3. **Check internet**: Required for first-time model download
4. **Check disk space**: Translation models require ~500MB each
5. **Wait for download**: First translation may take time
6. **Check console**: Look for error messages
7. **Try different language**: Some languages may not be available

### Translation Model Download Fails

**Problem**: "Failed to download translation model" error

**Solutions**:
1. **Check internet connection**: Stable connection required
2. **Check firewall**: Allow Python to access internet
3. **Check disk space**: Ensure 1GB+ free space
4. **Clear cache**:
   - Windows: Delete `%USERPROFILE%\.cache\huggingface`
   - macOS/Linux: Delete `~/.cache/huggingface`
5. **Manual download**:
   ```bash
   python -c "from transformers import MarianMTModel; MarianMTModel.from_pretrained('Helsinki-NLP/opus-mt-en-yo')"
   ```

### Poor Translation Quality

**Problem**: Translations are inaccurate or nonsensical

**Solutions**:
1. **Improve transcription first**: Better input = better translation
2. **Use larger Whisper model**: More accurate transcription
3. **Set source language manually**: Helps translation model
4. **Check language pair**: Some language pairs work better than others
5. **Report issue**: Translation models are community-maintained

---

## Keyboard Shortcut Issues

### Global Shortcuts Not Working

**Problem**: `Ctrl+Shift+S` and `Ctrl+Shift+H` don't work

**Solutions**:
1. **Check conflicts**: Another app may be using the shortcut
2. **Grant permissions**:
   - **macOS**: System Preferences > Security & Privacy > Accessibility
   - **Linux**: May not work on Wayland
3. **Customize shortcuts**: Settings > Shortcuts > Change to different keys
4. **Use alternatives**:
   - System tray menu
   - Control window buttons
5. **Install keyboard library**: `pip install keyboard`
6. **Run as administrator** (Windows only)

**Linux/Wayland specific**:
- Global shortcuts may not work due to security restrictions
- Use system tray or control window instead
- Try X11 session instead of Wayland

### Shortcut Conflicts

**Problem**: Shortcut triggers wrong action or multiple actions

**Solutions**:
1. **Identify conflict**: Check which apps use the same shortcut
2. **Change in OpenLiveCaption**: Settings > Shortcuts
3. **Change in other app**: Modify conflicting application
4. **Use different modifiers**: Try `Alt` instead of `Ctrl`

---

## Export Issues

### Subtitle File Not Created

**Problem**: No SRT/VTT file generated after session

**Solutions**:
1. **Enable export**: Settings > Export > Enable Export
2. **Check output path**: Ensure path is writable
3. **Check permissions**: Ensure write access to directory
4. **Check disk space**: Ensure sufficient space available
5. **Stop captions properly**: Click "Stop Captions" to finalize file
6. **Check console**: Look for error messages

### Subtitle File Corrupted

**Problem**: SRT/VTT file is empty or malformed

**Solutions**:
1. **Stop captions properly**: Don't force quit application
2. **Check disk space**: Ensure space during writing
3. **Use different path**: Try saving to different location
4. **Check file permissions**: Ensure write access
5. **Restart application**: May fix file handle issues

### Timestamps Incorrect

**Problem**: Subtitle timestamps don't match audio

**Solutions**:
1. **Check system time**: Ensure system clock is correct
2. **Restart session**: Stop and start captions
3. **Report issue**: May be a bug

---

## Platform-Specific Issues

### Windows Issues

**WASAPI Loopback Not Available**:
- Update audio drivers
- Enable Stereo Mix in Recording Devices
- Run as administrator

**Antivirus Blocking**:
- Add OpenLiveCaption to antivirus exceptions
- Temporarily disable for testing

**DLL Errors**:
- Install Visual C++ Redistributable
- Update Windows

### macOS Issues

**BlackHole Not Working**:
- Reinstall BlackHole
- Restart Mac
- Check Audio MIDI Setup configuration
- See [docs/MACOS_SETUP.md](docs/MACOS_SETUP.md)

**Microphone Permission Denied**:
- System Preferences > Security & Privacy > Microphone
- Add and enable OpenLiveCaption

**Overlay Not Visible in Fullscreen**:
- Grant accessibility permissions
- Use windowed mode
- Try different overlay position

### Linux Issues

**PulseAudio Not Running**:
```bash
pulseaudio --start
```

**Permission Denied**:
```bash
sudo usermod -a -G audio $USER
# Log out and back in
```

**Wayland Limitations**:
- Global shortcuts may not work
- Try X11 session
- Use system tray instead

**Missing Dependencies**:
```bash
# Ubuntu/Debian
sudo apt install python3-pyqt6 portaudio19-dev

# Fedora
sudo dnf install python3-qt6 portaudio-devel

# Arch
sudo pacman -S python-pyqt6 portaudio
```

---

## Error Messages

### "Failed to initialize audio capture"

**Cause**: Audio device not accessible

**Solutions**:
- Check device is connected
- Grant microphone permissions
- Select different device
- Restart application

### "Model loading failed: Out of memory"

**Cause**: Insufficient RAM for model

**Solutions**:
- Use smaller model (tiny or base)
- Close other applications
- Restart computer
- Upgrade RAM

### "Transcription timeout"

**Cause**: Transcription taking too long

**Solutions**:
- Use smaller model
- Reduce chunk duration
- Enable GPU acceleration
- Check CPU usage

### "Configuration file corrupted"

**Cause**: Invalid JSON in config file

**Solutions**:
- Delete config file (will reset to defaults):
  - Windows: `%APPDATA%\OpenLiveCaption\config.json`
  - macOS: `~/Library/Application Support/OpenLiveCaption/config.json`
  - Linux: `~/.config/OpenLiveCaption/config.json`
- Restart application

### "Failed to create overlay window"

**Cause**: Display system issue

**Solutions**:
- Update graphics drivers
- Restart display manager (Linux)
- Check Qt installation: `pip install --upgrade PyQt6`
- Restart computer

---

## Getting Help

### Before Asking for Help

1. **Check this guide**: Search for your issue above
2. **Check console output**: Look for error messages
3. **Try basic troubleshooting**:
   - Restart application
   - Restart computer
   - Update dependencies
   - Delete config file
4. **Gather information**:
   - Operating system and version
   - Python version
   - Error messages
   - Steps to reproduce

### Where to Get Help

1. **Documentation**:
   - [README.md](README.md) - User guide
   - [QUICK_START.md](QUICK_START.md) - Quick start guide
   - [docs/](docs/) - Platform-specific guides

2. **GitHub Issues**:
   - Search existing issues: https://github.com/yourusername/OpenLiveCaption/issues
   - Create new issue with:
     - Clear description
     - Steps to reproduce
     - Error messages
     - System information

3. **GitHub Discussions**:
   - Ask questions: https://github.com/yourusername/OpenLiveCaption/discussions
   - Share tips and tricks
   - Request features

### Reporting Bugs

When reporting a bug, include:

1. **System Information**:
   ```bash
   python --version
   pip list | grep -E "PyQt6|whisper|torch"
   # On Windows: systeminfo | findstr /B /C:"OS"
   # On macOS: sw_vers
   # On Linux: lsb_release -a
   ```

2. **Error Messages**: Copy full error from console

3. **Steps to Reproduce**:
   - What you did
   - What you expected
   - What actually happened

4. **Configuration**: Attach config.json (remove sensitive data)

5. **Logs**: Include relevant console output

### Contributing Fixes

Found a solution? Help others:
1. Update this troubleshooting guide
2. Submit a pull request
3. Share in GitHub Discussions

---

## Diagnostic Commands

### Check Installation

```bash
# Python version
python --version

# Installed packages
pip list

# Check specific packages
pip show PyQt6 openai-whisper torch

# Test imports
python -c "import PyQt6; import whisper; import torch; print('All imports successful')"
```

### Check Audio System

**Windows**:
```bash
python -c "import pyaudiowpatch as pyaudio; p = pyaudio.PyAudio(); [print(f'{i}: {p.get_device_info_by_index(i)[\"name\"]}') for i in range(p.get_device_count())]"
```

**macOS/Linux**:
```bash
python -c "import sounddevice as sd; print(sd.query_devices())"
```

**Linux PulseAudio**:
```bash
pactl list sources short
pactl list sinks short
```

### Check GPU

```bash
# NVIDIA GPU
nvidia-smi

# PyTorch CUDA
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda}')"
```

### Check Configuration

```bash
# Windows
type %APPDATA%\OpenLiveCaption\config.json

# macOS/Linux
cat ~/Library/Application\ Support/OpenLiveCaption/config.json  # macOS
cat ~/.config/OpenLiveCaption/config.json  # Linux
```

---

**Still having issues?** Open an issue on [GitHub](https://github.com/yourusername/OpenLiveCaption/issues) with detailed information.
