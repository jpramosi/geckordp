from pathlib import Path
from geckordp.logger import *
# pylint: disable=invalid-name


class Settings():
    """ Global settings for geckordp.
    """ 

    def __init__(self):
        self.__XDEBUG = 0
        self.__XDEBUG_EVENTS = 0
        self.__XDEBUG_REQUEST = 0
        self.__XDEBUG_RESPONSE = 0
        self.__XLOG_FILE = ""

    @property
    def DEBUG(self) -> int:
        """ Sets geckordp in debug mode.
        Environment variable: GECKORDP_DEBUG

        Returns:
            int: 0: disabled, 1: enabled
        """
        return self.__XDEBUG

    @DEBUG.setter
    def DEBUG(self, value: int):
        if (type(self.__XDEBUG) != type(value)):
            print(f"invalid value '{value}' for 'DEBUG'")
            return
        set_stdout_log_level(logging.DEBUG)
        self.__XDEBUG = value

    @property
    def DEBUG_EVENTS(self) -> int:
        """ Logs all received events.
        Environment variable: GECKORDP_DEBUG_EVENTS

        Returns:
            int: 0: disabled, 1: enabled
        """
        return self.__XDEBUG_EVENTS

    @DEBUG_EVENTS.setter
    def DEBUG_EVENTS(self, value: int):
        if (type(self.__XDEBUG_EVENTS) != type(value)):
            print(f"invalid value '{value}' for 'DEBUG_EVENTS'")
            return
        self.__XDEBUG_EVENTS = value

    @property
    def DEBUG_REQUEST(self) -> int:
        """ Logs all received events.
        Environment variable: GECKORDP_DEBUG_REQUEST

        Returns:
            int: 0: disabled, 1: enabled
        """
        return self.__XDEBUG_REQUEST

    @DEBUG_REQUEST.setter
    def DEBUG_REQUEST(self, value: int):
        if (type(self.__XDEBUG_REQUEST) != type(value)):
            print(f"invalid value '{value}' for 'DEBUG_REQUEST'")
            return
        self.__XDEBUG_REQUEST = value

    @property
    def DEBUG_RESPONSE(self) -> int:
        """ Logs all received events.
        Environment variable: GECKORDP_DEBUG_RESPONSE

        Returns:
            int: 0: disabled, 1: enabled
        """
        return self.__XDEBUG_RESPONSE

    @DEBUG_RESPONSE.setter
    def DEBUG_RESPONSE(self, value: int):
        if (type(self.__XDEBUG_RESPONSE) != type(value)):
            print(f"invalid value '{value}' for 'DEBUG_RESPONSE'")
            return
        self.__XDEBUG_RESPONSE = value

    @property
    def LOG_FILE(self) -> str:
        """ Write logs to file.
        Environment variable: GECKORDP_LOG_FILE

        Returns:
            str: "": disabled, "xyz.log": enabled
        """
        return self.__XLOG_FILE

    @LOG_FILE.setter
    def LOG_FILE(self, value: str):
        if (type(self.__XLOG_FILE) != type(value)):
            print(f"invalid value '{value}' for 'LOG_FILE'")
            return
        self.__XLOG_FILE = value
        set_file_logger(Path(self.__XLOG_FILE).absolute())


GECKORDP = Settings()
init_logger(logging.ERROR)
