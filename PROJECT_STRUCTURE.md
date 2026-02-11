# OpenLiveCaption Project Structure

## Directory Layout

```
openlivecaption/
├── src/                          # Source code
│   ├── __init__.py
│   ├── audio/                    # Audio capture components
│   │   └── __init__.py
│   ├── transcription/            # Transcription and translation
│   │   └── __init__.py
│   ├── ui/                       # User interface components
│   │   └── __init__.py
│   ├── config/                   # Configuration management
│   │   ├── __init__.py
│   │   └── config_manager.py
│   └── export/                   # Subtitle export
│       └── __init__.py
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── test_audio/
│   │   └── __init__.py
│   ├── test_transcription/
│   │   └── __init__.py
│   ├── test_ui/
│   │   └── __init__.py
│   ├── test_config/
│   │   └── __init__.py
│   └── test_export/
│       └── __init__.py
├── .kiro/                        # Kiro specs and configuration
│   └── specs/
│       └── system-wide-live-captions/
├── requirements.txt              # Python dependencies
├── pytest.ini                    # Pytest configuration
├── setup.py                      # Package setup
└── Main.py                       # Legacy entry point (to be migrated)
```

## Module Responsibilities

### src/audio/
Audio capture engine for system audio and microphone input:
- Device enumeration and selection
- WASAPI loopback (Windows) via PyAudioWPatch
- Core Audio (macOS) and PulseAudio (Linux) via sounddevice
- Voice Activity Detection (VAD)
- Multi-source audio mixing

### src/transcription/
Speech-to-text and translation:
- Whisper model integration
- Real-time transcription with overlapping chunks
- Language detection and manual override
- MarianMT translation engine
- Model caching and lazy loading

### src/ui/
PyQt6-based user interface:
- Caption overlay (always-on-top, click-through)
- Control window with start/stop controls
- System tray integration
- Settings dialog
- Keyboard shortcut handling

### src/config/
Configuration management:
- JSON-based persistence
- Platform-specific config paths
- Dataclass-based configuration models
- Default value handling
- Config validation and error recovery

### src/export/
Subtitle file export:
- SRT format support
- VTT format support
- Timestamp formatting
- Dual-language export (original + translation)

### tests/
Comprehensive test suite:
- Unit tests for individual components
- Property-based tests using Hypothesis
- Integration tests for end-to-end workflows
- Platform-specific tests

## Configuration File Locations

- **Windows**: `%APPDATA%/OpenLiveCaption/config.json`
- **macOS**: `~/Library/Application Support/OpenLiveCaption/config.json`
- **Linux**: `~/.config/OpenLiveCaption/config.json`

## Testing

Run tests with pytest:
```bash
# Run all tests
pytest

# Run specific test category
pytest -m unit
pytest -m property
pytest -m integration

# Run with coverage
pytest --cov=src --cov-report=html
```

## Development Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install in development mode:
```bash
pip install -e .
```

3. Run tests:
```bash
pytest
```

## Next Steps

Follow the implementation tasks in `.kiro/specs/system-wide-live-captions/tasks.md` to build out each component.
