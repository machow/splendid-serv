from app import db
ROLE_USER = 0
ROLE_ADMIN = 1

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

    def add_user(self, user):
        self.players.append(user)
        return self
