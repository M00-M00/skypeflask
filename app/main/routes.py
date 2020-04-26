from flask import render_template, flash, redirect, url_for, session, current_app
import requests
from flask_login import current_user, login_required
from app import weather
from app.main.forms import AddTickerForm, ViewTickerForm, RemoveTickerForm
from app.models import User, Transaction, Security, ItemTable
from app import db
from app.main import bp
from werkzeug.urls import url_parse
from flask import request
import app.stocks as stocks
from flask_table import Table, Col
from datetime import datetime


dict = {"temp" : weather.CurrentTemp, "wind" : weather.WindSpeed, "weatherstate": weather.WeatherState, "icon": weather.iconUrl}

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()



@bp.route('/')
@bp.route('/index')
@login_required
def index():
    user = dict
    return render_template('index.html', title='Home', user=user)




@bp.route('/markets', methods=['GET', 'POST'])
@login_required
def markets():
    formView = ViewTickerForm()
    users_tickers = current_user.followed_tickers()
    securities_info = [stocks.live_price(u) for u in users_tickers]
    if formView.validate_on_submit():
            ticker = formView.ticker.data
            db_ticker = Security.query.filter_by(ticker = ticker).first()
            if db_ticker is None:
                info_to_add = stocks.get_information(ticker)
                new_ticker = Security(ticker=ticker, website=info_to_add["website"], name = info_to_add["shortName"], sector = info_to_add["sector"], summary = info_to_add["longBusinessSummary"])
                db.session.add(new_ticker)
                db.session.commit()
                flash("Ticker New Ticker Added to DB")
            return redirect(url_for('main.security', ticker= ticker))
    return render_template('markets.html', title = 'Markets', form = formView, users_tickers = users_tickers, live_price = stocks.live_price)

@bp.route('/security/<ticker>', methods=['GET', 'POST'])
@login_required
def security(ticker):
    ticker = ticker
    db_ticker = Security.query.filter_by(ticker = ticker).first()
    return render_template("security.html" , ticker = ticker, db_ticker = db_ticker)

@bp.route('/follow/<ticker>')
@login_required
def follow(ticker):
    db_ticker = Security.query.filter_by(ticker = ticker).first()
    current_user.follow(db_ticker)
    db.session.commit()
    flash("Ticker {} is followed!".format(ticker))
    return redirect(url_for('main.markets'))

@bp.route('/unfollow/<ticker>')
@login_required
def unfollow(ticker):
    db_ticker = Security.query.filter_by(ticker = ticker).first()
    current_user.unfollow(db_ticker)
    db.session.commit()
    flash("Ticker {} is unfollowed!".format(ticker))
    return redirect(url_for('main.markets'))
