import os
from os import listdir
from os.path import isfile, join, splitext
import shutil
import dearpygui.dearpygui as dpg

width = 790
height = 599
selected_file_path = ""
organized_info = ""
function_result = ""

class DataValues():
	result_list = ""

# ---------------------- FILE SORT FUNCTION
folder_names = {
        "Audio": {'aif', 'cda', 'flac', 'm4a', 'mid', 'midi', 'mp3', 'mpa', 'ogg', 'wav', 'wma', 'aiff', 'au', 'aac'},
        "Compressed": {'7z', 'deb', 'pkg', 'rar', 'rpm', 'z', 'gz', 'bz2', 'xz', 'lz', 'iso', 'zip', 'tar'},
        "Code": {'js', 'jsp', 'html', 'ipynb', 'py', 'java', 'css', 'cpp', 'c', 'h', 'php', 'rb', 'json', 'xml', 'yml', 'md'},
        "Documents": {'ppt', 'pptx', 'pdf', 'doc', 'docx', 'txt', 'tex', 'rtf', 'odt', 'csv'},
        "Images": {'bmp', 'gif', 'ico', 'jpeg', 'jpg', 'png', 'jfif', 'svg', 'tif', 'tiff', 'webp', 'eps', 'raw', 'cr2'},
        "Programs": {'apk', 'exe', 'jar', 'msi', 'dmg', 'app', 'com', 'appimage', 'dll'},
        "Videos": {'3gp', 'avi', 'flv', 'h264', 'mkv', 'mov', 'mp4', 'mpg', 'mpeg', 'wmv', 'm4v', 'webm', 'vob', 'ts'},
        "Spreadsheets": {'xls', 'xlsx'},
        "Fonts": {'otf', 'ttf', 'fnt', 'pfa', 'vfb', 'jfproj', 'vlw', 'woff', 'sfd', 'fon'},
        "Scripts": {'sh', 'bat', 'bash', 'ps1', 'vbs', 'php', 'rb', 'pl', 'pyc'},
        "Web": {'html', 'css', 'js', 'php', 'asp', 'jsp', 'xml', 'json', 'htm', 'xhtml', 'scss', 'less'},
        "Ebooks": {'epub', 'mobi', 'pdf'},
        "Design": {'psd', 'ai', 'indd', 'cdr', 'sketch', 'xd'},
        "Databases": {'sql', 'sqlite', 'mdb', 'accdb', 'db', 'dbf'}
    }

for folder_name, extensions in folder_names.items():
    organized_info += f"{folder_name}: {', '.join(extensions)}\n"

def file_sorter_function(directory):
    # ---------------------- GET ALL FILES
    files = [f for f in listdir(directory) if isfile(join(directory, f))]
    organized_files = {folder_name: [] for folder_name in folder_names}

    # ---------------------- CREATE FOLDERS
    for file in files:
        filename, file_extension = os.path.splitext(file)
        file_extension = file_extension[1:].lower()

        for folder_name, extensions in folder_names.items():
            if file_extension in extensions:
                target_folder = os.path.join(directory, folder_name)
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)

                # ---------------------- MOVE FILES / KEEP TRACK
                shutil.move(os.path.join(directory, file), os.path.join(target_folder, file))
                organized_files[folder_name].append(file)
                break

    # ---------------------- PRINT RESULT
    for folder_name, files in organized_files.items():
        if files:
            result = f"\n{folder_name}:"
            for file in files:
                result += f"\n- {file}" # TODO More data for the report should be here
            DataValues.result_list += result
            DataValues.result_list += "\n"

    if DataValues.result_list:
        print("\nSorted Categories Result:")
        print("--------------------------------------")
        print(DataValues.result_list)
        print("\nFiles organized.")

# ---------------------- GUI BRAIN
def create_folder_dialog(sender, app_data):
    dpg.show_item("file_dialog_id")

def ok_callback(sender, app_data):
    global selected_file_path
    selected_file_path = app_data['file_path_name']  # Get the selected file path
    dpg.hide_item("file_dialog_id")
    dpg.set_value("selected_folder_text", selected_file_path)

