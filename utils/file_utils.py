import os
import shutil
import sys

import os

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

    all_files = [
        os.path.normpath(os.path.join(root, f))
        for root, _, files in os.walk(dir_path)
        for f in files
    ]

    text_files = [file for file in all_files if os.path.splitext(file)[1].lower() in text_exts]
    image_files = [file for file in all_files if os.path.splitext(file)[1].lower() in image_exts]
    video_files = [file for file in all_files if os.path.splitext(file)[1].lower() in video_exts]
    audio_files = [file for file in all_files if os.path.splitext(file)[1].lower() in audio_exts]
    
    return video_files,audio_files,image_files,text_files