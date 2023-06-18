import tkinter as tk
import tkinter.ttk as ttk

from page_selector import *

class SendPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        row_frame = ttk.Frame(self)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(4, weight=1)
        
        send_to_label = ttk.Label(self, text="Send to:")
        user_id_label = ttk.Label(self, text="UserID")
        key_id_label = ttk.Label(self, text="KeyID")
        
        user_id_label.grid(row=1, column=2, padx=5)
        key_id_label.grid(row=1, column=3, padx=5)
        send_to_label.grid(row=2, column=1, padx=5)
        
        self.user_id_dropdown = ttk.Combobox(self)
        self.key_id_dropdown = ttk.Combobox(self)
        
        self.user_id_dropdown.grid(row=2, column=2, padx=5)
        self.key_id_dropdown.grid(row=2, column=3, padx=5)
        
        private_key_label = ttk.Label(self, text="Private Key:")
        key_id_label2 = ttk.Label(self, text="KeyID")
        
        key_id_label2.grid(row=3, column=2, padx=5)
        private_key_label.grid(row=4, column=1, padx=5)
        
        self.private_key_dropdown = ttk.Combobox(self)
        
        self.private_key_dropdown.grid(row=4, column=2, padx=5)
        
        password_label = ttk.Label(self, text="Password:")
        password_label.grid(row=5, column=1, padx=5, pady=10)
        
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=5, column=2, padx=5, pady=10)
        
        check_button = ttk.Button(self, text="✔")
        check_button.grid(row=6, column=2, padx=5, pady=10)

        back_button = ttk.Button(self, text="Back", command = lambda: controller.display_frame(page_selector(HOME)))
        back_button.grid(row=6, column=3, padx=5, pady=10)
        

SEND_PAGE = SendPage