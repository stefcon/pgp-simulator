import tkinter as tk
import tkinter.ttk as ttk

from page_selector import *
from lib.key_rings import *
from lib.pipeline import ReceivePipeline
from lib.exceptions import NoPassphrase

@implementer(IObserver)
class ReceivePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller



        #grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(4, weight=1)

        #Graphic elements
        from_label = ttk.Label(self, text="From:")
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
        from_label.grid(row=1, column=1, padx=5)

        user_id_label = ttk.Label(self, text="UserID")
        user_id_label.grid(row=1, column=2, padx=5)

        # Second row
        public_key_label.grid(row=2, column=1, padx=5)

        public_key_id_label = ttk.Label(self, text="PublicKeyId")
        public_key_id_label.grid(row=2, column=2, padx=5)

        # Third row
        password_label.grid(row=3, column=1, padx=5)

        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=3, column=2, padx=5)

        # Fourth row
        check_button = ttk.Button(self, text="✔", command=self.receive_file)
        check_button.grid(row=4, column=1, padx=5, pady=10)

        back_button = ttk.Button(self, text="Back", command=lambda: controller.display_frame(page_selector(HOME)))
        back_button.grid(row=4, column=2, padx=5, pady=10)

    def browse_file(self):
        filepath = tk.filedialog.askopenfilename()
        self.path_text.delete(1.0, tk.END)
        self.path_text.insert(tk.END, filepath)

    def receive_file(self):
        #Prvo pronadji odgovarajuci privatni kljuc
        rp = ReceivePipeline(self.path_text.get(1.0, tk.END).strip())
        rp.attach(self)
        rp.run()

        #Nakon unosa sifre procitaj poruku
        rp.run()


    def update(self, subject: ReceivePipeline, keyID):
        print("update")
        #Otvori prozor za unos sifre
        self.pop = tk.Toplevel(self.controller)
        self.pop.title("Input passphrase")
        self.pop.geometry("300x200")
        self.pop.resizable(False, False)

        name_label = ttk.Label(self.pop, text="KeyID:")
        name_label.pack(pady=10)
        self.passphrase_entry = ttk.Entry(self.pop)
        self.passphrase_entry.pack()

        password_button = ttk.Button(self.pop, text="✔", command=lambda: subject.run_with_passphrase(self.passphrase_entry.get()))
        password_button.pack(pady=10)

        self.pop.mainloop()




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
