"""Configuration management with JSON-based persistence"""

import json
import os
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Optional
import platform


@dataclass
class AudioConfig:
    """Audio capture configuration"""
    device_id: int = -1  # -1 means default device
    sample_rate: int = 16000
    chunk_duration: float = 1.0
    vad_threshold: float = 0.01


@dataclass
class TranscriptionConfig:
    """Transcription engine configuration"""
    model_name: str = "tiny"
    device: str = "cpu"
    language: Optional[str] = None
    enable_translation: bool = False
    target_language: Optional[str] = None


@dataclass
class OverlayConfig:
    """Caption overlay display configuration"""
    position: str = "bottom"  # "top", "bottom", or "custom"
    custom_x: int = 0
    custom_y: int = 0
    width: int = 0  # 0 = full screen width
    height: int = 150
    font_family: str = "Arial"
    font_size: int = 24
    text_color: str = "#FFFFFF"
    background_color: str = "#000000"
    background_opacity: float = 0.7
    max_lines: int = 3
    scroll_mode: str = "replace"  # "replace" or "scroll"
    clear_timeout: float = 5.0


@dataclass
class ExportConfig:
    """Subtitle export configuration"""
    enabled: bool = True
    format: str = "srt"  # "srt" or "vtt"
    output_path: str = "subtitles.srt"


@dataclass
class ShortcutConfig:
    """Keyboard shortcut configuration"""
    start_stop: str = "Ctrl+Shift+S"
    show_hide: str = "Ctrl+Shift+H"


@dataclass
class Config:
    """Main application configuration"""
    audio: AudioConfig = field(default_factory=AudioConfig)
    transcription: TranscriptionConfig = field(default_factory=TranscriptionConfig)
    overlay: OverlayConfig = field(default_factory=OverlayConfig)
    export: ExportConfig = field(default_factory=ExportConfig)
    shortcuts: ShortcutConfig = field(default_factory=ShortcutConfig)


class ConfigManager:
    """Manages loading and saving configuration to JSON files"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize ConfigManager with optional custom config path.
        
        Args:
            config_path: Custom path to config file. If None, uses platform default.
        """
        if config_path:
            self.config_path = Path(config_path)
        else:
            self.config_path = self._get_default_config_path()
        
        # Ensure config directory exists
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
    
    def _get_default_config_path(self) -> Path:
        """Get platform-specific default config file path"""
        system = platform.system()
        
        if system == "Windows":
            # Windows: %APPDATA%/OpenLiveCaption/config.json
            base_dir = Path(os.environ.get("APPDATA", "~"))
        elif system == "Darwin":
            # macOS: ~/Library/Application Support/OpenLiveCaption/config.json
            base_dir = Path.home() / "Library" / "Application Support"
        else:
            # Linux: ~/.config/OpenLiveCaption/config.json
            base_dir = Path.home() / ".config"
        
        return base_dir / "OpenLiveCaption" / "config.json"
    
    def load(self) -> Config:
        """
        Load configuration from file.
        
        Returns:
            Config object with loaded settings, or default config if file doesn't exist
        """
        if not self.config_path.exists():
            return self.get_default()
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Ensure data is a dictionary
            if not isinstance(data, dict):
                print(f"Warning: Configuration file has invalid structure (not a dict), using defaults")
                return self.get_default()
            
            # Reconstruct nested dataclasses
            config = Config(
                audio=AudioConfig(**data.get('audio', {})),
                transcription=TranscriptionConfig(**data.get('transcription', {})),
                overlay=OverlayConfig(**data.get('overlay', {})),
                export=ExportConfig(**data.get('export', {})),
                shortcuts=ShortcutConfig(**data.get('shortcuts', {}))
            )
            return config
        except (json.JSONDecodeError, TypeError, KeyError, UnicodeDecodeError, AttributeError) as e:
            # If config is corrupted, return default and log warning
            print(f"Warning: Configuration file corrupted ({e}), using defaults")
            return self.get_default()
    
    def save(self, config: Config) -> None:
        """
        Save configuration to file.
        
        Args:
            config: Config object to save
        """
        # Convert dataclasses to dict
        data = {
            'audio': asdict(config.audio),
            'transcription': asdict(config.transcription),
            'overlay': asdict(config.overlay),
            'export': asdict(config.export),
            'shortcuts': asdict(config.shortcuts)
        }
        
        # Ensure directory exists
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write to file with pretty formatting
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get_default(self) -> Config:
        """
        Get default configuration.
        
        Returns:
            Config object with default values
        """
        return Config()
