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
import utils.decorator_util as decorator_util
class user_service:

    @decorator_util.decorator_none
    def do_login(self,text_json):
        users = user_dao.select(model={"username":text_json["username"],"password":text_json["password"],"status":0})
        if not users:return {"code":10001}
        else: return users[0]


    def update_user(self,text_json):
        res = user_dao.update_by_id(model=text_json)
        return res

    def select_users(self,text_json):
        data = user_dao.select(model=text_json,fields=["id","username","create_time"])
        total = user_dao.select_total(model=text_json)
        return {"total":total["total"],"data":data,"page_num":text_json["page_num"],"page_size":text_json["page_size"]}

    def test_group(self,text_json):
        data = user_dao.test_group1()
        # 或 data = user_dao.test_group2()
        return data




if __name__ == '__main__':
    pass