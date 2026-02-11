"""Settings dialog for configuring application options"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QLabel, QComboBox, QSpinBox, QDoubleSpinBox, QLineEdit,
    QPushButton, QCheckBox, QColorDialog, QFileDialog, QGroupBox,
    QFormLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from typing import Optional

from src.config.config_manager import Config, ConfigManager


class SettingsDialog(QDialog):
    """
    Settings dialog with tabbed interface for all configuration options.
    
    Tabs: Audio, Transcription, Overlay, Export, Shortcuts
    """
    
    def __init__(self, config: Config, config_manager: ConfigManager, parent: Optional[QWidget] = None):
        """
        Initialize settings dialog.
        
        Args:
            config: Current application configuration
            config_manager: Configuration manager for saving settings
            parent: Optional parent widget
        """
        super().__init__(parent)
        
        self.config = config
        self.config_manager = config_manager
        
        # Set up dialog
        self.setWindowTitle("Settings")
        self.setMinimumSize(600, 500)
        self.resize(650, 550)
        
        # Create main layout
        main_layout = QVBoxLayout(self)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Create tabs
        self._create_audio_tab()
        self._create_transcription_tab()
        self._create_overlay_tab()
        self._create_export_tab()
        self._create_shortcuts_tab()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(self._on_apply)
        button_layout.addWidget(apply_button)
        
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self._on_ok)
        ok_button.setDefault(True)
        button_layout.addWidget(ok_button)
        
        main_layout.addLayout(button_layout)
    
    def _create_audio_tab(self):
        """Create audio settings tab"""
        audio_widget = QWidget()
        layout = QFormLayout(audio_widget)
        layout.setSpacing(15)
        
        # Sample rate
        self.sample_rate_spin = QSpinBox()
        self.sample_rate_spin.setRange(8000, 48000)
        self.sample_rate_spin.setSingleStep(1000)
        self.sample_rate_spin.setValue(self.config.audio.sample_rate)
        self.sample_rate_spin.setSuffix(" Hz")
        layout.addRow("Sample Rate:", self.sample_rate_spin)
        
        # Chunk duration
        self.chunk_duration_spin = QDoubleSpinBox()
        self.chunk_duration_spin.setRange(0.1, 5.0)
        self.chunk_duration_spin.setSingleStep(0.1)
        self.chunk_duration_spin.setValue(self.config.audio.chunk_duration)
        self.chunk_duration_spin.setSuffix(" seconds")
        layout.addRow("Chunk Duration:", self.chunk_duration_spin)
        
        # VAD threshold
        self.vad_threshold_spin = QDoubleSpinBox()
        self.vad_threshold_spin.setRange(0.001, 0.1)
        self.vad_threshold_spin.setSingleStep(0.001)
        self.vad_threshold_spin.setDecimals(3)
        self.vad_threshold_spin.setValue(self.config.audio.vad_threshold)
        layout.addRow("VAD Threshold:", self.vad_threshold_spin)
        
        # Add help text
        help_label = QLabel(
            "Sample Rate: Audio sampling frequency (16000 Hz recommended for Whisper)\n"
            "Chunk Duration: Length of audio chunks to process\n"
            "VAD Threshold: Voice activity detection threshold (lower = more sensitive)"
        )
        help_label.setWordWrap(True)
        help_label.setStyleSheet("color: #666; font-size: 10px; margin-top: 10px;")
        layout.addRow(help_label)
        
        self.tab_widget.addTab(audio_widget, "Audio")
    
    def _create_transcription_tab(self):
        """Create transcription settings tab"""
        transcription_widget = QWidget()
        layout = QFormLayout(transcription_widget)
        layout.setSpacing(15)
        
        # Model size
        self.model_combo = QComboBox()
        self.model_combo.addItems(["tiny", "base", "small", "medium", "large"])
        self.model_combo.setCurrentText(self.config.transcription.model_name)
        layout.addRow("Model Size:", self.model_combo)
        
        # Device
        self.device_combo = QComboBox()
        self.device_combo.addItems(["cpu", "cuda"])
        self.device_combo.setCurrentText(self.config.transcription.device)
        layout.addRow("Device:", self.device_combo)
        
        # Translation
        self.translation_check = QCheckBox("Enable Translation")
        self.translation_check.setChecked(self.config.transcription.enable_translation)
        self.translation_check.stateChanged.connect(self._on_translation_toggled)
        layout.addRow(self.translation_check)
        
        # Target language
        self.target_language_combo = QComboBox()
        self.target_language_combo.addItems([
            "None",
            # European Languages
            "Spanish 🇪🇸 (es)",
            "French 🇫🇷 (fr)",
            "German 🇩🇪 (de)",
            "Portuguese 🇵🇹 (pt)",
            "Russian 🇷🇺 (ru)",
            "Italian 🇮🇹 (it)",
            "Dutch 🇳🇱 (nl)",
            "Polish 🇵🇱 (pl)",
            "Turkish 🇹🇷 (tr)",
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
            # Asian Languages
            "Chinese 🇨🇳 (zh)",
            "Hindi 🇮🇳 (hi)",
            "Arabic 🇸🇦 (ar)",
            "Japanese 🇯🇵 (ja)",
            "Korean 🇰🇷 (ko)",
            "Vietnamese 🇻🇳 (vi)",
            "Thai 🇹🇭 (th)",
            "Persian 🇮🇷 (fa)",
            "Hebrew 🇮🇱 (he)",
            "Indonesian 🇮🇩 (id)",
            "Malay 🇲🇾 (ms)",
            "Filipino 🇵🇭 (fil)",
            "Bengali 🇧🇩 (bn)",
            "Urdu 🇵🇰 (ur)",
            # African Languages
            "Yoruba 🇳🇬 (yo)",
            "Twi 🇬🇭 (twi)",
            "Swahili 🇰🇪 (sw)",
            "Afrikaans 🇿🇦 (af)"
        ])
        self.target_language_combo.setEnabled(self.config.transcription.enable_translation)
        if self.config.transcription.target_language:
            # Try to find matching item
            for i in range(self.target_language_combo.count()):
                text = self.target_language_combo.itemText(i)
                if f"({self.config.transcription.target_language})" in text:
                    self.target_language_combo.setCurrentIndex(i)
                    break
        layout.addRow("Target Language:", self.target_language_combo)
        
        # Help text
        help_label = QLabel(
            "Model Size: Larger models are more accurate but slower\n"
            "Device: Use 'cuda' for GPU acceleration if available\n"
            "Translation: Translate captions to another language"
        )
        help_label.setWordWrap(True)
        help_label.setStyleSheet("color: #666; font-size: 10px; margin-top: 10px;")
        layout.addRow(help_label)
        
        self.tab_widget.addTab(transcription_widget, "Transcription")
    
    def _create_overlay_tab(self):
        """Create overlay settings tab"""
        overlay_widget = QWidget()
        layout = QVBoxLayout(overlay_widget)
        layout.setSpacing(15)
        
        # Position group
        position_group = QGroupBox("Position")
        position_layout = QFormLayout(position_group)
        
        self.position_combo = QComboBox()
        self.position_combo.addItems(["top", "bottom", "custom"])
        self.position_combo.setCurrentText(self.config.overlay.position)
        self.position_combo.currentTextChanged.connect(self._on_position_changed)
        position_layout.addRow("Position:", self.position_combo)
        
        self.custom_x_spin = QSpinBox()
        self.custom_x_spin.setRange(0, 10000)
        self.custom_x_spin.setValue(self.config.overlay.custom_x)
        self.custom_x_spin.setEnabled(self.config.overlay.position == "custom")
        position_layout.addRow("Custom X:", self.custom_x_spin)
        
        self.custom_y_spin = QSpinBox()
        self.custom_y_spin.setRange(0, 10000)
        self.custom_y_spin.setValue(self.config.overlay.custom_y)
        self.custom_y_spin.setEnabled(self.config.overlay.position == "custom")
        position_layout.addRow("Custom Y:", self.custom_y_spin)
        
        layout.addWidget(position_group)
        
        # Appearance group
        appearance_group = QGroupBox("Appearance")
        appearance_layout = QFormLayout(appearance_group)
        
        self.font_family_edit = QLineEdit(self.config.overlay.font_family)
        appearance_layout.addRow("Font Family:", self.font_family_edit)
        
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 72)
        self.font_size_spin.setValue(self.config.overlay.font_size)
        appearance_layout.addRow("Font Size:", self.font_size_spin)
        
        # Text color
        text_color_layout = QHBoxLayout()
        self.text_color_edit = QLineEdit(self.config.overlay.text_color)
        self.text_color_edit.setMaximumWidth(100)
        text_color_layout.addWidget(self.text_color_edit)
        
        text_color_button = QPushButton("Choose...")
        text_color_button.clicked.connect(self._on_choose_text_color)
        text_color_layout.addWidget(text_color_button)
        text_color_layout.addStretch()
        appearance_layout.addRow("Text Color:", text_color_layout)
        
        # Background color
        bg_color_layout = QHBoxLayout()
        self.bg_color_edit = QLineEdit(self.config.overlay.background_color)
        self.bg_color_edit.setMaximumWidth(100)
        bg_color_layout.addWidget(self.bg_color_edit)
        
        bg_color_button = QPushButton("Choose...")
        bg_color_button.clicked.connect(self._on_choose_bg_color)
        bg_color_layout.addWidget(bg_color_button)
        bg_color_layout.addStretch()
        appearance_layout.addRow("Background Color:", bg_color_layout)
        
        self.bg_opacity_spin = QDoubleSpinBox()
        self.bg_opacity_spin.setRange(0.0, 1.0)
        self.bg_opacity_spin.setSingleStep(0.1)
        self.bg_opacity_spin.setValue(self.config.overlay.background_opacity)
        appearance_layout.addRow("Background Opacity:", self.bg_opacity_spin)
        
        layout.addWidget(appearance_group)
        
        # Behavior group
        behavior_group = QGroupBox("Behavior")
        behavior_layout = QFormLayout(behavior_group)
        
        self.max_lines_spin = QSpinBox()
        self.max_lines_spin.setRange(1, 10)
        self.max_lines_spin.setValue(self.config.overlay.max_lines)
        behavior_layout.addRow("Max Lines:", self.max_lines_spin)
        
        self.scroll_mode_combo = QComboBox()
        self.scroll_mode_combo.addItems(["replace", "scroll"])
        self.scroll_mode_combo.setCurrentText(self.config.overlay.scroll_mode)
        behavior_layout.addRow("Scroll Mode:", self.scroll_mode_combo)
        
        self.clear_timeout_spin = QDoubleSpinBox()
        self.clear_timeout_spin.setRange(0.0, 60.0)
        self.clear_timeout_spin.setSingleStep(1.0)
        self.clear_timeout_spin.setValue(self.config.overlay.clear_timeout)
        self.clear_timeout_spin.setSuffix(" seconds")
        behavior_layout.addRow("Clear Timeout:", self.clear_timeout_spin)
        
        layout.addWidget(behavior_group)
        layout.addStretch()
        
        self.tab_widget.addTab(overlay_widget, "Overlay")
    
    def _create_export_tab(self):
        """Create export settings tab"""
        export_widget = QWidget()
        layout = QFormLayout(export_widget)
        layout.setSpacing(15)
        
        # Enable export
        self.export_enabled_check = QCheckBox("Enable Subtitle Export")
        self.export_enabled_check.setChecked(self.config.export.enabled)
        self.export_enabled_check.stateChanged.connect(self._on_export_toggled)
        layout.addRow(self.export_enabled_check)
        
        # Format
        self.export_format_combo = QComboBox()
        self.export_format_combo.addItems(["srt", "vtt"])
        self.export_format_combo.setCurrentText(self.config.export.format)
        self.export_format_combo.setEnabled(self.config.export.enabled)
        layout.addRow("Format:", self.export_format_combo)
        
        # Output path
        output_path_layout = QHBoxLayout()
        self.output_path_edit = QLineEdit(self.config.export.output_path)
        self.output_path_edit.setEnabled(self.config.export.enabled)
        output_path_layout.addWidget(self.output_path_edit)
        
        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self._on_browse_output_path)
        browse_button.setEnabled(self.config.export.enabled)
        output_path_layout.addWidget(browse_button)
        layout.addRow("Output Path:", output_path_layout)
        
        # Help text
        help_label = QLabel(
            "Enable subtitle export to save captions to a file.\n"
            "SRT and VTT formats are supported."
        )
        help_label.setWordWrap(True)
        help_label.setStyleSheet("color: #666; font-size: 10px; margin-top: 10px;")
        layout.addRow(help_label)
        
        self.tab_widget.addTab(export_widget, "Export")
    
    def _create_shortcuts_tab(self):
        """Create keyboard shortcuts tab"""
        shortcuts_widget = QWidget()
        layout = QFormLayout(shortcuts_widget)
        layout.setSpacing(15)
        
        # Start/Stop shortcut
        self.start_stop_edit = QLineEdit(self.config.shortcuts.start_stop)
        layout.addRow("Start/Stop:", self.start_stop_edit)
        
        # Show/Hide shortcut
        self.show_hide_edit = QLineEdit(self.config.shortcuts.show_hide)
        layout.addRow("Show/Hide Overlay:", self.show_hide_edit)
        
        # Help text
        help_label = QLabel(
            "Enter keyboard shortcuts in the format: Ctrl+Shift+S\n"
            "Supported modifiers: Ctrl, Shift, Alt\n"
            "Note: Global hotkeys may not work on all platforms."
        )
        help_label.setWordWrap(True)
        help_label.setStyleSheet("color: #666; font-size: 10px; margin-top: 10px;")
        layout.addRow(help_label)
        
        self.tab_widget.addTab(shortcuts_widget, "Shortcuts")
    
    def _on_translation_toggled(self, state):
        """Handle translation checkbox toggle"""
        enabled = state == Qt.CheckState.Checked.value
        self.target_language_combo.setEnabled(enabled)
    
    def _on_export_toggled(self, state):
        """Handle export checkbox toggle"""
        enabled = state == Qt.CheckState.Checked.value
        self.export_format_combo.setEnabled(enabled)
        self.output_path_edit.setEnabled(enabled)
    
    def _on_position_changed(self, position):
        """Handle position combo change"""
        is_custom = position == "custom"
        self.custom_x_spin.setEnabled(is_custom)
        self.custom_y_spin.setEnabled(is_custom)
    
    def _on_choose_text_color(self):
        """Open color picker for text color"""
        current_color = QColor(self.text_color_edit.text())
        color = QColorDialog.getColor(current_color, self, "Choose Text Color")
        if color.isValid():
            self.text_color_edit.setText(color.name())
    
    def _on_choose_bg_color(self):
        """Open color picker for background color"""
        current_color = QColor(self.bg_color_edit.text())
        color = QColorDialog.getColor(current_color, self, "Choose Background Color")
        if color.isValid():
            self.bg_color_edit.setText(color.name())
    
    def _on_browse_output_path(self):
        """Open file dialog for output path"""
        file_filter = "Subtitle Files (*.srt *.vtt);;All Files (*.*)"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Choose Output File",
            self.output_path_edit.text(),
            file_filter
        )
        if file_path:
            self.output_path_edit.setText(file_path)
    
    def _on_apply(self):
        """Apply settings without closing dialog"""
        self._save_settings()
    
    def _on_ok(self):
        """Apply settings and close dialog"""
        self._save_settings()
        self.accept()
    
    def _save_settings(self):
        """Save all settings to configuration"""
        # Audio settings
        self.config.audio.sample_rate = self.sample_rate_spin.value()
        self.config.audio.chunk_duration = self.chunk_duration_spin.value()
        self.config.audio.vad_threshold = self.vad_threshold_spin.value()
        
        # Transcription settings
        self.config.transcription.model_name = self.model_combo.currentText()
        self.config.transcription.device = self.device_combo.currentText()
        self.config.transcription.enable_translation = self.translation_check.isChecked()
        
        # Extract target language code
        target_lang_text = self.target_language_combo.currentText()
        if target_lang_text != "None" and "(" in target_lang_text:
            lang_code = target_lang_text.split("(")[1].split(")")[0]
            self.config.transcription.target_language = lang_code
        else:
            self.config.transcription.target_language = None
        
        # Overlay settings
        self.config.overlay.position = self.position_combo.currentText()
        self.config.overlay.custom_x = self.custom_x_spin.value()
        self.config.overlay.custom_y = self.custom_y_spin.value()
        self.config.overlay.font_family = self.font_family_edit.text()
        self.config.overlay.font_size = self.font_size_spin.value()
        self.config.overlay.text_color = self.text_color_edit.text()
        self.config.overlay.background_color = self.bg_color_edit.text()
        self.config.overlay.background_opacity = self.bg_opacity_spin.value()
        self.config.overlay.max_lines = self.max_lines_spin.value()
        self.config.overlay.scroll_mode = self.scroll_mode_combo.currentText()
        self.config.overlay.clear_timeout = self.clear_timeout_spin.value()
        
        # Export settings
        self.config.export.enabled = self.export_enabled_check.isChecked()
        self.config.export.format = self.export_format_combo.currentText()
        self.config.export.output_path = self.output_path_edit.text()
        
        # Shortcut settings
        self.config.shortcuts.start_stop = self.start_stop_edit.text()
        self.config.shortcuts.show_hide = self.show_hide_edit.text()
        
        # Save to file
        self.config_manager.save(self.config)
