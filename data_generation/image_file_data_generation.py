import os
import shutil
import time
import ollama
import re
import pytesseract
from PIL import Image, ExifTags
import concurrent.futures

def extract_metadata(image_file):
  img = Image.open(image_file)
  width, height = img.size
  info = {
    "width": width,
    "height": height,
    "aspect_ratio": round(width/height,2),
    "mode": img.mode,
    "format": img.format,
    "exif": {}
  }

  try:
    exif = {ExifTags.TAGS[k]: v for k, v in img._getexif().items()} if hasattr(img,"_getexif") else {}
    info["exif"] = exif
  except Exception as e:
    pass
  return img,info

def preprocess_for_ocr(img):
  gray = img.convert("L") # convert to grayscale
  bw = gray.point(lambda x: 0 if x < 140 else 255,"1") # binarization
  return bw


def ocr_analysis(img):
  preprocessed_img = preprocess_for_ocr(img)
  text = pytesseract.image_to_string(preprocessed_img)
  words = text.strip().split()
  return text.strip(), len(words)


def classify_image(image_file):
  ''' Image classification is done on the following parameters 
  
  1. Extract basic metadata like width, height, aspect_ratio and color channels
  2. Based on text density, image can be classified as screenshots/scanned images/receipts/notes etc.
  3. If there isn't enough text then image is classified as photo/landscape/potrait/poster etc.

  Category numbers
  Category "1" -> screenshots/document/receipts/notes/diagrams
  Category "2" -> photo/potrait/art/landscape/poster/logos/icons
  
  '''

  img,meta_data = extract_metadata(image_file)

  text,word_count = ocr_analysis(img)
  
  if word_count > 25:
    return (1,meta_data,text)
  else: 
    return (2,meta_data,None)

def categorize_image_files(image_files,workers=4):
  ''' Before feeding data directly to the model, we classify the image into the two categories

  1. A picture taken from camera, an art, poster, landscape, potrait, illustration, logo, icon etc.
  2. A screenshot, scanned document, receipts, diagrams, flowcharts, notes etc

  Based on the category, either the whole image is given as input to the model or the extracted text is sent to the model to
  generate appropriate output.
  '''
  categories = []
  with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
    results = executor.map(classify_image,image_files)
  
  for image_file,category in zip(image_files,results):
    category_list = {
      "image_file_path": image_file,
      "category": category[0],
      "meta_data": category[1],
      "ocr_text": category[2]
    }
    categories.append(category_list)
  return categories
