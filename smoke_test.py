import os
import traceback
try:
    from gtts import gTTS
    from pydub import AudioSegment
    import whisper
    from transformers import MarianTokenizer, MarianMTModel
except Exception as e:
    print('Missing dependency:', e)
    raise

TTS_TEXT = "Hello world, this is a smoke test for transcription and translation."
MP3 = "test.mp3"
WAV = "test.wav"

try:
    print('Generating TTS...')
    tts = gTTS(TTS_TEXT, lang='en')
    tts.save(MP3)

    print('Converting to WAV (16kHz mono)...')
    audio = AudioSegment.from_file(MP3, format='mp3')
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export(WAV, format='wav')

    model_name = os.environ.get('WHISPER_MODEL', 'tiny')
    print(f"Loading Whisper model '{model_name}'...")
    model = whisper.load_model(model_name)

    print('Transcribing...')
    res = model.transcribe(WAV, fp16=False)
    text = res.get('text', '')
    print('Transcription:', repr(text))

    target = os.environ.get('TARGET_LANG', 'yo')
    MODEL_MAP = {
        'yo': 'Helsinki-NLP/opus-mt-en-yo',
        'twi': 'Helsinki-NLP/opus-mt-en-tw',
    }
    model_name = MODEL_MAP.get(target)
    if not model_name:
        print('No Marian model configured for target', target)
    else:
        print('Loading MarianMT model for', target)
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        trans_model = MarianMTModel.from_pretrained(model_name)
        toks = tokenizer(text, return_tensors='pt', padding=True)
        out = trans_model.generate(**toks)
        translation = tokenizer.decode(out[0], skip_special_tokens=True)
        print('Translation:', repr(translation))

    print('Smoke test completed successfully.')
except Exception:
    traceback.print_exc()
    raise
