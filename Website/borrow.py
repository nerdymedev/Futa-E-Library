from flask import Flask,Blueprint,render_template,redirect,url_for,jsonify,flash,request
from .models import User,Book

borrow = Blueprint('borrow',__name__)

@borrow.route('/get_user',methods=['POST'])
def get_user():
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

