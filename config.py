import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask.ext.script import Manager, Server
from requestforchange import app, login_manager, db

from flask import Flask, render_template, request, url_for, redirect, jsonify, flash
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import *
from sqlalchemy import *
import loginmod
import datetime
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.login import (UserMixin, current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
from constants import get_committees
from pdfs import create_pdf

manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    )
)

@app.route('/heartbeat')
def heartbeat():
    return jsonify(requestforchange = True)

@app.route("/")
def hello():
	if current_user.is_authenticated() :
		print 'is is_authenticated'
		return redirect('/show')
	else :
		print 'not authenticated'
		return render_template('index.html')

@app.route("/addcomment", methods=['GET','POST'])
def addcomment():
    if request.method == 'POST':
        postid = request.form['postid']
        post = Requests.query.filter(Requests.id == postid).first()
        userid = current_user.id
        date = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        content = request.form['content']
        comment = Comments(date,userid,postid,content)
        post.comments_no = post.comments_no + 1
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for("showpost",postid = postid))
    else:
        return redirect('/show')


@app.route("/showpost/<postid>")
@login_required
def showpost(postid):
    post = Requests.query.filter(Requests.id == postid).first()
    comments = Comments.query.filter(Comments.request_id == post.id)
    return render_template('showpost.html',post=post,comments=comments)

@login_required
@app.route("/showtag/<tagid>")
def showtag(tagid):
    committees = get_committees()
    if tagid == 'all':
        posts = Requests.query.all()
    else :
        posts = Requests.query.filter(Requests.tags == tagid)
    return render_template('requests.html', posts = posts, committees = committees)

@app.route("/show")
def show_reqs():
	committees = get_committees()
	searchtext = request.args.get('search')
	if searchtext is None:
		requests = Requests.query.all()
		return render_template("requests.html", posts = requests, allposts = Requests.query.all(), committees = committees)
	else:
		allrequests = Requests.query.all()
		requests = []
		for req in allrequests:
			#or searchtext in req.subtitle or searchtext in req.content
			if searchtext in req.title :
				requests.append(req)		
		return render_template("requests.html", posts = requests, allposts = Requests.query.all(), committees = committees)
	

@app.route("/showpost/<postid>")
@login_required
def show_post(postid):
    post = Requests.query.filter(Requests.id == postid).first()
    comments = Comments.query.filter(Comments.request_id == post.id)
    return render_template("showpost.html",post = post, comments = comments)

@app.route("/login", methods=['GET', 'POST'])
def login():
    print request.form['password']
    print request.form['webmailid']
    if request.method == 'POST':
        webmailid = request.form['webmailid']
        password = request.form['password']
        print webmailid," ",password
        string = loginmod.makerequest(webmailid,password)
        if string == 'True':
            if User.query.filter(User.id == webmailid).count() == 1:
                print "user already exists"
            else :
                print "creating new user"
                user = User(webmailid, False, True)
                db.session.add(user)
                db.session.commit()
            print "Coming here"
            user = User.query.filter(User.id == webmailid).first()

            print user.id
            print user.active
            if user.active:
                print "User is active"
                if login_user(user):
                    login_user(user)
                    print "User logged in"
                    print current_user.id
                    return redirect('/show')
                else:
                    return render_template('index.html',error = "Could not login. System error. We apologize for the inconvenience")
        else:
            error = 'Invalid Credentials'
            return render_template('index.html', error = error)
    else:
        return render_template('index.html', error = error)

@app.route("/change", methods=['GET', 'POST'])
@login_required
def change():
    if request.method == 'POST':
        
        #owner = request.form['owner']
        title = request.form['title']
        subtitle = request.form['subtitle']
        content = request.form['content']
        #supporters = request.form['supporters']
        status = request.form['status'] #public/private
        approved = False
        tags = request.form['tags']
        subtitle = request.form['subtitle']
        priority_str = request.form['priority_str']
        '''id_ = current_user.get_id()
        user = User.query.filter_by(User.id == id_).first()
        print user.webmailid'''

        priority = 0
        if priority_str == 'Low':
            priority = 1
        elif priority_str == 'Medium':
            priority = 2
        else:
            priority = 3
        #priority = request.form['priority']
        date = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        comments_no = 0

        newrequest = Requests(current_user.id, title, subtitle, content, str(current_user.id), status, False, tags, priority, date, comments_no)
        db.session.add(newrequest)
        db.session.commit()
        #return "POSTED"
        return redirect('/show')
    else:
        return render_template('change.html', committees = get_committees())

