import os
from config import basedir
from app import app, db
from app.models import User, Game

app.config['TESTING'] = True
app.config['CSRF_ENABLED'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')

app =  app.test_client()
db.create_all()

u = User(nickname='joe', email='joe@gmail.com')
g1 = Game(name='coolgame111') 

