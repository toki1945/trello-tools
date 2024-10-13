#!/usr/bin/env python3
import logging
from logging.handlers import RotatingFileHandler
import os


class Commonlogger:
    def __init__(self, name):
        self.name = name

    def setup(self):
        # ログディレクトリ作成
        LOG_DIR = os.path.join(os.getcwd(), "log")
        if not os.path.exists(LOG_DIR):
            os.mkdir(LOG_DIR)
            print(f"#### create {LOG_DIR} ")

        logger = logging.getLogger(self.name)
        logger.setLevel(logging.DEBUG)
        stream_handler = logging.StreamHandler()
        logfile_handler = RotatingFileHandler(filename=f"{LOG_DIR}/{self.name}.log", encoding="utf-8",
                                            maxBytes=1000000,
                                            backupCount=10)
        logfile_handler.setLevel(logging.INFO)
        log_format = '%(levelname)s : %(asctime)s : %(message)s'
        formatter = logging.Formatter(log_format)
        stream_handler.setFormatter(formatter)
        logfile_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        logger.addHandler(logfile_handler)

        return logger
