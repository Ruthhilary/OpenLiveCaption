"""Shared pytest fixtures and configuration for OpenLiveCaption tests"""

import pytest
import tempfile
import shutil
from pathlib import Path
from hypothesis import settings, Verbosity

# Configure hypothesis for property-based testing
settings.register_profile("default", max_examples=20, deadline=None)
settings.register_profile("ci", max_examples=100, deadline=None)
settings.register_profile("dev", max_examples=10, deadline=None, verbosity=Verbosity.verbose)
settings.load_profile("default")


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files"""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def temp_config_file(temp_dir):
    """Create a temporary config file path"""
    config_path = temp_dir / "config.json"
    yield config_path
    if config_path.exists():
        config_path.unlink()


@pytest.fixture
def sample_audio_data():
    """Generate sample audio data for testing"""
    import numpy as np
    # 1 second of 16kHz audio
    sample_rate = 16000
    duration = 1.0
    samples = int(sample_rate * duration)
    # Generate a simple sine wave
    frequency = 440.0  # A4 note
    t = np.linspace(0, duration, samples, False)
    audio = np.sin(2 * np.pi * frequency * t).astype(np.float32)
    return audio


@pytest.fixture
def mock_whisper_result():
    """Mock Whisper transcription result"""
    return {
        "text": "This is a test transcription",
        "language": "en",
        "segments": [
            {
                "start": 0.0,
                "end": 2.0,
                "text": "This is a test transcription"
            }
        ]
    }
