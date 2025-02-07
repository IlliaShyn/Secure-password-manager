from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import db, bcrypt, login_manager
from flask_login import login_user, logout_user, login_required
from app.models import User

#############################
main = Blueprint('main', __name__)

@main.route('/')
@login_required
def home():
    return render_template('index.html', title="Password Manager")
#############################
auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid credentials. Try again.', 'danger')

    return render_template('login.html', title="Login")

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists.', 'warning')
        else:
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('signup.html', title="Signup")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

#############################
settings = Blueprint('settings', __name__)

@settings.route('/')
def set():
    return render_template('settings.html', title="Settings")

profile = Blueprint('profile', __name__)

@profile.route('/')
def profile():
    return render_template('profile.html', title="Profile")