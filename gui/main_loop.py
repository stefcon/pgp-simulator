# USED JUST FOR TESTING PURPOSES
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

def browse_file():
    filepath = filedialog.askopenfilename()
    path_text.delete(1.0, tk.END)
    path_text.insert(tk.END, filepath)

def open_send_window():
    # Add code to open the send window/page
    pass

def open_receive_window():
    # Add code to open the receive window/page
    pass

def open_key_vault_window():
    # Add code to open the key vault window/page
    pass

# Create the main Tkinter window
root = tk.Tk()
root.title("PGP Simulator")

# First row
row1_frame = ttk.Frame(root)
row1_frame.pack(pady=10)

browse_button = ttk.Button(row1_frame, text="Browse", command=browse_file)
browse_button.pack(side=tk.LEFT, padx=5)

path_text = tk.Text(row1_frame, height=1, width=50)
path_text.pack(side=tk.LEFT, padx=5)

# Second row
row2_frame = ttk.Frame(root)
row2_frame.pack(pady=10)

send_button = ttk.Button(row2_frame, text="Send", command=open_send_window)
send_button.pack(side=tk.LEFT, padx=5)

receive_button = ttk.Button(row2_frame, text="Receive", command=open_receive_window)
receive_button.pack(side=tk.LEFT, padx=5)

# Third row
row3_frame = ttk.Frame(root)
row3_frame.pack(pady=10)

key_vault_button = ttk.Button(row3_frame, text="Key Vault", command=open_key_vault_window)
key_vault_button.pack()

# Start the Tkinter event loop
root.mainloop()
