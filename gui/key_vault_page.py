import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
from page_selector import *
from lib.key_rings import *

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
        # self.public_key_ring_listbox = tk.Listbox(row1_frame, height=10, width=50)

        public_key_ring_column_names = ("KeyID", "Timestamp", "Public Key", "UserID", "Key length", "Encryption type")
        public_key_ring_columns = ("key_id", "timestamp", "public_key", "user_id", "key_length", "type")
        self.public_key_ring_treeview = ttk.Treeview(row1_frame, columns=public_key_ring_columns, show='headings')
        for c, n in zip(public_key_ring_columns, public_key_ring_column_names):
            self.public_key_ring_treeview.heading(c, text=n)
        self.update_public_key_ring()

        self.public_key_ring_treeview.pack(side=tk.LEFT, padx=5)

        # Second row
        row2_frame = ttk.Frame(self)
        row2_frame.pack(pady=10)

        private_key_ring_label = ttk.Label(row2_frame, text="Private Key Ring")
        private_key_ring_label.pack(side=tk.LEFT, padx=5)

        self.private_key_ring_listbox = tk.Listbox(row2_frame, height=10, width=50)
        self.private_key_ring_listbox.pack(side=tk.LEFT, padx=5)

        # Third row
        row3_frame = ttk.Frame(self)
        row3_frame.pack(pady=10)

        generate_button = ttk.Button(row3_frame, text="Generate", command=lambda: controller.display_frame(page_selector(GENERATE_KEY)))
        generate_button.pack(side=tk.LEFT, padx=5)

        import_button = ttk.Button(row3_frame, text="Import", command=self.import_popup)
        import_button.pack(side=tk.LEFT, padx=5)

        export_button = ttk.Button(row3_frame, text="Export", command=self.export_key)
        export_button.pack(side=tk.LEFT, padx=5)

        back_button = ttk.Button(row3_frame, text="Back", command = lambda: controller.display_frame(page_selector(HOME)))
        back_button.pack(side=tk.LEFT, padx=5)

    def update_public_key_ring(self):
        """
        Function that updates the public key ring treeview
        """
        for row in public_key_ring.get_all_entries():
            self.public_key_ring_treeview.insert("", tk.END, values=(row["key_id"], row["timestamp"], row["public_key"], row["user_id"], row["key_length"], row["type"]))

    def update_private_key_ring(self):
        """
        Function that updates the private key ring listbox
        """
        for row in private_key_ring.get_all_entries():
            self.private_key_ring_listbox.insert("", tk.END, row) # TODO: change this to something that works

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

    def import_key(self, public=True):
        """
        Function that imports a key from a file and adds it to the public/private key ring
        """

        try:
            filepath = filedialog.askopenfilename()
            if public:
                public_key_ring.import_key(self.name_entry.get(), self.email_entry.get(), filepath)
                self.update_public_key_ring()
            else:
                private_key_ring.import_key(filepath)
                self.update_private_key_ring()
            messagebox.showinfo("Success", "Key imported successfully!")
            self.pop.destroy()
        except Exception as e:
            # Add error message popup for each exception
            messagebox.showerror("Error", str(e))


    def export_key(self):
        pass


KEY_VAULT_PAGE = KeyVaultPage