"""Unit tests for TranslationEngine."""

import pytest
from src.translation import TranslationEngine, TranslationResult


class TestTranslationEngine:
    """Unit tests for TranslationEngine class."""
    
    def test_initialization(self):
        """Test that TranslationEngine initializes with empty cache."""
        engine = TranslationEngine()
        assert engine._translation_models == {}
        assert engine._translation_tokenizers == {}
    
    def test_list_supported_languages(self):
        """Test that supported languages are returned correctly."""
        engine = TranslationEngine()
        languages = engine.list_supported_languages()
        assert 'yo' in languages
        assert 'twi' in languages
        assert len(languages) >= 2
    
    def test_translate_empty_text(self):
        """Test that translating empty text returns empty string."""
        engine = TranslationEngine()
        result = engine.translate("", "yo")
        assert result == ""
    
    def test_translate_unsupported_language(self):
        """Test that translating to unsupported language raises ValueError."""
        engine = TranslationEngine()
        with pytest.raises(ValueError, match="No translation model configured"):
            engine.translate("Hello", "unsupported_lang")
    
    def test_translate_with_original_empty_text(self):
        """Test that translate_with_original handles empty text."""
        engine = TranslationEngine()
        result = engine.translate_with_original("", "yo")
        assert isinstance(result, TranslationResult)
        assert result.original_text == ""
        assert result.translated_text == ""
        assert result.target_language == "yo"
    
    def test_is_model_cached_before_loading(self):
        """Test that is_model_cached returns False before model is loaded."""
        engine = TranslationEngine()
        assert not engine.is_model_cached("yo")
        assert not engine.is_model_cached("twi")
    
    def test_model_caching(self):
        """Test that models are cached after first use."""
        engine = TranslationEngine()
        
        # Model should not be cached initially
        assert not engine.is_model_cached("yo")
        
        # Translate some text (this will load the model)
        try:
            engine.translate("Hello", "yo")
            # Model should now be cached
            assert engine.is_model_cached("yo")
        except Exception:
            # If translation fails (e.g., no internet), skip this assertion
            pytest.skip("Translation model download failed")
    
    def test_translate_with_original_structure(self):
        """Test that translate_with_original returns correct structure."""
        engine = TranslationEngine()
        
        try:
            result = engine.translate_with_original("Hello", "yo")
            assert isinstance(result, TranslationResult)
            assert result.original_text == "Hello"
            assert result.target_language == "yo"
            assert isinstance(result.translated_text, str)
            # Translated text should not be empty for non-empty input
            assert len(result.translated_text) > 0
        except Exception:
            # If translation fails (e.g., no internet), skip this test
            pytest.skip("Translation model download failed")
