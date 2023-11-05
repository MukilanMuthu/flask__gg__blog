from project import db, login_manager
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from datetime import datetime

bcrypt = Bcrypt()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    profile_picture = db.Column(
        db.String(50), nullable=False, default="default_profile.png"
    )
    email = db.Column(db.String(50), unique=True, index=True)
    username = db.Column(db.String(50), unique=True, index=True)
    roll = db.Column(db.String(20), unique=True, index=True)
    password_hashed = db.Column(db.String(128))

    posts = db.relationship("BlogPost", backref="author", lazy=True)

    def __init__(self, email, username, roll, password):
        self.email = email
        self.username = username
        self.roll = roll
        self.password_hashed = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hashed, password)

    def __repr__(self):
        return f"username: {self.username}"


class BlogPost(db.Model):
    users = db.relationship(User)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id = user_id

    def __repr__(self):
        return f"post ID: {self.id} --- Title: {self.title}"
