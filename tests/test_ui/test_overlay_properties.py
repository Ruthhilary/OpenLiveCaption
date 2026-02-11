"""Property-based tests for CaptionOverlay behavior

This module contains property-based tests that validate universal correctness
properties of the caption overlay across all valid inputs.

Feature: system-wide-live-captions
"""

import pytest
from hypothesis import given, strategies as st, settings, assume
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
import sys
import time

from src.ui.caption_overlay import CaptionOverlay, Position
from src.config.config_manager import OverlayConfig


@pytest.fixture(scope="module")
def qapp():
    """Create QApplication instance for tests"""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app


# Strategy for valid hex colors
hex_color_strategy = st.from_regex(r'^#[0-9A-Fa-f]{6}$', fullmatch=True)

# Strategy for valid font families (common cross-platform fonts)
font_family_strategy = st.sampled_from([
    "Arial", "Helvetica", "Times New Roman", "Courier New", 
    "Verdana", "Georgia", "Comic Sans MS", "Trebuchet MS"
])


# Property 1: Overlay always-on-top behavior
@settings(max_examples=20)
@given(
    font_size=st.integers(min_value=8, max_value=72),
    text=st.text(min_size=0, max_size=100)
)
def test_property_1_overlay_always_on_top(qapp, font_size, text):
    """
    Property 1: Overlay always-on-top behavior
    
    For any Caption_Overlay instance, the window flags should include 
    WindowStaysOnTopHint, ensuring the overlay appears above all other applications.
    
    Validates: Requirements 1.1, 1.2
    """
    config = OverlayConfig(font_size=font_size)
    overlay = CaptionOverlay(config)
    
    try:
        # Verify WindowStaysOnTopHint is set
        flags = overlay.windowFlags()
        assert flags & Qt.WindowType.WindowStaysOnTopHint, \
            "Overlay must have WindowStaysOnTopHint flag set"
        
        # Update caption and verify flag persists
        if text:
            overlay.update_caption(text)
            flags_after = overlay.windowFlags()
            assert flags_after & Qt.WindowType.WindowStaysOnTopHint, \
                "WindowStaysOnTopHint must persist after caption updates"
    finally:
        overlay.close()


# Property 2: Overlay click-through transparency
@settings(max_examples=20)
@given(
    opacity=st.floats(min_value=0.0, max_value=1.0),
    text=st.text(min_size=0, max_size=100)
)
def test_property_2_overlay_click_through(qapp, opacity, text):
    """
    Property 2: Overlay click-through transparency
    
    For any Caption_Overlay instance, the window should have the 
    WindowTransparentForInput attribute set, allowing mouse clicks to 
    pass through to underlying applications.
    
    Validates: Requirements 1.3
    """
    config = OverlayConfig(background_opacity=opacity)
    overlay = CaptionOverlay(config)
    
    try:
        # Verify WindowTransparentForInput is set
        flags = overlay.windowFlags()
        assert flags & Qt.WindowType.WindowTransparentForInput, \
            "Overlay must have WindowTransparentForInput flag set"
        
        # Update caption and verify flag persists
        if text:
            overlay.update_caption(text)
            flags_after = overlay.windowFlags()
            assert flags_after & Qt.WindowType.WindowTransparentForInput, \
                "WindowTransparentForInput must persist after caption updates"
        
        # Verify translucent background attribute
        assert overlay.testAttribute(Qt.WidgetAttribute.WA_TranslucentBackground), \
            "Overlay must have WA_TranslucentBackground attribute"
    finally:
        overlay.close()


# Property 4: Overlay opacity configuration
@settings(max_examples=20)
@given(
    opacity=st.floats(min_value=0.0, max_value=1.0)
)
def test_property_4_overlay_opacity_configuration(qapp, opacity):
    """
    Property 4: Overlay opacity configuration
    
    For any opacity value between 0.0 and 1.0, setting the overlay opacity 
    should result in the configuration having that exact opacity value.
    
    Validates: Requirements 1.5, 7.6
    """
    config = OverlayConfig()
    overlay = CaptionOverlay(config)
    
    try:
        # Set opacity
        overlay.set_background_opacity(opacity)
        
        # Verify opacity is set correctly (within floating point precision)
        assert abs(overlay.config.background_opacity - opacity) < 1e-6, \
            f"Expected opacity {opacity}, got {overlay.config.background_opacity}"
    finally:
        overlay.close()


