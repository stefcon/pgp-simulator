import tkinter as tk
import tkinter.ttk as ttk
from zope.interface import implementer
from lib.interfaces import IObserver

from page_selector import *
from lib.key_rings import *


@implementer(IObserver)
class SendPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Observe changes in key rings
        private_key_ring.attach(self)
        public_key_ring.attach(self)

        row_frame = ttk.Frame(self)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(4, weight=1)
        
        send_from_label = ttk.Label(self, text="Send from:")
        send_to_label = ttk.Label(self, text="Send to:")
        user_id1_label = ttk.Label(self, text="UserID")
        key_id1_label = ttk.Label(self, text="KeyID")

        # First row
        user_id1_label.grid(row=1, column=2, padx=5)
        key_id1_label.grid(row=1, column=3, padx=5)

        # Second row
        send_to_label.grid(row=2, column=1, padx=5)
        
        
        self.user_id1_dropdown = ttk.Combobox(self)
        self.key_id1_dropdown = ttk.Combobox(self)
        
        # Populate with private keys user_ids
        self.user_id1_dropdown["values"] = private_key_ring.get_user_ids()
        self.user_id1_dropdown.bind("<<ComboboxSelected>>", self.on_user_id1_selected)

        self.user_id1_dropdown.grid(row=2, column=2, padx=5)
        self.key_id1_dropdown.grid(row=2, column=3, padx=5)

        # Fifth row
        send_from_label = ttk.Label(self, text="Send from:")
        user_id2_label = ttk.Label(self, text="UserID")
        key_id2_label = ttk.Label(self, text="KeyID")
        
        user_id2_label.grid(row=3, column=2, padx=5)
        key_id2_label.grid(row=3, column=3, padx=5)
        send_from_label.grid(row=4, column=1, padx=5)
        
        self.user_id2_dropdown = ttk.Combobox(self)
        self.private_key_dropdown = ttk.Combobox(self)

        self.user_id2_dropdown["values"] = public_key_ring.get_user_ids()
        self.user_id2_dropdown.bind("<<ComboboxSelected>>", self.on_user_id2_selected)
        
        self.user_id2_dropdown.grid(row=4, column=2, padx=5)
        self.private_key_dropdown.grid(row=4, column=3, padx=5)
        
        password_label = ttk.Label(self, text="Private key passphrase:")
        password_label.grid(row=5, column=1, padx=5, pady=10)
        
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.configure(state="disabled")
        self.password_entry.grid(row=5, column=2, padx=5, pady=10)


        # Sixth row
        authentication_label = ttk.Label(self, text="Authentication:")
        authentication_label.grid(row=6, column=1, padx=5, pady=10)

        self.authentication_dropdown = ttk.Combobox(self)
        self.authentication_dropdown["values"] = (None, RSA_ALGORITHM, DSA_ALGORITHM)
        self.authentication_dropdown.bind("<<ComboboxSelected>>", self.on_auth_selected)
        self.authentication_dropdown.current(0)

        self.authentication_dropdown.grid(row=6, column=2, padx=5, pady=10)

        # Seventh row
        encryption_label = ttk.Label(self, text="Encryption:")
        encryption_label.grid(row=7, column=1, padx=5, pady=10)

        self.encryption_dropdown = ttk.Combobox(self)
        self.encryption_dropdown["values"] = (None, AES_ALGORITHM, DES3_ALGORITHM)
        self.encryption_dropdown.current(0)

        self.encryption_dropdown.grid(row=7, column=2, padx=5, pady=10)

        # Eight row
        zip_label = ttk.Label(self, text="Zip:")
        zip_label.grid(row=8, column=1, padx=5, pady=10)

        self.zip_var = tk.IntVar()
        zip_checkbox = ttk.Checkbutton(self, variable=self.zip_var)
        zip_checkbox.grid(row=8, column=2, padx=5, pady=10)

        # Ninth row
        radix_label = ttk.Label(self, text="Radix:")
        radix_label.grid(row=9, column=1, padx=5, pady=10)
        self.radix_var = tk.IntVar()
        radix_checkbox = ttk.Checkbutton(self, variable=self.radix_var)
        radix_checkbox.grid(row=9, column=2, padx=5, pady=10)
        
        check_button = ttk.Button(self, text="✔")
        check_button.grid(row=10, column=2, padx=5, pady=10)

        back_button = ttk.Button(self, text="Back", command = lambda: controller.display_frame(page_selector(HOME)))
        back_button.grid(row=10, column=3, padx=5, pady=10)
        
    def on_user_id1_selected(self, event):
        print('Usao sam u on_user_id1_selected')
        user_id = self.user_id1_dropdown.get()
        self.key_id1_dropdown["values"] = private_key_ring.get_key_ids_for_user_id(user_id)

    def on_user_id2_selected(self, event):
        print('Usao sam u on_user_id2_selected')
        user_id = self.user_id2_dropdown.get()
        self.private_key_dropdown["values"] = private_key_ring.get_key_ids_for_user_id(user_id)

    def on_auth_selected(self, event):
        print("Usao sam u on_auth_selected")
        print(self.authentication_dropdown.get())
        if self.authentication_dropdown.get() is not None and \
                    self.authentication_dropdown.get() != "None":
            self.password_entry.configure(state="normal")
        else:
            self.password_entry.configure(state="disabled")

    def update(self, subject, new_entry):
        if subject == private_key_ring:
            self.user_id2_dropdown["values"] = private_key_ring.get_user_ids()
            self.user_id2_dropdown.current(0)
        elif subject == public_key_ring:
            self.user_id1_dropdown["values"] = public_key_ring.get_user_ids()
            self.user_id1_dropdown.current(0)
        else:
            raise ValueError("Invalid subject")

SEND_PAGE = SendPage