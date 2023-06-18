import tkinter as tk
import tkinter.ttk as ttk

from page_selector import *

class ReceivePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        row1_frame = ttk.Frame(self)
        row1_frame.pack(pady=10)
        
        from_label = ttk.Label(row1_frame, text="From:")
        from_label.pack(side=tk.LEFT, padx=5)
        
        self.user_id_label = ttk.Label(row1_frame, text="UserID")
        self.user_id_label.pack(side=tk.LEFT, padx=5)
        
        row2_frame = ttk.Frame(self)
        row2_frame.pack(pady=10)
        
        public_key_label = ttk.Label(row2_frame, text="Private Key:")
        public_key_label.pack(side=tk.LEFT, padx=5)
        
        self.public_key_id_label = ttk.Label(row2_frame, text="PublicKeyId")
        self.public_key_id_label.pack(side=tk.LEFT, padx=5)
        
        row3_frame = ttk.Frame(self)
        row3_frame.pack(pady=10)

        password_label = ttk.Label(row3_frame, text="Password:")
        password_label.pack(side=tk.LEFT, padx=5)
        
        self.password_entry = ttk.Entry(row3_frame, show="*")
        self.password_entry.pack(side=tk.LEFT, padx=5)
        
        check_button = ttk.Button(row3_frame, text="✔")
        check_button.pack(side=tk.LEFT)

        row4_frame = ttk.Frame(self)
        row4_frame.pack(pady=10)

        self.back_button = ttk.Button(row4_frame, text="Back", command = lambda: controller.display_frame(page_selector(HOME)))
        self.back_button.pack(side=tk.LEFT, padx=5)


RECEIVE_PAGE = ReceivePage

    # TODO: ako ipak pozelimo da radimo preko grida!
    # self.grid_columnconfigure(0, weight=1)
    
    # from_label = ttk.Label(self, text="From:")
    # from_label.grid(row=0, column=0, padx=5)
    
    # user_id_label = ttk.Label(self, text="UserID")
    # user_id_label.grid(row=0, column=1, padx=5)
    
    # public_key_label = ttk.Label(self, text="Private Key:")
    # public_key_label.grid(row=1, column=0, padx=5)
    
    # public_key_id_label = ttk.Label(self, text="PublicKeyId")
    # public_key_id_label.grid(row=1, column=1, padx=5)

    # password_label = ttk.Label(self, text="Password:")
    # password_label.grid(row=2, column=0, padx=5)
    
    # self.password_entry = ttk.Entry(self, show="*")
    # self.password_entry.grid(row=2, column=1, padx=5)
    
    # check_button = ttk.Button(self, text="✔")
    # check_button.grid(row=3, column=0, padx=5, pady=10)

    # back_button = ttk.Button(self, text="Back", command = lambda: controller.display_frame(page_selector(HOME)))
    # back_button.grid(row=3, column=1, padx=5, pady=10)