"""Unit tests for AudioCaptureEngine"""

import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from src.audio.audio_capture import AudioCaptureEngine, AudioDevice
from src.config.config_manager import AudioConfig


class TestAudioCaptureEngine:
    """Test suite for AudioCaptureEngine"""
    
    def test_initialization(self):
        """Test AudioCaptureEngine initialization"""
        config = AudioConfig()
        engine = AudioCaptureEngine(config)
        
        assert engine.config == config
        assert not engine.is_capturing
        assert engine.current_device_id is None
        assert engine.current_audio_level == 0.0
    
    def test_audio_device_dataclass(self):
        """Test AudioDevice dataclass"""
        device = AudioDevice(
            id=0,
            name="Test Device",
            channels=2,
            sample_rate=16000,
            is_loopback=False,
            is_default=True
        )
        
        assert device.id == 0
        assert device.name == "Test Device"
        assert device.channels == 2
        assert device.sample_rate == 16000
        assert not device.is_loopback
        assert device.is_default
    
    def test_get_audio_level(self):
        """Test get_audio_level method"""
        config = AudioConfig()
        engine = AudioCaptureEngine(config)
        
        # Initial level should be 0
        assert engine.get_audio_level() == 0.0
        
        # Update level
        engine.current_audio_level = 0.5
        assert engine.get_audio_level() == 0.5
    
    def test_update_audio_level(self):
        """Test _update_audio_level method"""
        config = AudioConfig()
        engine = AudioCaptureEngine(config)
        
        # Test with silent audio
        silent_audio = np.zeros(1000, dtype=np.float32)
        engine._update_audio_level(silent_audio)
        assert engine.current_audio_level < 0.01
        
        # Test with loud audio
        loud_audio = np.ones(1000, dtype=np.float32) * 0.5
        engine._update_audio_level(loud_audio)
        assert engine.current_audio_level > 0.4
    
    def test_should_pause_on_silence(self):
        """Test _should_pause_on_silence method"""
        config = AudioConfig(vad_threshold=0.01)
        engine = AudioCaptureEngine(config)
        
        # No silence initially
        engine.current_audio_level = 0.5
        assert not engine._should_pause_on_silence()
        
        # Below threshold but not long enough
        engine.current_audio_level = 0.005
        assert not engine._should_pause_on_silence()
        
        # Silence timer should be set
        assert engine.silence_start_time is not None
    
    def test_check_device_available(self):
        """Test check_device_available method"""
        config = AudioConfig()
        engine = AudioCaptureEngine(config)
        
        # Mock list_devices to return test devices
        with patch.object(engine, 'list_devices') as mock_list:
            mock_list.return_value = [
                AudioDevice(0, "Device 0", 2, 16000),
                AudioDevice(1, "Device 1", 2, 16000),
            ]
            
            assert engine.check_device_available(0)
            assert engine.check_device_available(1)
            assert not engine.check_device_available(2)
    
    def test_detect_device_changes(self):
        """Test detect_device_changes method"""
        config = AudioConfig()
        engine = AudioCaptureEngine(config)
        
        # No device set
        assert not engine.detect_device_changes()
        
        # Set device and mock availability check
        engine.current_device_id = 0
        
        with patch.object(engine, 'check_device_available') as mock_check:
            # Device available
            mock_check.return_value = True
            assert not engine.detect_device_changes()
            
            # Device not available
            mock_check.return_value = False
            assert engine.detect_device_changes()
    
    def test_stop_capture_when_not_capturing(self):
        """Test stop_capture when not capturing"""
        config = AudioConfig()
        engine = AudioCaptureEngine(config)
        
        # Should not raise error
        engine.stop_capture()
        assert not engine.is_capturing
    
    def test_set_device_when_not_capturing(self):
        """Test set_device when not capturing"""
        config = AudioConfig()
        engine = AudioCaptureEngine(config)
        
        engine.set_device(5)
        assert engine.current_device_id == 5
    
    def test_error_callback_invocation(self):
        """Test that error callback is invoked on errors"""
        config = AudioConfig()
        engine = AudioCaptureEngine(config)
        
        error_callback = Mock()
        engine.error_callback = error_callback
        
        # Trigger device disconnection
        engine.current_device_id = 0
        engine.is_capturing = True
        engine.handle_device_disconnection()
        
        # Error callback should be called
        assert error_callback.call_count >= 1


class TestAudioDeviceEnumeration:
    """Test audio device enumeration"""
    
    @pytest.mark.skipif(True, reason="Requires actual audio hardware")
    def test_list_devices_returns_list(self):
        """Test that list_devices returns a list"""
        config = AudioConfig()
        engine = AudioCaptureEngine(config)
        
        devices = engine.list_devices()
        assert isinstance(devices, list)
    
    @pytest.mark.skipif(True, reason="Requires actual audio hardware")
    def test_list_devices_contains_audio_devices(self):
        """Test that list_devices returns AudioDevice objects"""
        config = AudioConfig()
        engine = AudioCaptureEngine(config)
        
        devices = engine.list_devices()
        if devices:
            assert all(isinstance(d, AudioDevice) for d in devices)


class TestMultiSourceCapture:
    """Test multi-source audio capture"""
    
    def test_start_multi_source_with_empty_list(self):
        """Test start_multi_source_capture with empty device list"""
        config = AudioConfig()
        engine = AudioCaptureEngine(config)
        
        callback = Mock()
        result = engine.start_multi_source_capture([], callback)
        
        assert not result
    
    def test_start_multi_source_with_single_device(self):
        """Test start_multi_source_capture with single device"""
        config = AudioConfig()
        engine = AudioCaptureEngine(config)
        
        callback = Mock()
        
        with patch.object(engine, 'start_capture') as mock_start:
            mock_start.return_value = True
            result = engine.start_multi_source_capture([0], callback)
            
            assert mock_start.called
            mock_start.assert_called_once_with(0, callback)
    
    def test_mix_and_callback(self):
        """Test _mix_and_callback method"""
        config = AudioConfig()
        engine = AudioCaptureEngine(config)
        
        # Setup buffers
        engine.primary_buffer = [np.ones(100, dtype=np.float32) * 0.5]
        engine.secondary_buffer = [np.ones(100, dtype=np.float32) * 0.3]
        
        callback = Mock()
        engine._mix_and_callback(callback)
        
        # Callback should be called with mixed audio
        assert callback.called
        mixed_audio = callback.call_args[0][0]
        
        # Mixed audio should be average of both sources
        expected = (0.5 + 0.3) / 2.0
        assert np.allclose(mixed_audio, expected, atol=0.01)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
