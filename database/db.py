from flask_mongoengine import MongoEngine

db:MongoEngine = MongoEngine()
dir(db)

def initialize_db(app):
    db.init_app(app)