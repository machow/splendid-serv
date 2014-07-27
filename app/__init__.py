#=================================================
# Setup app
#=================================================
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='templates/_')
app.config.from_object('config')
db = SQLAlchemy(app)

# Login extension------------------------------------
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir
import os

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

oid = OpenID(app, os.path.join(basedir, 'tmp'))

from app import views, models
