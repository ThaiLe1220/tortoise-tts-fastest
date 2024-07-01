from flask import Flask, request, jsonify, send_from_directory
import time
import torchaudio
from tortoise.api import TextToSpeech
import os
import uuid
from queue import Queue
import threading

app = Flask(__name__)

# Ensure the output directory exists
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Load TextToSpeech models
tts = TextToSpeech()
tts_vi = TextToSpeech(lang="vi")

# Create a queue to handle requests
request_queue = Queue()


# Function to process requests in the queue
def process_queue():
    while True:
        tts_model, text, output_file, result_queue = request_queue.get()
        try:
            start_time = time.time()
            gen = tts_model.tts_with_preset(
                text, voice_samples=None, conditioning_latents=None, preset="ultra_fast"
            )
            torchaudio.save(output_file, gen.squeeze(0).cpu(), 24000)
            end_time = time.time()
            result_queue.put((output_file, end_time - start_time))
        finally:
            request_queue.task_done()


# Start a thread to process the queue
threading.Thread(target=process_queue, daemon=True).start()


@app.route("/generate_audio", methods=["POST"])
def generate_audio():
    data = request.json
    text = data.get("text")
    lang = data.get("lang")

    if not text or not lang:
        return jsonify({"error": "Please provide both text and lang"}), 400

    if lang == "vi":
        tts_model = tts_vi
    else:
        tts_model = tts

    session_id = str(uuid.uuid4())
    output_file = os.path.join(output_dir, f"{session_id}_generated.wav")

    result_queue = Queue()
    request_queue.put((tts_model, text, output_file, result_queue))

    # Wait for the result
    output_file, duration = result_queue.get()

    file_url = request.url_root + "download/" + os.path.basename(output_file)

    return jsonify(
        {
            "message": "Audio generated successfully",
            "file_url": file_url,
            "duration": duration,
        }
    )


@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    return send_from_directory(output_dir, filename)


if __name__ == "__main__":
    app.run(debug=True)
