from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all()
from flask_cors import *
from flask import Flask, jsonify,g,render_template
from flask_restful import Api, Resource, request
app = Flask(__name__)
# 跨域
CORS(app, supports_credentials=True)
api = Api(app)
# 设置后返回成中文
app.config['JSON_AS_ASCII'] = False
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))


# ----- restful api路由配置
import controller.user_controller as user_controller
api.add_resource(user_controller.do_login, '/api/login', endpoint="user_controller.do_login")
api.add_resource(user_controller.select_users, '/api/user/select_users', endpoint="user_controller.select_users")
api.add_resource(user_controller.test_group, '/api/user/test_group', endpoint="user_controller.test_group")

# import controller.domain_controller as domain_controller
# api.add_resource(domain_controller.create, '/api/domain/create', endpoint="domain_controller.create")
#
# import controller.project_controller as project_controller
# api.add_resource(project_controller.create, '/api/project/create', endpoint="project_controller.create")


if __name__ == '__main__':
    # app.run(host="0.0.0.0", debug=True,port=7789)
    WSGIServer(('0.0.0.0', 7789),app).serve_forever()




