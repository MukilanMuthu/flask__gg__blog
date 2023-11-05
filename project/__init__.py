import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)

##### database setup #####
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    base_dir, "data.sqlite"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "pearl"

db = SQLAlchemy(app)
Migrate(app, db)

##### login config #####
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "user.login"

from project.core.views import core
from project.error.handler import error_pages
from project.users.views import users
from project.blog_posts.views import blog_post

app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(users)
app.register_blueprint(blog_post)
