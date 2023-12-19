"""
logger.py

This module defines a utility function for creating a logger with file output.
"""

import logging


def create_logger(file_name: str, log_name: str, log_level=logging.INFO):
    """
    Create and configure a logger with file output.

    Args:
        file_name (str): The name of the log file.
        log_name (str): The name of the logger.
        log_level (int): The logging level (default is logging.INFO).

    Returns:
        logging.Logger: The configured logger.
    """
    formatter = logging.Formatter(
        fmt="[%(asctime)s] %(levelname)s: %(message)s", datefmt="%d.%m.%Y %H:%M:%S"
    )

    handler = logging.FileHandler(file_name)
    handler.setFormatter(formatter)

    logger = logging.getLogger(log_name)
    logger.setLevel(log_level)

    logger.addHandler(handler)

    return logger
