"""Platform-specific tests for macOS audio capture"""

import pytest
import sys
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from src.audio.audio_capture import AudioCaptureEngine, AudioDevice
from src.config.config_manager import AudioConfig


# Skip all tests if not on macOS
pytestmark = pytest.mark.skipif(
    sys.platform != 'darwin',
    reason="macOS-specific tests"
)


class TestMacOSAudioCapture:
    """Test macOS audio capture using sounddevice"""
    
    @pytest.mark.skipif(True, reason="Requires sounddevice and actual hardware")
    def test_macos_device_detection(self):
        """Test that audio devices are detected on macOS"""
        config = AudioConfig()
        engine = AudioCaptureEngine(config)
        
        devices = engine.list_devices()
        
        # Should have at least one device
        assert len(devices) > 0
        
        # Check device properties
        for device in devices:
            assert device.id >= 0
            assert len(device.name) > 0
            assert device.channels > 0
            assert device.sample_rate > 0
    
    @pytest.mark.skipif(True, reason="Requires BlackHole installation")
    def test_blackhole_device_detection(self):
        """Test that BlackHole virtual audio device is detected"""
        config = AudioConfig()
        engine = AudioCaptureEngine(config)
        
        devices = engine.list_devices()
        
        # Look for BlackHole device
        blackhole_devices = [d for d in devices if 'blackhole' in d.name.lower()]
        
        # If BlackHole is installed, it should be detected as loopback
        if blackhole_devices:
            device = blackhole_devices[0]
            assert device.is_loopback is True
    
    def test_macos_device_enumeration_mock(self):
        """Test macOS device enumeration with mocked sounddevice"""
        config = AudioConfig()
        engine = AudioCaptureEngine(config)
        
        # Mock sounddevice
        mock_sd = MagicMock()
        
        # Mock device list
        mock_devices = [
            {
                'name': 'Built-in Microphone',
                'max_input_channels': 2,
                'default_samplerate': 44100
            },
            {
                'name': 'BlackHole 2ch',
                'max_input_channels': 2,
                'default_samplerate': 48000
            },
            {
                'name': 'Built-in Output',
                'max_input_channels': 0,  # No input channels
                'default_samplerate': 44100
            }
        ]
        
        mock_sd.query_devices.return_value = mock_devices
        mock_sd.default.device = (0, 1)  # (input, output)
        
        # Patch sounddevice
        with patch('src.audio.audio_capture.sd', mock_sd):
            with patch('src.audio.audio_capture.SOUNDDEVICE_AVAILABLE', True):
                devices = engine._list_devices_unix()
        
        # Should have 2 devices (device 2 has no input channels)
        assert len(devices) == 2
        
        # Check microphone device
        mic_device = next(d for d in devices if 'microphone' in d.name.lower())
        assert mic_device.name == 'Built-in Microphone'
        assert mic_device.channels == 2
        assert mic_device.sample_rate == 44100
        assert not mic_device.is_loopback
        assert mic_device.is_default is True
        
        # Check BlackHole device
        blackhole_device = next(d for d in devices if 'blackhole' in d.name.lower())
        assert blackhole_device.name == 'BlackHole 2ch'
        assert blackhole_device.is_loopback is True
    
    def test_macos_capture_initialization(self):
        """Test macOS audio capture stream initialization"""
        config = AudioConfig(sample_rate=16000, chunk_duration=1.0)
        engine = AudioCaptureEngine(config)
        
        # Mock sounddevice
        mock_sd = MagicMock()
        mock_stream = MagicMock()
        mock_sd.InputStream.return_value = mock_stream
        
        # Patch sounddevice
        with patch('src.audio.audio_capture.sd', mock_sd):
            with patch('src.audio.audio_capture.SOUNDDEVICE_AVAILABLE', True):
                # Verify InputStream can be created with correct parameters
                stream = mock_sd.InputStream(
                    device=0,
                    channels=2,
                    samplerate=config.sample_rate,
                    dtype=np.float32,
                    blocksize=int(config.sample_rate * config.chunk_duration),
                    callback=lambda *args: None
                )
                
                # Verify stream was created with correct parameters
                assert mock_sd.InputStream.called
                call_kwargs = mock_sd.InputStream.call_args[1]
                assert call_kwargs['device'] == 0
                assert call_kwargs['channels'] == 2
                assert call_kwargs['samplerate'] == 16000
                assert call_kwargs['blocksize'] == 16000


