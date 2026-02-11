from flask import Flask, request, send_from_directory, jsonify, send_file
import os
import tempfile
import whisper
from transformers import MarianMTModel, MarianTokenizer
import zipfile
import io

app = Flask(__name__, static_folder="web")

# Load whisper model on CPU by default for predictable performance
model_name = os.environ.get("WHISPER_MODEL", "tiny")
print(f"Loading Whisper model '{model_name}' (this may take a moment)...")
model = whisper.load_model(model_name, device=os.environ.get("WHISPER_DEVICE", "cpu"))
print("Model loaded.")

# Simple translation helpers (lazy-loaded)
MODEL_MAP = {
    "yo": "Helsinki-NLP/opus-mt-en-yo",
    "twi": "Helsinki-NLP/opus-mt-en-tw",
}
_translation_models = {}
_translation_tokenizers = {}

def get_translation_model(lang_key):
    if lang_key in _translation_models:
        return _translation_tokenizers[lang_key], _translation_models[lang_key]
    model_name = MODEL_MAP.get(lang_key)
    if not model_name:
        raise ValueError(f"No translation model configured for '{lang_key}'")
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model_t = MarianMTModel.from_pretrained(model_name)
    _translation_tokenizers[lang_key] = tokenizer
    _translation_models[lang_key] = model_t
    return tokenizer, model_t

def translate_text(text, target_lang=None):
    if not text:
        return ""
    if not target_lang:
        return text
    try:
        tokenizer, model_t = get_translation_model(target_lang)
    except Exception:
        return text
    tokens = tokenizer(text, return_tensors="pt", padding=True)
    translated = model_t.generate(**tokens, max_length=512)
    return tokenizer.decode(translated[0], skip_special_tokens=True)


@app.route("/")
def index():
    return send_from_directory("web", "index.html")


@app.route("/download")
def download():
    """Serve the entire project as a ZIP file for download"""
    import zipfile
    import io
    from flask import send_file
    
    # Create ZIP in memory
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add all project files
        for root, dirs, files in os.walk('.'):
            # Skip certain directories
            if any(skip in root for skip in ['.git', '__pycache__', 'venv', '.kiro', 'node_modules']):
                continue
            for file in files:
                file_path = os.path.join(root, file)
                arcname = file_path.replace('.\\', '').replace('./', '')
                try:
                    zf.write(file_path, arcname)
                except Exception:
                    pass
    
    memory_file.seek(0)
    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name='OpenLiveCaption.zip'
    )


@app.route("/transcribe", methods=["POST"])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({"error": "no audio file uploaded"}), 400
    f = request.files['audio']
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    try:
        f.save(tmp.name)
        result = model.transcribe(tmp.name, fp16=False)
        text = result.get('text', '')
        # target language may be provided as form field 'target' or query string
        target = request.form.get('target') or request.args.get('target')
        translated = None
        if target:
            translated = translate_text(text, target_lang=target)
        resp = jsonify({"text": text, "translated": translated})
        resp.headers.add("Access-Control-Allow-Origin", "*")
        return resp
    finally:
        try:
            tmp.close()
            os.unlink(tmp.name)
        except Exception:
            pass


@app.after_request
def add_cors(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    return response


if __name__ == '__main__':
    # Listen on all interfaces so your phone can connect via local IP
    app.run(host='0.0.0.0', port=5000)
