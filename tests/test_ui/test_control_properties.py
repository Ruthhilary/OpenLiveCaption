"""Property-based tests for control interface"""

import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtTest import QTest
import sys
import time

from src.ui.control_window import ControlWindow
from src.ui.keyboard_shortcuts import KeyboardShortcutManager
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


# Feature: system-wide-live-captions, Property 23: Keyboard shortcuts trigger actions
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture], max_examples=100)
@given(
    action_type=st.sampled_from(['start_stop', 'show_hide'])
)
def test_keyboard_shortcuts_trigger_actions(qapp, config, config_manager, tmp_path, action_type):
    """
    For any configured keyboard shortcut, pressing that shortcut should trigger 
    the associated action (start/stop, show/hide).
    
    Validates: Requirements 6.8
    """
    # Create control window
    window = ControlWindow(config, config_manager)
    
    try:
        # Track if signal was emitted
        signal_emitted = {'value': False}
        
        def on_signal():
            signal_emitted['value'] = True
        
        # Connect to appropriate signal based on action type
        if action_type == 'start_stop':
            # Connect to both start and stop signals
            window.start_requested.connect(on_signal)
            window.stop_requested.connect(on_signal)
            
            # Trigger the shortcut callback directly
            window._on_shortcut_start_stop()
            
        elif action_type == 'show_hide':
            # Connect to both show and hide signals
            window.show_overlay_requested.connect(on_signal)
            window.hide_overlay_requested.connect(on_signal)
            
            # Trigger the shortcut callback directly
            window._on_shortcut_show_hide()
        
        # Process events to ensure signals are delivered
        qapp.processEvents()
        
        # Verify that the action was triggered
        assert signal_emitted['value'], f"Keyboard shortcut for {action_type} did not trigger action"
        
    finally:
        window.close()
        qapp.processEvents()


# Feature: system-wide-live-captions, Property 24: Minimize to tray on close
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture], max_examples=100)
@given(
    has_tray_icon=st.booleans()
)
def test_minimize_to_tray_on_close(qapp, config, config_manager, tmp_path, has_tray_icon):
    """
    For any close event on the main window, the Control_Interface should minimize 
    to the system tray rather than exiting the application.
    
    Validates: Requirements 6.9
    """
    # Create control window
    window = ControlWindow(config, config_manager)
    
    try:
        # Show the window first
        window.show()
        qapp.processEvents()
        
        # Configure tray icon visibility based on test parameter
        if not has_tray_icon:
            # Hide tray icon to test fallback behavior
            if window.tray_icon:
                window.tray_icon.hide()
        else:
            # Ensure tray icon is visible
            if window.tray_icon:
                window.tray_icon.show()
        
        qapp.processEvents()
        
        # Create a close event
        from PyQt6.QtGui import QCloseEvent
        close_event = QCloseEvent()
        
        # Send close event to window
        window.closeEvent(close_event)
        qapp.processEvents()
        
        # Verify behavior based on tray icon presence
        if has_tray_icon and window.tray_icon and window.tray_icon.isVisible():
            # Should minimize to tray (event ignored, window hidden)
            assert close_event.isAccepted() == False, "Close event should be ignored when tray icon is visible"
            assert not window.isVisible(), "Window should be hidden when minimizing to tray"
        else:
            # Should allow close (event accepted)
            assert close_event.isAccepted() == True, "Close event should be accepted when no tray icon"
        
    finally:
        # Force close for cleanup
        window.close()
        qapp.processEvents()


# Additional property test: Verify keyboard shortcut manager availability
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture], max_examples=50)
@given(
    dummy=st.just(None)  # Dummy parameter to make it a property test
)
def test_keyboard_shortcut_manager_exists(qapp, config, config_manager, tmp_path, dummy):
    """
    Verify that keyboard shortcut manager is properly initialized and available.
    
    This is a supporting property for Property 23.
    """
    # Create control window
    window = ControlWindow(config, config_manager)
    
    try:
        # Verify shortcut manager exists
        assert window.shortcut_manager is not None, "Keyboard shortcut manager should be initialized"
        assert isinstance(window.shortcut_manager, KeyboardShortcutManager), \
            "Shortcut manager should be instance of KeyboardShortcutManager"
        
        # Verify signals are connected
        assert window.shortcut_manager.start_stop_triggered is not None
        assert window.shortcut_manager.show_hide_triggered is not None
        
    finally:
        window.close()
        qapp.processEvents()


# Additional property test: Verify start/stop toggle behavior
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture], max_examples=100)
@given(
    initial_state=st.booleans()
)
def test_start_stop_shortcut_toggles_state(qapp, config, config_manager, tmp_path, initial_state):
    """
    Verify that the start/stop keyboard shortcut properly toggles between states.
    
    This is a supporting property for Property 23.
    """
    # Create control window
    window = ControlWindow(config, config_manager)
    
    try:
        # Set initial state
        window.set_status(initial_state)
        qapp.processEvents()
        
        # Trigger start/stop shortcut
        window._on_shortcut_start_stop()
        qapp.processEvents()
        
        # Verify state toggled
        assert window.is_running != initial_state, \
            f"Start/stop shortcut should toggle state from {initial_state} to {not initial_state}"
        
    finally:
        window.close()
        qapp.processEvents()


# Additional property test: Verify show/hide toggle behavior
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture], max_examples=100)
@given(
    initial_visibility=st.booleans()
)
def test_show_hide_shortcut_toggles_visibility(qapp, config, config_manager, tmp_path, initial_visibility):
    """
    Verify that the show/hide keyboard shortcut properly toggles overlay visibility.
    
    This is a supporting property for Property 23.
    """
    # Create control window
    window = ControlWindow(config, config_manager)
    
    try:
        # Set initial visibility state
        window.overlay_visible = initial_visibility
        if initial_visibility:
            window.overlay_button.setText("📊 Hide Overlay")
        else:
            window.overlay_button.setText("📊 Show Overlay")
        qapp.processEvents()
        
        # Trigger show/hide shortcut
        window._on_shortcut_show_hide()
        qapp.processEvents()
        
        # Verify visibility toggled
        assert window.overlay_visible != initial_visibility, \
            f"Show/hide shortcut should toggle visibility from {initial_visibility} to {not initial_visibility}"
        
    finally:
        window.close()
        qapp.processEvents()
