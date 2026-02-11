"""Unit tests for SettingsDialog"""

import pytest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
import sys

from src.ui.settings_dialog import SettingsDialog
from src.config.config_manager import Config, ConfigManager


@pytest.fixture(scope="module")
def qapp():
    """Create QApplication instance for tests"""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app


@pytest.fixture
def config():
    """Create test configuration"""
    return Config()


@pytest.fixture
def config_manager(tmp_path):
    """Create test configuration manager"""
    config_path = tmp_path / "test_config.json"
    return ConfigManager(str(config_path))


@pytest.fixture
def settings_dialog(qapp, config, config_manager):
    """Create SettingsDialog instance for testing"""
    dialog = SettingsDialog(config, config_manager)
    yield dialog
    dialog.close()


def test_settings_dialog_creation(settings_dialog):
    """Test that settings dialog is created successfully"""
    assert settings_dialog is not None
    assert settings_dialog.windowTitle() == "Settings"


def test_tab_widget_exists(settings_dialog):
    """Test that tab widget is created with all tabs"""
    assert settings_dialog.tab_widget is not None
    assert settings_dialog.tab_widget.count() == 5
    
    # Check tab names
    tab_names = [settings_dialog.tab_widget.tabText(i) for i in range(settings_dialog.tab_widget.count())]
    assert "Audio" in tab_names
    assert "Transcription" in tab_names
    assert "Overlay" in tab_names
    assert "Export" in tab_names
    assert "Shortcuts" in tab_names


def test_audio_tab_widgets(settings_dialog):
    """Test audio tab widgets"""
    assert settings_dialog.sample_rate_spin is not None
    assert settings_dialog.chunk_duration_spin is not None
    assert settings_dialog.vad_threshold_spin is not None
    
    # Check default values
    assert settings_dialog.sample_rate_spin.value() == 16000
    assert settings_dialog.chunk_duration_spin.value() == 1.0
    assert settings_dialog.vad_threshold_spin.value() == 0.01


def test_transcription_tab_widgets(settings_dialog):
    """Test transcription tab widgets"""
    assert settings_dialog.model_combo is not None
    assert settings_dialog.device_combo is not None
    assert settings_dialog.translation_check is not None
    assert settings_dialog.target_language_combo is not None
    
    # Check model options
    assert settings_dialog.model_combo.count() == 5


def test_overlay_tab_widgets(settings_dialog):
    """Test overlay tab widgets"""
    assert settings_dialog.position_combo is not None
    assert settings_dialog.custom_x_spin is not None
    assert settings_dialog.custom_y_spin is not None
    assert settings_dialog.font_family_edit is not None
    assert settings_dialog.font_size_spin is not None
    assert settings_dialog.text_color_edit is not None
    assert settings_dialog.bg_color_edit is not None
    assert settings_dialog.bg_opacity_spin is not None
    assert settings_dialog.max_lines_spin is not None
    assert settings_dialog.scroll_mode_combo is not None
    assert settings_dialog.clear_timeout_spin is not None


def test_export_tab_widgets(settings_dialog):
    """Test export tab widgets"""
    assert settings_dialog.export_enabled_check is not None
    assert settings_dialog.export_format_combo is not None
    assert settings_dialog.output_path_edit is not None


def test_shortcuts_tab_widgets(settings_dialog):
    """Test shortcuts tab widgets"""
    assert settings_dialog.start_stop_edit is not None
    assert settings_dialog.show_hide_edit is not None
    
    # Check default values
    assert settings_dialog.start_stop_edit.text() == "Ctrl+Shift+S"
    assert settings_dialog.show_hide_edit.text() == "Ctrl+Shift+H"


def test_translation_toggle(settings_dialog):
    """Test translation checkbox toggle"""
    # Initially, target language should be disabled if translation is off
    initial_translation_state = settings_dialog.translation_check.isChecked()
    initial_target_state = settings_dialog.target_language_combo.isEnabled()
    
    assert initial_target_state == initial_translation_state
    
    # Toggle translation
    settings_dialog.translation_check.setChecked(not initial_translation_state)
    
    # Target language should now have opposite state
    assert settings_dialog.target_language_combo.isEnabled() == (not initial_translation_state)


