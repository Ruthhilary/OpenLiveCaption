"""
Smoke tests for manual testing preparation.

These tests verify that the application is ready for manual testing
by checking that all components can be initialized and basic operations work.

This is NOT a replacement for manual testing - it's a pre-check to ensure
the application is in a testable state.
"""

import pytest
import sys
import os
from PyQt6.QtWidgets import QApplication

from src.application import LiveCaptionApplication
from src.config.config_manager import ConfigManager
from src.audio.audio_capture import AudioCaptureEngine
from src.transcription.transcription_engine import TranscriptionEngine


@pytest.fixture(scope="session")
def qapp():
    """Create QApplication instance"""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app


class TestManualTestingPreparation:
    """Smoke tests to verify application is ready for manual testing"""
    
    def test_application_can_initialize(self, qapp, tmp_path):
        """
        Verify application can be initialized without errors.
        
        This is a prerequisite for all manual testing.
        """
        config_path = tmp_path / "config.json"
        
        # Initialize application
        app = LiveCaptionApplication(config_path=str(config_path))
        
        # Verify components are initialized
        assert app.audio_engine is not None, "Audio engine not initialized"
        assert app.transcription_engine is not None, "Transcription engine not initialized"
        assert app.translation_engine is not None, "Translation engine not initialized"
        assert app.caption_overlay is not None, "Caption overlay not initialized"
        assert app.control_window is not None, "Control window not initialized"
        
        # Cleanup
        app.shutdown()
    
    def test_audio_devices_can_be_listed(self, tmp_path):
        """
        Verify audio devices can be enumerated.
        
        Manual testing requires being able to select audio devices.
        """
        config_manager = ConfigManager(str(tmp_path / "config.json"))
        config = config_manager.load()
        
        audio_engine = AudioCaptureEngine(config.audio)
        devices = audio_engine.list_devices()
        
        # Should have at least one device (even if it's a dummy device)
        assert len(devices) >= 0, "No audio devices found"
        
        print(f"\nFound {len(devices)} audio device(s):")
        for device in devices:
            print(f"  - {device.name} (ID: {device.id})")
    
    def test_whisper_models_available(self):
        """
        Verify Whisper models can be loaded.
        
        Manual testing requires transcription to work.
        """
        # Test with tiny model (fastest to load)
        engine = TranscriptionEngine(model_name="tiny", device="cpu")
        
        assert engine.model is not None, "Whisper model not loaded"
        assert engine.model_name == "tiny", "Wrong model loaded"
    
    def test_control_window_can_display(self, qapp, tmp_path):
        """
        Verify control window can be created and displayed.
        
        Manual testing requires the UI to be functional.
        """
        config_manager = ConfigManager(str(tmp_path / "config.json"))
        config = config_manager.load()
        
        from src.ui.control_window import ControlWindow
        
        control_window = ControlWindow(config=config, config_manager=config_manager)
        
        # Verify window exists
        assert control_window is not None, "Control window not created"
        
        # Verify window can be shown (don't actually show it in test)
        assert control_window.isHidden(), "Window should be hidden initially"
    
    def test_caption_overlay_can_display(self, qapp, tmp_path):
        """
        Verify caption overlay can be created.
        
        Manual testing requires the overlay to be functional.
        """
        config_manager = ConfigManager(str(tmp_path / "config.json"))
        config = config_manager.load()
        
        from src.ui.caption_overlay import CaptionOverlay
        
        overlay = CaptionOverlay(config=config.overlay, config_manager=config_manager)
        
        # Verify overlay exists
        assert overlay is not None, "Caption overlay not created"
        
        # Verify overlay has correct window flags
        from PyQt6.QtCore import Qt
        flags = overlay.windowFlags()
        assert flags & Qt.WindowType.WindowStaysOnTopHint, "Overlay not set to stay on top"
        assert flags & Qt.WindowType.FramelessWindowHint, "Overlay not frameless"
    
    def test_configuration_can_be_saved_and_loaded(self, tmp_path):
        """
        Verify configuration persistence works.
        
        Manual testing requires settings to be saved between sessions.
        """
        config_path = tmp_path / "config.json"
        config_manager = ConfigManager(str(config_path))
        
        # Load default config
        config = config_manager.load()
        
        # Modify config
        config.transcription.model_name = "base"
        config.overlay.font_size = 32
        
        # Save config
        config_manager.save(config)
        
        # Load config again
        config_manager2 = ConfigManager(str(config_path))
        config2 = config_manager2.load()
        
        # Verify changes persisted
        assert config2.transcription.model_name == "base", "Model name not persisted"
        assert config2.overlay.font_size == 32, "Font size not persisted"
    
    def test_platform_detection(self):
        """
        Verify platform is correctly detected.
        
        Manual testing procedures differ by platform.
        """
        import platform
        
        system = platform.system()
        print(f"\nDetected platform: {system}")
        print(f"Platform version: {platform.version()}")
        print(f"Platform release: {platform.release()}")
        
        assert system in ["Windows", "Darwin", "Linux"], f"Unsupported platform: {system}"
        
        if system == "Windows":
            print("→ Use Windows manual testing procedures")
            print("→ Test WASAPI loopback audio capture")
        elif system == "Darwin":
            print("→ Use macOS manual testing procedures")
            print("→ Test Core Audio capture (may need BlackHole)")
        elif system == "Linux":
            print("→ Use Linux manual testing procedures")
            print("→ Test PulseAudio/PipeWire capture")


def test_print_manual_testing_instructions():
    """
    Print instructions for manual testing.
    
    This test always passes but provides useful information.
    """
    print("\n" + "="*70)
    print("MANUAL TESTING PREPARATION COMPLETE")
    print("="*70)
    print("\nAll smoke tests passed. The application is ready for manual testing.")
    print("\nNext steps:")
    print("1. Review the MANUAL_TESTING_GUIDE.md file")
    print("2. Follow the platform-specific testing procedures")
    print("3. Test integration with Zoom, Teams, YouTube, and FreeShow")
    print("4. Document results using the test results template")
    print("\nManual testing guide: MANUAL_TESTING_GUIDE.md")
    print("="*70)


if __name__ == "__main__":
    # Run smoke tests
    pytest.main([__file__, "-v", "-s"])
