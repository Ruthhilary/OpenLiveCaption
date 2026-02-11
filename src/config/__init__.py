"""Configuration management for OpenLiveCaption"""

from .config_manager import (
    Config,
    AudioConfig,
    TranscriptionConfig,
    OverlayConfig,
    ExportConfig,
    ShortcutConfig,
    ConfigManager
)

__all__ = [
    "Config",
    "AudioConfig",
    "TranscriptionConfig",
    "OverlayConfig",
    "ExportConfig",
    "ShortcutConfig",
    "ConfigManager"
]
