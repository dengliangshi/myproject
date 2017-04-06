#encoding=utf-8

# -------------------------------------------------------libraries----------------------------------------------------------
# Standard library
from threading import Thread
from flask import current_app, render_template

# Third-party libraries
from flask_mail import Message

# User define module
from . import mail

# ------------------------------------------------------Global Variables----------------------------------------------------



# -----------------------------------------------------------Main-----------------------------------------------------------
def send_async_email(app, msg):
    """Send emails.
    """
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    """Send email using multible threads.
    """
    app = current_app._get_current_object()
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thread = Thread(target=send_async_email, args=[app, msg])
    thread.start()
    return thread