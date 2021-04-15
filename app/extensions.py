from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()                # Initialize Database Object
bcrypt = Bcrypt()                # Initialize Password Bcrypt object
login_manager = LoginManager()   # Initialize Flask Login Manager for session and auth etc.
login_manager.login_view = "users.login"
login_manager.login_message_category='info'
mail = Mail()
