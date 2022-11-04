import os

from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "secret string")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "sqlite:////" + os.path.join(app.root_path, "../data.db"),
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


from password_manager.models import db

db.init_app(app)

import password_manager.handlers
import password_manager.views
