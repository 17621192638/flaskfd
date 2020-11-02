#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  : jzy
@Contact :  : 905414225@qq.com
@Software: PyCharm
@File    : decorator_util.py
@Time    : 2019/1/16 18:08
@Desc    : 装饰器类
@Scene   : 追溯异常状态
"""
import traceback,datetime,time

def decorator_none_list(fn):
    """
    返回为none时,修饰为[]
    :param fn:被修饰的方法体
    :return:
    """
    def wrapper(*args, **kwargs):
        try:
            res = fn(*args, **kwargs)
            return res if res else []
        except Exception as e:
            traceback.print_exc()
            # error_msg = "{0} - decorator_util - {1} - {2}".format(utils.get_current_time(), str(e),
            #                                                      str(traceback.format_exc()))
            # utils.write(service_error_log_path, error_msg)
            return []
    return wrapper

def decorator_none_list_no_save(fn):
    """
    返回为none时,修饰为[]
    :param fn:被修饰的方法体
    :return:
    """
    def wrapper(*args, **kwargs):
        try:
            res = fn(*args, **kwargs)
            return res if res else []
        except Exception as e:
            traceback.print_exc()
            return []
    return wrapper



def decorator_none(fn):
    """
    捕获方法异常,并返回None
    :param fn:被修饰的方法体
    :return:
    """
    def wrapper(*args, **kwargs):
        try:
            res = fn(*args, **kwargs)
            return res
        except Exception as e:
            traceback.print_exc()
            return None
    return wrapper

def decorator_none_print(fn):
    """
    捕获方法异常,并返回None，不保存只输出异常
    :param fn:被修饰的方法体
    :return:
    """
    def wrapper(*args, **kwargs):
        try:
            res = fn(*args, **kwargs)
            return res
        except Exception as e:
            traceback.print_exc()
            return None
    return wrapper


def decorator_none_no_print_no_save(fn):
    """
    捕获方法异常,并返回None，不保存只输出异常
    :param fn:被修饰的方法体
    :return:
    """
    def wrapper(*args, **kwargs):
        try:
            res = fn(*args, **kwargs)
            return res
        except Exception as e:
            return None
    return wrapper


def decorator_False(fn):
    """
    捕获方法异常,并返回False
    :param fn:被修饰的方法体
    :return:
    """
    def wrapper(*args, **kwargs):
        try:
            res = fn(*args, **kwargs)
            return res
        except Exception as e:
            traceback.print_exc()
            return False
    return wrapper

def pymysql_time_deal(fn):
    """
    时间格式处理类,默认mysql返回的是datetime.datetime GMT格式
    :param fn:被修饰的方法体
    :return:
    """
    def wrapper(*args, **kwargs):
        res = fn(*args, **kwargs)
        if res:
            if type(res)==dict:
                for key in res.keys():
                    if type(res[key])==datetime.datetime:
                        res[key]= str(res[key])
            elif type(res)==list:
                for model in res:
                    for key in model.keys():
                        if type(model[key]) == datetime.datetime:
                            model[key] = str(model[key])
            return res
        else:
            return res
    return wrapper


def decorator_timeout_print(fn):
    """
    时间计时器
    :param fn:被修饰的方法体
    :return:
    """
    def wrapper(*args, **kwargs):
        try:
            time1 = time.time()
            res = fn(*args, **kwargs)
            time2 = time.time()
            timeout = '%.3f' % (time2 - time1)
            print("任务时间：{0}".format(timeout))
            return res
        except Exception as e:
            traceback.print_exc()
            return False
    return wrapper