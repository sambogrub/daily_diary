## Plans and ideas
 - Use SQLite3 for all data handling, not .csv
 - Build a 'Day' class to handle all the stuff from that day. That way I can pass around all the data in one object rather than calling things randomly. __DAY OBJECT EVERYWHERE, EVEN BETWEEN CLASSES__
 - Build a 'Month' class that will be the container for the day objects of that month. It will have the functions to create the day objects, get specific days, possibly even reveal the calendar itself
 - use a date object throughout the code to keep consistency 
 - Simplistic design, swap between journal and 'progress' (keep track of meeing goals, shown in a calendar format)
   - show journal, not calendar, at start of app
 - should I move some of the GUI aspects to their own classes? like some of the frames or the journal and calendar sections?

## TO DO
 - DONE edit goals function in journal_backend
 - DONE edit goals options in journal_gui
 - DONE deal with increase or decrease of month when changing days
 - edit journal function in journal_backend
 - save day functions in journal_gui 
   - save new journal and daily goal data
   - edit existing journal and daily goal data
 - Sorta Done change month functions
 - select days in calendar functions
 - select goals to view in calendar functions

## Controller actions
 - get currently focused month object
   - populate all the day data forr each day in the month
 - pass needed data to repository to store
 -  






 ## things for base_repository.py
 __possible generic methods__

    def insert(self, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        values = tuple(data.values())
        with self.connect() as cursor:
            cursor.execute(
                f'INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})',
                values
            )
            return cursor.lastrowid

    def update(self, data, conditions):
        set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
        where_clause = ' AND '.join([f"{k} = ?" for k in conditions.keys()])
        values = tuple(data.values()) + tuple(conditions.values())
        with self.connect() as cursor:
            cursor.execute(
                f'UPDATE {self.table_name} SET {set_clause} WHERE {where_clause}',
                values
            )

    def delete(self, conditions):
        where_clause = ' AND '.join([f"{k} = ?" for k in conditions.keys()])
        values = tuple(conditions.values())
        with self.connect() as cursor:
            cursor.execute(
                f'DELETE FROM {self.table_name} WHERE {where_clause}',
                values
            )

    def select(self, columns='*', conditions=None):
        where_clause = ''
        values = ()
        if conditions:
            where_clause = ' WHERE ' + ' AND '.join([f"{k} = ?" for k in conditions.keys()])
            values = tuple(conditions.values())
        with self.connect() as cursor:
            cursor.execute(
                f'SELECT {columns} FROM {self.table_name}{where_clause}',
                values
            )
            return cursor.fetchall()