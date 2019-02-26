from flask import Flask, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User
#from forms import NewSongForPlaylistForm, SongForm, PlaylistForm
from form import RegisterForm, LoginForm

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

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password,
                                email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.username

        flash("Registered!")
        return redirect(f'/users/{username}')

    else:
        return render_template('register_form.html', form=form)

@app.route('/secret')
def show_secret():
    """shows the secret page"""

    if "user_id" not in session:
        return redirect('/login')


    return "You made it!"

@app.route('/login', methods=["GET", "POST"])
def login_user():
    """login user: produce form & handle form submission"""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["user_id"] = user.username
            flash("Logged in!")
            return redirect(f'/users/{username}')
        else:
            flash("Invalid username/password")
            return redirect('/login')

    else:
        return render_template('login_form.html', form=form)

@app.route('/logout')
def logout_user():
    """ logout user from current session and redirect to '/' """

    session.pop("user_id")
    return redirect('/')

@app.route('/users/<username>')
def display_user_detail(username):
    """display a user's detailed information when logged in"""
    user = User.query.get(username)
    return render_template('user_details.html', user=user)