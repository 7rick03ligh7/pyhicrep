import logging
import traceback
import sys


def configure_logging(log_file="./logfile.log",
                      log_level=logging.DEBUG,
                      stdout=False):
    handlers = []
    if log_file:
        handler = logging.FileHandler(filename=log_file,
                                      mode="w+")
        handlers.append(handler)
    if stdout:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        handlers.append(handler)

    logging.basicConfig(level=log_level,
                        format="%(asctime)-15s %(levelname)-8s %(message)s",
                        handlers=handlers)


def log(func):
    """ Decorator """
    def call(*args, **kwargs):
        """ Actual wrapping """
        indent = "-" * len(traceback.extract_stack())
        logging.debug(f"{indent} ENTER %s", func.__name__)
        result = func(*args, **kwargs)
        logging.debug(f"{indent} EXIT %s", func.__name__)
        return result
    return call
