from config import basedir
from app import app, db
from app.models import User, Match
import os

class TestCase():
    def setup(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

        u1 = User(nickname='amy', email='amy@gmail.com')
        u2 = User(nickname='bob', email='bob@gmail.com')
        u3 = User(nickname='cat', email='cat@gmail.com')

        self.users = [u1, u2, u3]
        self.games = [Match(name='one'), Match(name='two')]

    def teardown(self):
        db.session.remove()
        db.drop_all()

    def test_association(self):
        g1 = self.games[0]
        for u in self.users: g1.add_user(u)
        for u in self.users: 
            assert u in g1.players.all()
            assert g1 in u.playing.all()


    def test_game_retrieve(self):
        pass
        