def report_callback(sender, app_data):
    dpg.set_value("result_list", DataValues.result_list)

def cancel_callback(sender, app_data):
    print('Cancel was clicked.')

# ---------------------- GUI WINDOWS / ITEMS
dpg.create_context()
data = DataValues()
with dpg.window(label="FILE SORTER AUTOMATION", # --------- MAIN WINDOW
                width=370,
                height=340,
                pos=(2, 1),
                no_close=True,
                no_collapse=True,
                no_move=True,
                no_resize=True,
                no_scrollbar=True,
                no_title_bar=True):

    with dpg.menu_bar():
        with dpg.menu(label="Supported Files"): dpg.add_menu_item(label=organized_info) # --------- MENU BAR
        with dpg.menu(label="WARNINGS!!!"):
            bar = dpg.add_menu_item(label=
                       "-> Be cautious when selecting the folder to run this script.\n\n"
                       "-> Running it on the wrong directory could impact your system's functionality.\n\n"
                       "-> This script also operates on hidden folders, so exercise extra care during usage.\n\n"
                       "-> Files with the same name in the destination folder will be automatically overwritten.\n\n"
                       "-> Reccomend to use only on personal folders such as Downloads, Documents...\n\n"
                       "-> Close any open files before running the script, so it is possible to move the file.")

    inst = dpg.add_input_text(label="string", # --------- INSTRUCTIONS
                       width=width,
                       height=306,
                       multiline = True,
                       readonly = True,
                       default_value=
                       "===== INSTRUCTIONS =====\n\n"
                       "This tool is designed to simplify \nthe process of organizing a directory.\n\n"
                       "Its purpose is to help you structure \nyour digital space efficiently:\n\n"
                       "-> Specify the target folder where you want \n   the tool to organize your files.\n\n"
                       "-> All of the files will be sorted \n   to the respected folder. \n   * See the Supported files!\n\n"
                       "-> Folders that already exists will \n   be left untouched.\n\n"
                       "-> READ THE WARNINGS SECTION OR \n   SUFFER THE CONSEQUENCES! =D")

    with dpg.window(label="Choose & Run:", # --------- FOLDER SELCTION
                    pos=(2, 347),
                    width=370,
                    height=208,
                    no_scrollbar=True,
                    no_resize=True,
                    no_collapse=True,
                    no_move=True,
                    no_close=True):

        menu = dpg.add_file_dialog(directory_selector=True, # --------- FOLDER MENU
                            show=False,
                            callback=ok_callback,
                            cancel_callback=cancel_callback,
                            tag="file_dialog_id",
                            width=700,
                            height=430)

        dpg.add_button(label="Select your folder:", # --------- SELECT YOUR FOLDER
                       callback=create_folder_dialog,
                       width=360,
                       height=40)

        dpg.add_input_text(default_value="...",
                           width=360,
                           height=30,
                           readonly=True,
                           tag="selected_folder_text",
                           track_offset=0.5)

        dpg.add_button(label="RUN",
                       callback=lambda: file_sorter_function(selected_file_path), # --------- RUN
                       width=360,
                       height=60)

        dpg.add_button(label="Download: report.txt",
                       # callback=lambda: file_sorter_function(selected_file_path),  # --------- RUN
                       width=360,
                       height=40)

    with dpg.window(label="Report:", # --------- RUN RESULT
                    pos=(378,1),
                    width=395,
                    height=555,
                    no_resize=True,
                    no_collapse=True,
                    no_close=True,
                    no_move=True):

        rep = dpg.add_button(label="Generate Report", # --------- REPORT BUTTON
                        width=390,
                        height=30,
                        callback=report_callback)

        dpg.add_input_text(default_value="...", # --------- REPORT
                           width=390,
                           height=485,
                           readonly=True,
                           multiline=True,
                           callback=report_callback,
                           tag="result_list")

dpg.create_viewport(title='File Sorter', # --------- SCREE CONFIG
                    width=width,
                    height=height,
                    y_pos=200,
                    x_pos=900,
                    resizable=False)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
