#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  : jzy
@Contact :  : 905414225@qq.com
@Software: PyCharm
@File    : conf_util.py
@Time    : 2019/6/19 15:03
@Desc    :
@Scene   : 静态配置加载类
"""
from faker import Faker
import random
class faker_util():
    fake=Faker(locale='zh_CN')

    lats=[
        # 北京
        (116.435691,39.893917),
        (116.360681,39.981516),
        (116.831093,40.369179),
        (116.360566,39.981552),
        (116.190008,39.876282),
        (116.283546,39.856128),
        (116.42633,39.917461),
        (116.534897,39.917134),
        (116.358667,39.955296),
        (116.594926,40.048833),
        (116.421841,40.042816),
    ]

    def get_phone(self):
        return self.fake.phone_number()

    def func_list(self):
        return dir(self.fake)


    def get_log_and_lat(self):
        return self.lats[random.randint(0,self.lats.__len__()-1)]
        # return self.fake.longitude(), self.fake.latitude() 坐标太离谱


    def get_phone_model(self):
        """手机型号"""
        models=  ["Z3","L6i","W375"
                  "N7360","N6080","N6270","E50",
                  "X568","E208",
                  "K510c","Z558c",
                  "Redmi Note8","realme Q","Redmi Note 8 Pro","realme X2","nova 5z","Redmi K30 4G","Redmi K30 5G",
                  "Redmi K20 Pro","realme X2 Pro","Redmi K20 Pro","OPPO Reno Ace","V30 PRO 5G","Mate 30 4G",
                  "P30 Pro","Galaxy S10+"
                  ]
        return models[random.randint(0,models.__len__()-1)]


f=faker_util()
get_phone = f.get_phone
func_list=f.func_list
get_phone_model=f.get_phone_model
get_log_and_lat=f.get_log_and_lat
if __name__ == '__main__':
    print(get_log_and_lat())


