# main journal controller. will interact with both the ui and data access

from models import Month
from data_access import JournalData
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

class JournalController():
    def __init__(self):
        self.journal_data = JournalData()
        self.current_date = self.initialize_date() # date object with day, month, year attributes
        self.month = self.get_month()
        
    def initialize_date(self):
        today = date.today()
        return today

    def get_month(self):
        month = Month(self.current_date, self.journal_data)
        entries, goals = self.journal_data.populate_month_data(self.current_date)
        month.data_to_days(entries, goals)

        return month
    
    def increase_month(self):
        self.current_date = self.current_date+relativedelta(days =+ 1)

    def decrease_mont(self):
        self.current_date = self.current_date+relativedelta(days =- 1)
        

