import os
import time
import ollama

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
  print("\n---------------------------------")
  print(f"Generated File Description\t\n\n{description}\n")
  print(f"[Butler AI Time Stats] Time taken to generate file description: {end-start:.2f} seconds\n")

  return description

def generate_text_file_name(file,file_description,local_client):
  file_name_prompt = f'''You are tasked to provide a short and clear file name based on the file description provided, use plain
  english and the file name should capture the file's essence and clearly convey the topic it contains. Avoid special characters, limit the filename to a maximum of 3 words, connect words with underscores and do not include file extensions. Each word of the file name should have the starting letter capitalized. Descriptions which contain year or month as a pivotal factor or keywords like "textbook", "research", "draft", "report", "article" should be included in the filename.
  
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
  print("Generated File Name\t\n")
  print(f"Original Filename: {file}")
  print(f"Suggested Filename: {filename}\n")
  print(f"[Butler AI Time Stats] Time taken to generate file name: {end-start:.2f} seconds\n")
  print("---------------------------------\n")

  return filename

def generate_text_file_attributes(file,text,local_client):
  ''' Generating file attributes like file name and file description'''

  ''' The file attributes generation is done as follows:
  
  1. A short 100 word file description is given from the extracted file content
  2. From the generated description, a file name is suggested (maximum of 3 words).
  
  '''

  print(f"\t{file}")

  # Generating file description
  description = generate_file_description(text,local_client)

  # Generating file name
  file_name = generate_text_file_name(file,description,local_client)

  generated_attributes = {
    "original_file_name": file,
    "generated_description": description,
    "generated_file_name": file_name,
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