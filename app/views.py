from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, current_app
from flask.ext.login import login_user,  current_user, login_required, logout_user
from app import app, db, lm, oid
from forms import LoginForm
from models import User, Match
from config import OPENID_PROVIDERS, savedir
import json
import pickle


@app.before_request
def before_request():
    g.user = current_user

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
        # use nickname given in form, else openID nickname
        nickname = session.get('nickname') or resp.nickname
        # worst case scenario, use email address, cropped at @
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

# at some point I should replace this with a proper cache
CRNT_GAMES = {}
def load_games(crnt_games):
    matches = [m.name for m in Match.query.filter_by(is_active = True).all()]
    # load matches that are active but are not in dictionary
    for m in matches:
        if m not in crnt_games:
            print 'loading ' + m
            CRNT_GAMES[m] = Game.load(savedir + '/' + m)
    # remove matches that are no longer active
    for key in CRNT_GAMES.keys():
        if key not in matches: 
            print 'removing ' + key
            del CRNT_GAMES[key]

load_games(CRNT_GAMES)

@app.route('/')
def index():
    return render_template('index.html',
                           user = g.user)

@app.route('/profile/<nickname>')
def profile(nickname):
    #look up matches by active not active
    u = User.query.filter_by(nickname=nickname).first()
    if u: 
        active = [match for match in u.playing if match.is_active]
        not_active = [match for match in u.playing if not match.is_active]
    else:
        active, not_active = [],[]

    return render_template('profile.html', 
                            nickname=nickname,
                            active=active,
                            not_active=not_active)

@app.route('/game', methods=['GET', 'POST'])
@app.route('/game/<game_name>', methods=['GET', 'POST'])
def game(game_name=''):
    load_games(CRNT_GAMES)
    if game_name: game = CRNT_GAMES[game_name]
    return render_template('game.html', CRNT_GAMES = CRNT_GAMES, 
                                         game_name = game_name,
                                         user = g.user)

@app.route('/game2/<game_name>', methods=['GET', 'POST'])
@login_required
def game2(game_name=''):
    load_games(CRNT_GAMES)
    if game_name: game = CRNT_GAMES[game_name]
    return render_template('game2.html', CRNT_GAMES = CRNT_GAMES, 
                                         game_name = game_name,
                                         user = g.user)

@app.route('/newgame', methods=['GET', 'POST'])
@login_required
def newgame():
    """Create new game from request. Commit new game to db, save to fold.

    Form Parameters:
        name: new game name
        player{1,2,..}: players to add (e.g. /newgame?player1=joe&player2=sally)
        add_gems: gems to add to default (e.g. rgbbb)

    If game exists, redirect to game with that name.
    """
    # PARSE FORM INPUTS
    args = request.form or request.args

    name = args.get('game') or 'default'
    players = [player for k, player in args.items() if 'player' in k and player]
    add_gems = args.get('add_gems') or ""
    # MAKE SURE PLAYERS EXIST
    users = []
    for pname in players:
        u = User.query.filter_by(nickname=pname).first()
        if not u: raise BaseException("invalid player name, %s"%pname)
        else: users.append(u)

    if name not in CRNT_GAMES:
        print players
        print type(players)
        # create game
        G = pickle.load(open('game_default.pickle', 'rb'))
        G.start(players, add_gems)
        # create db entry
        m = Match(name=name, is_active=True, creator=g.user.id)
        m.players.extend(users)
        db.session.add(m)
        db.session.commit()
        # save initial copy of game and add to game dict
        G.save(savedir + '/' + name)
        CRNT_GAMES[name] = G

    return redirect('/game/%s'%name)

@app.route('/info', methods=['GET', 'POST'])
@login_required
def info():
    """Return json info for specified player. If no player given, return all. 
    If invalid player, return dict with None.

    Form Parameters:
        nickname:   Player nickname
    """
    
    args = request.json or request.args
    nickname = args.get('nickname')

    if nickname:
        u = User.query.filter_by(nickname=nickname).first()
        if u: 
            active = [match.name for match in u.playing if match.is_active]
            not_active = [match.name for match in u.playing if match.is_active]
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
    print request.args.get('nickname')
    return jsonify(request.args)



@app.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    """Submit game turn.

    Form Parameters:
        game:   game to submit turn for.
        commands:   string with commands (fed to Game.__call__). First word is move.
                    Following words are move arguments.
    """
    game_name = request.json.get('game')
    commands  = request.json.get('commands').split(" ")

    G = CRNT_GAMES.get(game_name)
    if G: 
        print "game exists"
        print G._players
    else: return render_template('404.html')

    if not commands[0]:
        return jsonify(G.output())

    if g.user.nickname not in [p.name for p in G._players]: 
        "player not in game..."
        return jsonify({'error_code': 1, 'text':'move by non-game player'})

    try: 
        # Run player move -----------------------------------------------------
        if g.user.nickname != G.crnt_player.name and g.user.nickname != 'plasticandglass': #TODO remove plasticandglass 
            raise MoveError(110, text='it is the turn of %s'%G.crnt_player.name)
        cmd = commands[0]
        line = " ".join(commands[1:])
        G(cmd, line)
        G.save(savedir + '/' + game_name)

        # Post move wrap-up ---------------------------------------------------
        m = Match.query.filter_by(name = game_name).first()
        # End game if winner
        if G.winner:
            m.is_active = False
        # Update match summary text
        m.summary = str(G)
        db.session.add(m)
        db.session.commit()
        # Output JSON game data
        outputs = G.output()
        return jsonify(outputs)
    except MoveError as e:
        print e.code
        print e.value
        return jsonify({'error_code': e.code, 'value': e.value, 'text':e.text})

@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete_it():
    game_name = request.args.get('game')
    m = Match.query.filter_by(name = game_name).first()
    if game_name and (g.user.id == m.creator):
        m.is_active = False
        db.session.add(m)
        db.session.commit()
    else:
        print "could not delete, put more informative message here"
    return jsonify({'game': game_name})
