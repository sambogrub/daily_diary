
# data_access.py
 holds the operators for all sqlite operations

## journal_data
 Controls the flow of data access with the repositories.


## base_repository
 parent module for all repositories to inherit the context manager for sqlite connections

 __insert Function__
 - Attributes: (formatting of attributes will be done in the child repository modules)
   - table: string
   - columns: list - takes a list of strings ['column1', 'column2']
   - values: list[tuple] - takes a list of tuples that corresponds to the columns [(value1, value2)]

## entries_repository
 - inherits from base_repository.py
 manages all methods and functions for interaction with entries table
 
 __Schema__
 - entries table
    - id - INTEGER PRIMARY KEY AUTOINCREMENT
    - date - DATE UNIQUE (date is .isoformat(), ex. 2024-01-01)
    - entry - TEXT

## goals_repository
 - inherits from base_repository.py
 manages all methods and functions for interations with goals and goals_state tables

 __Schema__
 - goals_state table
    - id - INTEGER PRIMARY KEY AUTOINCREMENT
    - entry_date - DATE (matches entry(date))(date is .isoformat(), ex. 2024-01-01)
    - goal_id - INTEGER (matches goals(id))
    - state - BOOLEAN defaults to 0

 - goals table
    - id - INTEGER PRIMARY KEY AUTOINCREMENT
    - goal_description - TEXT





 __Functions/Operations__
 - create tables
 - provide list of goals
   - helpful when making the goal checkboxes? and drop downs
 - retrieve data and assign it to day objects
 - pulling data from the day object and storing it
 - edit entries using the day object data
 - pull data using key words
  
# models.py

 __Variables__
 - date
 - journal entry
 - goals and states - dictionary {goal:[goal_id, state]}

 __Functions/Operations__
 - assigning attributes in their own functions to allow more options to be encapsulated in the function


## Month class
 __Variables__
 - month number
 - month name
 - day matrix (holds all the day ojects needed for that month)

 __Functions/Operations__
 - building the day matrix to hold all the day objects that are needed for that month
   - days in the day
 - revealing the buttons that correspond with the day matrix's days
 


# journal_ui.py

 - top frame with selection buttons
 - 'date'label will change when viewing the journal or calendar (from date format to just the month)
 - journal and calendar frames will be built at the beginning and will be raised/lowered via the selection buttons
 - self.daily_goal_button_dict holds all the daily goal button objects, the keys are the goal ids
   - 
   - this will also be used to activate or deactivate the buttons when a new day is selected
  
