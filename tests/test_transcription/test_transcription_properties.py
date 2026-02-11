"""Property-based tests for TranscriptionEngine

These tests validate universal correctness properties across all inputs
using hypothesis for property-based testing.

Feature: system-wide-live-captions
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from hypothesis import given, strategies as st, assume, settings
from src.transcription.transcription_engine import TranscriptionEngine, TranscriptionResult


# Test strategies
model_names = st.sampled_from(["tiny", "base", "small", "medium", "large"])
language_codes = st.sampled_from(["en", "es", "fr", "de", "zh", "ja", "ko", None])
audio_durations = st.floats(min_value=0.1, max_value=5.0)


# Feature: system-wide-live-captions, Property 16: All Whisper model sizes supported
@given(model_name=model_names)
@settings(max_examples=100, deadline=None)
def test_property_16_all_model_sizes_supported(model_name):
    """
    Property 16: All Whisper model sizes supported
    
    For any Whisper model size (tiny, base, small, medium, large),
    the Transcription_Engine should successfully load and use that model for transcription.
    
    Validates: Requirements 3.3
    """
    with patch('src.transcription.transcription_engine.whisper.load_model') as mock_load:
        mock_model = Mock()
        mock_model.transcribe.return_value = {
            "text": "Test transcription",
            "language": "en",
            "segments": [{"confidence": 0.9}]
        }
        mock_load.return_value = mock_model
        
        # Should successfully initialize with any supported model
        engine = TranscriptionEngine(model_name=model_name, device="cpu")
        
        # Verify model was loaded
        assert engine.model_name == model_name
        assert engine.model is not None
        mock_load.assert_called_once_with(model_name, device="cpu")
        
        # Verify model can be used for transcription
        audio = np.zeros(16000, dtype=np.float32)
        with patch('src.transcription.transcription_engine.sf.write'):
            with patch('src.transcription.transcription_engine.os.unlink'):
                result = engine.transcribe(audio)
        
        assert isinstance(result, TranscriptionResult)
        assert result.text == "Test transcription"


# Feature: system-wide-live-captions, Property 17: Model switching without restart
@given(
    initial_model=model_names,
    target_model=model_names
)
@settings(max_examples=100, deadline=None)
def test_property_17_model_switching_without_restart(initial_model, target_model):
    """
    Property 17: Model switching without restart
    
    For any two different Whisper model sizes, calling change_model() should switch
    from the first to the second model without requiring application restart.
    
    Validates: Requirements 3.4
    """
    with patch('src.transcription.transcription_engine.whisper.load_model') as mock_load:
        mock_model = Mock()
        mock_model.transcribe.return_value = {
            "text": "Test",
            "language": "en"
        }
        mock_load.return_value = mock_model
        
        # Initialize with first model
        engine = TranscriptionEngine(model_name=initial_model, device="cpu")
        assert engine.model_name == initial_model
        initial_load_count = mock_load.call_count
        
        # Switch to second model
        engine.change_model(target_model)
        
        # Verify model was switched
        assert engine.model_name == target_model
        
        # If models are different, should have loaded new model
        if initial_model != target_model:
            assert mock_load.call_count == initial_load_count + 1
            # Verify new model was loaded with correct name
            last_call = mock_load.call_args
            assert last_call[0][0] == target_model
        else:
            # Same model, should not reload
            assert mock_load.call_count == initial_load_count
        
        # Verify engine still works after switch
        audio = np.zeros(16000, dtype=np.float32)
        with patch('src.transcription.transcription_engine.sf.write'):
            with patch('src.transcription.transcription_engine.os.unlink'):
                result = engine.transcribe(audio)
        
        assert isinstance(result, TranscriptionResult)


# Feature: system-wide-live-captions, Property 18: Manual language override
@given(
    model_name=model_names,
    language=language_codes
)
@settings(max_examples=100, deadline=None)
def test_property_18_manual_language_override(model_name, language):
    """
    Property 18: Manual language override
    
    For any supported language code, setting a fixed language should override
    auto-detection and force transcription in that language.
    
    Validates: Requirements 3.6
    """
    with patch('src.transcription.transcription_engine.whisper.load_model') as mock_load:
        mock_model = Mock()
        
        # Mock transcription to return the requested language
        def mock_transcribe(audio_path, language=None, **kwargs):
            return {
                "text": "Test transcription",
                "language": language if language else "en",
                "segments": [{"confidence": 0.9}]
            }
        
        mock_model.transcribe.side_effect = mock_transcribe
        mock_load.return_value = mock_model
        
        engine = TranscriptionEngine(model_name=model_name, device="cpu")
        
        # Set language
        engine.set_language(language)
        assert engine.language == language
        
        # Transcribe audio
        audio = np.zeros(16000, dtype=np.float32)
        with patch('src.transcription.transcription_engine.sf.write'):
            with patch('src.transcription.transcription_engine.os.unlink'):
                result = engine.transcribe(audio)
        
        # Verify transcription was called with correct language parameter
        call_args = mock_model.transcribe.call_args
        if language is not None:
            # Language should be passed to Whisper
            assert call_args[1]["language"] == language
        else:
            # None means auto-detect
            assert call_args[1]["language"] is None


# Feature: system-wide-live-captions, Property 19: Overlapping chunk processing
@given(
    num_chunks=st.integers(min_value=2, max_value=10),
    chunk_size=st.integers(min_value=8000, max_value=32000)
)
@settings(max_examples=100, deadline=None)
def test_property_19_overlapping_chunk_processing(num_chunks, chunk_size):
    """
    Property 19: Overlapping chunk processing
    
    For any continuous audio stream, the Transcription_Engine should process audio
    in overlapping chunks to avoid cutting words at chunk boundaries.
    
    Validates: Requirements 3.7
    """
    with patch('src.transcription.transcription_engine.whisper.load_model') as mock_load:
        mock_model = Mock()
        mock_model.transcribe.return_value = {
            "text": "Test",
            "language": "en",
            "segments": [{"confidence": 0.9}]
        }
        mock_load.return_value = mock_model
        
        engine = TranscriptionEngine(model_name="tiny", device="cpu")
        
        results = []
        for i in range(num_chunks):
            # Generate unique audio chunk
            audio = np.full(chunk_size, fill_value=float(i), dtype=np.float32)
            
            with patch('src.transcription.transcription_engine.sf.write'):
                with patch('src.transcription.transcription_engine.os.unlink'):
                    result = engine.process_with_overlap(audio)
            
            if result is not None:
                results.append(result)
        
        # First chunk should return None (need 2 chunks for overlap)
        # Subsequent chunks should return results
        assert len(results) == num_chunks - 1
        
        # Verify all results are valid TranscriptionResults
        for result in results:
            assert isinstance(result, TranscriptionResult)
            assert result.text is not None
            assert result.language is not None
        
        # Verify buffer management: should keep only last chunk
        assert len(engine.audio_buffer) == 1
        
        # Verify chunk index incremented correctly
        assert engine.chunk_index == num_chunks - 1


# Feature: system-wide-live-captions, Property 20: Continue after transcription errors
@given(
    num_chunks=st.integers(min_value=3, max_value=10),
    error_chunk_index=st.integers(min_value=0, max_value=2)
)
@settings(max_examples=100, deadline=None)
def test_property_20_continue_after_transcription_errors(num_chunks, error_chunk_index):
    """
    Property 20: Continue after transcription errors
    
    For any transcription error, the Transcription_Engine should log the error
    and continue processing subsequent audio chunks without stopping.
    
    Validates: Requirements 9.2
    """
    assume(error_chunk_index < num_chunks)
    
    with patch('src.transcription.transcription_engine.whisper.load_model') as mock_load:
        mock_model = Mock()
        
        # Track which transcribe() call we're on (0-indexed)
        call_count = [0]
        
        def mock_transcribe_with_error(*args, **kwargs):
            current_call = call_count[0]
            call_count[0] += 1
            
            # Fail on the specified chunk
            if current_call == error_chunk_index:
                raise RuntimeError("Simulated transcription error")
            
            return {
                "text": f"Chunk {current_call}",
                "language": "en",
                "segments": [{"confidence": 0.9}]
            }
        
        mock_model.transcribe.side_effect = mock_transcribe_with_error
        mock_load.return_value = mock_model
        
        engine = TranscriptionEngine(model_name="tiny", device="cpu")
        # Set language to avoid auto-detect retry logic
        engine.set_language("en")
        
        results = []
        error_occurred = False
        
        for i in range(num_chunks):
            audio = np.zeros(16000, dtype=np.float32)
            
            with patch('src.transcription.transcription_engine.sf.write'):
                with patch('src.transcription.transcription_engine.os.unlink'):
                    result = engine.transcribe(audio)
            
            results.append(result)
            
            # Check if this was the error chunk
            if i == error_chunk_index:
                # Should return empty result, not crash
                assert result.text == ""
                assert result.language == "unknown"
                assert result.confidence == 0.0
                error_occurred = True
            else:
                # Should have valid result
                assert result.text != ""
                assert result.language == "en"
        
        # Verify we got results for all chunks
        assert len(results) == num_chunks
        
        # Verify error occurred
        assert error_occurred
        
        # Verify processing continued after error
        # All chunks after error should have valid results
        for i in range(error_chunk_index + 1, num_chunks):
            result = results[i]
            assert result is not None
            assert result.text != ""
            assert result.language == "en"


# Additional property test: Model switching preserves language setting
@given(
    initial_model=model_names,
    target_model=model_names,
    language=language_codes
)
@settings(max_examples=100, deadline=None)
def test_property_model_switching_preserves_language(initial_model, target_model, language):
    """
    Property: Model switching preserves language setting
    
    When switching models, the language configuration should be preserved.
    """
    with patch('src.transcription.transcription_engine.whisper.load_model') as mock_load:
        mock_model = Mock()
        mock_load.return_value = mock_model
        
        engine = TranscriptionEngine(model_name=initial_model, device="cpu")
        engine.set_language(language)
        
        # Switch model
        engine.change_model(target_model)
        
        # Language setting should be preserved
        assert engine.language == language


# Additional property test: Buffer reset clears state
@given(
    num_chunks_before_reset=st.integers(min_value=2, max_value=5),
    num_chunks_after_reset=st.integers(min_value=2, max_value=5)
)
@settings(max_examples=100, deadline=None)
def test_property_buffer_reset_clears_state(num_chunks_before_reset, num_chunks_after_reset):
    """
    Property: Buffer reset clears state
    
    After resetting the buffer, the engine should start fresh with chunk_index=0
    and empty buffer.
    """
    with patch('src.transcription.transcription_engine.whisper.load_model') as mock_load:
        mock_model = Mock()
        mock_model.transcribe.return_value = {
            "text": "Test",
            "language": "en"
        }
        mock_load.return_value = mock_model
        
        engine = TranscriptionEngine(model_name="tiny", device="cpu")
        
        # Process some chunks
        for i in range(num_chunks_before_reset):
            audio = np.zeros(16000, dtype=np.float32)
            with patch('src.transcription.transcription_engine.sf.write'):
                with patch('src.transcription.transcription_engine.os.unlink'):
                    engine.process_with_overlap(audio)
        
        # Verify state before reset
        assert len(engine.audio_buffer) > 0
        assert engine.chunk_index > 0
        
        # Reset buffer
        engine.reset_buffer()
        
        # Verify state after reset
        assert len(engine.audio_buffer) == 0
        assert engine.chunk_index == 0
        
        # Verify engine still works after reset
        for i in range(num_chunks_after_reset):
            audio = np.zeros(16000, dtype=np.float32)
            with patch('src.transcription.transcription_engine.sf.write'):
                with patch('src.transcription.transcription_engine.os.unlink'):
                    result = engine.process_with_overlap(audio)
            
            # First chunk after reset should return None
            if i == 0:
                assert result is None
            else:
                assert result is not None
