# Platform-Specific Testing Checklist

Quick reference checklist for manual testing on each platform.

## Windows 10/11 Testing Checklist

**Platform:** Windows _____ (10/11)  
**Build:** _____________  
**Date:** _____________  
**Tester:** _____________

### Installation & Startup
- [ ] Installer runs without security warnings
- [ ] Application installs successfully
- [ ] Start menu entry created
- [ ] Application launches within 5 seconds
- [ ] System tray icon appears

### Audio Capture (WASAPI)
- [ ] WASAPI loopback device listed in dropdown
- [ ] System audio capture works (test with YouTube)
- [ ] Microphone capture works
- [ ] Device switching works without restart
- [ ] Audio quality is good

### Overlay
- [ ] Overlay stays on top of all windows
- [ ] Overlay is click-through
- [ ] Overlay works on multiple monitors
- [ ] Position is saved on restart

### Performance
- [ ] Tiny model: latency < 2 seconds
- [ ] Tiny model: memory < 500MB
- [ ] Base model: latency < 3 seconds
- [ ] Base model: memory < 1GB
- [ ] Startup time < 5 seconds

### Application Integration
- [ ] Works with Zoom
- [ ] Works with Microsoft Teams
- [ ] Works with YouTube
- [ ] Works with PowerPoint fullscreen

### Error Handling
- [ ] Handles device disconnection gracefully
- [ ] Shows clear error messages
- [ ] Recovers from errors without crashing

**Issues Found:**
```
[List any issues here]
```

**Overall Result:** [ ] PASS [ ] FAIL

---

## macOS 11+ Testing Checklist

**Platform:** macOS _____________  
**Chip:** [ ] Intel [ ] Apple Silicon  
**Date:** _____________  
**Tester:** _____________

### Installation & Startup
- [ ] DMG opens without issues
- [ ] Application installs to Applications folder
- [ ] No security warnings (if signed)
- [ ] Application launches within 5 seconds
- [ ] Menu bar icon appears
- [ ] Microphone permission requested

### Audio Capture (Core Audio)
- [ ] BlackHole device listed (if installed)
- [ ] System audio capture works with BlackHole
- [ ] Microphone capture works
- [ ] Device switching works without restart
- [ ] Audio quality is good

### Overlay
- [ ] Overlay stays on top of all windows
- [ ] Overlay works in fullscreen apps
- [ ] Overlay works with Mission Control
- [ ] Position is saved on restart

### Performance
- [ ] Tiny model: latency < 2 seconds
- [ ] Tiny model: memory < 500MB
- [ ] Base model: latency < 3 seconds
- [ ] Base model: memory < 1GB
- [ ] Startup time < 5 seconds
- [ ] (Apple Silicon) Runs natively, not through Rosetta

### Application Integration
- [ ] Works with Zoom
- [ ] Works with Microsoft Teams
- [ ] Works with YouTube
- [ ] Works with Keynote fullscreen

### Error Handling
- [ ] Handles device disconnection gracefully
- [ ] Shows clear error messages
- [ ] Recovers from errors without crashing

**Issues Found:**
```
[List any issues here]
```

**Overall Result:** [ ] PASS [ ] FAIL

---

## Ubuntu 20.04+ Testing Checklist

**Platform:** Ubuntu _____________  
**Desktop Environment:** _____________  
**Display Server:** [ ] X11 [ ] Wayland  
**Date:** _____________  
**Tester:** _____________

### Installation & Startup
- [ ] AppImage downloads successfully
- [ ] AppImage is executable
- [ ] Application launches within 5 seconds
- [ ] System tray icon appears (if supported)

### Audio Capture (PulseAudio/PipeWire)
- [ ] Monitor sources (*.monitor) listed
- [ ] System audio capture works
- [ ] Microphone capture works
- [ ] Device switching works without restart
- [ ] Audio quality is good
- [ ] Works with PipeWire (if applicable)

### Overlay
- [ ] Overlay stays on top of all windows
- [ ] Overlay works with window manager
- [ ] Overlay works across workspaces
- [ ] Position is saved on restart
- [ ] Works correctly on X11
- [ ] Works correctly on Wayland (if applicable)

### Performance
- [ ] Tiny model: latency < 2 seconds
- [ ] Tiny model: memory < 500MB
- [ ] Base model: latency < 3 seconds
- [ ] Base model: memory < 1GB
- [ ] Startup time < 5 seconds

### Application Integration
- [ ] Works with Zoom
- [ ] Works with Microsoft Teams (web or app)
- [ ] Works with YouTube
- [ ] Works with LibreOffice Impress fullscreen

### Error Handling
- [ ] Handles device disconnection gracefully
- [ ] Shows clear error messages
- [ ] Recovers from errors without crashing

**Issues Found:**
```
[List any issues here]
```

**Overall Result:** [ ] PASS [ ] FAIL

---

## Application Integration Testing

### Zoom Integration

**Platform:** _____________  
**Zoom Version:** _____________

- [ ] Captions appear for meeting audio (system audio capture)
- [ ] Captions appear for own speech (microphone capture)
- [ ] Captions work during screen sharing
- [ ] Overlay doesn't interfere with Zoom controls
- [ ] Captions are accurate
- [ ] No audio feedback or echo

**Issues:** _____________

### Microsoft Teams Integration

**Platform:** _____________  
**Teams Version:** _____________

- [ ] Captions appear for meeting audio (system audio capture)
- [ ] Captions appear for own speech (microphone capture)
- [ ] Captions work during screen sharing
- [ ] Overlay doesn't interfere with Teams controls
- [ ] Captions are accurate
- [ ] Works alongside Teams built-in captions

**Issues:** _____________

### YouTube Integration

**Platform:** _____________  
**Browser:** _____________

- [ ] Captions appear for video audio
- [ ] Captions are accurate
- [ ] Language auto-detection works
- [ ] Captions work in fullscreen mode
- [ ] Performance is acceptable

**Issues:** _____________

### FreeShow/Presentation Software Integration

**Platform:** _____________  
**Software:** _____________

- [ ] Captions appear during presentation
- [ ] Overlay visible in fullscreen mode
- [ ] Captions don't interfere with presentation
- [ ] Works on dual monitor setup
- [ ] Presenter can control captions

**Issues:** _____________

---

## Summary Report

### Test Coverage

| Platform | Tested | Pass | Fail | Notes |
|----------|--------|------|------|-------|
| Windows 10/11 | [ ] | [ ] | [ ] | |
| macOS 11+ | [ ] | [ ] | [ ] | |
| Ubuntu 20.04+ | [ ] | [ ] | [ ] | |

### Application Integration

| Application | Tested | Pass | Fail | Notes |
|-------------|--------|------|------|-------|
| Zoom | [ ] | [ ] | [ ] | |
| Microsoft Teams | [ ] | [ ] | [ ] | |
| YouTube | [ ] | [ ] | [ ] | |
| FreeShow/Presentations | [ ] | [ ] | [ ] | |

### Critical Issues

```
[List any critical issues that block release]
```

### Non-Critical Issues

```
[List any minor issues that can be addressed post-release]
```

### Recommendations

```
[Provide recommendations for improvements or next steps]
```

### Release Readiness

**Is the application ready for release?**

[ ] YES - All tests pass, no critical issues  
[ ] NO - Critical issues must be fixed first  
[ ] CONDITIONAL - Can release with known minor issues documented

**Justification:**
```
[Explain the release readiness decision]
```

---

**Testing Completed By:** _____________  
**Date:** _____________  
**Signature:** _____________
