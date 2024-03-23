import logging
import inspect
import os
from logging.handlers import RotatingFileHandler

import absl.logging

logging.root.removeHandler(absl.logging._absl_handler)
absl.logging._warn_preinit_stderr = False


def get_logger():
    logger = logging.getLogger("code_generator_logger")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s:%(name)s:%(levelname)s:%(pathname)s:%(funcName)s:%(lineno)d:%(message)s"
    )

    file_handler = logging.handlers.RotatingFileHandler(
        os.path.join("log_dir", "full_logs.txt"),
        mode="a",
        maxBytes=1000000,
        backupCount=2,
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    error_file_handler = logging.FileHandler(os.path.join("log_dir", "errors.txt"))

    error_file_handler.setFormatter(formatter)
    error_file_handler.setLevel(logging.ERROR)

    logger.addHandler(file_handler)
    logger.addHandler(error_file_handler)

    return logger


class CodeGenLogger:
    lgr = get_logger()
