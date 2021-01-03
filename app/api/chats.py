from app.api import bp
from flask import jsonify

from flask import render_template, flash, redirect, url_for, current_app, request
import requests
from flask_login import current_user, login_required
from app.main.forms import SendSkypeMessageForm, CheckSkypeMessageForm, ChatReplyForm
from app.models import user, contact, message, group
from app import db
from werkzeug.urls import url_parse
from flask import request
from datetime import datetime
from skpy import Skype
from app.skype import SkypeClass
import json
import time
from flask import jsonify




@bp.route('/chats/<string:user_id>', methods=['GET'])
def check_chat_messages(user_id):
    skypeSession = SkypeClass()
    skypeSession.receive_message([user_id])
    data = message.messages_collection_dict(user_id = user_id)
    message.mark_as_read(user_id)
    return jsonify(data)

@bp.route('/chats/<string:user_id>/get_all', methods=['GET'])
def get_all(id):
    pass


@bp.route('/chats/<string:user_id>/get_new', methods=['GET'])
def check_one_messages(user_id):
    skypeSession = SkypeClass()
    skypeSession.receive_message([user_id])
    chat_id = f"8:{user_id}"
    page = request.args.get("page", 1, type=int)
    messages = message.query.filter_by(chat_id = chat_id).first()
    #messages = messages.order_by(message.timestamp.desc())
    messages.mark_read()
    return jsonify(data.to_dict())


@bp.route('/chats/<string:user_id>/send', methods=['POST'])
def reply(id):
    pass


@bp.route('/chats/<string:user_id>/mark_read', methods=['PUT'])
def mark_chat_as_read(id):
    pass


@bp.route("/contacts", methods=["GET"])
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




@bp.route('/fetch_contacts/<int:current_user_id>', methods=['GET'])
#@login_required
def fetch_c(current_user_id):
#Eventually !!! CHANGE Curren User ID 
    data = contact.contacts_collection_dict(current_user_id = 1)
    return jsonify(data)


@bp.route('/groups/<int:id>/', methods=['GET'])
def f_groups(id):
    data = group.group_collection_dict(current_user_id = 1)
    return jsonify(data)



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