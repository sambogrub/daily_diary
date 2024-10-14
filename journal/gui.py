import controller
import tkinter as tk
from tkinter import ttk

WINDOW_SIZE = (500,600,150,150) # (size x, size y, location x, location y)
WINDOW_RESIZEABLE = (False,False)

class JournalGUI(tk.Tk):
    def __init__(self,controller):
        super().__init__()
        self.controller = controller
        self.window_specs()
        self.style_configure()
        

    # define out specs for the main window
    def window_specs(self):
        self.geometry(f'{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}+{WINDOW_SIZE[2]}+{WINDOW_SIZE[3]}')
        self.resizable(WINDOW_RESIZEABLE[0],WINDOW_RESIZEABLE[1])
        self.title("Daily Journal")

    # configure styles for windows and widgets
    def style_configure(self):
        style = ttk.Style()
        style.theme_use('alt')
    
    # populate window with appropriate frames
    def building_frames(self):
        pass





    # start the gui side of the app
    def start_gui(self):
        self.mainloop()
