from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import pdb

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

bcrypt = Bcrypt()

class User(db.Model):
    """User info"""
    __tablename__ = "users"
    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    username = db.Column(db.String(20), 
                        unique = True,
                        nullable = False)
    password = db.Column(db.String,
                         nullable = False)
    email = db.Column(db.String(50),
                      nullable = False,
                      unique = True)
    first_name = db.Column(db.String(30),
                           nullable = False)
    last_name = db.Column(db.String(30),
                          nullable = False)
    
    feedback = db.relationship('Feedback', backref="user", cascade="all, delete-orphan")
    
    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Register user with hashed password and return user"""
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 =  hashed.decode("utf8")

        return cls(username = username, password = hashed_utf8, email = email, first_name = first_name, last_name = last_name)
    
    @classmethod
    def authenticate(cls, username, pwd):
        """validate that a user exists and password is correct. Return user if valid, else return false"""
        u = User.query.filter_by(username = username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else: 
            return 'false'
        
class Feedback(db.Model):
    """feedback info"""
    __tablename__ = "feedback"
    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    title = db.Column(db.String(20),
                        nullable = False)
    content = db.Column(db.String,
                         nullable = False)
    username = db.Column(db.String, 
                         db.ForeignKey('users.username'))
    
    