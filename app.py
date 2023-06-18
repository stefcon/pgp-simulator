# Initialize the user modules first by importing them!
import lib
import gui
import tkinter as tk
from gui.index import *

# All frames/pages used in the app
FRAMES = (HOME_PAGE, SEND_PAGE, RECEIVE_PAGE, KEY_VAULT_PAGE)

class PGPSimulatorApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("PGP Simulator")

        container = tk.Frame(self) 
        container.pack(side = "top", fill = "both", expand = True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {} 
  
        for F in FRAMES:
            frame = F(container, self)
  
            self.frames[F] = frame
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.display_frame(HOME_PAGE)
  

    def display_frame(self, cont):
        """
        Display a frame for the given page name
        """
        frame : tk.Frame = self.frames[cont]
        frame.tkraise()


def main():
    app = PGPSimulatorApp()
    app.mainloop()

if __name__ == "__main__":
    main()
