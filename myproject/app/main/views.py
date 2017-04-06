#encoding=utf-8

# -------------------------------------------------------libraries----------------------------------------------------------
# Standard library
from flask import render_template

# Third-party libraries


# User define module
from . import main


# ------------------------------------------------------Global Variables----------------------------------------------------


# -----------------------------------------------------------Main-----------------------------------------------------------
@main.app_errorhandler(404)
def page_not_found(e):
    """Deal with global 404 error.
    """
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def page_not_found(e):
    """Deal with global 500 error.
    """
    return render_template('500.html'), 500

@main.app_errorhandler(403)
def page_not_found(e):
    """Deal with global 403 error.
    """
    return render_template('403.html'), 403

@main.route('/')
def index():
    """Home page.
    """
    return render_template('index.html')