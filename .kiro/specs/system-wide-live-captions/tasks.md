# Implementation Plan: System-Wide Live Captions

## Overview

This implementation plan transforms OpenLiveCaption from a webcam-based subtitle display into a system-wide overlay application. The implementation follows a phased approach, building core functionality first (overlay, audio capture, transcription) before adding advanced features (translation, export, packaging).

The plan prioritizes getting a working MVP quickly, with optional tasks marked for comprehensive testing and polish.

## Tasks

- [x] 1. Set up project structure and dependencies
  - Create new project directory structure separating UI, audio, transcription, and config modules
  - Update requirements.txt with PyQt6, PyAudioWPatch, hypothesis for testing
  - Create configuration module with JSON-based settings management
  - Set up pytest and hypothesis for testing framework
  - _Requirements: 6.10, 5.4_

- [x] 2. Implement configuration management system
  - [x] 2.1 Create Config dataclasses for all settings (AudioConfig, TranscriptionConfig, OverlayConfig, ExportConfig, ShortcutConfig)
    - Define dataclass structures matching design specifications
    - Include default values for all settings
    - _Requirements: 6.10_
  
  - [x] 2.2 Implement ConfigManager class with load/save methods
    - Implement JSON serialization/deserialization
    - Handle platform-specific config file locations (Windows: %APPDATA%, macOS: ~/Library/Application Support, Linux: ~/.config)
    - Create config directory if it doesn't exist
    - _Requirements: 6.10_
  
  - [x] 2.3 Write property test for configuration round-trip

    - **Property 3: Overlay position persistence**
    - **Property 25: Preferences persistence**
    - **Validates: Requirements 1.4, 6.10**
  
  - [x] 2.4 Write unit tests for config file corruption handling

    - Test loading corrupted JSON
    - Test missing config file
    - Test invalid config values
    - _Requirements: 6.10_

- [x] 3. Implement Caption Overlay window
  - [x] 3.1 Create CaptionOverlay class inheriting from QWidget
    - Set up PyQt6 window with frameless, always-on-top, click-through flags
    - Implement transparent background with configurable opacity
    - Create text rendering with QLabel or QPainter
    - _Requirements: 1.1, 1.2, 1.3, 1.5_
  
  - [x] 3.2 Implement caption display logic
    - Add text wrapping at word boundaries
    - Enforce maximum 3 lines display
    - Implement scroll and replace modes
    - Add auto-clear timeout functionality
    - _Requirements: 7.2, 7.3, 7.4, 7.8_
  
  - [x] 3.3 Implement styling configuration
    - Add methods to set font family and size
    - Add methods to set text and background colors
    - Add method to set background opacity
    - Apply text shadow/outline for readability
    - _Requirements: 7.1, 7.5, 7.6, 7.7_
  
  - [x] 3.4 Implement position management
    - Add methods for top, bottom, and custom positioning
    - Handle multi-monitor setups
    - Save position changes to configuration
    - _Requirements: 1.4, 6.7_
  
  - [x] 3.5 Write property tests for overlay behavior

    - **Property 1: Overlay always-on-top behavior**
    - **Property 2: Overlay click-through transparency**
    - **Property 4: Overlay opacity configuration**
    - **Property 5: Font configuration**
    - **Property 6: Text wrapping at word boundaries**
    - **Property 7: Maximum three lines display**
    - **Property 8: Scroll and replace modes**
    - **Property 9: Color configuration**
    - **Property 10: Auto-clear timeout**
    - **Validates: Requirements 1.1, 1.2, 1.3, 1.5, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.8**

- [x] 4. Checkpoint - Test overlay functionality
  - Manually test overlay appears on top of other applications
  - Test click-through behavior
  - Test text display with various lengths
  - Ensure all tests pass, ask the user if questions arise

