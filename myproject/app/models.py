#encoding=utf-8

# -------------------------------------------------------libraries----------------------------------------------------------
# Standard library
from flask import current_app

# Third-party libraries
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# User define module
from app import db, login_manager


# ------------------------------------------------------Global Variables----------------------------------------------------


# -----------------------------------------------------------Main-----------------------------------------------------------
class Permission:
    """Different Perssions.
    """
    API = 0x01                                                            # perssion to acess apis
    ADMIN = 0x80                                                          # admin permission, higest permission


class Role(db.Model):
    """Table for roles.
    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)                          # role id
    name = db.Column(db.String(64), unique=True)                          # role name
    default = db.Column(db.Boolean, default=False, index=True)            # if the default role for new users, only one
    permissions = db.Column(db.Integer)                                   # permissions for this role
    users = db.relationship('User', backref='role', lazy='dynamic')       # relation to the table of users

    @staticmethod
    def insert_roles():
        """Insert roles info, for initialize the this table.
        """
        roles = {
            'User': (Permission.API, True),
            'Admin': (0xff, False)
        }
        for key, value in roles.items():
            role = Role.query.filter_by(name=key).first()
            if role is None: role = Role(name=key)
            role.permissions = value[0]
            role.default = value[1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    """Table for users.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)                          # user's id
    username = db.Column(db.String(64), unique=True, index=True)          # username
    email = db.Column(db.String(64), unique=True, index=True)             # user's email address
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))            # user's role
    password_hash = db.Column(db.String(128))                             # user's password hash string
    confirmed = db.Column(db.Boolean, default=False)                      # if this user's account confirmed by admin

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            # if the email address is the admin's, set him as Admin and no confrimation needed
            if self.email == current_app.config['FLASK_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
                self.confirmed = True
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        """Disable the access to password.
        """
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """Set password.
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Verified password.
        """
        return check_password_hash(self.password_hash, password)

    def confirm(self):
        """Confirmed this user's account by Admin.
        """
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        """Generate token for password reset only with email address.
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        """Reset password with tokens.
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        """Generate token for changing email address.
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        """Change email address using token.
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    def change_username(self, new_username):
        """Change username.
        """
        self.username = new_username
        db.session.add(self)
        return True

    def can(self, permissions):
        """Verify if this user have specified permission.
        """
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        """Verify if this user have admin permission.
        """
        return self.can(Permission.ADMINISTER)

    def generate_auth_token(self, expiration):
        """Generate token for authentication.
        """
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('ascii')

    @staticmethod
    def verify_auth_token(token):
        """Verify the given token for authentication.
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    """For anonymous users.
    """
    def can(self, permissions):
        """Anonymous users have no permissions.
        """
        return False

    def is_administrator(self):
        """Anonymous users, of course, do not have admin permission.
        """
        return False

login_manager.anonymous_user = AnonymousUser                              # anonymous user defination required by login manager


@login_manager.user_loader                                                # function for loading user required by login manager
def load_user(user_id):
    return User.query.get(int(user_id))