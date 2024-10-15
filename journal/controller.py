# main journal controller. will interact with both the ui and data access

import calendar
import datetime

from dateutil.relativedelta import relativedelta

import model
from journal.model import Month


class JournalData:
    """ TODO: Document me! """

    def __init__(self, entry_repo, goals_repo):
        self.entry_repo = entry_repo
        self.goals_repo = goals_repo

    # get all the data needed for each day in the month. takes a date, and returns a list of dictionaries for the whole month
    # returns [{date: {entry: entry,goal_id:(description,state)}}]
    def populate_month_data(self, date_: datetime.date) -> list[dict]:
        # get the current year and month from the given date then get the first and last days of the current month
        year = date_.year
        month = date_.month
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
        if self.entry_repo.get_entry(date) is None:
            self.save_day_data(date, entry, goals)
        else:
            self.update_day_data(date, entry, goals)

    # saves new day data to tables
    def save_day_data(self, date, entry: str, goals: list[dict] = None):
        self.entry_repo.add_entry(date, entry)

    # update entries data to tables
    def update_day_data(self, date, entry: str, goals: list[dict] = None):
        self.entry_repo.edit_entry(date, entry)


class JournalController:
    """ TODO: Document me! """

    def __init__(self, entry_repo, goals_repo):
        self.journal_data = JournalData(entry_repo, goals_repo)
        self.current_date = datetime.date.today()
        self.month = self.load_month()

    # Does it make sense to use this method outside the JournalController?
    # If not, we should make it "private" by adding an underscore to the
    # beginning of the name i.e. _load_month
    def load_month(self) -> Month:
        month = model.Month(self.current_date)
        entries, goals = self.journal_data.populate_month_data(self.current_date)
        month.data_to_days(entries, goals)
        return month

    # Maybe it could be called next_month?
    def increase_month(self):
        self.current_date = self.current_date + relativedelta(month=1)
        self.month = self.load_month()

    # Maybe it could be called previous_month?
    def decrease_month(self):
        self.current_date = self.current_date + relativedelta(month=-1)
        self.month = self.load_month()

    # Maybe it could be called next_day?
    def increase_day(self):
        self.current_date = self.current_date + relativedelta(days=1)
        # what if we cross to the next month?

    # Maybe it could be called previous_day?
    def decrease_day(self):
        self.current_date = self.current_date + relativedelta(days=-1)
        # what if we cross to the previous month?

    def add_day_entry(self, entry):
        day_num = self.current_date.day
        day = self.month.get_day(day_num)
        day.set_entry(entry)
        self.journal_data.save_day_data(self.current_date, day.entry)

    def get_day_entry(self):
        day_num = self.current_date.day
        day = self.month.get_day(day_num)
        return day.entry

