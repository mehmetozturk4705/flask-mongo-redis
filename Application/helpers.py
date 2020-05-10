from flask import Flask, jsonify
from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.exceptions import HTTPException
from flask_restful import Api
from mongoengine.errors import NotUniqueError, ValidationError as ModelValidationError
from api.exceptions import PasswordValidationError
from jsonschema.exceptions import ValidationError
from flask_caching import Cache
from Application import config
import re

def flask_register_module_as_config(app:Flask, module):
    """
    This helper registers central config file as Flask config.

    :param app Flask application
    :param module Configiration module
    :returns None
    """
    if not isinstance(app, Flask):
        raise TypeError(f"app should be type of {Flask}")
    for key in dir(module):
        if len(key) == sum(map(lambda x: 1 if (ord(x)>=65 and ord(x)<=90) or x=="_" else 0, key)):
            app.config[key]=getattr(module, key)


#Custom error handling
class ExtendedAPI(Api):
    def handle_error(self, err):
        print(type(err))
        print(err)
        # Handle HTTPExceptions
        if isinstance(err, HTTPException):
            return jsonify({
                    'message': getattr(
                        err, 'description', HTTP_STATUS_CODES.get(err.code, '')
                    )
                }), err.code
        #Handle validation error
        if isinstance(err, ValidationError) or isinstance(err, ModelValidationError) or isinstance(err, PasswordValidationError):
            return jsonify({
                'message': getattr(
                    err, 'description', str(err)
                )
            }), 400

        #Handle duplication
        if isinstance(err, NotUniqueError):
            expr = re.compile("(\{\s*.*\})")
            m = expr.findall(str(err))
            print(type(m[0]))
            str(err)
            return jsonify({
                'message': getattr(
                    err, 'description', f"There is a unique constraint violation. {m[0] if len(m)>0 else ''}"
                )
            }), 400
        # If msg attribute is not set,
        # consider it as Python core exception and
        # hide sensitive error info from end user
        if not getattr(err, 'message', None):
            return jsonify({
                'detail': 'Server has encountered some error'
                }), 500
        # Handle application specific custom exceptions
        return jsonify(**err.kwargs), err.http_status_code



class ApplicationHelper:
    __cache__=None
    @classmethod
    def get_application_cache(cls):
        if cls.__cache__ is None:
            cls.__cache__  = Cache(config={'CACHE_TYPE': 'redis',
                                  'CACHE_KEY_PREFIX': 'fcache',
                                  'CACHE_REDIS_HOST': config.CACHE_REDIS_HOST,
                                  'CACHE_REDIS_PORT': config.CACHE_REDIS_PORT})

        return cls.__cache__