import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from page_selector import *
from lib.key_rings import *

class GenerateKeyPage(tk.Frame):
    """
    Generate key page that has the following structure
    - Label 'Name' with an entry
    - Label 'Email' with an entry
    - Radio buttons in every row that has the following labels: 'RSA', 'DSA', 'ElGamal'
    - Label 'Key length' and a dropdown with the following values: 1024, 2048, 4096
    - Button labeled 'Generate'
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # First row
        row1_frame = ttk.Frame(self)
        row1_frame.pack(pady=10)

        name_label = ttk.Label(row1_frame, text="Name:")
        name_label.pack(side=tk.LEFT, padx=5)

        self.name_entry = ttk.Entry(row1_frame)
        self.name_entry.pack(side=tk.LEFT, padx=5)

        # Second row
        row2_frame = ttk.Frame(self)
        row2_frame.pack(pady=10)

        email_label = ttk.Label(row2_frame, text="Email:")
        email_label.pack(side=tk.LEFT, padx=5)

        self.email_entry = ttk.Entry(row2_frame)
        self.email_entry.pack(side=tk.LEFT, padx=5)

        # Third row
        row3_frame = ttk.Frame(self)
        row3_frame.pack(pady=10)

        key_type_label = ttk.Label(row3_frame, text="Key type:")
        key_type_label.pack(side=tk.LEFT, padx=5)

        self.key_type = tk.StringVar()
        self.key_type.set(RSA_ALGORITHM)

        rsa_radio_button = ttk.Radiobutton(row3_frame, text="RSA", variable=self.key_type, value=RSA_ALGORITHM)
        rsa_radio_button.pack(side=tk.LEFT, padx=5)

        dsa_radio_button = ttk.Radiobutton(row3_frame, text="DSA", variable=self.key_type, value=DSA_ALGORITHM)
        dsa_radio_button.pack(side=tk.LEFT, padx=5)

        elgamal_radio_button = ttk.Radiobutton(row3_frame, text="ElGamal", variable=self.key_type, value=ELGAMAL_ALGORITHM)
        elgamal_radio_button.pack(side=tk.LEFT, padx=5)

        # Fourth row
        row4_frame = ttk.Frame(self)
        row4_frame.pack(pady=10)

        key_length_label = ttk.Label(row4_frame, text="Key length:")
        key_length_label.pack(side=tk.LEFT, padx=5)

        self.key_length_dropdown = ttk.Combobox(row4_frame)
        self.key_length_dropdown["values"] = (1024, 2048)
        self.key_length_dropdown.pack(side=tk.LEFT, padx=5)

        # Fifth row
        row5_frame = ttk.Frame(self)
        row5_frame.pack(pady=10)

        generate_button = ttk.Button(row5_frame, text="Generate", command=self.generate_key)
        generate_button.pack(side=tk.LEFT, padx=5)

        cancel_button = ttk.Button(row5_frame, text="Cancel", command=lambda: controller.display_frame(page_selector(KEY_VAULT)))
        cancel_button.pack(side=tk.LEFT, padx=5)


    def generate_key(self):
        pass

GENERATE_KEY_PAGE = GenerateKeyPage