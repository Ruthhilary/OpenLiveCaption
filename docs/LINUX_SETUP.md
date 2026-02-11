# Linux Setup Guide for System Audio Capture

## Overview

On Linux, capturing system audio (audio from applications like Zoom, Teams, YouTube) is supported through PulseAudio monitor sources or PipeWire loopback devices. This guide explains how to configure your Linux system for system audio capture with OpenLiveCaption.

## Audio System Detection

OpenLiveCaption automatically detects and works with:
- **PulseAudio** (most common on Ubuntu, Fedora, Debian)
- **PipeWire** (newer systems, Fedora 34+, Ubuntu 22.10+)
- **ALSA** (fallback for basic audio capture)

## PulseAudio Setup (Ubuntu, Debian, Fedora)

### Checking if PulseAudio is Running

```bash
pactl info
```

If PulseAudio is running, you'll see system information. If not, install it:

```bash
# Ubuntu/Debian
sudo apt install pulseaudio

# Fedora
sudo dnf install pulseaudio

# Arch Linux
sudo pacman -S pulseaudio
```

### Finding Monitor Sources

PulseAudio automatically creates monitor sources for each audio output device:

```bash
pactl list sources | grep -E "Name:|Description:"
```

Look for sources with "monitor" in the name, such as:
- `alsa_output.pci-0000_00_1f.3.analog-stereo.monitor`
- `Monitor of Built-in Audio Analog Stereo`

### Using Monitor Sources in OpenLiveCaption

1. Launch OpenLiveCaption

2. In the audio source dropdown, look for devices with "monitor" in the name

3. Select a monitor source (e.g., "Monitor of Built-in Audio Analog Stereo")

4. Start caption generation

5. Play audio from any application (YouTube, Zoom, etc.)

6. Verify captions appear

### Creating a Loopback Device (Alternative Method)

If you want to capture audio from a specific application:

```bash
# Load the loopback module
pactl load-module module-loopback
```

To make this permanent, add to `/etc/pulse/default.pa`:
```
load-module module-loopback
```

## PipeWire Setup (Fedora 34+, Ubuntu 22.10+)

### Checking if PipeWire is Running

```bash
pw-cli info
```

If PipeWire is running, you'll see system information.

### Finding Monitor/Loopback Devices

```bash
pw-cli list-objects | grep -A 5 "node.name"
```

Look for devices with "monitor" or "loopback" in the name.

### Using PipeWire Devices in OpenLiveCaption

1. Launch OpenLiveCaption

2. In the audio source dropdown, look for devices with "monitor" or "loopback" in the name

3. Select a monitor/loopback device

4. Start caption generation

5. Play audio from any application

6. Verify captions appear

### Creating a Virtual Loopback (Advanced)

Create a virtual loopback device with PipeWire:

```bash
pw-loopback -C alsa_output.pci-0000_00_1f.3.analog-stereo.monitor
```

## ALSA Setup (Fallback)

If neither PulseAudio nor PipeWire is available, you can use ALSA directly:

### Finding ALSA Devices

```bash
arecord -L
```

Look for devices like:
- `hw:0,0` (hardware device)
- `plughw:0,0` (plugin hardware device)
- `default` (default capture device)

### Configuring ALSA Loopback

1. Load the ALSA loopback module:
```bash
sudo modprobe snd-aloop
```

2. Make it permanent by adding to `/etc/modules`:
```
snd-aloop
```

3. The loopback device will appear as `hw:Loopback,1`

## Testing the Setup

### Test with YouTube

1. Open a web browser (Firefox, Chrome)

2. Play a YouTube video

3. In OpenLiveCaption:
   - Select a monitor source
   - Start caption generation
   - Verify captions appear for the video audio

### Test with Zoom

1. In Zoom settings:
   - Go to **Audio**
   - Set **Speaker** to your default output device
   - Set **Microphone** to your actual microphone

2. In OpenLiveCaption:
   - Select the monitor source for your speakers
   - Start caption generation

3. Join a Zoom meeting and verify captions appear

### Test with Microsoft Teams

1. In Teams settings:
   - Go to **Devices**
   - Set **Speaker** to your default output device
   - Set **Microphone** to your actual microphone

2. In OpenLiveCaption:
   - Select the monitor source for your speakers
   - Start caption generation

3. Join a Teams meeting and verify captions appear

## Desktop Environment Compatibility

OpenLiveCaption's overlay is designed to work across different Linux desktop environments:

### GNOME (Ubuntu, Fedora)

- The overlay uses X11/Wayland window flags to stay on top
- Works in both X11 and Wayland sessions
- May require granting accessibility permissions

### KDE Plasma

