#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  : jzy
@Contact :  : 905414225@qq.com
@Software: PyCharm
@File    : common_dao.py
@Time    : 2020-08-07 11:11
@Desc    :
@Scene   : 公共表母类
"""

import utils.mysql.mysql_common_util as mysql_util


class common_dao(object):

    def __init__(self,table_name):
        self.table_name = table_name

    common_escape_key = ["page_num","page_size","order_by","mode"]
    # global run_sql 修饰器是先定义的，执行顺序在init之前，因此无法通过传参的形式动态变化
    def select(self,model={"username":"admin","password":"admin","page_num":1,"page_size":10},fields=[],fuzzy_query_key=[],prefix_sql=None,escape_key=[]):
        """
        * params model 检索条件 dict
            * key mode 排序的模式,"asc","desc"
            * key order_by 排序的字段 "create_time","update_time","id",自定义
        * params escape_key 非检索条件所在的key
        * params fields 筛选字段
        * params fuzzy_query_key 模糊查询字段
        * params prefix_sql 自定义前缀的sql

        """
        sql = " select %s from %s " % (",".join(fields) if fields else "*",self.table_name) if not prefix_sql else prefix_sql
        if model:
            query = mysql_util.dict_to_str(model,escape_key=self.common_escape_key if not escape_key else self.common_escape_key+escape_key,fuzzy_query_key=fuzzy_query_key)
            if query: sql +=" {} ".format("where" if "where" not in sql else "and")+ query
            order_by =model.get("order_by",None)
            mode =model.get("mode",None)
            if order_by and mode: sql+=" order by %s %s "%(order_by,mode)
            page_num = model.get("page_num",None)
            page_size = model.get("page_size",None)
            if page_num !=None and page_size:
                begin = ((page_num if page_num>=1 else 1) - 1) * page_size
                sql+=" limit %s,%s" % (begin,page_size)
        return sql

    # @mysql_util.pymysql_time_deal
    # @run_sql(fetch_type="one")
    def select_one(self,model={"username":"admin","password":"admin"},fields=[],fuzzy_query_key=[],prefix_sql=None,escape_key=[]):
        sql = " select %s from %s " % (",".join(fields) if fields else "*",self.table_name) if not prefix_sql else prefix_sql
        if model:
            query = mysql_util.dict_to_str(model,escape_key=self.common_escape_key if not escape_key else self.common_escape_key+escape_key,fuzzy_query_key=fuzzy_query_key)
            if query: sql +=" {} ".format("where" if "where" not in sql else "and")+ query
            order_by =model.get("order_by",None)
            mode =model.get("mode",None)
            if order_by and mode: sql+=" order by %s %s "%(order_by,mode)

        return sql


    # @run_sql(fetch_type=None)
    def update_by_id(self,model={"password":"admin123","id":1},escape_key=["id","user_type","username","company_name"]):
        sql = "update %s " % self.table_name
        if model:
            # escape_key 禁止更改的字段
            sql +=" set "+ mysql_util.dict_to_str(model,join_type=",",escape_key=escape_key)
            sql +=" where id=%s" % ("'"+model["id"]+"'" if type(model["id"])==str else model["id"])
            return sql

    # @run_sql_v2(fetch_type=None)
    def update_by_id_v2(self,model={"password":"admin123","id":1}):
        sql = "update %s " % self.table_name
        if model:
            # escape_key 禁止更改的字段
            sql +=" set "+ mysql_util.dict_to_str_v2(model,join_type=",",escape_key=["id"])
            sql +=" where id=%s "
            args = mysql_util.get_sql_args(model,escape_key=["id"])
            return sql,args


    # @run_sql(fetch_type=None)
    def insert(self,model={"password":"admin123","username":"jzy","user_type":1,"company_name":"赅推科技"}):
        sql = "insert into %s" % self.table_name
        if model:
            ks,vs = mysql_util.dict_to_str_mode_insert(model)
            sql +="(%s) values(%s)"%(ks,vs)
            return sql

    # @run_sql(fetch_type="one")
    def select_total(self,model={"username":"admin","password":"admin","page_num":1,"page_size":10},fuzzy_query_key=[],prefix_sql=None,escape_key=[]):
        sql = " select count(1) as total from %s " % self.table_name if not prefix_sql else prefix_sql
        if model:
            query = mysql_util.dict_to_str(model,escape_key=self.common_escape_key if not escape_key else self.common_escape_key+escape_key,fuzzy_query_key=fuzzy_query_key)
            if query: sql +=" {} ".format("where" if "where" not in sql else "and")+ query
        return sql


    # @run_sql(fetch_type=None)
    def delete_by_id(self,model={"username":"admin","password":"admin","page_num":1,"page_size":10}):
        sql = " delete from %s " % self.table_name
        if model:
            sql +=" where "+ mysql_util.dict_to_str(model,escape_key=self.common_escape_key)
        return sql

    def delete(self,model={"username":"admin","password":"admin","page_num":1,"page_size":10}):
        sql = " delete from %s " % self.table_name
        if model:
            sql +=" where "+ mysql_util.dict_to_str(model,escape_key=self.common_escape_key)
        return sql


    # @run_sql_v2(fetch_type="all")
    def insert_v2(self,model={"text":"奥术大师客单价客单价的卡ad看见爱上大健康","p_id":123123}):
        sql = "insert %s into %s"%("ignore" if type(model)==list else "",self.table_name)
        if model:
            ks,vs = mysql_util.dict_to_insert_sql(model[0] if type(model)==list else model)
            sql +="(%s) values(%s)"%(ks,vs)
            return sql,mysql_util.get_sql_args(model)


    def select_by_ids(self,model={},fields=[]):
        sql = " select %s from %s " % (",".join(fields) if fields else "*",self.table_name)
        if model:
            sql+=" where id in ({})".format(",".join([str(i) for i in model["ids"]]))
            order_by =model.get("order_by",None)
            mode =model.get("mode",None)
            if order_by and mode: sql+=" order by %s %s "%(order_by,mode)
        return sql


if __name__ == '__main__':
    pass
