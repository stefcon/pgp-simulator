import tkinter as tk
import tkinter.ttk as ttk
from zope.interface import implementer
from lib.interfaces import IObserver
from tkinter import messagebox, filedialog
from page_selector import *
from lib.key_rings import *
from lib.Msg import Msg
from lib.pipeline import SendPipeline
import os


@implementer(IObserver)
class SendPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Observe changes in key rings
        private_key_ring.attach(self)
        public_key_ring.attach(self)

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
        self.user_id1_dropdown["values"] = private_key_ring.get_user_ids(type=DSA_ALGORITHM)
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

        self.user_id2_dropdown["values"] = public_key_ring.get_user_ids(type=ELGAMAL_ALGORITHM)
        self.user_id2_dropdown.bind("<<ComboboxSelected>>", self.on_user_id2_selected)
        
        self.user_id2_dropdown.grid(row=4, column=2, padx=5)
        self.private_key_dropdown.grid(row=4, column=3, padx=5)
        self.private_key_dropdown.bind("<<ComboboxSelected>>", self.on_private_key_selected)

        authentication_label = ttk.Label(self, text="Authentication:")
        authentication_label.grid(row=5, column=1, padx=5, pady=10)

        self.authentication_var = tk.StringVar()
        self.authentication_var.set("None")
        self.authentication_output = ttk.Entry(self, textvariable=self.authentication_var, state="disabled")
        self.authentication_output.bind("<<ComboboxSelected>>", self.on_auth_selected)

        self.authentication_output.grid(row=5, column=2, padx=5, pady=10)

        self.authentication_enable = tk.IntVar()
        self.authentication_checkbox = ttk.Checkbutton(self, variable=self.authentication_enable)
        self.authentication_checkbox.bind("<Button-1>", self.on_auth_selected)
        self.authentication_checkbox.grid(row=5, column=3, padx=5, pady=10)


        # Sixth row
        password_label = ttk.Label(self, text="Private key passphrase:")
        password_label.grid(row=6, column=1, padx=5, pady=10)
        
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.configure(state="disabled")
        self.password_entry.grid(row=6, column=2, padx=5, pady=10)
 
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


        # Tenth row
        body_label = ttk.Label(self, text="Message body:")
        body_label.grid(row=10, column=1, padx=5, pady=10)

        self.body_text = tk.Text(self, height=10, width=50)
        self.body_text.grid(row=10, column=2, padx=5, pady=10)

        # Eleventh row
        file_label = ttk.Label(self, text="Output file path:")
        file_label.grid(row=11, column=1, padx=5, pady=10)

        self.path_text = tk.Text(self, height=1, width=50)
        self.path_text.grid(row=11, column=2, padx=5, pady=10)
        self.path_text.insert(tk.END, "Choose a file")
        self.path_text.bind("<FocusIn>", lambda event: self.path_text.delete(1.0, tk.END))
        self.path_text.bind("<FocusOut>", lambda event: self.path_text.insert(tk.END, "Choose a file") if self.path_text.get(1.0, tk.END).strip() == "" else None)

        browse_button = ttk.Button(self, text="Browse", command=self.browse_file)
        browse_button.grid(row=11, column=3, padx=5, pady=10)
        
        check_button = ttk.Button(self, text="✔", command=self.send_message)
        check_button.grid(row=12, column=2, padx=5, pady=10)

        back_button = ttk.Button(self, text="Back", command = lambda: controller.display_frame(page_selector(HOME)))
        back_button.grid(row=12, column=3, padx=5, pady=10)
        

    def browse_file(self):
        filepath = filedialog.askopenfilename()
        self.path_text.delete(1.0, tk.END)
        self.path_text.insert(tk.END, filepath)

    def on_user_id1_selected(self, event):
        user_id = self.user_id1_dropdown.get()
        self.key_id1_dropdown["values"] = private_key_ring.get_key_ids_for_user_id(user_id, type=DSA_ALGORITHM)
        self.key_id1_dropdown.current(0)

    def on_user_id2_selected(self, event):
        user_id = self.user_id2_dropdown.get()
        self.private_key_dropdown["values"] = private_key_ring.get_key_ids_for_user_id(user_id, type=ELGAMAL_ALGORITHM)
        self.private_key_dropdown.current(0)

    def on_private_key_selected(self, event):
        key_id = int(self.private_key_dropdown.get())
        key_type = private_key_ring.get_entry_by_key_id(key_id)['type']
        if key_type == RSA_ALGORITHM:
            self.authentication_var.set(RSA_PSS_ALGORITHM)
        else:
            self.authentication_var.set(DSA_ALGORITHM)


    def on_auth_selected(self, event):
        if (self.authentication_output.get() is not None and \
                    self.authentication_output.get() != "None") and not self.authentication_enable.get():
            self.password_entry.configure(state="normal")
        else:
            self.password_entry.configure(state="disabled")

    def update(self, subject, new_entry):
        if subject == private_key_ring:
            self.user_id2_dropdown["values"] = private_key_ring.get_user_ids(type=ELGAMAL_ALGORITHM)
            if len(self.user_id2_dropdown["values"]):
                self.user_id2_dropdown.current(0)

            self.private_key_dropdown["values"] = private_key_ring.get_key_ids_for_user_id(self.user_id2_dropdown.get(), type=ELGAMAL_ALGORITHM)
            if len(self.private_key_dropdown["values"]):
                self.private_key_dropdown.current(0)
                self.on_private_key_selected(None)
        elif subject == public_key_ring:
            self.user_id1_dropdown["values"] = public_key_ring.get_user_ids(type=DSA_ALGORITHM)
            if len(self.user_id1_dropdown["values"]):
                self.user_id1_dropdown.current(0)

            self.key_id1_dropdown["values"] = public_key_ring.get_key_ids_for_user_id(self.user_id1_dropdown.get(), type=DSA_ALGORITHM)
            if len(self.key_id1_dropdown["values"]):
                self.key_id1_dropdown.current(0)
        else:
            raise ValueError("Invalid subject")
        
    def send_message(self):
        try:
            msg = Msg()
            msg.data = self.body_text.get(1.0, tk.END).strip().encode()
            msg.enc = self.encryption_dropdown.get() if self.encryption_dropdown.get() != "None"  else None
            msg.auth = self.authentication_output.get() if self.authentication_output.get() != "None" and self.authentication_enable.get() else None
            msg.uze_zip = bool(self.zip_var.get())
            msg.uze_rad64 = bool(self.radix_var.get())

            print(msg)

            send_from_key_id = int(self.key_id1_dropdown.get())
            send_to_key_id = int(self.private_key_dropdown.get())

            filepath = os.path.abspath(self.path_text.get('1.0', tk.END).strip())
            send_pipeline = SendPipeline(msg, filepath, send_from_key_id, send_to_key_id, self.password_entry.get().strip())
            msg = send_pipeline.run()
            messagebox.showinfo("Success", "Message sent successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            # raise e
            return



SEND_PAGE = SendPage