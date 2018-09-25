import logging
import os
import datetime


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(object, metaclass=Singleton):
    _logger = None

    def __init__(self):
        self._logger = logging.getLogger("log-processor")
        self._logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s \t [%(levelname)s | %(filename)s:%(lineno)s] > %(message)s')

        now = datetime.datetime.now()
        dir_name = "./log"

        if not os.path.isdir(dir_name):
            os.mkdir(dir_name)
        file_handler = logging.FileHandler(dir_name + "/log_"
                                           + now.strftime("%Y-%m-%d")+".log")

        stream_handler = logging.StreamHandler()

        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        self._logger.addHandler(file_handler)
        self._logger.addHandler(stream_handler)

    def get_logger(self):
        return self._logger
