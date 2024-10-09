# module that contains the main models, the day and the month that contains the days

import calendar as cal
import datetime


class Day():
    def __init__(self, date, entry = None, goals = None, entry_id = None):
        self.date = date
        self.entry = entry
        self.goals = goals if goals is not None else {}
        self.day_num = self.get_day_num()
        self.entry_id = entry_id

    # sets the entry text for the day
    def set_entry(self, entry):
        self.entry = entry

    #returns the number of the day
    def get_day_num(self):
        day_num = self.date.day
        return day_num
    
    # adds the parts of the goals list to the goals dictionary, key = goal id, values = [goal description, state]
    def add_goals(self, goals_list):
        for goal in goals_list:
            id, description, state = goal


#basic month class, builds and holds the day classes in a matrix
class Month():
    def __init__(self, date, journal_data = None):
        self.month_num = date.month
        self.year = date.year
        self.journal_data = journal_data 
        self.month_name = self.set_month_name()
        self.calendar_matrix = self.initialize_calendar_matrix()

    # returns the string of the month name
    def set_month_name(self):
        return cal.month_name[self.month_num]
    
    # builds each day and then adds it to a month matrix, [month[week[day]]]
    def initialize_calendar_matrix(self):
        #blank calendar matrix
        calendar_matrix = []

        # builds the base reference calendar, also where the day objects get their date
        cal_matrix = cal.monthcalendar(self.year, self.month_num)
        
        # ensures the reference calendar matrix is 6 'weeks' long
        while len(cal_matrix) < 6:
            cal_matrix.append([0,0,0,0,0,0,0])
        
        index_dict = {}

        # iterrates over the reference matrix and adds days where appropriate
        for w,week in enumerate(cal_matrix):
            week_list = []

            for i, week_day in enumerate(week):
                if week_day == 0:
                    week_list.append(None)
                else:
                    date = datetime.date(self.year, self.month_num, week_day)
                    day = Day(date)

                    index_dict[week_day] = (w+1,i)

                    week_list.append(day)
            calendar_matrix.append(week_list)

        # insert the index dict at the beginning of the calendar_matrix to easily find the correct

        calendar_matrix.insert(0, index_dict)

        return calendar_matrix
    
    # returns a specific day
    def get_day(self, day_num):
        
        index = self.calendar_matrix[0]
        w,i = index[day_num]
        return self.calendar_matrix[w][i]
    
    #adds all data to days of month. Entries tuples will be (date, entry). goals tuple will be (goal id, state)
    def data_to_days(self,entries: list[tuple],goals: list[tuple]):
        for entry in entries:
            day_num = datetime.datetime.strptime(entry[0], '%Y-%m-%d').date().day
            day = self.get_day(day_num)
            day.set_entry(entry[1])

        for goal in goals:
            day_num = datetime.datetime.strptime(entry[0], '%Y-%m-%d').date().day
            day = self.get_day(day_num)
            goal = [goal]
            day.add_goals(goal)


