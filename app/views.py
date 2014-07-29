from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, current_app
from flask.ext.login import login_user,  current_user, login_required, logout_user
from app import app, db, lm, oid
from forms import LoginForm
from models import User
from config import OPENID_PROVIDERS
import json
import pickle


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

# Routes ----------------------------------------------------------------------
from splendid.classes import Game
from splendid.classes import MoveError

G = pickle.load(open('game_default.pickle', 'rb'))
CRNT_GAMES = {}

@app.route('/')
def index():
    return render_template('index.html',
                           user = g.user)

@login_required
@app.route('/game', methods=['GET', 'POST'])
@app.route('/game/<game_name>', methods=['GET', 'POST'])
def game(game_name=''):
    if game_name: game = CRNT_GAMES[game_name]
    return render_template('game.html', CRNT_GAMES = CRNT_GAMES, 
                                         game_name = game_name,
                                         user = g.user)

@login_required
@app.route('/newgame', methods=['GET', 'POST'])
def newgame():
    args = request.form or request.args

    name = args.get('name') or 'default'
    players = [player for k, player in args.items() if 'player' in k]
    add_gems = args.get('add_gems')
    # MAKE SURE PLAYERS EXIST
    for pname in players:
        if not User.query.filter_by(nickname=pname).all():
            raise BaseException("return warning here")

    if name not in CRNT_GAMES:
        print players
        print type(players)
        G = pickle.load(open('game_default.pickle', 'rb'))
        G.start(players, add_gems)
        CRNT_GAMES[name] = G
    return redirect('/game/%s'%name)

@login_required
@app.route('/info', methods=['GET', 'POST'])
def info():
    args = request.json or request.args
    nickname = args.get('nickname')

    if nickname:
        u = User.query.filter_by(nickname=nickname).first()
        if u: 
            active = [game.name for game in u.playing if game.is_active]
            not_active = [game.name for game in u.playing if game.is_active]
            return jsonify({'nickname':u.nickname,
                            'active': active,
                            'previous': not_active})
        else:
            return jsonify({'nickname':None})
    else:
        nicknames = [name[0] for name in db.session.query(User.nickname).all()]
        return jsonify({'nicknames': nicknames})

@app.route('/test', methods=['GET', 'POST'])
def test():
    return jsonify(request.args)


@login_required
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    game_name = request.json.get('game')
    commands  = request.json.get('commands').split(" ")

    print CRNT_GAMES.keys()
    G = CRNT_GAMES.get(game_name)
    if G: 
        print "game exists"
        print G._players
    else: return render_template('404.html')

    if g.user.nickname not in [p.name for p in G._players]: 
        "player not in game..."
        return jsonify({'error_code': 1, 'value':'move by non-game player'})

    print g.user
    g.user.nickname
    try: 
        if g.user.nickname != G.crnt_player.name: 
            raise MoveError(106, 'it is the turn of %s'%G.crnt_player.name)
        cmd = commands[0]
        line = " ".join(commands[1:])
        G(cmd, line)
        print G
        outputs = G.output()
        return jsonify(outputs)
    except MoveError as e:
        print e.code
        print e.value
        return jsonify({'error_code': e.code, 'value': e.value})
