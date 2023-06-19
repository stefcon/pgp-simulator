import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from page_selector import *
from lib.key_rings import *
from lib.pipeline import ReceivePipeline
from lib.exceptions import NoPassphrase
from lib.exceptions import *

@implementer(IObserver)
class ReceivePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.receive_pipeline = None

        #grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(4, weight=1)

        #Graphic elements
        to_label = ttk.Label(self, text="To:")
        public_key_label = ttk.Label(self, text="Private Key:")
        password_label = ttk.Label(self, text="Password:")

        # First row
        browse_button = ttk.Button(self, text="Browse", command=self.browse_file)
        browse_button.grid(row=0, column=1, padx=5)
        self.path_text = tk.Text(self, height=1, width=50)
        self.path_text.grid(row=0, column=2, padx=5, pady=20)
        self.path_text.insert(tk.END, "Choose a file")
        self.bind("<FocusIn>", lambda event: self.path_text.delete(1.0, tk.END))
        self.bind("<FocusOut>", lambda event: self.path_text.insert(tk.END, "Choose a file") if self.path_text.get(1.0, tk.END).strip() == "" else None)

        # First row
        to_label.grid(row=1, column=1, padx=5)

        self.to_id_var = tk.StringVar()
        self.to_id_var.set("Unknown")
        user_id_label = ttk.Label(self, textvariable=self.to_id_var)
        user_id_label.grid(row=1, column=2, padx=5)

        # Second row
        public_key_label.grid(row=2, column=1, padx=5)

        self.public_key_id_var = tk.StringVar()
        self.public_key_id_var.set("Unknown")
        public_key_id_label = ttk.Label(self, textvariable=self.public_key_id_var)
        public_key_id_label.grid(row=2, column=2, padx=5)

        # Third row
        password_label.grid(row=3, column=1, padx=5)

        self.password_entry = ttk.Entry(self, show="*", state="disabled")
        self.password_entry.grid(row=3, column=2, padx=5)

        # Fourth row

        from_label = ttk.Label(self, text="From:")
        from_label.grid(row=5, column=1, padx=5 )

        self.from_id_var = tk.StringVar()
        self.from_id_var.set("Unknown")
        from_id_label = ttk.Label(self, textvariable=self.from_id_var)
        from_id_label.grid(row=5, column=2, padx=5)

        self.verified_var = tk.StringVar()
        self.verified_var.set("Unknown")
        verified_label = ttk.Label(self, text="Verified:")
        verified_label.grid(row=6, column=1, padx=5)
        verified = ttk.Label(self, textvariable=self.verified_var)
        verified.grid(row=6, column=2, padx=5)

        self.msg_label = ttk.Label(self, text="Message:")
        self.msg_label.grid(row=7, column=1, padx=5, pady=10)
        self.msg_text = tk.Text(self, height=10, width=50, state="disabled")
        self.msg_text.grid(row=7, column=2, padx=5, pady=10)

        check_button = ttk.Button(self, text="✔", command=lambda: self.run_with_passphrase())
        check_button.grid(row=8, column=1, padx=5, pady=10)

        back_button = ttk.Button(self, text="Save message", command=self.save_message)
        back_button.grid(row=8, column=2, padx=5, pady=10)

        back_button = ttk.Button(self, text="Back", command=self.back_and_reset)
        back_button.grid(row=8, column=3, padx=5, pady=10)
        

    def browse_file(self):
        filepath = tk.filedialog.askopenfilename()
        self.path_text.delete(1.0, tk.END)
        self.path_text.insert(tk.END, os.path.abspath(filepath))
        self.receive_pipeline = ReceivePipeline(self.path_text.get(1.0, tk.END).strip())
        self.receive_pipeline.attach(self)
        msg = self.receive_pipeline.run()
        if msg is not None:
            try:
                self.update_frame()
            except BadSignature as bp:
                self.from_id_var.set(hex(self.receive_pipeline.msg.signature_id))
                self.verified_var.set('Bad Signature')

    def update_frame(self):
        self.msg_text.configure(state="normal")
        self.msg_text.insert(tk.END, self.receive_pipeline.msg.data.decode('utf-8'))
        self.msg_text.configure(state="disabled")
        if self.receive_pipeline.msg.signature_id is not None:
                self.from_id_var.set(hex(self.receive_pipeline.msg.signature_id))
                self.verified_var.set('Good Signature')

    def run_with_passphrase(self):
        try:
            self.receive_pipeline.run_with_passphrase(self.password_entry.get().strip())
            self.update_frame()
        except WrongPassphrase as wp:
            messagebox.showerror("Error", "Wrong passphrase!")
            return
        except BadSignature as bp:
            self.from_id_var.set(hex(self.receive_pipeline.msg.signature_id))
            self.verified_var.set('Bad Signature')
            return

    def back_and_reset(self):
        """
        Resets the page to the default state
        """
        self.to_id_var.set("Unknown")
        self.public_key_id_var.set("Unknown")
        self.password_entry.configure(state="disabled")
        self.password_entry.delete(0, tk.END)
        self.path_text.delete(1.0, tk.END)
        self.path_text.insert(tk.END, "Choose a file")
        self.from_id_var.set("Unknown")
        self.verified_var.set("Unknown")
        self.msg_text.configure(state="normal")
        self.msg_text.delete(1.0, tk.END)
        self.msg_text.configure(state="disabled")

        self.controller.display_frame(page_selector(HOME))

    def save_message(self):
        filename = tk.filedialog.asksaveasfilename()
        with open(filename, 'w') as f:
            f.write(self.msg_text.get(1.0, tk.END).strip())

    def update(self, subject: ReceivePipeline, keyID):
        self.public_key_id_var.set(str(hex(keyID)))
        self.to_id_var.set(public_key_ring.get_entry_by_key_id(keyID)['user_id'])
        self.password_entry.configure(state="normal")




RECEIVE_PAGE = ReceivePage

# TODO: ako ipak pozelimo da radimo preko pack!
# row1_frame = ttk.Frame(self)
# row1_frame.pack(pady=10)
#
# from_label = ttk.Label(row1_frame, text="From:")
# from_label.pack(side=tk.LEFT, padx=5)
#
# self.user_id_label = ttk.Label(row1_frame, text="UserID")
# self.user_id_label.pack(side=tk.LEFT, padx=5)
#
# row2_frame = ttk.Frame(self)
# row2_frame.pack(pady=10)
#
# public_key_label = ttk.Label(row2_frame, text="Private Key:")
# public_key_label.pack(side=tk.LEFT, padx=5)
#
# self.public_key_id_label = ttk.Label(row2_frame, text="PublicKeyId")
# self.public_key_id_label.pack(side=tk.LEFT, padx=5)
#
# row3_frame = ttk.Frame(self)
# row3_frame.pack(pady=10)
#
# password_label = ttk.Label(row3_frame, text="Password:")
# password_label.pack(side=tk.LEFT, padx=5)
#
# self.password_entry = ttk.Entry(row3_frame, show="*")
# self.password_entry.pack(side=tk.LEFT, padx=5)
#
# check_button = ttk.Button(row3_frame, text="✔")
# check_button.pack(side=tk.LEFT)
#
# row4_frame = ttk.Frame(self)
# row4_frame.pack(pady=10)
#
# self.back_button = ttk.Button(row4_frame, text="Back", command = lambda: controller.display_frame(page_selector(HOME)))
# self.back_button.pack(side=tk.LEFT, padx=5)
