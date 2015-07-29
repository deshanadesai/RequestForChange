#import requests
from flask import Flask, render_template, request, session, url_for, redirect, jsonify

import loginmod
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

db = SQLAlchemy(app)
db.create_all()
print "cerae"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///therequests.db'

@app.route('/heartbeat')
def heartbeat():
	return jsonify(requestforchange = True)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/showpost/<postid>")
def showpost(postid):
	post = Requests.query.filter(Requests.id == postid).first()
	return render_template('showpost.html',post=post)

@app.route("/showtag/<tagid>")
def showtag(tagid):
	posts = Requests.query.filter(Requests.tags = tagid)
	return render_template('requests.html',posts = posts)

@app.route("/login", methods=['GET', 'POST'])
def login():
	print request.form['password']
	print request.form['webmailid']
	if request.method == 'POST':
		webmailid = request.form['webmailid']
		password = request.form['password']
		print webmailid," ",password
		string = loginmod.makerequest(webmailid,password)
		if string == True:
			user = User()
			user.webmailid = webmailid
			user.is_admin = False
			db.session.add(user)
			db.session.commit()
			return redirect(url_for('change'))
		else:
			return render_template('index.html')
	else:
		return render_template('index.html')

@app.route("/change", methods=['GET', 'POST'])
def change():
	if request.method == 'POST':
		request = Request()
		return "POST"
	else:
		return render_template('change.html')

@app.route('/show/<which>')
def show(which):
	if which == 'user':
		jsonData = []
		users = User.query.all()
		for user in users :
			jsonData.append({'id':user.id, 'webmailid':user.webmailid, 'is_admin':user.is_admin})
		return jsonify(results = jsonData)
	if which == 'request':
		jsonData = []
		requests = Request.query.all()
		for request in request :
			jsonData.append({'title':request.title, 'owner':request.owner})
		return jsonify(results = jsonData)


# Database tables
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


if __name__ == "__main__":
	#db.app = app
	#db.init_app(ap

	app.run(debug = True)



