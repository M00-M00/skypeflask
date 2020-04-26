from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
from app.models import User, Security
import app.stocks as stocks

class ViewTickerForm(FlaskForm):
    ticker = StringField("ticker", validators=[DataRequired()])
    submit = SubmitField("View")

    def validate_ticker(self, ticker):
        ticker = ticker.data
        try:
            df = stocks.live_price(ticker)
        except AssertionError:
            raise ValidationError("Ticker does not exist!")

class AddTickerForm(FlaskForm):
    Add = SubmitField("Add")

class RemoveTickerForm(FlaskForm):
    Remove = SubmitField("Remove")
