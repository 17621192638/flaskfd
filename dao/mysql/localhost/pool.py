import utils.mysql.mysql_common_util as mysql_util
import configparser,os,time


cf = configparser.ConfigParser()
cf.read(os.path.dirname(__file__)+"/../conf.ini")

key = "localhost"
# 创建当前数据库的连接池对象
class service(object):
    def __init__(self):
        environment = cf.get(key,"environment")
        for i in range(3):
            print("当前mysql运行环境: {} !!!!".format(environment))
            time.sleep(0.1)
        self.pool = mysql_util.get_mysql_pool(
            host=cf.get(key,"host"),
            port=cf.get(key,"port"),
            user=cf.get(key,"user"),
            password=cf.get(key,"passwd"),
            database=cf.get(key,"db"),
            charset="utf8mb4"
        )
        self.conn, self.cursor = mysql_util.get_db_from_pool(pool=self.pool)

s = service()
run_sql = mysql_util.get_wrapper(s.pool)
run_sql_v2 = mysql_util.get_wrapper_v2(s.pool)


from utils.mysql.common_dao import common_dao as common
# 给公共方法加上带pool的注释器，无法通过init方法传递注释器
class common_dao(common):


    def __init__(self,table_name):
        super().__init__(table_name=table_name)

    escape_none_keys = ["status","email","phone","text","sentiment","img_url","dms_name","twords"]
    def move_none_keys(self,**kwargs):
        """移除不接受None的key"""
        model = kwargs.get("model",None)
        if model:
            escape_keys = [k for k,v in model.items() if (v ==None or v=="") and k in self.escape_none_keys]
            for k in escape_keys: del model[k]

    @mysql_util.pymysql_time_deal
    @run_sql(fetch_type="all")
    def select(self,*args, **kwargs):
        self.move_none_keys(**kwargs)
        return super().select(*args, **kwargs)

    @mysql_util.pymysql_time_deal
    @run_sql(fetch_type="one")
    def select_one(self,*args, **kwargs):
        self.move_none_keys(**kwargs)
        return super().select_one(*args, **kwargs)


    @run_sql(fetch_type=None)
    def update_by_id(self,*args, **kwargs):
        self.move_none_keys(**kwargs)
        return super().update_by_id(*args, **kwargs)

    @run_sql_v2(fetch_type=None)
    def update_by_id_v2(self,*args, **kwargs):
        self.move_none_keys(**kwargs)
        return super().update_by_id_v2(*args, **kwargs)


    @run_sql(fetch_type=None)
    def insert(self,*args, **kwargs):
        return super().insert(*args, **kwargs)

    @run_sql(fetch_type="one")
    def select_total(self,*args, **kwargs):
        self.move_none_keys(**kwargs)
        return super().select_total(*args, **kwargs)


    @run_sql(fetch_type=None)
    def delete_by_id(self,*args, **kwargs):
        return super().delete_by_id(*args, **kwargs)


    @run_sql(fetch_type=None)
    def delete(self,*args, **kwargs):
        return super().delete(*args, **kwargs)


    @run_sql_v2(fetch_type="all")
    def insert_v2(self,*args, **kwargs):
        return super().insert_v2(*args, **kwargs)



if __name__ == '__main__':
    pass
