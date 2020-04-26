from app import app
from flask import render_template, flash, redirect, url_for, session
import requests
from app import weather
from app.forms import LoginForm, RegistrationForm, AddTickerForm, ViewTickerForm, RemoveTickerForm, ResetPasswordRequestForm, ResetPasswordForm
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User, Transaction, Security, ItemTable
from app import db
from werkzeug.urls import url_parse
from flask import request
import app.stocks as stocks
from flask_table import Table, Col
from datetime import datetime
from app.email import send_password_reset_email


dict = {"temp" : weather.CurrentTemp, "wind" : weather.WindSpeed, "weatherstate": weather.WeatherState, "icon": weather.iconUrl}

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()



@app.route('/')
@app.route('/index')
@login_required
def index():
    user = dict
    return render_template('index.html', title='Home', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password')
            return redirect(url_for('login'))
        login_user(user, remember= form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title = 'Sign In', form = form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/markets', methods=['GET', 'POST'])
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
            return redirect(url_for('security', ticker= ticker))
    return render_template('markets.html', title = 'Markets', form = formView, users_tickers = users_tickers, live_price = stocks.live_price)

@app.route('/security/<ticker>', methods=['GET', 'POST'])
@login_required
def security(ticker):
    ticker = ticker
    db_ticker = Security.query.filter_by(ticker = ticker).first()
    return render_template("security.html" , ticker = ticker, db_ticker = db_ticker)

@app.route('/follow/<ticker>')
@login_required
def follow(ticker):
    db_ticker = Security.query.filter_by(ticker = ticker).first()
    current_user.follow(db_ticker)
    db.session.commit()
    flash("Ticker {} is followed!".format(ticker))
    return redirect(url_for('markets'))

@app.route('/unfollow/<ticker>')
@login_required
def unfollow(ticker):
    db_ticker = Security.query.filter_by(ticker = ticker).first()
    current_user.unfollow(db_ticker)
    db.session.commit()
    flash("Ticker {} is unfollowed!".format(ticker))
    return redirect(url_for('markets'))


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
