"""
The flask application package.
"""
import logging
from flask import Flask
from config import Config
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
app.config.from_object(Config)

#  Add Logging levels and handlers
app.logger.setLevel(logging.INFO)

# Console handler (works in VS Code + Azure Log Stream)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
))
app.logger.addHandler(console_handler)

# Optional: file handler for local development
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
))
app.logger.addHandler(file_handler)

app.logger.info("Flask application initialized with logging")


# Extensions
Session(app)
db = SQLAlchemy(app)

login = LoginManager(app)
login.login_view = 'login'

import FlaskWebProject.views
