## FlaskFD


基于flask的后端敏捷开发框架，围绕多个项目的业务代码进行整合调整，模块抽象，易于理解和助力快速开发。
* flask 引入 gevent、cors，提高并发和兼容跨域
* 精简整合路由配置，还原经典controller、service、dao后台架构分层
* 引入多种业务装饰器，大幅减少前后端数据格式化、业务异常捕获、mysql事务查询等高频次耦合性代码

## run 开发
```

# 拉取项目代码
git clone git@github.com:17621192638/flaskfd.git

# 安装依赖
pip3 install -r /home/flaskfd/requirements.txt

# 运行
python3 /home/flaskfd/web_api.py

```


## FileTree 目录结构

```

┌── FlaskFD
├── controller  // 控制器层 
├── service      // 业务逻辑层 
├── dao          // 数据库层
│ ├── mysql    // mysql数据库
│ ├── ├── localhost1   // 数据库1
│ ├── ├── localhost2   // 数据库2
│ ├── ├── conf.ini       // mysql数据库 
├── utils                // 项目工具类，基本通用方法汇总 
│ ├── mysql          
│ ├── nlp 
│ ├── code_util.py          // 自定义返回状态码
│ ├── common_util.py     // 公共基础方法类
│ ├── decorator_util.py    // 通用修饰器
│ ├── faker_util.py          
│ ├── logger_util.py        // 日志工具类
│ ├── response_util.py     // 通用response解释器
├── .gitignore 
├── requirements.txt // 项目依赖 
├── web_api.py       // api路由配置和项目启动服务 
└── ...
```


## RestFul Api 接口路由配置


```
web_api.py
...
...
import controller.user_controller as user_controller

api.add_resource(user_controller.do_login, '/api/login', 
endpoint="user_controller.do_login")

# import controller.domain_controller as domain_controller
# api.add_resource(domain_controller.create, 
'/api/domain/create', endpoint="domain_controller.create")

## import controller.project_controller as project_controller
# api.add_resource(project_controller.create, 
'/api/project/create', endpoint="project_controller.create")
...
...
```
在web_api.py 项目启动文件中进行api接口路由的配置，引入不同的controller，每个controller方法对应一个api方法，自定义api的地址。

## Controller配置

```
user_controller.py
...
...
from flask_restful import Resource, request
from  service.user_service import  user_service
import utils.response_util as response_util

service =user_service()

class do_login(Resource):    
    @response_util.response_filter_v2    
    def post(self):        
        text_json = request.get_json()        
        return service.do_login(text_json)


...
...
```
flask支持多种路由配置方式，建议统一风格通过class的形式进行单路由配置。每个controller可以对应一个/多个service服务.
**@response_util.response_filter_v2 修饰器**将会对service主体进行异常捕获，异常提示，返回内容格式化，耗时统计等操作
*  **内容格式化** 通过对service返回值进行拦截判断与处理，返回给前端统一的接口格式（JSON）
```
{
"code": 200, # 返回状态码，接口正常，返回200
"data": res,  # 内容主体
"timeout":timeout,   # 接口耗时
"message":message  # 备注信息
}
```
*  **异常捕获** 对service异常代码进行捕获返回
```
{
"code":400, # 返回状态码
"data": None,  
"timeout":timeout,   # 接口耗时
"message":"traceback message"  # 代码异常堆栈信息
}
```

*  **自定义code类型** 通过对 **utils/code_util.py** 进行添加修改删除自定义状态码，返回给前端特殊code代码和message补充信息（与项目前端协商）
```
{
"code":10001, 
"data": None,  
"timeout":timeout, 
"message":"登录失败,账号或者密码错误."
}


```
可以补充在Controller层实现接口权限控制、请求数据统计等功能。

## Service处理
```
user_service.py
...
...
import dao.mysql.localhost.user_dao as user_dao
import utils.common_util as common_util
import utils.decorator_util as decorator_util

class user_service:    
    
    @decorator_util.decorator_none
    def do_login(self,text_json):        
        users = user_dao.select(model{"username":text_json["username"],"password":text_json["password"],"status":0})        
        if not users:return {"code":10001}        
        else: return users[0]
...
...
```
具体业务逻辑层，一个service对应一个/多个dao，按具体业务类型和模块进行拆分。
**@decorator_util.decorator_none** 公共拦截器，拦截捕获业务逻辑异常，返回None。 主要应用于局部service业务逻辑处理方法，减少重复 **try exception**代码。通过自定义拦截器 **uitls/decorator_util**，完成对业务逻辑的统一处理。


