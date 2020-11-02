#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  : jzy
@Contact :  : 905414225@qq.com
@Software: PyCharm
@File    : logger_util.py
@Time    : 2020-06-04 13:29
@Desc    : log工具类
@Scene   :
介绍 https://www.cnblogs.com/huaizhi/p/11245246.html
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')
"""

import logging.handlers
import logging,os
from logging.handlers import TimedRotatingFileHandler

def get_logger(logger_name=__file__,file_path=None,use_console_handler =True,use_file_handler=True,when="D"):
    """
    文件名作为 logger_name
    """
    logger = logging.getLogger(logger_name)

    logger.setLevel(logging.DEBUG)
    """
    formatter参数
    * levelname : 日志级别
    * thread : 线程号
    * filename: 打印日志的文件名
    * message: 信息
    * name: 自定义的logger名称
    """
    formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(thread)s:%(name)s_|_%(message)s", "%Y-%m-%d %H:%M:%S")

    if use_console_handler:
        handler_console = logging.StreamHandler()
        handler_console.setLevel(logging.DEBUG)
        handler_console.setFormatter(formatter)
        logger.addHandler(handler_console)


    if use_file_handler: # 是否使用文件输出流
        dir_name = os.path.dirname(file_path)
        if not os.path.exists(dir_name): os.mkdir(dir_name)
        # 每隔1天写一个日志文件
        handler_file = TimedRotatingFileHandler(filename=file_path,encoding="utf-8", when=when, interval=1, backupCount=10)
        # handler_file = logging.FileHandler(filename=file_path,encoding="utf-8")
        handler_file.setLevel(logging.DEBUG)
        handler_file.setFormatter(formatter)
        logger.addHandler(handler_file)
    return logger

def disable_logger(logger):
    """禁用当前 logger,不会输出和打印日志"""
    logger.disabled = True



if __name__ == '__main__':
    logger= get_logger(logger_name=__file__,file_path="./test.log")
    logger.info("哈哈哈{} {}","323","121")



