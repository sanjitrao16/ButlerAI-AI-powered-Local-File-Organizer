import os
import shutil
import sys
import re
import concurrent.futures

from .file_processing import (
    process_txt_file,
    process_doc_file,
    process_pdf_file,
    process_ppt_file,
    process_spreadsheet_file
)

def extract_text_content(file_path):
    ''' Extracting file content for different types of files '''
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext in [".txt",".md"]:
            return (file_path, process_txt_file(file_path))
        elif ext in [".doc",".docx"]:
            return (file_path, process_doc_file(file_path))
        elif ext in [".ppt",".pptx"]:
            return (file_path, process_ppt_file(file_path))
        elif ext in [".pdf"]:
            return (file_path, process_pdf_file(file_path))
        elif ext in [".csv",".xls",".xlsx"]:
            return (file_path, process_spreadsheet_file(file_path))
    except Exception as e:
        print(f"[Butler AI] File type not supported {file_path}: {e}")


def display_directory_tree(dir_path, prefix=""):
    ''' Displaying the file directory in a directory-tree structure '''
    contents = sorted([f for f in os.listdir(dir_path) if not f.startswith(".")]) #Ignores hidden files (UNIX naming convention)
    pointers = ['├── '] * (len(contents) - 1) + ['└── ']
    for pointer, name in zip(pointers, contents):
        path = os.path.join(dir_path, name)
        print(prefix + pointer + name)
        if os.path.isdir(path):
            extension = '│   ' if pointer == '├── ' else '    '
            display_directory_tree(path, prefix + extension)


def separate_files_by_type(files):
    '''
    Text-File formats: .pdf, .docx, .pptx, .txt, .csv, .md, .xlsx
    Image-File formats: .jpg, .jpeg, .png, .webp, .gif
    Video-File formats: .mp4
    Audio-File formats: .mp3
    
    '''
    text_exts = (".csv",".doc",".docx",".md",".pdf",".ppt",".pptx",".txt",".xls",".xlsx")
    image_exts = (".gif",".jpeg",".jpg",".png",".webp")
    video_exts = (".mp4")
    audio_exts = (".mp3")

    text_files = [file for file in files if os.path.splitext(file)[1].lower() in text_exts]
    image_files = [file for file in files if os.path.splitext(file)[1].lower() in image_exts]
    video_files = [file for file in files if os.path.splitext(file)[1].lower() in video_exts]
    audio_files = [file for file in files if os.path.splitext(file)[1].lower() in audio_exts]
    
    return video_files,audio_files,image_files,text_files

def exclude_hidden_files(dir_path):
    ''' Excludes hidden files as per UNIX File Naming convention that is files starting with "." '''
    files = []
    for file in os.listdir(dir_path):
        if (os.path.isfile(os.path.join(dir_path,file)) and (not file.startswith("."))):
            files.append(os.path.abspath(os.path.join(dir_path,file)))
    return files

def process_text_files(text_files,workers=4):
    ''' Processing text files parallely through concurrent processes to save time '''
    results = {}
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        for file_path,content in executor.map(extract_text_content,text_files):
            results[file_path] = content
    return results

def display_suggested_dir_tree(existing_path,json_data):
    display_existing(existing_path)
    display_json(json_data)

def display_existing(path):
    if not os.path.exists(path):
        print(f"[Butler AI] The directory {path} does not exist.")
        return
    
    is_root = True
    
    for root,dirs,files in os.walk(path):
        if is_root:
            is_root = False
            for d in dirs:
                print(f"├── .{d}/")
            continue

        level = root.replace(path,'').count(os.sep)
        indent = '│   ' * (level - 1)
        for file in files:
            print(f"{indent}│   └── {file}")

def display_json(data,prefix=""):
    if "folders" in data and isinstance(data["folders"], list):
        folders = data["folders"]
        pointers = ['├── '] * (len(folders) - 1) + ['└── ']
        for i,folder in enumerate(folders):
            pointer = pointers[i]
            folder_name = folder.get("folder_name","Unknown Folder").strip()
            print(prefix+pointer+"."+folder_name,"/")

            files = folder.get("files",[])
            if files:
                extension = "|   " if pointer == "├── " else "    "
                file_pointers = ["├── "] * (len(files) - 1) + ["└── "]
                for j, file in enumerate(files):
                    file_pointer = file_pointers[j]
                    file_name = file.get("generated_name", "Unknown File")
                    print(prefix + extension + file_pointer + file_name)
        