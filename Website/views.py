from flask import Flask,Blueprint,render_template,url_for,request,redirect,flash
from flask_login import login_required as lr
from .models import User
from flask_login import current_user
from werkzeug.security import generate_password_hash
from . import db

views = Blueprint('views', __name__)

@views.route('/')
@lr
def home():
    user=current_user
    print(user.role)
    return render_template('/Home/index.html',user=user)

@views.route('/profile',methods=['GET','POST'])
@lr
def profile_page():
    user = User.query.get(current_user.id)
    return render_template('Profile/index.html', user=user)

@views.route('/change_password', methods=['GET','POST'])
@lr
def change_password():
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    

    if new_password != confirm_password:
        flash('Passwords do not match!', 'danger')
        return redirect(url_for('profile.profile_page'))

    current_user.password_hash = generate_password_hash(new_password)
    current_user.password_changed = True
    db.session.commit()
    
    flash('Password changed successfully!', 'success')
    return redirect(url_for('views.profile_page'))

@views.route('/borrowed_book')
@lr
def borrowed_book():
    return render_template('Profile/borrow.html')
