from datetime import datetime

from flask import Flask, render_template, request, json
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='templates/_')
app.config.from_object('config')
db = SQLAlchemy(app)

#=================================================
# Database
#=================================================

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    beginhit = db.Column(db.Date)
    datastring = db.Column(db.Text)

    def __init__(self, datastring=None):
        self.beginhit = datetime.now()
        if not datastring: self.datastring = datastring


    def __repr__(self):
        return "<Entry %s, Time %s>"%(self.id, self.beginhit)

#=================================================
# Views
#=================================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/testajax')
def testajax():
    u = User(datastring = json.dumps(request.json))
    db.session.add(u)
    db.session.commit()
    return render_template('testajax.html')

@app.route('/submit', methods=['POST'])
def submit():
    print request.json
    return render_template('goodbye.html')

#=================================================
# Run app
#=================================================

if __name__ == '__main__':
    app.run()
