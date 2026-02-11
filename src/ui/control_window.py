"""Control window for managing caption system"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QComboBox, QLabel, QSystemTrayIcon, QMenu, QDialog
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QAction
from typing import Optional, List
import sys

from src.config.config_manager import Config, ConfigManager
from src.audio.audio_capture import AudioDevice
from src.ui.keyboard_shortcuts import KeyboardShortcutManager


class ControlWindow(QMainWindow):
    """
    Main control window for OpenLiveCaption.
    
    Provides UI controls for starting/stopping captions, selecting audio sources,
    configuring models, and accessing settings.
    """
    
    # Signals
    start_requested = pyqtSignal()
    stop_requested = pyqtSignal()
    show_overlay_requested = pyqtSignal()
    hide_overlay_requested = pyqtSignal()
    settings_requested = pyqtSignal()
    audio_device_changed = pyqtSignal(int)  # device_id
    model_changed = pyqtSignal(str)  # model_name
    language_changed = pyqtSignal(str)  # language_code
    
    def __init__(self, config: Config, config_manager: ConfigManager, parent: Optional[QWidget] = None):
        """
        Initialize control window.
        
        Args:
            config: Application configuration
            config_manager: Configuration manager for saving settings
            parent: Optional parent widget
        """
        super().__init__(parent)
        
        self.config = config
        self.config_manager = config_manager
        self.is_running = False
        self.overlay_visible = True
        
        # Set up window
        self.setWindowTitle("OpenLiveCaption")
        self.setMinimumSize(400, 300)
        self.resize(450, 350)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Status label
        self.status_label = QLabel("● Stopped")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #888;")
        main_layout.addWidget(self.status_label)
        
        # Start/Stop buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.start_button = QPushButton("Start Captions")
        self.start_button.setMinimumHeight(40)
        self.start_button.clicked.connect(self._on_start_clicked)
        button_layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton("Stop Captions")
        self.stop_button.setMinimumHeight(40)
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self._on_stop_clicked)
        button_layout.addWidget(self.stop_button)
        
        main_layout.addLayout(button_layout)
        
        # Audio source selection
        audio_label = QLabel("Audio Source:")
        audio_label.setStyleSheet("font-weight: bold;")
        main_layout.addWidget(audio_label)
        
        self.audio_combo = QComboBox()
        self.audio_combo.setMinimumHeight(35)
        self.audio_combo.currentIndexChanged.connect(self._on_audio_device_changed)
        main_layout.addWidget(self.audio_combo)
        
        # Model size selection
        model_label = QLabel("Model Size:")
        model_label.setStyleSheet("font-weight: bold;")
        main_layout.addWidget(model_label)
        
        self.model_combo = QComboBox()
        self.model_combo.setMinimumHeight(35)
        self.model_combo.addItems(["tiny", "base", "small", "medium", "large"])
        self.model_combo.setCurrentText(config.transcription.model_name)
        self.model_combo.currentTextChanged.connect(self._on_model_changed)
        main_layout.addWidget(self.model_combo)
        
        # Language selection
        language_label = QLabel("Language:")
        language_label.setStyleSheet("font-weight: bold;")
        main_layout.addWidget(language_label)
        
        self.language_combo = QComboBox()
        self.language_combo.setMinimumHeight(35)
        self.language_combo.addItems([
            "Auto-detect",
            # Most common languages
            "English 🇺🇸 (en)",
            "Spanish 🇪🇸 (es)",
            "French 🇫🇷 (fr)",
            "German 🇩🇪 (de)",
            "Chinese 🇨🇳 (zh)",
            "Hindi 🇮🇳 (hi)",
            "Arabic 🇸🇦 (ar)",
            "Portuguese 🇵🇹 (pt)",
            "Russian 🇷🇺 (ru)",
            "Japanese 🇯🇵 (ja)",
            "Korean 🇰🇷 (ko)",
            "Italian 🇮🇹 (it)",
            # Additional European languages
            "Dutch 🇳🇱 (nl)",
            "Polish 🇵🇱 (pl)",
            "Turkish 🇹🇷 (tr)",
            "Vietnamese 🇻🇳 (vi)",
            "Thai 🇹🇭 (th)",
            "Persian 🇮🇷 (fa)",
            "Hebrew 🇮🇱 (he)",
            "Ukrainian 🇺🇦 (uk)",
            "Greek 🇬🇷 (el)",
            "Swedish 🇸🇪 (sv)",
            "Danish 🇩🇰 (da)",
            "Finnish 🇫🇮 (fi)",
            "Norwegian 🇳🇴 (no)",
            "Czech 🇨🇿 (cs)",
            "Hungarian 🇭🇺 (hu)",
            "Romanian 🇷🇴 (ro)",
            "Bulgarian 🇧🇬 (bg)",
            "Serbian 🇷🇸 (sr)",
            "Croatian 🇭🇷 (hr)",
            "Slovak 🇸🇰 (sk)",
            "Slovenian 🇸🇮 (sl)",
            "Lithuanian 🇱🇹 (lt)",
            "Latvian 🇱🇻 (lv)",
            "Estonian 🇪🇪 (et)",
            "Maltese 🇲🇹 (mt)",
            "Irish 🇮🇪 (ga)",
            "Welsh 🏴󠁧󠁢󠁷󠁬󠁳󠁿 (cy)",
            "Icelandic 🇮🇸 (is)",
            # Asian languages
            "Indonesian 🇮🇩 (id)",
            "Malay 🇲🇾 (ms)",
            "Filipino 🇵🇭 (fil)",
            "Bengali 🇧🇩 (bn)",
            "Urdu 🇵🇰 (ur)",
            # African languages
            "Yoruba 🇳🇬 (yo)",
            "Twi 🇬🇭 (twi)",
            "Swahili 🇰🇪 (sw)",
            "Afrikaans 🇿🇦 (af)"
        ])
        self.language_combo.currentTextChanged.connect(self._on_language_changed)
        main_layout.addWidget(self.language_combo)
        
        # Settings and overlay buttons
        bottom_button_layout = QHBoxLayout()
        bottom_button_layout.setSpacing(10)
        
        self.settings_button = QPushButton("⚙ Settings")
        self.settings_button.setMinimumHeight(35)
        self.settings_button.clicked.connect(self._on_settings_clicked)
        bottom_button_layout.addWidget(self.settings_button)
        
        self.overlay_button = QPushButton("📊 Hide Overlay")
        self.overlay_button.setMinimumHeight(35)
        self.overlay_button.clicked.connect(self._on_overlay_toggle_clicked)
        bottom_button_layout.addWidget(self.overlay_button)
        
        main_layout.addLayout(bottom_button_layout)
        
        # Add stretch to push everything to the top
        main_layout.addStretch()
        
        # System tray icon
        self.tray_icon: Optional[QSystemTrayIcon] = None
        self._setup_system_tray()
        
        # Keyboard shortcuts
        self.shortcut_manager = KeyboardShortcutManager(self)
        self.shortcut_manager.start_stop_triggered.connect(self._on_shortcut_start_stop)
        self.shortcut_manager.show_hide_triggered.connect(self._on_shortcut_show_hide)
        self._setup_keyboard_shortcuts()
    
    def _on_start_clicked(self):
        """Handle start button click"""
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.is_running = True
        self._update_status_label()
        self._update_tray_menu()
        self.start_requested.emit()
    
    def _on_stop_clicked(self):
        """Handle stop button click"""
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.is_running = False
        self._update_status_label()
        self._update_tray_menu()
        self.stop_requested.emit()
    
    def _on_audio_device_changed(self, index: int):
        """Handle audio device selection change"""
        if index >= 0:
            device_id = self.audio_combo.itemData(index)
            if device_id is not None:
                self.audio_device_changed.emit(device_id)
    
    def _on_model_changed(self, model_name: str):
        """Handle model size selection change"""
        if model_name:
            self.model_changed.emit(model_name)
    
    def _on_language_changed(self, language_text: str):
        """Handle language selection change"""
        # Extract language code from text (e.g., "English (en)" -> "en")
        if language_text == "Auto-detect":
            self.language_changed.emit("")  # Empty string for auto-detect
        else:
            # Extract code from parentheses
            if "(" in language_text and ")" in language_text:
                lang_code = language_text.split("(")[1].split(")")[0]
                self.language_changed.emit(lang_code)
    
    def _on_settings_clicked(self):
        """Handle settings button click"""
        from src.ui.settings_dialog import SettingsDialog
        
        dialog = SettingsDialog(self.config, self.config_manager, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Settings were saved, update keyboard shortcuts
            self.update_keyboard_shortcuts()
            # Emit signal for other components
            self.settings_requested.emit()
    
    def _on_overlay_toggle_clicked(self):
        """Handle overlay show/hide button click"""
        if self.overlay_visible:
            self.overlay_button.setText("📊 Show Overlay")
            self.overlay_visible = False
            self.hide_overlay_requested.emit()
        else:
            self.overlay_button.setText("📊 Hide Overlay")
            self.overlay_visible = True
            self.show_overlay_requested.emit()
        self._update_tray_menu()
    
    def _update_status_label(self):
        """Update status label based on current state"""
        if self.is_running:
            self.status_label.setText("● Running")
            self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #4CAF50;")
        else:
            self.status_label.setText("● Stopped")
            self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #888;")
    
    def populate_audio_devices(self, devices: List[AudioDevice]):
        """
        Populate audio device dropdown with available devices.
        
        Args:
            devices: List of available audio devices
        """
        self.audio_combo.clear()
        
        for device in devices:
            # Format device name with type indicator
            device_type = " [Loopback]" if device.is_loopback else " [Microphone]"
            default_indicator = " (Default)" if device.is_default else ""
            display_name = f"{device.name}{device_type}{default_indicator}"
            
            self.audio_combo.addItem(display_name, device.id)
            
            # Select default device
            if device.is_default or device.id == self.config.audio.device_id:
                self.audio_combo.setCurrentIndex(self.audio_combo.count() - 1)
    
    def set_status(self, is_running: bool):
        """
        Set the running status of the application.
        
        Args:
            is_running: True if captions are running, False otherwise
        """
        self.is_running = is_running
        self.start_button.setEnabled(not is_running)
        self.stop_button.setEnabled(is_running)
        self._update_status_label()
        self._update_tray_menu()
    
    def closeEvent(self, event):
        """
        Handle window close event.
        
        Minimizes to tray instead of exiting (if tray icon is set up).
        """
        if self.tray_icon and self.tray_icon.isVisible():
            # Minimize to tray instead of closing
            event.ignore()
            self.hide()
            if self.tray_icon:
                self.tray_icon.showMessage(
                    "OpenLiveCaption",
                    "Application minimized to tray",
                    QSystemTrayIcon.MessageIcon.Information,
                    2000
                )
        else:
            # No tray icon, allow close
            event.accept()
    
    def _setup_system_tray(self):
        """Set up system tray icon and menu"""
        # Create tray icon
        self.tray_icon = QSystemTrayIcon(self)
        
        # Set icon (use default icon for now, can be customized later)
        # For now, use a simple text-based icon
        from PyQt6.QtGui import QPixmap, QPainter, QFont as QGuiFont, QColor as QGuiColor
        
        # Create a simple icon with "OLC" text
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw background circle
        painter.setBrush(QGuiColor(76, 175, 80))  # Green color
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(2, 2, 60, 60)
        
        # Draw text
        painter.setPen(QGuiColor(255, 255, 255))
        font = QGuiFont("Arial", 16, QGuiFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "OLC")
        painter.end()
        
        icon = QIcon(pixmap)
        self.tray_icon.setIcon(icon)
        
        # Create tray menu
        tray_menu = QMenu()
        
        # Start/Stop action
        self.tray_start_action = QAction("Start Captions", self)
        self.tray_start_action.triggered.connect(self._on_start_clicked)
        tray_menu.addAction(self.tray_start_action)
        
        self.tray_stop_action = QAction("Stop Captions", self)
        self.tray_stop_action.setEnabled(False)
        self.tray_stop_action.triggered.connect(self._on_stop_clicked)
        tray_menu.addAction(self.tray_stop_action)
        
        tray_menu.addSeparator()
        
        # Show/Hide overlay action
        self.tray_overlay_action = QAction("Hide Overlay", self)
        self.tray_overlay_action.triggered.connect(self._on_overlay_toggle_clicked)
        tray_menu.addAction(self.tray_overlay_action)
        
        tray_menu.addSeparator()
        
        # Show window action
        show_action = QAction("Show Window", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)
        
        # Settings action
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self._on_settings_clicked)
        tray_menu.addAction(settings_action)
        
        tray_menu.addSeparator()
        
        # Exit action
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self._on_exit_clicked)
        tray_menu.addAction(exit_action)
        
        # Set menu and show tray icon
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.setToolTip("OpenLiveCaption")
        
        # Double-click to show window
        self.tray_icon.activated.connect(self._on_tray_activated)
        
        # Show tray icon
        self.tray_icon.show()
    
    def _on_tray_activated(self, reason):
        """Handle tray icon activation (click)"""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show()
            self.activateWindow()
    
    def _on_exit_clicked(self):
        """Handle exit action from tray menu"""
        # Actually exit the application
        from PyQt6.QtWidgets import QApplication
        QApplication.quit()
    
    def _setup_keyboard_shortcuts(self):
        """Set up global keyboard shortcuts"""
        if self.shortcut_manager.is_available():
            self.shortcut_manager.setup_default_shortcuts(
                self.config.shortcuts.start_stop,
                self.config.shortcuts.show_hide
            )
        else:
            # Show warning that shortcuts are not available
            import logging
            logging.warning("Global keyboard shortcuts are not available. Install 'keyboard' library for this feature.")
    
    def _on_shortcut_start_stop(self):
        """Handle start/stop keyboard shortcut"""
        if self.is_running:
            self._on_stop_clicked()
        else:
            self._on_start_clicked()
    
    def _on_shortcut_show_hide(self):
        """Handle show/hide keyboard shortcut"""
        self._on_overlay_toggle_clicked()
    
    def update_keyboard_shortcuts(self):
        """Update keyboard shortcuts after settings change"""
        if self.shortcut_manager.is_available():
            self.shortcut_manager.update_shortcuts(
                self.config.shortcuts.start_stop,
                self.config.shortcuts.show_hide
            )
    
    def _update_tray_menu(self):
        """Update tray menu items based on current state"""
        if self.tray_icon:
            self.tray_start_action.setEnabled(not self.is_running)
            self.tray_stop_action.setEnabled(self.is_running)
            
            if self.overlay_visible:
                self.tray_overlay_action.setText("Hide Overlay")
            else:
                self.tray_overlay_action.setText("Show Overlay")
            
            # Update icon color based on status
            from PyQt6.QtGui import QPixmap, QPainter, QFont as QGuiFont, QColor as QGuiColor
            
            pixmap = QPixmap(64, 64)
            pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # Draw background circle with status color
            if self.is_running:
                painter.setBrush(QGuiColor(76, 175, 80))  # Green when running
            else:
                painter.setBrush(QGuiColor(136, 136, 136))  # Gray when stopped
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(2, 2, 60, 60)
            
            # Draw text
            painter.setPen(QGuiColor(255, 255, 255))
            font = QGuiFont("Arial", 16, QGuiFont.Weight.Bold)
            painter.setFont(font)
            painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "OLC")
            painter.end()
            
            icon = QIcon(pixmap)
            self.tray_icon.setIcon(icon)
