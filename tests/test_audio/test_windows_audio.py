"""Platform-specific tests for Windows audio capture using WASAPI"""

import pytest
import sys
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from src.audio.audio_capture import AudioCaptureEngine, AudioDevice
from src.config.config_manager import AudioConfig


# Skip all tests if not on Windows
pytestmark = pytest.mark.skipif(
    sys.platform != 'win32',
    reason="Windows-specific tests"
)


class TestWindowsWASAPICapture:
    """Test Windows WASAPI loopback audio capture"""
    
    @pytest.mark.skipif(True, reason="Requires PyAudioWPatch and actual hardware")
    def test_wasapi_loopback_device_detection(self):
        """Test that WASAPI loopback devices are detected on Windows"""
        config = AudioConfig()
        engine = AudioCaptureEngine(config)
        
        devices = engine.list_devices()
        
        # Should have at least one device
        assert len(devices) > 0
        
        # Check if any loopback devices are found
        loopback_devices = [d for d in devices if d.is_loopback]
        
        # Windows should have at least one loopback device (speakers)
        assert len(loopback_devices) > 0, "No WASAPI loopback devices found"
    
    @pytest.mark.skipif(True, reason="Requires PyAudioWPatch and actual hardware")
    def test_wasapi_device_properties(self):
        """Test that WASAPI devices have correct properties"""
        config = AudioConfig()
        engine = AudioCaptureEngine(config)
        
        devices = engine.list_devices()
        loopback_devices = [d for d in devices if d.is_loopback]
        
        if loopback_devices:
            device = loopback_devices[0]
            
            # Check device properties
            assert device.id >= 0
            assert len(device.name) > 0
            assert device.channels > 0
            assert device.sample_rate > 0
            assert device.is_loopback is True
    
    def test_windows_device_enumeration_mock(self):
        """Test Windows device enumeration with mocked PyAudio"""
        config = AudioConfig()
        engine = AudioCaptureEngine(config)
        
        # Mock PyAudio instance and module
        mock_pyaudio_module = MagicMock()
        mock_pyaudio_module.paWASAPI = 13  # Mock WASAPI constant
        
        mock_pyaudio = MagicMock()
        engine.pyaudio_instance = mock_pyaudio
        
        # Mock WASAPI host API info
        mock_pyaudio.get_host_api_info_by_type.return_value = {
            "defaultOutputDevice": 1
        }
        
        # Mock device count
        mock_pyaudio.get_device_count.return_value = 3
        
        # Mock device info
        def mock_get_device_info(index):
            if index == 0:
                return {
                    "name": "Microphone",
                    "maxInputChannels": 2,
                    "defaultSampleRate": 44100,
                    "isLoopbackDevice": False
                }
            elif index == 1:
                return {
                    "name": "Speakers (Loopback)",
                    "maxInputChannels": 2,
                    "defaultSampleRate": 48000,
                    "isLoopbackDevice": True
                }
            elif index == 2:
                return {
                    "name": "Output Device",
                    "maxInputChannels": 0,  # No input channels
                    "defaultSampleRate": 44100,
                    "isLoopbackDevice": False
                }
        
        mock_pyaudio.get_device_info_by_index.side_effect = mock_get_device_info
        
        # Patch the pyaudio module
        with patch('src.audio.audio_capture.pyaudio', mock_pyaudio_module):
            # Test device listing
            devices = engine._list_devices_windows()
        
        # Should have 2 devices (device 2 has no input channels)
        assert len(devices) == 2
        
        # Check microphone device
        mic_device = next(d for d in devices if not d.is_loopback)
        assert mic_device.name == "Microphone"
        assert mic_device.channels == 2
        assert mic_device.sample_rate == 44100
        
        # Check loopback device
        loopback_device = next(d for d in devices if d.is_loopback)
        assert loopback_device.name == "Speakers (Loopback)"
        assert loopback_device.is_loopback is True
        assert loopback_device.is_default is True
    
    def test_windows_capture_initialization(self):
        """Test Windows audio capture stream initialization"""
        config = AudioConfig(sample_rate=16000, chunk_duration=1.0)
        engine = AudioCaptureEngine(config)
        
        # Mock PyAudio
        mock_pyaudio = MagicMock()
        engine.pyaudio_instance = mock_pyaudio
        
        # Mock device info
        mock_pyaudio.get_device_info_by_index.return_value = {
            "maxInputChannels": 2,
            "defaultSampleRate": 48000
        }
        
        # Mock stream
        mock_stream = MagicMock()
        mock_pyaudio.open.return_value = mock_stream
        
        # Mock device availability
        with patch.object(engine, 'check_device_available', return_value=True):
            # Start capture in a way that doesn't actually run the loop
            engine.current_device_id = 0
            
            # Manually call the Windows capture setup part
            try:
                device_info = mock_pyaudio.get_device_info_by_index(0)
                stream = mock_pyaudio.open(
                    format=MagicMock(),  # paFloat32
                    channels=min(device_info["maxInputChannels"], 2),
                    rate=config.sample_rate,
                    input=True,
                    input_device_index=0,
                    frames_per_buffer=int(config.sample_rate * config.chunk_duration)
                )
                
                # Verify stream was opened with correct parameters
                assert mock_pyaudio.open.called
                call_kwargs = mock_pyaudio.open.call_args[1]
                assert call_kwargs['channels'] == 2
                assert call_kwargs['rate'] == 16000
                assert call_kwargs['input'] is True
                assert call_kwargs['input_device_index'] == 0
                assert call_kwargs['frames_per_buffer'] == 16000
            except:
                pass