def test_export_toggle(settings_dialog):
    """Test export checkbox toggle"""
    # Initially, export widgets should match export enabled state
    initial_export_state = settings_dialog.export_enabled_check.isChecked()
    initial_format_state = settings_dialog.export_format_combo.isEnabled()
    initial_path_state = settings_dialog.output_path_edit.isEnabled()
    
    assert initial_format_state == initial_export_state
    assert initial_path_state == initial_export_state
    
    # Toggle export
    settings_dialog.export_enabled_check.setChecked(not initial_export_state)
    
    # Export widgets should now have opposite state
    assert settings_dialog.export_format_combo.isEnabled() == (not initial_export_state)
    assert settings_dialog.output_path_edit.isEnabled() == (not initial_export_state)


def test_position_toggle(settings_dialog):
    """Test position combo change"""
    # Set to custom position
    settings_dialog.position_combo.setCurrentText("custom")
    
    # Custom X and Y should be enabled
    assert settings_dialog.custom_x_spin.isEnabled()
    assert settings_dialog.custom_y_spin.isEnabled()
    
    # Set to top position
    settings_dialog.position_combo.setCurrentText("top")
    
    # Custom X and Y should be disabled
    assert not settings_dialog.custom_x_spin.isEnabled()
    assert not settings_dialog.custom_y_spin.isEnabled()


def test_save_settings(settings_dialog, config_manager, tmp_path):
    """Test saving settings"""
    # Modify some settings
    settings_dialog.sample_rate_spin.setValue(22050)
    settings_dialog.model_combo.setCurrentText("base")
    settings_dialog.font_size_spin.setValue(32)
    
    # Save settings
    settings_dialog._save_settings()
    
    # Load config and verify changes
    loaded_config = config_manager.load()
    assert loaded_config.audio.sample_rate == 22050
    assert loaded_config.transcription.model_name == "base"
    assert loaded_config.overlay.font_size == 32


def test_audio_settings_ranges(settings_dialog):
    """Test audio settings have correct ranges"""
    # Sample rate range
    assert settings_dialog.sample_rate_spin.minimum() == 8000
    assert settings_dialog.sample_rate_spin.maximum() == 48000
    
    # Chunk duration range
    assert settings_dialog.chunk_duration_spin.minimum() == 0.1
    assert settings_dialog.chunk_duration_spin.maximum() == 5.0
    
    # VAD threshold range
    assert settings_dialog.vad_threshold_spin.minimum() == 0.001
    assert settings_dialog.vad_threshold_spin.maximum() == 0.1


def test_transcription_device_options(settings_dialog):
    """Test transcription device options"""
    assert settings_dialog.device_combo.count() == 2
    device_options = [settings_dialog.device_combo.itemText(i) for i in range(settings_dialog.device_combo.count())]
    assert "cpu" in device_options
    assert "cuda" in device_options


def test_overlay_position_options(settings_dialog):
    """Test overlay position options"""
    position_options = [settings_dialog.position_combo.itemText(i) for i in range(settings_dialog.position_combo.count())]
    assert "top" in position_options
    assert "bottom" in position_options
    assert "custom" in position_options


def test_overlay_scroll_mode_options(settings_dialog):
    """Test overlay scroll mode options"""
    scroll_options = [settings_dialog.scroll_mode_combo.itemText(i) for i in range(settings_dialog.scroll_mode_combo.count())]
    assert "replace" in scroll_options
    assert "scroll" in scroll_options


def test_export_format_options(settings_dialog):
    """Test export format options"""
    format_options = [settings_dialog.export_format_combo.itemText(i) for i in range(settings_dialog.export_format_combo.count())]
    assert "srt" in format_options
    assert "vtt" in format_options


def test_color_fields_have_valid_colors(settings_dialog):
    """Test that color fields contain valid color values"""
    # Text color should be a valid hex color
    text_color = settings_dialog.text_color_edit.text()
    assert text_color.startswith("#")
    assert len(text_color) == 7  # #RRGGBB format
    
    # Background color should be a valid hex color
    bg_color = settings_dialog.bg_color_edit.text()
    assert bg_color.startswith("#")
    assert len(bg_color) == 7


def test_overlay_opacity_range(settings_dialog):
    """Test overlay opacity has correct range"""
    assert settings_dialog.bg_opacity_spin.minimum() == 0.0
    assert settings_dialog.bg_opacity_spin.maximum() == 1.0


