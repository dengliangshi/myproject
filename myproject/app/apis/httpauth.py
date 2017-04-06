#encoding=utf-8

# -------------------------------------------------------libraries----------------------------------------------------------
# Standard library
from flask import g, jsonify, abort
from functools import wraps

# Third-party libraries
from flask_httpauth import HTTPBasicAuth

# User define module
from app.apis import api_bp
from app.models import User, AnonymousUser


# ------------------------------------------------------Global Variables----------------------------------------------------
auth = HTTPBasicAuth()


# -----------------------------------------------------------Main-----------------------------------------------------------
@auth.verify_password
def verify_password(email_or_token, password):
    """Verify user using email and address or token, 
    otherwise, set as anonymous user.
    """
    if email_or_token == '':
        g.current_user = AnonymousUser()
        return True
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)

def permission_required(permission):
    """Decorator for specified permission verification.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    """Decorator for admin permission verificaiton.
    """
    return permission_required(Permission.ADMIN)(f)

