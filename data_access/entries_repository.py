from .base_repository import BaseRepository
from config import ENTRIES_TABLE
import datetime
from typing import *


class EntriesRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.entries_table = ENTRIES_TABLE
        self.create_table()

    def create_table(self):
        # query to create the entry table
        entry_table_query = '''
        CREATE TABLE IF NOT EXIsTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE UNIQUE,
        entry TEXT
        )'''

        with self.cursor() as cursor:
            cursor.execute(entry_table_query)

    # adds a new entry to the table, takes a datetime.date() object
    def add_entry(self, date: datetime, entry_text: str):
        formatted_date = date.isoformat()
        self.insert(self.entries_table, ['date','entry'], [(formatted_date, entry_text)])

    # gets the specified dates entry, takes a datetime.date() object
    def get_entry(self, date: datetime):
        formatted_date = date.isoformat()
        entry = self.select(self.entries_table, conditions = {'date': formatted_date})
        return entry
    # deletes the specified dates entry, takes a datetime.date() object
    def delete_entry(self, date: datetime):
        formatted_date = date.isoformat()
        self.delete(self.entries_table,{'date': formatted_date})

    # edits the entry for a specified date
    def edit_entry(self, date: datetime, entry_text: str):
        formatted_date = date.isoformat()
        self.update(self.entries_table,{'date':formatted_date},{'entry':entry_text})

    #gets the entries for the entire given month
    def get_monthly_entries(self, first_day, last_day)->list[tuple]:
        entries =self.select(self.entries_table,['date','entry'], conditions_range = {'date':(first_day,last_day)})
        return entries