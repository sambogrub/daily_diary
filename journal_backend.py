import sqlite3
import calendar as cal
from datetime import datetime



#journal class
class JournalData():
    def __init__(self, db_name = 'daily_journal.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        

    #context management for cursor
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        #handle exceptions and clean up resources
        if exc_type is not None:
            #if there is an exception, roll back the transaction
            self.conn.rollback()
        else:
            self.conn.commit()

        #clean up cursor connection
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    #make sure the connection is closed
    def __del__(self):
        if self.conn:
            self.conn.close()

    #create tables if needed
    def create_tables(self):
        
        queries = [
            '''CREATE TABLE IF NOT EXISTS entries(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE UNIQUE,
            entry TEXT
            )''',
            '''CREATE TABLE IF NOT EXISTS goals(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal_description TEXT UNIQUE
            )''',
            '''CREATE TABLE IF NOT EXISTS goals_state(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_date INTEGER NOT NULL,
            goal_id INTEGER NOT NULL,
            completed BOOLEAN DEFAULT 0,
            FOREIGN KEY (entry_date) REFERENCES entries(date) ON DELETE CASCADE,
            FOREIGN KEY (goal_id) REFERENCES goals(id) ON DELETE CASCADE
            )''']
        

        
        try:
                
            for query in queries:
                self.cursor.execute(query)
            self.conn.commit()
                    
        except Exception as e:
            print(f'Error occured in JournalData().create_tables(): {e}')
               
    


    #get list of all goals
    def get_goals_dict(self):
        query = '''SELECT id, goal_description FROM goals'''
        
        goals_dict = {}
        
        try:
            self.cursor.execute(query)
            goals = self.cursor.fetchall()
            goals_dict = {goal[0]: goal[1] for goal in goals}
            return goals_dict
        except Exception as e:
            print(f'Error getting list of goals: {e}')
            return None
       

    #add new goals
    def add_goals(self, goals):
        goal_query = '''INSERT INTO goals (goal_description)
                        VALUES (?)'''
        
        for goal in goals:
            try:
                self.cursor.execute(goal_query,(goal,))
                        
            except Exception as e:
                print(f'error storing goal: {e}')
            
       

    #edit goals table given the goal id
    def edit_goal(self, goal_id, edited_goal):
        edit_query = '''UPDATE goals
                        SET goal_description = ?
                        WHERE id = ?'''
        
        try:
            self.cursor.execute(edit_query,(edited_goal,goal_id))
                    
        except Exception as e:
            print(f'Error updating goal: {e}')
     

    #delete goal from list
    def delete_goal(self, goal_id):
        delete_query = '''DELETE FROM goals
                        WHERE id = ?'''
        
        try:
            self.cursor.execute(delete_query,(goal_id,))
                   
        except Exception as e:
            print(f'Error deleteing goal: {e}')
      
        
    #assign data to day
    def assign_day_data(self, day):
        date = day.date
        # entry = None
        entry_query = '''SELECT entry FROM entries WHERE date = ?'''
        goal_query = '''SELECT goals.id, goals.goal_description, goals_state.completed
                        FROM goals
                        LEFT JOIN goals_state ON goals.id = goals_state.goal_id AND goals_state.entry_date = ?'''
        
        try:
            self.cursor.execute(entry_query,(date,))
            entry = self.cursor.fetchone()
            day.set_entry(entry)
        except Exception as e:
            print(f'Error assigning entry to day {date}: {e}')
        if entry is not None:
            try:
                self.cursor.execute(goal_query,(date,))
                goals = self.cursor.fetchall()
                day.add_goals(goals)
            except Exception as e:
                print(f'Error adding goals on day {date}: {e}')
           

    #check if data is already present in table, then act on that
    def check_if_date(self, day):
       
        try:
            self.cursor.execute('''SELECT 1 FROM entries WHERE date = ?''', (day.date,))
            result = self.cursor.fetchone()
        except Exception as e:
            result = None
            print(f'Error checking day data: {e}')
        if result:
                    
            self.edit_days_data(day)
        else:
                    
            self.add_day_data(day)

        

    #edits entries and goals_state table
    def edit_days_data(self, day):
        
        goals = day.goals #returns a dictionary {goal_id:(goal_description,goal_state)}
        edit_entry_query = '''UPDATE entries
                            SET entry = ?
                            WHERE date = ?'''
        check_goal_state_query = '''SELECT 1 FROM goals_state WHERE (entry_date, goal_id) = (?,?)'''
        edit_goal_state_query = '''UPDATE goals_state
                                SET completed = ?
                                WHERE (entry_date, goal_id) = (?,?)
                                '''
        add_goal_query = '''INSERT INTO goals_state (entry_date, goal_id, completed)
                        VALUES (?,?,?)'''
        
        try:
            self.cursor.execute(edit_entry_query,(day.entry,day.date))
                    
        except Exception as e:
            print(f'Error storing entry: {e}')

        for goal_id, (description,state) in goals.items():
            try:
                self.cursor.execute(check_goal_state_query, (day.date, goal_id))
                result = self.cursor.fetchone()
            except Exception as e:
                print(f'Error checking goal {description} presence: {e}')
            if result:
                try:
                    self.cursor.execute(edit_goal_state_query, (state,day.date,goal_id))
                            
                except Exception as e:
                    print(f'Error updating goal {description} state: {e}')
            else:
                try:
                    self.cursor.execute(add_goal_query, (day.date,goal_id,state))
                    
                except Exception as e:
                    print(f'Error adding goal {description} state: {e}')
       

    #get data from day and load to tables
    def add_day_data(self, day):
        stored = False
        goals = day.goals #returns a dictionary {goal_id:(goal_description,goal_state)}
        entry_query = '''INSERT INTO entries (date, entry)
                        VALUES (?,?)
                        '''
        goals_query = '''INSERT INTO goals_state (entry_date, goal_id, completed)
                        VALUES (?,?,?)'''
        
        #try to insert the day entry
        try:
            self.cursor.execute(entry_query,(day.date,day.entry))
                    
            stored= True
        except Exception as e:
            print(f'Error storing entry: {e}')
                
        #if the day entry insert worked then try to insert the goals states
        if stored:
            for goal_id, (description, state) in goals.items():
                try:
                        
                    self.cursor.execute(goals_query,(day.date,goal_id,state))
                            
                except Exception as e:
                    print(f'Error storing goal {description}: {e}')
                

#day class
class Day():
    def __init__(self, date, entry = None, goals = None, entry_id = None):
        self.date = date
        self.entry = entry
        self.goals = goals if goals is not None else {}
        self.day_num = self.get_day_num()

    def set_entry(self, entry):
        self.entry = entry

    def set_date(self, date):
        self.date = date
    
    def get_day_num(self):
        day_num = self.date.day
        return day_num
    
    #get list of goal touples (goal description, goal id, goal state)
    def add_goals(self, goals_list):
        for goal in goals_list:
            id, description, state = goal
            if state == None:
                state = 0
            self.goals[id] = [description, state]

    #goals are saved by id, need to receive goal id and description
    def is_goal_completed(self, goal):
        if goal[0] in self.goals:
            return self.goals[goal[0]][1]
        else:
            return False
            
    

    
#month class, will open a journal_data object in main class
class Month():
    def __init__(self, month_num, year, journal_data):
        self.month_num = month_num
        self.year = year
        self.journal_data = journal_data
        self.month_name = self.set_month_name()
        self.day_matrix, self.calendar_matrix = self.populate_day_matrix()
        
    

    def set_month_name(self):
        return cal.month_name[self.month_num]
    
    #making the day matrix that holds all the day objects for the month
    def populate_day_matrix(self):
        day_matrix = []
        calendar_matrix = cal.monthcalendar(self.year,self.month_num)
        
        #ensure the day matrix that is built from calendar comparison has the same shape as the button matrix
        while len(calendar_matrix) < 6: # this is the max number of 'weeks' in a month
            calendar_matrix.append([0,0,0,0,0,0,0])
        
        for i, week in enumerate(calendar_matrix):
            week_list = []
            
            
            for i, week_day in enumerate(week):
                
                if week_day == 0:
                    
                    week_list.append(None)
                else:
                    
                    date_str = f'{str(self.year)}-{str(self.month_num)}-{str(week_day)}'
                    date = datetime.strptime(date_str,'%Y-%m-%d').date()
                    day = Day(date)
                    self.journal_data.assign_day_data(day)
                    week_list.append(day)
                    
            day_matrix.append(week_list)
        return day_matrix, calendar_matrix
    
    #return a specific day object that corresponds with the given date
    def get_day(self, date):
        for week in self.day_matrix:
            for day in week:
                if day:
                    if day.date == date:
                        return day
        

