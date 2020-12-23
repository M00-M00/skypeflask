from flask import render_template, flash, redirect, url_for, current_app, request
import requests
from flask_login import current_user, login_required
from app.main.forms import SendSkypeMessageForm, CheckSkypeMessageForm
from app.models import user, contact, message, group
from app import db
from app.main import bp
from werkzeug.urls import url_parse
from flask import request
from datetime import datetime
from skpy import Skype
from app.skype import SkypeClass
import json
import time
from flask import jsonify


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        #db.session.commit()



@bp.route('/')
@bp.route('/index')
@login_required
def index():

    return render_template('index.html', title='Home')


@bp.route('/fetch_contacts', methods=['GET', 'POST'])
@login_required
def fetch_contacts():
    skypeSession = SkypeClass()
    contacts = skypeSession.fetch_contacts()
    for c in contacts:
        db_contact = contact.query.filter_by(contact_skype_id = contacts[c]["id"]).first()
        if db_contact is None:
            contact_to_add = contact(contact_skype_id = contacts[c]["id"], contact_name = contacts[c]["name"], user_id = current_user.id)
            db.session.add(contact_to_add)
            db.session.commit()
    contacts = contact.query.filter_by(user_id = current_user.id).all()
    d ={}
    for c in contacts:
        d[c.contact_skype_id] = {"id": c.contact_skype_id, "name": c.contact_name}
    return json.dumps(d)



@bp.route('/fetch', methods=['POST'])

def fetch():
    data = request.get_json()
    group_name = data["groupName"]
    ids = [n["value"] for n in data["contacts"]]
    print(ids)
    db_group = group.query.filter_by(group_name = group_name).first()
    if db_group != None:
        db.session.delete(db_group)
        db.session.commit()

    db_group = group(group_name = group_name, user_id = 1)
    db.session.add(db_group)
    db.session.commit()
    for n in ids:
        contact_db = contact.query.filter_by(contact_skype_id = n).first()   
        db_group.contacts.append(contact_db) 
        db.session.add(db_group)
        db.session.commit()
    response = jsonify("New group has been created!")
    response.status_code = 201
    return response


@bp.route('/skype', methods=['GET', 'POST'])
@login_required
def skype():
    form = SendSkypeMessageForm()
    check_messages = CheckSkypeMessageForm()
    #contacts = [["test", "test"], ["test2", "test3"]]
    skypeSession = SkypeClass()
    print(current_app.config['SKYPE_EMAIL'], current_app.config['SKYPE_PASSWORD'])
    contacts = contact.query.filter_by(user_id = current_user.id).all()
    groups = group.query.filter_by(user_id = current_user.id).all()
    selected = request.form.getlist('check')
    message = form.text.data
    if form.validate_on_submit():
        #skypeSession.send_message_individually(selected, message)
        flash(str(selected) + "were sent a message" + message)
    #if check_messages.submit():
        #skypeSession.receive_message(selected)

    return render_template('skype.html', title='Skype Messaging',  contacts = contacts, groups = groups,  form = form, check_messages = check_messages )

@bp.route("/messages/<string:user_id>", methods=["GET", "POST"])
@login_required
def messages(user_id):
    skypeSession = SkypeClass()
    skypeSession.receive_message([user_id])
    chat_id = f"8:{user_id}"
    page = request.args.get("page", 1, type=int)
    messages = message.query.filter_by(chat_id = chat_id)
    messages_ordered = messages.order_by(message.timestamp.desc())
    #next_url = url_for('main.messages/<string:chat_id', page=messages.next_num) \
    #    if messages.has_next else None
    #prev_url = url_for('main.messages/<string:chat_id', page=messages.prev_num) \
    #    if messages.has_prev else None
    return render_template('messages.html', messages=messages_ordered)
                      # next_url=next_url, prev_url=prev_url)

@bp.route("/contacts")
def contacts():
    contacts = contact.query.filter_by(user_id = current_user.id).all()
    contact_list = {}
    contact_list['contact'] = []
    for c in contacts:
        contact_db = {'value':c.contact_skype_id, 'label': c.contact_name} 
        contact_list["contact"].append(contact_db)
    with open("./react-flask-app/src/data.json", "w") as o:
        json.dump(contact_list, o)
    return json.dumps(contact_list)


@bp.route('/time')
@login_required
def get_current_time():
    d = current_user.id
    dd = {"id": d}
    return jsonify(dd)



