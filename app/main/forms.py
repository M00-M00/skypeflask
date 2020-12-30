from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Length
from app.models import user, contact, message, group


class SendSkypeMessageForm(FlaskForm):
    text = TextAreaField("text", validators = [DataRequired()])
    select = BooleanField("Select Contact")
    message_as_a_group = BooleanField("Group in one chat")
    submit = SubmitField("Send Message")


class ChatReplyForm(FlaskForm):
    text = TextAreaField("text", validators = [DataRequired()])
    submit = SubmitField("Send Message")

class CheckSkypeMessageForm(FlaskForm):
    submit = SubmitField("Check Messages")
