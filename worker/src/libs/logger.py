import logging
import os
from datetime import datetime


class Logger:
    LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../logs")
    os.makedirs(LOG_DIR, exist_ok=True)

    @staticmethod
    def get_log_file():
        return os.path.join(Logger.LOG_DIR, datetime.now().strftime("%Y%m%d.out"))

    @staticmethod
    def get_logger():
        logger = logging.getLogger("CustomLogger")
        logger.setLevel(logging.INFO)

        log_path = Logger.get_log_file()
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)

        if logger.hasHandlers():
            logger.handlers.clear()

        logger.addHandler(file_handler)
        return logger

    @staticmethod
    def log(level, message):
        logger = Logger.get_logger()
        if not isinstance(message, str):
            message = str(message)

        if level.lower() == "info":
            logger.info(message)
        elif level.lower() == "warning":
            logger.warning(message)
        elif level.lower() == "error":
            logger.error(message)
        elif level.lower() == "debug":
            logger.debug(message)
        else:
            logger.info(message)

        print(message)
