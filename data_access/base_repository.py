import sqlite3
from contextlib import contextmanager
from config import DATABASE_NAME, DEBUG
from typing import *
from utils.app_logger import AppLogger

class BaseRepository:
    def __init__(self):
        self.db_name = DATABASE_NAME

        # get logger instance
        self.logger = AppLogger()

        #set the debugging value (true will log debug messages)
        self.debugger = DEBUG

    # connection manager, to be used in 'with' statements
    @contextmanager
    def cursor(self):
        conn = sqlite3.connect(self.db_name)
        try:
            cursor = conn.cursor()
            yield cursor
            conn.commit()
        except sqlite3.IntegrityError as e:
            conn.rollback()
            self.logger.error(f'sqlite error: {e}')
        except Exception as e:
            conn.rollback()
            self.logger.error(f'Error at: {e}')
            raise
        finally:
            conn.close()

    # basic insert function. Does not return anything. Takes a list of the columns needed, and a list of tuples
    def insert(self, table: str, columns: list, values: list[tuple]):
        columns_str = ', '.join(columns)
        placeholders = ', '.join(['?'] * len(columns))
        query = f'INSERT INTO {table} ({columns_str}) VALUES ({placeholders})'

        if self.debugger:
            self.logger.debug(f'Inserting with query: {query}, and values {values}')

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

        if self.debugger:
            self.logger.debug(f'selecting with query: SELECT {columns_str} FROM {table} {where_clause}, and values {values}')

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

        if self.debugger:
            self.logger.debug(f'deleting with query: DELETE FROM {table} WHERE {where_clause}, and values {values}')

        with self.cursor() as cursor:
            cursor.execute(f'DELETE FROM {table} WHERE {where_clause}', values)

    # basic update function
    def update(self, table: str, conditions: dict, data: dict):
        set_clause = ', '.join([f'{key} = ?' for key in data.keys()])
        where_clause = ' AND '.join([f'{key} = ?' for key in conditions.keys()])
        values = tuple(data.values()) + tuple(conditions.values())

        if self.debugger:
            self.logger.debug(f'updating with query: UPDATE {table} SET {set_clause} WHERE {where_clause}, and values {values}')

        with self.cursor() as cursor:
            cursor.execute(f'UPDATE {table} SET {set_clause} WHERE {where_clause}', values)