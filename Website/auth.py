# auth.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        reg_no_or_email = request.form.get('regNo')
        password = request.form.get('password')

        user = User.query.filter((User.email == reg_no_or_email) | (User.reg_no == reg_no_or_email)).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            if user.role in ['Super Admin', 'admin']:
                flash(f'Successfully logged in as {user.role}', 'success')
                return redirect(url_for('views.home'))  
            elif user.role == 'student':
                flash('Successfully logged in as a student!', 'success')
                return redirect(url_for('views.home'))  
            else:
                flash('You do not have the correct privileges.', 'error')
        else:
            flash('Invalid credentials. Please try again.', 'error')

    return render_template('/Auth/index.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out.', 'success')
    return redirect(url_for('auth.login'))