@app.route('/show/<which>')
@login_required
def show(which):
    if which == 'user':
        jsonData = []
        users = User.query.all()
        for user in users :
            jsonData.append({'id':user.id, 'is_admin':user.is_admin})
        return jsonify(results = jsonData)
    if which == 'request':
        jsonData = []
        requests = Requests.query.all()
        for request in requests :
            jsonData.append({'id':request.id,'owner':request.owner,'title':request.title,'subtitle':request.subtitle, 'content':request.content, 'supporters':request.supporters, 'status':request.status, 'approved':request.approved, 'tags':request.tags, 'priority':request.priority, 'date':str(request.date)})
        return jsonify(results = jsonData)

@app.route('/search', methods =['POST'])
def search():
	return redirect(url_for("show_reqs", search = request.form['srch-term']))

@app.route('/savepost/<postid>')
@login_required
def savepost(postid):
    post = Requests.query.filter(Requests.id == postid).first()
    comments = Comments.query.filter(Comments.request_id == post.id)
    pdf = create_pdf(render_template('showpost.html',post=post,comments=comments))
    return pdf
    
@app.route('/upvote/<postid>')
@login_required
def upvote(postid):
    post = Requests.query.filter(Requests.id == postid).first()
    supporters = str(post.supporters).split()
    print supporters
    if str(current_user.id) not in supporters :
        supporters.append(current_user.id)
        print 'added user to supporting list'
    else :
        print 'user already supporting'

    post.supporters = ' '.join(str(sup) for sup in supporters)
    db.session.commit()
    return redirect(url_for("showpost", postid = postid))
	
@login_manager.user_loader
def load_user(userid):
    print "User loader function"
    print userid
    user = User.query.filter(User.id == userid).first()
    return user

@app.route("/logout")
@login_required
def logout():
    '''
        Logs a user out. (No need to pass the actual user, pops current_user out of session). 
    This will also clean up the remember me cookie if it exists.
        '''
    logout_user()
    flash("Logged out.")
    return render_template("index.html")

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    is_admin = db.Column(db.Boolean, default = False)
    active = db.Column(db.Boolean, default = True)

    def __init__(self, id=None, is_admin=None, active=None):
        self.id = id
        self.is_admin = is_admin
        self.active = active
    
    def get_id(self):
        try:
            return unicode(self.id)
        except AttributeError:
            raise NotImplementedError('No id attribute - override get_id')

    def get_by_id(self, id):
        try:
            dbUser = User.query.filter(User.id == id).first()
            return dbUser
        except Exception, e:
            print str(e)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False


class Requests(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    owner = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(511))
    subtitle = db.Column(db.String(511))
    content = db.Column(db.Text)
    supporters = db.Column(db.Text)
    status = db.Column(db.Text)
    approved = db.Column(db.Boolean, default = False)
    tags = db.Column(db.Text)
    priority = db.Column(db.Integer, default = 3) # 3 = low
    comments_no = db.Column(db.Integer, default = 0)
    date = db.Column(db.Date)

    def __init__(self, owner, title, subtitle, content, supporters, status, approved, tags, priority, date, comments_no):
        self.owner = owner
        self.title = title
        self.content = content
        self.supporters = supporters
        self.status = status
        self.approved = approved
        self.tags = tags
        self.priority = priority
        self.date = date
        self.comments_no = 0

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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    request_id = db.Column(db.Integer, db.ForeignKey('requests.id'))
    content = db.Column(db.Text)

    def __init__(self,date,user_id,request_id,content):
        self.date = date
        self.user_id = user_id
        self.request_id = request_id
        self.content = content

if __name__ == "__main__":
    #db.app = app
    #db.init_app(app)
    db.create_all()
    #app.run(debug = True)
    manager.run()