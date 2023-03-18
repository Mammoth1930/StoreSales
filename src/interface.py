"""
This file contains logic for the application GUI.
"""
import customtkinter as ctk

from ingest import *
from export import *

# Font to be used for text in the application.
FONT_BOLD = ('Arial', 24, 'bold')
MESSAGE_FONT = ('Arial', 18)

IMPORT_MESSAGE_LABEL_FAILURE = None
IMPORT_MESSAGE_LABEL_SUCCESS = None

EXPORT_MESSAGE_LABEL_FAILURE = None
EXPORT_MESSAGE_LABEL_SUCCESS = None

"""
Specifies the format of the basic GUI used for this application.

Return:
    Tk: Top level widget for the GUI. This can be thought of as the application
    window or root.
"""
def init_gui():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    gui_root = ctk.CTk()
    gui_root.geometry('800x600')
    gui_root.title('Store Sales')

    import_frame = ctk.CTkFrame(master=gui_root)
    import_frame.pack(pady=20, padx=60, fill='x', expand=True)
    
    export_frame = ctk.CTkFrame(master=gui_root)
    export_frame.pack(pady=(0, 20), padx=60, fill='both', expand=True)

    import_label = ctk.CTkLabel(import_frame, text='Upload File', font=FONT_BOLD)
    import_label.pack(pady=20)

    import_button = ctk.CTkButton(
        import_frame,
        text='Browse',
        command=lambda: import_files()
    )
    import_button.pack()

    global IMPORT_MESSAGE_LABEL_FAILURE
    IMPORT_MESSAGE_LABEL_FAILURE = ctk.CTkLabel(
        import_frame,
        text='',
        font=MESSAGE_FONT,
        text_color='red'
    )
    IMPORT_MESSAGE_LABEL_FAILURE.pack(pady=(30, 5))

    global IMPORT_MESSAGE_LABEL_SUCCESS
    IMPORT_MESSAGE_LABEL_SUCCESS = ctk.CTkLabel(
        import_frame,
        text='',
        font=MESSAGE_FONT,
        text_color='green'
    )
    IMPORT_MESSAGE_LABEL_SUCCESS.pack(pady=(0, 30))

    export_label = ctk.CTkLabel(export_frame, text='Export File', font=FONT_BOLD)
    export_label.pack(pady=20)

    group_by = ctk.StringVar()
    group_by.set('ExtractionDate')
    group_by_dropdown = ctk.CTkOptionMenu(
        master=export_frame,
        variable=group_by,
        values=list(GROUP_BY_OPTIONS.keys())
    )
    group_by_dropdown.pack(pady=(0, 10))

    export_button = ctk.CTkButton(
        export_frame,
        text='Export',
        command=lambda: export_file(group_by.get())
    )
    export_button.pack()

    global EXPORT_MESSAGE_LABEL_FAILURE
    EXPORT_MESSAGE_LABEL_FAILURE = ctk.CTkLabel(
        export_frame,
        text='',
        font=MESSAGE_FONT,
        text_color='red'
    )
    EXPORT_MESSAGE_LABEL_FAILURE.pack(pady=(30, 5))

    global EXPORT_MESSAGE_LABEL_SUCCESS
    EXPORT_MESSAGE_LABEL_SUCCESS = ctk.CTkLabel(
        export_frame,
        text='',
        font=MESSAGE_FONT,
        text_color='green'
    )
    EXPORT_MESSAGE_LABEL_SUCCESS.pack(pady=(0, 30))

    return gui_root

"""

"""
def import_files():
    import_status = ingest_data()
    send_status_messages(import_status, 'import')
    
"""

"""
def export_file(group_by_option:str):
    export_status = export_data(group_by_option)
    send_status_messages(export_status, 'export')

"""

"""
def send_status_messages(file_status:dict, operation:str):
    success_msgs = []
    failure_msgs = []

    for file, error in file_status['failed']:
        if isinstance(error, sqlite3.IntegrityError):
            failure_msgs.append(
                f"{file} has already been imported or partially imported! 😐"
            )
        elif operation == 'import':
            failure_msgs.append(
                f"{file} threw the following exception: {error}. It's likely that the format of the file you are importing was incorrect. 😞"
            )
        else:
            failure_msgs.append(
                f"{file} threw the following exception: {error}. It's likely that location you are exporting to doesn't exist. 😞"
            )

    for file in file_status['successful']:
        success_msgs.append(f"{file} was successfully {operation}ed! 😃")

    failure_message = ""
    success_message = ""

    if len(failure_msgs) > 0:
        failure_message = "\n".join(msg for msg in failure_msgs)
    
    if len(success_msgs) > 0:
        success_message = "\n".join(msg for msg in success_msgs)

    update_message_label(operation, failure_message, success_message)


"""

"""
def update_message_label(label_type:str, failure_msg:str, success_msg:str):
    
    if label_type == 'import':
        success_label = IMPORT_MESSAGE_LABEL_SUCCESS
        failure_label = IMPORT_MESSAGE_LABEL_FAILURE
    else:
        success_label = EXPORT_MESSAGE_LABEL_SUCCESS
        failure_label = EXPORT_MESSAGE_LABEL_FAILURE

    failure_label.configure(text_color='red', text=failure_msg)
    success_label.configure(text_color='green', text=success_msg)