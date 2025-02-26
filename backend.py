from flask import Flask, request, send_file
from pathlib import Path
from openai import OpenAI
import tempfile

app = Flask(__name__)
client = OpenAI(api_key="YOUR_API_KEY")  # Ensure your API key is kept secure

@app.route('/tts', methods=['POST'])
def tts():
    text = request.json.get('text')
    if not text:
        return {"error": "No text provided"}, 400
    
    # Generate TTS output
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        speech_file_path = Path(tmp.name)
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text,
        )
        response.stream_to_file(speech_file_path)
        
    # Return the file
    return send_file(str(speech_file_path), mimetype="audio/mpeg", as_attachment=False)

if __name__ == '__main__':
    app.run(port=5000)
