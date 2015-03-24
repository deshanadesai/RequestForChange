#import requests
from flask import Flask, render_template, request, session, url_for
import loginmod

app = Flask(__name__)



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
			return render_template('change.html')
		else:
			return render_template('index.html')
	else:
		return render_template('index.html')

@app.route("/change", methods=['GET', 'POST'])
def change():
	if request.method == 'POST':
		print "Hurray!"
	else:
		print "Bugger!"

if __name__ == "__main__":
    app.run(debug = True)