#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  : jzy
@Contact :  : 905414225@qq.com
@Software: PyCharm
@File    : hanlp_util.py
@Time    : 2019/5/29 15:40
@Desc    :
@Scene   : Hanlp相关的操作
如果要在多台机器都配置hanlp,在复制完 data后，记得修改 hanlp.properties中的root的值为当前引用路径
"""
from pyhanlp import *
import os
# Hanlp初始启动JVM占用内存大小
os.environ["HANLP_JVM_XMS"] = "1g"
print("HANLP_JVM_XMS {0}".format( "1g"))
# Hanlp最大占用JVM内存大小
os.environ["HANLP_JVM_XMX"] = "4g"
print("HANLP_JVM_XMX {0}".format("4g"))

from utils import common_util as utils

class hanlp_util(object):
    # ----   通过感知机 进行分词和词性标注 ---------------
    stopwords = utils.read(os.path.dirname(__file__) + "/stopwords.txt")
    perceptron_analyzer = PerceptronLexicalAnalyzer()

    def cut_by_perceptron(self,text,filter_punctuation=True,filter_stopwords=True):
        """通过感知机 进行分词和词性标注"""
        # 实测效果 感知机模式下 不用空格分隔的效果更好
        text = utils.pick_valid_text(text,sep="")
        res = self.perceptron_analyzer.analyze(text)
        res = res.toWordTagArray()
        datas =[ data for data in zip(res[0], res[1])]
        if filter_punctuation: datas =[ data for data in  datas if data[1]!="w" ]
        if filter_stopwords: datas =[ data for data in  datas if data[0].strip() not in self.stopwords ]
        return datas
    

    def cut_by_default(self,text):
        """通过一般分词 进行分词和词性标注"""
        res = HanLP.segment(text)
        datas = [(data.word,str(data.nature)) for data in res]
        return datas


    def pick_keywords(self, content,res_num):
        """提取关键词"""
        keywords = HanLP.extractKeyword(content,res_num)
        return [keyword for  keyword in keywords if len(keyword)>1]


    def extract_summary(self, content, res_num):
        """提取摘要"""
        return HanLP.extractSummary(content, res_num)


    CustomDictionary = SafeJClass("com.hankcs.hanlp.dictionary.CustomDictionary")
    def load_dict(self,words):
        """加载自定义词库"""
        # CustomDictionary.insert("饿了么", "nz 1024")  # 强行插入 词性 权重
        # #CustomDictionary.remove("攻城狮"); # 删除词语（注释掉试试）
        # CustomDictionary.add("单身狗", "nz 1024 n 1")  # 多个词性
        [ self.CustomDictionary.add(word,"nz 1024") for word in words if word ]
        print("加载自定义词典完成")

s = hanlp_util()
load_dict = s.load_dict
extract_summary= s.extract_summary
pick_keywords=s.pick_keywords
cut_by_default=s.cut_by_default
cut_by_perceptron=s.cut_by_perceptron
stopwords = s.stopwords
if __name__ == '__main__':
    # res = service.pick_keywords("孙宇晨怼王思聪",res_num=10)
    res = cut_by_default("甜的不太行​")
    # print(res)
    # load_dict(["孙宇晨"])
    # res = cut_by_perceptron("甜的不太行​")
    print(res)
    # 多进程冲突
    # from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
    # with ThreadPoolExecutor(max_workers=5) as thread_pool:
    #     all_task = thread_pool.map(cut_by_perceptron, ["孙宇晨怼王思聪" for i in range(10)])
    #     for i in all_task:
    #         print(i)