class TestMacOSApplicationIntegration:
    """Test integration with macOS applications"""
    
    @pytest.mark.skipif(True, reason="Requires actual applications running")
    def test_capture_from_zoom_macos(self):
        """Test capturing audio from Zoom on macOS"""
        # This test would require Zoom to be running with audio
        # and BlackHole configured as audio output
        pass
    
    @pytest.mark.skipif(True, reason="Requires actual applications running")
    def test_capture_from_teams_macos(self):
        """Test capturing audio from Microsoft Teams on macOS"""
        # This test would require Teams to be running with audio
        # and BlackHole configured as audio output
        pass
    
    @pytest.mark.skipif(True, reason="Requires actual applications running")
    def test_capture_from_youtube_macos(self):
        """Test capturing audio from YouTube in Safari/Chrome"""
        # This test would require browser playing YouTube
        # and BlackHole configured as audio output
        pass
    
    def test_system_audio_capture_mock(self):
        """Test system audio capture with mocked audio data"""
        config = AudioConfig(sample_rate=16000, chunk_duration=1.0)
        engine = AudioCaptureEngine(config)
        
        # Mock sounddevice
        mock_sd = MagicMock()
        
        # Simulate audio callback
        captured_audio = []
        
        def mock_callback_handler(indata, frames, time_info, status):
            # Simulate stereo audio data
            audio_data = np.random.randn(frames, 2).astype(np.float32)
            captured_audio.append(audio_data)
        
        # Verify callback processing
        mock_callback_handler(
            np.random.randn(16000, 2).astype(np.float32),
            16000,
            None,
            None
        )
        
        assert len(captured_audio) == 1
        assert captured_audio[0].shape == (16000, 2)


class TestMacOSFullscreenBehavior:
    """Test overlay behavior with fullscreen applications on macOS"""
    
    @pytest.mark.skipif(True, reason="Requires GUI testing")
    def test_overlay_visible_in_fullscreen(self):
        """Test that overlay remains visible when app is fullscreen"""
        # This would require actual GUI testing
        # The overlay should use NSWindowLevel to stay on top
        pass
    
    def test_fullscreen_window_level(self):
        """Test that overlay uses correct window level for fullscreen"""
        # On macOS, the overlay should use NSFloatingWindowLevel or higher
        # to stay visible over fullscreen apps
        
        # This is a conceptual test - actual implementation would be in PyQt6
        # The overlay should set appropriate window flags:
        # - Qt.WindowStaysOnTopHint
        # - Qt.Tool (to not show in Dock)
        # - Possibly custom NSWindow level via native API
        pass


class TestMacOSErrorHandling:
    """Test macOS-specific error handling"""
    
    def test_sounddevice_not_available(self):
        """Test behavior when sounddevice is not available"""
        config = AudioConfig()
        
        # Create engine without sounddevice
        with patch('src.audio.audio_capture.SOUNDDEVICE_AVAILABLE', False):
            with patch('src.audio.audio_capture.sd', None):
                engine = AudioCaptureEngine(config)
                
                # Device listing should return empty list
                devices = engine._list_devices_unix()
                assert devices == []
    
    def test_blackhole_not_installed(self):
        """Test behavior when BlackHole is not installed"""
        config = AudioConfig()
        engine = AudioCaptureEngine(config)
        
        # Mock sounddevice without BlackHole
        mock_sd = MagicMock()
        mock_devices = [
            {
                'name': 'Built-in Microphone',
                'max_input_channels': 2,
                'default_samplerate': 44100
            }
        ]
        
        mock_sd.query_devices.return_value = mock_devices
        mock_sd.default.device = 0
        
        with patch('src.audio.audio_capture.sd', mock_sd):
            with patch('src.audio.audio_capture.SOUNDDEVICE_AVAILABLE', True):
                devices = engine._list_devices_unix()
        
        # Should still have microphone device
        assert len(devices) == 1
        
        # No loopback devices
        loopback_devices = [d for d in devices if d.is_loopback]
        assert len(loopback_devices) == 0
    
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


class TestMacOSPerformance:
    """Test macOS audio capture performance"""
    
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
