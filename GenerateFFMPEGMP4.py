import subprocess
from youtubeExampleCompiled import FPS, RESOLUTION, AUDIO_FILE

# Replace these with your actual values
FPS = 30
RESOLUTION = (1920, 1080)
OUTPUT_VIDEO = 'output_video.mp4'
FRAME_DIRECTORY = './frames/'
AUDIO_FILE = 'C_major_scale_cut.wav'  # Change this to your audio file

# Run ffmpeg command
cmd = [
    'ffmpeg',
    '-y',
    '-r', str(FPS),
    '-f', 'image2',
    '-s', f'{RESOLUTION[0]}x{RESOLUTION[1]}',
    '-i', f'{FRAME_DIRECTORY}frame%d.png',
    '-i', AUDIO_FILE,  # Add this line to include the audio
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    OUTPUT_VIDEO
]

try:
    subprocess.run(cmd, check=True)
    print(f"Video successfully created: {OUTPUT_VIDEO}")
except subprocess.CalledProcessError as e:
    print(f"Error creating video: {e}")