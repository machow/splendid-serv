from config import basedir
from app import app, db
from app.models import User, Game
import os

class TestCase():
    def setup(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def teardown(self):
        db.session.remove()
        db.drop_all()

    def test_newgame(self):
        u1 = User(nickname='joe', email='joe@gmail.com')
        u2 = User(nickname='amy', email='amy@gmail.com')
        g1 = Game(name='reallycool111')
        for u in [u1, u2]: g1.add_user(u)
        for u in [u1, u2]: assert u in g1.players.all()
    
