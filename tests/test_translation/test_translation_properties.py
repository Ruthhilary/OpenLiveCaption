"""Property-based tests for TranslationEngine

These tests validate universal correctness properties across all inputs
using hypothesis for property-based testing.

Feature: system-wide-live-captions
"""

import pytest
from hypothesis import given, strategies as st, settings, assume
from unittest.mock import Mock, patch
from src.translation.translation_engine import TranslationEngine, TranslationResult


# Test strategies
supported_languages = st.sampled_from(["yo", "twi"])
text_samples = st.text(min_size=1, max_size=200, alphabet=st.characters(
    whitelist_categories=('Lu', 'Ll', 'Nd', 'Zs'),  # Letters, digits, spaces
    blacklist_characters='\x00\n\r\t'
))


# Feature: system-wide-live-captions, Property 21: Translation when enabled
@given(
    text=text_samples,
    target_lang=supported_languages
)
@settings(max_examples=100, deadline=None)
def test_property_21_translation_when_enabled(text, target_lang):
    """
    Property 21: Translation when enabled
    
    For any transcribed text, when translation is enabled, the Transcription_Engine
    should produce both original and translated text.
    
    Validates: Requirements 10.1
    """
    # Mock the MarianMT model and tokenizer
    with patch('src.translation.translation_engine.MarianTokenizer') as mock_tokenizer_class, \
         patch('src.translation.translation_engine.MarianMTModel') as mock_model_class:
        
        # Create mock instances
        mock_tokenizer = Mock()
        mock_model = Mock()
        
        # Configure tokenizer mock
        mock_tokenizer.return_value = {"input_ids": [[1, 2, 3]]}
        mock_tokenizer.decode.return_value = f"Translated: {text}"
        
        # Configure model mock
        mock_model.generate.return_value = [[1, 2, 3]]
        
        # Set up class mocks to return instances
        mock_tokenizer_class.from_pretrained.return_value = mock_tokenizer
        mock_model_class.from_pretrained.return_value = mock_model
        
        # Create engine
        engine = TranslationEngine()
        
        # Translate with original
        result = engine.translate_with_original(text, target_lang)
        
        # Verify result structure
        assert isinstance(result, TranslationResult)
        
        # Verify original text is preserved
        assert result.original_text == text
        
        # Verify translated text is present
        assert result.translated_text is not None
        assert isinstance(result.translated_text, str)
        assert len(result.translated_text) > 0
        
        # Verify target language is recorded
        assert result.target_language == target_lang
        
        # Verify both texts are different (unless text is empty)
        if text:
            # Translation should produce some output
            assert result.translated_text != ""


# Feature: system-wide-live-captions, Property 22: Translation model caching
@given(
    text1=text_samples,
    text2=text_samples,
    target_lang=supported_languages
)
@settings(max_examples=100, deadline=None)
def test_property_22_translation_model_caching(text1, text2, target_lang):
    """
    Property 22: Translation model caching
    
    For any translation model, loading the model a second time should not trigger
    a download or reload, but should use the cached model.
    
    Validates: Requirements 10.5
    """
    # Ensure we have two different texts to translate
    assume(text1 != text2)
    
    # Mock the MarianMT model and tokenizer
    with patch('src.translation.translation_engine.MarianTokenizer') as mock_tokenizer_class, \
         patch('src.translation.translation_engine.MarianMTModel') as mock_model_class:
        
        # Create mock instances
        mock_tokenizer = Mock()
        mock_model = Mock()
        
        # Configure tokenizer mock
        def tokenizer_side_effect(text, **kwargs):
            return {"input_ids": [[1, 2, 3]]}
        
        mock_tokenizer.side_effect = tokenizer_side_effect
        mock_tokenizer.decode.side_effect = lambda x, **kwargs: f"Translated: {x}"
        
        # Configure model mock
        mock_model.generate.return_value = [[1, 2, 3]]
        
        # Set up class mocks to return instances
        mock_tokenizer_class.from_pretrained.return_value = mock_tokenizer
        mock_model_class.from_pretrained.return_value = mock_model
        
        # Create engine
        engine = TranslationEngine()
        
        # Verify model is not cached initially
        assert not engine.is_model_cached(target_lang)
        
        # First translation - should load model
        result1 = engine.translate(text1, target_lang)
        
        # Verify model was loaded
        assert mock_tokenizer_class.from_pretrained.call_count == 1
        assert mock_model_class.from_pretrained.call_count == 1
        
        # Verify model is now cached
        assert engine.is_model_cached(target_lang)
        
        # Second translation - should use cached model
        result2 = engine.translate(text2, target_lang)
        
        # Verify model was NOT loaded again (still 1 call)
        assert mock_tokenizer_class.from_pretrained.call_count == 1
        assert mock_model_class.from_pretrained.call_count == 1
        
        # Verify both translations succeeded
        assert isinstance(result1, str)
        assert isinstance(result2, str)
        assert len(result1) > 0
        assert len(result2) > 0
        
        # Verify the same model instance was used
        assert engine._translation_models[target_lang] is mock_model
        assert engine._translation_tokenizers[target_lang] is mock_tokenizer


