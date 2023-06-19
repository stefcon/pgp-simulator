import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
from page_selector import *
from lib.key_rings import *
from lib.interfaces import * 

@implementer(IObserver)
class KeyVaultPage(tk.Frame):
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

        export_button = ttk.Button(row3_frame, text="Export", command=self.export_popup)
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
        new_entry_values = (hex(entry["key_id"]), entry["timestamp"], entry["public_key"], entry["user_id"], entry["key_length"], entry["type"])
        self.public_key_ring_treeview.insert("", tk.END, values=new_entry_values)

    def update_private_key_ring(self, entry):
        """
        Function that updates the private key ring listbox
        """
        new_entry_values = (hex(entry["key_id"]), entry["timestamp"], entry["public_key"], entry["user_id"], entry["encrypted_private_key"], entry["key_length"], entry["type"])
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

    def export_popup(self):
        if len(self.private_key_ring_treeview.selection()) == 0 and len(self.public_key_ring_treeview.selection()) == 0:
            messagebox.showerror("Error", "Please select a key!")
            return
        if len(self.private_key_ring_treeview.selection()) > 1 or len(self.public_key_ring_treeview.selection()) > 1 or \
            len(self.private_key_ring_treeview.selection()) > 0 and len(self.public_key_ring_treeview.selection()) > 0:
            messagebox.showerror("Error", "Please select only one key!")
            return
        
        self.pop = tk.Toplevel(self.controller)
        self.pop.title("Export key")
        self.pop.geometry("300x200")
        self.pop.resizable(False, False)

        row_frame = ttk.Frame(self.pop)
        row_frame.pack(pady=10)

        filename_label = ttk.Label(self.pop, text="File name:")
        filename_label.pack(pady=10)
        self.filename_entry = ttk.Entry(self.pop)
        self.filename_entry.pack()

        enter_button = ttk.Button(self.pop, text="✔", command=self.export_key)
        enter_button.pack(pady=10)

        self.pop.mainloop()


    def export_key(self):
        # Destroy popup
        
        if len(self.private_key_ring_treeview.selection()) > 0:
            # Needs a passphrase for exporting the private key
            self.pop1 = tk.Toplevel(self.controller)
            self.pop1.title("Insert passphrase")
            self.pop1.geometry("300x200")
            self.pop1.resizable(False, False)

            name_label = ttk.Label(self.pop1, text="Passphrase:")
            name_label.pack(pady=10)
            self.passphrase_entry = ttk.Entry(self.pop1, show="*")
            self.passphrase_entry.pack()

            password_button = ttk.Button(self.pop1, text="✔", command=self.export_private_key)
            password_button.pack(pady=10)

            self.pop1.mainloop()
        else:
            key_id = self.public_key_ring_treeview.item(self.public_key_ring_treeview.selection()[0])["values"][0]
            key_id = int(key_id, base=16)

            key = public_key_ring.get_entry_by_key_id(key_id)["public_key"]
            key_type = public_key_ring.get_entry_by_key_id(key_id)["type"]

            export_key(key, key_type, self.filename_entry.get())
            self.pop.destroy()

    def export_private_key(self):
        try:
            key_id = self.private_key_ring_treeview.item(self.private_key_ring_treeview.selection()[0])["values"][0]
            key_id = int(key_id, base=16)
     
            key, key_length, key_type =  private_key_ring.get_decrypted_private_key(key_id=key_id, passphrase=self.passphrase_entry.get())

            export_key(key, key_type, self.filename_entry.get(),  private=True, passphrase=self.passphrase_entry.get())
            print("Exported private key")
        except Exception as e:
            messagebox.showerror("Error", "Wrong passphrase!")
            raise
        finally:
            self.pop.destroy()
            self.pop1.destroy()

    def update_key_rings(self, key, length, key_type):
        try:
            if key_type == RSA_ALGORITHM:
                key_id = key.n % (2**64)
            else:
                key_id = key.p % (2**64)
            if key.has_private():
                private_key_ring.add_entry(
                        key_id=key_id, 
                        key=key,
                        email=self.email_entry.get(),
                        name=self.name_entry.get(),
                        passphrase=self.passphrase_entry.get(),
                        key_length=length, 
                        type=key_type)
                # Only if private part doesn't throw an error!
            public_key_ring.add_entry(
                key_id=key_id, 
                key=key,
                email=self.email_entry.get(),
                name=self.name_entry.get(),
                key_length=length,
                type=key_type)
            messagebox.showinfo("Success", "Key imported successfully!")
        except Exception as e:
            # Add error message popup for each exception
            messagebox.showerror("Error", str(e))
            # raise e
        finally:
            self.pop.destroy()

    def try_to_decrypt(self, filepath, passphrase):
        try:
            key, key_type, key_length = import_key(filepath, passphrase)
            self.update_key_rings(key, key_length, key_type)
        except Exception as e:
            messagebox.showerror("Error", "Wrong passphrase!")
            return
        finally:
            self.pop2.destroy()
        

    def import_key(self):
        """
        Function that imports a key from a file and adds it to the public/private key ring
        """
        filepath = filedialog.askopenfilename()
        try:
            key, key_type, key_length = import_key(filepath)
            self.update_key_rings(key, key_length, key_type)
        except Exception as e:
            if str(e) == "PEM is encrypted, but no passphrase available":
                self.pop2 = tk.Toplevel(self.controller)
                self.pop2.title("Insert passphrase")
                self.pop2.geometry("300x200")
                self.pop2.resizable(False, False)

                name_label = ttk.Label(self.pop2, text="Passphrase:")
                name_label.pack(pady=10)
                self.passphrase_entry = ttk.Entry(self.pop2, show="*")
                self.passphrase_entry.pack()

                password_button = ttk.Button(self.pop2, text="✔", command=lambda: self.try_to_decrypt(filepath, self.passphrase_entry.get()))
                password_button.pack(pady=10)

                self.pop2.mainloop()
            else:
                messagebox.showerror("Error", str(e))
                return
        finally:
            if self.pop is not None:
                self.pop.destroy()


KEY_VAULT_PAGE = KeyVaultPage