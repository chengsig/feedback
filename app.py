from flask import Flask, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User
#from forms import NewSongForPlaylistForm, SongForm, PlaylistForm
#import bcrypt
from flask_bcrypt import Bcrypt
from form import RegisterForm

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

    form = RegisterForm()
    print(form.validate_on_submit(), form.errors)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        print(last_name)
        new_user = User.register(username, password, 
                                email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/secret')

    else:
        return render_template('register_form.html', form=form)
