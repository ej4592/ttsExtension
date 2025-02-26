from flask import Flask, request, send_file
from flask_cors import CORS
from pathlib import Path
import tempfile
import openai

app = Flask(__name__)
CORS(app)

# Set your OpenAI API key (preferably load from an environment variable)
openai.api_key = "YOUR_OPENAI_API_KEY"


@app.route("/tts", methods=["POST"])
def tts():
    data = request.get_json()
    text = data.get("text")
    if not text:
        return {"error": "No text provided"}, 400

    # Create a temporary file for the TTS output
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        speech_file_path = Path(tmp.name)
        # Call the OpenAI TTS API (update parameters as needed)
        response = openai.Audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text,
        )
        response.stream_to_file(speech_file_path)

    return send_file(str(speech_file_path), mimetype="audio/mpeg")


if __name__ == "__main__":
    app.run(port=5000)
