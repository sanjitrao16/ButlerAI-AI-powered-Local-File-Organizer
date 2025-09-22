import os
import shutil
import time

from utils.file_renaming import (
  rename_files
)

def organize_directory(path,folder_obj,video_files,audio_files,mode):
  print(f"[Butler AI] Started to make changes in directory {path}")
  start = time.time()

  # Renaming files based on the generated suggestions
  if mode == 1:
    folder_obj = rename_files(path,folder_obj)
    print("[Butler AI] Files are successfully renamed into the the generated names")

  # # Organizing Video Files into a generic "Videos" folder
  organize_video_files(path,video_files)

  # # Organizing Audio Files into a generic "Audios" folder
  organize_audio_files(path,audio_files)

  # # Organizing the renamed file into the generated folder suggestions
  if mode == 1:
    organize_gen_files(path,folder_obj)
  elif mode == 2:
    organize_by_file(path,folder_obj)

  end = time.time()

  print("[Butler AI] Files are successfully organized into the designated folders")
  print(f"[Butler AI Time Stats] Total time taken to organize the directory: {end-start:.2f} seconds")

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

def organize_audio_files(path,audio_files):
  if audio_files == []:
    return
  
  # Creating folder "Audios" in the root directory
  dest_dir = "Audios"
  dest_path = os.path.join(path,dest_dir)
  if not os.path.exists(dest_dir):
    os.mkdir(dest_path)

  # Moving files from the root directory to the newly created folder
  for audio_file in audio_files:
    try:
      shutil.move(audio_file,dest_path)
    except FileNotFoundError:
      print(f"[Butler AI] File {audio_file} not found.")
    except Exception as e:
      print(f"[Butler AI] Error occured, {e}")


def organize_gen_files(path,folder_obj):
  # Organzing files from the generated folder structure
  folders = folder_obj["folders"]
  for folder in folders:
    dest_dir = folder["folder_name"]
    dest_path = os.path.join(path,dest_dir)
    if not os.path.exists(dest_dir):
      os.mkdir(dest_path)
    
    # Moving the files suggested in that folder to the created folder
    files = folder["files"]
    for file in files:
      try:
        file_path = file["renamed_file_path"]
        shutil.move(file_path,dest_path)
      except FileNotFoundError:
        print(f"[Butler AI] File {file_path} not found.")
      except Exception as e:
        print(f"[Butler AI] Error occured, {e}")

def organize_by_file(path,folder_obj):
  # Organzing files by file type
  folders = folder_obj["folders"]
  for folder in folders:
    dest_dir = folder["folder_name"]
    dest_path = os.path.join(path,dest_dir)
    if not os.path.exists(dest_dir):
      os.mkdir(dest_path)
    
    # Moving the files suggested in that folder to the created folder
    files = folder["files"]
    for file in files:
      try:
        file_path = file["original_file_name"]
        shutil.move(file_path,dest_path)
      except FileNotFoundError:
        print(f"[Butler AI] File {file_path} not found.")
      except Exception as e:
        print(f"[Butler AI] Error occured, {e}")