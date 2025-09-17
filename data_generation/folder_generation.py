import ollama
import time
import os
import json

def generate_folder_json(filenames,local_client):
  ''' Folder generation prompt where the output is in raw JSON format '''
  foldername_prompt = f'''You are an intelligent file organizer. You will be given a list of generated file names and their corresponding original file names. Your task is to group these files into meaningful and logical folders based on their content, context, or similarities.

  Instructions:
  1. Analyze the provided file names carefully.
  2. Group files into AS FEW FOLDERS as possible, while ensuring each folder is semantically consistent.
  3. Limit the folder name to a MAXIMUM OF 2 words and use nouns and avoid verbs.
  4. Do not include specific details, words from the filename or any generic terms.
  5. The first letter of the word should be capitalized and use underscores to group words.
  6. Output must strictly be in **valid JSON format only**, no explanations or text outside JSON.
  7. Each folder must have:
    - A **folder name** that is short, descriptive, and meaningful.
    - A list of **files**, where each file entry contains:
     - `"generated_name"` → the AI-generated filename
     - `"original_name"` → the original filename

  File Names List (Generated Name, Original Name): {filenames}

  1. The original file name shouldn't change and should remain the same even in the output.
  2. The output should include all the list elements which are present in the above given list.

  Output only the JSON Format without any additional text.

  JSON Output:'''

  start = time.time()
  response = local_client.chat(
    model= "gemma3:4b",
    messages= [
      {"role": "user","content": foldername_prompt}
    ]
  )
  end = time.time()

  print("JSON OUTPUT")
  json_output = response["message"]["content"].strip()
  print(json_output)

  print(f"[Butler AI Time Stats] Time taken to format the JSON Structure: {end-start:.2f} seconds")
  print("[Butler AI] Files categorized and JSON output is given.")

  cleaned_output = cleaned_json_output(json_output) # Cleaning the output

  parsed_response = parse_json_output(cleaned_output) # converting to JSON object

  return parsed_response

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