## Dao层封装


### 连接多种数据库
```
...
├── dao          // 数据库层
│ ├── mysql   // mysql数据库
│ ├── elasticsearch         // 其它数据库
...
```
项目中存在多个数据库的类型处理的与连接，都放到 **dao/** 文件夹下，如mysql、elasticsearch、mongo等


### 连接多个mysql数据库
```
...
│ ├── mysql    // mysql数据库
│ ├── ├── localhost1   // 数据库1
│ ├── ├── localhost2   // 数据库2
│ ├── ├── conf.ini       // 数据库配置文件
...
```

多个同数据库类型的库方法按照数据库名称放到**dao/mysql/**文件夹下。

```
pool.py
...
...
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
        user=cf.get(key,"user"),            password=cf.get(key,"passwd"),            database=cf.get(key,"db"),           
        charset="utf8mb4"        )        
        self.conn,self.cursor
        =mysql_util.get_db_from_pool(pool=self.pool)
        
s = service()
run_sql = mysql_util.get_wrapper(s.pool)
run_sql_v2 = mysql_util.get_wrapper_v2(s.pool)
...
...
from utils.mysql.common_dao import common_dao as common
# 给公共方法加上带pool的注释器，无法通过init方法传递注释器
class common_dao(common):    
    def __init__(self,table_name):        
        super().__init__(table_name=table_name)    

    @mysql_util.pymysql_time_deal    
    @run_sql(fetch_type="all")    
    def select(self,*args, **kwargs):        
        return super().select(*args, **kwargs)
...
```

 *   **pool.py** 每个数据库下面都有一个统一的pool.py文件，通过修改**key**的值，指定加载对应的conf.ini配置文件信息，pool.py在被引用时会初始化并生成一个**mysql连接池对象**。**仅需修改文件中的key值即可**。

 *   **run_sql** pool.py文件会向外暴露一个run_sql方法，仔细看其实是一个装饰器，被该装饰器装饰的sql语句，会从连接池中获取一个mysql连接对象，去执行sql语句， 并返回执行结果。装饰器封装了连接池**获取连接对象，提交事务，执行事务，按条件执行sql，返回sql结果和异常捕获**相关的逻辑操作代码，灵活运用@run_sql可大幅减少sql相关的重复流程性代码。
     *  @run_sql(fetch_type="all")  对应返回 cursor.fetchall()方法结果
     *  @run_sql(fetch_type="one")  对应返回 cursor.fetchone()方法结果
     *  @run_sql(fetch_type="None")  执行语句不返回结果
     *  其它自定义执行内容可按需求更改

* **继承common_dao**  当前pool下的内部类common_dao继承了 **utils/mysql.common_dao** common_dao中封装了**select**、**select_one**、**select_total** 等在内的多种基本sql语句的生成方法。



```
``
user_dao.py
...
...
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
...
```

*  **table_name_dao.py** 每个表一一对应一个dao文件，仅仅封装了该表的数据库操作
*  **继承common_dao** 每个表的dao文件都会继承对应**dao.mysql.localhost.pool** 数据源下的公共方法，并向service层暴露了该表**select，update_by_id，update，delete，insert** 在内的多种基本sql方法，并开放多个参数用来灵活控制和拼接sql语句，完成业务逻辑
    * **model** 字典类型，  service传递到dao的sql检索条件（where后面的部分）
        * order_by：create_time 排序字段名称
        * mode: "asc"  排序的模式,"asc","desc"
        * page_num：1 页码
        * page_size：20 每页返回数量
        * 其它查询条件,多个查询条件会自动拼接，如 username:"admin","password":"admin"，会拼接成 "username='admin' and password= 'admin' "

    * **fields** 数组类型， 查询返回的属性字段集合，如仅返回["id","username","password"]
    * **escape_key** 数据类型，**自定义model中无需进行拼接的属性名称**，默认为["page_num","page_size","order_by","mode"]
    * **fuzzy_query_key** 数据类型， 自定义需要进行模糊匹配查询的字段，匹配模式为 like "%key名称%" 
    * **prefix_sql** 字符串类型，高级用法，**自定义sql查询的前缀**（where条件之前的部分），默认为""，即"select fields from table_name"语句，可自定义为其它语句，如"select sum(key) from table_name"等灵活的sql用法

    
## 业务实践案例快速上手



### case1 基本查询—账号密码验证
账号密码验证

```
--> flaskfd/service/user_service.py
# 调用基本select方法，启用状态下的账号是否存在，不存在返回10001,存在返回用于信息
@decorator_util.decorator_nonedef do_login(self,text_json):    
    users = user_dao.select(model={"username":text_json["username"],"password":text_json["password"],"status":0})    
    if not users:return {"code":10001}    
    else: return users[0]

--> flaskfd/controller/user_controller.py
# 方法调用
class do_login(Resource):    
    @response_util.response_filter_v2    
    def post(self):        
        text_json = request.get_json()        
        return service.do_login(text_json)

--> flaskfd/web_api.py
# 添加路由

import controller.user_controller as u ser_controller
api.add_resource(user_controller.do_login,'/api/login',endpoint="user_controller.do_login")

```

```
--> POST

http://localhost:7789/api/login

--> Body JSON 

{
"username":"admin",
"password":"admin"
}

--> Response JSON

{
    "code": 200,
    "data": {
        "avatar_url": "",
        "company_name": "超级管理员",
        "create_time": "2020-07-25 10:25:03",
        "email": "",
        "email_code": "",
        "email_status": null,
        "id": 1,
        "nickname": "超管",
        "password": "admin",
        "phone": "",
        "phone_code": "",
        "phone_status": null,
        "remarks": "超级管理员",
        "status": 0,
        "update_time": "2020-11-02 14:16:15",
        "user_type": 1,
        "username": "admin"
    },
    "message": null,
    "timeout": "0.002"
}

```


### case2 复杂条件查询—用户表查询

分页查询用户表用户

```

--> flaskfd/service/user_service.py

def select_users(self,text_json):    
    data = user_dao.select(model=text_json,fields["id","username","create_time"])    
    total = user_dao.select_total(model=text_json,fields["id","username","create_time"])    
    return {"total":total["total"],"data":data,"page_num":text_json["page_num"],"page_size":text_json["page_size"]}

--> flaskfd/controller/user_controller.py
# 方法调用
class select_users(Resource):    
    @response_util.response_filter_v2    
    def post(self):        
        text_json = request.get_json()        
        return service.select_users(text_json)

--> flaskfd/web_api.py
# 添加路由
api.add_resource(user_controller.select_users,'/api/user/select_users',endpoint="user_controller.select_users")

```

```
--> POST

http://localhost:7789/api/user/select_users

--> Body JSON 


{
"page_num":1,
"page_size":10,
"order_by":"create_time",
"mode":"asc"
}



--> Response JSON
{
    "code": 200,
    "data": {
        "data": [
            {
                "create_time": "2020-07-25 10:25:03",
                "id": 1,
                "username": "admin"
            },
            {
                "create_time": "2020-11-02 14:32:58",
                "id": 45,
                "username": "张三"
            },
            {
                "create_time": "2020-11-02 14:33:09",
                "id": 46,
                "username": "李四"
            },
            {
                "create_time": "2020-11-02 14:33:24",
                "id": 47,
                "username": "王五"
            },
            {
                "create_time": "2020-11-02 14:33:45",
                "id": 48,
                "username": "admin2"
            }
        ],
        "page_num": 1,
        "page_size": 10,
        "total": 5
    },
    "message": null,
    "timeout": "0.011"
}
```


### case3 自定义复杂查询—聚合统计

统计用户表用户数量

```
--> flaskfd/dao/mysql/localhost/user_dao.py

# prefix用法
def test_group1(self):    
    return self.select(model=None,prefix_sql="select count(1) as num from %s "%self.table_name)
    
 # 自定义注解用法
@run_sql(fetch_type="all")
def test_group2(self):    
    sql = "select count(1) as num from %s " %  self.table_name    
    return sql

test_group1=d.test_group1
test_group2=d.test_group2





--> flaskfd/service/user_service.py

def test_group(self,text_json):    
    data = user_dao.test_group1()    
    # 或 data = user_dao.test_group2()   
    return data

--> flaskfd/controller/user_controller.py
# 方法调用
class test_group(Resource):    
    @response_util.response_filter_v2    
    def post(self):        
        text_json = request.get_json()        
        return service.test_group(text_json)

--> flaskfd/web_api.py
# 添加路由
api.add_resource(user_controller.test_group,'/api/user/test_group',endpoint="user_controller.test_group")

```

```
--> POST


http://localhost:7789/api/user/test_group

--> Body JSON 


{
}



--> Response JSON

{
    "code": 200,
    "data": [
        {
            "num": 5
        }
    ],
    "message": null,
    "timeout": "0.003"
}

```

两种特殊查询用法，基本能满足全部的自定义复杂sql查询场景，对比理解，熟练上手。








