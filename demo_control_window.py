"""Demo script for ControlWindow"""

import sys
from PyQt6.QtWidgets import QApplication

from src.config.config_manager import Config, ConfigManager
from src.ui.control_window import ControlWindow
from src.audio.audio_capture import AudioCaptureEngine


def main():
    """Run control window demo"""
    # Create QApplication
    app = QApplication(sys.argv)
    
    # Create configuration
    config_manager = ConfigManager()
    config = config_manager.load()
    
    # Create control window
    window = ControlWindow(config, config_manager)
    
    # Populate audio devices
    audio_engine = AudioCaptureEngine(config.audio)
    devices = audio_engine.list_devices()
    window.populate_audio_devices(devices)
    
    # Connect signals for demo
    window.start_requested.connect(lambda: print("Start requested"))
    window.stop_requested.connect(lambda: print("Stop requested"))
    window.show_overlay_requested.connect(lambda: print("Show overlay requested"))
    window.hide_overlay_requested.connect(lambda: print("Hide overlay requested"))
    window.settings_requested.connect(lambda: print("Settings requested"))
    window.audio_device_changed.connect(lambda device_id: print(f"Audio device changed to: {device_id}"))
    window.model_changed.connect(lambda model: print(f"Model changed to: {model}"))
    window.language_changed.connect(lambda lang: print(f"Language changed to: {lang}"))
    
    # Show window
    window.show()
    
    print("Control window demo started")
    print("Features:")
    print("- Start/Stop buttons")
    print("- Audio device selection")
    print("- Model size selection")
    print("- Language selection")
    print("- Settings dialog (click Settings button)")
    print("- System tray icon (minimize to tray)")
    print("- Keyboard shortcuts (if 'keyboard' library is installed):")
    print(f"  - Start/Stop: {config.shortcuts.start_stop}")
    print(f"  - Show/Hide: {config.shortcuts.show_hide}")
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
