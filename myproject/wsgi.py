#encoding=utf-8

# -------------------------------------------------------libraries----------------------------------------------------------
# Standard library
import os

# Third-party libraries


# User define module


# ------------------------------------------------------Global Variables----------------------------------------------------



# -----------------------------------------------------------Main-----------------------------------------------------------
if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from myproject import app