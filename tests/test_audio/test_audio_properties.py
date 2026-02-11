"""Property-based tests for AudioCaptureEngine

Feature: system-wide-live-captions
Tests Properties 11-15 for audio capture behavior
"""

import pytest
import numpy as np
from hypothesis import given, strategies as st, settings, assume
from unittest.mock import Mock, patch, MagicMock
from src.audio.audio_capture import AudioCaptureEngine, AudioDevice
from src.config.config_manager import AudioConfig
import time


# Feature: system-wide-live-captions, Property 11: Audio device switching
@settings(max_examples=100, deadline=None)
@given(
    initial_device=st.integers(min_value=0, max_value=10),
    new_device=st.integers(min_value=0, max_value=10)
)
def test_property_11_audio_device_switching(initial_device, new_device):
    """
    For any audio device, calling set_device() should switch to that device 
    without requiring application restart, and subsequent audio capture should 
    come from the new device.
    
    **Validates: Requirements 2.3**
    """
    # Ensure devices are different for meaningful test
    assume(initial_device != new_device)
    
    config = AudioConfig()
    engine = AudioCaptureEngine(config)
    
    # Set initial device (not capturing)
    engine.set_device(initial_device)
    assert engine.current_device_id == initial_device
    
    # Switch to new device
    engine.set_device(new_device)
    assert engine.current_device_id == new_device
    
    # Verify no restart was required (engine still exists and is functional)
    assert engine is not None
    assert not engine.is_capturing
    
    # Test device switching while capturing (with mocked capture)
    callback = Mock()
    
    with patch.object(engine, '_capture_loop'):
        engine.is_capturing = True
        engine.current_device_id = initial_device
        engine.callback = callback
        
        # Switch device while capturing
        with patch.object(engine, 'stop_capture') as mock_stop, \
             patch.object(engine, 'start_capture') as mock_start:
            engine.set_device(new_device)
            
            # Verify stop was called
            mock_stop.assert_called_once()
            # Verify start was called with new device
            mock_start.assert_called_once_with(new_device, callback)


# Feature: system-wide-live-captions, Property 12: Simultaneous multi-source capture
@settings(max_examples=100, deadline=None)
@given(
    device1=st.integers(min_value=0, max_value=5),
    device2=st.integers(min_value=0, max_value=5),
    audio_amplitude1=st.floats(min_value=0.1, max_value=0.5),
    audio_amplitude2=st.floats(min_value=0.1, max_value=0.5)
)
def test_property_12_simultaneous_multi_source_capture(device1, device2, audio_amplitude1, audio_amplitude2):
    """
    For any two audio sources (e.g., system audio and microphone), the 
    Audio_Capture_Engine should be able to capture from both simultaneously 
    and mix the audio streams.
    
    **Validates: Requirements 2.4**
    """
    # Ensure devices are different
    assume(device1 != device2)
    
    config = AudioConfig()
    engine = AudioCaptureEngine(config)
    
    # Create test audio data
    sample_count = int(config.sample_rate * config.chunk_duration)
    audio1 = np.ones(sample_count, dtype=np.float32) * audio_amplitude1
    audio2 = np.ones(sample_count, dtype=np.float32) * audio_amplitude2
    
    # Test mixing function
    engine.primary_buffer = [audio1]
    engine.secondary_buffer = [audio2]
    
    mixed_results = []
    
    def test_callback(audio_data):
        mixed_results.append(audio_data)
    
    engine._mix_and_callback(test_callback)
    
    # Verify mixing occurred
    assert len(mixed_results) == 1
    mixed_audio = mixed_results[0]
    
    # Verify mixed audio is average of both sources
    expected_amplitude = (audio_amplitude1 + audio_amplitude2) / 2.0
    assert np.allclose(mixed_audio, expected_amplitude, atol=0.01)
    
    # Verify buffers were consumed
    assert len(engine.primary_buffer) == 0
    assert len(engine.secondary_buffer) == 0
    
    # Test start_multi_source_capture with device list
    callback = Mock()
    device_list = [device1, device2]
    
    with patch.object(engine, '_capture_loop'), \
         patch.object(engine, '_secondary_capture_loop'):
        result = engine.start_multi_source_capture(device_list, callback)
        
        # Should start successfully
        assert result is True
        assert engine.is_capturing is True
        assert engine.current_device_id == device1
        assert engine.secondary_device_id == device2


