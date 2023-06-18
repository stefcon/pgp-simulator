import tkinter as tk
import tkinter.ttk as ttk
from lib.constants import *


class ImportKeyPopup(tk.Toplevel):
    def __init__(self, parent, controller, title):
        tk.Toplevel.__init__(self, parent)
        self.title(title)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)

        row1_frame = ttk.Frame(self)
        row1_frame.grid(row=0, column=0, padx=5, pady=10)

        key_type_label = ttk.Label(row1_frame, text="Key Type:")
        key_type_label.grid(row=0, column=0, padx=5)

        self.key_type_dropdown = ttk.Combobox(row1_frame)
        self.key_type_dropdown["values"] = (RSA_ALGORITHM, DSA_ALGORITHM, ELGAMAL_ALGORITHM)
        self.key_type_dropdown.grid(row=0, column=1, padx=5)
        self.selected_type = RSA_ALGORITHM

        row3_frame = ttk.Frame(self)
        row3_frame.grid(row=2, column=0, padx=5, pady=10)

        import_button = ttk.Button(row3_frame, text="Import", command=self.import_key)
        import_button.grid(row=0, column=0, padx=5)

        cancel_button = ttk.Button(row3_frame, text="Cancel", command=self.destroy)
        cancel_button.grid(row=0, column=1, padx=5)