"""Translation engine for OpenLiveCaption using MarianMT models."""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from transformers import MarianMTModel, MarianTokenizer


@dataclass
class TranslationResult:
    """Result of a translation operation.
    
    Attributes:
        original_text: The original English text
        translated_text: The translated text in the target language
        target_language: The target language code
    """
    original_text: str
    translated_text: str
    target_language: str


class TranslationEngine:
    """Translation engine that uses MarianMT models for text translation.
    
    This class implements lazy loading of translation models to avoid
    downloading models until they are actually needed. Models are cached
    in memory after first use to avoid re-downloading.
    
    Supports Yoruba and Twi languages as per existing functionality.
    """
    
    # Mapping of target language keys to Marian model names (English->target)
    # Using Helsinki-NLP OPUS-MT models for translation
    MODEL_MAP = {
        # European Languages
        "es": "Helsinki-NLP/opus-mt-en-es",    # English -> Spanish
        "fr": "Helsinki-NLP/opus-mt-en-fr",    # English -> French
        "de": "Helsinki-NLP/opus-mt-en-de",    # English -> German
        "pt": "Helsinki-NLP/opus-mt-en-roa",   # English -> Portuguese (Romance)
        "ru": "Helsinki-NLP/opus-mt-en-ru",    # English -> Russian
        "it": "Helsinki-NLP/opus-mt-en-it",    # English -> Italian
        "nl": "Helsinki-NLP/opus-mt-en-nl",    # English -> Dutch
        "pl": "Helsinki-NLP/opus-mt-en-pl",    # English -> Polish
        "tr": "Helsinki-NLP/opus-mt-en-tr",    # English -> Turkish
        "uk": "Helsinki-NLP/opus-mt-en-uk",    # English -> Ukrainian
        "el": "Helsinki-NLP/opus-mt-en-el",    # English -> Greek
        "sv": "Helsinki-NLP/opus-mt-en-sv",    # English -> Swedish
        "da": "Helsinki-NLP/opus-mt-en-da",    # English -> Danish
        "fi": "Helsinki-NLP/opus-mt-en-fi",    # English -> Finnish
        "no": "Helsinki-NLP/opus-mt-en-no",    # English -> Norwegian
        "cs": "Helsinki-NLP/opus-mt-en-cs",    # English -> Czech
        "hu": "Helsinki-NLP/opus-mt-en-hu",    # English -> Hungarian
        "ro": "Helsinki-NLP/opus-mt-en-ro",    # English -> Romanian
        "bg": "Helsinki-NLP/opus-mt-en-bg",    # English -> Bulgarian
        "sr": "Helsinki-NLP/opus-mt-en-sla",   # English -> Serbian (Slavic)
        "hr": "Helsinki-NLP/opus-mt-en-sla",   # English -> Croatian (Slavic)
        "sk": "Helsinki-NLP/opus-mt-en-sla",   # English -> Slovak (Slavic)
        "sl": "Helsinki-NLP/opus-mt-en-sla",   # English -> Slovenian (Slavic)
        "lt": "Helsinki-NLP/opus-mt-en-lt",    # English -> Lithuanian
        "lv": "Helsinki-NLP/opus-mt-en-lv",    # English -> Latvian
        "et": "Helsinki-NLP/opus-mt-en-et",    # English -> Estonian
        "mt": "Helsinki-NLP/opus-mt-en-mt",    # English -> Maltese
        "ga": "Helsinki-NLP/opus-mt-en-ga",    # English -> Irish
        "cy": "Helsinki-NLP/opus-mt-en-cy",    # English -> Welsh
        "is": "Helsinki-NLP/opus-mt-en-is",    # English -> Icelandic
        
        # Asian Languages
        "zh": "Helsinki-NLP/opus-mt-en-zh",    # English -> Chinese
        "hi": "Helsinki-NLP/opus-mt-en-hi",    # English -> Hindi
        "ar": "Helsinki-NLP/opus-mt-en-ar",    # English -> Arabic
        "ja": "Helsinki-NLP/opus-mt-en-jap",   # English -> Japanese
        "ko": "Helsinki-NLP/opus-mt-en-ko",    # English -> Korean
        "vi": "Helsinki-NLP/opus-mt-en-vi",    # English -> Vietnamese
        "th": "Helsinki-NLP/opus-mt-en-th",    # English -> Thai
        "fa": "Helsinki-NLP/opus-mt-en-fa",    # English -> Persian
        "he": "Helsinki-NLP/opus-mt-en-he",    # English -> Hebrew
        "id": "Helsinki-NLP/opus-mt-en-id",    # English -> Indonesian
        "ms": "Helsinki-NLP/opus-mt-en-ms",    # English -> Malay
        "fil": "Helsinki-NLP/opus-mt-en-phi",  # English -> Filipino (Philippine)
        "bn": "Helsinki-NLP/opus-mt-en-bn",    # English -> Bengali
        "ur": "Helsinki-NLP/opus-mt-en-ur",    # English -> Urdu
        
        # African Languages
        "yo": "Helsinki-NLP/opus-mt-en-yo",    # English -> Yoruba
        "twi": "Helsinki-NLP/opus-mt-en-tw",   # English -> Twi
        "sw": "Helsinki-NLP/opus-mt-en-sw",    # English -> Swahili
        "af": "Helsinki-NLP/opus-mt-en-af",    # English -> Afrikaans
    }
    
    def __init__(self):
        """Initialize translation engine with empty model cache.
        
        Models are loaded lazily on first use to avoid unnecessary
        downloads and memory usage.
        """
        self._translation_models: Dict[str, MarianMTModel] = {}
        self._translation_tokenizers: Dict[str, MarianTokenizer] = {}
    
    def _get_translation_model(self, lang_key: str) -> Tuple[MarianTokenizer, MarianMTModel]:
        """Get or load translation model and tokenizer for the given language.
        
        Args:
            lang_key: Language code (e.g., 'yo' for Yoruba, 'twi' for Twi)
            
        Returns:
            Tuple of (tokenizer, model)
            
        Raises:
            ValueError: If no translation model is configured for the language
        """
        # Return cached model if available
        if lang_key in self._translation_models:
            return self._translation_tokenizers[lang_key], self._translation_models[lang_key]
        
        # Get model name from mapping
        model_name = self.MODEL_MAP.get(lang_key)
        if not model_name:
            raise ValueError(f"No translation model configured for '{lang_key}'")
        
        # Load model and tokenizer (lazy loading)
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        
        # Cache for future use
        self._translation_tokenizers[lang_key] = tokenizer
        self._translation_models[lang_key] = model
        
        return tokenizer, model
    
    def translate(self, text: str, target_lang: str) -> str:
        """Translate English text to the target language.
        
        This method lazily downloads and caches the MarianMT model/tokenizer
        on first use for each language.
        
        Args:
            text: English text to translate
            target_lang: Target language code (e.g., 'yo', 'twi')
            
        Returns:
            Translated text in the target language
            
        Raises:
            ValueError: If target language is not supported
        """
        if not text:
            return ""
        
        # Get or load the translation model
        tokenizer, model = self._get_translation_model(target_lang)
        
        # Tokenize input text
        tokens = tokenizer(text, return_tensors="pt", padding=True)
        
        # Generate translation
        translated = model.generate(**tokens, max_length=512)
        
        # Decode and return translated text
        return tokenizer.decode(translated[0], skip_special_tokens=True)
    
    def translate_with_original(self, text: str, target_lang: str) -> TranslationResult:
        """Translate text and return both original and translated text.
        
        This method supports dual-language display by returning both the
        original English text and the translated text in a structured format.
        
        Args:
            text: English text to translate
            target_lang: Target language code (e.g., 'yo', 'twi')
            
        Returns:
            TranslationResult containing original and translated text
            
        Raises:
            ValueError: If target language is not supported
        """
        if not text:
            return TranslationResult(
                original_text="",
                translated_text="",
                target_language=target_lang
            )
        
        # Translate the text
        translated_text = self.translate(text, target_lang)
        
        # Return both original and translated
        return TranslationResult(
            original_text=text,
            translated_text=translated_text,
            target_language=target_lang
        )
    
    def is_model_cached(self, lang_key: str) -> bool:
        """Check if a translation model is already cached in memory.
        
        This method allows checking whether a model has been loaded without
        triggering a download.
        
        Args:
            lang_key: Language code to check
            
        Returns:
            True if the model is cached, False otherwise
        """
        return lang_key in self._translation_models
    
    def list_supported_languages(self) -> List[str]:
        """Return list of supported target languages.
        
        Returns:
            List of language codes (e.g., ['yo', 'twi'])
        """
        return list(self.MODEL_MAP.keys())
