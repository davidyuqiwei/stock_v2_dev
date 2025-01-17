'''
该日志类可以把不同级别的日志输出到不同的日志文件中
'''

import os
import sys
import time
import logging
import inspect
from scripts_stock.cfg.set_dir import ProjectDir
import traceback

handlers = {
            logging.NOTSET: os.path.join(ProjectDir.log_dir,"logging.log"),
            logging.DEBUG: os.path.join(ProjectDir.log_dir,"logging.log"),
            logging.INFO: os.path.join(ProjectDir.log_dir,"info.log"),
            logging.WARNING: os.path.join(ProjectDir.log_dir,"logging.log"),
            logging.ERROR: os.path.join(ProjectDir.log_dir,"error.log"),
            logging.CRITICAL: os.path.join(ProjectDir.log_dir,"logging.log")
            }


def createHandlers():
    logLevels = handlers.keys()
    for level in logLevels:
        path = os.path.abspath(handlers[level])
        handlers[level] = logging.FileHandler(path)


# 加载模块时创建全局变量
createHandlers()


class TNLog(object):
    def printfNow(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    def __init__(self, level=logging.NOTSET):
        self.__loggers = {}
        logLevels = handlers.keys()
        logging.basicConfig(level=logging.ERROR)
        for level in logLevels:
            logger = logging.getLogger(str(level))
            # 如果不指定level，获得的handler似乎是同一个handler?
            logger.addHandler(handlers[level])
            logger.setLevel(level)
            self.__loggers.update({level: logger})

    def getLogMessage(self, level, message):
        frame, filename, lineNo, functionName, code, unknowField = inspect.stack()[2]
        '''日志格式：[时间] [类型] [记录代码] 信息'''
        return "[%s] [%s] [%s - %s - %s] %s" % (self.printfNow(), level, filename, lineNo, functionName, message)

    def info(self, message):
        message = self.getLogMessage("info", message)
        self.__loggers[logging.INFO].info(message)

    def error(self, message):
        message = self.getLogMessage("error", message)
        self.__loggers[logging.ERROR].error(message)

    def warning(self, message):
        message = self.getLogMessage("warning", message)
        self.__loggers[logging.WARNING].warning(message)

    def debug(self, message):
        message = self.getLogMessage("debug", message)
        self.__loggers[logging.DEBUG].debug(message)

    def critical(self, message):
        message = self.getLogMessage("critical", message)
        self.__loggers[logging.CRITICAL].critical(message)


def print_exception_info():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print("Exception Type:", exc_type)
    print("Exception Message:", exc_value)

    # 获取回溯对象中的帧列表
    tb_frames = traceback.extract_tb(exc_traceback)

    for frame in tb_frames:
        filename, line_number, function_name, text = frame
        print(
            f'File: {filename}, Line: {line_number}, In Function: {function_name}')
        print(f'  {text}')


if __name__ == "__main__":
    # logger = TNLog()
    # logger.debug("debug")
    # logger = TNLog()
    # logger.info("info")
    # logger = TNLog()
    # logger.warning("warning")
    logger = TNLog()
    logger.error("error")
    logger = TNLog()
    logger.error("data is blank")
    # logger = TNLog()
    # logger.critical("critical")
