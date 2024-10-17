<<<<<<< Updated upstream
# TODO: 
# start logger functions
# call controller
# call gui to build window

=======
import logger
import controller
>>>>>>> Stashed changes
import tkinter as tk

import controller
import logger
from repository import GoalsRepository, EntriesRepository
from config import WINDOW_SIZE, WINDOW_RESIZEABLE


def main():
    """ This module starts the logger, initializes the tkinter window, initializes the controller,
     then starts the tkinter mainloop """
    logger.configure_logger()

    root = tk.Tk()

    root.geometry(f'{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}+{WINDOW_SIZE[2]}+{WINDOW_SIZE[3]}')
    root.resizable(WINDOW_RESIZEABLE[0],WINDOW_RESIZEABLE[1])
    root.title("Daily Journal")

    app = controller.JournalController(
        goals_repo=GoalsRepository(),
        entries_repo=EntriesRepository(),
        root=root
    )

    root.mainloop()


if __name__ == "__main__":
    main()
