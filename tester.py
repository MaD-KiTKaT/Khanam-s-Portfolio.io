# Python
import subprocess

# Path to the application executable
app_path = r"C:\Users\Khanam\Downloads\inkscape-1.4.2_2025-05-13_f4327f4-x64.msi"

# Open the application
subprocess.Popen([app_path])

# Optional: add arguments if the application requires them
# subprocess.Popen([app_path, "example.txt"])