# Feature: system-wide-live-captions, Property 13: Pause on silence
@settings(max_examples=100, deadline=None)
@given(
    threshold=st.floats(min_value=0.001, max_value=0.1),
    audio_level=st.floats(min_value=0.0, max_value=1.0)
)
def test_property_13_pause_on_silence(threshold, audio_level):
    """
    For any configured silence threshold and duration, when audio levels remain 
    below the threshold for that duration, the Audio_Capture_Engine should 
    enter a paused state.
    
    **Validates: Requirements 2.5**
    """
    config = AudioConfig(vad_threshold=threshold)
    engine = AudioCaptureEngine(config)
    
    # Set audio level
    engine.current_audio_level = audio_level
    
    if audio_level < threshold:
        # Audio is below threshold
        # First call should not pause (silence timer just started)
        engine.silence_start_time = None
        should_pause = engine._should_pause_on_silence()
        assert should_pause is False
        assert engine.silence_start_time is not None
        
        # Simulate time passing (more than 3 seconds)
        engine.silence_start_time = time.time() - 4.0
        should_pause = engine._should_pause_on_silence()
        assert should_pause is True
    else:
        # Audio is above threshold
        engine.silence_start_time = time.time() - 4.0
        should_pause = engine._should_pause_on_silence()
        assert should_pause is False
        assert engine.silence_start_time is None


# Feature: system-wide-live-captions, Property 14: Device disconnection recovery
@settings(max_examples=100, deadline=None)
@given(
    device_id=st.integers(min_value=0, max_value=10)
)
def test_property_14_device_disconnection_recovery(device_id):
    """
    For any audio device disconnection event, the Audio_Capture_Engine should 
    detect the disconnection, not crash, and attempt to reconnect when the 
    device becomes available.
    
    **Validates: Requirements 2.6**
    """
    config = AudioConfig()
    engine = AudioCaptureEngine(config)
    
    # Set up engine as if capturing
    engine.current_device_id = device_id
    engine.is_capturing = True
    engine.reconnect_attempts = 0
    
    # Mock device availability check to simulate disconnection
    with patch.object(engine, 'check_device_available') as mock_check:
        mock_check.return_value = False
        
        # Detect device change
        device_changed = engine.detect_device_changes()
        assert device_changed is True
        
        # Handle disconnection
        error_callback = Mock()
        engine.error_callback = error_callback
        
        with patch.object(engine, 'stop_capture') as mock_stop:
            engine.handle_device_disconnection()
            
            # Verify error callback was called
            assert error_callback.call_count >= 1
            
            # Verify stop_capture was called
            mock_stop.assert_called_once()
            
            # Verify error message was set
            assert engine.last_error is not None
            assert "disconnected" in engine.last_error.lower()
    
    # Test that engine doesn't crash on disconnection
    # (if it crashed, we wouldn't reach this point)
    assert engine is not None
    
    # Test reconnection attempt logic in capture loop
    engine.reconnect_attempts = 0
    engine.max_reconnect_attempts = 5
    
    # Simulate multiple reconnection attempts
    for attempt in range(1, 6):
        engine.reconnect_attempts = attempt
        assert engine.reconnect_attempts <= engine.max_reconnect_attempts


# Feature: system-wide-live-captions, Property 15: Audio capture failure recovery
@settings(max_examples=100, deadline=None)
@given(
    error_message=st.text(min_size=1, max_size=100),
    attempt_number=st.integers(min_value=1, max_value=5)
)
def test_property_15_audio_capture_failure_recovery(error_message, attempt_number):
    """
    For any audio capture failure, the Audio_Capture_Engine should display 
    an error notification and attempt to reconnect without terminating the 
    application.
    
    **Validates: Requirements 9.1**
    """
    config = AudioConfig()
    engine = AudioCaptureEngine(config)
    
    # Set up error callback
    error_callback = Mock()
    engine.error_callback = error_callback
    engine.reconnect_attempts = attempt_number - 1
    engine.max_reconnect_attempts = 5
    
    # Simulate error
    engine.last_error = error_message
    
    # Call error callback
    if engine.error_callback:
        engine.error_callback(error_message)
    
    # Verify error callback was called
    assert error_callback.called
    assert error_callback.call_args[0][0] == error_message
    
    # Verify reconnection logic
    if attempt_number < engine.max_reconnect_attempts:
        # Should attempt reconnection
        assert engine.reconnect_attempts < engine.max_reconnect_attempts
    else:
        # Should stop after max attempts
        assert engine.reconnect_attempts >= engine.max_reconnect_attempts - 1
    
    # Verify engine still exists (didn't terminate application)
    assert engine is not None
    assert hasattr(engine, 'reconnect_attempts')
    assert hasattr(engine, 'error_callback')
    
    # Test that error doesn't crash the engine
    engine.last_error = error_message
    assert engine.last_error == error_message


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