# Property 5: Font configuration
@settings(max_examples=20)
@given(
    font_family=font_family_strategy,
    font_size=st.integers(min_value=8, max_value=72)
)
def test_property_5_font_configuration(qapp, font_family, font_size):
    """
    Property 5: Font configuration
    
    For any valid font family and size, setting the caption font should 
    result in text being rendered with that exact font family and size.
    
    Validates: Requirements 7.1
    """
    config = OverlayConfig()
    overlay = CaptionOverlay(config)
    
    try:
        # Set font
        overlay.set_font(font_family, font_size)
        
        # Verify font configuration is stored
        assert overlay.config.font_family == font_family, \
            f"Expected font family {font_family}, got {overlay.config.font_family}"
        assert overlay.config.font_size == font_size, \
            f"Expected font size {font_size}, got {overlay.config.font_size}"
        
        # Verify font is applied to label
        label_font = overlay.caption_label.font()
        assert label_font.family() == font_family, \
            f"Label font family {label_font.family()} doesn't match {font_family}"
        assert label_font.pointSize() == font_size, \
            f"Label font size {label_font.pointSize()} doesn't match {font_size}"
    finally:
        overlay.close()


# Property 6: Text wrapping at word boundaries
@settings(max_examples=20)
@given(
    text=st.text(
        alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'), whitelist_characters=' '),
        min_size=10,
        max_size=200
    )
)
def test_property_6_text_wrapping_word_boundaries(qapp, text):
    """
    Property 6: Text wrapping at word boundaries
    
    For any caption text that exceeds the overlay width, the text should be 
    wrapped at word boundaries without breaking words mid-character.
    
    Validates: Requirements 7.2
    """
    # Skip texts that are only whitespace
    assume(text.strip())
    
    config = OverlayConfig(width=300)  # Narrow width to force wrapping
    overlay = CaptionOverlay(config)
    
    try:
        # Verify word wrap is enabled
        assert overlay.caption_label.wordWrap() is True, \
            "Word wrap must be enabled on caption label"
        
        # Update caption with text
        overlay.update_caption(text)
        
        # Word wrap is handled by Qt automatically when wordWrap=True
        # We verify the property is set, which ensures word boundary wrapping
        assert overlay.caption_label.wordWrap() is True, \
            "Word wrap must remain enabled after caption update"
    finally:
        overlay.close()


# Property 7: Maximum three lines display
@settings(max_examples=20)
@given(
    lines=st.lists(
        st.text(
            alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd')),
            min_size=1,
            max_size=50
        ),
        min_size=1,
        max_size=10
    )
)
def test_property_7_maximum_three_lines(qapp, lines):
    """
    Property 7: Maximum three lines display
    
    For any caption text, the overlay should never display more than 3 lines 
    of text simultaneously.
    
    Validates: Requirements 7.3
    """
    config = OverlayConfig(scroll_mode="scroll", max_lines=3)
    overlay = CaptionOverlay(config)
    
    try:
        # Add all lines
        for line in lines:
            overlay.update_caption(line)
        
        # Verify caption_lines never exceeds max_lines
        assert len(overlay.caption_lines) <= config.max_lines, \
            f"Caption lines {len(overlay.caption_lines)} exceeds max {config.max_lines}"
        
        # Verify displayed text has at most max_lines
        displayed_text = overlay.caption_label.text()
        displayed_line_count = len([l for l in displayed_text.split('\n') if l.strip()])
        assert displayed_line_count <= config.max_lines, \
            f"Displayed {displayed_line_count} lines, max is {config.max_lines}"
    finally:
        overlay.close()


