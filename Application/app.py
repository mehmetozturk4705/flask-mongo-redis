from flask import Flask, request, jsonify
from .helpers import flask_register_module_as_config, ExtendedAPI, ApplicationHelper
from api.views import User, UserList, ChangePassword, Login
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from Application import config
from database.db import initialize_db


app = Flask(__name__)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
def init_paths(api_obj):
    api_obj.add_resource(User, '/user/<string:user_id>/', strict_slashes=False)
    api_obj.add_resource(UserList, '/user/', strict_slashes=False)
    api_obj.add_resource(ChangePassword, '/changepassword/', strict_slashes=False)
    api_obj.add_resource(Login, '/login/', strict_slashes=False)

ApplicationHelper.get_application_cache().init_app(app)
ApplicationHelper.get_application_cache().clear()
flask_register_module_as_config(app, config)
api = ExtendedAPI(app)
initialize_db(app)
init_paths(api)

@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(401)
@app.errorhandler(500)
def HandlerError(ex):
    desc = "There is an error."
    code = 500
    try:
        desc = ex.description
        code = ex.code
    except:
        pass
    return jsonify({"detail": desc}), code

if __name__ == '__main__':
    app.run()

