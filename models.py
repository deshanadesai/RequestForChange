from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from manage import db
from sqlalchemy.dialects.postgresql import JSON

class User(db.Model):
	id = db.Column(db.Integer, autoincrement = True)
	webmailid = db.Column(db.String(63), primary_key = True)
	is_admin = db.Column(db.Boolean, default = False)

class Requests(db.Model):
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	owner = db.Column(db.String(63), db.ForeignKey('User.id'))
	title = db.Column(db.String(511))
	subtitle = db.Column(db.String(511))
	content = db.Column(db.Text)
	supporters = db.Column(db.JSON)
	status = db.Column(db.Text)
	approved = db.Column(db.Boolean, default = False)
	tags = db.Column(db.JSON)
	priority = db.Column(db.Integer, default = 3) # 3 = low
	date = db.Column(db.Date)

class Updates(db.Model):
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	request_id = db.Column(db.Integer, db.ForeignKey('Requests.id'))
	date = db.Column(db.Date)
	content = db.Column(db.Text)

class Comments(db.Model):
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	date = db.Column(db.Date)
	user_id = db.Column(db.String(63), db.ForeignKey('User.id'))
	request_id = db.Column(db.Integer, db.ForeignKey('Requests.id'))
	content = db.Column(db.Text)

