import logging


def create_logger(file_name: str, log_name: str, log_level=logging.INFO):
    formatter = logging.Formatter(
        fmt="[%(asctime)s] %(levelname)s: %(message)s", datefmt="%d.%m.%Y %H:%M:%S"
    )

    handler = logging.FileHandler(file_name)
    handler.setFormatter(formatter)

    logger = logging.getLogger(log_name)
    logger.setLevel(log_level)

    logger.addHandler(handler)

    return logger
