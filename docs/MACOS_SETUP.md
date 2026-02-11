# macOS Setup Guide for System Audio Capture

## Overview

On macOS, capturing system audio (audio from applications like Zoom, Teams, YouTube) requires a virtual audio device. This guide explains how to install and configure BlackHole for system audio capture with OpenLiveCaption.

## Why BlackHole is Needed

macOS does not provide built-in system audio loopback like Windows (WASAPI). To capture audio from applications, you need to route audio through a virtual audio device that can be monitored by OpenLiveCaption.

## Installing BlackHole

### Option 1: Homebrew (Recommended)

1. Open Terminal
2. Install Homebrew if not already installed:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

3. Install BlackHole:
   ```bash
   brew install blackhole-2ch
   ```

### Option 2: Manual Installation

1. Download BlackHole from the official website:
   - Visit: https://existential.audio/blackhole/
   - Download BlackHole 2ch (stereo) installer

2. Open the downloaded `.pkg` file

3. Follow the installation wizard

4. Restart your Mac (recommended)

## Configuring Audio Routing

After installing BlackHole, you need to configure macOS to route audio through it:

### Method 1: Multi-Output Device (Recommended)

This method allows you to hear audio while capturing it:

1. Open **Audio MIDI Setup** (Applications > Utilities > Audio MIDI Setup)

2. Click the **+** button at the bottom left and select **Create Multi-Output Device**

3. In the Multi-Output Device:
   - Check **Built-in Output** (or your speakers/headphones)
   - Check **BlackHole 2ch**
   - Set **Built-in Output** as the master device (right-click > Use This Device For Sound Output)

4. In **System Preferences > Sound > Output**, select the **Multi-Output Device**

5. In OpenLiveCaption, select **BlackHole 2ch** as the audio input device

### Method 2: Direct BlackHole Output (Silent Monitoring)

This method captures audio but you won't hear it:

1. In **System Preferences > Sound > Output**, select **BlackHole 2ch**

2. In OpenLiveCaption, select **BlackHole 2ch** as the audio input device

3. Audio will be captured but not played through speakers

### Method 3: Aggregate Device (Advanced)

For capturing both system audio and microphone simultaneously:

1. Open **Audio MIDI Setup**

2. Click the **+** button and select **Create Aggregate Device**

3. In the Aggregate Device:
   - Check **BlackHole 2ch** (for system audio)
   - Check **Built-in Microphone** (for microphone input)

4. In OpenLiveCaption, select the **Aggregate Device** as the audio input

5. OpenLiveCaption will capture audio from both sources

## Testing the Setup

### Test System Audio Capture

1. Configure audio routing using Method 1 above

2. Launch OpenLiveCaption

3. Select **BlackHole 2ch** as the audio input device

4. Start caption generation

5. Play a YouTube video or any audio

6. Verify that captions appear for the audio

### Test with Video Conferencing

#### Zoom

1. In Zoom settings:
   - Go to **Audio**
   - Set **Speaker** to **Multi-Output Device**
   - Set **Microphone** to your actual microphone

2. In OpenLiveCaption:
   - Select **BlackHole 2ch** as input
   - Start caption generation

3. Join a Zoom meeting and verify captions appear

#### Microsoft Teams

1. In Teams settings:
   - Go to **Devices**
   - Set **Speaker** to **Multi-Output Device**
   - Set **Microphone** to your actual microphone

2. In OpenLiveCaption:
   - Select **BlackHole 2ch** as input
   - Start caption generation

3. Join a Teams meeting and verify captions appear

## Fullscreen Application Support

OpenLiveCaption's overlay is designed to stay on top of fullscreen applications on macOS:

- The overlay uses `Qt.WindowStaysOnTopHint` to remain visible
- The overlay is configured as a `Qt.Tool` window to not appear in the Dock
- The overlay should remain visible over fullscreen presentations, videos, and meetings

### Testing Fullscreen Behavior

1. Start OpenLiveCaption with captions enabled

2. Open a fullscreen application:
   - Safari in fullscreen mode
   - PowerPoint presentation in fullscreen
   - Zoom in fullscreen mode

3. Verify the caption overlay remains visible

4. If the overlay is not visible, try:
   - Adjusting the overlay position in settings
   - Checking macOS System Preferences > Security & Privacy > Accessibility
   - Granting OpenLiveCaption accessibility permissions

## Troubleshooting

### BlackHole Not Appearing in Device List

1. Verify BlackHole is installed:
   ```bash
   ls /Library/Audio/Plug-Ins/HAL/
   ```
   You should see `BlackHole2ch.driver`

2. Restart your Mac

3. Open Audio MIDI Setup and verify BlackHole appears in the device list

### No Audio Being Captured

1. Verify audio routing:
   - Check System Preferences > Sound > Output
   - Ensure Multi-Output Device or BlackHole is selected

2. Check OpenLiveCaption settings:
   - Verify BlackHole 2ch is selected as input device
   - Check audio level indicator shows activity

3. Test with a simple audio source:
   - Play a YouTube video
   - Check if audio level indicator responds

### Can't Hear Audio

If using Method 1 (Multi-Output Device) and you can't hear audio:

1. Open Audio MIDI Setup

2. Select the Multi-Output Device

3. Verify both Built-in Output and BlackHole are checked

4. Verify Built-in Output is set as master device

5. Check volume levels in System Preferences > Sound

### Overlay Not Visible in Fullscreen

1. Grant accessibility permissions:
   - System Preferences > Security & Privacy > Accessibility
   - Add OpenLiveCaption to the list
   - Enable the checkbox

2. Try adjusting overlay position:
   - Use "Top" position instead of "Bottom"
   - Try custom position

3. Check if overlay is hidden:
   - Use keyboard shortcut (Ctrl+Shift+H) to toggle visibility
   - Check system tray menu

## Uninstalling BlackHole

If you need to remove BlackHole:

### Homebrew Installation

```bash
brew uninstall blackhole-2ch
```

### Manual Installation

1. Open Terminal

2. Run:
   ```bash
   sudo rm -rf /Library/Audio/Plug-Ins/HAL/BlackHole2ch.driver
   ```

3. Restart your Mac

## Additional Resources

- BlackHole Official Website: https://existential.audio/blackhole/
- BlackHole GitHub: https://github.com/ExistentialAudio/BlackHole
- macOS Audio MIDI Setup Guide: https://support.apple.com/guide/audio-midi-setup/

## Performance Notes

- BlackHole adds minimal latency (typically < 10ms)
- CPU usage is negligible
- Works with all audio sample rates
- Compatible with macOS 10.10 and later

## Security and Privacy

- BlackHole is open source and auditable
- No network access or data collection
- Runs entirely locally on your Mac
- Does not modify system audio drivers permanently
