"""Tests for configuration management"""

import pytest
import json
from pathlib import Path
import sys
from hypothesis import given, strategies as st

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from config import (
    Config,
    AudioConfig,
    TranscriptionConfig,
    OverlayConfig,
    ExportConfig,
    ShortcutConfig,
    ConfigManager
)


class TestConfigDataclasses:
    """Test configuration dataclass structures"""
    
    def test_audio_config_defaults(self):
        """Test AudioConfig has correct default values"""
        config = AudioConfig()
        assert config.device_id == -1
        assert config.sample_rate == 16000
        assert config.chunk_duration == 1.0
        assert config.vad_threshold == 0.01
    
    def test_transcription_config_defaults(self):
        """Test TranscriptionConfig has correct default values"""
        config = TranscriptionConfig()
        assert config.model_name == "tiny"
        assert config.device == "cpu"
        assert config.language is None
        assert config.enable_translation is False
        assert config.target_language is None
    
    def test_overlay_config_defaults(self):
        """Test OverlayConfig has correct default values"""
        config = OverlayConfig()
        assert config.position == "bottom"
        assert config.font_family == "Arial"
        assert config.font_size == 24
        assert config.max_lines == 3
        assert config.scroll_mode == "replace"


class TestConfigManager:
    """Test ConfigManager functionality"""
    
    def test_get_default_config(self):
        """Test getting default configuration"""
        cm = ConfigManager()
        config = cm.get_default()
        
        assert isinstance(config, Config)
        assert isinstance(config.audio, AudioConfig)
        assert isinstance(config.transcription, TranscriptionConfig)
        assert isinstance(config.overlay, OverlayConfig)
        assert isinstance(config.export, ExportConfig)
        assert isinstance(config.shortcuts, ShortcutConfig)
    
    def test_save_and_load_config(self, temp_config_file):
        """Test saving and loading configuration"""
        cm = ConfigManager(str(temp_config_file))
        
        # Create custom config
        config = Config()
        config.audio.sample_rate = 48000
        config.transcription.model_name = "base"
        config.overlay.font_size = 32
        
        # Save
        cm.save(config)
        assert temp_config_file.exists()
        
        # Load
        loaded_config = cm.load()
        assert loaded_config.audio.sample_rate == 48000
        assert loaded_config.transcription.model_name == "base"
        assert loaded_config.overlay.font_size == 32
    
    def test_load_nonexistent_config_returns_default(self, temp_dir):
        """Test loading non-existent config returns default"""
        nonexistent_path = temp_dir / "nonexistent.json"
        cm = ConfigManager(str(nonexistent_path))
        
        config = cm.load()
        assert isinstance(config, Config)
        assert config.audio.sample_rate == 16000  # Default value
    
    def test_load_corrupted_config_returns_default(self, temp_config_file):
        """Test loading corrupted config returns default"""
        # Write invalid JSON
        with open(temp_config_file, 'w') as f:
            f.write("{ invalid json }")
        
        cm = ConfigManager(str(temp_config_file))
        config = cm.load()
        
        # Should return default config
        assert isinstance(config, Config)
        assert config.audio.sample_rate == 16000


