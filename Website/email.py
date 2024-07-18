# email.py
from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app
from .models import User
from . import db
from werkzeug.security import generate_password_hash
import string

email = Blueprint('email', __name__)

@email.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        email_address = request.form.get('email')
        reg_no = request.form.get('reg_no')
        surname = request.form.get('surname')
        other_names = request.form.get('other_names')
        department = request.form.get('department')
        level = request.form.get('level')
        year = request.form.get('year')
        user_type = request.form.get('userType')
        print(user_type)

        # Check if email or registration number already exists
        if User.query.filter_by(email=email_address).first() or User.query.filter_by(reg_no=reg_no).first():
            flash('Email or Registration Number already exists.', 'danger')
            return redirect(url_for('email.add_user'))

        
        role = 'admin' if user_type == 'staff' else 'student'

       
        password = surname.upper()
        password_hash = generate_password_hash(password)

        # Create a new user
        new_user = User(email=email_address, reg_no=reg_no, surname=surname, other_names=other_names,
                        department=department, level=level, year=year, password_hash=password_hash, role=role,
                        password_changed=False)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Render the success page with a message
        message = f"User {surname} {other_names} added successfully with role {role}."
        flash(message,'success')
        return render_template('Home/student.html', message=message)
    else:
        return render_template('Home/student.html')  