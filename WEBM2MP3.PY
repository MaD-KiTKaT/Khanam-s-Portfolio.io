###CREATE WEBM TO MP3!!!###

import os
import subprocess

# Path to the folder containing .webm files
input_folder = r"C:\Users\Khanam\mp3_downloads"  # <-- change this
output_folder = os.path.join(input_folder, "mp3_output")

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Loop through all files in the folder
for filename in os.listdir(input_folder):
    if filename.endswith(".webm"):
        webm_path = os.path.join(input_folder, filename)
        mp3_filename = os.path.splitext(filename)[0] + ".mp3"
        mp3_path = os.path.join(output_folder, mp3_filename)

        # Run FFmpeg command to convert to mp3
        command = ["ffmpeg", "-i", webm_path, "-vn", "-ab", "192k", "-ar", "44100", "-y", mp3_path]
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        

        print(f"Converted: {filename} -> {mp3_filename}")

print("Conversion complete!")

