from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from requestforchange import db

"""
class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, autoincrement = True, primary_key = True)
	webmailid = db.Column(db.String(63))
	is_admin = db.Column(db.Boolean, default = False)

class Requests(db.Model):
	__tablename__ = 'requests'
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	owner = db.Column(db.String(63), db.ForeignKey('users.id'))
	title = db.Column(db.String(511))
	subtitle = db.Column(db.String(511))
	content = db.Column(db.Text)
	supporters = db.Column(db.Text)
	status = db.Column(db.Text)
	approved = db.Column(db.Boolean, default = False)
	tags = db.Column(db.Text)
	priority = db.Column(db.Integer, default = 3) # 3 = low
	date = db.Column(db.Date)

class Updates(db.Model):
	__tablename__ = 'updates'
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	request_id = db.Column(db.Integer, db.ForeignKey('requests.id'))
	date = db.Column(db.Date)
	content = db.Column(db.Text)

class Comments(db.Model):
	__tablename__ = 'comments'
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	date = db.Column(db.Date)
	user_id = db.Column(db.String(63), db.ForeignKey('users.id'))
	request_id = db.Column(db.Integer, db.ForeignKey('requests.id'))
	content = db.Column(db.Text)

"""