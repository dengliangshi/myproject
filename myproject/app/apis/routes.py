#encoding=utf-8

# -------------------------------------------------------libraries----------------------------------------------------------
# Standard library


# Third-party libraries
from flask_restful import Api

# User define module
from . import api_bp
from resources import *

# ------------------------------------------------------Global Variables----------------------------------------------------
api = Api(api_bp)


# -----------------------------------------------------------Main-----------------------------------------------------------
api.add_resource(Todo, '/todo')                  # an api example