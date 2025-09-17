import sys,os
import threading
import ollama
import time

from utils.file_utils import (
  display_directory_tree,
  exclude_hidden_files,
  separate_files_by_type,
  process_text_files,
  display_suggested_dir_tree
)

from data_generation.text_file_data_generation import (
  feed_text_files_data
)

from image_file_categorization import (
  categorize_image_files
)

from data_generation.image_file_data_generation import (
  feed_image_files_data
)

from data_generation.folder_generation import (
  generate_folder_json
)

from organization import (
  organize_directory
)

local_client = ollama.Client(host="http://localhost:11434")
model_ready = False
model_failed = False


def initialize_model():
  start = time.time()
  global model_ready,model_failed
  local_model = "gemma3:4b"

  try:
    model_info = local_client.show(model=local_model)
    model_ready = True
    end = time.time()
    print("\n[Butler AI] Ollama model initialized successfully...")
    print(f"\n[Butler AI Time Stats] Time taken to initialize model: {end-start:.2f} seconds")
  except Exception as e:
    end = time.time()
    print(f"\n[Butler AI] Failed to initialize model : {e}")
    model_failed = True

def isQuit(user_input):
  if user_input.lower() == 'q':
    print("Exiting application...")
    return True
  return False

def get_mode():
  ''' User enters a mode '''
  while True:
    print("\n\tSelect the mode in which you want your directory to be organized:\t\n")
    print("1. Rename and Organize by Content (Type 1).")
    print("2. Organize by File Type (Type 2).")
    print("3. Organize by Date (Type 3).")
    
    mode = int(input("Enter an option: "))

    if (mode == 1):
      print("[Butler AI] Mode of directory organization: Rename and Organize by Content")
      return mode
    elif (mode == 2):
      print("[Butler AI] Mode of directory organization: By File Type")
      return mode
    elif (mode == 3):
      print("[Butler AI] Mode of directory organization: By Date")
      return mode
    else:
      print("Enter a valid mode option.")

def interpret_response(text):
  '''Parse Yes/No response '''
  while True:
    response = input(text)
    response = response.strip().lower()
    if response in ('yes','y'):
      return True
    elif response in ('no','n'):
      return False
    else:
      print("Enter either yes or no")

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
  
  while True:
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
    
    1. Rename and Organize by Content
    2. Organize by file type
    3. Organize by date
  
    '''
    while True:
      mode = get_mode()

      if (mode == 1): # Rename and Organize
        if not model_ready:
          print("[Butler AI] Models not initialized, initializing it...")
          initialize_model()
  
        # Separating files by types (video, audio, image, text)
        video_files, audio_files, image_files, text_files = separate_files_by_type(visible_files)
    
        # Processing text files
        start = time.time()
        text_files_content = process_text_files(text_files,workers=4)
        end = time.time()
    
        print("[Butler AI] Text file content are extracted and ready to be fed to the model")
        print(f"[Butler AI Time Stats] Time Taken to read and extract file contents: {end-start:.2f} seconds")
    
        # Feeding the extracted content into the Gemma3:4b model and get appropriate file descriptions and file name.
        start = time.time()
        text_files_data = feed_text_files_data(text_files_content,local_client)
        end = time.time()

        print("[Butler AI] Generated text file attributes")
        print(f"[Butler AI Time Stats] Total Time Taken to generate file attributes: {end-start:.2f} seconds")

        # Categorizing image files on how text-heavy it is
        start = time.time()
        image_files_category = categorize_image_files(image_files)
        end = time.time()

        print("[Butler AI] Categorized image files into relevant categories")
        print(f"[Butler AI Time Stats] Total Time Taken to categorize image files: {end-start:.2f} seconds")

        # Feeding the categorized image files into the Gemma3:4b model to get appropriate image captions and file names
        start = time.time()
        image_files_data = feed_image_files_data(image_files_category,local_client)
        end = time.time()

        print("[Butler AI] Generated image file attributes")
        print(f"[Butler AI Time Stats] Total Time Taken to generate file attributes: {end-start:.2f} seconds")
        print()

        # Storing the generated file names in a list
        file_names = []
        for text_file in text_files_data:
          file_names.append([text_file["generated_file_name"],text_file["original_file_name"]])
        for image_file in image_files_data:
          file_names.append([image_file["generated_file_name"],image_file["original_file_name"]])
        
        # Generating folder names and returning as JSON
        folder_object = generate_folder_json(file_names,local_client)

        print("\n")
        print("+==================================+")
        print("|  Suggested Directory Structure   |")
        print("+==================================+")
        print("\n")

        # Suggested Directory Structure
        print(os.path.abspath(directory_path))
        display_suggested_dir_tree(directory_path,folder_object,video_files,audio_files)

      # Ask user if performed changes are as expected
      accept_changes = interpret_response("Are you satisfied with the mentioned changes? (Yes/No): ")

      if accept_changes:
        print("[Butler AI] User has accepted changes...Proceeding to apply..")

        organize_directory(
          directory_path,folder_object,video_files,audio_files
        )

        break # Exit mode loop
      else:
        # Ask user if the directory has to be reorganized
        reorganize = interpret_response("Do you want to reorganize the directory better? (Yes/No):  ")
        if reorganize:
          continue # Again ask the choice of organization
        else:
          print("[Butler AI] User not satisfied with organization..terminating application..")
          break # Exit mode loop
    
    # Ask user if another directory has to be organized
    dir_path = interpret_response("Do you want to organize another directory (Yes/No): ")
    if not dir_path:
      break # Exit main loop


if __name__ == "__main__":
  print("Starting the application...")
  
  # Initializing Gemma 3 model.
  model_init_thread = threading.Thread(target=initialize_model,daemon=True)
  model_init_thread.start()

  # Starting the app.
  start()