# __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_login import LoginManager
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash
from flask_admin import Admin


db = SQLAlchemy()
DB_NAME = "database.db"
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_default_secret_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from .views import views
    from .auth import auth  
    from .email import email
    app.register_blueprint(email,url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    app.register_blueprint(views, url_prefix='/')
    
    admin = Admin(app)
    
    from .models import User 
    create_database(app)

    with app.app_context():
        if len(User.query.all()) < 1:
            hashed_password = generate_password_hash('Scriptpythonic', method='scrypt', salt_length=8)
            # Create the admin user
            admin_user = User(
                email='Admin@gmail.com',
                reg_no='000001',
                surname='Admin',
                other_names='Super',
                department='Admin Department',
                level=0,
                year=2024,
                password_hash=hashed_password,
                role='Super Admin'
            )
            
            db.session.add(admin_user)
            db.session.commit()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User  
        return User.query.get(int(user_id))

    return app

def create_database(app):
    with app.app_context():
        if not path.exists('Website/' + DB_NAME):
            db.create_all()
