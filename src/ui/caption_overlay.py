"""Caption overlay window for system-wide subtitle display"""

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer, QRect
from PyQt6.QtGui import QFont, QColor, QPalette, QScreen
from typing import Optional
from enum import Enum

from src.config.config_manager import OverlayConfig


class Position(Enum):
    """Overlay position options"""
    TOP = "top"
    BOTTOM = "bottom"
    CUSTOM = "custom"


class CaptionOverlay(QWidget):
    """
    System-wide caption overlay window.
    
    Displays captions as an always-on-top, click-through transparent overlay
    that works across all applications.
    """
    
    def __init__(self, config: OverlayConfig, parent: Optional[QWidget] = None, 
                 config_manager=None):
        """
        Initialize caption overlay window.
        
        Args:
            config: Overlay configuration settings
            parent: Optional parent widget
            config_manager: Optional ConfigManager instance for saving position changes
        """
        super().__init__(parent)
        
        self.config = config
        self.config_manager = config_manager
        self.caption_lines = []  # Store current caption lines
        self.clear_timer = QTimer(self)
        self.clear_timer.timeout.connect(self._clear_captions)
        
        # Set up window with frameless, always-on-top, click-through flags
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |      # No title bar
            Qt.WindowType.WindowStaysOnTopHint |     # Always on top
            Qt.WindowType.Tool |                      # Don't show in taskbar
            Qt.WindowType.WindowTransparentForInput  # Click-through
        )
        
        # Enable transparent background
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Set window opacity
        self.setWindowOpacity(1.0)  # Window itself is fully opaque, background transparency handled by palette
        
        # Create label for text rendering
        self.caption_label = QLabel(self)
        self.caption_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.caption_label.setWordWrap(True)
        
        # Set up layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.caption_label)
        layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(layout)
        
        # Apply initial styling and position
        self._apply_style()
        self._apply_position()
    
    def _apply_style(self):
        """Apply styling configuration to the overlay"""
        # Set font
        font = QFont(self.config.font_family, self.config.font_size)
        self.caption_label.setFont(font)
        
        # Parse colors
        text_color = QColor(self.config.text_color)
        bg_color = QColor(self.config.background_color)
        
        # Apply background opacity to the background color
        bg_color.setAlphaF(self.config.background_opacity)
        
        # Create stylesheet with text shadow for readability
        stylesheet = f"""
            QLabel {{
                color: {self.config.text_color};
                background-color: rgba({bg_color.red()}, {bg_color.green()}, {bg_color.blue()}, {bg_color.alphaF()});
                padding: 10px;
                border-radius: 5px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
            }}
        """
        self.caption_label.setStyleSheet(stylesheet)
    
    def _apply_position(self):
        """Apply position configuration to the overlay with multi-monitor support"""
        from PyQt6.QtWidgets import QApplication
        
        # Get all available screens
        screens = QApplication.screens()
        if not screens:
            return
        
        # Use primary screen by default
        screen = QApplication.primaryScreen()
        if screen is None:
            return
        
        screen_geometry = screen.geometry()
        
        # Determine position based on config
        position = Position(self.config.position)
        
        if position == Position.TOP:
            x = screen_geometry.x()
            y = screen_geometry.y()
            width = screen_geometry.width() if self.config.width == 0 else self.config.width
            height = self.config.height
        elif position == Position.BOTTOM:
            x = screen_geometry.x()
            y = screen_geometry.y() + screen_geometry.height() - self.config.height
            width = screen_geometry.width() if self.config.width == 0 else self.config.width
            height = self.config.height
        else:  # CUSTOM
            x = self.config.custom_x
            y = self.config.custom_y
            width = screen_geometry.width() if self.config.width == 0 else self.config.width
            height = self.config.height
            
            # For custom position, check if coordinates are on any screen
            # If not, default to primary screen
            on_screen = False
            for scr in screens:
                if scr.geometry().contains(x, y):
                    on_screen = True
                    break
            
            if not on_screen:
                # Reset to bottom of primary screen if custom position is off-screen
                x = screen_geometry.x()
                y = screen_geometry.y() + screen_geometry.height() - self.config.height
        
        # Set geometry
        self.setGeometry(x, y, width, height)
    
    def update_caption(self, text: str):
        """
        Update displayed caption text.
        
        Implements text wrapping at word boundaries and enforces maximum line limit.
        
        Args:
            text: Caption text to display
        """
        if not text:
            return
        
        # Handle scroll vs replace mode
        if self.config.scroll_mode == "scroll":
            # Add new line and keep max_lines
            self.caption_lines.append(text)
            # Enforce maximum lines - remove oldest lines if exceeded
            while len(self.caption_lines) > self.config.max_lines:
                self.caption_lines.pop(0)
        else:  # replace mode
            # Replace all text with new text
            self.caption_lines = [text]
        
        # Combine lines and enforce max_lines limit
        display_text = "\n".join(self.caption_lines[-self.config.max_lines:])
        
        # Update label with current lines
        # QLabel with wordWrap=True handles word boundary wrapping automatically
        self.caption_label.setText(display_text)
        
        # Reset clear timer
        if self.config.clear_timeout > 0:
            self.clear_timer.stop()
            self.clear_timer.start(int(self.config.clear_timeout * 1000))
    
    def _clear_captions(self):
        """Clear all displayed captions (called by timer)"""
        self.caption_lines.clear()
        self.caption_label.setText("")
    
    def set_position(self, position: Position, custom_x: int = 0, custom_y: int = 0, 
                     save_to_config: bool = False):
        """
        Set overlay position.
        
        Args:
            position: Position preset (TOP, BOTTOM, or CUSTOM)
            custom_x: X coordinate for custom position
            custom_y: Y coordinate for custom position
            save_to_config: If True, save position changes to configuration file
        """
        self.config.position = position.value
        if position == Position.CUSTOM:
            self.config.custom_x = custom_x
            self.config.custom_y = custom_y
        
        self._apply_position()
        
        # Save to config file if requested and config_manager is available
        if save_to_config and self.config_manager is not None:
            from src.config.config_manager import Config
            full_config = self.config_manager.load()
            full_config.overlay = self.config
            self.config_manager.save(full_config)
    
    def move_to_screen(self, screen_index: int):
        """
        Move overlay to a specific screen in multi-monitor setup.
        
        Args:
            screen_index: Index of the screen (0 = primary)
        """
        from PyQt6.QtWidgets import QApplication
        
        screens = QApplication.screens()
        if screen_index < 0 or screen_index >= len(screens):
            return
        
        screen = screens[screen_index]
        screen_geometry = screen.geometry()
        
        # Apply current position mode to the new screen
        position = Position(self.config.position)
        
        if position == Position.TOP:
            x = screen_geometry.x()
            y = screen_geometry.y()
        elif position == Position.BOTTOM:
            x = screen_geometry.x()
            y = screen_geometry.y() + screen_geometry.height() - self.config.height
        else:  # CUSTOM - maintain relative position
            x = screen_geometry.x() + self.config.custom_x
            y = screen_geometry.y() + self.config.custom_y
        
        width = screen_geometry.width() if self.config.width == 0 else self.config.width
        height = self.config.height
        
        self.setGeometry(x, y, width, height)
    
    def set_style(self, font_family: Optional[str] = None, font_size: Optional[int] = None,
                  text_color: Optional[str] = None, background_color: Optional[str] = None,
                  background_opacity: Optional[float] = None):
        """
        Update overlay styling.
        
        Args:
            font_family: Font family name
            font_size: Font size in points
            text_color: Text color in hex format (#RRGGBB)
            background_color: Background color in hex format (#RRGGBB)
            background_opacity: Background opacity (0.0 to 1.0)
        """
        if font_family is not None:
            self.config.font_family = font_family
        if font_size is not None:
            self.config.font_size = font_size
        if text_color is not None:
            self.config.text_color = text_color
        if background_color is not None:
            self.config.background_color = background_color
        if background_opacity is not None:
            self.config.background_opacity = max(0.0, min(1.0, background_opacity))
        
        self._apply_style()
    
    def set_font(self, font_family: str, font_size: int):
        """
        Set font family and size.
        
        Args:
            font_family: Font family name (e.g., "Arial", "Times New Roman")
            font_size: Font size in points
        """
        self.set_style(font_family=font_family, font_size=font_size)
    
    def set_colors(self, text_color: str, background_color: str):
        """
        Set text and background colors.
        
        Args:
            text_color: Text color in hex format (#RRGGBB)
            background_color: Background color in hex format (#RRGGBB)
        """
        self.set_style(text_color=text_color, background_color=background_color)
    
    def set_background_opacity(self, opacity: float):
        """
        Set background opacity.
        
        Args:
            opacity: Opacity value from 0.0 (transparent) to 1.0 (opaque)
        """
        self.set_style(background_opacity=opacity)
    
    def show_overlay(self):
        """Make overlay visible"""
        self.show()
    
    def hide_overlay(self):
        """Hide overlay"""
        self.hide()
