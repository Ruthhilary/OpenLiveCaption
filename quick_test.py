import numpy as np
import soundfile as sf
import os
import traceback
print('Starting quick audio -> transcribe -> translate test')
try:
    # generate 1s 440Hz sine
    sr = 16000
    t = np.linspace(0, 1, int(sr), endpoint=False)
    x = 0.1 * np.sin(2 * np.pi * 440 * t).astype(np.float32)
    wav = 'quick_test.wav'
    sf.write(wav, x, sr)
    print('WAV written:', wav)

    import whisper
    model_name = os.environ.get('WHISPER_MODEL', 'tiny')
    print('Loading whisper model', model_name)
    model = whisper.load_model(model_name)
    print('Transcribing...')
    r = model.transcribe(wav, fp16=False)
    print('Transcription result:', r.get('text'))

    target = os.environ.get('TARGET_LANG', 'yo')
    MODEL_MAP = {
        'yo': 'Helsinki-NLP/opus-mt-en-yo',
        'twi': 'Helsinki-NLP/opus-mt-en-tw',
    }
    mname = MODEL_MAP.get(target)
    if mname:
        from transformers import MarianTokenizer, MarianMTModel
        print('Loading Marian model', mname)
        tok = MarianTokenizer.from_pretrained(mname)
        m = MarianMTModel.from_pretrained(mname)
        toks = tok(r.get('text',''), return_tensors='pt', padding=True)
        out = m.generate(**toks)
        tr = tok.decode(out[0], skip_special_tokens=True)
        print('Translation:', tr)
    else:
        print('No Marian model for target', target)

    print('Quick test completed')
except Exception:
    traceback.print_exc()
    raise
