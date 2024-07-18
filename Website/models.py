
from flask_login import UserMixin
from . import db

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    reg_no = db.Column(db.String(20), unique=True, nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    other_names = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    password_changed = db.Column(db.Boolean, default=False, nullable=False)
    
    def get_id(self):
        return str(self.id)
    
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    author = db.Column(db.String(200), nullable=False)
    publisher = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=False)

class BorrowRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')