# Additional property test: Empty text handling
@given(target_lang=supported_languages)
@settings(max_examples=100, deadline=None)
def test_property_empty_text_handling(target_lang):
    """
    Property: Empty text handling
    
    For any target language, translating empty text should return empty string
    without attempting to load models.
    """
    engine = TranslationEngine()
    
    # Translate empty text
    result = engine.translate("", target_lang)
    
    # Should return empty string
    assert result == ""
    
    # Model should not be cached (no need to load for empty text)
    assert not engine.is_model_cached(target_lang)
    
    # Test with translate_with_original
    result_with_original = engine.translate_with_original("", target_lang)
    
    # Should return empty TranslationResult
    assert isinstance(result_with_original, TranslationResult)
    assert result_with_original.original_text == ""
    assert result_with_original.translated_text == ""
    assert result_with_original.target_language == target_lang


# Additional property test: Unsupported language handling
@given(
    text=text_samples,
    unsupported_lang=st.text(min_size=1, max_size=10, alphabet=st.characters(
        whitelist_categories=('Ll',)
    )).filter(lambda x: x not in ["yo", "twi"])
)
@settings(max_examples=100, deadline=None)
def test_property_unsupported_language_handling(text, unsupported_lang):
    """
    Property: Unsupported language handling
    
    For any unsupported language, translation should raise ValueError
    with a clear error message.
    """
    engine = TranslationEngine()
    
    # Attempt to translate to unsupported language
    with pytest.raises(ValueError) as exc_info:
        engine.translate(text, unsupported_lang)
    
    # Verify error message is informative
    assert "No translation model configured" in str(exc_info.value)
    assert unsupported_lang in str(exc_info.value)
    
    # Verify model was not cached
    assert not engine.is_model_cached(unsupported_lang)


# Additional property test: Multiple language caching
@given(
    text=text_samples,
    lang1=st.just("yo"),
    lang2=st.just("twi")
)
@settings(max_examples=100, deadline=None)
def test_property_multiple_language_caching(text, lang1, lang2):
    """
    Property: Multiple language caching
    
    The engine should be able to cache models for multiple languages
    simultaneously without interference.
    """
    # Mock the MarianMT model and tokenizer
    with patch('src.translation.translation_engine.MarianTokenizer') as mock_tokenizer_class, \
         patch('src.translation.translation_engine.MarianMTModel') as mock_model_class:
        
        # Create separate mock instances for each language
        mock_tokenizer1 = Mock()
        mock_model1 = Mock()
        mock_tokenizer2 = Mock()
        mock_model2 = Mock()
        
        # Configure mocks
        mock_tokenizer1.return_value = {"input_ids": [[1, 2, 3]]}
        mock_tokenizer1.decode.return_value = f"Yoruba: {text}"
        mock_model1.generate.return_value = [[1, 2, 3]]
        
        mock_tokenizer2.return_value = {"input_ids": [[4, 5, 6]]}
        mock_tokenizer2.decode.return_value = f"Twi: {text}"
        mock_model2.generate.return_value = [[4, 5, 6]]
        
        # Set up class mocks to return different instances based on model name
        def tokenizer_factory(model_name):
            if "yo" in model_name:
                return mock_tokenizer1
            else:
                return mock_tokenizer2
        
        def model_factory(model_name):
            if "yo" in model_name:
                return mock_model1
            else:
                return mock_model2
        
        mock_tokenizer_class.from_pretrained.side_effect = tokenizer_factory
        mock_model_class.from_pretrained.side_effect = model_factory
        
        # Create engine
        engine = TranslationEngine()
        
        # Translate to first language
        result1 = engine.translate(text, lang1)
        assert engine.is_model_cached(lang1)
        assert not engine.is_model_cached(lang2)
        
        # Translate to second language
        result2 = engine.translate(text, lang2)
        assert engine.is_model_cached(lang1)
        assert engine.is_model_cached(lang2)
        
        # Verify both models are cached
        assert len(engine._translation_models) == 2
        assert len(engine._translation_tokenizers) == 2
        
        # Verify correct models are cached
        assert engine._translation_models[lang1] is mock_model1
        assert engine._translation_models[lang2] is mock_model2
        assert engine._translation_tokenizers[lang1] is mock_tokenizer1
        assert engine._translation_tokenizers[lang2] is mock_tokenizer2
        
        # Translate again to first language (should use cache)
        result3 = engine.translate(text, lang1)
        
        # Verify no additional model loads
        assert mock_tokenizer_class.from_pretrained.call_count == 2
        assert mock_model_class.from_pretrained.call_count == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
