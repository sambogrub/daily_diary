from dateutil.relativedelta import relativedelta
from datetime import datetime
import calendar as cal
import tkinter as tk
from tkinter import ttk
from journal_backend import JournalData, Day, Month



class JournalApp():
    def __init__(self, root):
        self.window = root
        self.start()
    
    #calling the startup functions
    def start(self):
        self.journal_data = JournalData()
        self.initial_date_vars()
        self.size_vars()
        self.window_attributes()
        self.ttk_styles()
        self.get_backend_objs()
        self.build_selection_frame()
        self.build_journal_frame()


    def initial_date_vars(self):
        #Setting the current date
        today = datetime.today()
        self.current_date =today.date()
        
        #tkinter variables
        self.selection_label_var = tk.StringVar()       

    #size touples (x,y)
    def size_vars(self):
        self.window_size = (600,800)
        self.selection_frame_size = (self.window_size[0],75)
        self.journal_frame_size = (self.window_size[0], self.window_size[1]-self.selection_frame_size[1])
        self.daily_options_frame_size = (self.window_size[0], 150)
        self.journal_entry_frame_size = (self.window_size[0], self.journal_frame_size[1]-self.daily_options_frame_size[1])

    #initializing the styles used
    def ttk_styles(self):
        style = ttk.Style()
        style.theme_use('alt')
        style.configure('TFrame', borderwidth = 2, relief = 'sunken')

    def get_backend_objs(self):
        self.journal_data = JournalData()

        goal_list = ['Get up early', 'read 20 min', 'exercise']
       
        self.journal_data.add_goals(goal_list)


        self.month = Month(self.current_date.month,self.current_date.year,self.journal_data)

    #shaping and labeling the main window
    def window_attributes(self):
                
        self.window.geometry(f'{self.window_size[0]}x{self.window_size[1]}+250+100')
        self.window.resizable(False, False)
        self.window.title('Journal and Goals')

    
    def build_selection_frame(self):
        self.selection_frame = ttk.Frame(self.window)
        #buttons and date/month label (will swap from date to month depending on what frame is visible)
        self.journal_button = ttk.Button(self.selection_frame, text = 'Journal')
        self.selection_frame_lable = ttk.Label(self.selection_frame, textvariable=self.selection_label_var)
        self.calendar_button = ttk.Button(self.selection_frame, text = 'Calendar')

        self.journal_button.place(anchor = 'w', relx = .1, rely = .5, width = 75, height = 40)
        self.selection_frame_lable.place(anchor = 'center', relx = .5, rely = .5, width = 150, height = 40)
        self.calendar_button.place(anchor = 'e', relx = .9, rely=.5, width = 75, height = 40)


        self.selection_frame.place(x = 0, y = 0, relwidth=1, height = self.selection_frame_size[1])

        self.change_selection_frame_label('date')
    
    def change_selection_frame_label(self, how):
        if how == 'date':
            date = self.current_date.strftime('%B %d, %Y')
            self.selection_label_var.set(date)
        elif how == 'month':
            month = self.current_date.strftime('%B')
            self.selection_label_var.set(month)

    def build_journal_frame(self):
        self.journal_frame = ttk.Frame(self.window)
        self.journal_entry_frame = ttk.Frame(self.journal_frame)
        self.daily_options_frame = ttk.Frame(self.journal_frame)

        self.journal_entry = tk.Text(self.journal_entry_frame)

        self.populate_goal_buttons()

        self.edit_goals_button = ttk.Button(self.daily_options_frame, text = 'Edit Goals')
        self.save_day_button = ttk.Button(self.daily_options_frame, text = 'Save Day')

        self.journal_entry.place(x = 3, y =3, relwidth=.99, relheight=.99)
        self.journal_entry_frame.place(x = 0, y = 0, relwidth=1, height = self.journal_entry_frame_size[1])



        self.daily_options_frame.place(x = 0, y = self.journal_entry_frame_size[1], relwidth=1, height = self.daily_options_frame_size[1])
        self.journal_frame.place(x = 0, y = self.selection_frame_size[1], relwidth=1, height = self.journal_frame_size[1])

        for i in range(4):
            self.daily_options_frame.grid_columnconfigure(i, weight = 1, uniform = 'daily_options_columns')
        
        for i in range(4):
            self.daily_options_frame.grid_rowconfigure(i, weight = 1, uniform = 'daily_options_uniform_rows')

    def populate_goal_buttons(self):
        goals_dict = self.journal_data.get_goals_dict()
        #holds the button objects
        self.daily_goal_button_dict = {}
        column = 0
        row = 0
        for i, id in enumerate(goals_dict):
            goal_button = ttk.Button(self.daily_options_frame, text = goals_dict[id])
            goal_button.grid(column = column, row = row, sticky = 'nsew')
            self.daily_goal_button_dict[id] = goal_button

            row = row if column <3 else row +1
            column = column +1 if column <3 else 0
            

        
       


        

if __name__ == '__main__':
    root = tk.Tk()
    app = JournalApp(root)
    root.mainloop()