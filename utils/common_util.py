
import datetime,re,time,os
import hashlib,uuid,json


class time_util(object):

    def get_current_time(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def format_int_to_time(self,tss1 ="1594778574970" ):
        return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(tss1[0:10])))
    def get_current_time_10(self):
        return datetime.datetime.now().strftime('%Y-%m-%d')

    def format_time_to_int(self,tss1='2020-07-08 18:27:00'):
        """
        将固定时间戳转换为数值 1594204020
        当前时间 int(time.time())
        """
        return int(time.mktime(time.strptime(tss1, "%Y-%m-%d %H:%M:%S")))

t1 = time_util()
get_current_time = t1.get_current_time
get_current_time_10 = t1.get_current_time_10
format_time_to_int = t1.format_time_to_int
format_int_to_time = t1.format_int_to_time

class text_util:
    """文本处理工具类"""
    def get_MD5(self,text):
        """获取MD5编码后的内容"""
        return hashlib.md5(str(text).lower().encode("utf-8")).hexdigest()

    def get_uuid(self,sep=""):
        return re.sub('-', sep, str(uuid.uuid1()))

    def filter_punctuation_mark(self,text,sep=""):
        """
        jieba 文本处理:过滤文章中的标点符号以及特殊字符、空格
        :param text:
        :return:
        """
        return re.sub("[《》;；<>【】,\[\]\.、。，:~!！/、?？@#$%^&*()+_\-：“”\"{}'…\s]", sep, str(text).lower())

    def filter_number_and_punctuation_mark(self, text,sep=""):
        """
        jieba 文本处理:过滤文章中的标点符号以及特殊字符、空格、数字
        :param text:
        :return:
        """
        return re.sub("[,\[\]\.、。，:~!！?？@#$%^&*()+_：“”\"''…\s0-9]", sep, str(text).lower())


    def get_json_string(self,text):
        """将内容转换为jsonstring"""
        return json.dumps(text,ensure_ascii=False)


    def filter_blank(self,text):
        """
        jieba 文本处理:过滤文本空格
        :param text:
        :return:
        """
        return re.sub("\s", '', str(text))

    def pick_valid_text(self,text,sep=" "):
        """
        文本处理 仅提取中英文数字内容，排除表情、标点、空格符
        """
        rules = "[^\u4e00-\u9fff0-9A-Za-z]+"
        return re.sub(rules,sep,str(text).lower())


t= text_util()
get_MD5=t.get_MD5
filter_punctuation_mark =t.filter_punctuation_mark
filter_number_and_punctuation_mark =t.filter_number_and_punctuation_mark
get_uuid =t.get_uuid
get_json_string=t.get_json_string
filter_blank=t.filter_blank
pick_valid_text= t.pick_valid_text

class file_util:
    """文本处理工具类"""
    # ------------------------------------------------------文档处理--------------------------------------------------------
    # 写入文档, a 追加写入, w 清空后添加记录, r 阅读
    def write(self, path, text,mode="a"):
        with open(path, mode, encoding='utf-8') as f:
            f.writelines(text)
            f.write('\n')

    def write_list2txt(self, path, words,mode="a"):
        """将list数组按行存储成txt文件"""
        with open(path, mode, encoding='utf-8') as f:
            f.writelines([str(word) + "\n" for word in words])


    # 清空文档
    def truncatefile(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            f.truncate()

    # 读取文档
    def read(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            txt = []
            for s in f.readlines():
                txt.append(s.strip())
        return txt


    def read_txtTolist(self, path):
        """ 读取txt文件转换为list,每行的文本用逗号进行了分隔"""
        with open(path, 'r', encoding='utf-8') as f:
            txt = []
            for s in f.readlines():
                txt.append(",".join(s.strip().split(",")))
        return txt

    def read_list_txt(self, path):
        """ 读取txt文件 每行是一个 list对象,但是这个list对象本身是字符串 """
        with open(path, 'r', encoding='utf-8') as f:
            txt = []
            for s in f.readlines():
                txt.append(eval(s))
        return txt

    def write_json_file(self, path, dict_model):
        """
        将dict转换为json dumps 并存储为json文件 dump
        :param path:
        :return:
        """
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(dict_model, f, ensure_ascii=False)


    def read_json_file(self, path):
        """
        读取json文件
        :param path:
        :return:
        """
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)


    def get_file_dirpath(self,path):
        """获取当前文件的文件夹路径
        直接使用 dirname的问题是，如果启动路径是相对路径，则返回/；如 cd /home python3 test.py

        """
        return os.path.dirname(os.path.abspath(path))


f = file_util()
write = f.write
write_list2txt = f.write_list2txt
read = f.read
get_file_dirpath=f.get_file_dirpath
import sys
class sys_util:
    def  get_sys_platform(self):
        if sys.platform.__contains__("linux"):return "linux"
        elif sys.platform.__contains__("win"):return "windows"

    def run_cmd(self,cmd_line,mode="read"):
        with os.popen(cmd_line) as p :
            if mode=="read":return p.read()
            elif mode=="readlines":return p.readlines()

s=sys_util()
get_sys_platform =s.get_sys_platform
run_cmd=s.run_cmd



import urllib

class  encrypt_util:

    def url_quote(self, text):

        return urllib.parse.quote(text)

    def url_unquote(self, text):
        """解码"""
        return urllib.parse.unquote(text)

    def url_quote_gbk(self, text):
        return urllib.parse.quote(text.encode("gbk"))

e = encrypt_util()
url_quote=e.url_quote
url_unquote=e.url_unquote
url_quote_gbk=e.url_quote_gbk

if __name__ == '__main__':
    pass
    print(get_uuid(sep="-"))
