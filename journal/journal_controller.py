# main journal controller. will interact with both the ui and data access

from models import Month
from data_access import JournalData
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

class JournalController():
    def __init__(self):
        self.journal_data = JournalData()
        self.current_date = self.initialize_date() # date object with day, month, year attributes
        self.month = None
        self.get_month()
        
    def initialize_date(self):
        today = date.today()
        return today

    def get_month(self):
        month = Month(self.current_date)
        entries, goals = self.journal_data.populate_month_data(self.current_date)
        month.data_to_days(entries, goals)
        self.month = month
    
    def increase_month(self):
        self.current_date = self.current_date+relativedelta(month =+ 1)
        self.get_month()

    def decrease_month(self):
        self.current_date = self.current_date+relativedelta(month =- 1)
        self.get_month()

    def increase_day(self):
        self.current_date = self.current_date+relativedelta(days =+1)

    def decrease_day(self):
        self.current_date = self.current_date+relativedelta(days =- 1)
    

    def add_day_entry(self,entry):
        day_num = self.current_date.day
        day = self.month.get_day(day_num)
        day.set_entry(entry)
        self.journal_data.save_day_data(self.current_date,day.entry)

    def get_day_entry(self):
        day_num = self.current_date.day
        day = self.month.get_day(day_num)
        return day.entry  



