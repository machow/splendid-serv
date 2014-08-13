import os

basedir = os.path.abspath(os.path.dirname(__file__))
savedir = os.path.join(basedir, 'saved')

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'mysql://machow@localhost/foo'#'sqlite:///' + os.path.join(basedir, 'app.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

#SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


DEBUG = True
CSRF_ENABLED = True
SECRET_KEY = 'MASTEROFSECRETZ'

OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]

