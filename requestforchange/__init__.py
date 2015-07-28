from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager, Server

app = Flask(__name__)
app.config.from_object(__name__)

app.config['SECRET_KEY'] = 'Desh$&Rish'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:root@localhost/rooter'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    app.run()