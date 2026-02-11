"""Integration tests for AudioCaptureEngine (requires audio hardware)"""

import pytest
import numpy as np
import time
from src.audio.audio_capture import AudioCaptureEngine, AudioDevice
from src.config.config_manager import AudioConfig


@pytest.mark.skipif(True, reason="Requires actual audio hardware - run manually")
class TestAudioCaptureIntegration:
    """Integration tests for audio capture (manual testing only)"""
    
    def test_list_devices_integration(self):
        """Test listing actual audio devices"""
        config = AudioConfig()
        engine = AudioCaptureEngine(config)
        
        devices = engine.list_devices()
        
        print(f"\nFound {len(devices)} audio devices:")
        for device in devices:
            print(f"  [{device.id}] {device.name}")
            print(f"      Channels: {device.channels}, Sample Rate: {device.sample_rate}")
            print(f"      Loopback: {device.is_loopback}, Default: {device.is_default}")
        
        assert isinstance(devices, list)
        if devices:
            assert all(isinstance(d, AudioDevice) for d in devices)
    
    def test_audio_capture_integration(self):
        """Test actual audio capture from default device"""
        config = AudioConfig(chunk_duration=0.5)
        engine = AudioCaptureEngine(config)
        
        devices = engine.list_devices()
        if not devices:
            pytest.skip("No audio devices available")
        
        # Use first available device
        device_id = devices[0].id
        
        captured_chunks = []
        
        def audio_callback(audio_data: np.ndarray):
            captured_chunks.append(audio_data)
            print(f"Captured chunk: {len(audio_data)} samples, level: {engine.get_audio_level():.3f}")
        
        # Start capture
        success = engine.start_capture(device_id, audio_callback)
        assert success
        assert engine.is_capturing
        
        # Capture for 2 seconds
        time.sleep(2.0)
        
        # Stop capture
        engine.stop_capture()
        assert not engine.is_capturing
        
        # Verify we captured some audio
        print(f"\nCaptured {len(captured_chunks)} chunks")
        assert len(captured_chunks) > 0
        
        # Verify audio data format
        for chunk in captured_chunks:
            assert isinstance(chunk, np.ndarray)
            assert chunk.dtype == np.float32
            assert len(chunk) > 0
    
    def test_device_switching_integration(self):
        """Test switching between audio devices"""
        config = AudioConfig(chunk_duration=0.5)
        engine = AudioCaptureEngine(config)
        
        devices = engine.list_devices()
        if len(devices) < 2:
            pytest.skip("Need at least 2 audio devices for this test")
        
        captured_chunks = []
        
        def audio_callback(audio_data: np.ndarray):
            captured_chunks.append(audio_data)
        
        # Start with first device
        engine.start_capture(devices[0].id, audio_callback)
        time.sleep(1.0)
        
        chunks_from_device1 = len(captured_chunks)
        print(f"Captured {chunks_from_device1} chunks from device 1")
        
        # Switch to second device
        engine.set_device(devices[1].id)
        time.sleep(1.0)
        
        chunks_from_device2 = len(captured_chunks) - chunks_from_device1
        print(f"Captured {chunks_from_device2} chunks from device 2")
        
        # Stop capture
        engine.stop_capture()
        
        # Verify we captured from both devices
        assert chunks_from_device1 > 0
        assert chunks_from_device2 > 0
    
    def test_vad_integration(self):
        """Test Voice Activity Detection"""
        config = AudioConfig(vad_threshold=0.01, chunk_duration=0.5)
        engine = AudioCaptureEngine(config)
        
        devices = engine.list_devices()
        if not devices:
            pytest.skip("No audio devices available")
        
        audio_levels = []
        
        def audio_callback(audio_data: np.ndarray):
            level = engine.get_audio_level()
            audio_levels.append(level)
            print(f"Audio level: {level:.4f}, Paused: {engine.is_paused}")
        
        # Start capture
        engine.start_capture(devices[0].id, audio_callback)
        
        # Capture for 5 seconds (should detect silence if no audio playing)
        print("\nMonitoring audio levels for 5 seconds...")
        time.sleep(5.0)
        
        # Stop capture
        engine.stop_capture()
        
        print(f"\nCaptured {len(audio_levels)} audio level measurements")
        if audio_levels:
            print(f"Min level: {min(audio_levels):.4f}")
            print(f"Max level: {max(audio_levels):.4f}")
            print(f"Avg level: {sum(audio_levels)/len(audio_levels):.4f}")


if __name__ == "__main__":
    # Run integration tests manually
    pytest.main([__file__, "-v", "-s", "-k", "integration"])
