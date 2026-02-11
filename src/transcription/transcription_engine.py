"""Transcription engine using OpenAI Whisper"""

import whisper
import numpy as np
import torch
import os
import tempfile
import soundfile as sf
import logging
from dataclasses import dataclass
from typing import Optional, List
from pathlib import Path


# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class TranscriptionResult:
    """Result from transcription operation"""
    text: str
    language: str
    confidence: float
    start_time: float
    end_time: float


class TranscriptionEngine:
    """
    Transcription engine using OpenAI Whisper.
    
    Supports configurable model sizes, language detection/override,
    and overlapping chunk processing for continuous speech.
    """
    
    SUPPORTED_MODELS = ["tiny", "base", "small", "medium", "large"]
    
    def __init__(self, model_name: str = "tiny", device: str = "cpu"):
        """
        Initialize TranscriptionEngine with Whisper model.
        
        Args:
            model_name: Whisper model size (tiny, base, small, medium, large)
            device: Device to run model on ("cpu" or "cuda")
        
        Raises:
            ValueError: If model_name is not supported
            RuntimeError: If model fails to load
        """
        if model_name not in self.SUPPORTED_MODELS:
            raise ValueError(
                f"Unsupported model '{model_name}'. "
                f"Supported models: {', '.join(self.SUPPORTED_MODELS)}"
            )
        
        self.model_name = model_name
        self.device = device
        self.language = None  # None = auto-detect
        self.model = None
        self.audio_buffer: List[np.ndarray] = []
        self.chunk_index = 0
        self.sample_rate = 16000
        
        # Configure threading for CPU performance
        if device == "cpu":
            os.environ["OMP_NUM_THREADS"] = "1"
            os.environ["MKL_NUM_THREADS"] = "1"
            os.environ["OPENBLAS_NUM_THREADS"] = "1"
            try:
                torch.set_num_threads(1)
                torch.set_num_interop_threads(1)
            except Exception:
                pass
        
        # Load model
        self._load_model()
    
    def _load_model(self):
        """Load Whisper model"""
        try:
            logger.info(f"Loading Whisper model '{self.model_name}' on device '{self.device}'...")
            self.model = whisper.load_model(self.model_name, device=self.device)
            logger.info(f"Model '{self.model_name}' loaded successfully")
        except Exception as e:
            error_msg = f"Failed to load Whisper model '{self.model_name}': {e}"
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e
    
    def transcribe(
        self, 
        audio: np.ndarray, 
        language: Optional[str] = None
    ) -> TranscriptionResult:
        """
        Transcribe audio chunk and return result.
        
        Args:
            audio: Audio data as float32 numpy array (16kHz sample rate)
            language: Optional language code to override auto-detection
        
        Returns:
            TranscriptionResult with text, language, confidence, and timestamps
        
        Raises:
            RuntimeError: If transcription fails
        """
        if self.model is None:
            raise RuntimeError("Model not loaded")
        
        # Use instance language setting if not overridden
        lang = language if language is not None else self.language
        
        # Calculate timestamps
        start_time = self.chunk_index * len(audio) / self.sample_rate
        end_time = start_time + len(audio) / self.sample_rate
        
        try:
            # Write audio to temporary file for Whisper
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp_path = tmp.name
            
            try:
                sf.write(tmp_path, audio, self.sample_rate)
                
                # Transcribe with language specification
                try:
                    if lang:
                        result = self.model.transcribe(
                            tmp_path, 
                            language=lang, 
                            fp16=False, 
                            verbose=False
                        )
                    else:
                        # Auto-detect language
                        try:
                            result = self.model.transcribe(
                                tmp_path, 
                                language=None, 
                                fp16=False, 
                                verbose=False
                            )
                        except (RuntimeError, ValueError, KeyError) as e:
                            # If auto-detect fails, fallback to English
                            logger.warning(f"Language auto-detection failed, using English: {e}")
                            result = self.model.transcribe(
                                tmp_path, 
                                language="en", 
                                fp16=False, 
                                verbose=False
                            )
                except Exception as e:
                    error_msg = f"Transcription failed: {e}"
                    logger.error(error_msg)
                    raise RuntimeError(error_msg) from e
                
            finally:
                # Clean up temp file
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass
            
            # Extract result data
            text = result.get("text", "").strip()
            detected_lang = result.get("language") or result.get("lang", "unknown")
            
            # Whisper doesn't provide confidence directly, use segments if available
            confidence = 0.0
            if "segments" in result and result["segments"]:
                # Average confidence from segments
                confidences = [
                    seg.get("confidence", 0.0) 
                    for seg in result["segments"] 
                    if "confidence" in seg
                ]
                if confidences:
                    confidence = sum(confidences) / len(confidences)
            
            self.chunk_index += 1
            
            return TranscriptionResult(
                text=text,
                language=detected_lang,
                confidence=confidence,
                start_time=start_time,
                end_time=end_time
            )
            
        except Exception as e:
            # Log error but don't crash - allow processing to continue
            logger.error(f"Error during transcription: {e}")
            # Return empty result to allow processing to continue
            self.chunk_index += 1
            return TranscriptionResult(
                text="",
                language="unknown",
                confidence=0.0,
                start_time=start_time,
                end_time=end_time
            )
    
    def change_model(self, model_name: str):
        """
        Switch to a different Whisper model without restarting application.
        
        Args:
            model_name: New model size (tiny, base, small, medium, large)
        
        Raises:
            ValueError: If model_name is not supported
            RuntimeError: If model fails to load
        """
        if model_name not in self.SUPPORTED_MODELS:
            raise ValueError(
                f"Unsupported model '{model_name}'. "
                f"Supported models: {', '.join(self.SUPPORTED_MODELS)}"
            )
        
        if model_name == self.model_name:
            logger.info(f"Model '{model_name}' already loaded")
            return
        
        logger.info(f"Switching from model '{self.model_name}' to '{model_name}'...")
        
        # Unload old model
        self.model = None
        
        # Update model name
        self.model_name = model_name
        
        # Load new model
        self._load_model()
        
        logger.info(f"Successfully switched to model '{model_name}'")
    
    def set_language(self, language: Optional[str]):
        """
        Set fixed language or enable auto-detection.
        
        Args:
            language: Language code (e.g., "en", "es") or None for auto-detect
        """
        self.language = language
        if language:
            logger.info(f"Language set to: {language}")
        else:
            logger.info("Language auto-detection enabled")
    
    def process_with_overlap(
        self, 
        audio_chunk: np.ndarray, 
        overlap_seconds: float = 0.5
    ) -> Optional[TranscriptionResult]:
        """
        Process audio with overlapping chunks to avoid cutting words.
        
        Args:
            audio_chunk: New audio chunk (1 second duration)
            overlap_seconds: Overlap duration in seconds (default 0.5)
        
        Returns:
            TranscriptionResult if buffer is ready, None otherwise
        """
        # Add chunk to buffer
        self.audio_buffer.append(audio_chunk)
        
        # Need at least 2 chunks to create overlap
        if len(self.audio_buffer) < 2:
            return None
        
        # Combine last two chunks with overlap
        combined = np.concatenate(self.audio_buffer[-2:])
        
        # Transcribe combined audio
        result = self.transcribe(combined)
        
        # Keep only last chunk for next iteration
        self.audio_buffer = self.audio_buffer[-1:]
        
        return result
    
    def reset_buffer(self):
        """Reset audio buffer (useful when starting new session)"""
        self.audio_buffer = []
        self.chunk_index = 0
        logger.info("Audio buffer reset")
