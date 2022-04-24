"""To be refactored to use pathlib """


import logging
import os
import sys

from logging.handlers import TimedRotatingFileHandler


class CustomFormatter(logging.Formatter):
    """Custom formatter, overrides funcName with value of name_override if it exists
    Source: https://stackoverflow.com/questions/7003898/using-functools-wraps-with-a-logging-decorator
    """

    def format(self, record):
        if hasattr(record, "name_override"):
            record.funcName = record.name_override
        return super(CustomFormatter, self).format(record)


def log_setup(
    parent_dir,
    log_filename,
    logger_level,
    log_stdout: bool = True,
    log_name: str = None,
) -> logging.Logger:
    """Setup the logger to output both in ./logs/ directory and stdout at the same time."""
    # Set up logging directory, if necessary
    if not os.path.exists(parent_dir + "/logs"):
        os.makedirs(parent_dir + "/logs/")
    log_filename_path = parent_dir + "/logs/{}.log".format(log_filename)

    # Setting log format
    log_format: str = "%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(funcName)s - %(message)s"
    formatter = CustomFormatter(fmt=log_format, datefmt="%Y-%m-%d %I:%M:%S %p")

    # Start setup of logger
    logger: logging.Logger = logging.getLogger(
        log_name
    ) if log_name else logging.getLogger()
    logger.setLevel(logger_level)

    # Create Time Rotating File handler with logging level at INFO
    handler = TimedRotatingFileHandler(
        log_filename_path, when="midnight", backupCount=10
    )
    handler.setFormatter(formatter)
    handler.suffix = "_%Y-%m-%d_%H%M%S.log"
    logger.addHandler(handler)

    if log_stdout:
        # Create console handler with logging level at INFO
        console = logging.StreamHandler(sys.stdout)
        console.setLevel(logger_level)
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger
