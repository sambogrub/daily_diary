"""
This is the main data access module. It contains the BaseRepository parent class, which both the EntriesRepository and GoalsRepository classes use.
The db connection and initialization have been separated from the repository classes.
"""

import datetime
import sqlite3
from contextlib import contextmanager

import logger
from config import DATABASE_NAME, GOALS_STATE_TABLE, GOALS_TABLE, ENTRIES_TABLE


# # retreive the db connection
# def journal_db_connection(database_name: str = DATABASE_NAME) -> sqlite3.Connection:
#     """ Function provides a sqlite3.Connection for the Journal DB. """
#     return sqlite3.connect(database_name)


# initialize the db and tables if needed
def initialize_journal_db(cursor: sqlite3.Cursor, logger: logger) -> None:
    """ Function responsible for initializing Journal DB. """
    # Querys to create the appropriate tables
    goals_table_query = f'''
    CREATE TABLE IF NOT EXISTS {GOALS_TABLE} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal_description TEXT UNIQUE
    )'''
    goals_state_table_query = f'''
    CREATE TABLE IF NOT EXISTS {GOALS_STATE_TABLE} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_date DATE NOT NULL,
    goal_id INTEGER NOT NULL,
    state BOOLEAN DEFAULT 0,
    FOREIGN KEY (entry_date) REFERENCES entries(date) ON DELETE CASCADE,
    FOREIGN KEY (goal_id) REFERENCES goals(id) ON DELETE CASCADE
    )'''
    entry_table_query = '''
        CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE UNIQUE,
        entry TEXT
        )'''

    with cursor() as cursor:
        cursor.execute(goals_table_query)
        # cursor.execute(goals_state_table_query)
        # cursor.execute(entry_table_query)

    # try:
    #     cursor = connection.cursor()
    #     cursor.execute(goals_table_query)
    #     cursor.execute(goals_state_table_query)
    #     cursor.execute(entry_table_query)
    #     connection.commit()
    # except sqlite3.IntegrityError as e:
    #     connection.rollback()
    #     logger.exception('SQLite error: %s', e)
    # except Exception as e:
    #     connection.rollback()
    #     logger.exception('Error at: %s', e)
    #     raise
    

class BaseRepository:
    # parent class for the other repositories
 
    def __init__(self,cursor):
        self.logger = logger.journal_logger()
        self.cursor = cursor
        initialize_journal_db(cursor, self.logger)

    # connection manager, to be used in 'with' statements
    # @contextmanager
    # def cursor(self):
        
    #     try:
    #         cursor = self.conn.cursor()
    #         yield cursor
    #         self.conn.commit()
    #     except sqlite3.IntegrityError as e:
    #         self.conn.rollback()
    #         self.logger.exception('SQLite error: %s', e)
    #     except Exception as e:
    #         self.conn.rollback()
    #         self.logger.exception('Error at: %s', e)
    #         raise
    #     # I'm unsure if this needs to still be implemented
    #     # finally:
    #     #     self.conn.close()

    # basic insert function. Does not return anything. Takes a list of the columns needed, and a list of tuples
    def insert(self, table: str, columns: list, values: list[tuple]):
        columns_str = ', '.join(columns)
        placeholders = ', '.join(['?'] * len(columns))
        query = f'INSERT INTO {table} ({columns_str}) VALUES ({placeholders})'

        self.logger.debug('Inserting with query: %s, and values %s', query, values)

        with self.cursor() as cursor:
            cursor.executemany(query, values)

    # basic select function. Returns all the results as a list. Takes a list of columns and a dictionary of conditions.
    # conditions should be in the format of column: condition
    def select(self, table: str, columns: list = ['*'], conditions: dict = None, conditions_range: dict = None) -> list:
        columns_str = ', '.join(columns)
        where_clause = ''
        values = ()

        # takes conditions and adds them to the where clause
        if conditions:
            where_clause = ' WHERE ' + ' AND '.join([f'{k} = ?' for k in conditions.keys()])
            values = tuple(conditions.values())

        # takes the conditions range items, like a date, and arranges them in the where clause
        if conditions_range:
            if where_clause:
                where_clause += ' AND '
            else:
                where_clause += ' WHERE '
            where_clause += ' AND '.join([f'{key} BETWEEN ? AND ?' for key in conditions_range.keys()])
            for key in conditions_range:
                values += tuple(conditions_range[key])

        self.logger.debug('selecting with query: SELECT %s FROM %s %s, and values %s',
                          columns_str, table, where_clause, values)

        with self.cursor() as cursor:
            cursor.execute(
                f'SELECT {columns_str} FROM {table} {where_clause}', values
            )
            results = cursor.fetchall()
        return results

    # basic delete function. takes a table name as a string, and takes a dictionary of conditions {column_name: condtition}
    def delete(self, table: str, conditions: dict):
        where_clause = ' AND '.join([f'{key} = ?' for key in conditions.keys()])
        values = tuple(conditions.values())

        self.logger.debug('deleting with query: DELETE FROM %s WHERE %s, and values %s',
                          table, where_clause, values)

        with self.cursor() as cursor:
            cursor.execute(f'DELETE FROM {table} WHERE {where_clause}', values)

    # basic update function
    def update(self, table: str, conditions: dict, data: dict):
        set_clause = ', '.join([f'{key} = ?' for key in data.keys()])
        where_clause = ' AND '.join([f'{key} = ?' for key in conditions.keys()])
        values = tuple(data.values()) + tuple(conditions.values())

        self.logger.debug('updating with query: UPDATE % SET %s WHERE %s, and values %s',
                          table, set_clause, where_clause, values)

        with self.cursor() as cursor:
            cursor.execute(f'UPDATE {table} SET {set_clause} WHERE {where_clause}', values)


