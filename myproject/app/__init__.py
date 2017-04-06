#encoding=utf-8

# -------------------------------------------------------libraries----------------------------------------------------------
# Standard library
from flask import Flask

# Third-party libraries
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from celery import Celery

# User define module
from config import config

# ------------------------------------------------------Global Variables----------------------------------------------------
bootstrap = Bootstrap()                                     # Bootstrap template
moment = Moment()                                           # time
db = SQLAlchemy()                                           # database model
mail = Mail()

celery = Celery(__name__)                                   # instance of celery

login_manager = LoginManager()
login_manager.session_protection = 'strong'                 # level of security, None, basic, strong
login_manager.login_view = 'auth.login'                     # login page for login_required

# -----------------------------------------------------------Main-----------------------------------------------------------
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])             # configure application
    config[config_name].init_app(app)

    celery.conf.update(app.config)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    from main import main as main_bp                        # register the blueprint for main body
    app.register_blueprint(main_bp)

    from auth import auth as auth_bp                        # register the blueprint for authenticaiton module
    app.register_blueprint(auth_bp)

    from apis import api_bp                                 # register the blueprint for restful apis
    app.register_blueprint(api_bp, url_prefix="/api")
    
    return app