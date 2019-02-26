from models import db, User, Feedback
from app import app

# Create all tables
db.create_all()

# If table isn't empty, empty it
# User.query.delete()
# Feedback.query.delete()

# Add pet
whiskey = User.register(username='whiskey', pwd='popcorn', email='whiskey@dog.com', fname='Whiskey', lname='The Dog')
spike = User.register(username='spike', pwd='popcorn', email='spike@porcupine.com', fname='Spike', lname='The Porcupine')

# Add feedback
feedback1 = Feedback(title='woof', content='I love snacks!', username='whiskey')
feedback2 = Feedback(title='Hi!', content='I love snacks!', username='whiskey')
feedback3 = Feedback(title='woof', content='I love snacks!', username='spike')
feedback4 = Feedback(title='Hi!', content='I love snacks!', username='spike')


db.session.add(whiskey)
db.session.add(spike)
db.session.add(feedback1)
db.session.add(feedback2)
db.session.add(feedback3)
db.session.add(feedback4)

# Commit--otherwise, this never gets saved!
db.session.commit()