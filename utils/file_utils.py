import os
import shutil
import sys
import re
import concurrent.futures

from file_processing import (
    process_txt_file,
    process_doc_file,
    process_pdf_file,
    process_ppt_file,
    process_spreadsheet_file
)

def extract_text_content(file_path):
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
    contents = sorted(os.listdir(dir_path))
    pointers = ['├── '] * (len(contents) - 1) + ['└── ']
    for pointer, name in zip(pointers, contents):
        path = os.path.join(dir_path, name)
        print(prefix + pointer + name)
        if os.path.isdir(path):
            extension = '│   ' if pointer == '├── ' else '    '
            display_directory_tree(path, prefix + extension)


def separate_files_by_type(dir_path):
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

    files = [
        os.path.join(dir_path,name) for name in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path,name))
    ]

    text_files = [file for file in files if os.path.splitext(file)[1].lower() in text_exts]
    image_files = [file for file in files if os.path.splitext(file)[1].lower() in image_exts]
    video_files = [file for file in files if os.path.splitext(file)[1].lower() in video_exts]
    audio_files = [file for file in files if os.path.splitext(file)[1].lower() in audio_exts]
    
    return video_files,audio_files,image_files,text_files

def process_text_files(text_files,workers=4):
    results = {}
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        for file_path,content in executor.map(extract_text_content,text_files):
            results[file_path] = content
    return results