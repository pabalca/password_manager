import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from password_manager.crypto import Cypher

db = SQLAlchemy()


def generate_uuid():
    return str(uuid.uuid4())


class User(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    pwd_hash = db.Column(db.String)

    def __init__(self, pwd):
        self.pwd_hash = generate_password_hash(pwd)

    def __repr__(self):
        return f"<User> {self.id}"

    def verify_password(self, pwd):
        return check_password_hash(self.pwd_hash, pwd)


class Password(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    website = db.Column(db.Text)
    user = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    passphrase_hash = db.Column(db.String, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    crypto = Cypher()

    @property
    def passphrase(self):
        return self.crypto.decrypt(self.passphrase_hash.encode("utf-8"))

    @passphrase.setter
    def passphrase(self, passphrase):
        self.passphrase_hash = self.crypto.encrypt(passphrase).decode("utf-8")

    def __repr__(self):
        return f"<Password {self.website}:{self.user}>"
