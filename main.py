from crop_with_tkinter import create_screen_rectangle 
import os, glob, subprocess
from send2trash import send2trash

default_captures_folder = "G:/Videos/Captures"
os.chdir(default_captures_folder)

video_extensions = ['.mp4', '.avi', '.flv', '.mov', '.wmv', '.mkv']

list_of_files = [file for file in os.listdir(".") if os.path.splitext(file)[1] in video_extensions]
latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)

# Obtain video duration
probe = subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', latest_file])
duration = float(probe)
print("probe:", duration)

# Get screenshot 10% into the video
screenshot_time = duration * 0.10
screenshot_file = "temp_screenshot.png"
subprocess.call(['ffmpeg', '-t', str(duration), '-i', latest_file, '-vf', 'scale=1920:-1', '-frames:v', '1', screenshot_file])

result = create_screen_rectangle(screenshot_file)  # assuming you modified the function to accept an image file

output_file = os.path.splitext(latest_file)[0] + "_cropped.mp4"
output_gif = os.path.splitext(latest_file)[0] + "_cropped.gif"

subprocess.call(['ffmpeg', '-i', latest_file, '-vf', f"crop={result[2]}:{result[3]}:{result[0]}:{result[1]}", output_file])
subprocess.call(['ffmpeg', '-i', output_file, '-vf', 'fps=10,scale=320:-1:flags=lanczos,palettegen', '-y', 'palette.png'])
subprocess.call(['ffmpeg', '-i', output_file, '-i', 'palette.png', '-filter_complex', 'fps=10,scale=320:-1:flags=lanczos[x];[x][1:v]paletteuse', '-y', output_gif])


send2trash(latest_file)
send2trash(output_file)
os.remove(screenshot_file) 
os.remove("palette.png")
