# main journal controller. will interact with both the ui and data access
"""
TODO: Add module docs...
"""

import calendar
import datetime

from dateutil.relativedelta import relativedelta

from gui import JournalGUI
from model import Month
from repository import EntriesRepository, GoalsRepository


class JournalData():
    def __init__(self):
        self.entry_repo = EntriesRepository()
        self.goals_repo = GoalsRepository()

    # get all the data needed for each day in the month. takes a date, and returns a list of dictionaries for the whole month
    # returns [{date: {entry: entry,goal_id:(description,state)}}]
    def populate_month_data(self, date: datetime.date) -> list[dict]:
        # get the current year and month from the given date then get the first and last days of the current month
        year = date.year
        month = date.month
        first_day = self.format_date_for_repos(datetime.date(year, month, 1))
        last_day_cal = calendar.monthrange(year, month)
        last_day = self.format_date_for_repos(datetime.date(year, month, last_day_cal[1]))

        # get the journal entries for the month
        entries = self.entry_repo.get_monthly_entries(first_day, last_day)
        goals = self.goals_repo.get_goals()
        goal_states = self.goals_repo.get_monthly_states(first_day, last_day)

        goal_states_and_descriptions = []

        # add the descriptions to the tuples of id and state
        for goal_state in goal_states:
            goal_id = goal_state[0]
            state = goal_state[1]
            for goal in goals:
                if goal[0] == goal_id:
                    goal_states_and_descriptions.append((goal_id, goal[1], state))

        return entries, goal_states_and_descriptions

    # ensure that the dates passed to the repo are in the correct string format
    def format_date_for_repos(self, date) -> str:
        formatted_date = date.isoformat()
        return formatted_date

    def check_if_entry(self, date, entry: str, goals: list[dict] = None):
        if self.entry_repo.get_entry(date) == None:
            self.save_day_data(date, entry, goals)
        else:
            self.update_day_data(date, entry, goals)

    # saves new day data to tables
    def save_day_data(self, date, entry: str, goals: list[dict] = None):
        self.entry_repo.add_entry(date, entry)

    # update entries data to tables
    def update_day_data(self, date, entry: str, goals: list[dict] = None):
        self.entry_repo.edit_entry(date, entry)


class JournalController():
    def __init__(self, root):
        self.journal_data = JournalData()
        self.current_date = self.initialize_date() # date object with day, month, year attributes
        self.month = None
        self.get_month()
        self.ui = JournalGUI(root, self)
        
    def initialize_date(self):
        today = datetime.date.today()
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

