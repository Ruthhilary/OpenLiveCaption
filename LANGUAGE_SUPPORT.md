# OpenLiveCaption Language Support

OpenLiveCaption supports transcription and translation for a wide range of languages.

## Transcription Support (Whisper)

OpenLiveCaption uses OpenAI Whisper for speech-to-text transcription, which supports **99+ languages** with automatic language detection.

### Supported Languages for Transcription

All of the following languages are supported for transcription with automatic language detection:

#### European Languages
- 🇺🇸 **English** (en)
- 🇪🇸 **Spanish** (es)
- 🇫🇷 **French** (fr)
- 🇩🇪 **German** (de)
- 🇵🇹 **Portuguese** (pt)
- 🇷🇺 **Russian** (ru)
- 🇮🇹 **Italian** (it)
- 🇳🇱 **Dutch** (nl)
- 🇵🇱 **Polish** (pl)
- 🇹🇷 **Turkish** (tr)
- 🇺🇦 **Ukrainian** (uk)
- 🇬🇷 **Greek** (el)
- 🇸🇪 **Swedish** (sv)
- 🇩🇰 **Danish** (da)
- 🇫🇮 **Finnish** (fi)
- 🇳🇴 **Norwegian** (no)
- 🇨🇿 **Czech** (cs)
- 🇭🇺 **Hungarian** (hu)
- 🇷🇴 **Romanian** (ro)
- 🇧🇬 **Bulgarian** (bg)
- 🇷🇸 **Serbian** (sr)
- 🇭🇷 **Croatian** (hr)
- 🇸🇰 **Slovak** (sk)
- 🇸🇮 **Slovenian** (sl)
- 🇱🇹 **Lithuanian** (lt)
- 🇱🇻 **Latvian** (lv)
- 🇪🇪 **Estonian** (et)
- 🇲🇹 **Maltese** (mt)
- 🇮🇪 **Irish** (ga)
- 🏴󠁧󠁢󠁷󠁬󠁳󠁿 **Welsh** (cy)
- 🇮🇸 **Icelandic** (is)

#### Asian Languages
- 🇨🇳 **Chinese** (zh)
- 🇮🇳 **Hindi** (hi)
- 🇸🇦 **Arabic** (ar)
- 🇯🇵 **Japanese** (ja)
- 🇰🇷 **Korean** (ko)
- 🇻🇳 **Vietnamese** (vi)
- 🇹🇭 **Thai** (th)
- 🇮🇷 **Persian** (fa)
- 🇮🇱 **Hebrew** (he)
- 🇮🇩 **Indonesian** (id)
- 🇲🇾 **Malay** (ms)
- 🇵🇭 **Filipino** (fil)
- 🇧🇩 **Bengali** (bn)
- 🇵🇰 **Urdu** (ur)

#### African Languages
- 🇳🇬 **Yoruba** (yo)
- 🇬🇭 **Twi** (twi)
- 🇰🇪 **Swahili** (sw)
- 🇿🇦 **Afrikaans** (af)

**Total**: 47 languages explicitly listed, plus 50+ additional languages supported by Whisper

### How Transcription Works

1. **Automatic Language Detection**: By default, Whisper automatically detects the spoken language
2. **Manual Language Selection**: You can manually select a language in Settings > Transcription > Language
3. **Multi-Language Support**: Whisper can handle code-switching (multiple languages in one session)

## Translation Support (MarianMT)

OpenLiveCaption uses Helsinki-NLP's MarianMT models for translation from English to other languages.

### Supported Languages for Translation

All of the following languages support translation **from English**:

#### European Languages
- 🇪🇸 **Spanish** (es) ✅
- 🇫🇷 **French** (fr) ✅
- 🇩🇪 **German** (de) ✅
- 🇵🇹 **Portuguese** (pt) ✅
- 🇷🇺 **Russian** (ru) ✅
- 🇮🇹 **Italian** (it) ✅
- 🇳🇱 **Dutch** (nl) ✅
- 🇵🇱 **Polish** (pl) ✅
- 🇹🇷 **Turkish** (tr) ✅
- 🇺🇦 **Ukrainian** (uk) ✅
- 🇬🇷 **Greek** (el) ✅
- 🇸🇪 **Swedish** (sv) ✅
- 🇩🇰 **Danish** (da) ✅
- 🇫🇮 **Finnish** (fi) ✅
- 🇳🇴 **Norwegian** (no) ✅
- 🇨🇿 **Czech** (cs) ✅
- 🇭🇺 **Hungarian** (hu) ✅
- 🇷🇴 **Romanian** (ro) ✅
- 🇧🇬 **Bulgarian** (bg) ✅
- 🇷🇸 **Serbian** (sr) ✅
- 🇭🇷 **Croatian** (hr) ✅
- 🇸🇰 **Slovak** (sk) ✅
- 🇸🇮 **Slovenian** (sl) ✅
- 🇱🇹 **Lithuanian** (lt) ✅
- 🇱🇻 **Latvian** (lv) ✅
- 🇪🇪 **Estonian** (et) ✅
- 🇲🇹 **Maltese** (mt) ✅
- 🇮🇪 **Irish** (ga) ✅
- 🏴󠁧󠁢󠁷󠁬󠁳󠁿 **Welsh** (cy) ✅
- 🇮🇸 **Icelandic** (is) ✅

