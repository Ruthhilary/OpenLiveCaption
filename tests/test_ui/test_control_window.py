"""Unit tests for ControlWindow"""

import pytest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
import sys

from src.ui.control_window import ControlWindow
from src.config.config_manager import Config, ConfigManager
from src.audio.audio_capture import AudioDevice


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
def control_window(qapp, config, config_manager):
    """Create ControlWindow instance for testing"""
    window = ControlWindow(config, config_manager)
    yield window
    window.close()


def test_control_window_creation(control_window):
    """Test that control window is created successfully"""
    assert control_window is not None
    assert control_window.windowTitle() == "OpenLiveCaption"
    assert not control_window.is_running


def test_start_stop_buttons(control_window):
    """Test start and stop button functionality"""
    # Initially, start button should be enabled, stop button disabled
    assert control_window.start_button.isEnabled()
    assert not control_window.stop_button.isEnabled()
    
    # Click start button
    control_window.start_button.click()
    
    # After start, start button should be disabled, stop button enabled
    assert not control_window.start_button.isEnabled()
    assert control_window.stop_button.isEnabled()
    assert control_window.is_running
    
    # Click stop button
    control_window.stop_button.click()
    
    # After stop, start button should be enabled, stop button disabled
    assert control_window.start_button.isEnabled()
    assert not control_window.stop_button.isEnabled()
    assert not control_window.is_running


def test_audio_device_population(control_window):
    """Test populating audio device dropdown"""
    devices = [
        AudioDevice(id=0, name="Microphone", channels=1, sample_rate=44100, is_loopback=False, is_default=True),
        AudioDevice(id=1, name="Speakers", channels=2, sample_rate=44100, is_loopback=True, is_default=False),
    ]
    
    control_window.populate_audio_devices(devices)
    
    # Check that devices were added
    assert control_window.audio_combo.count() == 2
    
    # Check that default device is selected
    assert control_window.audio_combo.currentIndex() == 0


def test_model_selection(control_window):
    """Test model size selection"""
    # Check that model combo has all options
    assert control_window.model_combo.count() == 5
    assert "tiny" in [control_window.model_combo.itemText(i) for i in range(control_window.model_combo.count())]
    assert "base" in [control_window.model_combo.itemText(i) for i in range(control_window.model_combo.count())]
    assert "small" in [control_window.model_combo.itemText(i) for i in range(control_window.model_combo.count())]
    assert "medium" in [control_window.model_combo.itemText(i) for i in range(control_window.model_combo.count())]
    assert "large" in [control_window.model_combo.itemText(i) for i in range(control_window.model_combo.count())]


def test_language_selection(control_window):
    """Test language selection"""
    # Check that language combo has options
    assert control_window.language_combo.count() > 0
    assert "Auto-detect" in [control_window.language_combo.itemText(i) for i in range(control_window.language_combo.count())]


def test_overlay_toggle(control_window):
    """Test overlay show/hide toggle"""
    # Initially overlay should be visible
    assert control_window.overlay_visible
    assert "Hide Overlay" in control_window.overlay_button.text()
    
    # Click toggle button
    control_window.overlay_button.click()
    
    # Overlay should now be hidden
    assert not control_window.overlay_visible
    assert "Show Overlay" in control_window.overlay_button.text()
    
    # Click toggle button again
    control_window.overlay_button.click()
    
    # Overlay should be visible again
    assert control_window.overlay_visible
    assert "Hide Overlay" in control_window.overlay_button.text()


def test_status_label_updates(control_window):
    """Test that status label updates correctly"""
    # Initially stopped
    assert "Stopped" in control_window.status_label.text()
    
    # Start captions
    control_window.start_button.click()
    assert "Running" in control_window.status_label.text()
    
    # Stop captions
    control_window.stop_button.click()
    assert "Stopped" in control_window.status_label.text()


def test_set_status_method(control_window):
    """Test set_status method"""
    # Set to running
    control_window.set_status(True)
    assert control_window.is_running
    assert not control_window.start_button.isEnabled()
    assert control_window.stop_button.isEnabled()
    
    # Set to stopped
    control_window.set_status(False)
    assert not control_window.is_running
    assert control_window.start_button.isEnabled()
    assert not control_window.stop_button.isEnabled()


def test_system_tray_creation(control_window):
    """Test that system tray icon is created"""
    assert control_window.tray_icon is not None
    assert control_window.tray_icon.isVisible()


def test_keyboard_shortcut_manager(control_window):
    """Test that keyboard shortcut manager is created"""
    assert control_window.shortcut_manager is not None


def test_signals_exist(control_window):
    """Test that all required signals exist"""
    # Check that signals are defined
    assert hasattr(control_window, 'start_requested')
    assert hasattr(control_window, 'stop_requested')
    assert hasattr(control_window, 'show_overlay_requested')
    assert hasattr(control_window, 'hide_overlay_requested')
    assert hasattr(control_window, 'settings_requested')
    assert hasattr(control_window, 'audio_device_changed')
    assert hasattr(control_window, 'model_changed')
    assert hasattr(control_window, 'language_changed')


