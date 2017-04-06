#encoding=utf-8

# -------------------------------------------------------libraries----------------------------------------------------------
# Standard library
from flask import Blueprint

# Third-party libraries


# User define module


# ------------------------------------------------------Global Variables----------------------------------------------------
api_bp = Blueprint('api', __name__)    # blueprint for restful apis


# -----------------------------------------------------------Main-----------------------------------------------------------
import routes, httpauth                # import views after creating blueprint for avoiding loops