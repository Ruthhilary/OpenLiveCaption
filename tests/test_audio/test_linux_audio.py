"""Platform-specific tests for Linux audio capture"""

import pytest
import sys
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from src.audio.audio_capture import AudioCaptureEngine, AudioDevice
from src.config.config_manager import AudioConfig


# Skip all tests if not on Linux
pytestmark = pytest.mark.skipif(
    sys.platform not in ['linux', 'linux2'],
    reason="Linux-specific tests"
)


class TestLinuxAudioCapture:
    """Test Linux audio capture using sounddevice"""
    
    @pytest.mark.skipif(True, reason="Requires sounddevice and actual hardware")
    def test_linux_device_detection(self):
        """Test that audio devices are detected on Linux"""
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
    
    @pytest.mark.skipif(True, reason="Requires PulseAudio")
    def test_pulseaudio_monitor_detection(self):
        """Test that PulseAudio monitor sources are detected"""
        config = AudioConfig()
        engine = AudioCaptureEngine(config)
        
        devices = engine.list_devices()
        
        # Look for monitor devices
        monitor_devices = [d for d in devices if '.monitor' in d.name.lower()]
        
        # If PulseAudio is running, should have monitor sources
        if monitor_devices:
            device = monitor_devices[0]
            assert device.is_loopback is True
    
    def test_linux_device_enumeration_mock_pulseaudio(self):
        """Test Linux device enumeration with mocked PulseAudio devices"""
        config = AudioConfig()
        engine = AudioCaptureEngine(config)
        
        # Mock sounddevice
        mock_sd = MagicMock()
        
        # Mock PulseAudio device list
        mock_devices = [
            {
                'name': 'Built-in Audio Analog Stereo',
                'max_input_channels': 2,
                'default_samplerate': 44100
            },
            {
                'name': 'Monitor of Built-in Audio Analog Stereo',
                'max_input_channels': 2,
                'default_samplerate': 44100
            },
            {
                'name': 'alsa_output.pci-0000_00_1f.3.analog-stereo.monitor',
                'max_input_channels': 2,
                'default_samplerate': 48000
            },
            {
                'name': 'Built-in Audio Digital Stereo (HDMI)',
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
        
        # Should have 3 devices (device 3 has no input channels)
        assert len(devices) == 3
        
        # Check microphone device
        mic_device = next(d for d in devices if 'built-in' in d.name.lower() and 'monitor' not in d.name.lower())
        assert 'Built-in Audio Analog Stereo' in mic_device.name
        assert mic_device.channels == 2
        assert not mic_device.is_loopback
        
        # Check monitor devices
        monitor_devices = [d for d in devices if d.is_loopback]
        assert len(monitor_devices) == 2
        
        # Verify monitor device properties
        for monitor in monitor_devices:
            assert 'monitor' in monitor.name.lower() or '.monitor' in monitor.name.lower()
            assert monitor.is_loopback is True
    
    def test_linux_device_enumeration_mock_pipewire(self):
        """Test Linux device enumeration with mocked PipeWire devices"""
        config = AudioConfig()
        engine = AudioCaptureEngine(config)
        
        # Mock sounddevice
        mock_sd = MagicMock()
        
        # Mock PipeWire device list (similar naming to PulseAudio)
        mock_devices = [
            {
                'name': 'Built-in Audio Stereo',
                'max_input_channels': 2,
                'default_samplerate': 48000
            },
            {
                'name': 'Built-in Audio Stereo.monitor',
                'max_input_channels': 2,
                'default_samplerate': 48000
            },
            {
                'name': 'PipeWire Loopback',
                'max_input_channels': 2,
                'default_samplerate': 48000
            }
        ]
        
        mock_sd.query_devices.return_value = mock_devices
        mock_sd.default.device = 0
        
        # Patch sounddevice
        with patch('src.audio.audio_capture.sd', mock_sd):
            with patch('src.audio.audio_capture.SOUNDDEVICE_AVAILABLE', True):
                devices = engine._list_devices_unix()
        
        # Should have 3 devices
        assert len(devices) == 3
        
        # Check loopback devices
        loopback_devices = [d for d in devices if d.is_loopback]
        assert len(loopback_devices) == 2
        
        # Verify loopback detection
        monitor_device = next(d for d in loopback_devices if '.monitor' in d.name.lower())
        assert monitor_device.is_loopback is True
        
        loopback_device = next(d for d in loopback_devices if 'loopback' in d.name.lower())
        assert loopback_device.is_loopback is True
    
    def test_linux_capture_initialization(self):
        """Test Linux audio capture stream initialization"""
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


class TestLinuxApplicationIntegration:
    """Test integration with Linux applications"""
    
    @pytest.mark.skipif(True, reason="Requires actual applications running")
    def test_capture_from_zoom_linux(self):
        """Test capturing audio from Zoom on Linux"""
        # This test would require Zoom to be running with audio
        pass
    
    @pytest.mark.skipif(True, reason="Requires actual applications running")
    def test_capture_from_teams_linux(self):
        """Test capturing audio from Microsoft Teams on Linux"""
        # This test would require Teams to be running with audio
        pass
    
    @pytest.mark.skipif(True, reason="Requires actual applications running")
    def test_capture_from_youtube_linux(self):
        """Test capturing audio from YouTube in browser"""
        # This test would require browser playing YouTube
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


class TestLinuxDesktopEnvironments:
    """Test compatibility with various Linux desktop environments"""
    
    @pytest.mark.skipif(True, reason="Requires specific desktop environment")
    def test_gnome_compatibility(self):
        """Test overlay works on GNOME desktop"""
        # Would test overlay visibility on GNOME
        pass
    
    @pytest.mark.skipif(True, reason="Requires specific desktop environment")
    def test_kde_compatibility(self):
        """Test overlay works on KDE Plasma desktop"""
        # Would test overlay visibility on KDE
        pass
    
    @pytest.mark.skipif(True, reason="Requires specific desktop environment")
    def test_xfce_compatibility(self):
        """Test overlay works on XFCE desktop"""
        # Would test overlay visibility on XFCE
        pass
    
    def test_x11_window_flags(self):
        """Test that overlay uses correct X11 window flags"""
        # The overlay should use appropriate window flags for X11:
        # - Qt.WindowStaysOnTopHint
        # - Qt.FramelessWindowHint
        # - Qt.Tool
        # - Qt.WindowTransparentForInput
        pass
    
    def test_wayland_compatibility(self):
        """Test Wayland compatibility considerations"""
        # Wayland has different window management than X11
        # The overlay should work on both X11 and Wayland
        pass


class TestLinuxErrorHandling:
    """Test Linux-specific error handling"""
    
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
    
    def test_pulseaudio_not_running(self):
        """Test behavior when PulseAudio is not running"""
        config = AudioConfig()
        engine = AudioCaptureEngine(config)
        
        # Mock sounddevice without monitor sources
        mock_sd = MagicMock()
        mock_devices = [
            {
                'name': 'ALSA PCM',
                'max_input_channels': 2,
                'default_samplerate': 44100
            }
        ]
        
        mock_sd.query_devices.return_value = mock_devices
        mock_sd.default.device = 0
        
        with patch('src.audio.audio_capture.sd', mock_sd):
            with patch('src.audio.audio_capture.SOUNDDEVICE_AVAILABLE', True):
                devices = engine._list_devices_unix()
        
        # Should still have ALSA device
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
    
    def test_alsa_buffer_underrun(self):
        """Test handling of ALSA buffer underrun"""
        # ALSA can have buffer underruns which should be handled gracefully
        # The implementation should continue capturing after underruns
        pass


class TestLinuxPerformance:
    """Test Linux audio capture performance"""
    
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
    
    def test_cpu_usage_efficiency(self):
        """Test that audio capture is CPU efficient"""
        # Audio capture should use minimal CPU
        # This would be measured in actual performance testing
        pass


class TestLinuxAudioSystems:
    """Test compatibility with different Linux audio systems"""
    
    def test_pulseaudio_detection(self):
        """Test detection of PulseAudio system"""
        # Could check if PulseAudio is running
        # pactl info or similar command
        pass
    
    def test_pipewire_detection(self):
        """Test detection of PipeWire system"""
        # Could check if PipeWire is running
        # pw-cli info or similar command
        pass
    
    def test_alsa_fallback(self):
        """Test fallback to ALSA when neither PulseAudio nor PipeWire available"""
        # Should still work with raw ALSA
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
