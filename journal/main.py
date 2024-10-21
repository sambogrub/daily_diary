import logger
import controller
import tkinter as tk
import sqlite3
from contextlib import contextmanager

import controller
import logger
from repository import GoalsRepository, EntriesRepository
from config import WINDOW_SIZE, WINDOW_RESIZEABLE, DATABASE_NAME

def main():
    """ This module starts the logger, initializes the tkinter window, initializes the controller,
        initializes the db connection manager, then starts the tkinter mainloop """
    logger.configure_logger()

    log = logger.journal_logger()
    db_conn = journal_db_connection()
   
    root = tk.Tk()
    root.geometry(f'{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}+{WINDOW_SIZE[2]}+{WINDOW_SIZE[3]}')
    root.resizable(WINDOW_RESIZEABLE[0],WINDOW_RESIZEABLE[1])
    root.title("Daily Journal")

    with sqlite_cursor(log,db_conn) as cursor:
        app = controller.JournalController(
            goals_repo=GoalsRepository(cursor),
            entries_repo=EntriesRepository(cursor),
            root=root
        )

    root.mainloop()

# retreive the db connection
def journal_db_connection(database_name: str = DATABASE_NAME) -> sqlite3.Connection:
    """ Function provides a sqlite3.Connection for the Journal DB. """
    return sqlite3.connect(database_name)

 # connection manager, to be used in 'with' statements
@contextmanager
def sqlite_cursor(logger,conn):
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except sqlite3.IntegrityError as e:
        conn.rollback()
        logger.exception('SQLite error: %s', e)
    except Exception as e:
        conn.rollback()
        logger.exception('Error at: %s', e)
        raise
    # I'm unsure if this needs to still be implemented
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
