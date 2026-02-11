"""Main application class that wires all components together"""

import sys
import logging
from typing import Optional
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QObject, pyqtSignal
import numpy as np

from src.config.config_manager import ConfigManager, Config
from src.audio.audio_capture import AudioCaptureEngine, AudioDevice
from src.transcription.transcription_engine import TranscriptionEngine, TranscriptionResult
from src.translation.translation_engine import TranslationEngine
from src.ui.caption_overlay import CaptionOverlay
from src.ui.control_window import ControlWindow
from src.export.subtitle_exporter import SubtitleExporter


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LiveCaptionApplication(QObject):
    """
    Main application class that coordinates all components.
    
    This class:
    - Instantiates all components (audio, transcription, translation, UI, export)
    - Connects audio capture callback to transcription engine
    - Connects transcription results to overlay display
    - Connects transcription results to subtitle exporter
    - Manages application lifecycle (startup, shutdown)
    - Handles error propagation and recovery
    """
    
    # Signals for error handling
    error_occurred = pyqtSignal(str)
    device_disconnected = pyqtSignal()
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the application.
        
        Handles application startup:
        - Loads configuration from file
        - Initializes all components
        - Connects signals between components
        
        Args:
            config_path: Optional custom path to config file
        """
        super().__init__()
        
        logger.info("Initializing OpenLiveCaption application...")
        
        # Load configuration
        logger.info("Loading configuration...")
        self.config_manager = ConfigManager(config_path)
        self.config = self.config_manager.load()
        logger.info(f"Configuration loaded from: {self.config_manager.config_path}")
        
        # Initialize components
        self.audio_engine: Optional[AudioCaptureEngine] = None
        self.transcription_engine: Optional[TranscriptionEngine] = None
        self.translation_engine: Optional[TranslationEngine] = None
        self.caption_overlay: Optional[CaptionOverlay] = None
        self.control_window: Optional[ControlWindow] = None
        self.subtitle_exporter: Optional[SubtitleExporter] = None
        
        # Application state
        self.is_running = False
        self.current_session_start_time = 0.0
        self.device_monitor_timer = None
        
        # Initialize all components
        logger.info("Initializing components...")
        self._initialize_components()
        
        # Connect signals
        logger.info("Connecting component signals...")
        self._connect_signals()
        
        logger.info("Application initialized successfully")
    
    def _initialize_components(self):
        """Initialize all application components"""
        try:
            # Initialize audio capture engine
            self.audio_engine = AudioCaptureEngine(self.config.audio)
            logger.info("Audio capture engine initialized")
            
            # Initialize transcription engine
            self.transcription_engine = TranscriptionEngine(
                model_name=self.config.transcription.model_name,
                device=self.config.transcription.device
            )
            logger.info(f"Transcription engine initialized with model '{self.config.transcription.model_name}'")
            
            # Set language if configured
            if self.config.transcription.language:
                self.transcription_engine.set_language(self.config.transcription.language)
            
            # Initialize translation engine (lazy loading)
            self.translation_engine = TranslationEngine()
            logger.info("Translation engine initialized")
            
            # Initialize caption overlay
            self.caption_overlay = CaptionOverlay(
                config=self.config.overlay,
                config_manager=self.config_manager
            )
            logger.info("Caption overlay initialized")
            
            # Initialize control window
            self.control_window = ControlWindow(
                config=self.config,
                config_manager=self.config_manager
            )
            logger.info("Control window initialized")
            
            # Populate audio devices in control window
            devices = self.audio_engine.list_devices()
            self.control_window.populate_audio_devices(devices)
            
            # Initialize subtitle exporter if enabled
            if self.config.export.enabled:
                self.subtitle_exporter = SubtitleExporter(
                    output_path=self.config.export.output_path,
                    format=self.config.export.format
                )
                logger.info(f"Subtitle exporter initialized ({self.config.export.format} format)")
            
        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
            raise
    
    def _connect_signals(self):
        """Connect signals between components"""
        # Control window signals
        self.control_window.start_requested.connect(self.start_captions)
        self.control_window.stop_requested.connect(self.stop_captions)
        self.control_window.show_overlay_requested.connect(self.caption_overlay.show_overlay)
        self.control_window.hide_overlay_requested.connect(self.caption_overlay.hide_overlay)
        self.control_window.audio_device_changed.connect(self._on_audio_device_changed)
        self.control_window.model_changed.connect(self._on_model_changed)
        self.control_window.language_changed.connect(self._on_language_changed)
        
        # Overlay close event handling (for recreation on unexpected close)
        self.caption_overlay.destroyed.connect(self._on_overlay_destroyed)
        
        # Error handling signals
        self.error_occurred.connect(self._on_error)
        self.device_disconnected.connect(self._on_device_disconnected)
        
        # Start device monitoring timer
        self._start_device_monitoring()
        
        logger.info("Component signals connected")
    
    def start_captions(self):
        """Start caption generation"""
        if self.is_running:
            logger.warning("Captions already running")
            return
        
        try:
            logger.info("Starting caption generation...")
            
            # Reset transcription buffer
            self.transcription_engine.reset_buffer()
            
            # Get selected audio device
            device_id = self.config.audio.device_id
            if device_id == -1:
                # Use default device
                devices = self.audio_engine.list_devices()
                if devices:
                    device_id = devices[0].id
                else:
                    self._show_error("No audio devices found")
                    return
            
            # Start audio capture with callback
            success = self.audio_engine.start_capture(
                device_id=device_id,
                callback=self._on_audio_chunk,
                error_callback=self._on_audio_error
            )
            
            if not success:
                self._show_error("Failed to start audio capture")
                return
            
            # Show overlay
            self.caption_overlay.show_overlay()
            
            # Update state
            self.is_running = True
            self.control_window.set_status(True)
            
            logger.info("Caption generation started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start captions: {e}")
            self._show_error(f"Failed to start captions: {e}")
    
    def stop_captions(self):
        """Stop caption generation"""
        if not self.is_running:
            logger.warning("Captions not running")
            return
        
        try:
            logger.info("Stopping caption generation...")
            
            # Stop audio capture
            self.audio_engine.stop_capture()
            
            # Finalize subtitle export
            if self.subtitle_exporter and not self.subtitle_exporter.is_finalized():
                self.subtitle_exporter.finalize()
                logger.info(f"Subtitles saved to: {self.config.export.output_path}")
            
            # Update state
            self.is_running = False
            self.control_window.set_status(False)
            
            logger.info("Caption generation stopped")
            
        except Exception as e:
            logger.error(f"Error stopping captions: {e}")
            self._show_error(f"Error stopping captions: {e}")
    
    def _on_audio_chunk(self, audio_data: np.ndarray):
        """
        Handle audio chunk from capture engine.
        
        This callback is called by the audio capture engine with each audio chunk.
        It processes the audio through transcription and optionally translation,
        then updates the overlay and exports to subtitle file.
        
        Args:
            audio_data: Audio chunk as float32 numpy array
        """
        try:
            # Transcribe audio with overlapping chunks
            result = self.transcription_engine.process_with_overlap(audio_data)
            
            if result is None:
                # Not enough chunks yet for overlap processing
                return
            
            # Skip empty transcriptions
            if not result.text or result.text.strip() == "":
                return
            
            logger.info(f"Transcribed: {result.text}")
            
            # Translate if enabled
            display_text = result.text
            translated_text = None
            
            if self.config.transcription.enable_translation and self.config.transcription.target_language:
                try:
                    translation_result = self.translation_engine.translate_with_original(
                        result.text,
                        self.config.transcription.target_language
                    )
                    translated_text = translation_result.translated_text
                    
                    # Display both original and translated if configured
                    # For now, just display translated
                    display_text = translated_text
                    logger.info(f"Translated: {translated_text}")
                    
                except Exception as e:
                    logger.error(f"Translation failed: {e}")
                    # Continue with original text
            
            # Update caption overlay
            self.caption_overlay.update_caption(display_text)
            
            # Export to subtitle file
            if self.subtitle_exporter:
                self.subtitle_exporter.add_subtitle(
                    text=result.text,
                    start_time=result.start_time,
                    end_time=result.end_time,
                    translated_text=translated_text
                )
            
        except Exception as e:
            logger.error(f"Error processing audio chunk: {e}")
            # Don't crash - continue processing next chunk
    
    def _on_audio_error(self, error_message: str):
        """
        Handle audio capture errors.
        
        Args:
            error_message: Error message from audio engine
        """
        logger.error(f"Audio error: {error_message}")
        self.error_occurred.emit(error_message)
    
    def _on_error(self, error_message: str):
        """
        Handle general errors.
        
        Args:
            error_message: Error message
        """
        # Show error to user
        self._show_error(error_message)
    
    def _on_device_disconnected(self):
        """Handle audio device disconnection"""
        logger.warning("Audio device disconnected")
        
        # Stop captions
        if self.is_running:
            self.stop_captions()
        
        # Show error message
        self._show_error(
            "Audio device disconnected. Please select a different device in the audio source dropdown."
        )
        
        # Refresh device list
        devices = self.audio_engine.list_devices()
        self.control_window.populate_audio_devices(devices)
    
    def _on_audio_device_changed(self, device_id: int):
        """
        Handle audio device change from control window.
        
        Args:
            device_id: New device ID
        """
        logger.info(f"Audio device changed to: {device_id}")
        
        # Update config
        self.config.audio.device_id = device_id
        self.config_manager.save(self.config)
        
        # If running, switch device
        if self.is_running:
            self.audio_engine.set_device(device_id)
    
    def _on_model_changed(self, model_name: str):
        """
        Handle model size change from control window.
        
        Args:
            model_name: New model name
        """
        logger.info(f"Model changed to: {model_name}")
        
        try:
            # Change model
            self.transcription_engine.change_model(model_name)
            
            # Update config
            self.config.transcription.model_name = model_name
            self.config_manager.save(self.config)
            
        except Exception as e:
            logger.error(f"Failed to change model: {e}")
            self._show_error(f"Failed to change model: {e}")
    
    def _on_language_changed(self, language_code: str):
        """
        Handle language change from control window.
        
        Args:
            language_code: New language code (empty string for auto-detect)
        """
        logger.info(f"Language changed to: {language_code or 'auto-detect'}")
        
        # Set language (None for auto-detect)
        lang = language_code if language_code else None
        self.transcription_engine.set_language(lang)
        
        # Update config
        self.config.transcription.language = lang
        self.config_manager.save(self.config)
    
    def _show_error(self, message: str):
        """
        Show error message to user.
        
        Args:
            message: Error message
        """
        QMessageBox.critical(
            self.control_window,
            "Error",
            message
        )
    
    def _start_device_monitoring(self):
        """Start monitoring for audio device changes"""
        from PyQt6.QtCore import QTimer
        
        # Create timer for periodic device checking
        self.device_monitor_timer = QTimer(self)
        self.device_monitor_timer.timeout.connect(self._check_device_changes)
        self.device_monitor_timer.start(5000)  # Check every 5 seconds
        
        logger.info("Device monitoring started")
    
    def _check_device_changes(self):
        """Check for audio device changes"""
        if not self.is_running:
            return
        
        try:
            # Check if current device is still available
            if self.audio_engine.detect_device_changes():
                logger.warning("Audio device change detected")
                self.device_disconnected.emit()
        except Exception as e:
            logger.error(f"Error checking device changes: {e}")
    
    def _on_overlay_destroyed(self):
        """
        Handle unexpected overlay window destruction.
        
        Recreates the overlay window if it was closed unexpectedly.
        """
        logger.warning("Overlay window was destroyed unexpectedly")
        
        try:
            # Recreate overlay
            logger.info("Recreating overlay window...")
            self.caption_overlay = CaptionOverlay(
                config=self.config.overlay,
                config_manager=self.config_manager
            )
            
            # Reconnect show/hide signals
            self.control_window.show_overlay_requested.connect(self.caption_overlay.show_overlay)
            self.control_window.hide_overlay_requested.connect(self.caption_overlay.hide_overlay)
            self.caption_overlay.destroyed.connect(self._on_overlay_destroyed)
            
            # Show overlay if it should be visible
            if self.control_window.overlay_visible:
                self.caption_overlay.show_overlay()
            
            logger.info("Overlay window recreated successfully")
            
        except Exception as e:
            logger.error(f"Failed to recreate overlay: {e}")
            self._show_error(f"Failed to recreate overlay window: {e}")
    
    def run(self):
        """
        Run the application.
        
        Handles application startup:
        - Shows control window
        - Shows overlay (initially visible)
        - Loads configuration on startup
        """
        logger.info("Starting application...")
        
        # Show control window
        self.control_window.show()
        
        # Show overlay (initially visible)
        self.caption_overlay.show_overlay()
        
        logger.info("Application running")
    
    def shutdown(self):
        """
        Gracefully shutdown the application.
        
        Handles:
        - Stopping audio capture
        - Finalizing subtitle exports
        - Saving configuration
        - Cleaning up resources
        """
        logger.info("Shutting down application...")
        
        try:
            # Stop captions if running
            if self.is_running:
                logger.info("Stopping active caption session...")
                self.stop_captions()
            
            # Finalize any open subtitle files
            if self.subtitle_exporter and not self.subtitle_exporter.is_finalized():
                logger.info("Finalizing subtitle export...")
                self.subtitle_exporter.finalize()
            
            # Save configuration
            logger.info("Saving configuration...")
            self.config_manager.save(self.config)
            logger.info("Configuration saved")
            
            # Clean up audio engine
            if self.audio_engine:
                logger.info("Cleaning up audio engine...")
                self.audio_engine.stop_capture()
            
            # Stop device monitoring
            if self.device_monitor_timer:
                self.device_monitor_timer.stop()
            
            # Hide windows
            if self.caption_overlay:
                self.caption_overlay.hide()
            
            if self.control_window:
                self.control_window.hide()
            
            logger.info("Application shutdown complete")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
            # Continue shutdown even if there's an error


def main():
    """Main entry point for the application"""
    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("OpenLiveCaption")
    app.setOrganizationName("OpenLiveCaption")
    
    try:
        # Create and run application
        live_caption_app = LiveCaptionApplication()
        live_caption_app.run()
        
        # Run Qt event loop
        exit_code = app.exec()
        
        # Shutdown gracefully
        live_caption_app.shutdown()
        
        sys.exit(exit_code)
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        QMessageBox.critical(None, "Fatal Error", f"Application failed to start: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
