from wtforms import SelectField, StringField, TextField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Optional, Length, Email


class RegisterForm(FlaskForm):
    """Form for user to register"""

    username = StringField('Username:', validators=[InputRequired(),
                                                    Length(max=20)])
    password = TextField('Password:', validators=[InputRequired()])
    email = StringField('Email:', validators=[InputRequired(),
                                              Email()])
    first_name = StringField('First name:', validators=[InputRequired(),
                                                        Length(max=30)])
    last_name = StringField('Last name:', validators=[InputRequired(),
                                                      Length(max=30)])


class LoginForm(FlaskForm):
    """Form for user to login"""

    username = StringField('Username:', validators=[InputRequired(),
                                                    Length(max=20)])
    password = PasswordField('Password:', validators=[InputRequired()])


class FeedbackForm(FlaskForm):
    """Form for adding feedback for logged in user"""

    title = StringField('title', validators=[InputRequired(), 
                                             Length(max=100)])
    content = TextField('content', validators=[InputRequired()])     