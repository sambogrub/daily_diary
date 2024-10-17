import controller
import tkinter as tk
from tkinter import ttk



class JournalGUI():
    def __init__(self,root,controller):
        super().__init__()
        self.controller = controller
        self.style_configure()
        self.window = root
        

    # configure styles for windows and widgets
    def style_configure(self):
        style = ttk.Style()
        style.theme_use('alt')
    
    # populate window with appropriate frames
    def building_frames(self):
        pass


class JournalView():
    def __init__(self,root):
        pass


class CalendarView():
    def __init__(self, root):
        pass
