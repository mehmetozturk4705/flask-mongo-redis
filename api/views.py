from flask import request
from flask_restful import Resource

class UserList(Resource):
    def get(self):
        return {"get": ""}

    def post(self):
        return {"post": ""}

class User(Resource):
    def get(self, user_id=None):
        return {"get": user_id}
    def post(self, user_id=None):
        return {"post":user_id}
