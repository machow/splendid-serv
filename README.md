Flask Test Server
========================
This simple [Flask](http://flask.pocoo.org/) server was made to be a simple template for testing javascript
apps, ajax calls, etc..

Dependencies
----------------------
The necessary libraries are listed in `requirements.txt`. After setting up and activating
a new [virtual environment](http://www.virtualenv.org/en/latest/virtualenv.html) (or living
dangerously!), run `pip -r requirements.txt` to install them.

Setup
-----------------------
Set up the database by running `db_create.py` from the project directory. Replace `templates/index.html`
with whatever page you want to test. Put static files in `templates/_`, or change the `static_folder`
argument when initializing Flask in `app.py`.

Running
-----------------------
To start the server, run `app.py`.
