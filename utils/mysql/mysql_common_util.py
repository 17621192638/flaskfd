#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  : jzy
@Contact :  : 905414225@qq.com
@Software: PyCharm
@File    : db_service.py
@Time    : 2018/12/10 16:51
@Desc    : 数据库连接配置文件
"""
import pymysql,traceback,datetime,decimal
from DBUtils.PooledDB import PooledDB



def get_mysql_pool(host,port,user,password,database,charset="utf8mb4"):
    """获取连接池对象"""
    pool =  PooledDB(
        creator=pymysql,
        maxconnections=55,  # 连接池允许的最大连接数，0和None表示不限制连接数
        mincached=5,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
        maxcached=15,  # 链接池中最多闲置的链接，0和None不限制
        blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
        maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
        host=host,
        port=int(port),
        user=user,
        password= password,
        database= database,
        charset= charset
    )
    return pool

def get_db_from_pool(pool):
    """从连接池中获取一条连接"""
    conn = pool.connection()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    return conn,cursor

def get_wrapper(pool):
    """返回固定连接池 pool的run_sql修饰器"""
    def run_sql(fetch_type="all"):
        def wrapper0(fn):
            def wrapper(*args, **kwargs):
                sql=None
                try:
                    sql = fn(*args, **kwargs)
                    if not sql: return None
                    # 判断当前连接是否处于连接状态，不是的话重新从连接池拿一条连接
                    # if s.conn.open:s.conn, s.cursor = mysql_common_util.get_db_from_pool(pool=pool)
                    conn, cursor = get_db_from_pool(pool=pool)

                    cursor.execute(sql.replace("'None'", "Null").replace("=None","=null").replace(",None",",null").replace("None,","null,"))

                    conn.commit()
                    return cursor.fetchall()  if fetch_type=="all" else cursor.fetchone() if fetch_type=="one" else None
                except Exception as e:
                    if e.args[0]==1062:
                        print("当前ID重复 {}".format(str(e)))
                        return {"code":200,"message":"插入重复"}
                    traceback.print_exc()
                    print(sql)
                    return {"code":400,"message":str(e)}
            return wrapper
        return wrapper0
    return run_sql


def get_wrapper_v2(pool):
    """v2 使用 execute args传值"""
    def run_sql(fetch_type: str = "all"):
        def wrapper0(fn):
            def wrapper(*args, **kwargs):
                conn, cursor =None,None
                try:
                    sql,r_args = fn(*args, **kwargs)
                    if not sql: return None
                    # 判断当前连接是否处于连接状态，不是的话重新从连接池拿一条连接
                    # if s.conn.open:s.conn, s.cursor = mysql_common_util.get_db_from_pool(pool=pool)
                    conn, cursor = get_db_from_pool(pool=pool)
                    # sql = "insert ignore into data_text2(id,text,p_id,source_name) values(%s,%s,%s,%s)"
                    # r_args = [["⌛321","2dasda","大",None]]
                    # 如果使用ignore 则会忽略所有错误类型
                    # res = cursor.executemany(sql,args=r_args)
                    if type(r_args)==tuple:
                        cursor.execute(sql,args=r_args)
                        conn.commit()
                        return cursor.fetchall()  if fetch_type=="all" else cursor.fetchone() if fetch_type=="one" else None
                    elif type(r_args) ==list:
                        s_num =cursor.executemany(sql,args=r_args) # 返回成功执行的数量
                        conn.commit()
                        return s_num
                except Exception as e:
                    if e.args[0]==1062:
                        print("当前ID重复 {}".format(str(e)))
                        return {"code":200,"message":"插入重复"}
                    traceback.print_exc()
                    conn.rollback()
                    return {"code":400,"message":str(e)}
            return wrapper
        return wrapper0
    return run_sql


def dict_to_str(model={},join_type=" and ",escape_key=[],fuzzy_query_key=[]):
    """拼接 全and 查询条件
    拼接形式
    select  “ and ”
    update  ","
    escape_key 不需要的key放这里
    fuzzy_query_key 需要模糊查询的key放这里
    """
    return join_type.join(["{} like '%{}%'".format(k,pymysql.escape_string(v)) if k in fuzzy_query_key else  "%s='%s'"%(k,pymysql.escape_string(v)) if type(v)==str else "%s is null"%(k) if v==None else "%s=%s"%(k,v) for k,v in model.items() if k not in escape_key])




def dict_to_str_v2(model={},join_type=" and ",escape_key=[]):
    """拼接 全and 查询条件
    拼接形式
    select  “ and ”
    update  ","
    escape_key 不需要的key放这里
    """
    return join_type.join(["{}=%s".format(k) for k in model.keys() if k not in escape_key])


def dict_to_str_mode_insert(model={}):
    """
    insert模式
    """
    return ",".join(model.keys()),",".join([ "'%s'"%(pymysql.escape_string(v)) if type(v)==str else "%s"%v for v in model.values()])


def dict_to_insert_sql(model={}):
    """
    insert模式
    """
    return ",".join(model.keys()), ",".join(['%s' for i in model.keys()])

def get_sql_args(model={},escape_key=[]):
    """
    获取sql执行的的tuples
    """
    if type(model)==dict:
        vs = [ v for k,v in model.items() if k not in escape_key]
        if "id" in escape_key:
            vs.append(model["id"])
        return tuple(vs)
    elif type(model) ==list:  # [(a,b,c),(a,b,c)]
        return [tuple(i.values()) for i in model if i]


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
                    elif type(res[key])==decimal.Decimal:
                        res[key]= float(res[key].normalize())
            elif type(res)==list:
                for model in res:
                    for key in model.keys():
                        if type(model[key]) == datetime.datetime:
                            model[key] = str(model[key])
                        elif type(model[key])==decimal.Decimal:
                            model[key]= float(model[key].normalize())
            return res
        else:
            return res
    return wrapper


if __name__ == '__main__':
    pass
    res = dict_to_str(model={"text":"123","key1":"哈哈","key2":"value2","key3":"value3"},escape_key=["key1"],fuzzy_query_key=["key2","key3"])
    print(res)