import os
import shutil
import tkinter as tk
from tkinter import filedialog

class File:
    def __init__(self, name, content, path="", binary=False):
        self.name = name
        self.content = content
        self.path = path
        self.binany = binary

def exists(path):
    return os.path.exists(path)

def is_file(path):
    return os.path.isfile(path)

def is_dir(path):
    return os.path.isdir(path)

def create_dir(path):
    if not exists(path):
        os.makedirs(path)

def get_filename(path):
    return os.path.basename(path)

def ls_all(path):
    return os.listdir(path)

def ls_files(path):
    files = ls_all(path)
    files = [file for file in files if is_file(f'{path}/{file}')]
    return files

def ls_dirs(path):
    dirs = ls_all(path)
    dirs = [dir for dir in dirs if is_dir(f'{path}/{dir}')]
    return dirs

def get_file(path):
    if not (exists(path) and is_file(path)):
        return None

    binary = is_binary(path)
    
    method = 'rb' if binary else 'r'
    encoding = None if binary else 'utf-8'
    
    with open(path, method, encoding=encoding) as file:
        filename = get_filename(path)
        content = file.read()
        return File(filename, content, path, binary)

def get_files(path, extension=None):
    filenames = []
    for f in ls_files(path):
        if extension and f.endswith(extension):
            filenames.append(f)
    
    files = []
    for name in filenames:
        file = get_file(f'{path}/{name}')
        files.append(file)
    
    return files

def create_file(file, path=""):
    binary = is_binary(file.name)

    method = 'wb' if binary else 'w'
    encoding = None if binary else 'utf-8'

    if path:
        create_dir(path)

    path = join(path, file.name)

    with open(path, method, encoding=encoding) as new_file:
        new_file.write(file.content)
    

def delete_file(path):
    os.remove(path)

def delete_dir(path):
    shutil.rmtree(path)

def move_file(og_path, new_path):
    shutil.move(og_path, new_path)

def clear_dir(path):
    delete_dir(path)
    create_dir(path)

def select_path(extension="*.*", title="Select file"):
    root = tk.Tk()
    root.withdraw()

    if(extension != "*.*"):
        extension = f"*.{extension}"

    path = filedialog.askopenfilename(
        title=title,
        filetypes=[(title, extension)]
    )

    return path

def select_paths(extension="*.*", title="Select files"):
    root = tk.Tk()
    root.withdraw()

    if(extension != "*.*"):
        extension = f"*.{extension}"

    paths = filedialog.askopenfilenames(
        title=title,
        filetypes=[(title, extension)]
    )

    return paths

def select_file(extension="*.*", title="Select file"):
    path = select_path(extension, title)
    return get_file(path)

def select_files(extension="*.*", title="Select files"):
    paths = select_paths(extension, title)

    files = []

    for path in paths:
        file = get_file(path)
        files.append(file)

    return files

def is_binary(path):
    extension = get_extension(path)

    binary_extensions = {
        'exe', 'bin', 'jpg', 'jpeg', 'png', 'gif', 'bmp', 
        'zip', 'rar', '7z', 'tar', 'gz', 'iso', 'dll', 
        'so', 'mp3', 'mp4', 'avi', 'mkv', 'mov', 'flac',
        'wav', 'ogg', 'pdf', 'doc', 'docx', 'ppt', 'pptx', 
        'xls', 'xlsx', 'pfx'
    }
    return extension.lower() in binary_extensions

def get_extension(path):
    _, extension = os.path.splitext(path)
    return extension.lstrip('.')

def join(path, file_name):
    return os.path.join(path, file_name)