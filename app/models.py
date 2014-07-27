from app import db
ROLE_USER = 0
ROLE_ADMIN = 1

from datetime import datetime
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index=True, unique = True)
    email = db.Column(db.String(120), index=True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    cdate       = db.Column(db.DateTime, default=datetime.utcnow)

    games = db.Column(db.Text)

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
        return "<Entry %s, Time %s>"%(self.id, self.reg_date)
