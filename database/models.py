from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash

class UserModel(db.Document):
    name = db.StringField(required=True)
    middle_name = db.StringField(required=False)
    surname = db.StringField(required=True)
    email = db.EmailField(unique=True, required=True)
    password = db.StringField(required=True)
    meta = {'collection': 'contacts'}
    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def to_representation(self):
        return {"id": self.id.__str__(), "email": self.email, "name": self.name, "middle_name": self.middle_name, "surname": self.surname}