#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  : jzy
@Contact :  : 905414225@qq.com
@Software: PyCharm
@File    :
@Time    :
@Desc    :
@Scene   :
"""
from flask_restful import Resource, request
from  service.user_service import  user_service
import utils.response_util as response_util
service =user_service()
class do_login(Resource):
    @response_util.response_filter_v2
    def post(self):
        text_json = request.get_json()
        return service.do_login(text_json)


class update_user(Resource):
    """更新用户信息"""
    @response_util.response_filter_v2
    def post(self):
        text_json = request.get_json()
        return service.update_user(text_json)


class select_users(Resource):
    """查询用户信息"""
    @response_util.response_filter_v2
    def post(self):
        text_json = request.get_json()
        return service.select_users(text_json)


class test_group(Resource):
    @response_util.response_filter_v2
    def post(self):
        text_json = request.get_json()
        return service.test_group(text_json)