- [x] 5. Implement Audio Capture Engine
  - [x] 5.1 Create AudioCaptureEngine class with device enumeration
    - Implement list_devices() to enumerate audio input and loopback devices
    - Use PyAudioWPatch for Windows WASAPI loopback support
    - Use sounddevice for macOS and Linux
    - _Requirements: 2.1, 2.2, 12.4, 12.5, 12.6_
  
  - [x] 5.2 Implement audio capture with callback
    - Implement start_capture() with audio callback
    - Configure for 16kHz sample rate, float32 format
    - Process audio in 1-second chunks
    - Implement stop_capture() to cleanly stop audio stream
    - _Requirements: 2.1, 2.2, 3.1_
  
  - [x] 5.3 Implement device switching and multi-source capture
    - Add set_device() method to switch devices without restart
    - Implement simultaneous capture from multiple sources with audio mixing
    - _Requirements: 2.3, 2.4_
  
  - [x] 5.4 Implement Voice Activity Detection (VAD)
    - Add get_audio_level() method to measure audio amplitude
    - Implement pause on silence when audio below threshold for configured duration
    - _Requirements: 2.5_
  
  - [x] 5.5 Implement error handling and recovery
    - Handle device disconnection gracefully
    - Implement automatic reconnection attempts
    - Display error notifications for capture failures
    - _Requirements: 2.6, 9.1, 9.5_
  
  - [x] 5.6 Write property tests for audio capture

    - **Property 11: Audio device switching**
    - **Property 12: Simultaneous multi-source capture**
    - **Property 13: Pause on silence**
    - **Property 14: Device disconnection recovery**
    - **Property 15: Audio capture failure recovery**
    - **Validates: Requirements 2.3, 2.4, 2.5, 2.6, 9.1**

- [x] 6. Implement Transcription Engine
  - [x] 6.1 Create TranscriptionEngine class with Whisper integration
    - Reuse Whisper model loading from existing Main.py
    - Support configurable model sizes (tiny, base, small, medium, large)
    - Default to CPU device for compatibility
    - _Requirements: 3.1, 3.3, 8.3_
  
  - [x] 6.2 Implement transcription with overlapping chunks
    - Process audio in 1-second chunks with 0.5-second overlap
    - Maintain audio buffer for overlap
    - Return TranscriptionResult with text, language, confidence, timestamps
    - _Requirements: 3.1, 3.7_
  
  - [x] 6.3 Implement model switching and language configuration
    - Add change_model() method to switch Whisper models without restart
    - Support auto-detect and manual language selection
    - _Requirements: 3.4, 3.5, 3.6_
  
  - [x] 6.4 Implement error handling
    - Handle transcription failures gracefully
    - Log errors and continue processing subsequent audio
    - Handle model loading failures with clear error messages
    - _Requirements: 9.2, 9.3_
  
  - [x] 6.5 Write property tests for transcription


    - **Property 16: All Whisper model sizes supported**
    - **Property 17: Model switching without restart**
    - **Property 18: Manual language override**
    - **Property 19: Overlapping chunk processing**
    - **Property 20: Continue after transcription errors**
    - **Validates: Requirements 3.3, 3.4, 3.6, 3.7, 9.2**

- [x] 7. Integrate Translation Engine
  - [x] 7.1 Create TranslationEngine class with MarianMT
    - Reuse translation logic from existing Main.py
    - Implement lazy loading of translation models
    - Support Yoruba and Twi languages (existing functionality)
    - _Requirements: 10.1, 10.3_
  
  - [x] 7.2 Implement translation caching and dual-language display
    - Cache loaded translation models to avoid re-downloading
    - Support displaying both original and translated text
    - _Requirements: 10.4, 10.5_
  
  - [x] 7.3 Write property tests for translation

    - **Property 21: Translation when enabled**
    - **Property 22: Translation model caching**
    - **Validates: Requirements 10.1, 10.5**

- [x] 8. Checkpoint - Test audio and transcription pipeline
  - Test audio capture from microphone
  - Test transcription with different model sizes
  - Test translation functionality
  - Ensure all tests pass, ask the user if questions arise

