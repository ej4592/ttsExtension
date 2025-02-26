from flask import Flask, request, send_file, jsonify
from flask_cors import CORS  # Import Flask-Cors
import tempfile
from TTS.api import TTS

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes

# Initialize the TTS model (adjust model name as needed)
tts = TTS(model_name="tts_models/en/ljspeech/fast_pitch", progress_bar=False, gpu=False)


@app.route("/tts", methods=["POST"])
def synthesize():
    data = request.get_json()
    text = data.get("text")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Create a temporary file for output audio
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        output_path = tmp.name

    # Run TTS inference (this should be near-real-time on your M2 with a light model)
    tts.tts_to_file(text=text, file_path=output_path)

    return send_file(output_path, mimetype="audio/wav", as_attachment=False)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
