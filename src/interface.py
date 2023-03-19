"""
This file contains logic for the application GUI.
"""
import customtkinter as ctk

from ingest import *
from export import *

# Fonts to be used for text in the application.
FONT_BOLD = ('Arial', 24, 'bold')
MESSAGE_FONT = ('Arial', 18)

# Labels used to display messages to the user on import/export.
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
    # General window/application settings.
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    gui_root = ctk.CTk()
    gui_root.geometry('800x600')
    gui_root.title('Store Sales')

    # Two main frames are used to separate the import and export functionality.
    import_frame = ctk.CTkFrame(master=gui_root)
    import_frame.pack(pady=20, padx=60, fill='x', expand=True)
    
    export_frame = ctk.CTkFrame(master=gui_root)
    export_frame.pack(pady=(0, 20), padx=60, fill='both', expand=True)

    # Widgets for the import functionality.
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

    # Widgets for the export functionality.
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
Function used to begin the file ingestion process. This function will open the
file(s), import the data into the database, and display a message to the user
as to whether or not the operation was successful for each file.
"""
def import_files():
    import_status = ingest_data()
    send_status_messages(import_status, 'import')
    
"""
Function used to begin the file export process. This function will export all of
the information in the database to an .xlsx file and display a message to the
user as to whether or not the operation was successful.

Params:
    group_by_option: A string specifying how the data should be grouped in the
    exported file. This can be one of the following: 'ExtractionDate', 'Month', or 'Year'.
"""
def export_file(group_by_option:str):
    export_status = export_data(group_by_option)
    send_status_messages(export_status, 'export')

"""
Displays a message to the user regarding the success/failure of an import/export
operation. This function will display a message for each file that was imported/
exported.

Params:
    file_status: A dictionary containing the status of each file that
        was imported/exported. The error is also stored with any files that
        failed to import/export.

    operation: A string specifying whether the messages being displayed are
        for an import or export operation.
"""
def send_status_messages(file_status:dict, operation:str):
    success_msgs = []
    failure_msgs = []

    # Get all of the failure messages.
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

    # Get all of the success messages.
    for file in file_status['successful']:
        success_msgs.append(f"{file} was successfully {operation}ed! 😃")

    # Group all failure and success messages together into two strings.
    failure_message = ""
    success_message = ""

    if len(failure_msgs) > 0:
        failure_message = "\n".join(msg for msg in failure_msgs)
    
    if len(success_msgs) > 0:
        success_message = "\n".join(msg for msg in success_msgs)

    # Display the messages.
    update_message_label(operation, failure_message, success_message)


"""
Updates the GUI to display import/export success/failure messages to the user.

Params:
    label_type: A string specifying whether the messages being displayed are
        for an import or export operation.

    failure_msg: A string containing all of the failure messages to be
        displayed.

    success_msg: A string containing all of the success messages to be
        displayed.
"""
def update_message_label(label_type:str, failure_msg:str, success_msg:str):
    
    # Get the appropriate label widgets.
    if label_type == 'import':
        success_label = IMPORT_MESSAGE_LABEL_SUCCESS
        failure_label = IMPORT_MESSAGE_LABEL_FAILURE
    else:
        success_label = EXPORT_MESSAGE_LABEL_SUCCESS
        failure_label = EXPORT_MESSAGE_LABEL_FAILURE

    # Display the messages.
    failure_label.configure(text_color='red', text=failure_msg)
    success_label.configure(text_color='green', text=success_msg)