- [x] 9. Implement Control Interface
  - [x] 9.1 Create ControlWindow class with main UI
    - Design main window layout with start/stop buttons
    - Add dropdowns for audio source, model size, language selection
    - Add buttons for settings and show/hide overlay
    - Display current status (running/stopped)
    - _Requirements: 6.1, 6.4, 6.5, 6.6, 6.7_
  
  - [x] 9.2 Implement system tray integration
    - Create system tray icon with status indicator
    - Add right-click menu with start/stop, show/hide, settings, exit options
    - Implement minimize to tray on window close
    - _Requirements: 6.2, 6.3, 6.9_
  
  - [x] 9.3 Create Settings dialog
    - Create tabbed settings dialog (Audio, Transcription, Overlay, Export, Shortcuts)
    - Implement UI controls for all configuration options
    - Save settings to ConfigManager on apply
    - _Requirements: 6.4, 6.5, 6.6, 6.7_
  
  - [x] 9.4 Implement keyboard shortcuts
    - Add global hotkey support for start/stop (Ctrl+Shift+S)
    - Add global hotkey for show/hide overlay (Ctrl+Shift+H)
    - Make shortcuts configurable in settings
    - _Requirements: 6.8_
  
  - [x] 9.5 Write property tests for control interface

    - **Property 23: Keyboard shortcuts trigger actions**
    - **Property 24: Minimize to tray on close**
    - **Validates: Requirements 6.8, 6.9**
  
  - [x] 9.6 Write unit tests for UI components

    - Test button existence and functionality
    - Test system tray menu items
    - Test settings dialog controls
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7_

- [x] 10. Implement Subtitle Exporter
  - [x] 10.1 Create SubtitleExporter class
    - Implement SRT format export with timestamps
    - Implement VTT format export
    - Support configurable output file location
    - _Requirements: 11.1, 11.4, 11.2_
  
  - [x] 10.2 Implement file finalization and dual-language export
    - Properly close and finalize subtitle files on session end
    - Support exporting both original and translated text when translation enabled
    - _Requirements: 11.3, 11.5_
  
  - [x] 10.3 Write property tests for subtitle export

    - **Property 26: SRT export round-trip**
    - **Property 27: File finalization on session end**
    - **Property 28: VTT format support**
    - **Property 29: Dual-language export**
    - **Validates: Requirements 11.1, 11.3, 11.4, 11.5**

- [x] 11. Wire all components together
  - [x] 11.1 Create main application class
    - Instantiate all components (AudioCaptureEngine, TranscriptionEngine, TranslationEngine, CaptionOverlay, ControlWindow, SubtitleExporter)
    - Connect audio capture callback to transcription engine
    - Connect transcription results to overlay display
    - Connect transcription results to subtitle exporter
    - _Requirements: All_
  
  - [x] 11.2 Implement application lifecycle
    - Handle application startup and initialization
    - Load configuration on startup
    - Handle graceful shutdown (stop capture, finalize exports, save config)
    - _Requirements: 6.10, 11.3_
  
  - [x] 11.3 Implement error propagation and recovery
    - Connect error handlers across components
    - Implement overlay recreation on unexpected close
    - Handle device change notifications
    - _Requirements: 9.4, 9.5_
  
  - [x] 11.4 Write integration tests

    - Test end-to-end flow: audio → transcription → display → export
    - Test error recovery across components
    - Test configuration persistence across restart
    - _Requirements: All_

- [x] 12. Checkpoint - Test complete application
  - Test full workflow from audio capture to caption display
  - Test all UI controls and settings
  - Test error handling and recovery
  - Ensure all tests pass, ask the user if questions arise

