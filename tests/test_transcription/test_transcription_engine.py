"""Unit tests for TranscriptionEngine"""

import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from src.transcription.transcription_engine import TranscriptionEngine, TranscriptionResult


class TestTranscriptionEngineInit:
    """Tests for TranscriptionEngine initialization"""
    
    def test_init_with_valid_model(self):
        """Test initialization with valid model name"""
        with patch('src.transcription.transcription_engine.whisper.load_model') as mock_load:
            mock_load.return_value = Mock()
            engine = TranscriptionEngine(model_name="tiny", device="cpu")
            
            assert engine.model_name == "tiny"
            assert engine.device == "cpu"
            assert engine.language is None
            assert engine.chunk_index == 0
            mock_load.assert_called_once_with("tiny", device="cpu")
    
    def test_init_with_invalid_model(self):
        """Test initialization with invalid model name raises ValueError"""
        with pytest.raises(ValueError, match="Unsupported model"):
            TranscriptionEngine(model_name="invalid", device="cpu")
    
    def test_init_model_load_failure(self):
        """Test initialization handles model loading failure"""
        with patch('src.transcription.transcription_engine.whisper.load_model') as mock_load:
            mock_load.side_effect = Exception("Model load failed")
            
            with pytest.raises(RuntimeError, match="Failed to load Whisper model"):
                TranscriptionEngine(model_name="tiny", device="cpu")
    
    def test_all_supported_models(self):
        """Test that all supported models can be initialized"""
        with patch('src.transcription.transcription_engine.whisper.load_model') as mock_load:
            mock_load.return_value = Mock()
            
            for model in ["tiny", "base", "small", "medium", "large"]:
                engine = TranscriptionEngine(model_name=model, device="cpu")
                assert engine.model_name == model


class TestTranscriptionEngineTranscribe:
    """Tests for transcription functionality"""
    
    @pytest.fixture
    def mock_engine(self):
        """Create a mock TranscriptionEngine"""
        with patch('src.transcription.transcription_engine.whisper.load_model') as mock_load:
            mock_model = Mock()
            mock_load.return_value = mock_model
            engine = TranscriptionEngine(model_name="tiny", device="cpu")
            yield engine, mock_model
    
    def test_transcribe_success(self, mock_engine):
        """Test successful transcription"""
        engine, mock_model = mock_engine
        
        # Mock transcription result
        mock_model.transcribe.return_value = {
            "text": "Hello world",
            "language": "en",
            "segments": [{"confidence": 0.95}]
        }
        
        # Create test audio
        audio = np.zeros(16000, dtype=np.float32)
        
        with patch('src.transcription.transcription_engine.sf.write'):
            with patch('src.transcription.transcription_engine.os.unlink'):
                result = engine.transcribe(audio)
        
        assert isinstance(result, TranscriptionResult)
        assert result.text == "Hello world"
        assert result.language == "en"
        assert result.confidence == 0.95
    
    def test_transcribe_with_language_override(self, mock_engine):
        """Test transcription with manual language override"""
        engine, mock_model = mock_engine
        
        mock_model.transcribe.return_value = {
            "text": "Hola mundo",
            "language": "es"
        }
        
        audio = np.zeros(16000, dtype=np.float32)
        
        with patch('src.transcription.transcription_engine.sf.write'):
            with patch('src.transcription.transcription_engine.os.unlink'):
                result = engine.transcribe(audio, language="es")
        
        # Verify language was passed to Whisper
        call_args = mock_model.transcribe.call_args
        assert call_args[1]["language"] == "es"
    
    def test_transcribe_auto_detect_fallback(self, mock_engine):
        """Test auto-detect fallback to English on failure"""
        engine, mock_model = mock_engine
        
        # First call fails, second succeeds
        mock_model.transcribe.side_effect = [
            RuntimeError("Language detection failed"),
            {"text": "Hello", "language": "en"}
        ]
        
        audio = np.zeros(16000, dtype=np.float32)
        
        with patch('src.transcription.transcription_engine.sf.write'):
            with patch('src.transcription.transcription_engine.os.unlink'):
                result = engine.transcribe(audio)
        
        assert result.text == "Hello"
        assert mock_model.transcribe.call_count == 2
    
    def test_transcribe_handles_error_gracefully(self, mock_engine):
        """Test transcription error handling returns empty result"""
        engine, mock_model = mock_engine
        
        mock_model.transcribe.side_effect = Exception("Transcription failed")
        
        audio = np.zeros(16000, dtype=np.float32)
        
        with patch('src.transcription.transcription_engine.sf.write'):
            with patch('src.transcription.transcription_engine.os.unlink'):
                result = engine.transcribe(audio)
        
        # Should return empty result, not crash
        assert result.text == ""
        assert result.language == "unknown"
        assert result.confidence == 0.0
    
    def test_transcribe_empty_text(self, mock_engine):
        """Test transcription with empty result"""
        engine, mock_model = mock_engine
        
        mock_model.transcribe.return_value = {
            "text": "",
            "language": "en"
        }
        
        audio = np.zeros(16000, dtype=np.float32)
        
        with patch('src.transcription.transcription_engine.sf.write'):
            with patch('src.transcription.transcription_engine.os.unlink'):
                result = engine.transcribe(audio)
        
        assert result.text == ""


