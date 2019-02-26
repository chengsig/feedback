from flask import Flask, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User
#from forms import NewSongForPlaylistForm, SongForm, PlaylistForm
#import bcrypt
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route('/')
def redirect_to_register():
    """redirecting user to register page"""
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """register user: produce form & handle form submission"""
    