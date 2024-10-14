# TODO: 
# start logger functions
# call controller
# call gui to build window



import logger
import controller
import gui


def main():
    """ TODO: describe me... """
    
    logger.configure_logger()

    con = controller.JournalController()

    app = gui.JournalGUI(con)
    app.start_gui()


if __name__ == "__main__":
    main()
