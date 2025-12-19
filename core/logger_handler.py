import logging.handlers
import os

import settings

formatter = logging.Formatter(settings.LOGS_FORMAT)

project_logger = logging.getLogger("novelservice_logger")
project_logger.setLevel(settings.LOGS_LEVEL)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
project_logger.addHandler(console_handler)

if settings.LOGS_DIR:
    log_file_path = os.path.join(settings.LOGS_DIR, "novelservice.log")
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=log_file_path,
        when="midnight",
        interval=1,
        backupCount=15,
        encoding="UTF-8"
    )
    file_handler.setFormatter(formatter)
    project_logger.addHandler(file_handler)


def get_logger() -> logging.Logger:
    return project_logger
