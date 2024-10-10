import logging
from logging.handlers import RotatingFileHandler
from config import LOG_FILE

class AppLogger:
    def __init__(self, max_bytes: int = 5*1024*1024, backup_count: int = 5):
        self.log_file = LOG_FILE
        self.logger = logging.getLogger(self.log_file)
        self.logger.setLevel(logging.DEBUG)
        
        # creates rotating file handler
        handler = RotatingFileHandler(self.log_file, maxBytes=max_bytes, backupCount=backup_count)

        # log formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # adding handler
        if not self.logger.hasHandlers(): # keep from having multiple handlers
            self.logger.addHandler(handler)

    def debug(self, message: str):
        self.logger.debug(message)

    def info(self,message: str):
        self.logger.info(message)
        
    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)
    
    def critical(self, message: str):
        self.logger.critical(message)