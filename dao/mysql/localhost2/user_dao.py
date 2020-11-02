#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  : jzy
@Contact :  : 905414225@qq.com
@Software: PyCharm
@File    : spider_user_info_dao.py
@Time    :
@Desc    :
@Scene   :
"""
import pymysql
from dao.mysql.localhost.pool import run_sql
import utils.mysql.mysql_common_util as mysql_util
from dao.mysql.localhost.pool import common_dao
class user_dao(common_dao):
    """ 用户表相关 """
    table_name = "user"

    def __init__(self):
        super().__init__(table_name=self.table_name)


d = user_dao()
select = d.select
update_by_id = d.update_by_id
insert =d.insert
select_one =d.select_one
select_total = d.select_total

if __name__ == '__main__':
    pass
