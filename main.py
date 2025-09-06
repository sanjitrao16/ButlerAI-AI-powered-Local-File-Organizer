import sys,os
import threading
import ollama

from utils.file_utils import (
  display_directory_tree,
  exclude_hidden_files,
  separate_files_by_type,
  process_text_files
)

local_client = ollama.Client(host="http://localhost:11434")
model_ready = False
model_failed = False

rename_only = False
organize_only = False
rename_and_organize = False

def initialize_model():
  global model_ready,model_failed
  local_model = "gemma3:4b"

  try:
    model_info = local_client.show(model=local_model)
    model_ready = True
    print("\n[Butler AI] Ollama model initialized successfully...")
  except Exception as e:
    print(f"\n[Butler AI] Failed to initialize model : {e}")
    model_failed = True

def isQuit(user_input):
  if user_input.lower() == 'q':
    print("Exiting application...")
    return True
  return False

def display_available_modes():
  print("\n\tSelect one of the options in which you want your directory to be organized:\t\n")
  print("1. Rename each file (Type 1).")
  print("2. Organize files into folders (Type 2).")
  print("3. Rename files and organize into folders (Type 3).")

def get_and_set_mode():
  mode = int(input("Enter an option: "))

  if (mode == 1):
    rename_only = True
  elif (mode == 2):
    organize_only = True
  else:
    rename_and_organize = True

def start():
  print("+======================================+")
  print("|                                      |")
  print("|                                      |")
  print("|   Butler AI - Local File Organizer   |")
  print("|                                      |")
  print("|                                      |")
  print("+======================================+")


  userQuit = input("Press 'q' to quit the application or any other key to continue:")
  if (isQuit(userQuit)):
    return
  
  # Ensure model initialized successfully
  if model_failed:
    print("\n[Butler AI] Critical Error: Model initialization failed. Exiting...")
    sys.exit(1)
  elif not model_ready:
    print("\n[Butler AI] Waiting for model to finish initializing...")
    # Wait until success/failure
    while not (model_ready or model_failed):
      pass
      if model_failed:
        print("\n[Butler AI] Critical Error: Model initialization failed. Exiting...")
        sys.exit(1)
  
  # Getting directory path
  directory_path = input("Enter the path of the directory to organize: ")

  # Checking the existence of the given directory
  while (not os.path.isdir(directory_path)):
    print(f"The directory {directory_path} doesn't exist. Enter a valid directory path")
    directory_path = input("Enter a valid path of the directory to organzie: ")
  
  # Excluding hidden files from the directory list

  ''' Note: The below function, excludes the hidden file as per UNIX file naming convention that is file names
  which start with "."
  '''

  visible_files = exclude_hidden_files(directory_path)

  # Listing the files in the directory
  print("\n")
  print("+===========================================+")
  print("|  The files present in the directory are   |")
  print("+===========================================+")
  print("\n")
  
  print(os.path.abspath(directory_path))
  display_directory_tree(directory_path)

  '''
  User has three options
  1. To rename the files
  2. To only organize into folders
  3. To rename and organize
  
  '''

  display_available_modes()
  get_and_set_mode()
  
  # Separating files by types (video, audio, image, text)
  video_files, audio_files, image_files, text_files = separate_files_by_type(visible_files)

  # print("\nFiles sorted by types:\n")
  # print(f"Text Files: {text_files}\n")
  # print(f"Image Files: {image_files}\n")
  # print(f"Video Files: {video_files}\n")
  # print(f"Audio Files: {audio_files}\n")

  # Processing text files

  text_content = process_text_files(text_files,workers=4)

  # for f,snippet in text_content.items():
  #   print(f"\n--- {f} ---\n{snippet[:200]}...")


if __name__ == "__main__":
  print("Starting the application...")
  
  # Initializing Gemma 3 model.
  model_init_thread = threading.Thread(target=initialize_model,daemon=True)
  model_init_thread.start()

  # Starting the app.
  start()