import json
import os
import time

def cleaned_json_output(json_output):
  # Clean the response and get only the JSON File
  try:
    start_index = json_output.find("{")
    end_index = json_output.rfind("}")+1
    cleaned_output = json_output[start_index:end_index]
  except Exception as e:
    print(f"[Butler AI] Could not find a valid JSON string, Error: {e}")
    cleaned_output = None
  
  return cleaned_output

def parse_json_output(json_output):
  # Converting the JSON string to JSON object
  if json_output:
    try:
      json_object = json.loads(json_output)
      print("[Butler AI] Successfully converted JSON Object.")
    except json.JSONDecodeError as e:
      print(f"[Butler AI] Failed to decode JSON, Error: {e}")
      json_object = None
    
    return json_object
  else:
    print("[Butler AI] No JSON structure found.")

def data_to_json(app_dir,text_files,image_files):
  file_data = {
     "files": []
  }

  id = 1
  for text_file in text_files:
    data = {key:text_file[key] for key in {"original_file_name","generated_file_name"} if key in text_file}
    data["id"] = id
    id +=1
    file_data["files"].append(data)
  for image_file in image_files:
    data = {key:image_file[key] for key in {"original_file_name","generated_file_name"} if key in image_file}
    data["id"] = id
    id +=1
    file_data["files"].append(data)
  
  data_fname = "data.json"
  
  with open(os.path.join(app_dir,data_fname),"w") as file:
     json.dump(file_data,file,indent=4)
     print("[Butler AI] Converted generated data into JSON format.")
     print()

  return file_data
  
def display_json(data,prefix=""):
    ''' Displaying the JSON data in directory tree format '''
    if "folders" in data and isinstance(data["folders"], list):
        folders = data["folders"]
        pointers = ['├── '] * (len(folders) - 1) + ['└── ']
        for i,folder in enumerate(folders): # Iterating over each of the suggested folder
            pointer = pointers[i]
            folder_name = folder.get("folder_name","Unknown Folder").strip()
            print(prefix+pointer+"."+folder_name+"/")

            files = folder.get("files",[]) # Getting individual files
            if files:
                extension = "|   " if pointer == "├── " else "    "
                file_pointers = ["├── "] * (len(files) - 1) + ["└── "]
                for j, file in enumerate(files):
                    file_pointer = file_pointers[j]
                    file_name = file.get("generated_file_name", "Unknown File")
                    print(prefix + extension + file_pointer + file_name)