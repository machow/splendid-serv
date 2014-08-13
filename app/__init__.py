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

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'


# Cache ---------------------------------------------
from flask.ext.cache import Cache
cache = Cache(app,config={'CACHE_TYPE': 'simple'})

from app import models, views
