from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, Email
from wtforms.widgets import TextArea

class RegisterUser(FlaskForm):
    """Form for registering a user"""
    username = StringField("Username", 
                       validators=[DataRequired()])
    password = PasswordField("Password", 
                       validators=[DataRequired()])
    email = EmailField("email", 
                       validators=[DataRequired(), Email()])
    first_name = StringField("First Name", 
                       validators=[DataRequired()])
    last_name = StringField("Last Name", 
                       validators=[DataRequired()])
    
class LoginUser(FlaskForm):
    """Form for log in"""
    username = StringField("Username", 
                       validators=[DataRequired()])
    password = PasswordField("Password", 
                       validators=[DataRequired()])

class AddFeedback(FlaskForm):
    """Form to add feedback"""
    title = StringField("Title", 
                       validators=[DataRequired()])
    feedback = StringField("Feedback", 
                       validators=[DataRequired()],
                       widget=TextArea())
    
class UpdateFeedback(FlaskForm):
    """Form to add feedback"""
    title = StringField("Title")
    content = StringField("Content",
                       widget=TextArea())
    