class GoalsRepository(BaseRepository):
    def __init__(self,cursor):
        super().__init__(cursor)
        self.goals_table = GOALS_TABLE
        self.goals_state_table = GOALS_STATE_TABLE

    # adds a new goal to the goals table
    def add_new_goal(self, description):
        self.insert(self.goals_table, ['goal_description'], [(description,)])

    # updates the selected goal
    def edit_goal(self, old_goal, new_goal):
        self.update(self.goals_table, {'goal_description': old_goal}, {'goal_description': new_goal})

    # returns a list of all goals with their ids
    def get_goals(self) -> list[tuple]:
        goals = self.select(self.goals_table)
        return goals

    # deletes a specified goal
    def delete_goal(self, goal_id: int):
        self.delete(self.goals_table, {'id': goal_id})

    # adding goal states to the goal_states table. Takes a date and a dictionary of {goal_id: state}
    def add_goal_states(self, entry_date: datetime, goals: dict):
        formatted_date = entry_date.isoformat()
        columns = ['entry_date', 'goal_id', 'state']
        values = []
        for goal in goals:
            value = (formatted_date, goal, goals[goal])
            values.append(value)

        self.insert(self.goals_state_table, columns, values)

    # get the goals state of completion for the specific date
    def get_goal_states(self, date: datetime) -> list[tuple]:
        formatted_date = date.isoformat()
        states = self.select(self.goals_state_table, conditions={'entry_date': formatted_date})
        return states

    # delete the goal states for the given date
    def delete_goal_states(self, date: datetime):
        formatted_date = date.isoformat()
        self.delete(self.goals_state_table, {'entry_date': formatted_date})

    # edit goal states. takes a date, and dictionary with {goal_id: state}
    def edit_goal_states(self, date: datetime, new_states: dict):
        formatted_date = date.isoformat()
        with self.cursor() as cursor:
            for goal_id in new_states:
                set_clause = 'state = ?'
                where_clause = 'entry_date = ? AND goal_id = ?'
                values = (new_states[goal_id], formatted_date, goal_id)
                cursor.execute(f'UPDATE {self.goals_state_table} SET {set_clause} WHERE {where_clause}', values)

    # get the goal states for the entire month
    def get_monthly_states(self, first_day, last_day) -> list[tuple]:
        states = self.select(self.goals_state_table, ['goal_id', 'state'],
                             conditions_range={'entry_date': (first_day, last_day)})
        return states


class EntriesRepository(BaseRepository):
    def __init__(self, cursor):
        super().__init__(cursor)
        self.entries_table = ENTRIES_TABLE
       
    # adds a new entry to the table, takes a datetime.date() object
    def add_entry(self, date: datetime, entry_text: str):
        formatted_date = date.isoformat()
        self.insert(self.entries_table, ['date', 'entry'], [(formatted_date, entry_text)])

    # gets the specified dates entry, takes a datetime.date() object
    def get_entry(self, date: datetime):
        formatted_date = date.isoformat()
        entry = self.select(self.entries_table, conditions={'date': formatted_date})
        return entry

    # deletes the specified dates entry, takes a datetime.date() object
    def delete_entry(self, date: datetime):
        formatted_date = date.isoformat()
        self.delete(self.entries_table, {'date': formatted_date})

    # edits the entry for a specified date
    def edit_entry(self, date: datetime, entry_text: str):
        formatted_date = date.isoformat()
        self.update(self.entries_table, {'date': formatted_date}, {'entry': entry_text})

    # gets the entries for the entire given month
    def get_monthly_entries(self, first_day, last_day) -> list[tuple]:
        entries = self.select(self.entries_table, ['date', 'entry'], conditions_range={'date': (first_day, last_day)})
        return entries

