import sys,os
import threading
import ollama
from utils.file_utils import (display_directory_tree)

local_client = ollama.Client(host="http://localhost:11434")
model_ready = False
model_failed = False

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


def start():
  print('''+======================================+
|                                      |
|                                      |
|   Butler AI - Local File Organizer   |
|                                      |
|                                      |
+======================================+''')
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
  
  # Listing the files in the directory
  print('''+===========================================+
|  The files present in the directory are   |   
+===========================================+''')
  
  print(directory_path)
  display_directory_tree(directory_path)




if __name__ == "__main__":
  print("Starting the application...")
  
  # Initializing Gemma 3 model.
  model_init_thread = threading.Thread(target=initialize_model,daemon=True)
  model_init_thread.start()

  # Starting the app.
  start()