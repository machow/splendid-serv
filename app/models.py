from sqlalchemy.ext.mutable import Mutable
from app import db
ROLE_USER = 0
ROLE_ADMIN = 1

# Class to track changes in Game for db ---------------------------------------
from splendid.classes import Game
class MutableGame(Mutable, Game, object):
    def __init__(self, *args, **kwargs):
        Mutable.__init__(self)
        Game.__init__(self, *args, **kwargs)    

    def __call__(self, *args, **kwargs):
        Game.__call__(self, *args, **kwargs)
        self.changed()
        
    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, MutableGame):
            if isinstance(value, Game):
                return MutableGame(value)
        else: return value

    def __getstate__(self): 
        d = self.__dict__.copy()
        d.pop('_parents', None)
        return d

    def __setstate__(self, state):
        self.__dict__ = state

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        self.changed()

# Database models -------------------------------------------------------------
from datetime import datetime
association = db.Table('association',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('match_id', db.Integer, db.ForeignKey('match.id'))
        )

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index=True, unique = True)
    email = db.Column(db.String(120), index=True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    cdate       = db.Column(db.DateTime, default=datetime.utcnow)

    playing = db.relationship('Match', 
            secondary = association, 
            backref = db.backref('players', lazy = 'dynamic'), 
            lazy = 'dynamic')

    @staticmethod
    def make_unique_nickname(nickname):
        new_nickname = nickname
        version = 2
        while User.query.filter_by(nickname=new_nickname).first() is not None:
            new_nickname = nickname + str(version)
            version += 1
        return new_nickname

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return "<Entry %s, Time %s>"%(self.id, self.cdate)

class Match(db.Model):
    __tablename__ = 'match'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index=True, unique = True)
    is_active = db.Column(db.Boolean, unique=False, default=True)
    creator = db.Column(db.Integer, db.ForeignKey('user.id'))
    summary = db.Column(db.Text)
    #game = db.deferred(db.Column(db.PickleType))
    game = db.Column(MutableGame.as_mutable(db.PickleType))

    @staticmethod
    def make_unique_gamename(gamename):
        new_gamename = gamename
        version = 2
        while Match.query.filter_by(name=new_gamename).first() is not None:
            new_gamename = gamename + str(version)
            version += 1
        return new_gamename
