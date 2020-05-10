from flask import request, Request
from jsonschema import validate


def parse_request_data(request:Request, jsonchema:str = None):
    if jsonchema is not None:
        pass
