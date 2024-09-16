# Daily Diary
 Initial thoughts were to make an app that would act as a daily journal along with a daily goal tracker and visualization. 

## Plans and ideas
 - Use SQLite3 for all data handling, not .csv
 - Build a 'Day' class to handle all the stuff from that day. That way I can pass around all the data in one object rather than calling things randomly. __DAY OBJECT EVERYWHERE, EVEN BETWEEN CLASSES__
 - Build a 'Month' class that will be the container for the day objects of that month. It will have the functions to create the day objects, get specific days, possibly even reveal the calendar itself
 - use a date object throughout the code to keep consistency 
 - Simplistic design, swap between journal and 'progress' (keep track of meeing goals, shown in a calendar format)
   - only show journal at start

## TO DO
 - DONE edit goals function in journal_backend
 - DONE edit goals options in journal_gui
 - edit journal function in journal_backend
 - save day functions in journal_gui 
   - save new journal and daily goal data
   - edit existing journal and daily goal data
 - change month functions
 - select days in calendar functions
 - select goals to view in calendar functions

# journal_backend

## Journal class
 holds the operators for all sqlite operations

 __Schema__

 - entries table
    - id - INTEGER PRIMARY KEY AUTOINCREMENT
    - date - DATE UNIQUE 
    - entry - TEXT

 - goals_state table
    - id - INTEGER PRIMARY KEY AUTOINCREMENT
    - entry_date - DATE (matches entry(date))
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
  
## Day class
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
 


# journal_gui

 - top frame with selection buttons
 - 'date'label will change when viewing the journal or calendar (from date format to just the month)
 - journal and calendar frames will be built at the beginning and will be raised/lowered via the selection buttons
 - self.daily_goal_button_dict holds all the daily goal button objects, the keys are the goal ids
   - 
   - this will also be used to activate or deactivate the buttons when a new day is selected
  