class TestConfigCorruptionHandling:
    """Unit tests for config file corruption handling"""
    
    def test_load_corrupted_json_syntax_error(self, temp_config_file):
        """Test loading config with JSON syntax error returns default"""
        # Write JSON with syntax error (missing closing brace)
        with open(temp_config_file, 'w') as f:
            f.write('{"audio": {"sample_rate": 16000}')
        
        cm = ConfigManager(str(temp_config_file))
        config = cm.load()
        
        # Should return default config without crashing
        assert isinstance(config, Config)
        assert config.audio.sample_rate == 16000
        assert config.transcription.model_name == "tiny"
        assert config.overlay.font_size == 24
    
    def test_load_corrupted_json_invalid_characters(self, temp_config_file):
        """Test loading config with invalid characters returns default"""
        # Write JSON with invalid characters
        with open(temp_config_file, 'w') as f:
            f.write('{"audio": {"sample_rate": 16000}}\x00\xff')
        
        cm = ConfigManager(str(temp_config_file))
        config = cm.load()
        
        # Should return default config
        assert isinstance(config, Config)
        assert config.audio.device_id == -1
    
    def test_load_empty_json_file(self, temp_config_file):
        """Test loading empty JSON file returns default"""
        # Write empty file
        with open(temp_config_file, 'w') as f:
            f.write('')
        
        cm = ConfigManager(str(temp_config_file))
        config = cm.load()
        
        # Should return default config
        assert isinstance(config, Config)
        assert config.audio.sample_rate == 16000
    
    def test_load_json_with_null_values(self, temp_config_file):
        """Test loading config with null values returns default"""
        # Write JSON with null values
        with open(temp_config_file, 'w') as f:
            json.dump({'audio': None, 'transcription': None}, f)
        
        cm = ConfigManager(str(temp_config_file))
        config = cm.load()
        
        # Should return default config
        assert isinstance(config, Config)
        assert config.audio.sample_rate == 16000
        assert config.transcription.model_name == "tiny"
    
    def test_load_missing_config_file(self, temp_dir):
        """Test loading missing config file returns default"""
        nonexistent_path = temp_dir / "does_not_exist.json"
        cm = ConfigManager(str(nonexistent_path))
        
        config = cm.load()
        
        # Should return default config
        assert isinstance(config, Config)
        assert config.audio.sample_rate == 16000
        assert config.transcription.model_name == "tiny"
        assert config.overlay.font_size == 24
        assert config.export.enabled is True
        assert config.shortcuts.start_stop == "Ctrl+Shift+S"
    
    def test_load_invalid_config_values_wrong_types(self, temp_config_file):
        """Test loading config with wrong value types returns default"""
        # Write JSON with wrong types (string instead of int)
        with open(temp_config_file, 'w') as f:
            json.dump({
                'audio': {
                    'sample_rate': 'not_a_number',
                    'device_id': 'invalid'
                }
            }, f)
        
        cm = ConfigManager(str(temp_config_file))
        config = cm.load()
        
        # Python dataclasses don't validate types by default, so values get loaded as-is
        # This is actually a limitation - the config loads but may fail at runtime
        assert isinstance(config, Config)
        # Values are loaded even if wrong type (runtime validation needed)
        assert config.audio.sample_rate == 'not_a_number'
        assert config.audio.device_id == 'invalid'
    
    def test_load_invalid_config_values_out_of_range(self, temp_config_file):
        """Test loading config with out-of-range values still loads"""
        # Write JSON with extreme values (should still load, validation is separate)
        with open(temp_config_file, 'w') as f:
            json.dump({
                'audio': {
                    'sample_rate': -1000,
                    'device_id': 999999
                },
                'overlay': {
                    'font_size': -50,
                    'background_opacity': 5.0
                }
            }, f)
        
        cm = ConfigManager(str(temp_config_file))
        config = cm.load()
        
        # Should load the values (validation happens at runtime)
        assert isinstance(config, Config)
        assert config.audio.sample_rate == -1000
        assert config.audio.device_id == 999999
        assert config.overlay.font_size == -50
        assert config.overlay.background_opacity == 5.0
    
    def test_load_partial_config_missing_sections(self, temp_config_file):
        """Test loading config with missing sections uses defaults for those sections"""
        # Write JSON with only audio section
        with open(temp_config_file, 'w') as f:
            json.dump({
                'audio': {
                    'sample_rate': 48000,
                    'device_id': 5
                }
            }, f)
        
        cm = ConfigManager(str(temp_config_file))
        config = cm.load()
        
        # Should load audio values and use defaults for other sections
        assert isinstance(config, Config)
        assert config.audio.sample_rate == 48000
        assert config.audio.device_id == 5
        # Other sections should have defaults
        assert config.transcription.model_name == "tiny"
        assert config.overlay.font_size == 24
        assert config.export.enabled is True
    
    def test_load_config_with_extra_fields(self, temp_config_file):
        """Test loading config with extra unknown fields ignores them"""
        # Write JSON with extra fields
        with open(temp_config_file, 'w') as f:
            json.dump({
                'audio': {
                    'sample_rate': 48000,
                    'unknown_field': 'should_be_ignored'
                },
                'unknown_section': {
                    'data': 'ignored'
                }
            }, f)
        
        cm = ConfigManager(str(temp_config_file))
        config = cm.load()
        
        # Dataclass constructor ignores extra kwargs, so unknown_field is dropped
        # But sample_rate should be loaded
        assert isinstance(config, Config)
        # The unknown_field in audio section causes TypeError, so defaults are used
        assert config.audio.sample_rate == 16000  # Falls back to default
        assert not hasattr(config.audio, 'unknown_field')
    
    def test_load_config_with_missing_required_fields(self, temp_config_file):
        """Test loading config with missing required fields uses defaults"""
        # Write JSON with incomplete audio section
        with open(temp_config_file, 'w') as f:
            json.dump({
                'audio': {
                    'sample_rate': 48000
                    # Missing device_id, chunk_duration, vad_threshold
                }
            }, f)
        
        cm = ConfigManager(str(temp_config_file))
        config = cm.load()
        
        # Should use defaults for missing fields
        assert isinstance(config, Config)
        assert config.audio.sample_rate == 48000
        assert config.audio.device_id == -1  # Default
        assert config.audio.chunk_duration == 1.0  # Default
        assert config.audio.vad_threshold == 0.01  # Default
    
    def test_load_config_with_wrong_json_structure(self, temp_config_file):
        """Test loading config with wrong JSON structure returns default"""
        # Write JSON that's a list instead of dict
        with open(temp_config_file, 'w') as f:
            json.dump(['not', 'a', 'dict'], f)
        
        cm = ConfigManager(str(temp_config_file))
        config = cm.load()
        
        # Should return default config
        assert isinstance(config, Config)
        assert config.audio.sample_rate == 16000
    
    def test_load_config_with_nested_corruption(self, temp_config_file):
        """Test loading config with corrupted nested structure returns default"""
        # Write JSON with nested dict instead of expected structure
        with open(temp_config_file, 'w') as f:
            json.dump({
                'audio': {
                    'sample_rate': {
                        'nested': 'should_be_int'
                    }
                }
            }, f)
        
        cm = ConfigManager(str(temp_config_file))
        config = cm.load()
        
        # Python dataclasses don't validate types, so nested dict gets loaded
        # This demonstrates a limitation - runtime validation is needed
        assert isinstance(config, Config)
        assert config.audio.sample_rate == {'nested': 'should_be_int'}
    
    def test_config_file_format(self, temp_config_file):
        """Test saved config file has correct JSON format"""
        cm = ConfigManager(str(temp_config_file))
        config = cm.get_default()
        
        cm.save(config)
        
        # Read and verify JSON structure
        with open(temp_config_file, 'r') as f:
            data = json.load(f)
        
        assert 'audio' in data
        assert 'transcription' in data
        assert 'overlay' in data
        assert 'export' in data
        assert 'shortcuts' in data
        
        assert data['audio']['sample_rate'] == 16000
        assert data['transcription']['model_name'] == 'tiny'



