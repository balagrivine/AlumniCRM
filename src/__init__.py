from flask import Flask
from decouple import config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))

login_manager = LoginManager(app)
#login_manager.init_app(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Registering blueprints
from .accounts.views import accounts_bp
from .core.views import core_bp

app.register_blueprint(accounts_bp)
app.register_blueprint(core_bp)

#default funciton to handle the login process
login_manager.login_view = "accounts.login"

#customize the message directory
login_manager.login_message_category = "danger"

#creating the user_loader callback
from src.accounts.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
