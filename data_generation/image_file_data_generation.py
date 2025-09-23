import os
import time
import ollama

def generate_image_filename_ocr(file,text,local_client):
  ''' Generating image file filename based on the extracted OCR text '''

  file_name_prompt = f'''You are tasked to provide a clear file name based on text extracted from the image via pytesseract and OCR. Parts of text might not be readable, may not be structured, sentenced or grammatically correct, but catch the overall and genereal essence and meaning of the given text and output a file name in plain english. The file name should also convey what the image was intended to convey. Avoid special characters, limit the filename to a maximum of 3 words, connect words with underscores and do not include file extensions. Each word of the file name should have the starting letter capitalized.

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

  print(f"\t{file}")

  print("\n---------------------------------")
  print(f"Generated Image Caption\t\n\nNO CAPTION GENERATED\n")
  print("Generated File Name\t\n")
  print(f"Original Filename: {file}")
  print(f"Suggested Filename: {filename}\n")

  print(f"[Butler AI Time Stats] Time taken to generate file name: {end-start:.2f} seconds\n")
  print("---------------------------------\n")

  generated_attributes = {
    "original_file_name": file,
    "generated_description": text,
    "generated_file_name": filename,
  }

  return generated_attributes

def generate_image_caption(file,text,local_client):
  ''' Generating image caption for the image '''

  caption_prompt = f'''You are tasked to provide a concise and clear caption based on the given input image file path. The caption should catch the overall essence and meaning of the image, focus on the main objects and important aspects of the picture and ignore the subtle and minute details present. The caption should a maximum of 100 words and use plain english.
  
  Do not invent new details which are not present in the image.
  Do not generate captions based on the file name present in the file path
  Analyse the image thoroughly and it doesn't matter if it takes time.
  Output only the image caption nothing else.

  Optionally, these are some of the texts which were extracted from the image using OCR, which can be helpful for better understanding the whole context of the image

  Text Extracted: {text}
  
  Caption:'''

  start = time.time()
  response = local_client.chat(
    model= "gemma3:4b",
    messages= [
      {"role": "user","content": caption_prompt,'images':[f"{file}"]}
    ]
  )

  end = time.time()
  img_caption = response['message']['content'].strip()

  print("\n---------------------------------")
  print(f"Generated Image Caption\t\n\n{img_caption}\n")

  print(f"[Butler AI Time Stats] Time taken to generate image caption: {end-start:.2f} seconds\n")

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

  print("Generated File Name\t\n")
  print(f"Original Filename: {file}")
  print(f"Suggested Filename: {filename}\n")

  print(f"[Butler AI Time Stats] Time taken to generate file name: {end-start:.2f} seconds\n")
  print("---------------------------------\n")
  
  return filename

def generate_image_attributes(file,text,local_client):
  ''' Generating image file attributes like image caption, filename based on the input image file '''

  ''' The file attributes generation is done as follows:
  
  1. A short 75 word image caption is generated from the image content
  2. From the generated caption, a file name is suggested (maximum of 3 words).
  
  '''

  print(f"\t{file}\n")

  # Generating image caption
  caption = generate_image_caption(file,text,local_client)

  # Generating file name
  filename = generate_file_name(file,caption,local_client)

  generated_attributes = {
    "original_file_name": file,
    "generated_description": caption,
    "generated_file_name": filename,
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
      data = generate_image_attributes(image_file["image_file_path"],image_file["ocr_text"],local_client)
    results.append(data)
  
  return results
