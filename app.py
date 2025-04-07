# app.py
import os
import json
import threading
from flask import Flask, request, render_template, send_from_directory
from whisper_video_summary.pipeline import run_pipeline

app = Flask(__name__)
UPLOAD_FOLDER = 'input'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['video']
    if uploaded_file.filename != '':
        video_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(video_path)

        # Clear old status
        with open("status.json", "w") as f:
            json.dump({"progress": 0, "message": "Starting..."}, f)

        # Run pipeline in a background thread
        threading.Thread(target=run_pipeline, args=(video_path,)).start()

        return render_template("progress.html")  # Frontend progress page
    return "No file uploaded", 400

@app.route('/status')
def status():
    with open("status.json") as f:
        return json.load(f)

@app.route('/download')
def download():
    return send_from_directory('output', 'output_video.mp4', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
