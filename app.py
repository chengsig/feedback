from flask import Flask, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User, Feedback
#from forms import NewSongForPlaylistForm, SongForm, PlaylistForm
from form import RegisterForm, LoginForm, FeedbackForm

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

    if "user_id" in session:
        return redirect(f'/users/{session.get("user_id")}')
    
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

        try:
            db.session.commit()
        except IntegrityError:
            flash("Username already exist! Please try to login")
            return redirect(f'/login')

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
    #redirect user to their own page if already logged in
    if "user_id" in session:
        return redirect(f'/users/{session.get("user_id")}')

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

    if "user_id" not in session:
        return redirect('/login')

    user = User.query.get(username)
    return render_template('user_details.html', user=user)

@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    """delete user"""

    if "user_id" not in session:
        return redirect('/login')
    elif username != session.get('user_id'):
        flash("You can't delete other user!!!")
        return redirect(f'/users/{session.get("user_id")}')

    session.pop("user_id")

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()

    return redirect('/')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    """loading feedback adding form for logged in user"""
    if "user_id" not in session:
        return redirect('/login')

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title=title,
                            content=content, username=username)

        db.session.add(feedback)
        db.session.commit()

        flash("feedback added!")
        return redirect(f'/users/{username}')

    else:
        return render_template('add_feedback.html', form=form, username=username)

@app.route('/feedback/<feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    """update a user's feedback"""
    feedback = Feedback.query.get_or_404(feedback_id)
    if "user_id" not in session:
        return redirect('/login')
    elif feedback.user.username != session.get('user_id'):
        flash("You can't delete feedback that doesn't belong to you")
        return redirect(f'/users/{session.get("user_id")}')

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        flash("feedback updated!")
        return redirect(f'/users/{feedback.user.username}')

    else:
        return render_template('update_feedback.html', form=form, feedback_id=feedback_id)

@app.route('/feedback/<feedback_id>/delete', methods=["POST"])
def delete_feedback(feedback_id):
    """delet the feedback if user is the author of the feedback"""

    feedback = Feedback.query.get_or_404(feedback_id)
    if "user_id" not in session:
        return redirect('/login')
    elif feedback.user.username != session.get('user_id'):
        flash("You can't delete feedback that doesn't belong to you")
        return redirect(f'/users/{session.get("user_id")}')


    db.session.delete(feedback)
    db.session.commit()

    flash("feedback deleted!")
    return redirect(f'/users/{session.get("user_id")}')

