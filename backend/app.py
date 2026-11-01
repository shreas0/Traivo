
from flask import Flask, request, jsonify
from flask_cors import CORS
import features.tts as tts
import model_router as mr

app = Flask(__name__)
CORS(app)

@app.route("/process", methods=["POST"])
def process_input():
    data = request.get_json()
    user_input = data.get("input", "")
    history = data.get("history", [])

    bot_response = mr.llm_reply(user_input, history)
    image_places = mr.analyze_image_request(user_input, bot_response, history)
    images = mr.place_images_for_response(image_places, history)
    return jsonify({"response": bot_response, "images": images})


@app.route("/save-audio", methods=["POST"])
def save_audio():
    audio = request.files["audio"]
    audio.save("features/recordings/audio.webm")
    return jsonify({"message": "Saved"})


@app.route("/get-text", methods=["GET"])
def send_text():
    text = tts.speechtotext()
    return jsonify({"text": text})


@app.route("/speak", methods=["POST"])

def speak():
    data = request.get_json()
    user_input = data.get("input", "")
    action = data.get("action", "speak")
    status = tts.texttospeech(user_input, action)

    return jsonify({"message": "Speech generated" , "status" : status})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
