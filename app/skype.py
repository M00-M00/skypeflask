from skpy import Skype, SkypeAuthException
from datetime import datetime
import os
from app.models import user, contact, message, group
from app.main import bp
from flask import render_template, flash, redirect, url_for, session, current_app, request
from app import db
import requests


class SkypeClass():

    def __init__(self):
        self._first_startup()
        if self._is_expired() == True:
            print("Token expires, getting a new token...")
            self._connect()



    def _connect(self):
        Skype("edimchenko@gmail.com", "C@ctus2747", ".skype_token")
        self._assign_token()


    def _assign_token(self):
        self.useToken = Skype(tokenFile=".skype_token")
        self.tokenExpiry = self.useToken.conn.tokenExpiry["skype"]
        self.test = "old"

    def _first_startup(self):
        if os.path.exists(".skype_token") == False:
            print("No token found, connecting...")
            self._connect()
        else:
            try:
                self._assign_token()
            except SkypeAuthException:
                print("Token expires, getting a new token...")
                self._connect()
        self.user_id = self.useToken.userId



    def _is_expired(self) -> bool:
         if self.tokenExpiry < datetime.now():
             return True
         return False

    def _check_expiration(self):
        if self._is_expired():
            print("Token expired: " + str(self.tokenExpiry) + "\n" + "Getting new Token...")
            self._connect()




    def show_contacts(self):
        #sk = Skype(current_app.config['SKYPE_EMAIL'], current_app.config['SKYPE_PASSWORD'])
        contacts = self.useToken.contacts
        return contacts

    def fetch_contacts(self):
        contacts = self.useToken.contacts
        contact_dict = {}
        for c in contacts:
            contact_dict[c.id] = {"id":c.id, "name": str(c.name.first) + " " + str(c.name.last)}
        return contact_dict

    def send_message_individually(self, recepients, message):
        self._check_expiration()
        for recepient in recepients:
            if type(recepient == app.models.group):
                for c in recepient.contacts:
                    recepients.append(c.contact_skype_id)
            else:
                new_chat = self.useToken.contacts[recepient].chat
                new_message = new_chat.sendMsg(message)
                nm = new_message
                db_message = message(chat_id = nm.chatId, skype_sender_name = nm.userId, skype_message_id = nm.id, timestamp = nm.time, body = nm.content, skype_account = self.useToken.userId)
                db.session.add(db_message)
                db.session.commit()
    
    def receive_message(self, recepients):
        self._check_expiration()
        for recepient in recepients:
            new_msgs = self.useToken.chats["8:" +  recepient].getMsgs()
            for nm in new_msgs:
                db_message = message.query.filter_by(skype_message_id= nm.id).first()
                if db_message is None:
                    db_message = message(chat_id = nm.chatId, skype_sender_name = nm.userId, skype_message_id = nm.id, timestamp = nm.time, body = nm.content, skype_account = self.useToken.userId)
                    db.session.add(db_message)
                    db.session.commit()



"""
    def check_messages(self):
        self._check_expiration()
        
        if len(new_msgs) > 0:
            for nm in new_msgs:
                db_message = message.query.filter_by(skype_message_id= nm.id).first()
                if db_message is None:
                    db_message = message(chat_id = nm.chatId, skype_sender_name = nm.userId, skype_message_id = nm.id, timestamp = nm.time, body = nm.content, skype_account = self.useToken.userId)
                    db.session.add(db_message)
                    db.session.commit()
        else:
            flash("No new messages!")
"""