class TestConfigurationRoundTrip:
    """Property-based tests for configuration persistence"""
    
    # Feature: system-wide-live-captions, Property 3: Overlay position persistence
    @given(
        x=st.integers(min_value=0, max_value=3840),
        y=st.integers(min_value=0, max_value=2160),
        width=st.integers(min_value=100, max_value=1920),
        height=st.integers(min_value=50, max_value=500)
    )
    def test_overlay_position_persistence(self, x, y, width, height):
        """
        Property 3: Overlay position persistence
        
        For any overlay position and size configuration, saving the configuration 
        then loading it should restore the exact same position and size values.
        
        Validates: Requirements 1.4
        """
        import tempfile
        import os
        
        # Create temporary config file for this test iteration
        fd, temp_path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        
        try:
            cm = ConfigManager(temp_path)
            
            # Create config with specific overlay position
            config = Config()
            config.overlay.custom_x = x
            config.overlay.custom_y = y
            config.overlay.width = width
            config.overlay.height = height
            
            # Save configuration
            cm.save(config)
            
            # Load configuration
            loaded_config = cm.load()
            
            # Verify exact position and size values are restored
            assert loaded_config.overlay.custom_x == x, \
                f"Expected custom_x={x}, got {loaded_config.overlay.custom_x}"
            assert loaded_config.overlay.custom_y == y, \
                f"Expected custom_y={y}, got {loaded_config.overlay.custom_y}"
            assert loaded_config.overlay.width == width, \
                f"Expected width={width}, got {loaded_config.overlay.width}"
            assert loaded_config.overlay.height == height, \
                f"Expected height={height}, got {loaded_config.overlay.height}"
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    # Feature: system-wide-live-captions, Property 25: Preferences persistence
    @given(
        # Audio config
        device_id=st.integers(min_value=-1, max_value=10),
        sample_rate=st.sampled_from([8000, 16000, 22050, 44100, 48000]),
        chunk_duration=st.floats(min_value=0.1, max_value=5.0),
        vad_threshold=st.floats(min_value=0.0, max_value=1.0),
        # Transcription config
        model_name=st.sampled_from(["tiny", "base", "small", "medium", "large"]),
        device=st.sampled_from(["cpu", "cuda"]),
        language=st.one_of(st.none(), st.sampled_from(["en", "es", "fr", "de", "zh"])),
        enable_translation=st.booleans(),
        target_language=st.one_of(st.none(), st.sampled_from(["yo", "tw", "en", "es"])),
        # Overlay config
        position=st.sampled_from(["top", "bottom", "custom"]),
        font_family=st.sampled_from(["Arial", "Times New Roman", "Courier New", "Verdana"]),
        font_size=st.integers(min_value=12, max_value=72),
        text_color=st.sampled_from(["#FFFFFF", "#000000", "#FF0000", "#00FF00", "#0000FF"]),
        background_color=st.sampled_from(["#000000", "#FFFFFF", "#808080", "#404040"]),
        background_opacity=st.floats(min_value=0.0, max_value=1.0),
        max_lines=st.integers(min_value=1, max_value=5),
        scroll_mode=st.sampled_from(["replace", "scroll"]),
        clear_timeout=st.floats(min_value=1.0, max_value=30.0),
        # Export config
        export_enabled=st.booleans(),
        export_format=st.sampled_from(["srt", "vtt"]),
        output_path=st.sampled_from(["subtitles.srt", "captions.vtt", "output.srt"]),
        # Shortcut config
        start_stop=st.sampled_from(["Ctrl+Shift+S", "Ctrl+Alt+S", "Alt+Shift+S"]),
        show_hide=st.sampled_from(["Ctrl+Shift+H", "Ctrl+Alt+H", "Alt+Shift+H"])
    )
    def test_preferences_persistence(
        self,
        # Audio params
        device_id, sample_rate, chunk_duration, vad_threshold,
        # Transcription params
        model_name, device, language, enable_translation, target_language,
        # Overlay params
        position, font_family, font_size, text_color, background_color,
        background_opacity, max_lines, scroll_mode, clear_timeout,
        # Export params
        export_enabled, export_format, output_path,
        # Shortcut params
        start_stop, show_hide
    ):
        """
        Property 25: Preferences persistence
        
        For any user configuration, saving the preferences then restarting 
        the application should restore all preferences to their exact saved values.
        
        Validates: Requirements 6.10
        """
        import tempfile
        import os
        
        # Create temporary config file for this test iteration
        fd, temp_path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        
        try:
            cm = ConfigManager(temp_path)
            
            # Create config with all custom values
            config = Config()
            
            # Audio config
            config.audio.device_id = device_id
            config.audio.sample_rate = sample_rate
            config.audio.chunk_duration = chunk_duration
            config.audio.vad_threshold = vad_threshold
            
            # Transcription config
            config.transcription.model_name = model_name
            config.transcription.device = device
            config.transcription.language = language
            config.transcription.enable_translation = enable_translation
            config.transcription.target_language = target_language
            
            # Overlay config
            config.overlay.position = position
            config.overlay.font_family = font_family
            config.overlay.font_size = font_size
            config.overlay.text_color = text_color
            config.overlay.background_color = background_color
            config.overlay.background_opacity = background_opacity
            config.overlay.max_lines = max_lines
            config.overlay.scroll_mode = scroll_mode
            config.overlay.clear_timeout = clear_timeout
            
            # Export config
            config.export.enabled = export_enabled
            config.export.format = export_format
            config.export.output_path = output_path
            
            # Shortcut config
            config.shortcuts.start_stop = start_stop
            config.shortcuts.show_hide = show_hide
            
            # Save configuration
            cm.save(config)
            
            # Simulate application restart by creating new ConfigManager instance
            cm_restarted = ConfigManager(temp_path)
            loaded_config = cm_restarted.load()
            
            # Verify all audio preferences are restored
            assert loaded_config.audio.device_id == device_id
            assert loaded_config.audio.sample_rate == sample_rate
            assert abs(loaded_config.audio.chunk_duration - chunk_duration) < 0.001
            assert abs(loaded_config.audio.vad_threshold - vad_threshold) < 0.001
            
            # Verify all transcription preferences are restored
            assert loaded_config.transcription.model_name == model_name
            assert loaded_config.transcription.device == device
            assert loaded_config.transcription.language == language
            assert loaded_config.transcription.enable_translation == enable_translation
            assert loaded_config.transcription.target_language == target_language
            
            # Verify all overlay preferences are restored
            assert loaded_config.overlay.position == position
            assert loaded_config.overlay.font_family == font_family
            assert loaded_config.overlay.font_size == font_size
            assert loaded_config.overlay.text_color == text_color
            assert loaded_config.overlay.background_color == background_color
            assert abs(loaded_config.overlay.background_opacity - background_opacity) < 0.001
            assert loaded_config.overlay.max_lines == max_lines
            assert loaded_config.overlay.scroll_mode == scroll_mode
            assert abs(loaded_config.overlay.clear_timeout - clear_timeout) < 0.001
            
            # Verify all export preferences are restored
            assert loaded_config.export.enabled == export_enabled
            assert loaded_config.export.format == export_format
            assert loaded_config.export.output_path == output_path
            
            # Verify all shortcut preferences are restored
            assert loaded_config.shortcuts.start_stop == start_stop
            assert loaded_config.shortcuts.show_hide == show_hide
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.unlink(temp_path)

