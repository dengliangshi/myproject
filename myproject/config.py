#encoding=utf-8

# -------------------------------------------------------libraries----------------------------------------------------------
# Standard library
import os
import logging
from logging.handlers import SMTPHandler

# Third-party libraries


# User define module


# ------------------------------------------------------Global Variables----------------------------------------------------
basedir = os.path.abspath(os.path.dirname(__file__))                      # the root path


# -----------------------------------------------------------Main-----------------------------------------------------------
class Config(object):
    """Base class for configuration.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY')                             # secret key for generating token
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True                                  # update database automatically
    SQLALCHEMY_TRACK_MODIFICATIONS = False                                # disenable tracking modifications of objects
    SQLALCHEMY_RECORD_QUERIES = True                                      # disable or enable query recording
    
    SSL_DISABLE = True                                                    # disable SSL(Secure Sockets Layer)

    MAIL_SERVER = 'smtp.163.com'                                          # email server(smtp)
    MAIL_PORT = 25                                                        # port number of email server
    MAIL_USE_TLS = True                                                   # if using TLS(Transport Layer Security)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')                       # username to login email server
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')                       # password to login email server
    MAIL_SUBJECT_PREFIX = '[MyProject]'                                   # prefix for email's subject
    MAIL_SENDER = 'Admin <example@163.com>'                               # email sender display string
    FLASK_ADMIN = os.environ.get('FLASK_ADMIN')                           # administrator's email address

    BROKER_URL = 'redis://localhost:6379/0',                              # broker for celery
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'                    # backend for celery
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_ACCEPT_CONTEN = ['json']
    CELERY_RESULT_SERIALIZE = 'json'
    CELERY_TIMEZONE = 'Asia/Shanghai'
    CELERY_ENABLE_UTC = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """Configuration for development phrase.
    """
    DEBUG = True                                                          # enable debug model
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'database/data-dev.sqlite')  # absolute path of database file


class TestingConfig(Config):
    """Configuration for testing phrase.
    """
    TESTING = True                                                        # enable test model
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'database/data-test.sqlite')
    WTF_CSRF_ENABLED = False                                              # disable CSRF protection during testing
    # CSRF - Cross-site Request Forgery

class ProductionConfig(Config):
    """Configuration for production environment.
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'database/data.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # email errors to the administrator.
        credentials, secure= None, None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.MAIL_SENDER,
            toaddrs=[cls.FLASK_ADMIN],
            subject=cls.MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


class UnixConfig(ProductionConfig):
    """Configuration for running on unix platform.
    """
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


# configuration mapping for diffrent cases
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'unix': UnixConfig,
    'default': DevelopmentConfig
}