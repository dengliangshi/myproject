#encoding=utf-8

# -------------------------------------------------------libraries----------------------------------------------------------
# Standard library
from flask import Blueprint

# Third-party libraries


# User define module


# ------------------------------------------------------Global Variables----------------------------------------------------
auth = Blueprint('auth', __name__)  # blueprint for authentication module


# -----------------------------------------------------------Main-----------------------------------------------------------
import views                        # import views after creating blueprint for avoiding loops