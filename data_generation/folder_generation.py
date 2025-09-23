import ollama
import time
import os
import json

from utils.json_parsing import (
  cleaned_json_output,
  parse_json_output
)

def generate_folder_json(app_dir,filenames,local_client):
  ''' Folder generation prompt where the output is in raw JSON format '''

  foldername_prompt = f'''You are an intelligent file organizer. INPUT is a JSON object, which has one key **files** and whose value is a list, where each element is an object representing the file, the structure of the object is given below:
  - `"original_file_name"`: The original name and path of the file (do not change or modify).
  - `"generated_file_name"`: The AI-suggested file name (do not change).
  - `"id"`: File ID (do not change).

  TASK:
  Your task is to group these files into meaningful and logically named folders by analysing similarites, patterns and meaning based on the "generated_file_name" key. Limit the folder name to a maximum of 2 words, underscore separated, no punctuation, use nouns and avoid verbs. Group files into **as few folders** as possible and also retaining the semantic meaning of the folders. 
  
  **Do not always categorize files on the basis of the file extensions.**
  **Do not ignore any files, all the files present in the input should be categorized.**

  OUTPUT RULES (must be followed exactly):
  1. Return **only** a single valid JSON object as the output and no additional text or explanations.
  3. Do not include specific details, words from the filename or any generic terms.
  4. The first letter of the word should be capitalized and use underscores to group words.
  5. Output must strictly be in **valid JSON format only**, no explanations or text outside JSON.
  6. The JSON object has one key: **folders**, the value is a list(array) of folders where each element represents one folder.
  7. Each element of the **folders** is an object having two keys:
     - **folder_name** → A string, the name of the folder generated.
     - **files** → a list(array) of files that belong to the folder.
  8. Each element of the **files** array is an object having three keys:
     - **original_file_name** → A string, the original name and path of the file. The value should be exactly as it is given in the input, without modifications.
     - **generated_file_name** → A string, the generated name of the file. This name should be exactly as it is given in the input.
     - **id** → An integer, the unique file id which should be exactly as it is given in the input.
  
  Input files: {filenames}

  JSON Output:'''

  start = time.time()
  response = local_client.chat(
    model= "gemma3:4b",
    messages= [
      {"role": "user","content": foldername_prompt}
    ]
  )
  end = time.time()

  json_output = response["message"]["content"].strip()

  print(f"[Butler AI Time Stats] Time taken to generate the folder structure: {end-start:.2f} seconds")
  print("[Butler AI] File categorized and returned as a JSON object.")

  cleaned_output = cleaned_json_output(json_output) # cleaning the output

  parsed_response = parse_json_output(cleaned_output) # converting to JSON object

  folder_fname = "folder_structure.json"

  with open(os.path.join(app_dir,folder_fname),"w") as file:
    json.dump(parsed_response,file,indent=4)

  return parsed_response