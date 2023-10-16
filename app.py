from flask import Flask, render_template, redirect, request, session, flash
"""from flask_debugtoolbar import DebugToolbarExtension"""
from models import db, connect_db, User, Feedback
from forms import RegisterUser, LoginUser, AddFeedback, UpdateFeedback
import pdb

app = Flask(__name__, template_folder = "templates")

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.app_context().push()

connect_db(app)

app.config['SECRET_KEY'] = "hellothere"
"""toolbar = DebugToolbarExtension(app)"""

@app.route('/')
def redirect_to_register():
    """Redirect to register route"""
    return redirect('/register')

@app.route('/register', methods = ['GET', 'POST'])
def show_register_form():
    """show form to register user and add user to db and then show secret page or if form does not get validated, show register form again"""
    form = RegisterUser()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        new_user = User.register(username = username, pwd = password, first_name = first_name, last_name = last_name, email = email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(f"/users/{username}")
    else:
        return render_template('register.html', form=form)
    
@app.route('/login', methods = ['GET', 'POST'])
def show_login_form():
    """show form to login user and authenticate user"""
    form = LoginUser()
    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data

        user = User.authenticate(username, pwd)

        if user:
            session["user_id"] = user.id #keep logged in
            return redirect(f"/users/{username}")
        else:
            form.username.errors = ['Bad name or password']
    return render_template('login.html', form=form)
    
@app.route('/users/<username>')
def show_secret(username):
    """show form to login user and authenticate user"""
    if "user_id" not in session:
        flash('You must be logged in to view')
        return redirect('/login')
    else:
        current_user = User.query.filter_by(username = username).first()
        feedback = Feedback.query.filter_by(username = username).all()
        return render_template('/secret.html', user = current_user, feedbacks = feedback)
    
@app.route('/logout')
def logout():
    """logout user and redirect to home"""
    session.pop('user_id')
    return redirect('/')

@app.route('/users/<username>/delete', methods = ['POST'])
def delete_user(username):
    """show form to login user and authenticate user"""
    if "user_id" not in session:
        return redirect('/login')
    else:
        Feedback.query.filter_by(username = username).delete()
        db.session.commit()
        User.query.filter_by(username = username).first()
        return redirect('/')
    
@app.route('/users/<username>/feedback/add', methods = ['GET', 'POST'])
def handle_feedback(username):
    form = AddFeedback()
    current_user = User.query.filter_by(username = username).first()
    if "user_id" in session:
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data

            new_feedback = Feedback(title = title, content = content, username = username)
            db.session.add(new_feedback)
            db.session.commit()
        else:
            return render_template('/feedback.html', form = form)
    else:
        return redirect('/login') 

@app.route('/feedback/<feedback_id>/update', methods = ['GET', 'POST'])
def update_feedback(feedback_id):
    form = UpdateFeedback()
    feedback = Feedback.query.get_or_404(feedback_id)
    
    if "user_id" in session:
        if form.validate_on_submit():
            title = form.title.data if form.title.data else feedback.title
            content = form.content.data if form.content.data else feedback.content
            
            feedback.title = title
            feedback.content = content

            db.session.commit()

            current_user = User.query.filter_by(username = feedback.username).first()
            feedback = Feedback.query.filter_by(username = feedback.username).all()
            return render_template('/secret.html', user = current_user, feedbacks = feedback)
        else:
            return render_template('/feedback.html', form = form, feedback = feedback)
    else:
        return redirect('/login') 
    
@app.route('/feedback/<feedback_id>/delete', methods = ['GET', 'POST'])
def delete_feedback(feedback_id):
    if "user_id" in session:
        feedback = Feedback.query.get(feedback_id)
        username = feedback.username 

        Feedback.query.filter(Feedback.id == feedback_id).delete()
        db.session.commit()
        return redirect(f"/users/{username}") 
    else:
        return redirect('/login') 