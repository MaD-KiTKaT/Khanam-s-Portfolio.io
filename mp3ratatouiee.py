import os
import sys
import subprocess

# Path to local ffmpeg.exe (put ffmpeg.exe in the same folder as this script)
ffmpeg_path = os.path.join(os.path.dirname(sys.argv[0]), "ffmpeg.exe")

# Get the folder you dragged onto the script
if len(sys.argv) < 2:
    # If no folder was provided, exit silently
    sys.exit()

input_folder = sys.argv[1]

if not os.path.isdir(input_folder):
    sys.exit()

output_folder = os.path.join(input_folder, "mp3_RAT")
os.makedirs(output_folder, exist_ok=True)

# Windows: hide FFmpeg console window
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

# Loop through all .webm files and convert
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".webm"):
        webm_path = os.path.join(input_folder, filename)
        mp3_filename = os.path.splitext(filename)[0] + ".mp3"
        mp3_path = os.path.join(output_folder, mp3_filename)

        command = [ffmpeg_path, "-i", webm_path, "-vn", "-ab", "192k", "-ar", "44100", "-y", mp3_path]
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, startupinfo=startupinfo)

# Optional: silent popup when done (Windows)
try:
    import ctypes
    ctypes.windll.user32.MessageBoxW(0, "Conversion complete!", "WEBM → MP3", 0)
except:
    pass
