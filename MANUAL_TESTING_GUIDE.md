# Manual Testing Guide for OpenLiveCaption

This guide provides comprehensive manual testing procedures for OpenLiveCaption across all supported platforms (Windows, macOS, Linux) and with various applications (Zoom, Teams, YouTube, FreeShow).

**Requirements Validated:**
- 12.1: Windows 10/11 compatibility
- 12.2: macOS 11+ compatibility  
- 12.3: Ubuntu 20.04+ compatibility
- 4.1: Zoom/Teams/Meet integration
- 4.2: Fullscreen presentation support
- 4.3: Streaming platform support

---

## Table of Contents

1. [Pre-Testing Setup](#pre-testing-setup)
2. [Windows 10/11 Testing](#windows-1011-testing)
3. [macOS 11+ Testing](#macos-11-testing)
4. [Ubuntu 20.04+ Testing](#ubuntu-2004-testing)
5. [Application Integration Testing](#application-integration-testing)
6. [Test Results Template](#test-results-template)

---

## Pre-Testing Setup

### General Requirements

Before starting manual testing, ensure you have:

- [ ] OpenLiveCaption installed on the target platform
- [ ] Test audio files or ability to generate test speech
- [ ] Internet connection for downloading Whisper models
- [ ] At least 2GB free RAM
- [ ] At least 1GB free disk space

### Test Applications

Install the following applications for integration testing:

- [ ] Zoom (latest version)
- [ ] Microsoft Teams (latest version)
- [ ] Web browser (Chrome/Firefox/Edge) for YouTube and Google Meet
- [ ] FreeShow (if testing presentation software)
- [ ] PowerPoint or Keynote (for fullscreen presentation testing)

---

## Windows 10/11 Testing

**Requirement: 12.1 - Application runs on Windows 10 and later**

### Platform Information

- OS Version: ________________
- Build Number: ________________
- Architecture: [ ] x64 [ ] ARM64

### Installation Testing

1. **Download and Install**
   - [ ] Download installer from release page
   - [ ] Run installer (should not show security warnings if signed)
   - [ ] Verify installation completes without errors
   - [ ] Check Start Menu entry created
   - [ ] Check Desktop shortcut created (if option selected)

2. **First Launch**
   - [ ] Launch application from Start Menu
   - [ ] Verify application starts within 5 seconds
   - [ ] Check system tray icon appears
   - [ ] Verify control window displays correctly

### Audio Capture Testing (Windows WASAPI)

**Requirement: 12.4 - Use WASAPI for system audio capture**

1. **System Audio Capture**
   - [ ] Open audio source dropdown in control window
   - [ ] Verify "System Audio (WASAPI Loopback)" device is listed
   - [ ] Select system audio device
   - [ ] Play audio from any application (e.g., YouTube in browser)
   - [ ] Click "Start Captions"
   - [ ] Verify captions appear for the audio being played
   - [ ] Verify captions are accurate

2. **Microphone Capture**
   - [ ] Select microphone device from dropdown
   - [ ] Click "Start Captions"
   - [ ] Speak into microphone
   - [ ] Verify captions appear for spoken words
   - [ ] Verify captions are accurate

3. **Device Switching**
   - [ ] Start captions with system audio
   - [ ] Switch to microphone while running
   - [ ] Verify captions switch to microphone input without crash
   - [ ] Switch back to system audio
   - [ ] Verify captions switch back successfully

### Overlay Testing

1. **Always-On-Top Behavior**
   - [ ] Start captions
   - [ ] Open various applications (browser, notepad, file explorer)
   - [ ] Verify overlay stays on top of all applications
   - [ ] Maximize an application window
   - [ ] Verify overlay still visible on top

2. **Click-Through Transparency**
   - [ ] Position overlay over a button in another application
   - [ ] Try to click the button through the overlay
   - [ ] Verify clicks pass through to underlying application

3. **Multi-Monitor Support**
   - [ ] If multiple monitors available:
     - [ ] Move overlay to second monitor
     - [ ] Verify overlay displays correctly
     - [ ] Verify position is saved when application restarts

### Performance Testing

1. **Transcription Latency**
   - [ ] Use "tiny" model
   - [ ] Speak a sentence
   - [ ] Measure time from end of speech to caption appearance
   - [ ] Verify latency is under 2 seconds
   - [ ] Repeat with "base" model
   - [ ] Verify latency is still reasonable (under 3 seconds)

2. **Memory Usage**
   - [ ] Open Task Manager
   - [ ] Start captions with "tiny" model
   - [ ] Check memory usage (should be under 500MB)
   - [ ] Switch to "base" model
   - [ ] Check memory usage (should be under 1GB)

### Error Handling

1. **Device Disconnection**
   - [ ] Start captions with USB microphone
   - [ ] Unplug microphone while running
   - [ ] Verify error notification appears
   - [ ] Verify application doesn't crash
   - [ ] Plug microphone back in
   - [ ] Verify device appears in dropdown again

2. **Model Loading Failure**
   - [ ] Disconnect internet
   - [ ] Try to load a model not yet downloaded
   - [ ] Verify clear error message appears
   - [ ] Reconnect internet
   - [ ] Retry model loading
   - [ ] Verify model loads successfully

---

## macOS 11+ Testing

**Requirement: 12.2 - Application runs on macOS 11 (Big Sur) and later**

### Platform Information

- macOS Version: ________________
- Chip: [ ] Intel [ ] Apple Silicon (M1/M2/M3)

### Installation Testing

1. **Download and Install**
   - [ ] Download DMG from release page
   - [ ] Open DMG file
   - [ ] Drag application to Applications folder
   - [ ] Verify no security warnings (if signed and notarized)
   - [ ] If security warning appears, verify instructions are clear

2. **First Launch**
   - [ ] Launch application from Applications folder
   - [ ] Grant microphone permission when prompted
   - [ ] Verify application starts within 5 seconds
   - [ ] Check menu bar icon appears
   - [ ] Verify control window displays correctly

### Audio Capture Testing (macOS Core Audio)

**Requirement: 12.5 - Use Core Audio for system audio capture**

1. **System Audio Capture (with BlackHole)**
   - [ ] Install BlackHole virtual audio device (if not installed)
   - [ ] Configure Audio MIDI Setup to route audio through BlackHole
   - [ ] Open audio source dropdown
   - [ ] Verify BlackHole device is listed
   - [ ] Select BlackHole device
   - [ ] Play audio from any application
   - [ ] Click "Start Captions"
   - [ ] Verify captions appear for the audio being played

2. **Microphone Capture**
   - [ ] Select built-in microphone from dropdown
   - [ ] Click "Start Captions"
   - [ ] Speak into microphone
   - [ ] Verify captions appear for spoken words
   - [ ] Verify captions are accurate

### Overlay Testing

1. **Fullscreen Application Support**
   - [ ] Start captions
   - [ ] Open PowerPoint or Keynote
   - [ ] Enter fullscreen presentation mode
   - [ ] Verify overlay remains visible on top of fullscreen presentation
   - [ ] Exit fullscreen
   - [ ] Verify overlay still works correctly

2. **Mission Control Compatibility**
   - [ ] Start captions
   - [ ] Open Mission Control (F3 or swipe up with 3 fingers)
   - [ ] Verify overlay behavior is appropriate
   - [ ] Switch between desktops
   - [ ] Verify overlay follows or stays on correct desktop

### Performance Testing

1. **Apple Silicon Optimization**
   - [ ] If on Apple Silicon (M1/M2/M3):
     - [ ] Verify application runs natively (not through Rosetta)
     - [ ] Check Activity Monitor for architecture
     - [ ] Verify performance is good (low CPU usage)

2. **Memory Usage**
   - [ ] Open Activity Monitor
   - [ ] Start captions with "tiny" model
   - [ ] Check memory usage (should be under 500MB)
   - [ ] Switch to "base" model
   - [ ] Check memory usage (should be under 1GB)

---

## Ubuntu 20.04+ Testing

**Requirement: 12.3 - Application runs on Ubuntu 20.04 and later**

### Platform Information

- Ubuntu Version: ________________
- Desktop Environment: [ ] GNOME [ ] KDE [ ] XFCE [ ] Other: ________

### Installation Testing

1. **Download and Install**
   - [ ] Download AppImage from release page
   - [ ] Make AppImage executable: `chmod +x OpenLiveCaption.AppImage`
   - [ ] Run AppImage: `./OpenLiveCaption.AppImage`
   - [ ] Verify application starts without errors

2. **First Launch**
   - [ ] Launch application
   - [ ] Verify application starts within 5 seconds
   - [ ] Check system tray icon appears (if supported by DE)
   - [ ] Verify control window displays correctly

### Audio Capture Testing (PulseAudio/PipeWire)

**Requirement: 12.6 - Use PulseAudio or PipeWire for system audio capture**

1. **System Audio Capture**
   - [ ] Open audio source dropdown
   - [ ] Verify monitor sources (*.monitor) are listed
   - [ ] Select a monitor source
   - [ ] Play audio from any application
   - [ ] Click "Start Captions"
   - [ ] Verify captions appear for the audio being played

2. **Microphone Capture**
   - [ ] Select microphone device from dropdown
   - [ ] Click "Start Captions"
   - [ ] Speak into microphone
   - [ ] Verify captions appear for spoken words
   - [ ] Verify captions are accurate

3. **PipeWire Support**
   - [ ] If using PipeWire instead of PulseAudio:
     - [ ] Verify audio devices are detected correctly
     - [ ] Verify audio capture works as expected
     - [ ] Note any differences from PulseAudio behavior

### Overlay Testing

1. **Window Manager Compatibility**
   - [ ] Start captions
   - [ ] Open various applications
   - [ ] Verify overlay stays on top
   - [ ] Test with different workspaces/virtual desktops
   - [ ] Verify overlay behavior is appropriate

2. **Wayland vs X11**
   - [ ] Note if running Wayland or X11: ________________
   - [ ] Verify overlay works correctly on current display server
   - [ ] If possible, test on both Wayland and X11
   - [ ] Note any differences in behavior

---

## Application Integration Testing

### Zoom Testing

**Requirement: 4.1 - Works with Zoom**

1. **Setup**
   - [ ] Install Zoom
   - [ ] Join a test meeting or start a personal meeting room
   - [ ] Enable computer audio

2. **System Audio Capture**
   - [ ] Configure OpenLiveCaption to capture system audio
   - [ ] Start captions
   - [ ] Have someone speak in the Zoom meeting
   - [ ] Verify captions appear for Zoom audio
   - [ ] Verify captions are accurate

3. **Microphone Capture**
   - [ ] Configure OpenLiveCaption to capture microphone
   - [ ] Start captions
   - [ ] Speak in the Zoom meeting
   - [ ] Verify captions appear for your speech
   - [ ] Verify captions are accurate

4. **Screen Sharing Compatibility**
   - [ ] Start screen sharing in Zoom
   - [ ] Verify overlay is visible in shared screen (or not, depending on preference)
   - [ ] Verify captions continue to work during screen sharing

### Microsoft Teams Testing

**Requirement: 4.1 - Works with Microsoft Teams**

1. **Setup**
   - [ ] Install Microsoft Teams
   - [ ] Join a test meeting

2. **System Audio Capture**
   - [ ] Configure OpenLiveCaption to capture system audio
   - [ ] Start captions
   - [ ] Have someone speak in the Teams meeting
   - [ ] Verify captions appear for Teams audio
   - [ ] Verify captions are accurate

3. **Integration with Teams Captions**
   - [ ] Enable Teams built-in captions
   - [ ] Verify OpenLiveCaption captions don't conflict
   - [ ] Compare accuracy between Teams and OpenLiveCaption captions

### YouTube Testing

**Requirement: 4.3 - Works with YouTube**

1. **Setup**
   - [ ] Open YouTube in web browser
   - [ ] Find a video with clear speech (e.g., news, tutorial)

2. **System Audio Capture**
   - [ ] Configure OpenLiveCaption to capture system audio
   - [ ] Start captions
   - [ ] Play YouTube video
   - [ ] Verify captions appear for video audio
   - [ ] Compare with YouTube's auto-generated captions
   - [ ] Note accuracy differences

3. **Multiple Languages**
   - [ ] Play videos in different languages
   - [ ] Verify language auto-detection works
   - [ ] Test manual language override if needed

### FreeShow Testing

**Requirement: 4.2 - Works with presentation software**

1. **Setup**
   - [ ] Install FreeShow
   - [ ] Create a test presentation

2. **Fullscreen Mode**
   - [ ] Start FreeShow presentation in fullscreen
   - [ ] Configure OpenLiveCaption to capture microphone
   - [ ] Start captions
   - [ ] Speak while presenting
   - [ ] Verify captions appear on top of fullscreen presentation
   - [ ] Verify captions don't interfere with presentation controls

3. **Dual Monitor Setup**
   - [ ] If dual monitors available:
     - [ ] Display presentation on one monitor
     - [ ] Position captions on presentation monitor
     - [ ] Verify captions are visible to audience
     - [ ] Verify presenter can control captions from other monitor

---

## Test Results Template

Use this template to document your test results:

```markdown
# OpenLiveCaption Manual Test Results

**Date:** ________________
**Tester:** ________________
**Version:** ________________

## Platform Information

- **OS:** ________________
- **Version:** ________________
- **Architecture:** ________________

## Test Results Summary

| Test Category | Pass | Fail | Notes |
|--------------|------|------|-------|
| Installation | [ ] | [ ] | |
| Audio Capture | [ ] | [ ] | |
| Overlay Display | [ ] | [ ] | |
| Performance | [ ] | [ ] | |
| Error Handling | [ ] | [ ] | |
| Zoom Integration | [ ] | [ ] | |
| Teams Integration | [ ] | [ ] | |
| YouTube Integration | [ ] | [ ] | |
| FreeShow Integration | [ ] | [ ] | |

## Detailed Results

### Installation
[Describe installation experience, any issues encountered]

### Audio Capture
[Describe audio capture testing, quality of transcriptions]

### Overlay Display
[Describe overlay behavior, any visual issues]

### Performance
[Report latency measurements, memory usage, startup time]

### Error Handling
[Describe how application handled errors, recovery behavior]

### Application Integration
[Describe integration testing with Zoom, Teams, YouTube, FreeShow]

## Issues Found

1. **Issue Title**
   - Severity: [ ] Critical [ ] Major [ ] Minor
   - Description: 
   - Steps to Reproduce:
   - Expected Behavior:
   - Actual Behavior:

## Recommendations

[Any recommendations for improvements or fixes]

## Overall Assessment

[ ] Ready for release
[ ] Needs minor fixes
[ ] Needs major fixes

**Comments:**
```

---

## Automated Test Execution

For automated verification of manual test scenarios, you can run:

```bash
# Run all tests
python -m pytest tests/ -v

# Run performance tests specifically
python -m pytest tests/test_performance.py -v -s

# Run integration tests
python -m pytest tests/test_integration.py -v

# Run platform-specific tests
python -m pytest tests/test_audio/test_windows_audio.py -v  # Windows
python -m pytest tests/test_audio/test_macos_audio.py -v    # macOS
python -m pytest tests/test_audio/test_linux_audio.py -v    # Linux
```

---

## Notes for Testers

1. **Document Everything**: Take screenshots of any issues or unexpected behavior
2. **Test Thoroughly**: Don't skip steps even if they seem redundant
3. **Report Issues**: Use the issue template above to document any problems
4. **Compare Platforms**: Note any differences in behavior between platforms
5. **Real-World Usage**: Try to use the application in real scenarios (actual meetings, presentations)

---

## Completion Checklist

Before marking manual testing as complete, ensure:

- [ ] All three platforms tested (Windows, macOS, Linux)
- [ ] All four applications tested (Zoom, Teams, YouTube, FreeShow)
- [ ] All critical features verified working
- [ ] Performance requirements validated
- [ ] All issues documented
- [ ] Test results documented using template
- [ ] Recommendations provided for any issues found

---

**End of Manual Testing Guide**