- [x] 13. Implement platform-specific optimizations
  - [x] 13.1 Add Windows-specific audio capture
    - Verify PyAudioWPatch WASAPI loopback works correctly
    - Test with Zoom, Teams, YouTube on Windows
    - _Requirements: 12.4, 4.1, 4.3_
  
  - [x] 13.2 Add macOS-specific audio capture
    - Document BlackHole installation for system audio capture
    - Test with Zoom, Teams, YouTube on macOS
    - Handle fullscreen app overlay behavior
    - _Requirements: 12.5, 4.1, 4.2, 4.3_
  
  - [x] 13.3 Add Linux-specific audio capture
    - Implement PulseAudio monitor source detection
    - Support PipeWire as alternative
    - Test with various desktop environments
    - _Requirements: 12.6, 4.1, 4.3_
  
  - [x] 13.4 Write platform-specific unit tests

    - Test Windows WASAPI usage
    - Test macOS Core Audio usage
    - Test Linux PulseAudio/PipeWire usage
    - _Requirements: 12.4, 12.5, 12.6_

- [x] 14. Create packaging configuration
  - [x] 14.1 Create PyInstaller spec file
    - Configure PyInstaller for single-file executable
    - Include all dependencies (Whisper, PyTorch, PyQt6)
    - Exclude unnecessary modules to reduce size
    - Add hidden imports for dynamic dependencies
    - _Requirements: 5.1, 5.2, 5.3, 5.4_
  
  - [x] 14.2 Create build scripts for all platforms
    - Create build.py script for automated building
    - Configure platform-specific options (Windows icon, macOS bundle, Linux AppImage)
    - Implement size optimization (UPX compression, exclude CUDA)
    - _Requirements: 5.1, 5.2, 5.3, 5.7_
  
  - [x] 14.3 Create installer configurations
    - Create Inno Setup script for Windows installer
    - Create DMG creation script for macOS
    - Create AppImageBuilder.yml for Linux AppImage
    - _Requirements: 5.1, 5.2, 5.3, 5.5_
  
  - [x] 14.4 Test packaged applications

    - Build and test Windows installer
    - Build and test macOS DMG
    - Build and test Linux AppImage
    - Verify all dependencies included
    - Verify size under 500MB
    - _Requirements: 5.4, 5.7_

- [x] 15. Implement code signing (optional for MVP)
  - [x] 15.1 Set up code signing for Windows
    - Obtain code signing certificate
    - Configure signtool for executable signing
    - _Requirements: 5.6_
  
  - [x] 15.2 Set up code signing for macOS
    - Obtain Apple Developer certificate
    - Configure codesign for app bundle signing
    - _Requirements: 5.6_

- [x] 16. Create documentation and assets
  - [x] 16.1 Create user documentation
    - Write README with installation instructions
    - Create quick start guide
    - Document keyboard shortcuts
    - Add troubleshooting section
    - _Requirements: All_
  
  - [x] 16.2 Create application assets
    - Design application icon (ICO, ICNS, PNG)
    - Create system tray icons (active/inactive states)
    - _Requirements: 6.2_

- [x] 17. Final testing and polish
  - [ ]* 17.1 Run full test suite
    - Execute all unit tests
    - Execute all property-based tests (100+ iterations each)
    - Execute integration tests
    - _Requirements: All_
  
  - [x] 17.2 Performance testing
    - Measure transcription latency with different models
    - Measure memory usage with different models
    - Measure application startup time
    - _Requirements: 3.2, 8.1, 8.2, 8.7_
  
  - [x] 17.3 Manual testing on all platforms
    - Test on Windows 10/11
    - Test on macOS 11+
    - Test on Ubuntu 20.04+
    - Test with Zoom, Teams, YouTube, FreeShow
    - _Requirements: 12.1, 12.2, 12.3, 4.1, 4.2, 4.3_

- [x] 18. Final checkpoint - Release preparation
  - Verify all tests pass
  - Verify all documentation complete
  - Verify installers work on all platforms
  - Prepare release notes
  - Ask the user if ready for release

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP delivery
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation throughout development
- Property tests validate universal correctness properties with 100+ iterations
- Unit tests validate specific examples and edge cases
- Integration tests validate end-to-end functionality
- Platform-specific testing ensures compatibility across Windows, macOS, and Linux
