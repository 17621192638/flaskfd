#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  : jzy
@Contact :  : 905414225@qq.com
@Software: PyCharm
@File    : user_service.py
@Time    : 2020-07-25 18:44
@Desc    :
@Scene   :
"""
import dao.mysql.localhost.user_dao as user_dao
import utils.common_util as common_util


class user_service:

    def do_login(self,text_json):
        users = user_dao.select(model={"username":text_json["username"],"password":text_json["password"],"status":0})
        if not users:return {"code":10001}
        else: return users[0]


    def update_user(self,text_json):
        res = user_dao.update_by_id(model=text_json)
        return res

    def select_users(self,text_json):
        if text_json.get("page_num",None)==None:return {"total":0,"data":None,"page_num":0,"page_size":0}
        data = user_dao.select(model=text_json,fuzzy_query_key=self.fuzzy_query_key)
        total = user_dao.select_total(model=text_json,fuzzy_query_key=self.fuzzy_query_key)
        return {"total":total["total"],"data":data,"page_num":text_json["page_num"],"page_size":text_json["page_size"]}





if __name__ == '__main__':
    pass