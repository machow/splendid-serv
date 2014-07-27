from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, current_app
from flask.ext.login import login_user,  current_user, login_required, logout_user
from app import app, db, lm, oid
from forms import LoginForm
from models import User
from config import OPENID_PROVIDERS
import json

@app.before_request
def before_request():
    g.user = current_user
    print 

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('invalid login, please try again')
        return redirect(url_for('login'))
    #check if user in db
    user = User.query.filter_by(email = resp.email).first()
    if not user:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        nickname = User.make_unique_nickname(nickname)
        print nickname
        user = User(nickname = nickname, email = resp.email)
        db.session.add(user)
        db.session.commit()
    #Login
    remember_me = session['remember_me'] if 'remember_me' in session else False
    login_user(user, remember_me)
    return redirect(request.args.get('next') or 'index')
    
# Routes ----------------------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html',
                           user = g.user)
@app.route('/login', methods=["GET", "POST"])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():     # user validation
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        print 'validated'
        print form.openid.data
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ['email', 'nickname'])
    print 'not validated'
    return render_template('login.html', 
                           form=form,
                           providers=OPENID_PROVIDERS)


@app.route('/testajax')
def testajax():
    u = User(games = json.dumps(request.json))
    db.session.add(u)
    db.session.commit()
    return render_template('testajax.html')

@app.route('/submit', methods=['POST'])
def submit():
    print request.json
    return render_template('goodbye.html')
