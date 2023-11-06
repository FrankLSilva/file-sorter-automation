from os import listdir
from os.path import isfile, join
import os
import shutil
import dearpygui.dearpygui as dpg


folder_names = {
    "Audio": {'aif', 'cda', 'flac', 'm4a', 'mid', 'midi', 'mp3', 'mpa', 'ogg', 'wav', 'wma', 'aiff', 'au', 'aac'},
    "Compressed": {'7z', 'deb', 'pkg', 'rar', 'rpm', 'z', 'gz', 'bz2', 'xz', 'lz', 'iso'},
    "Code": {'js', 'jsp', 'html', 'ipynb', 'py', 'java', 'css', 'cpp', 'c', 'h', 'php', 'rb', 'json', 'xml', 'yml', 'md'},
    "Documents": {'ppt', 'pptx', 'pdf', 'doc', 'docx', 'txt', 'tex', 'rtf', 'odt', 'csv'},
    "Images": {'bmp', 'gif', 'ico', 'jpeg', 'jpg', 'png', 'jfif', 'svg', 'tif', 'tiff', 'webp', 'eps', 'raw', 'cr2'},
    "Programs": {'apk', 'exe', 'jar', 'msi', 'dmg', 'app', 'com', 'appimage', 'dll'},
    "Videos": {'3gp', 'avi', 'flv', 'h264', 'mkv', 'mov', 'mp4', 'mpg', 'mpeg', 'wmv', 'm4v', 'webm', 'vob', 'ts'},
    "Spreadsheets": {'xls', 'xlsx'},
    "Archives": {'zip', 'tar'},
    "Scripts": {'sh', 'bat', 'bash', 'ps1', 'vbs', 'php', 'rb', 'pl', 'pyc'},
    "Web": {'html', 'css', 'js', 'php', 'asp', 'jsp', 'xml', 'json', 'htm', 'xhtml', 'scss', 'less'},
    "Ebooks": {'epub', 'mobi', 'pdf'},
    "Design": {'psd', 'ai', 'indd', 'cdr', 'sketch', 'xd'},
    "Databases": {'sql', 'sqlite', 'mdb', 'accdb', 'db', 'dbf'}
}

while True:
    print("\n===== FILE SORTER AUTOMATION =====")
    print("Welcome to the File Sorter Automation tool!")
    print("Please select the folder you want to organize.")
    print("You don't need to use quotation marks in your response.")

    print("\nSorted categories and extensions:")
    print("--------------------------------------")
    for category, extensions in folder_names.items():
        print(f"{category}: {', '.join(extensions)}")

    print("\n! ! !  WARNINGS ! ! !")
    print("--------------------------------------")
    print("-> Be cautious when selecting the folder to run this script.")
    print("-> Running it on the wrong directory could impact your system's functionality.")
    print("-> This script also operates on hidden folders, so exercise extra care during usage.")
    print("-> Files with the same name in the destination folder will be automatically overwritten.")
    print("--------------------------------------")

    # ---------------------- DIRECTORY PATH
    directory_input = input('\nSelect your directory (e.g. C:/): \n')
    directory = f'{directory_input}'.upper()
    main_path = os.path.join(directory)

    # ---------------------- PRINT FOLDERS
    existing_folders = os.listdir(main_path)
    print("\nList of existing folders:\n")
    for folder in existing_folders:
        print(f'-> {folder}')

    # ---------------------- FOLDER PATH
    folder_input = input('\nSelect your folder (e.g. "Downloads"): \n')
    folder = folder_input
    folder_path = os.path.join(directory, folder)

    # ---------------------- GET ALL FILES
    files = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]

    # Create a dictionary to store organized files
    organized_files = {folder_name: [] for folder_name in folder_names}

    # ---------------------- CREATE FOLDERS
    for file in files:
        filename, file_extension = os.path.splitext(file)
        file_extension = file_extension[1:].lower()

        for folder_name, extensions in folder_names.items():
            if file_extension in extensions:
                target_folder = os.path.join(folder_path, folder_name)
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)

                # ---------------------- MOVE FILES / KEEP TRACK
                shutil.move(os.path.join(folder_path, file), os.path.join(target_folder, file))
                organized_files[folder_name].append(file)
                break

    # ---------------------- PRINT RESULT
    print("\nSorted Categories Result:")
    print("--------------------------------------")
    for folder_name, files in organized_files.items():
        if files:
            print(f"\n{folder_name}:")
            for file in files:
                print(f"-> {file}")
    print("\nFiles organized.")

    restart = input("Do you want to restart the program? (y/n): ").strip().lower()
    if restart != 'y':
        print("\n--------------------------------------")
        break

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()