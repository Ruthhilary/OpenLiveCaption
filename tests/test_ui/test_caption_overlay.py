"""Unit tests for CaptionOverlay class"""

import pytest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
import sys

from src.ui.caption_overlay import CaptionOverlay, Position
from src.config.config_manager import OverlayConfig


@pytest.fixture(scope="module")
def qapp():
    """Create QApplication instance for tests"""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app


@pytest.fixture
def overlay_config():
    """Create default overlay configuration"""
    return OverlayConfig()


@pytest.fixture
def overlay(qapp, overlay_config):
    """Create CaptionOverlay instance"""
    overlay = CaptionOverlay(overlay_config)
    yield overlay
    overlay.close()


def test_overlay_window_flags(overlay):
    """Test that overlay has correct window flags for always-on-top and click-through"""
    flags = overlay.windowFlags()
    
    # Check for frameless window
    assert flags & Qt.WindowType.FramelessWindowHint
    
    # Check for always-on-top
    assert flags & Qt.WindowType.WindowStaysOnTopHint
    
    # Check for click-through
    assert flags & Qt.WindowType.WindowTransparentForInput
    
    # Check for tool window (no taskbar)
    assert flags & Qt.WindowType.Tool


def test_overlay_transparency(overlay):
    """Test that overlay has transparent background attribute"""
    assert overlay.testAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)


def test_update_caption_replace_mode(overlay):
    """Test caption update in replace mode"""
    overlay.config.scroll_mode = "replace"
    
    overlay.update_caption("First caption")
    assert overlay.caption_label.text() == "First caption"
    
    overlay.update_caption("Second caption")
    assert overlay.caption_label.text() == "Second caption"


def test_update_caption_scroll_mode(overlay):
    """Test caption update in scroll mode"""
    overlay.config.scroll_mode = "scroll"
    overlay.config.max_lines = 3
    
    overlay.update_caption("Line 1")
    assert "Line 1" in overlay.caption_label.text()
    
    overlay.update_caption("Line 2")
    assert "Line 1" in overlay.caption_label.text()
    assert "Line 2" in overlay.caption_label.text()
    
    overlay.update_caption("Line 3")
    assert "Line 1" in overlay.caption_label.text()
    assert "Line 2" in overlay.caption_label.text()
    assert "Line 3" in overlay.caption_label.text()
    
    # Adding 4th line should remove first line
    overlay.update_caption("Line 4")
    assert "Line 1" not in overlay.caption_label.text()
    assert "Line 2" in overlay.caption_label.text()
    assert "Line 3" in overlay.caption_label.text()
    assert "Line 4" in overlay.caption_label.text()


def test_max_lines_enforcement(overlay):
    """Test that maximum lines are enforced"""
    overlay.config.scroll_mode = "scroll"
    overlay.config.max_lines = 3
    
    # Add more than max_lines
    for i in range(5):
        overlay.update_caption(f"Line {i+1}")
    
    # Should only have last 3 lines
    assert len(overlay.caption_lines) == 3
    assert overlay.caption_lines == ["Line 3", "Line 4", "Line 5"]


def test_set_font(overlay):
    """Test font configuration"""
    overlay.set_font("Courier New", 32)
    
    assert overlay.config.font_family == "Courier New"
    assert overlay.config.font_size == 32
    assert overlay.caption_label.font().family() == "Courier New"
    assert overlay.caption_label.font().pointSize() == 32


def test_set_colors(overlay):
    """Test color configuration"""
    overlay.set_colors("#FF0000", "#0000FF")
    
    assert overlay.config.text_color == "#FF0000"
    assert overlay.config.background_color == "#0000FF"


def test_set_background_opacity(overlay):
    """Test background opacity configuration"""
    overlay.set_background_opacity(0.5)
    assert overlay.config.background_opacity == 0.5
    
    # Test clamping to valid range
    overlay.set_background_opacity(1.5)
    assert overlay.config.background_opacity == 1.0
    
    overlay.set_background_opacity(-0.5)
    assert overlay.config.background_opacity == 0.0


def test_set_position_top(overlay):
    """Test setting position to top"""
    overlay.set_position(Position.TOP)
    assert overlay.config.position == "top"
    assert overlay.y() == 0


def test_set_position_bottom(overlay):
    """Test setting position to bottom"""
    overlay.set_position(Position.BOTTOM)
    assert overlay.config.position == "bottom"


def test_set_position_custom(overlay):
    """Test setting custom position"""
    overlay.set_position(Position.CUSTOM, custom_x=100, custom_y=200)
    assert overlay.config.position == "custom"
    assert overlay.config.custom_x == 100
    assert overlay.config.custom_y == 200


def test_show_hide_overlay(overlay):
    """Test showing and hiding overlay"""
    overlay.show_overlay()
    assert overlay.isVisible()
    
    overlay.hide_overlay()
    assert not overlay.isVisible()


def test_clear_captions(overlay):
    """Test caption clearing"""
    overlay.update_caption("Test caption")
    assert overlay.caption_label.text() == "Test caption"
    
    overlay._clear_captions()
    assert overlay.caption_label.text() == ""
    assert len(overlay.caption_lines) == 0


def test_word_wrap_enabled(overlay):
    """Test that word wrap is enabled for text wrapping at word boundaries"""
    assert overlay.caption_label.wordWrap() is True
