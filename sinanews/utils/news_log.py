#!/usr/bin/env python2.7
#coding=utf-8
import logging
import logging.handlers

def getlogger():
    log_path = '/var/log/news/server.log'
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        handler = logging.handlers.TimedRotatingFileHandler(log_path, 'D')
        # fmt = logging.Formatter(“%(asctime)s – %(pathname)s – %(filename)s – %(funcName)s – %(lineno)s – %(levelname)s – %(message)s”, “%Y-%m-%d %H:%M:%S”)
        fmt = logging.Formatter("%(asctime)s – %(pathname)s – %(filename)s – %(funcName)s – %(lineno)s – %(levelname)s – %(message)s")
        handler.setFormatter(fmt)
        logger.addHandler(handler)
    return logger

