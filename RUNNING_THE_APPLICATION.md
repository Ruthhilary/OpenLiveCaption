# Running OpenLiveCaption

## Quick Start

### Prerequisites

Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Running the Application

**Option 1: Using the main entry point**
```bash
python main.py
```

**Option 2: Using the application module directly**
```bash
python -m src.application
```

### First Run

On first run, the application will:
1. Create a configuration file in the platform-specific location:
   - Windows: `%APPDATA%\OpenLiveCaption\config.json`
   - macOS: `~/Library/Application Support/OpenLiveCaption/config.json`
   - Linux: `~/.config/OpenLiveCaption/config.json`

2. Load the Whisper model (default: "tiny")
   - First time may take a few moments to download the model
   - Subsequent runs will use the cached model

3. Show the control window and caption overlay

### Using the Application

1. **Select Audio Source:**
   - Choose from the "Audio Source" dropdown
   - Options include microphone and system audio (loopback) devices
   - On Windows, WASAPI loopback devices are marked as [Loopback]

2. **Configure Model:**
   - Select Whisper model size from "Model Size" dropdown
   - Smaller models (tiny, base) are faster but less accurate
   - Larger models (medium, large) are more accurate but slower

3. **Set Language:**
   - Choose "Auto-detect" for automatic language detection
   - Or select a specific language for better accuracy

4. **Start Captions:**
   - Click "Start Captions" button
   - Speak into your microphone or play audio
   - Captions will appear in the overlay window

5. **Stop Captions:**
   - Click "Stop Captions" button
   - Subtitles will be saved to `subtitles.srt` (configurable in settings)

### Keyboard Shortcuts

- **Ctrl+Shift+S**: Start/Stop captions
- **Ctrl+Shift+H**: Show/Hide overlay

*Note: Global keyboard shortcuts require the `keyboard` library. If not installed, shortcuts will only work when the control window has focus.*

### System Tray

The application minimizes to the system tray when you close the control window:
- Right-click the tray icon for quick access to controls
- Double-click to show the control window
- Select "Exit" from the tray menu to fully quit

### Caption Overlay

The caption overlay appears on top of all windows:
- **Position:** Configurable in settings (top, bottom, or custom)
- **Styling:** Font, size, colors, and opacity can be customized
- **Click-through:** The overlay is transparent to mouse clicks
- **Multi-monitor:** Works across multiple displays

### Settings

Click the "⚙ Settings" button to configure:
- **Audio:** Device selection, silence detection threshold
- **Transcription:** Model size, language, translation options
- **Overlay:** Position, font, colors, opacity, display mode
- **Export:** Subtitle format (SRT/VTT), output location
- **Shortcuts:** Customize keyboard shortcuts

### Troubleshooting

**No audio devices found:**
- Check that your microphone or audio device is connected
- On macOS, you may need to install BlackHole for system audio capture
- On Linux, ensure PulseAudio or PipeWire is running

**Captions not appearing:**
- Check that the overlay is not hidden (click "Show Overlay")
- Verify audio is being captured (check audio level indicator)
- Try speaking louder or adjusting microphone volume

**Model loading fails:**
- Ensure you have internet connection for first-time model download
- Check available disk space (models can be 100MB-1GB)
- Try a smaller model size if memory is limited

**Application crashes:**
- Check the console output for error messages
- Ensure all dependencies are installed correctly
- Try deleting the config file and restarting

### Platform-Specific Notes

**Windows:**
- WASAPI loopback support for system audio capture
- Works with Zoom, Teams, YouTube, and other applications

**macOS:**
- Requires BlackHole or similar virtual audio device for system audio
- Install from: https://github.com/ExistentialAudio/BlackHole

**Linux:**
- Uses PulseAudio monitor sources for system audio
- PipeWire is also supported
- May require additional permissions for audio access

### Exiting the Application

**From Control Window:**
- Close the window to minimize to tray
- Use tray menu → Exit to fully quit

**From Tray:**
- Right-click tray icon → Exit

**Keyboard:**
- Press Ctrl+C in the terminal (if running from command line)

### Configuration File

The configuration file is stored in JSON format and can be manually edited:

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
    "font_family": "Arial",
    "font_size": 24,
    "text_color": "#FFFFFF",
    "background_color": "#000000",
    "background_opacity": 0.7
  }
}
```

### Logs

Application logs are printed to the console with timestamps:
```
2026-02-10 12:00:00 - src.application - INFO - Application initialized successfully
2026-02-10 12:00:05 - src.application - INFO - Starting caption generation...
2026-02-10 12:00:10 - src.application - INFO - Transcribed: Hello world
```

Use these logs for debugging and troubleshooting.
