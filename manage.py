#import requests
from flask import Flask, render_template, request, session, url_for, redirect, jsonify, flash

import loginmod
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'Desh$&Rish'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:root@localhost/rooter'
db = SQLAlchemy(app)

@app.route('/heartbeat')
def heartbeat():
	return jsonify(requestforchange = True)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
	print request.form['password']
	print request.form['webmailid']
	if request.method == 'POST':
		webmailid = request.form['webmailid']
		password = request.form['password']
		print webmailid," ",password
		string = loginmod.makerequest(webmailid,password)
		if string == "True":
			#flash('You successfully logged in')

			return redirect(url_for('change'))
			
		else:
			error = 'Invalid Credentials'
			return render_template('index.html', error = error)
	else:
		return render_template('index.html', error = error)

@app.route("/change", methods=['GET', 'POST'])
def change():
	if request.method == 'POST':
		return "POST"
	else:
		return render_template('change.html')

@app.route('/requests')
def requests():
	#requests = Request.query.all()
	return render_template('requests.html', requests = requests)

if __name__ == "__main__":
    app.run(debug = True)