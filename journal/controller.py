import calendar
import datetime

from dateutil.relativedelta import relativedelta

import model
from gui import JournalGUI
from model import Month


class JournalData:
    """ This is the controller for the data repositories. It receives instances of both repositories from the main controller. """

    def __init__(self, entries_repo, goals_repo):
        self.entry_repo = entries_repo
        self.goal_repo = goals_repo

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
        goals = self.goal_repo.get_goals()
        goal_states = self.goal_repo.get_monthly_states(first_day, last_day)

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

    # determine if there is an entry, then call the correct method
    def save_or_update_day_data(self, date, entry: str, goals: list[dict] = None):
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
    """ This is the main controller. It handles the Month instances and interfaces with the JournalData controller as well as the UI """

    def __init__(self, entries_repo, goals_repo, root):
        self.journal_data = JournalData(entries_repo, goals_repo)
        self.current_date = datetime.date.today()
        self.month = self._load_month()
        self.ui = JournalGUI(root, self)

    # This returns a Month instance using the current date
    def _load_month(self) -> Month:
        month = model.Month(self.current_date)
        entries, goals = self.journal_data.populate_month_data(self.current_date)
        month.data_to_days(entries, goals)
        return month

    # increases currrent dates month by 1, then creates new month instance with new date
    def next_month(self):
        self.current_date = self.current_date + relativedelta(month=1)
        self.month = self.load_month()

    # decreases current date's month by 1, then creates new month instance with new date
    def previous_month(self):
        self.current_date = self.current_date + relativedelta(month=-1)
        self.month = self.load_month()

    # increases current date's day, and creates new month instance if needed
    def increase_day(self):
        prev_month_num = self.current_date.month
        self.current_date = self.current_date + relativedelta(days=1)
        if prev_month_num != self.current_date.month:
            self.month = self._load_month()
        
    # decreases current date's day, and creates new month instance if needed
    def decrease_day(self):
        prev_month_num = self.current_date.month
        self.current_date = self.current_date + relativedelta(days=-1)
        if prev_month_num != self.current_date.month:
            self.month = self._load_month()

    # sets the current dates entry
    def add_day_entry(self, entry):
        day_num = self.current_date.day
        day = self.month.get_day(day_num)
        day.set_entry(entry)
        self.journal_data.save_day_data(self.current_date, day.entry)

    # gets the current dates entry
    def get_day_entry(self):
        day_num = self.current_date.day
        day = self.month.get_day(day_num)
        return day.entry