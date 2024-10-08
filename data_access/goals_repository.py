from .base_repository import BaseRepository
from config import GOALS_TABLE, GOALS_STATE_TABLE
import datetime
from typing import *

class GoalsRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.goals_table = GOALS_TABLE
        self.goals_state_table = GOALS_STATE_TABLE
        self.create_table()

    def create_table(self):
        # Querys to create the appropriate tables
        goals_table_query = f'''
        CREATE TABLE IF NOT EXISTS {self.goals_table} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        goal_description TEXT UNIQUE
        )'''
        goals_state_table_query = f'''
        CREATE TABLE IF NOT EXISTS {self.goals_state_table} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entry_date DATE NOT NULL,
        goal_id INTEGER NOT NULL,
        state BOOLEAN DEFAULT 0,
        FOREIGN KEY (entry_date) REFERENCES entries(date) ON DELETE CASCADE,
        FOREIGN KEY (goal_id) REFERENCES goals(id) ON DELETE CASCADE
        )'''

        # use the context manager from base_repository
        with self.cursor() as cursor:

            cursor.execute(goals_table_query)

            cursor.execute(goals_state_table_query)

    # adds a new goal to the goals table
    def add_new_goal(self, description):
        self.insert(self.goals_table, ['goal_description'],[(description,)])

    # updates the selected goal
    def edit_goal(self, old_goal, new_goal):
        self.update(self.goals_table, {'goal_description':old_goal},{'goal_description': new_goal})

    # returns a list of all goals with their ids
    def get_goals(self) -> list[tuple]: 
        goals = self.select(self.goals_table)
        return goals
    
    # deletes a specified goal
    def delete_goal(self, goal_id: int):
        self.delete(self.goals_table,{'id':goal_id})

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
        states = self.select(self.goals_state_table, conditions = {'entry_date': formatted_date})
        return states
    
    # delete the goal states for the given date
    def delete_goal_states(self, date: datetime):
        formatted_date = date.isoformat()
        self.delete(self.goals_state_table,{'entry_date':formatted_date})

    # edit goal states. takes a date, and dictionary with {goal_id: state}
    def edit_goal_states(self, date: datetime, new_states: dict):
        formatted_date = date.isoformat()
        with self.cursor() as cursor:
            for goal_id in new_states:
                set_clause = 'state = ?'
                where_clause = 'entry_date = ? AND goal_id = ?'
                values = (new_states[goal_id], formatted_date, goal_id)
                cursor.execute(f'UPDATE {self.goals_state_table} SET {set_clause} WHERE {where_clause}', values)

    #get the goal states for the entire month
    def get_monthly_states(self,first_day,last_day)->list[tuple]:
        states = self.select(self.goals_state_table,['goal_id','state'],conditions_range = {'entry_date':(first_day,last_day)})
        return states


  

