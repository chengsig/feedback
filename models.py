from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """create User class"""

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedbacks = db.relationship("Feedback",
                        backref="user",
                        cascade="all, delete-orphan",
                        single_parent=True)

    @classmethod
    def register(cls, username, pwd, email, fname, lname):
        """register user w/hashed password & return user"""

        hashed = bcrypt.generate_password_hash(pwd)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")
        # return instance of user

        return cls(username=username, password=hashed_utf8,
                    email=email, first_name=fname, last_name=lname)

    @classmethod
    def authenticate(cls, username, pwd):
        """validates that user exists and password is correct
        return user if valid, else returns false"""

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False

class Feedback(db.Model):
    """create class of feedback"""

    __tablename__ = "feedbacks"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    title = db.Column(db.String(100),
                        nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    username = db.Column(db.String(20),
                            db.ForeignKey('users.username'), nullable=False)

    # user = db.relationship("User",
    #                         backref="feedbacks",
    #                         cascade="all, delete-orphan",
    #                         single_parent=True) #check the direction of cascade delete is correct later!!