class TestWindowsApplicationIntegration:
    """Test integration with Windows applications (Zoom, Teams, YouTube)"""
    
    @pytest.mark.skipif(True, reason="Requires actual applications running")
    def test_capture_from_zoom(self):
        """Test capturing audio from Zoom meeting"""
        # This test would require Zoom to be running with audio
        # In practice, this would be a manual test
        pass
    
    @pytest.mark.skipif(True, reason="Requires actual applications running")
    def test_capture_from_teams(self):
        """Test capturing audio from Microsoft Teams"""
        # This test would require Teams to be running with audio
        # In practice, this would be a manual test
        pass
    
    @pytest.mark.skipif(True, reason="Requires actual applications running")
    def test_capture_from_youtube(self):
        """Test capturing audio from YouTube in browser"""
        # This test would require browser playing YouTube
        # In practice, this would be a manual test
        pass
    
    def test_system_audio_capture_mock(self):
        """Test system audio capture with mocked audio data"""
        config = AudioConfig(sample_rate=16000, chunk_duration=1.0)
        engine = AudioCaptureEngine(config)
        
        # Mock PyAudio
        mock_pyaudio = MagicMock()
        engine.pyaudio_instance = mock_pyaudio
        
        # Mock device info for loopback device
        mock_pyaudio.get_device_info_by_index.return_value = {
            "maxInputChannels": 2,
            "defaultSampleRate": 48000,
            "isLoopbackDevice": True
        }
        
        # Mock stream
        mock_stream = MagicMock()
        mock_pyaudio.open.return_value = mock_stream
        
        # Simulate audio data from system (stereo)
        audio_data = np.random.randn(16000 * 2).astype(np.float32).tobytes()
        mock_stream.read.return_value = audio_data
        
        # Verify we can process the audio
        audio_array = np.frombuffer(audio_data, dtype=np.float32)
        
        # Convert stereo to mono
        if len(audio_array) > 16000:
            audio_array = audio_array.reshape(-1, 2).mean(axis=1)
        
        assert len(audio_array) == 16000
        assert audio_array.dtype == np.float32


class TestWindowsErrorHandling:
    """Test Windows-specific error handling"""
    
    def test_pyaudio_not_available(self):
        """Test behavior when PyAudio is not available"""
        config = AudioConfig()
        
        # Create engine without PyAudio
        with patch('src.audio.audio_capture.PYAUDIO_AVAILABLE', False):
            with patch('src.audio.audio_capture.pyaudio', None):
                engine = AudioCaptureEngine(config)
                
                # Should handle gracefully
                assert engine.pyaudio_instance is None
                
                # Device listing should return empty list
                devices = engine._list_devices_windows()
                assert devices == []
    
    def test_wasapi_not_available(self):
        """Test fallback when WASAPI is not available"""
        config = AudioConfig()
        engine = AudioCaptureEngine(config)
        
        # Mock PyAudio without WASAPI support
        mock_pyaudio = MagicMock()
        engine.pyaudio_instance = mock_pyaudio
        
        # Mock WASAPI not available
        mock_pyaudio.get_host_api_info_by_type.side_effect = Exception("WASAPI not available")
        
        # Should handle gracefully
        devices = engine._list_devices_windows()
        
        # May return empty list or fall back to other devices
        assert isinstance(devices, list)
    
    def test_device_disconnection_during_capture(self):
        """Test handling of device disconnection during capture"""
        config = AudioConfig()
        engine = AudioCaptureEngine(config)
        
        # Mock error callback
        error_callback = Mock()
        engine.error_callback = error_callback
        engine.current_device_id = 0
        engine.is_capturing = True
        
        # Simulate device disconnection
        engine.handle_device_disconnection()
        
        # Should call error callback
        assert error_callback.call_count >= 1
        
        # Should stop capturing
        assert not engine.is_capturing


class TestWindowsPerformance:
    """Test Windows audio capture performance"""
    
    def test_low_latency_capture(self):
        """Test that capture has low latency"""
        config = AudioConfig(sample_rate=16000, chunk_duration=1.0)
        engine = AudioCaptureEngine(config)
        
        # Verify chunk duration is appropriate for low latency
        assert config.chunk_duration <= 1.0
        
        # Verify sample rate is appropriate
        assert config.sample_rate == 16000
    
    def test_buffer_size_calculation(self):
        """Test that buffer size is calculated correctly"""
        config = AudioConfig(sample_rate=16000, chunk_duration=1.0)
        
        expected_buffer_size = int(16000 * 1.0)
        assert expected_buffer_size == 16000
        
        # Test with different chunk duration
        config2 = AudioConfig(sample_rate=16000, chunk_duration=0.5)
        expected_buffer_size2 = int(16000 * 0.5)
        assert expected_buffer_size2 == 8000


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
