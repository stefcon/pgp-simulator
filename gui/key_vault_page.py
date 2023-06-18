import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
from page_selector import *
from lib.key_rings import *
from lib.interfaces import * 

@implementer(IObserver)
class KeyVaultPage(tk.Frame):
    """
    Key Vault page that has the following strucutre:
    - First row: label 'Public Key Ring' and a listbox with all the public keys
    - Second row: label 'Private Key Ring' and a listbox with all the private keys
    - Third row: button Three buttons with labels 'Generate', 'Import' and 'Export'
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # First row
        row1_frame = ttk.Frame(self)
        row1_frame.pack(pady=10)

        # Initializing public key ring
        public_key_ring_label = ttk.Label(row1_frame, text="Public Key Ring")
        public_key_ring_label.pack(side=tk.LEFT, padx=5)

        public_key_ring_column_names = ("KeyID", "Timestamp", "Public Key", "UserID", "Key length", "Encryption type")
        public_key_ring_columns = ("key_id", "timestamp", "public_key", "user_id", "key_length", "type")
        self.public_key_ring_treeview = ttk.Treeview(row1_frame, columns=public_key_ring_columns, show='headings')
        for c, n in zip(public_key_ring_columns, public_key_ring_column_names):
            self.public_key_ring_treeview.heading(c, text=n)

        self.public_key_ring_treeview.pack(side=tk.LEFT, padx=5)

        # Second row
        row2_frame = ttk.Frame(self)
        row2_frame.pack(pady=10)

        private_key_ring_label = ttk.Label(row2_frame, text="Private Key Ring")
        private_key_ring_label.pack(side=tk.LEFT, padx=5)

        private_key_ring_column_names = ("KeyID", "Timestamp", "Public Key", "UserID", "Encrypted Private Key", "Key length", "Encryption type")
        private_key_ring_columns = ("key_id", "timestamp", "public_key", "user_id", "encrypted_private_key" , "key_length", "type")
        self.private_key_ring_treeview = ttk.Treeview(row2_frame, columns=private_key_ring_columns, show='headings')
        for c, n in zip(private_key_ring_columns, private_key_ring_column_names):
            self.private_key_ring_treeview.heading(c, text=n)

        self.private_key_ring_treeview.pack(side=tk.LEFT, padx=5)

        # Subscribe to key rings
        public_key_ring.attach(self)
        private_key_ring.attach(self)

        # Third row
        row3_frame = ttk.Frame(self)
        row3_frame.pack(pady=10)

        generate_button = ttk.Button(row3_frame, text="Generate", command=lambda: controller.display_frame(page_selector(GENERATE_KEY)))
        generate_button.pack(side=tk.LEFT, padx=5)

        import_button = ttk.Button(row3_frame, text="Import", command=self.import_popup)
        import_button.pack(side=tk.LEFT, padx=5)

        export_button = ttk.Button(row3_frame, text="Export", command=self.export_key)
        export_button.pack(side=tk.LEFT, padx=5)

        unselect_button = ttk.Button(row3_frame, text="Unselect All", command=self.deselect_all)
        unselect_button.pack(side=tk.LEFT, padx=5)

        back_button = ttk.Button(row3_frame, text="Back", command = lambda: controller.display_frame(page_selector(HOME)))
        back_button.pack(side=tk.LEFT, padx=5)

    def deselect_all(self):
        """
        Function that deselects all the selected keys in the private key ring
        """
        for item in self.public_key_ring_treeview.selection():
            self.public_key_ring_treeview.selection_remove(item)
        for item in self.private_key_ring_treeview.selection():
            self.private_key_ring_treeview.selection_remove(item)

    def update(self, subject, new_entry):
        """
        Function that updates the key ring
        """
        if subject == public_key_ring:
            self.update_public_key_ring(new_entry)
        else:    
            self.update_private_key_ring(new_entry)

    def update_public_key_ring(self, entry):
        """
        Function that updates the public key ring treeview
        """
        
        new_entry_values = (entry["key_id"], entry["timestamp"], entry["public_key"], entry["user_id"], entry["key_length"], entry["type"])
        self.public_key_ring_treeview.insert("", tk.END, values=new_entry_values)

    def update_private_key_ring(self, entry):
        """
        Function that updates the private key ring listbox
        """
        new_entry_values = (entry["key_id"], entry["timestamp"], entry["public_key"], entry["user_id"], entry["encrypted_private_key"], entry["key_length"], entry["type"])
        self.private_key_ring_treeview.insert("", tk.END, values=new_entry_values)

    def import_popup(self):
        self.pop = tk.Toplevel(self.controller)
        self.pop.title("Import key")
        self.pop.geometry("300x200")
        self.pop.resizable(False, False)

        name_label = ttk.Label(self.pop, text="Name:")
        name_label.pack(pady=10)
        self.name_entry = ttk.Entry(self.pop)
        self.name_entry.pack()

        email_label = ttk.Label(self.pop, text="E-mail:")
        email_label.pack(pady=10)
        self.email_entry = ttk.Entry(self.pop)
        self.email_entry.pack()

        password_button = ttk.Button(self.pop, text="Browse", command=lambda: self.import_key())
        password_button.pack(pady=10)

        self.pop.mainloop()


    def export_key(self):
        if len(self.private_key_ring_treeview.selection()) == 0 or len(self.public_key_ring_treeview.selection()) == 0:
            messagebox.showerror("Error", "Please select a key!")
            return
        if len(self.private_key_ring_treeview.selection()) > 1 or len(self.public_key_ring_treeview.selection()) > 1 or \
            len(self.private_key_ring_treeview.selection()) > 0 and len(self.public_key_ring_treeview.selection()) > 0:
            messagebox.showerror("Error", "Please select only one key!")
            return
        
        if len(self.private_key_ring_treeview.selection()) > 0:
            # Needs a passphrase for exporting the private key
            self.pop = tk.Toplevel(self.controller)
            self.pop.title("Insert passphrase")
            self.pop.geometry("300x200")
            self.pop.resizable(False, False)

            name_label = ttk.Label(self.pop, text="Passphrase:")
            name_label.pack(pady=10)
            self.name_entry = ttk.Entry(self.pop)
            self.name_entry.pack()

            password_button = ttk.Button(self.pop, text="✔", command=self.export_private_key)
            password_button.pack(pady=10)

            self.pop.mainloop()


            key_id = self.private_key_ring_treeview.item(self.private_key_ring_treeview.selection()[0])["values"][0]
            key = private_key_ring.get_entry(key_id=key_id)["key"]
        else:
            key_id = self.public_key_ring_treeview.item(self.public_key_ring_treeview.selection()[0])["values"][0]
            key = public_key_ring.get_entry(key_id=key_id)["key"]

    def import_key(self, public=True):
        """
        Function that imports a key from a file and adds it to the public/private key ring
        """
        try:
            filepath = filedialog.askopenfilename()
            key, type, length = import_key(self.name_entry.get(), self.email_entry.get(), filepath)
            if key.has_private():
                private_key_ring.add_entry(
                    key_id=key.public_key().export_key('DER')[-8:], 
                    key=key,
                    email=self.email_entry.get(),
                    name=self.name_entry.get(),
                    passphrase='asd', # TODO: fix logic when importing private keys
                    key_length=length, 
                    type=type)
            # Only if private part doesn't throw an error!
            public_key_ring.add_entry(
                key_id=key.public_key().export_key('DER')[-8:], 
                key=key,
                email=self.email_entry.get(),
                name=self.name_entry.get(),
                key_length=length, 
                type=type)
            messagebox.showinfo("Success", "Key imported successfully!")
        except Exception as e:
            # Add error message popup for each exception
            messagebox.showerror("Error", str(e))
        finally:
            self.pop.destroy()


    def export_key(self):
        pass


KEY_VAULT_PAGE = KeyVaultPage