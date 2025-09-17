import os
import shutil
import time

from utils.file_renaming import (
  rename_files
)

def organize_directory(path,folder_obj,video_files,audio_files):
  print(f"[Butler AI] Started to make changes in directory {path}")
  start = time.time()

  # Renaming files based on the generated suggestions
  rename_files(path,folder_obj)

  # Organizing Video Files into a generic "Videos" folder
  organize_video_files(path,video_files)

  end = time.time()

def organize_video_files(path,video_files):
  if video_files == []:
    return
  
  # Creating folder "Videos" in the root directory
  dest_dir = "Videos"
  dest_path = os.path.join(path,dest_dir)
  if not os.path.exists(dest_dir):
    os.mkdir(dest_path)

  # Moving files from the root directory to the newly created folder
  for video_file in video_files:
    try:
      shutil.move(video_file,dest_path)
    except FileNotFoundError:
      print(f"[Butler AI] File {video_file} not found.")
    except Exception as e:
      print(f"[Butler AI] Error occured, {e}")