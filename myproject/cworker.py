#encoding=utf-8

# -------------------------------------------------------libraries----------------------------------------------------------
# Standard library
import os

# Third-party libraries


# User define module
from app import celery, create_app

# ------------------------------------------------------Global Variables----------------------------------------------------


# -----------------------------------------------------------Main-----------------------------------------------------------
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.app_context().push()