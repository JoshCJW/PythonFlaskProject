from flask import Flask
from flask import render_template, redirect, url_for, request, flash

from werkzeug.security import generate_password_hash, check_password_hash

from models import User, UserAccount

from flask_login import login_user, logout_user, login_required, current_user
from flask_login import LoginManager
import os

def create_app():
    
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config["MONGO_URI"] = 'mongodb://localhost:27017'

    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(email_id):
        return UserAccount.get_user_byEmail(email_id)
    




    return app