# video_utils.py
import subprocess

def extract_audio(input_video: str, output_audio: str):
    subprocess.run(['ffmpeg', '-i', input_video, '-q:a', '0', '-map', 'a', output_audio, '-y'])

def extract_video_segment(input_video: str, start_time: float, end_time: float, output_file: str):
    subprocess.run([
        'ffmpeg',
        '-i', input_video,
        '-ss', str(start_time),
        '-to', str(end_time),
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-y',
        output_file
    ])

def combine_segments(segment_files: list, output_file: str):
    with open('segments.txt', 'w') as f:
        for file in segment_files:
            f.write(f"file '{file}'\n")
    subprocess.run(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'segments.txt', '-c', 'copy', output_file])
