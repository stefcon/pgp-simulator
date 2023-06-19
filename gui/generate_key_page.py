import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from page_selector import *
from lib.key_rings import *

class GenerateKeyPage(tk.Frame):
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

        row5_frame = ttk.Frame(self)
        row5_frame.pack(pady=10)

        password_label = ttk.Label(row5_frame, text="Passphrase (private key):")
        password_label.pack(side=tk.LEFT, padx=5)

        self.passphrase_entry = ttk.Entry(row5_frame, show="*")
        self.passphrase_entry.pack(side=tk.LEFT, padx=5)

        # Fifth row
        row6_frame = ttk.Frame(self)
        row6_frame.pack(pady=10)

        generate_button = ttk.Button(row6_frame, text="Generate", command=self.generate_key)
        generate_button.pack(side=tk.LEFT, padx=5)

        cancel_button = ttk.Button(row6_frame, text="Cancel", command=lambda: controller.display_frame(page_selector(KEY_VAULT)))
        cancel_button.pack(side=tk.LEFT, padx=5)


    def generate_key(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        key_length = int(self.key_length_dropdown.get())
        passphrase = self.passphrase_entry.get()
        key_type = self.key_type.get()

        if not name or not email or not key_length or not key_type:
            messagebox.showerror("Error", "All fields are required")
            return
        
        if key_length not in (1024, 2048):
            messagebox.showerror("Error", "Key length can either be 1024 or 2048")
            return
        try:
            key, key_id = generate_key(key_length, key_type)

            private_key_ring.add_entry(
                key_id=key_id, 
                key=key,
                email=self.email_entry.get(),
                name=self.name_entry.get(),
                passphrase=passphrase,
                key_length=key_length//8,
                type=key_type)
            public_key_ring.add_entry(
                key_id=key_id, 
                key=key,
                email=self.email_entry.get(),
                name=self.name_entry.get(),
                key_length=key_length//8,
                type=key_type)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        messagebox.showinfo("Success", "Key generated successfully.")
        self.controller.display_frame(page_selector(KEY_VAULT))
        

GENERATE_KEY_PAGE = GenerateKeyPage