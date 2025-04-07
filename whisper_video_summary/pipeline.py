import os
from pathlib import Path
from whisper_video_summary.keywords import KEYWORDS
from whisper_video_summary.transcription_utils import transcribe_audio, load_transcription, find_keyword_segments
from whisper_video_summary.video_utils import extract_audio, extract_video_segment, combine_segments

def run_pipeline(video_path):
    os.makedirs('output', exist_ok=True)

    input_video = Path(video_path)
    base_name = input_video.stem  # e.g., 'biryani' from 'biryani.mp4'

    audio_file = f'output/{base_name}_audio.wav'
    transcription_file = f'output/{base_name}_audio.json'
    final_video = f'output/output_video.mp4'  # You may also make this dynamic if needed

    # ✅ Optional: update progress
    with open("status.json", "w") as f:
        f.write('{"progress": 10, "message": "Extracting audio..."}\n')

    extract_audio(str(input_video), audio_file)

    with open("status.json", "w") as f:
        f.write('{"progress": 30, "message": "Transcribing..."}\n')

    transcribe_audio(audio_file, 'output')

    with open("status.json", "w") as f:
        f.write('{"progress": 50, "message": "Finding segments..."}\n')

    transcription = load_transcription(transcription_file)
    matched_segments = find_keyword_segments(transcription, KEYWORDS)

    segment_files = []
    for i, segment in enumerate(matched_segments):
        segment_path = f'output/{base_name}_segment_{i}.mp4'
        extract_video_segment(str(input_video), segment['start'], segment['end'], segment_path)
        segment_files.append(segment_path)

    with open("status.json", "w") as f:
        f.write('{"progress": 80, "message": "Combining segments..."}\n')

    combine_segments(segment_files, final_video)

    with open("status.json", "w") as f:
        f.write('{"progress": 100, "message": "Done!"}\n')

    print(f"✅ Process complete. Final video at: {final_video}")
