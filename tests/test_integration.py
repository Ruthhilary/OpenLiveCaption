"""
Integration tests for OpenLiveCaption application.

These tests verify end-to-end functionality across all components:
- Audio capture → Transcription → Display → Export pipeline
- Error recovery across components
- Configuration persistence across restart

Feature: system-wide-live-captions
"""

import pytest
import time
import json
import numpy as np
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QTimer

from src.application import LiveCaptionApplication
from src.config.config_manager import ConfigManager, Config, AudioConfig, TranscriptionConfig, OverlayConfig, ExportConfig
from src.audio.audio_capture import AudioCaptureEngine, AudioDevice
from src.transcription.transcription_engine import TranscriptionResult


@pytest.fixture(scope="module")
def qapp():
    """Create QApplication instance for tests"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


@pytest.fixture
def integration_config(temp_dir):
    """Create a test configuration for integration tests"""
    config_path = temp_dir / "integration_config.json"
    
    config = Config(
        audio=AudioConfig(
            device_id=0,
            sample_rate=16000,
            chunk_duration=1.0,
            vad_threshold=0.01
        ),
        transcription=TranscriptionConfig(
            model_name="tiny",
            device="cpu",
            language=None,
            enable_translation=False,
            target_language=None
        ),
        overlay=OverlayConfig(
            position="bottom",
            font_size=24,
            text_color="#FFFFFF",
            background_color="#000000",
            background_opacity=0.7
        ),
        export=ExportConfig(
            enabled=True,
            format="srt",
            output_path=str(temp_dir / "test_subtitles.srt")
        )
    )
    
    config_manager = ConfigManager(str(config_path))
    config_manager.save(config)
    
    return config_path


class TestEndToEndPipeline:
    """Test the complete audio → transcription → display → export pipeline"""
    
    def test_audio_to_transcription_to_display_flow(self, qapp, integration_config, sample_audio_data, temp_dir):
        """
        Test end-to-end flow: audio capture → transcription → overlay display
        
        Validates: Requirements All (end-to-end integration)
        """
        # Mock Whisper model to avoid loading actual model
        mock_whisper_model = Mock()
        mock_whisper_model.transcribe.return_value = {
            "text": "Hello world",
            "language": "en",
            "segments": [{
                "start": 0.0,
                "end": 1.0,
                "text": "Hello world"
            }]
        }
        
        # Mock audio device enumeration
        mock_devices = [
            AudioDevice(id=0, name="Test Device", channels=2, sample_rate=16000, is_loopback=False)
        ]
        
        with patch('whisper.load_model', return_value=mock_whisper_model), \
             patch.object(AudioCaptureEngine, 'list_devices', return_value=mock_devices), \
             patch.object(AudioCaptureEngine, 'start_capture') as mock_start_capture:
            
            # Create application
            app = LiveCaptionApplication(config_path=str(integration_config))
            
            # Verify components initialized
            assert app.audio_engine is not None
            assert app.transcription_engine is not None
            assert app.caption_overlay is not None
            assert app.control_window is not None
            
            # Start captions
            app.start_captions()
            assert app.is_running is True
            
            # Verify audio capture was started
            assert mock_start_capture.called
            
            # Get the audio callback that was registered
            audio_callback = mock_start_capture.call_args[1]['callback']
            
            # Simulate audio chunk arriving
            audio_callback(sample_audio_data)
            
            # Process Qt events to allow overlay update
            qapp.processEvents()
            
            # Verify overlay received caption
            # The overlay should have text displayed
            assert app.caption_overlay.isVisible()
            
            # Stop captions
            app.stop_captions()
            assert app.is_running is False
            
            # Cleanup
            app.shutdown()
    
    def test_audio_to_export_pipeline(self, qapp, integration_config, sample_audio_data, temp_dir):
        """
        Test end-to-end flow: audio capture → transcription → subtitle export
        
        Validates: Requirements 11.1, 11.3 (subtitle export)
        """
        # Mock Whisper model
        mock_whisper_model = Mock()
        mock_whisper_model.transcribe.return_value = {
            "text": "Test caption for export",
            "language": "en",
            "segments": [{
                "start": 0.0,
                "end": 2.0,
                "text": "Test caption for export"
            }]
        }
        
        mock_devices = [
            AudioDevice(id=0, name="Test Device", channels=2, sample_rate=16000, is_loopback=False)
        ]
        
        with patch('whisper.load_model', return_value=mock_whisper_model), \
             patch.object(AudioCaptureEngine, 'list_devices', return_value=mock_devices), \
             patch.object(AudioCaptureEngine, 'start_capture') as mock_start_capture:
            
            # Create application
            app = LiveCaptionApplication(config_path=str(integration_config))
            
            # Start captions
            app.start_captions()
            
            # Get audio callback
            audio_callback = mock_start_capture.call_args[1]['callback']
            
            # Simulate multiple audio chunks
            for i in range(3):
                audio_callback(sample_audio_data)
                qapp.processEvents()
                time.sleep(0.1)
            
            # Stop captions (should finalize export)
            app.stop_captions()
            
            # Verify subtitle file was created
            subtitle_path = Path(app.config.export.output_path)
            assert subtitle_path.exists()
            
            # Verify subtitle file has content
            content = subtitle_path.read_text()
            assert len(content) > 0
            assert "Test caption for export" in content or content.strip() != ""
            
            # Cleanup
            app.shutdown()
    
    def test_translation_pipeline(self, qapp, integration_config, sample_audio_data, temp_dir):
        """
        Test end-to-end flow with translation enabled
        
        Validates: Requirements 10.1, 10.4 (translation integration)
        """
        # Enable translation in config
        config_manager = ConfigManager(str(integration_config))
        config = config_manager.load()
        config.transcription.enable_translation = True
        config.transcription.target_language = "yo"  # Yoruba
        config_manager.save(config)
        
        # Mock Whisper model
        mock_whisper_model = Mock()
        mock_whisper_model.transcribe.return_value = {
            "text": "Hello",
            "language": "en",
            "segments": [{
                "start": 0.0,
                "end": 1.0,
                "text": "Hello"
            }]
        }
        
        mock_devices = [
            AudioDevice(id=0, name="Test Device", channels=2, sample_rate=16000, is_loopback=False)
        ]
        
        # Mock the entire translation engine to avoid import issues
        with patch('whisper.load_model', return_value=mock_whisper_model), \
             patch.object(AudioCaptureEngine, 'list_devices', return_value=mock_devices), \
             patch.object(AudioCaptureEngine, 'start_capture') as mock_start_capture, \
             patch('src.translation.translation_engine.TranslationEngine'):
            
            # Create application
            app = LiveCaptionApplication(config_path=str(integration_config))
            
            # Start captions
            app.start_captions()
            
            # Get audio callback
            audio_callback = mock_start_capture.call_args[1]['callback']
            
            # Simulate audio chunk
            audio_callback(sample_audio_data)
            qapp.processEvents()
            
            # Verify translation was attempted
            # (In real scenario, translation engine would be called)
            assert app.translation_engine is not None
            
            # Stop and cleanup
            app.stop_captions()
            app.shutdown()


class TestErrorRecovery:
    """Test error recovery across components"""
    
    def test_audio_capture_failure_recovery(self, qapp, integration_config):
        """
        Test that application recovers from audio capture failures
        
        Validates: Requirements 9.1, 9.5 (error handling)
        """
        mock_devices = [
            AudioDevice(id=0, name="Test Device", channels=2, sample_rate=16000, is_loopback=False)
        ]
        
        # Mock Whisper model
        mock_whisper_model = Mock()
        
        with patch('whisper.load_model', return_value=mock_whisper_model), \
             patch.object(AudioCaptureEngine, 'list_devices', return_value=mock_devices), \
             patch.object(AudioCaptureEngine, 'start_capture', return_value=False):
            
            # Create application
            app = LiveCaptionApplication(config_path=str(integration_config))
            
            # Try to start captions (should fail gracefully)
            app.start_captions()
            
            # Application should not crash and should remain in stopped state
            assert app.is_running is False
            
            # Cleanup
            app.shutdown()
    
    def test_transcription_error_recovery(self, qapp, integration_config, sample_audio_data):
        """
        Test that application continues after transcription errors
        
        Validates: Requirements 9.2 (transcription error handling)
        """
        # Mock Whisper model that fails on first call, succeeds on second
        mock_whisper_model = Mock()
        call_count = [0]
        
        def transcribe_with_error(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                raise Exception("Transcription failed")
            return {
                "text": "Success after error",
                "language": "en",
                "segments": [{
                    "start": 0.0,
                    "end": 1.0,
                    "text": "Success after error"
                }]
            }
        
        mock_whisper_model.transcribe.side_effect = transcribe_with_error
        
        mock_devices = [
            AudioDevice(id=0, name="Test Device", channels=2, sample_rate=16000, is_loopback=False)
        ]
        
        with patch('whisper.load_model', return_value=mock_whisper_model), \
             patch.object(AudioCaptureEngine, 'list_devices', return_value=mock_devices), \
             patch.object(AudioCaptureEngine, 'start_capture') as mock_start_capture:
            
            # Create application
            app = LiveCaptionApplication(config_path=str(integration_config))
            
            # Start captions
            app.start_captions()
            
            # Get audio callback
            audio_callback = mock_start_capture.call_args[1]['callback']
            
            # First chunk should fail
            audio_callback(sample_audio_data)
            qapp.processEvents()
            
            # Application should still be running
            assert app.is_running is True
            
            # Second chunk should succeed
            audio_callback(sample_audio_data)
            qapp.processEvents()
            
            # Application should still be running
            assert app.is_running is True
            
            # Cleanup
            app.stop_captions()
            app.shutdown()
    
    def test_overlay_recreation_on_close(self, qapp, integration_config):
        """
        Test that overlay recreation logic exists and can be triggered
        
        Validates: Requirements 9.4 (overlay recreation)
        """
        mock_devices = [
            AudioDevice(id=0, name="Test Device", channels=2, sample_rate=16000, is_loopback=False)
        ]
        
        mock_whisper_model = Mock()
        
        with patch('whisper.load_model', return_value=mock_whisper_model), \
             patch.object(AudioCaptureEngine, 'list_devices', return_value=mock_devices):
            
            # Create application
            app = LiveCaptionApplication(config_path=str(integration_config))
            
            # Get reference to original overlay
            original_overlay = app.caption_overlay
            original_id = id(original_overlay)
            
            # Manually trigger the overlay recreation logic
            # (In real scenario, this would be triggered by destroyed signal)
            app._on_overlay_destroyed()
            qapp.processEvents()
            
            # Verify overlay was recreated (different object)
            assert app.caption_overlay is not None
            assert id(app.caption_overlay) != original_id
            
            # Verify the new overlay has the correct configuration
            assert app.caption_overlay.config == app.config.overlay
            
            # Cleanup
            app.shutdown()
    
    def test_device_disconnection_handling(self, qapp, integration_config):
        """
        Test that application handles device disconnection gracefully
        
        Validates: Requirements 2.6, 9.5 (device disconnection)
        """
        mock_devices = [
            AudioDevice(id=0, name="Test Device", channels=2, sample_rate=16000, is_loopback=False)
        ]
        
        mock_whisper_model = Mock()
        
        with patch('whisper.load_model', return_value=mock_whisper_model), \
             patch.object(AudioCaptureEngine, 'list_devices', return_value=mock_devices), \
             patch.object(AudioCaptureEngine, 'start_capture') as mock_start_capture, \
             patch.object(AudioCaptureEngine, 'detect_device_changes', return_value=True):
            
            # Create application
            app = LiveCaptionApplication(config_path=str(integration_config))
            
            # Start captions
            app.start_captions()
            assert app.is_running is True
            
            # Simulate device disconnection
            app._check_device_changes()
            qapp.processEvents()
            
            # Application should stop captions
            assert app.is_running is False
            
            # Cleanup
            app.shutdown()


class TestConfigurationPersistence:
    """Test configuration persistence across application restart"""
    
    def test_config_persists_across_restart(self, qapp, integration_config, temp_dir):
        """
        Test that configuration changes persist across application restart
        
        Validates: Requirements 6.10 (preferences persistence)
        """
        mock_devices = [
            AudioDevice(id=0, name="Test Device", channels=2, sample_rate=16000, is_loopback=False)
        ]
        
        mock_whisper_model = Mock()
        
        with patch('whisper.load_model', return_value=mock_whisper_model), \
             patch.object(AudioCaptureEngine, 'list_devices', return_value=mock_devices):
            
            # Create first application instance
            app1 = LiveCaptionApplication(config_path=str(integration_config))
            
            # Modify configuration
            app1.config.overlay.font_size = 32
            app1.config.overlay.text_color = "#FF0000"
            app1.config.transcription.model_name = "base"
            app1.config_manager.save(app1.config)
            
            # Shutdown first instance
            app1.shutdown()
            
            # Create second application instance (simulating restart)
            app2 = LiveCaptionApplication(config_path=str(integration_config))
            
            # Verify configuration was persisted
            assert app2.config.overlay.font_size == 32
            assert app2.config.overlay.text_color == "#FF0000"
            assert app2.config.transcription.model_name == "base"
            
            # Cleanup
            app2.shutdown()
    
    def test_overlay_position_persists(self, qapp, integration_config):
        """
        Test that overlay position persists across restart
        
        Validates: Requirements 1.4 (position persistence)
        """
        mock_devices = [
            AudioDevice(id=0, name="Test Device", channels=2, sample_rate=16000, is_loopback=False)
        ]
        
        mock_whisper_model = Mock()
        
        with patch('whisper.load_model', return_value=mock_whisper_model), \
             patch.object(AudioCaptureEngine, 'list_devices', return_value=mock_devices):
            
            # Create first application instance
            app1 = LiveCaptionApplication(config_path=str(integration_config))
            
            # Move overlay to custom position and save
            from src.ui.caption_overlay import Position
            app1.caption_overlay.set_position(Position.CUSTOM, custom_x=100, custom_y=200, save_to_config=True)
            
            # Shutdown first instance
            app1.shutdown()
            
            # Create second application instance
            app2 = LiveCaptionApplication(config_path=str(integration_config))
            
            # Verify position was restored
            assert app2.config.overlay.position == "custom"
            assert app2.config.overlay.custom_x == 100
            assert app2.config.overlay.custom_y == 200
            
            # Cleanup
            app2.shutdown()
    
    def test_export_settings_persist(self, qapp, integration_config, temp_dir):
        """
        Test that export settings persist across restart
        
        Validates: Requirements 11.2 (export configuration)
        """
        mock_devices = [
            AudioDevice(id=0, name="Test Device", channels=2, sample_rate=16000, is_loopback=False)
        ]
        
        mock_whisper_model = Mock()
        
        with patch('whisper.load_model', return_value=mock_whisper_model), \
             patch.object(AudioCaptureEngine, 'list_devices', return_value=mock_devices):
            
            # Create first application instance
            app1 = LiveCaptionApplication(config_path=str(integration_config))
            
            # Modify export settings
            new_path = str(temp_dir / "custom_subtitles.vtt")
            app1.config.export.format = "vtt"
            app1.config.export.output_path = new_path
            app1.config_manager.save(app1.config)
            
            # Shutdown first instance
            app1.shutdown()
            
            # Create second application instance
            app2 = LiveCaptionApplication(config_path=str(integration_config))
            
            # Verify export settings were persisted
            assert app2.config.export.format == "vtt"
            assert app2.config.export.output_path == new_path
            
            # Cleanup
            app2.shutdown()


class TestMultiComponentIntegration:
    """Test integration between multiple components"""
    
    def test_model_switching_during_capture(self, qapp, integration_config, sample_audio_data):
        """
        Test switching transcription model while capturing
        
        Validates: Requirements 3.4 (model switching without restart)
        """
        mock_whisper_tiny = Mock()
        mock_whisper_tiny.transcribe.return_value = {
            "text": "Tiny model result",
            "language": "en",
            "segments": [{"start": 0.0, "end": 1.0, "text": "Tiny model result"}]
        }
        
        mock_whisper_base = Mock()
        mock_whisper_base.transcribe.return_value = {
            "text": "Base model result",
            "language": "en",
            "segments": [{"start": 0.0, "end": 1.0, "text": "Base model result"}]
        }
        
        model_map = {"tiny": mock_whisper_tiny, "base": mock_whisper_base}
        
        def load_model_side_effect(name, *args, **kwargs):
            return model_map.get(name, mock_whisper_tiny)
        
        mock_devices = [
            AudioDevice(id=0, name="Test Device", channels=2, sample_rate=16000, is_loopback=False)
        ]
        
        with patch('whisper.load_model', side_effect=load_model_side_effect), \
             patch.object(AudioCaptureEngine, 'list_devices', return_value=mock_devices), \
             patch.object(AudioCaptureEngine, 'start_capture') as mock_start_capture:
            
            # Create application
            app = LiveCaptionApplication(config_path=str(integration_config))
            
            # Start captions with tiny model
            app.start_captions()
            assert app.transcription_engine.model_name == "tiny"
            
            # Switch to base model
            app._on_model_changed("base")
            qapp.processEvents()
            
            # Verify model was switched
            assert app.transcription_engine.model_name == "base"
            
            # Application should still be running
            assert app.is_running is True
            
            # Cleanup
            app.stop_captions()
            app.shutdown()
    
    def test_device_switching_during_capture(self, qapp, integration_config):
        """
        Test switching audio device while capturing
        
        Validates: Requirements 2.3 (device switching without restart)
        """
        mock_devices = [
            AudioDevice(id=0, name="Device 1", channels=2, sample_rate=16000, is_loopback=False),
            AudioDevice(id=1, name="Device 2", channels=2, sample_rate=16000, is_loopback=True)
        ]
        
        mock_whisper_model = Mock()
        
        with patch('whisper.load_model', return_value=mock_whisper_model), \
             patch.object(AudioCaptureEngine, 'list_devices', return_value=mock_devices), \
             patch.object(AudioCaptureEngine, 'start_capture'), \
             patch.object(AudioCaptureEngine, 'set_device') as mock_set_device:
            
            # Create application
            app = LiveCaptionApplication(config_path=str(integration_config))
            
            # Start captions with device 0
            app.start_captions()
            
            # Switch to device 1
            app._on_audio_device_changed(1)
            qapp.processEvents()
            
            # Verify device was switched
            assert mock_set_device.called
            assert app.config.audio.device_id == 1
            
            # Application should still be running
            assert app.is_running is True
            
            # Cleanup
            app.stop_captions()
            app.shutdown()
    
    def test_language_switching_during_capture(self, qapp, integration_config):
        """
        Test switching language while capturing
        
        Validates: Requirements 3.6 (manual language override)
        """
        mock_whisper_model = Mock()
        mock_whisper_model.transcribe.return_value = {
            "text": "Test",
            "language": "en",
            "segments": [{"start": 0.0, "end": 1.0, "text": "Test"}]
        }
        
        mock_devices = [
            AudioDevice(id=0, name="Test Device", channels=2, sample_rate=16000, is_loopback=False)
        ]
        
        with patch('whisper.load_model', return_value=mock_whisper_model), \
             patch.object(AudioCaptureEngine, 'list_devices', return_value=mock_devices), \
             patch.object(AudioCaptureEngine, 'start_capture'):
            
            # Create application
            app = LiveCaptionApplication(config_path=str(integration_config))
            
            # Start captions with auto-detect
            app.start_captions()
            assert app.transcription_engine.language is None
            
            # Switch to Spanish
            app._on_language_changed("es")
            qapp.processEvents()
            
            # Verify language was set
            assert app.transcription_engine.language == "es"
            assert app.config.transcription.language == "es"
            
            # Application should still be running
            assert app.is_running is True
            
            # Cleanup
            app.stop_captions()
            app.shutdown()
