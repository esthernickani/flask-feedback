from models import User, Feedback, db
from app import app

#Create all tables

db.drop_all()
db.create_all()
User.query.delete()

#Add User
new_user = User.register(username='amyfiles', pwd='helloworld', first_name='Amy', last_name='Files', email='amyfiles@yahoo.com')

db.session.add(new_user)
db.session.commit()

#Add Feedback
feedback1 = Feedback(title = "testtitle1", content = "This is a test content--1", username='amyfiles')
feedback2 = Feedback(title = "testtitle2", content = "This is a test content--2", username='amyfiles')

db.session.add_all([feedback1, feedback2])
db.session.commit()