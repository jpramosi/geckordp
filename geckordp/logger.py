import logging
from pathlib import Path
from json import dumps


LOGGER_NAME = "geckordp"
__STDOUT_HANDLER = None
__FILE_HANDLER = None
log = logging.getLogger(LOGGER_NAME).info
dlog = logging.getLogger(LOGGER_NAME).debug
elog = logging.getLogger(LOGGER_NAME).error
wlog = logging.getLogger(LOGGER_NAME).warning
clog = logging.getLogger(LOGGER_NAME).critical
exlog = logging.getLogger(LOGGER_NAME).exception


def init_logger(log_level=logging.ERROR):
    global __STDOUT_HANDLER
    if (__STDOUT_HANDLER != None):
        return

    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG)

    __STDOUT_HANDLER = logging.StreamHandler()
    __STDOUT_HANDLER.setLevel(log_level)
    __STDOUT_HANDLER.setFormatter(logging.Formatter(
        f'%(asctime)s [{LOGGER_NAME}][%(levelname)s] - %(funcName)s(): %(message)s'))
    logger.addHandler(__STDOUT_HANDLER)


def set_file_logger(log_path: Path, log_level=logging.DEBUG):
    global __FILE_HANDLER
    if (log_path == ""):
        return

    logger = logging.getLogger(LOGGER_NAME)
    log_file = str(Path(log_path))
    try:
        open(log_file, 'w').close()
    except:
        pass

    if (__FILE_HANDLER != None):
        logger.removeHandler(__FILE_HANDLER)
    __FILE_HANDLER = logging.FileHandler(log_file)
    __FILE_HANDLER.setLevel(log_level)
    __FILE_HANDLER.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] [%(module)s.py:%(lineno)s in %(funcName)s] - %(message)s'))
    logger.addHandler(__FILE_HANDLER)


def set_file_log_level(log_level=logging.DEBUG):
    if (__FILE_HANDLER == None):
        raise RuntimeError(
            "file logger was not initialized with 'set_file_logger()'")
    __FILE_HANDLER.setLevel(log_level)


def set_stdout_log_level(log_level=logging.DEBUG):
    assert __STDOUT_HANDLER != None
    __STDOUT_HANDLER.setLevel(log_level)


def logdict(dict_obj):
    log(dumps(dict_obj, indent=2))