class TestTranscriptionEngineModelSwitching:
    """Tests for model switching functionality"""
    
    def test_change_model_success(self):
        """Test successful model switching"""
        with patch('src.transcription.transcription_engine.whisper.load_model') as mock_load:
            mock_load.return_value = Mock()
            
            engine = TranscriptionEngine(model_name="tiny", device="cpu")
            assert engine.model_name == "tiny"
            
            engine.change_model("base")
            assert engine.model_name == "base"
            assert mock_load.call_count == 2
    
    def test_change_model_invalid(self):
        """Test changing to invalid model raises ValueError"""
        with patch('src.transcription.transcription_engine.whisper.load_model') as mock_load:
            mock_load.return_value = Mock()
            
            engine = TranscriptionEngine(model_name="tiny", device="cpu")
            
            with pytest.raises(ValueError, match="Unsupported model"):
                engine.change_model("invalid")
    
    def test_change_model_same_model(self):
        """Test changing to same model does nothing"""
        with patch('src.transcription.transcription_engine.whisper.load_model') as mock_load:
            mock_load.return_value = Mock()
            
            engine = TranscriptionEngine(model_name="tiny", device="cpu")
            initial_call_count = mock_load.call_count
            
            engine.change_model("tiny")
            
            # Should not reload model
            assert mock_load.call_count == initial_call_count


class TestTranscriptionEngineLanguageConfig:
    """Tests for language configuration"""
    
    def test_set_language(self):
        """Test setting fixed language"""
        with patch('src.transcription.transcription_engine.whisper.load_model') as mock_load:
            mock_load.return_value = Mock()
            
            engine = TranscriptionEngine(model_name="tiny", device="cpu")
            assert engine.language is None
            
            engine.set_language("es")
            assert engine.language == "es"
    
    def test_set_language_none_enables_auto_detect(self):
        """Test setting language to None enables auto-detection"""
        with patch('src.transcription.transcription_engine.whisper.load_model') as mock_load:
            mock_load.return_value = Mock()
            
            engine = TranscriptionEngine(model_name="tiny", device="cpu")
            engine.set_language("es")
            assert engine.language == "es"
            
            engine.set_language(None)
            assert engine.language is None


class TestTranscriptionEngineOverlapping:
    """Tests for overlapping chunk processing"""
    
    @pytest.fixture
    def mock_engine(self):
        """Create a mock TranscriptionEngine"""
        with patch('src.transcription.transcription_engine.whisper.load_model') as mock_load:
            mock_model = Mock()
            mock_model.transcribe.return_value = {
                "text": "Test",
                "language": "en"
            }
            mock_load.return_value = mock_model
            engine = TranscriptionEngine(model_name="tiny", device="cpu")
            yield engine
    
    def test_process_with_overlap_first_chunk(self, mock_engine):
        """Test first chunk returns None (need 2 chunks for overlap)"""
        audio = np.zeros(16000, dtype=np.float32)
        
        result = mock_engine.process_with_overlap(audio)
        assert result is None
        assert len(mock_engine.audio_buffer) == 1
    
    def test_process_with_overlap_second_chunk(self, mock_engine):
        """Test second chunk processes with overlap"""
        audio1 = np.zeros(16000, dtype=np.float32)
        audio2 = np.ones(16000, dtype=np.float32)
        
        # First chunk
        result1 = mock_engine.process_with_overlap(audio1)
        assert result1 is None
        
        # Second chunk should process
        with patch('src.transcription.transcription_engine.sf.write'):
            with patch('src.transcription.transcription_engine.os.unlink'):
                result2 = mock_engine.process_with_overlap(audio2)
        
        assert result2 is not None
        assert isinstance(result2, TranscriptionResult)
        # Buffer should keep only last chunk
        assert len(mock_engine.audio_buffer) == 1
    
    def test_reset_buffer(self, mock_engine):
        """Test buffer reset"""
        audio1 = np.zeros(16000, dtype=np.float32)
        audio2 = np.ones(16000, dtype=np.float32)
        
        # Process two chunks to increment chunk_index
        mock_engine.process_with_overlap(audio1)
        with patch('src.transcription.transcription_engine.sf.write'):
            with patch('src.transcription.transcription_engine.os.unlink'):
                mock_engine.process_with_overlap(audio2)
        
        assert len(mock_engine.audio_buffer) == 1
        assert mock_engine.chunk_index > 0
        
        mock_engine.reset_buffer()
        
        assert len(mock_engine.audio_buffer) == 0
        assert mock_engine.chunk_index == 0
