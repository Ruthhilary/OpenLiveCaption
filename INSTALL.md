# OpenLiveCaption Installation Guide

**Get started in 3 easy steps!**

## 🚀 Quick Install (Windows)

### Step 1: Install Python

1. Download Python 3.10 or later from: https://www.python.org/downloads/
2. Run the installer
3. **IMPORTANT**: Check the box "Add Python to PATH"
4. Click "Install Now"

### Step 2: Download OpenLiveCaption

**Option A: Download ZIP**
1. Download the ZIP file
2. Extract to a folder (e.g., `C:\OpenLiveCaption`)

**Option B: Clone from GitHub**
```bash
git clone https://github.com/YOUR_USERNAME/OpenLiveCaption.git
cd OpenLiveCaption
```

### Step 3: Run the Application

**Easy Way** (Recommended):
- Double-click `START_OPENLIVECAPTION.bat`
- The script will automatically install dependencies and start the app

**Manual Way**:
```bash
# Open Command Prompt in the OpenLiveCaption folder
pip install -r requirements.txt
python Main.py
```

**That's it!** The application will launch with:
- A control window to start/stop captions
- A caption overlay that appears on top of everything
- A system tray icon for quick access

---

## 🍎 macOS Installation

### Step 1: Install Python

```bash
# Using Homebrew (recommended)
brew install python@3.10

# Or download from python.org
```

### Step 2: Install BlackHole (for system audio capture)

```bash
brew install blackhole-2ch
```

See [docs/MACOS_SETUP.md](docs/MACOS_SETUP.md) for detailed audio setup.

### Step 3: Install OpenLiveCaption

```bash
# Download and extract, then:
cd OpenLiveCaption
pip3 install -r requirements.txt
python3 Main.py
```

---

## 🐧 Linux Installation

### Step 1: Install Python and Dependencies

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip portaudio19-dev
```

**Fedora:**
```bash
sudo dnf install python3 python3-pip portaudio-devel
```

**Arch:**
```bash
sudo pacman -S python python-pip portaudio
```

### Step 2: Install OpenLiveCaption

```bash
cd OpenLiveCaption
pip3 install -r requirements.txt
python3 Main.py
```

See [docs/LINUX_SETUP.md](docs/LINUX_SETUP.md) for audio setup details.

---

## ✅ Verify Installation

After installation, you should see:

1. **Control Window**
   - Start/Stop buttons
   - Audio source dropdown
   - Model size selection
   - Language selection

2. **Caption Overlay**
   - Transparent window at bottom of screen
   - Will show captions when you start

3. **System Tray Icon**
   - Right-click for quick menu
   - Start/Stop, Settings, Exit

---

## 🎯 First Run

### 1. Model Download (First Time Only)

On first launch, Whisper will download the AI model:
- **tiny model**: ~75MB (1-2 minutes)
- **base model**: ~150MB (2-3 minutes)

This happens once. Subsequent launches are instant!

### 2. Select Audio Source

In the control window:
- **Microphone**: To caption your own speech
- **System Audio** (Windows): To caption computer audio
- **BlackHole** (macOS): To caption computer audio
- **Monitor** (Linux): To caption computer audio

### 3. Start Captions

1. Click "Start Captions"
2. Speak or play audio
3. Watch captions appear in real-time!

---

## 🔧 Troubleshooting

### "Python not found"

**Windows:**
- Reinstall Python
- Make sure "Add Python to PATH" is checked
- Restart Command Prompt

**macOS/Linux:**
- Use `python3` instead of `python`
- Use `pip3` instead of `pip`

### "Module not found" errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### "No audio devices found"

**Windows:**
- Check Device Manager for audio devices
- Update audio drivers

**macOS:**
- Install BlackHole: `brew install blackhole-2ch`
- See [docs/MACOS_SETUP.md](docs/MACOS_SETUP.md)

**Linux:**
- Check PulseAudio: `pactl list sources`
- See [docs/LINUX_SETUP.md](docs/LINUX_SETUP.md)

### Application won't start

1. Check Python version: `python --version` (should be 3.8+)
2. Check dependencies: `pip list`
3. Try running with: `python Main.py` to see error messages
4. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more help

---

## 📚 Next Steps

After installation:

1. **Read the Quick Start**: [QUICK_START.md](QUICK_START.md)
2. **Explore Features**: Try different languages, translation, export
3. **Customize**: Settings → Adjust font, colors, position
4. **Learn Shortcuts**: [KEYBOARD_SHORTCUTS.md](KEYBOARD_SHORTCUTS.md)

---

## 🆘 Need Help?

- **Documentation**: Check the `docs/` folder
- **Troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Issues**: Report on GitHub Issues
- **Questions**: Ask in GitHub Discussions

---

## 🎉 You're All Set!

OpenLiveCaption is now installed and ready to use!

**Quick command to start**: `python Main.py`

Or just double-click: `START_OPENLIVECAPTION.bat` (Windows)

Enjoy real-time captions in 47 languages! 🌍

---

**Made with ❤️ for accessibility and inclusion**

