import os
from pathlib import Path

def rename_files(path,folder_obj):
  # Renaming files based on the data present in the JSON object
  folders = folder_obj["folders"]
  for folder in folders:
    files = folder["files"]
    for file in files:
      generated_name = file["generated_file_name"]
      original_name = file["original_file_name"]
      path_object = Path(original_name)
      file_ext = path_object.suffix # Getting the file extension

      renamed_file_name = generated_name+file_ext # Adding file extension to the generated name

      new_file_path = os.path.join(path,renamed_file_name)
      
      try:
        os.rename(original_name,new_file_path)
        # Updating file location
        file["renamed_file_path"] = new_file_path
      except FileNotFoundError:
        print(f"[Butler AI] File {original_name} not found.")
      except FileExistsError:
        print(f"[Butler AI] File with the name {renamed_file_name} already exists.")
      except Exception as e:
        print(f"[Butler AI] Error occurred, {e}")
      
  return folder_obj # Updated folder object
