from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import config
from flask_login import LoginManager, login_user, logout_user, login_required


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + config['development'].MYSQL_USER + \
    "@" + config['development'].MYSQL_HOST + \
    "/" + config['development'].MYSQL_DB

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager(app)
# login_manager.login_view = "login"

db = SQLAlchemy(app)
ma = Marshmallow(app)

