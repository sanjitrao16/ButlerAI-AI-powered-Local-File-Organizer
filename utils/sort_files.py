import os

def sort_text_files(text_files):
    doc_file_object = {
       "folder_name": "Documents",
    }

    pdf_file_object = {
       "folder_name": "PDFs",
    }

    ppt_file_object = {
       "folder_name": "Presentations",   
    }

    excel_file_object = {
       "folder_name": "Spreadsheets",
    }


    doc_files,pdf_files,ppt_files,excel_files = [],[],[],[]

    for text_file in text_files:
        ext = os.path.splitext(text_file)[1].lower()
        file_name = os.path.basename(text_file)
        file_object = {
           "original_file_name" : text_file,
           "generated_file_name": file_name,
        }
        try:
          if ext in [".txt",".md",".doc",".docx"]:
             doc_files.append(file_object)
          elif ext in [".ppt",".pptx"]:
             ppt_files.append(file_object)
          elif ext in [".pdf"]:
             pdf_files.append(file_object)
          elif ext in [".csv",".xls",".xlsx"]:
             excel_files.append(file_object)
        except Exception as e:
          print(f"[Butler AI] File type not supported {text_file}: {e}")
    
    doc_file_object["files"] = doc_files
    pdf_file_object["files"] = pdf_files
    ppt_file_object["files"] = ppt_files
    excel_file_object["files"] = excel_files

    return (doc_file_object,pdf_file_object,ppt_file_object,excel_file_object)

def sort_image_files(image_files):
    folder_object = {
        "folder_name": "Images",
    }
    files = []

    for image_file in image_files:
        file_name = os.path.basename(image_file)
        file_object = {
            "original_file_name": image_file,
            "generated_file_name": file_name,
        }
        files.append(file_object)
    
    folder_object["files"] = files

    return folder_object