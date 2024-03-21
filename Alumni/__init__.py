from flask import Flask
from decouple import config
from flask_bycypt import Bycrypt
from flask_migrate import Migrate
from flask_sqlalchemy SQLAlchemy

app = Flask(__name__)
app.config.from_object(config("APP SETTINGS"))

bycrypt = Bycrypt(app)
db = SQLAlchemy(app)
migrate = migrate(app)

#Registering blueprints
from .accounts.views import accounts_bp
from .core.views import core_bp

app.register_blueprint(accounts_bp)
app.register_blueprint(coer_bp)
