#encoding=utf-8

# -------------------------------------------------------libraries----------------------------------------------------------
# Standard library
from flask import Blueprint

# Third-party libraries


# User define module


# ------------------------------------------------------Global Variables----------------------------------------------------
main = Blueprint('main', __name__)  # blueprint for main body of this web application


# -----------------------------------------------------------Main-----------------------------------------------------------
import views                        # import views after creating blueprint for avoiding loops