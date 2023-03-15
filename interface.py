import tkinter as tk

from ingest import *
from export import *

FONT = ('Arial', 18)

"""

"""
def init_gui():
    gui_root = tk.Tk()
    gui_root.geometry('700x500')
    gui_root.title('Store Sales')

    upload_label = tk.Label(gui_root, text='Upload file', font=FONT)
    upload_label.pack()

    upload_button = tk.Button(gui_root, text='Browse', command=lambda: ingest_data())
    upload_button.pack()

    export_label = tk.Label(gui_root, text='Export file', font=FONT)
    export_label.pack()

    export_button = tk.Button(gui_root, text='Export', command=lambda: export_data(group_by.get()))
    export_button.pack()

    group_by = tk.StringVar()
    group_by.set('ExtractionDate')
    group_by_dropdown = tk.OptionMenu(gui_root, group_by, *list(GROUP_BY_OPTIONS.keys()))
    group_by_dropdown.pack()

    return gui_root