import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
import os

from page_selector import *

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        row1_frame = ttk.Frame(self)
        row1_frame.pack(pady=10)

        send_button = ttk.Button(row1_frame, text="Send", command=self.open_send_window)
        send_button.pack(side=tk.LEFT, padx=5)

        receive_button = ttk.Button(row1_frame, text="Receive", command=self.open_receive_window)
        receive_button.pack(side=tk.LEFT, padx=5)

        row1_frame = ttk.Frame(self)
        row1_frame.pack(pady=10)

        key_vault_button = ttk.Button(row1_frame, text="Key Vault", command=self.open_key_vault_window)
        key_vault_button.pack()

    def browse_file(self):
        filepath = filedialog.askopenfilename()
        self.path_text.delete(1.0, tk.END)
        self.path_text.insert(tk.END, filepath)

    def open_send_window(self):
        self.controller.display_frame(page_selector(SEND))

    def open_receive_window(self):

        # Check if file exists
        # if not os.path.exists(self.path_text.get(1.0, tk.END).strip()):
        #     messagebox.showerror("Error", "File does not exist!")
        #     return

        self.controller.display_frame(page_selector(RECEIVE))

    def open_key_vault_window(self):
        self.controller.display_frame(page_selector(KEY_VAULT))

HOME_PAGE = HomePage