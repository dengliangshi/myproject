#encoding=utf-8

# -------------------------------------------------------libraries----------------------------------------------------------
# Standard library
from functools import wraps
from flask import abort

# Third-party libraries
from flask_login import current_user

# User define module
from models import Permission

# ------------------------------------------------------Global Variables----------------------------------------------------


# -----------------------------------------------------------Main-----------------------------------------------------------
def permission_required(permission):
    """Decorator for permission verification.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    """Decorator for admin permission verificaiton.
    """
    return permission_required(Permission.ADMIN)(f)
