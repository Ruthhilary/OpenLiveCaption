"""Keyboard shortcut manager for global hotkeys"""

import sys
from typing import Callable, Dict, Optional
from PyQt6.QtCore import QObject, pyqtSignal, QThread
import logging

logger = logging.getLogger(__name__)

# Try to import keyboard library for global hotkeys
try:
    import keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False
    keyboard = None
    logger.warning("keyboard library not available - global hotkeys disabled")


class KeyboardShortcutManager(QObject):
    """
    Manages global keyboard shortcuts.
    
    Provides cross-platform support for global hotkeys that work
    even when the application is not in focus.
    """
    
    # Signals
    start_stop_triggered = pyqtSignal()
    show_hide_triggered = pyqtSignal()
    
    def __init__(self, parent: Optional[QObject] = None):
        """
        Initialize keyboard shortcut manager.
        
        Args:
            parent: Optional parent QObject
        """
        super().__init__(parent)
        
        self.shortcuts: Dict[str, Callable] = {}
        self.registered_hotkeys: list = []
        self.enabled = KEYBOARD_AVAILABLE
        
        if not self.enabled:
            logger.warning("Keyboard shortcuts are disabled (keyboard library not installed)")
    
    def register_shortcut(self, shortcut: str, callback: Callable):
        """
        Register a global keyboard shortcut.
        
        Args:
            shortcut: Shortcut string (e.g., "ctrl+shift+s")
            callback: Function to call when shortcut is triggered
        
        Returns:
            True if registration successful, False otherwise
        """
        if not self.enabled:
            logger.warning(f"Cannot register shortcut '{shortcut}' - keyboard library not available")
            return False
        
        try:
            # Normalize shortcut string
            normalized = self._normalize_shortcut(shortcut)
            
            # Unregister if already registered
            if normalized in self.shortcuts:
                self.unregister_shortcut(normalized)
            
            # Register with keyboard library
            keyboard.add_hotkey(normalized, callback, suppress=False)
            
            self.shortcuts[normalized] = callback
            self.registered_hotkeys.append(normalized)
            
            logger.info(f"Registered global hotkey: {normalized}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register shortcut '{shortcut}': {e}")
            return False
    
    def unregister_shortcut(self, shortcut: str):
        """
        Unregister a keyboard shortcut.
        
        Args:
            shortcut: Shortcut string to unregister
        """
        if not self.enabled:
            return
        
        try:
            normalized = self._normalize_shortcut(shortcut)
            
            if normalized in self.shortcuts:
                keyboard.remove_hotkey(normalized)
                del self.shortcuts[normalized]
                if normalized in self.registered_hotkeys:
                    self.registered_hotkeys.remove(normalized)
                
                logger.info(f"Unregistered global hotkey: {normalized}")
        
        except Exception as e:
            logger.error(f"Failed to unregister shortcut '{shortcut}': {e}")
    
    def unregister_all(self):
        """Unregister all keyboard shortcuts"""
        if not self.enabled:
            return
        
        for shortcut in list(self.registered_hotkeys):
            self.unregister_shortcut(shortcut)
    
    def setup_default_shortcuts(self, start_stop_shortcut: str, show_hide_shortcut: str):
        """
        Set up default application shortcuts.
        
        Args:
            start_stop_shortcut: Shortcut for start/stop action
            show_hide_shortcut: Shortcut for show/hide overlay action
        """
        # Register start/stop shortcut
        self.register_shortcut(start_stop_shortcut, self._on_start_stop)
        
        # Register show/hide shortcut
        self.register_shortcut(show_hide_shortcut, self._on_show_hide)
    
    def update_shortcuts(self, start_stop_shortcut: str, show_hide_shortcut: str):
        """
        Update shortcuts (unregister old ones and register new ones).
        
        Args:
            start_stop_shortcut: New shortcut for start/stop action
            show_hide_shortcut: New shortcut for show/hide overlay action
        """
        # Unregister all existing shortcuts
        self.unregister_all()
        
        # Register new shortcuts
        self.setup_default_shortcuts(start_stop_shortcut, show_hide_shortcut)
    
    def _on_start_stop(self):
        """Handle start/stop shortcut trigger"""
        logger.info("Start/stop shortcut triggered")
        self.start_stop_triggered.emit()
    
    def _on_show_hide(self):
        """Handle show/hide shortcut trigger"""
        logger.info("Show/hide shortcut triggered")
        self.show_hide_triggered.emit()
    
    def _normalize_shortcut(self, shortcut: str) -> str:
        """
        Normalize shortcut string to keyboard library format.
        
        Args:
            shortcut: Shortcut string (e.g., "Ctrl+Shift+S")
        
        Returns:
            Normalized shortcut string (e.g., "ctrl+shift+s")
        """
        # Convert to lowercase
        normalized = shortcut.lower()
        
        # Replace common variations
        normalized = normalized.replace("control", "ctrl")
        normalized = normalized.replace("command", "cmd")
        normalized = normalized.replace("option", "alt")
        
        # Remove spaces
        normalized = normalized.replace(" ", "")
        
        return normalized
    
    def is_available(self) -> bool:
        """
        Check if keyboard shortcuts are available.
        
        Returns:
            True if keyboard library is available, False otherwise
        """
        return self.enabled
    
    def __del__(self):
        """Cleanup on deletion"""
        self.unregister_all()