#### Asian Languages
- 🇨🇳 **Chinese** (zh) ✅
- 🇮🇳 **Hindi** (hi) ✅
- 🇸🇦 **Arabic** (ar) ✅
- 🇯🇵 **Japanese** (ja) ✅
- 🇰🇷 **Korean** (ko) ✅
- 🇻🇳 **Vietnamese** (vi) ✅
- 🇹🇭 **Thai** (th) ✅
- 🇮🇷 **Persian** (fa) ✅
- 🇮🇱 **Hebrew** (he) ✅
- 🇮🇩 **Indonesian** (id) ✅
- 🇲🇾 **Malay** (ms) ✅
- 🇵🇭 **Filipino** (fil) ✅
- 🇧🇩 **Bengali** (bn) ✅
- 🇵🇰 **Urdu** (ur) ✅

#### African Languages
- 🇳🇬 **Yoruba** (yo) ✅
- 🇬🇭 **Twi** (twi) ✅
- 🇰🇪 **Swahili** (sw) ✅
- 🇿🇦 **Afrikaans** (af) ✅

**Total**: 47 languages supported for translation

### How Translation Works

1. **Enable Translation**: Go to Settings > Transcription > Enable Translation
2. **Select Target Language**: Choose your target language from the dropdown
3. **Dual-Language Display**: Optionally display both original and translated text
4. **Model Caching**: Translation models are downloaded once and cached for future use

### Translation Notes

- **Source Language**: Translation currently supports English as the source language
- **First Use**: The first time you use a language, the translation model will be downloaded (~300MB per language)
- **Offline Use**: After downloading, translation works offline
- **Quality**: Translation quality varies by language pair; European languages generally have higher quality

## Using Languages in OpenLiveCaption

### Transcription Language Selection

#### Auto-Detect (Recommended)
1. Open Settings > Transcription
2. Set Language to "Auto-detect"
3. Whisper will automatically detect the spoken language

#### Manual Selection
1. Open Settings > Transcription
2. Select your language from the Language dropdown
3. Whisper will transcribe in that language only

### Translation Setup

1. **Enable Translation**:
   - Open Settings > Transcription
   - Check "Enable Translation"

2. **Select Target Language**:
   - Choose your target language from the "Target Language" dropdown
   - Model will download on first use (1-2 minutes)

3. **Dual-Language Display** (Optional):
   - Check "Show both original and translated text"
   - Both texts will appear in the overlay

### Example Workflows

#### Transcribe Spanish Audio
1. Set Language to "Spanish (es)" or "Auto-detect"
2. Start captions
3. Spanish speech will be transcribed in Spanish

#### Transcribe English and Translate to French
1. Set Language to "English (en)" or "Auto-detect"
2. Enable Translation
3. Set Target Language to "French (fr)"
4. Start captions
5. English speech will be transcribed and translated to French

#### Transcribe Any Language (Auto-Detect)
1. Set Language to "Auto-detect"
2. Start captions
3. Whisper will detect and transcribe in the spoken language

## Language Model Information

### Whisper Models
- **Provider**: OpenAI
- **Type**: Multilingual speech recognition
- **Languages**: 99+
- **Model Sizes**: tiny (75MB), base (150MB), small (500MB), medium (1.5GB), large (3GB)
- **Accuracy**: Larger models = better accuracy

### MarianMT Models
- **Provider**: Helsinki-NLP (Hugging Face)
- **Type**: Neural machine translation
- **Languages**: 47 (English to target)
- **Model Size**: ~300MB per language
- **Quality**: High quality for European languages, good for Asian languages

## Performance Considerations

### Transcription Performance
- **Tiny model**: Fastest, good for real-time use
- **Base model**: Fast, better accuracy
- **Small/Medium/Large**: Slower, best accuracy

### Translation Performance
- **First use**: 1-2 minutes to download model
- **Subsequent use**: < 1 second per caption
- **Memory**: ~500MB per loaded translation model

## Troubleshooting

### Language Not Detected Correctly
- Try manually selecting the language in Settings
- Use a larger Whisper model (base or small)
- Ensure audio quality is good (reduce background noise)

### Translation Not Working
- Check internet connection (required for first-time model download)
- Ensure sufficient disk space (~300MB per language)
- Check console for error messages
- Try a different target language

### Poor Translation Quality
- Translation quality depends on the language pair
- Some languages have better models than others
- Consider using a different translation service for critical applications

## Future Language Support

We plan to add support for:
- More African languages
- More Asian languages
- Bidirectional translation (not just English to target)
- Custom translation models
- Offline translation model bundles

## Contributing

If you'd like to help improve language support:
1. Report translation quality issues on GitHub
2. Suggest additional languages to support
3. Contribute translation model configurations
4. Help test languages you speak

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

**Last Updated**: February 10, 2026  
**Version**: 2.0.0

