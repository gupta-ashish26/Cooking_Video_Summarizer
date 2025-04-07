# transcription_utils.py
import subprocess
import json
import os

def transcribe_audio(audio_file: str, output_dir: str, model: str = 'medium'):
    subprocess.run([
        'whisper',
        audio_file,
        '--language', 'en',
        '--output_format', 'json',
        '--model', model,
        '--output_dir', output_dir
    ])

def load_transcription(transcription_path: str) -> dict:
    with open(transcription_path, 'r') as f:
        return json.load(f)

def find_keyword_segments(transcription: dict, keyword_set: set) -> list:
    matches = []
    for segment in transcription.get('segments', []):
        if any(word in segment['text'].lower() for word in keyword_set):
            matches.append({
                'start': segment['start'],
                'end': segment['end'],
                'text': segment['text']
            })
    return matches
