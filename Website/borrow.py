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

    # Check if the user already owes a book
    already_owing_book = BorrowRequest.query.filter_by(user_id=user.id).first()
    if already_owing_book:
        flash(f'User already owes a book: {already_owing_book.book_title}', 'error')
        return redirect(url_for('index'))

    # Create a new borrow request
    borrow_request = BorrowRequest(user_id=user.id, book_title=book_title)
    db.session.add(borrow_request)
    db.session.commit()

    flash('Borrow request submitted. User needs to accept the request.', 'success')
    return redirect(url_for('views.borrowed_book'))


@borrow.route('/student_dashboard', methods=['GET'])
@login_required
def student_dashboard():
    if current_user.role != 'student':
        flash('Unauthorized access', 'error')
        return redirect(url_for('index'))
    
    # Fetch all borrow requests for the logged-in student
    user_id = current_user.id
    all_borrow_requests = BorrowRequest.query.filter_by(user_id=user_id).all()
    
    return render_template('Borrow/student.html', borrow_requests=all_borrow_requests) 


@borrow.route('/accept_request/<int:request_id>', methods=['POST'])
@login_required
def accept_request(request_id):
    borrow_request = BorrowRequest.query.get_or_404(request_id)
    
    # Update status to accepted and save changes
    borrow_request.status = 'accepted'
    db.session.commit()
    
    flash('Borrow request accepted successfully.', 'success')
    return redirect(url_for('borrow.student_dashboard'))

@borrow.route('/decline_request/<int:request_id>', methods=['POST'])
@login_required
def decline_request(request_id):
    borrow_request = BorrowRequest.query.get_or_404(request_id)
    
    # Update status to declined and save changes
    borrow_request.status = 'declined'
    db.session.commit()
    
    flash('Borrow request declined.', 'success')
    return redirect(url_for('borrow.student_dashboard'))
