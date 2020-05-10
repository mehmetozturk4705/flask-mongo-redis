from flask import Flask

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