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



