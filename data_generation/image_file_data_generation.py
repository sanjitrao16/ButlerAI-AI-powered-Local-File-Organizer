import os
import shutil
import time
import ollama
import re

def generate_foldername_ocr(filename,local_client):
  foldername_prompt = f'''You are tasked to generate a general category or theme that best represents the main subject of the image based on the file name provided. The generated category name will be used as a folder name. Since it is being used a folder name, suggest names which serves as a more general categorization of the file which can also further be used for other related files. Limit the category name to a maximum of 2 words. Use nouns and avoid verbs. Do not include specific details, words from the filename or any generic terms.
  
  The first letter of the word should be capitalized and use underscores to group words.

  File Name: {filename}

  Examples:
  
  1. Image Caption: A scanned document of an electricity bill
     Category name: Electricity_Bills

  2. Image Caption: A screenshot of a Machine Learning course certificate
     Category name: Certificates
  
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

def generate_image_filename_ocr(file,text,local_client):
  ''' Generating image file filename based on the extracted OCR text '''

  file_name_prompt = f'''You are tasked to provide a clear file name based on text extracted from the image via pytesseract and OCR. Parts of text might not be readable, may not be structured, sentenced or grammatically correct, but catch the overall and genereal essence and meaning of the given text and output a file name in plain english. The file name should also convey what the image was intended to convey.Avoid special characters, limit the filename to a maximum of 3 words, connect words with underscores and do not include file extensions. Each word of the file name should have the starting letter capitalized.

  Output only the filename and nothing else.
  
  Text Extracted: {text}

  Filename:'''

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

  foldername = generate_foldername_ocr(filename,local_client)

  generated_attributes = {
    "original_file_name": file,
    "generated_description": text,
    "generated_file_name": filename,
    "generated_folder_name": foldername
  }

  return generated_attributes

def generate_image_caption(file,local_client):
  ''' Generating image caption for the image '''

  caption_prompt = f'''You are tasked to provide a concise and clear caption based on the given input image file path. The caption should catch the overall essence and meaning of the image, focus on the main objects and important aspects of the picture and ignore the subtle and minute details present. The caption should a maximum of 100 words and use plain english.
  
  Do not invent new details which are not present in the image and output only the image caption nothing else.
  
  Image File Path: {file}
  
  Caption:'''

  start = time.time()
  response = local_client.chat(
    model= "gemma3:4b",
    messages= [
      {"role": "user","content": caption_prompt}
    ]
  )

  end = time.time()
  img_caption = response['message']['content'].strip()
  print()
  print("---------------------------------")
  print(f"Generated Image Caption: {img_caption}")
  print("---------------------------------")
  print()
  print(f"[Butler AI Time Stats] Time taken to generate image caption: {end-start:.2f} seconds")

  return img_caption

def generate_file_name(file,caption,local_client):
  ''' Generating file name based on the generated caption ''' 

  file_name_prompt = f'''You are tasked to provide a clear file name for the image caption given below. The file name should be in plain english, and should convey the general idea of what the caption is saying. Avoid special characters, limit the filename to a maximum of 3 words, connect words with underscores and do not include file extensions. Each word of the file name should have the starting letter capitalized.

  For captions which has the word "logo" or "icon" in it, try to analyse the company/organization/business name and return the file name as
  "businessname_logo" or "businessname_icon"

  Output only the filename and nothing else.

  Image Caption: {caption}
  
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

def generate_folder_name(filename,local_client):
  foldername_prompt = f'''You are tasked to generate a general and generic category name or theme that best represents the main subject of the image based on the file name provided. This is will be used as a folder name. Since it is being used a folder name, suggest names which serves as a more general categorization of the file which can also further be used for other related files. Limit the category name to a maximum of 2 words. Use nouns and avoid verbs. Do not include specific details, words from the filename or any generic terms.
  
  The first letter of the word should be capitalized and use underscores to group words.

  File Name: {filename}

  Examples:
  
  1. Image Caption: A scenic place with a mountain and lake in the foreground.
     Category name: Nature

  2. Image Caption: A group of people posing near the Eiffel Tower.
     Category name: Paris_Trip
  
  3. Image Caption: A family celebrating their child's birthday.
     Category name: Birthday_Photos
  
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

def generate_image_attributes(file,local_client):
  ''' Generating image file attributes like image caption, filename based on the input image file '''

  ''' The file attributes generation is done as follows:
  
  1. A short 75 word image caption is generated from the image content
  2. From the generated caption, a file name is suggested (maximum of 3 words).
  
  '''

  # Generating image caption
  caption = generate_image_caption(file,local_client)

  # Generating file name
  filename = generate_file_name(file,caption,local_client)

  # Generating folder name
  folder_name = generate_folder_name(filename,local_client)

  generated_attributes = {
    "original_file_name": file,
    "generated_description": caption,
    "generated_file_name": filename,
    "generated_folder_name": folder_name
  }

  return generated_attributes

  

def feed_image_files_data(image_files,local_client):
  ''' Feeding the categorized image data to Gemma3:4b model '''
  # Feeding data sequentially
  results = []
  for image_file in image_files:
    if image_file["category"] == 1: # OCR extracted image file
      data = generate_image_filename_ocr(image_file["image_file_path"],image_file["ocr_text"],local_client)
    else: # Normal image directly given to AI Model
      data = generate_image_attributes(image_file["image_file_path"],local_client)
    results.append(data)
  
  return results