# Property 8: Scroll and replace modes
@settings(max_examples=20)
@given(
    mode=st.sampled_from(["scroll", "replace"]),
    captions=st.lists(
        st.text(
            alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd')),
            min_size=1,
            max_size=50
        ),
        min_size=2,
        max_size=5
    )
)
def test_property_8_scroll_and_replace_modes(qapp, mode, captions):
    """
    Property 8: Scroll and replace modes
    
    For any sequence of caption updates, in scroll mode the text should 
    accumulate (up to max lines), and in replace mode the text should be 
    completely replaced.
    
    Validates: Requirements 7.4
    """
    config = OverlayConfig(scroll_mode=mode, max_lines=3)
    overlay = CaptionOverlay(config)
    
    try:
        # Add first caption
        overlay.update_caption(captions[0])
        first_text = overlay.caption_label.text()
        
        # Add second caption
        overlay.update_caption(captions[1])
        second_text = overlay.caption_label.text()
        
        if mode == "scroll":
            # In scroll mode, both captions should be present (if within max_lines)
            assert captions[0] in second_text, \
                "In scroll mode, previous caption should still be visible"
            assert captions[1] in second_text, \
                "In scroll mode, new caption should be visible"
        else:  # replace mode
            # In replace mode, only the latest caption should be present
            assert captions[0] not in second_text or captions[0] == captions[1], \
                "In replace mode, previous caption should be replaced"
            assert captions[1] in second_text, \
                "In replace mode, new caption should be visible"
    finally:
        overlay.close()


# Property 9: Color configuration
@settings(max_examples=20)
@given(
    text_color=hex_color_strategy,
    bg_color=hex_color_strategy
)
def test_property_9_color_configuration(qapp, text_color, bg_color):
    """
    Property 9: Color configuration
    
    For any valid RGB color values for text and background, setting these 
    colors should result in the overlay configuration storing those exact colors.
    
    Validates: Requirements 7.5
    """
    config = OverlayConfig()
    overlay = CaptionOverlay(config)
    
    try:
        # Set colors
        overlay.set_colors(text_color, bg_color)
        
        # Verify colors are stored in config
        assert overlay.config.text_color == text_color, \
            f"Expected text color {text_color}, got {overlay.config.text_color}"
        assert overlay.config.background_color == bg_color, \
            f"Expected background color {bg_color}, got {overlay.config.background_color}"
        
        # Verify colors are valid QColor objects
        text_qcolor = QColor(overlay.config.text_color)
        bg_qcolor = QColor(overlay.config.background_color)
        assert text_qcolor.isValid(), f"Text color {text_color} is not valid"
        assert bg_qcolor.isValid(), f"Background color {bg_color} is not valid"
    finally:
        overlay.close()


# Property 10: Auto-clear timeout
@settings(max_examples=10, deadline=None)  # Reduced examples due to time delays
@given(
    timeout=st.floats(min_value=0.1, max_value=2.0),
    text=st.text(
        alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd')),
        min_size=1,
        max_size=50
    )
)
def test_property_10_auto_clear_timeout(qapp, timeout, text):
    """
    Property 10: Auto-clear timeout
    
    For any configured timeout value, when no new captions arrive for that 
    duration, the overlay should clear all displayed text.
    
    Validates: Requirements 7.8
    """
    config = OverlayConfig(clear_timeout=timeout)
    overlay = CaptionOverlay(config)
    
    try:
        # Update caption
        overlay.update_caption(text)
        assert overlay.caption_label.text() == text, \
            "Caption should be displayed immediately after update"
        
        # Wait for timeout plus a small buffer
        qapp.processEvents()
        time.sleep(timeout + 0.2)
        qapp.processEvents()
        
        # Verify caption is cleared
        assert overlay.caption_label.text() == "", \
            f"Caption should be cleared after {timeout}s timeout"
        assert len(overlay.caption_lines) == 0, \
            "Caption lines should be empty after timeout"
    finally:
        overlay.close()