def test_max_lines_range(settings_dialog):
    """Test max lines has correct range"""
    assert settings_dialog.max_lines_spin.minimum() == 1
    assert settings_dialog.max_lines_spin.maximum() == 10


def test_clear_timeout_range(settings_dialog):
    """Test clear timeout has correct range"""
    assert settings_dialog.clear_timeout_spin.minimum() == 0.0
    assert settings_dialog.clear_timeout_spin.maximum() == 60.0


def test_font_size_range(settings_dialog):
    """Test font size has correct range"""
    assert settings_dialog.font_size_spin.minimum() == 8
    assert settings_dialog.font_size_spin.maximum() == 72


def test_all_settings_persist(settings_dialog, config_manager):
    """Test that all settings are properly saved and loaded"""
    # Modify all settings
    settings_dialog.sample_rate_spin.setValue(22050)
    settings_dialog.chunk_duration_spin.setValue(2.0)
    settings_dialog.vad_threshold_spin.setValue(0.05)
    
    settings_dialog.model_combo.setCurrentText("small")
    settings_dialog.device_combo.setCurrentText("cuda")
    settings_dialog.translation_check.setChecked(True)
    settings_dialog.target_language_combo.setCurrentText("Spanish 🇪🇸 (es)")
    
    settings_dialog.position_combo.setCurrentText("custom")
    settings_dialog.custom_x_spin.setValue(100)
    settings_dialog.custom_y_spin.setValue(200)
    settings_dialog.font_family_edit.setText("Courier")
    settings_dialog.font_size_spin.setValue(28)
    settings_dialog.text_color_edit.setText("#FF0000")
    settings_dialog.bg_color_edit.setText("#0000FF")
    settings_dialog.bg_opacity_spin.setValue(0.5)
    settings_dialog.max_lines_spin.setValue(5)
    settings_dialog.scroll_mode_combo.setCurrentText("scroll")
    settings_dialog.clear_timeout_spin.setValue(10.0)
    
    settings_dialog.export_enabled_check.setChecked(True)
    settings_dialog.export_format_combo.setCurrentText("vtt")
    settings_dialog.output_path_edit.setText("test_output.vtt")
    
    settings_dialog.start_stop_edit.setText("Ctrl+Alt+S")
    settings_dialog.show_hide_edit.setText("Ctrl+Alt+H")
    
    # Save settings
    settings_dialog._save_settings()
    
    # Load config and verify all changes
    loaded_config = config_manager.load()
    
    # Audio settings
    assert loaded_config.audio.sample_rate == 22050
    assert loaded_config.audio.chunk_duration == 2.0
    assert loaded_config.audio.vad_threshold == 0.05
    
    # Transcription settings
    assert loaded_config.transcription.model_name == "small"
    assert loaded_config.transcription.device == "cuda"
    assert loaded_config.transcription.enable_translation == True
    assert loaded_config.transcription.target_language == "es"
    
    # Overlay settings
    assert loaded_config.overlay.position == "custom"
    assert loaded_config.overlay.custom_x == 100
    assert loaded_config.overlay.custom_y == 200
    assert loaded_config.overlay.font_family == "Courier"
    assert loaded_config.overlay.font_size == 28
    assert loaded_config.overlay.text_color == "#FF0000"
    assert loaded_config.overlay.background_color == "#0000FF"
    assert loaded_config.overlay.background_opacity == 0.5
    assert loaded_config.overlay.max_lines == 5
    assert loaded_config.overlay.scroll_mode == "scroll"
    assert loaded_config.overlay.clear_timeout == 10.0
    
    # Export settings
    assert loaded_config.export.enabled == True
    assert loaded_config.export.format == "vtt"
    assert loaded_config.export.output_path == "test_output.vtt"
    
    # Shortcut settings
    assert loaded_config.shortcuts.start_stop == "Ctrl+Alt+S"
    assert loaded_config.shortcuts.show_hide == "Ctrl+Alt+H"


def test_dialog_buttons_exist(settings_dialog):
    """Test that dialog has OK, Apply, and Cancel buttons"""
    # Find buttons by iterating through dialog's children
    buttons = settings_dialog.findChildren(pytest.importorskip("PyQt6.QtWidgets").QPushButton)
    button_texts = [btn.text() for btn in buttons]
    
    assert "OK" in button_texts
    assert "Apply" in button_texts
    assert "Cancel" in button_texts
