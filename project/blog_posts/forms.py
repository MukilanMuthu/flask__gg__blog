from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class BlogPostForm(FlaskForm):
    title = StringField("Blog title: ", validators=[DataRequired()])
    text = TextAreaField("Your blog: ", validators=[DataRequired()])
    submit = SubmitField("Post")
