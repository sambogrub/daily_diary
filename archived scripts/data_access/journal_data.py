from .entries_repository import EntriesRepository
from .goals_repository import GoalsRepository
import datetime
from typing import *
import calendar

class JournalData():
    def __init__(self):
        self.entry_repo = EntriesRepository()
        self.goals_repo = GoalsRepository()

    # get all the data needed for each day in the month. takes a date, and returns a list of dictionaries for the whole month
    # returns [{date: {entry: entry,goal_id:(description,state)}}]
    def populate_month_data(self, date: datetime) -> list[dict]:
        #get the current year and month from the given date then get the first and last days of the current month
        year = date.year
        month = date.month
        first_day = self.format_date_for_repos(datetime.date(year,month,1))
        last_day_cal = calendar.monthrange(year,month)
        last_day = self.format_date_for_repos(datetime.date(year,month,last_day_cal[1]))

        #get the journal entries for the month
        entries = self.entry_repo.get_monthly_entries(first_day, last_day)
        goals = self.goals_repo.get_goals()
        goal_states = self.goals_repo.get_monthly_states(first_day,last_day)
        
        goal_states_and_descriptions = []

        #add the descriptions to the tuples of id and state
        for goal_state in goal_states:
            goal_id = goal_state[0]
            state = goal_state[1]
            for goal in goals:
                if goal[0] == goal_id:
                    goal_states_and_descriptions.append((goal_id,goal[1],state))

        return entries,goal_states_and_descriptions

    # ensure that the dates passed to the repo are in the correct string format
    def format_date_for_repos(self,date)->str:
        formatted_date = date.isoformat()
        return formatted_date
            



    




