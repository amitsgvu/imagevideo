import shutil
import sys

# Check for ffmpeg availability
ffmpeg_path = shutil.which("ffmpeg")
if ffmpeg_path is None:
    sys.exit("❌ ffmpeg not found in system path.")

# Now use ffmpeg_path instead of plain 'ffmpeg' in subprocess
subprocess.call([
    ffmpeg_path, "-y",
    "-loop", "1", "-i", image_path,
    "-i", audio_path,
    "-c:v", "libx264", "-t", str(duration),
    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
    "-shortest", video_path
])
