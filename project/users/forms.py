from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed
from project.models import User


class LoginForm(FlaskForm):
    email = StringField("e-mail: ", validators=[DataRequired(), Email()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    submit = SubmitField("Log in")


class RegForm(FlaskForm):
    email = StringField("e-mail address: ", validators=[DataRequired(), Email()])
    username = StringField("Username: ", validators=[DataRequired()])
    roll = StringField("Roll number: ", validators=[DataRequired()])
    password = PasswordField(
        "Password: ",
        validators=[
            DataRequired(),
            EqualTo("confirm_password", message="Passwords do not match"),
        ],
    )
    confirm_password = PasswordField("Confirm Password: ", validators=[DataRequired()])
    submit = SubmitField("Register")

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("e-mail already exists")

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("username already exists")

    def check_roll(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Roll number already exists")


class UpdateUserForm(FlaskForm):
    email = StringField("e-mail :", validators=[DataRequired(), Email()])
    username = StringField("Username :", validators=[DataRequired()])
    picture = FileField(
        "Update profile picture", validators=[FileAllowed(["jpg", "jpeg", "png"])]
    )
    roll = StringField("Roll number: ", validators=[DataRequired()])
    submit = SubmitField("Update profile")

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("e-mail already exists")

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("username already exists")

    def check_roll(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Roll number already exists")
