from flask import Flask,Blueprint,render_template,redirect,url_for,jsonify,flash,request
from .models import User,BorrowRequest
from . import db
from flask_login import current_user,login_required

borrow = Blueprint('borrow',__name__)


admin_borrowed_url = 'views.borrowed_book'

@borrow.route('/get_user',methods=['get'])
def get_user_details():
    reg_no = request.args.get('reg_no')
    user = User.query.filter_by(reg_no=reg_no).first()
    if user:
        return jsonify({
            'email': user.email,
            'name': user.full_name,
            'department': user.department,
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
    already_owing_book = BorrowRequest.query.filter_by(user_id=user.id,status='accepted').first()
    if already_owing_book:
        flash(f'User already owes a book: {already_owing_book.book_title}', 'error')
        return redirect(url_for(admin_borrowed_url))

    # Create a new borrow request
    borrow_request = BorrowRequest(user_id=user.id, book_title=book_title)
    db.session.add(borrow_request)
    db.session.commit()

    flash('Borrow request submitted. User needs to accept the request.', 'success')
    return redirect(url_for(admin_borrowed_url))


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


@borrow.route('/return_book', methods=['GET', 'POST'])
@login_required
def return_book_view():
    borrow_requests = None

    if request.method == 'POST':
        reg_number = request.form.get('reg_number')

        # Fetch user based on registration number
        user = User.query.filter_by(reg_no=reg_number).first()

        if not user:
            flash('User with provided registration number not found.', 'error')
            return redirect(url_for('borrow.return_book_view'))

        # Fetch borrow requests for the user
        borrow_requests = BorrowRequest.query.filter_by(user_id=user.id).all()

    return render_template('Borrow/return.html', borrow_requests=borrow_requests)

@borrow.route('/returned_borrow/<int:request_id>', methods=['POST'])
@login_required
def decline_borrow(request_id):
    borrow_request = BorrowRequest.query.get_or_404(request_id)

    # Update status to declined and save changes
    borrow_request.status = 'Returned'
    db.session.commit()

    flash('Borrow request has been marked as returned.', 'success')
    return redirect(url_for('borrow.return_book_view'))