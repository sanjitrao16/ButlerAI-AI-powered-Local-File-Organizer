import os
import shutil
import time
import ollama
import re
from pathlib import Path

def generate_file_description(text,local_client):
  file_desc_prompt = f'''You are tasked to provide a clear and concise description of the file's content, use plain
  english focusing on the key details and main parts and do not invent new details which are not present. Limit the description
  to a maximum of 100 words.
  
  Text Content: {text}

  Description:'''

  start = time.time()
  response = local_client.chat(
    model= "gemma3:4b",
    messages= [
      {"role": "user","content": file_desc_prompt}
    ]
  )

  end = time.time()
  description = response['message']['content'].strip()
  print()
  print("---------------------------------")
  print(f"\t{description}\t")
  print("---------------------------------")
  print()
  print(f"[Butler AI Time Stats] Time taken to generate file description: {end-start:.2f} seconds")

  return description

def generate_text_file_name(file,file_description,local_client):
  file_name_prompt = f'''You are tasked to provide a short and clear file name based on the file description provided, use plain
  english and the file name should capture the file's essence and clearly convey the topic it contains. Avoid special characters, limit
  the filename to a maximum of 3 words, connect words with underscores and do not include file extensions.
  Each word of the file name should have the starting letter capitalized. Descriptions which contain year or month as a pivotal factor or keywords like "textbook", "research", "draft", "report", "article" should be included in the filename.
  
  File Description: {file_description}

  Output only the filename without any additional text.

  Examples:
  
  1. File Description: Meeting notes from the quarterly strategy review.
     Filename: Quarterly_Meeting_Notes

  2. File Description: Presentation on upcoming marketing campaign ideas
     Filename: Marketing_Campaign_Ideas

  File Name:'''

  start = time.time()
  response = local_client.chat(
    model= "gemma3:4b",
    messages= [
      {"role": "user","content": file_name_prompt}
    ]
  )

  end = time.time()
  filename = response['message']['content'].strip()
  print()
  print("---------------------------------")
  print(f"\tOriginal Filename: {file}\t Suggested Filename: {filename}\t")
  print("---------------------------------")
  print()
  print(f"[Butler AI Time Stats] Time taken to generate file name: {end-start:.2f} seconds")

  return filename

def generate_text_folder_name(file_name,extension,local_client):
  foldername_prompt = f'''You are tasked to generate a general category or theme that best represents the main subject of this document based on the filename provided. This is will be used as a folder name. Since it is being used a folder name, suggest names which serves as a more general categorization of the file which can also further be used for other related files. Limit the category name to a maximum of 2 words. Use nouns and avoid verbs. Do not include specific details, words from the filename or any generic terms.
  
  The first letter of the word should be capitalized and use underscores to group words.

  File Name: {file_name}

  Optionally the file extension is also provided, just for reference and letting you know what type of file you are dealing with.

  File Extension: {extension}

  Examples:
  
  1. File Description: Meeting notes from the quarterly strategy review.
     Category name: Business_Meetings

  2. File Description: Presentation on upcoming marketing campaign ideas
     Category name: Marketing
  
  Output only the category and nothing else.

  Category:'''

  start = time.time()
  response = local_client.chat(
    model= "gemma3:4b",
    messages= [
      {"role": "user","content": foldername_prompt}
    ]
  )

  end = time.time()
  foldername = response['message']['content'].strip()
  print()
  print("---------------------------------")
  print(f"Suggested Folder Name: {foldername}")
  print("---------------------------------")
  print()
  print(f"[Butler AI Time Stats] Time taken to generate folder name: {end-start:.2f} seconds")

  return foldername

def generate_text_file_attributes(file,text,local_client):
  ''' Generating file attributes like file name and file description'''

  ''' The file attributes generation is done as follows:
  
  1. A short 100 word file description is given from the extracted file content
  2. From the generated description, a file name is suggested (maximum of 3 words).
  
  '''

  # Generating file description
  description = generate_file_description(text,local_client)

  # Generating file name
  file_name = generate_text_file_name(file,description,local_client)

  # Generating folder name
  file_path = Path(file)
  extension = file_path.suffix
  folder_name = generate_text_folder_name(file_name,extension,local_client)

  generated_attributes = {
    "original_file_name": file,
    "generated_description": description,
    "generated_file_name": file_name,
    "generated_folder_name": folder_name
  }

  return generated_attributes



def feed_text_files_data(text_files,local_client):
  ''' Feeding extracted text content data to the model '''
  # Feeding data sequentially
  results = []
  for text_file,content in text_files.items():
    data = generate_text_file_attributes(text_file,content,local_client)
    results.append(data)
  return results