from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app.extensions import db, bcrypt
from app.models import User, Post
from app.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm)
from app.users.utils import save_picture, send_reset_email

users = Blueprint('users',__name__)

# Register Page
@users.route("/register", methods=['GET','POST'])
def register():

    # If user already is logged in return to home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm() # Initialize Registration FOrm and pass it to html template
    
    # Ths will check if it is a POST request and if it is valid.
    if form.validate_on_submit():
        # Create User Object (account) and save to Database
        # Before saving user details, password should be hashed
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # UTF-8 makes the hash string instead of bytes
        newUser = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(newUser)
        db.session.commit()

        flash(f'Account created, you can now log in!', 'success')
        return redirect(url_for('users.login'))

    return render_template('register.html', title='Register', form=form)

# Login Page
@users.route("/login", methods=['GET','POST'])
def login():

    # If user already is logged in return to home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm() # Initialize Login FOrm and pass it to html template

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # If a user with given email exists and password is correct login
        if user and bcrypt.check_password_hash(user.password,form.password.data):
             login_user(user, remember=form.remember.data)   # FLaskLogin handles all sessions stuff
             flash(f'Logged in succesfully', 'success')

             next_page = request.args.get('next')

             return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
             flash(f'The combination of Email and Password is not correct, Try again', 'danger')

    return render_template('login.html', title='Login', form=form)

# Logout Route
@users.route("/logout")
def logout():
    logout_user()
    flash(f'Logged out succesfully', 'info')
    return redirect(url_for('main.home'))

# My Acount route
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # If there is a profile pic passed save it
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        # Load with initial values if GET request
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

# Get All Posts for given username
@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)

#### ROUTES FOR RESET_PASSWORD and Sending mail with token ####
# Send password reset request via mail and generate token
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

# Verify token and Reset password route
@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)