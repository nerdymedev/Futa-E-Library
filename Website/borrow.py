from flask import Flask,Blueprint,render_template,redirect,url_for,jsonify,flash,request
from .models import User,BorrowRequest
from . import db
from flask_login import current_user,login_required

borrow = Blueprint('borrow',__name__)

@borrow.route('/get_user',methods=['get'])
def get_user_details():
    reg_no = request.args.get('reg_no')
    user = User.query.filter_by(reg_no=reg_no).first()
    if user:
        return jsonify({
            'email': user.email,
            'name': f"{user.surname} {user.other_names}",
            'department': user.department,
            'level': user.level,
            'year': user.year
        })
    return jsonify({'error': 'User not found'}), 404


@borrow.route('/process_borrow_request', methods=['POST'])
def process_borrow_request():
    reg_no = request.form.get('reg_no')
    book_title = request.form.get('book_title')

    user = User.query.filter_by(reg_no=reg_no).first()
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('index'))

    # Create a new borrow request
    borrow_request = BorrowRequest(user_id=user.id, book_title=book_title)
    db.session.add(borrow_request)
    db.session.commit()

    flash('Borrow request submitted. User needs to accept the request.', 'success')
    return redirect(url_for('index'))

@borrow.route('/student_dashboard', methods=['GET'])
def student_dashboard():
    if current_user.role != 'student':
        flash('Unauthorized access', 'error')
        return redirect(url_for('index'))
    
    # Fetch borrow requests for the logged-in student
    user_id = current_user.id
    borrow_requests = BorrowRequest.query.filter_by(user_id=user_id, status='pending').all()
    
    return render_template('Borrow/student.html', borrow_requests=borrow_requests)