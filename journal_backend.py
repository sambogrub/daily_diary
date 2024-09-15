import sqlite3
import calendar as cal
from datetime import datetime



#journal class
class JournalData():
    def __init__(self, db_name = 'daily_journal.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.create_tables()
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
        
        cursor = self.conn.cursor()
        try:
         
            for query in queries:
                cursor.execute(query)
            self.conn.commit()
            
        except Exception as e:
            print(f'Error occured in JournalData().create_tables(): {e}')
        finally:
            cursor.close()
        

    #get list of all goals
    def get_goals_dict(self):
        query = '''SELECT id, goal_description FROM goals'''
        cursor = self.conn.cursor()
        goals_dict = {}
        try:
            cursor.execute(query)
            goals = cursor.fetchall()
            goals_dict = {goal[0]: goal[1] for goal in goals}
            return goals_dict
        except Exception as e:
            print(f'Error getting list of goals: {e}')
        finally:
            cursor.close()

    #add new goals
    def add_goals(self, goals):
        goal_query = '''INSERT INTO goals (goal_description)
                        VALUES (?)'''
        cursor = self.conn.cursor()
        for goal in goals:
            try:
                cursor.execute(goal_query,(goal,))
                self.conn.commit()
            except Exception as e:
                print(f'error storing goal: {e}')
      
        cursor.close()

    #assign data to day
    def assign_day_data(self, day):
        date = day.date
        # entry = None
        entry_query = '''SELECT entry FROM entries WHERE date = ?'''
        goal_query = '''SELECT goals.id, goals.goal_description, goals_state.completed
                        FROM goals
                        LEFT JOIN goals_state ON goals.id = goals_state.goal_id AND goals_state.entry_date = ?'''
        cursor = self.conn.cursor()
        try:
            cursor.execute(entry_query,(date,))
            entry = cursor.fetchone()
            day.set_entry(entry)
        except Exception as e:
            print(f'Error assigning entry to day {date}: {e}')
        if entry is not None:
            try:
                cursor.execute(goal_query,(date,))
                goals = cursor.fetchall()
                day.add_goals(goals)
            except Exception as e:
                print(f'Error adding goals on day {date}: {e}')
            finally:
                cursor.close()
        else:
            cursor.close()

    #get data from day and load to tables
    def add_day_data(self, day):
        stored = False
        goals = day.goals #returns a dictionary {goal_id:(goal_description,goal_state)}
        entry_query = '''INSERT INTO entries (date, entry)
                        VALUES (?,?)
                        '''
        goals_query = '''INSERT INTO goals_state (entry_date, goal_id, state)
                        VALUES (?,?,?)'''
        cursor =  self.conn.cursor()

        #try to insert the day entry
        try:
            cursor.execute(entry_query,(day.date,day.entry))
            self.conn.commit()
            stored= True
        except Exception as e:
            print(f'Error storing entry: {e}')
        
        #if the day entry insert worked then try to insert the goals states
        if stored:
            try:
                for goal_id, (description, state) in goals.items():
                    cursor.execute(goals_query,(day.date,goal_id,state))
                self.conn.commit()
            except Exception as e:
                print(f'Error storing goals: {e}')
            finally:
                cursor.close()
        else:
            cursor.close()
        
  

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
        while len(calendar_matrix) < 6:
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
        

