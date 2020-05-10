from flask import Flask, request, jsonify
from helpers import flask_register_module_as_config
from flask_restful import Api
from api.views import User, UserList
import config


app = Flask(__name__)
flask_register_module_as_config(app, config)
api = Api(app)
api.add_resource(User, '/user/<string:user_id>')
api.add_resource(User, '/user/<int:user_id>')
print(app.url_map)

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

