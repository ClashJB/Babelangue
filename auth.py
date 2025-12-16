from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps
from database import UserDatabase

auth = Blueprint('auth', __name__)
db = UserDatabase()

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if db.verify_password(username, password):
            session['username'] = username
            return redirect('/trainer')
        flash('Wrong username or password')
    
    return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if db.create_user(username, email, password):
            session['username'] = username
            return redirect('/trainer')
        flash('Username already exists')
    
    return render_template('signup.html')

@auth.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('auth.login'))