def test_system_tray_menu_items(control_window):
    """Test that system tray menu has all required items"""
    assert control_window.tray_icon is not None
    
    # Get tray menu
    tray_menu = control_window.tray_icon.contextMenu()
    assert tray_menu is not None
    
    # Get all actions
    actions = tray_menu.actions()
    action_texts = [action.text() for action in actions if not action.isSeparator()]
    
    # Check that all required menu items exist
    assert "Start Captions" in action_texts
    assert "Stop Captions" in action_texts
    assert "Hide Overlay" in action_texts or "Show Overlay" in action_texts
    assert "Show Window" in action_texts
    assert "Settings" in action_texts
    assert "Exit" in action_texts


def test_system_tray_start_stop_actions(control_window):
    """Test system tray start/stop action states"""
    # Initially, start should be enabled, stop should be disabled
    assert control_window.tray_start_action.isEnabled()
    assert not control_window.tray_stop_action.isEnabled()
    
    # Start captions
    control_window.start_button.click()
    
    # Now start should be disabled, stop should be enabled
    assert not control_window.tray_start_action.isEnabled()
    assert control_window.tray_stop_action.isEnabled()
    
    # Stop captions
    control_window.stop_button.click()
    
    # Back to initial state
    assert control_window.tray_start_action.isEnabled()
    assert not control_window.tray_stop_action.isEnabled()


def test_system_tray_overlay_action_text(control_window):
    """Test system tray overlay action text updates"""
    # Initially overlay is visible, so action should say "Hide Overlay"
    assert control_window.tray_overlay_action.text() == "Hide Overlay"
    
    # Toggle overlay
    control_window.overlay_button.click()
    
    # Action should now say "Show Overlay"
    assert control_window.tray_overlay_action.text() == "Show Overlay"
    
    # Toggle back
    control_window.overlay_button.click()
    
    # Action should say "Hide Overlay" again
    assert control_window.tray_overlay_action.text() == "Hide Overlay"


def test_minimize_to_tray_on_close(control_window):
    """Test that closing window minimizes to tray instead of exiting"""
    from PyQt6.QtGui import QCloseEvent
    
    # Create a close event
    close_event = QCloseEvent()
    
    # Call closeEvent
    control_window.closeEvent(close_event)
    
    # Event should be ignored (not accepted) when tray icon is visible
    if control_window.tray_icon and control_window.tray_icon.isVisible():
        assert close_event.isAccepted() == False
        # Window should be hidden
        assert not control_window.isVisible()
    else:
        # If no tray icon, event should be accepted
        assert close_event.isAccepted() == True


def test_settings_button_functionality(control_window):
    """Test settings button opens settings dialog"""
    # We can't fully test dialog opening without mocking, but we can verify the button exists and is clickable
    assert control_window.settings_button is not None
    assert control_window.settings_button.isEnabled()
    assert "Settings" in control_window.settings_button.text()


def test_audio_device_signal_emission(control_window, qapp):
    """Test that audio device change emits signal"""
    signal_received = []
    
    def on_device_changed(device_id):
        signal_received.append(device_id)
    
    control_window.audio_device_changed.connect(on_device_changed)
    
    # Populate devices
    devices = [
        AudioDevice(id=5, name="Test Device", channels=2, sample_rate=44100, is_loopback=False, is_default=False),
    ]
    control_window.populate_audio_devices(devices)
    
    # Change selection
    control_window.audio_combo.setCurrentIndex(0)
    qapp.processEvents()
    
    # Signal should have been emitted
    assert len(signal_received) > 0
    assert signal_received[-1] == 5


def test_model_change_signal_emission(control_window, qapp):
    """Test that model change emits signal"""
    signal_received = []
    
    def on_model_changed(model_name):
        signal_received.append(model_name)
    
    control_window.model_changed.connect(on_model_changed)
    
    # Change model
    control_window.model_combo.setCurrentText("base")
    qapp.processEvents()
    
    # Signal should have been emitted
    assert len(signal_received) > 0
    assert signal_received[-1] == "base"


def test_language_change_signal_emission(control_window, qapp):
    """Test that language change emits signal"""
    signal_received = []
    
    def on_language_changed(lang_code):
        signal_received.append(lang_code)
    
    control_window.language_changed.connect(on_language_changed)
    
    # Change language to English (with emoji)
    control_window.language_combo.setCurrentText("English 🇺🇸 (en)")
    qapp.processEvents()
    
    # Signal should have been emitted with language code
    assert len(signal_received) > 0
    assert signal_received[-1] == "en"
    
    # Change to auto-detect
    signal_received.clear()
    control_window.language_combo.setCurrentText("Auto-detect")
    qapp.processEvents()
    
    # Signal should have been emitted with empty string
    assert len(signal_received) > 0
    assert signal_received[-1] == ""