- The overlay stays on top of all windows
- Works with KWin compositor
- Supports both X11 and Wayland

### XFCE

- The overlay uses X11 window flags
- Stays on top of all windows
- Lightweight and efficient

### i3/Sway (Tiling Window Managers)

- The overlay appears as a floating window
- Configure window rules if needed to keep it floating
- Works with both X11 (i3) and Wayland (Sway)

## Troubleshooting

### No Monitor Sources Available

If you don't see any monitor sources:

1. Check if PulseAudio is running:
```bash
pulseaudio --check
echo $?  # Should output 0 if running
```

2. Restart PulseAudio:
```bash
pulseaudio -k
pulseaudio --start
```

3. Check for monitor sources again:
```bash
pactl list sources short
```

### No Audio Being Captured

1. Verify the monitor source is working:
```bash
# Record 5 seconds of audio from monitor source
parecord --device=alsa_output.pci-0000_00_1f.3.analog-stereo.monitor test.wav
# Play it back
paplay test.wav
```

2. Check OpenLiveCaption settings:
   - Verify correct monitor source is selected
   - Check audio level indicator shows activity

3. Verify audio is actually playing:
```bash
pactl list sink-inputs
```

### Permission Denied Errors

If you get permission errors accessing audio devices:

1. Add your user to the audio group:
```bash
sudo usermod -a -G audio $USER
```

2. Log out and log back in

3. Verify group membership:
```bash
groups | grep audio
```

### Overlay Not Visible

1. Check if overlay is hidden:
   - Use keyboard shortcut (Ctrl+Shift+H) to toggle
   - Check system tray menu

2. Try different overlay positions:
   - Top, Bottom, or Custom position

3. Check window manager settings:
   - Some tiling window managers may need configuration
   - Add window rules to keep overlay floating

### High CPU Usage

If audio capture uses too much CPU:

1. Increase chunk duration in settings (reduces processing frequency)

2. Use a smaller Whisper model (tiny or base)

3. Check for other audio processing conflicts:
```bash
# Check what's using audio
lsof /dev/snd/*
```

### Wayland-Specific Issues

On Wayland, some features may be limited:

1. Global keyboard shortcuts may not work
   - Use the control window or system tray instead

2. Overlay positioning may be restricted
   - Wayland compositors control window positioning

3. Screen capture permissions may be needed
   - Grant permissions in system settings

## Advanced Configuration

### Capturing Specific Application Audio

To capture audio from only one application:

1. Find the application's audio stream:
```bash
pactl list sink-inputs
```

2. Create a null sink:
```bash
pactl load-module module-null-sink sink_name=app_capture
```

3. Move the application's audio to the null sink:
```bash
pactl move-sink-input <stream-id> app_capture
```

4. In OpenLiveCaption, select "Monitor of app_capture"

### Mixing Multiple Audio Sources

To capture both system audio and microphone:

1. In OpenLiveCaption settings, enable multi-source capture

2. Select both:
   - Monitor source (for system audio)
   - Microphone device (for your voice)

3. Audio will be mixed automatically

### Low-Latency Configuration

For minimal latency:

1. Reduce PulseAudio buffer size in `/etc/pulse/daemon.conf`:
```
default-fragments = 2
default-fragment-size-msec = 5
```

2. Restart PulseAudio:
```bash
pulseaudio -k
pulseaudio --start
```

3. In OpenLiveCaption, use:
   - Chunk duration: 0.5 seconds
   - Whisper model: tiny (fastest)

## Uninstalling Audio Components

### Remove PulseAudio

```bash
# Ubuntu/Debian
sudo apt remove pulseaudio

# Fedora
sudo dnf remove pulseaudio
```

### Remove PipeWire

```bash
# Ubuntu/Debian
sudo apt remove pipewire

# Fedora
sudo dnf remove pipewire
```

### Remove ALSA Loopback

```bash
sudo modprobe -r snd-aloop
```

Remove from `/etc/modules` to prevent loading on boot.

## Additional Resources

- PulseAudio Documentation: https://www.freedesktop.org/wiki/Software/PulseAudio/
- PipeWire Documentation: https://pipewire.org/
- ALSA Documentation: https://www.alsa-project.org/
- Linux Audio Wiki: https://wiki.archlinux.org/title/PulseAudio

## Performance Notes

- Monitor sources add minimal latency (< 10ms)
- CPU usage depends on Whisper model size
- PipeWire generally has lower latency than PulseAudio
- ALSA has the lowest latency but requires more configuration

## Security and Privacy

- All audio processing happens locally
- No network access required for audio capture
- Audio is not stored unless export is enabled
- Monitor sources only capture system audio output, not microphone input (unless explicitly configured)
