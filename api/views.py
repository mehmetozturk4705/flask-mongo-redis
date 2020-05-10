from flask import request
from flask_restful import Resource
from database.models import UserModel
import jsonschema
from Application import config
from .exceptions import PasswordValidationError
import random
from Application.helpers import ApplicationHelper

cache=ApplicationHelper.get_application_cache()

class UserList(Resource):
    __JSON_SCHEMA = {
                        "type" : "object",
                        "required": ["name", "surname", "email", "password", "password2"],
                        "properties" : {
                            "name" : {"type" : "string", "minLength": 2},
                            "middle_name" : {"type" : "string", "minLength": 2},
                            "surname": {"type": "string", "minLength": 2},
                            "email": {"type": "string"},
                            "password": {"type": "string", "minLength": 8},
                            "password2": {"type": "string", "minLength": 8},
                        },
                  }
    def get(self):
        page = 1
        try:
            page = int(request.args.get("page", 1))
        except:
            pass
        pagination = UserModel.objects.paginate(page=page, per_page=10)
        has_next = pagination.has_next
        has_previous = pagination.has_prev

        return {
            "next": has_next,
            "prev":has_previous,
            "next_querystring": "?page=" + str(page+1) if has_next else None,
            "prev_querystring": "?page=" + str(page - 1) if has_previous else None,
            "data": list(map(lambda x: x.to_representation(), pagination.items))
        }

    def post(self):
        request_dict = request.get_json(force=True)

        jsonschema.validate(
            instance=request_dict, schema=self.__JSON_SCHEMA)
        #Skipping extra fields
        to_be_deleted = []
        for key in request_dict:
            if key not in self.__JSON_SCHEMA["properties"]:
                to_be_deleted.append(key)

        for key in to_be_deleted:
            del request_dict[key]
        if request_dict["password"] != request_dict["password2"]:
            raise PasswordValidationError("Passwords does not match.")
        del request_dict["password2"]
        user = UserModel(**request_dict)
        user.hash_password()
        user.save()
        return user.to_representation(), 201


class User(Resource):
    __JSON_SCHEMA_UPDATE = {
        "type": "object",
        "required": ["name", "surname", "email", "password"],
        "properties": {
            "name": {"type": "string", "minLength": 2},
            "middle_name": {"type": "string", "minLength": 2},
            "surname": {"type": "string", "minLength": 2}
        },
    }
    @cache.cached(timeout=config.CACHE_TIMEOUT)
    def get(self, user_id=None):
        return UserModel.objects.get_or_404(id=user_id).to_representation()
    def put(self, user_id=None):
        request_dict = request.get_json(force=True)

        jsonschema.validate(
            instance=request_dict, schema=self.__JSON_SCHEMA_UPDATE)
        # Skipping extra fields
        to_be_deleted = []
        for key in request_dict:
            if key not in self.__JSON_SCHEMA_UPDATE["properties"]:
                to_be_deleted.append(key)

        for key in to_be_deleted:
            del request_dict[key]
        cur_user = UserModel.objects.get_or_404(id=user_id)
        cur_user.name = request_dict["name"]
        cur_user.middle_name = request_dict.get("middle_name", None)
        cur_user.surname = request_dict["surname"]
        cur_user.validate()
        cur_user.save()
        return cur_user.to_representation()
    def delete(self, user_id=None):
        cache.delete("/user/" + user_id)
        cache.delete("/user/" + user_id + "/")
        UserModel.objects.get_or_404(id=user_id).delete()
        return {}, 204

#A sample for authorized resource
class ChangePassword(Resource):
    def post(self):
        pass

class Login(Resource):
    def post(self):
        pass
