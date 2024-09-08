import sqlite3
import pandas as pd
import tkinter as tk
from tkinter import ttk
import calendar as cal
import datetime




#handling of the sqlite database to hold the diary entries
class DiaryDatabase():
    def __init__(self):
        self.db_name = 'diary_entries.db'
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS diary_entries(
                            date TEXT NOT NULL,
                            entry TEXT NOT NULL) ''')
        self.conn.commit()

    #Check if there is already an entry
    def add_or_update_entry(self, date, entry_text):
        self.cursor.execute('SELECT * FROM diary_entries WHERE date = ?', (date,))
        entry = self.cursor.fetchone()
        if entry:
            self.update_entry(date,entry_text)
        else:
            self.add_entry(date, entry_text)
        

    #if there is not an entry, add a new one
    def add_entry(self, date, entry_text):
        self.cursor.execute('''
        INSERT INTO diary_entries (date, entry)
        VALUES (?,?) 
        ''', (date, entry_text))
        self.conn.commit()

    #if there is an entry, update it
    def update_entry(self, date, entry_text):
        self.cursor.execute('''
                            UPDATE diary_entries
                            SET entry = ?
                            WHERE date = ?
                            ''', (entry_text, date))
        self.conn.commit()

    #get a specific entry coresponding to a date    
    def get_entry(self, date):
        self.cursor.execute('SELECT * FROM diary_entries WHERE date = ?', (date,))
        entry = self.cursor.fetchone()
        return entry
    
    def close(self):
        self.conn.close()

#handling of csv dataframe
class DailyGoals():
    def __init__(self):
        self.file_name = 'daily_goals.csv'
        self.goals_df = self.load_df()

    def load_df(self):
        df = pd.read_csv(self.file_name)
        return df
    
    def save_df(self):
        self.goals_df.to_csv(self.file_name, index = False)

    def goals_list(self):
        goals = list(self.goals_df.columns)
        goals.pop(0)
        return goals
    
    def goals_by_day(self,date):
        goals = self.goals_list()
        day = self.goals_df.loc[self.goals_df['date'] == date]
        goals_checks = []
        if day.shape[0] >0:
            goals_checks.append(day['mood'].iloc[0])
        else:
            goals_checks.append('')
        for goal in goals[1:]:
            if day.shape[0] >0:
                state = bool(day[goal].iloc[0])
            else:
                state = bool(False)
            goals_checks.append((goal,state))
        return goals_checks

    def goals_to_row(self,date,dict,mood):
        new_row = {}
        if not self.goals_df.loc[self.goals_df['date'] == date].empty:
            self.goals_df.loc[self.goals_df['date'] == date,'mood'] = int(mood)
            for goal in dict:
                self.goals_df.loc[self.goals_df['date'] == date,goal] = dict[goal][1].get()
        else:
            new_row['date'] = date
            new_row['mood'] =int(mood)
            for goal in dict:
                new_row[goal] = dict[goal][1]
            self.goals_df.loc[len(self.goals_df)] = new_row
        
        self.save_df()
        
    def day_has_goals(self,date):
        if not self.goals_df.loc[self.goals_df['date'] == date].empty:
            return True

    def day_goal_state(self,date,goal):
        try:
            state = self.goals_df.loc[self.goals_df['date'] == date, goal].values[0]
            return state
        except (KeyError,IndexError):
            return False


    def add_column(self, column):
        self.goals_df[column] = None
        self.save_df()

    def delete_column(self,column):
        self.goals_df = self.goals_df.drop(column, axis = 1)
        self.save_df()

#main app
class DiaryApp():
    def __init__(self, root):
        self.daily_goals = DailyGoals()
        self.goal_list = self.daily_goals.goals_list()
        self.diary = DiaryDatabase()
               
        self.window_size = (1100,600)

        self.window = root
        self.initialize_date()
        self.initialize_window()
        self.widget_styles()
        self.create_frames()
        self.populate_frames()

    #initialize current date variables
    def initialize_date(self):
        self.today = datetime.date.today()
        
        self.current_day = self.today.day
        self.current_month = self.today.month
        self.current_year = self.today.year
        self.previous_month = self.current_month-1
        if self.current_month == 1:
            self.previous_year = self.current_year -1
        else:
            self.previous_year = self.current_year

    #initialize window creation 
    def initialize_window(self):
        self.window.geometry(f'{str(self.window_size[0])}x{str(self.window_size[1])}+100+100')
        self.window.title('Daily Diary')
        self.window.resizable(False,False)

    #style definition method
    def widget_styles(self):
        self.true_bg_color = 'green'
        self.false_bg_color = 'red'
        self.bad_mood_bg_color = '#1A075D' #deep blue
        self.good_mood_bg_color = '#FFDD33' #golden yellowish

        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('Main.TFrame', borderwidth = 2, relief = 'ridge')
        self.style.configure('TButton', borderwidth = 1, relief = 'groove')
        self.style.configure('StatusTrue.TButton', background = self.true_bg_color)
        self.style.configure('StatusFalse.TButton', background = self.false_bg_color)

    #creates the main frames in the window
    def create_frames(self):
        self.left_frame_width = self.window_size[0]*.7
        self.right_frame_width = self.window_size[0] - self.left_frame_width

        date_frame_height = 50
        options_frame_height = 100
        options_frame_y = self.window_size[1] - options_frame_height
        self.diary_frame_height = self.window_size[1] - date_frame_height - options_frame_height

        
        self.goals_selection_frame_height = 50
        self.calendar_frame_height = (self.window_size[1]-self.goals_selection_frame_height)/2

        self.left_frame = ttk.Frame(self.window, style = 'Main.TFrame')
        self.right_frame = ttk.Frame(self.window, style = 'Main.TFrame')
        self.date_frame = ttk.Frame(self.left_frame, style = 'Main.TFrame')
        self.diary_frame = ttk.Frame(self.left_frame, style = 'Main.TFrame')
        self.daily_goals_frame = ttk.Frame(self.left_frame, style = 'Main.TFrame')
        self.goals_selection_frame = ttk.Frame(self.right_frame, style = 'Main.TFrame')
        self.top_calendar_frame = ttk.Frame(self.right_frame, style = 'Main.TFrame', padding = 5)
        self.bottom_calendar_frame = ttk.Frame(self.right_frame, style = 'Main.TFrame', padding=5)
        

        

        self.left_frame.place(x = 0, y = 0, width= self.left_frame_width, relheight=1)
        self.right_frame.place(x = self.left_frame_width, y = 0, width= self.right_frame_width, relheight=1)
        self.date_frame.place(x = 0, y = 0, relwidth= 1, height = date_frame_height)
        self.diary_frame.place(x = 0, y = date_frame_height, relwidth = 1, height = self.diary_frame_height)
        self.daily_goals_frame.place(x = 0, y = options_frame_y, relwidth = 1, height = options_frame_height)
        self.goals_selection_frame.place(x = 0, y = 0, relwidth=1, height = self.goals_selection_frame_height)
        self.top_calendar_frame.place(x = 0, y = self.goals_selection_frame_height, relwidth=1, height = self.calendar_frame_height)
        self.bottom_calendar_frame.place(x = 0, y = self.calendar_frame_height+self.goals_selection_frame_height, relwidth=1, height=self.calendar_frame_height)
        
        #uniforming the row and columns in the calendar frames
        for i in range(0,8):
            self.top_calendar_frame.grid_columnconfigure(i, weight = 1, uniform = 'cal_col')
            self.bottom_calendar_frame.grid_columnconfigure(i, weight = 1, uniform = 'cal_col')
        
        for i in range (0,7):
            self.top_calendar_frame.grid_rowconfigure(i, weight = 1, uniform='cal_rows')
            self.bottom_calendar_frame.grid_rowconfigure(i, weight = 1, uniform='cal_rows')
       
    #populates the date frame and calls the other populate frame functions
    def populate_frames(self):
        
        #date frame to hold the date label
        month_name = cal.month_name[self.current_month]
        self.current_date = tk.StringVar()
        self.current_date.set(f'{month_name} {str(self.current_day)}, {str(self.current_year)}')

        self.date_label = ttk.Label(self.date_frame, textvariable=self.current_date)

        self.date_label.place(anchor = 'n',x = self.left_frame_width/2, rely = .05, width = 150, relheight=.9)

        #the diary text entry widget
        self.diary_area = tk.Text(self.diary_frame, wrap = 'word')
        self.diary_area.place(x = 3, y = 3, relwidth=.99, height = self.diary_frame_height - 6)
        
        
        #calling the other construction methods
        self.populate_daily_goals_frame()
        self.populate_goal_selection_frame()
        
        self.create_calendars()
        self.reveal_calendars()

        self.update_diary_entry()
    
    #daily goals frame to hold the different daily goals
    def populate_daily_goals_frame(self):
        self.goal_check_dict = {}
        
        self.goals_section_label = ttk.Label(self.daily_goals_frame, text = 'Daily Goals')

        self.edit_goals_button = ttk.Button(self.daily_goals_frame, text = 'Edit Goals', command = self.edit_goals)

        self.goals_section_label.grid(column = 0, row = 0, sticky = 'nsew', padx = 3, pady = 3)
        self.edit_goals_button.grid(column = 1, row = 0, sticky = 'nsew', padx = 3, pady = 3)

        self.save_day_button = ttk.Button(self.daily_goals_frame, text = 'Save Day',command = self.check_day_info)
        self.mood_label = ttk.Label(self.daily_goals_frame, text = 'Overall Mood')
        self.mood_value = tk.StringVar()
        self.mood_entry = ttk.Entry(self.daily_goals_frame, textvariable=self.mood_value)


        self.save_day_button.place(anchor = 'w', x = self.left_frame_width - 125, rely=.65, height = 40, width = 110)
        self.mood_label.place(anchor = 'w', x = self.left_frame_width - 125, rely = .25, height = 35, width = 85)
        self.mood_entry.place(anchor = 'w', x = self.left_frame_width - 40, rely=.25, height = 25, width = 25)
        self.daily_goals_checkboxes()

    #sets the daily goal checkboxes
    def daily_goals_checkboxes(self):
        #this is defined when the frame itself is populated
        if self.goal_check_dict:
            for goal in self.goal_check_dict:
                self.goal_check_dict[goal][0].destroy()

        date = self.format_date(self.current_date.get(),'%Y-%m-%d')

        goal_state_list = self.daily_goals.goals_by_day(date)
        self.mood_value.set(goal_state_list[0])
        column = 0
        row = 1
        for set in goal_state_list[1:]:
            checked_state = tk.BooleanVar(value= set[1])
            
            checkbutton = ttk.Checkbutton(self.daily_goals_frame, text = set[0], variable = checked_state)
            checkbutton.grid(column = column, row = row, sticky = 'nsew', padx = 3, pady = 3)
            if column == 4:
                row +=1
                column = 0
            else:
                column +=1
            self.goal_check_dict[set[0]] = (checkbutton,checked_state)
    
    #create the selection box for the frame
    def populate_goal_selection_frame(self):
        #the selection box for daily goals
        self.selectionbox = ttk.Combobox(self.goals_selection_frame, values = self.goal_list[1:])
        self.selectionbox.place(anchor = 'center', relx=.5, rely = .5, height = 35, width = 150)
        self.selectionbox.bind('<<ComboboxSelected>>', self.reveal_calendars)

        #the previous and next buttons to cycle through the months
        self.previous_month_button = ttk.Button(self.goals_selection_frame, text = '<- Month', command = lambda: self.change_calendar_months('back'))
        self.next_month_button = ttk.Button(self.goals_selection_frame, text = 'Month ->', command = lambda: self.change_calendar_months('forward'))

        self.previous_month_button.place(anchor = 'w', x =10, rely = .5, height = 35, width = 75)
        self.next_month_button.place(anchor = 'e', x = self.right_frame_width - 10, rely=.5, height = 35, width = 75)

    #change the calendar style based on what goal is selected
    def goal_selection_changed(self,event):
        self.current_goal_selection = self.selectionbox.selection_get()
        self.reveal_calendars()
    
    #called when the previous or next month buttons are slected, moving the current and previous months and calling the reveal_calendars function
    def change_calendar_months(self,direction):
        if direction == 'forward':
            if self.current_month == 12:
                self.current_month = 1
                self.current_year +=1
                self.previous_month = 12
            elif self.current_month == 1:
                self.current_month +=1
                self.previous_month = 1
                self.previous_year +=1
            else:
                self.current_month +=1
                self.previous_month+=1
        elif direction == 'back':
            if self.current_month == 2:
                self.current_month -= 1
                self.previous_month = 12
                self.previous_year -= 1
            elif self.current_month == 1:
                self.current_month = 12
                self.current_year -= 1
                self.previous_month -=1
            else:
                self.current_month -= 1
                self.previous_month -= 1

        self.reveal_calendars()

    #create the top calendar using buttons
    def create_calendars(self):
        #day labels at top of calendars
        day_label_list = ['M', 'T','W','Th','F','Sa','Su']
        for i,day in enumerate(day_label_list):
            day_label = ttk.Label(self.top_calendar_frame,text = day)
            day_label.grid(row = 0, column = i + 1, sticky = 'nsew')
            day_label.config(padding=(0,0))

        #month labels at the side of the calendars
        self.top_month_canvas = tk.Canvas(self.top_calendar_frame)
        self.top_month_canvas.grid(row = 0, column = 0, rowspan = 7, sticky = 'nsew')
        self.top_month = self.top_month_canvas.create_text(20, 125, angle = 90, anchor = 'center')

        self.bottom_month_canvas = tk.Canvas(self.bottom_calendar_frame)
        self.bottom_month_canvas.grid(row = 0, column = 0, rowspan = 7, sticky = 'nsew')
        self.bottom_month = self.bottom_month_canvas.create_text(20, 125, angle = 90, anchor = 'center')

        #top section calendar button matrix, will be .grid later
        self.t_day_button_matrix = []
        for row in range(6):
            self.week_day_list = []
            for i in range(7):
                self.day_button = ttk.Button(self.top_calendar_frame) 
                button_touple = [(self.day_button, row+1, i+1), False]
                self.week_day_list.append(button_touple)
            self.t_day_button_matrix.append(self.week_day_list)

        #bottom section calendar button matrix, will be .grid(later)
        self.b_day_button_matrix = []
        for row in range(6):
            self.week_day_list = []
            for i in range(7):
                self.day_button = ttk.Button(self.bottom_calendar_frame)
                button_touple = [(self.day_button, row, i+1), False]
                self.week_day_list.append(button_touple)
            self.b_day_button_matrix.append(self.week_day_list)

    #function to reaveal the buttons that make up the calendars, will be called when the months are changed
    def reveal_calendars(self, event = None):

        #text in the sideways month labels
        top_month = cal.month_name[self.current_month]
        self.top_month_name = top_month + '  ' + str(self.current_year)
        bottom_month = cal.month_name[self.previous_month]
        self.bottom_month_name = bottom_month + '  ' +str(self.previous_year)
        
        self.top_month_canvas.itemconfig(self.top_month, text = self.top_month_name)
        self.bottom_month_canvas.itemconfig(self.bottom_month, text = self.bottom_month_name)

        if self.selectionbox.get():
            self.current_goal_selection = self.selectionbox.selection_get()
        else:
            self.current_goal_selection = None
    
        #matricies from the calendar module, added a blank list as needed
        t_calendar_matrix = cal.monthcalendar(self.current_year,self.current_month)
        if len(t_calendar_matrix) == 5:
            t_calendar_matrix.append([0,0,0,0,0,0,0]) 
        b_calendar_matrix = cal.monthcalendar(self.current_year,self.previous_month)
        if len(b_calendar_matrix) == 5:
            b_calendar_matrix.append([0,0,0,0,0,0,0])

        #hiding and revealing the buttons from the matricies
        for i, week in enumerate(self.t_day_button_matrix):
            calendar_week = t_calendar_matrix[i]
            for i, day in enumerate(week):
                calendar_day = calendar_week[i]
                button_tp, state = day
                button, row, column = button_tp
                if calendar_day == 0 and state == True:
                    button.grid_forget()
                    day[1] = False
                    continue
                elif calendar_day == 0:
                    continue
                date_string = f'{top_month} {calendar_day}, {self.current_year}' 
                date = self.format_date(date_string, '%Y-%m-%d')
                
                if self.current_goal_selection != None:
                    goal_state =self.daily_goals.day_goal_state(date,self.current_goal_selection)
                else:
                    goal_state = False
                    
                    
                day[1] = True
                button.configure(text = calendar_day)
                button.config(command = lambda button = button, m = self.current_month: self.date_selection(button,m,self.current_year))
                button.config(style = 'TButton')
                if goal_state == True:
                    button.config(style = 'StatusTrue.TButton')
                button.grid(row = row, column = column, sticky = 'nsew')

        for i, week in enumerate(self.b_day_button_matrix):
            calendar_week = b_calendar_matrix[i]
            for i, day in enumerate(week):
                calendar_day = calendar_week[i]
                button_tp, state = day
                button, row, column = button_tp
                if calendar_day == 0 and state == True:
                    button.grid_forget()
                    day[1] = False
                    continue
                elif calendar_day == 0:
                    continue
                day[1] = True
                button.configure(text = calendar_day)
                button.config(command = lambda button = button, m = self.previous_month: self.date_selection(button, m, self.previous_year))
                button.grid(row = row, column = column, sticky = 'nsew')
    
    #date selection function for when a date is selected on a calendar
    def date_selection(self, button, month, year):
        day = button.cget('text')
        month_name = cal.month_name[month]
        self.current_date.set(f'{month_name} {day}, {year}')
        self.daily_goals_checkboxes()
        self.update_diary_entry()

    #the edit goals frame
    def edit_goals(self):
        #create the frame and place it in the middle of the window
        self.edit_goals_frame = ttk.Frame(self.window, borderwidth=3, relief='raised', padding=3)
        self.edit_goals_frame.place(anchor = 'center', relx = .5, rely = .5, relheight=.7, relwidth=.25)

        self.edit_goals_frame.grid_columnconfigure(0, weight = 1, uniform = 'edit_goals')
        self.edit_goals_frame.grid_columnconfigure(1, weight = 1, uniform = 'edit_goals')

        #create and populate the widgets inside
        edit_goals_label = ttk.Label(self.edit_goals_frame, text = 'Edit Daily Goals')
        edit_goals_label.grid(row = 0, column = 0, columnspan=2, sticky = 'nsew')

        
        for i, goal in enumerate(self.goal_list[1:]):
            self.goal_label = ttk.Label(self.edit_goals_frame, text = goal)
            self.delete_button = ttk.Button(self.edit_goals_frame, text = 'Delete')
            self.delete_button.config(command = lambda label = self.goal_label: self.delete_goal_check(label))
            self.goal_label.grid(column = 0, row = i+1, sticky = 'nsew')
            self.delete_button.grid(column = 1, row = i+1, sticky = 'nsew')

        self.add_goal_button = ttk.Button(self.edit_goals_frame, text = 'Add New Goal', command = self.create_add_goal_frame)
        self.done_button = ttk.Button(self.edit_goals_frame, text = 'Done', command = self.edit_goals_frame.destroy)
        self.add_goal_button.place(anchor = 's', relx = .5, rely = .9, height = 35, width = 100)
        self.done_button.place(anchor = 's', relx = .5, rely = .99, height = 35, width = 100)
            
    #reinitialize edit goals frame can resets the goals checkboxes in the main window
    def call_edit_goals_frame(self):
        self.daily_goals = DailyGoals()
        self.goal_list = self.daily_goals.goals_list()
        self.daily_goals_checkboxes()
        self.edit_goals()

   #delete goals functions
    def delete_goal_check(self, label):
        goal = label.cget('text')
        
        self.edit_goals_frame.destroy()
        self.you_sure_frame = ttk.Frame(self.window, borderwidth=3, relief='raised')
        self.you_sure_label = ttk.Label(self.you_sure_frame, text = f'Delete {goal}?')
        self.yes_button = ttk.Button(self.you_sure_frame, text = 'Yes, Delete', command = lambda: self.delete_goal(goal))
        self.no_button = ttk.Button(self.you_sure_frame, text = '''Don't Delete''')

        self.you_sure_frame.place(anchor = 'center', relx = .5, rely = .5, height = 95, width = 200)
        self.you_sure_label.place(anchor = 'n', relx = .5, y = 5, height = 35, relwidth=.98)
        self.yes_button.place(anchor = 'sw', x = 5, y = 90, height = 40, relwidth=.45)
        self.no_button.place(anchor = 'se', x = 190, y = 90, height = 40, relwidth=.45)

        self.no_button.config(command = self.dont_delete_goal)
    #called when the 'no' button is selected    
    def dont_delete_goal(self):
        self.you_sure_frame.destroy()
        self.call_edit_goals_frame()
    #called when the 'yes' button is selected
    def delete_goal(self, goal):
        self.daily_goals.delete_column(goal)
        self.you_sure_frame.destroy()
        self.call_edit_goals_frame()

   #add goal function
    def create_add_goal_frame(self):
        #destroy the edit goals frame so it can be rebuilt with updated goals list
        self.edit_goals_frame.destroy()


        self.add_goal_frame = ttk.Frame(self.window, borderwidth=3, relief='raised')     
        self.goal_entry = ttk.Entry(self.add_goal_frame)
        self.add_button = ttk.Button(self.add_goal_frame, text = 'Add')
        self.add_button.config(command = lambda entry = self.goal_entry: self.add_goal(entry))

        self.add_goal_frame.place(anchor = 'center', relx = .5, rely = .5, height = 95, width = 130)
        self.goal_entry.place(anchor = 'n', relx = .5, y = 10, height = 35, width = 110)
        self.add_button.place(anchor = 'n', relx = .5, y = 50, height = 35, width = 70)

    def add_goal(self, entry):
        goal = entry.get()
        goal = goal.replace(' ', '_')
        self.daily_goals.add_column(goal)
        self.add_goal_frame.destroy()
        self.call_edit_goals_frame()

    #function to save the current goals and diary entry to the dataframes
    def check_day_info(self):
        date = self.format_date(self.current_date.get(),'%Y-%m-%d')
        if self.daily_goals.day_has_goals(date):
            self.replace_check_frame = ttk.Frame(self.window)
            self.replace_check_label = ttk.Label(self.replace_check_frame, text = 'Replace day data?')
            self.replace_yes_button = ttk.Button(self.replace_check_frame, text = 'Yes', command = lambda: (self.replace_check_frame.destroy(),self.save_day()))
            self.replace_no_button = ttk.Button(self.replace_check_frame,text = 'No')
            
            self.replace_check_frame.place(anchor = 'center', relx=.5, rely = .5, height = 100, width = 200)
            self.replace_check_label.place(x = 0, y = 0, height = 35, relwidth=1)
            self.replace_yes_button.place(anchor = 'se', relx=.48,rely = .98, height = 35, width = 75)
            self.replace_no_button.place(anchor = 'sw', relx = .52, rely=.98, height = 35, width = 75)

            self.replace_no_button.config(command = self.replace_check_frame.destroy)
        else:
            self.save_day()
        

    def save_day(self):
        
        date = self.format_date(self.current_date.get(),'%Y-%m-%d')
        goals = self.goal_check_dict
        mood = self.mood_entry.get()
        entry = self.diary_area.get('1.0', tk.END)
        self.diary.add_or_update_entry(date,entry)
        self.daily_goals.goals_to_row(date,goals,mood)
        self.daily_goals = DailyGoals()

    #updating the diary entry with an entry if there is one in the database
    def update_diary_entry(self):
        date = self.format_date(self.current_date.get(),'%Y-%m-%d')
        entry = self.diary.get_entry(date)
        self.diary_area.delete('1.0', tk.END)
        if entry:
            self.diary_area.insert(tk.END, entry[1])


    #formatting the date as needed
    def format_date(self,date,how):
        if how == '%Y-%m-%d':
            parsed_date = datetime.datetime.strptime(date, '%B %d, %Y')
            formatted_date = parsed_date.strftime(how)
            return formatted_date
    

            
        
    
        

if __name__ == '__main__':
    root = tk.Tk()
    app = DiaryApp(root)
    root.mainloop()