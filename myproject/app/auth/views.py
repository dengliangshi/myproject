#encoding=utf-8

# -------------------------------------------------------libraries----------------------------------------------------------
# Standard library
from flask import render_template, session, redirect, url_for, request, flash, current_app, abort

# Third-party libraries
from flask_login import login_user, logout_user, login_required, current_user

# User define module
from . import auth
from app import db
from forms import *
from app.models import User, Role
from app.email import send_email
from app.decorators import admin_required


# ------------------------------------------------------Global Variables----------------------------------------------------


# -----------------------------------------------------------Main-----------------------------------------------------------
@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Register page. 
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        send_email(current_app.config['FLASK_ADMIN'], 'New Register Request',
                   'auth/email/confirm', user=user)
        flash('Your register request has been sent to adminstrator by email.')
        return redirect(url_for('.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Log in page.
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            if not user.confirmed:  # account did not confirmed by admin cannot login
                flash('Your register request has not been confirmed by administrator yet.')
                return render_template('auth/login.html', form=form)
            return redirect(request.args.get('next') or url_for('.profile'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    """Log out page.
    """
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/manage', methods=['GET', 'POST'])
@admin_required
def manage():
    """Manage all users' info, need administrator permission.
    """
    users = User.query.all()
    roles = Role.query.all()
    return render_template('auth/manage.html', users=users, roles=roles)


@auth.route('/delete/<user_id>', methods=['GET', 'POST'])
@admin_required
def delete(user_id):
    """Delete user by specified id, need administrator permission.
    """
    user = User.query.filter_by(id=user_id).first()
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        flash('You have deleted the account of "%s".' % user.username)
    return redirect(url_for('.manage'))


@auth.route('/change_role/<int:user_id>/<new_role>', methods=['GET', 'POST'])
@admin_required
def change_role(user_id, new_role):
    """Change user's role, need administrator permission.
    """
    user = User.query.filter_by(id=user_id).first()
    if user is not None and user.role.name != new_role:
        role = Role.query.filter_by(name=new_role).first()
        if role is not None:
            user.role = role
            db.session.commit()
            flash('The role of %s has been change to %s.' % (user.username, new_role))
    return redirect(url_for('.manage'))


@auth.route('/confirm/<user_id>')
@admin_required
def confirm(user_id):
    """Active new user's account.
    """
    user = User.query.filter_by(id=user_id).first()
    if user is not None:
        user.confirm()
        send_email(user.email, 'Your Register Request Passed',
                   'auth/email/confirmed', user=user)
        flash('You have confirmed the account of "%s".' % user.username)
    return redirect(url_for('.manage'))


@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Profile page for all active users.
    """
    admin =False
    if current_user.role.name == 'Admin':
        admin = True
    return render_template('auth/profile.html', user=current_user, admin=admin)


@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change password when user knows his/her password.
    """
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password has been updated.')
            return redirect(url_for('.profile'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    """Request for reseting password when user forget his/her password.
    """
    if not current_user.is_anonymous:
        return redirect(url_for('.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
        flash('An email with instructions to reset your password has been '
              'sent to you.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    """Reset password using token.
    """
    if not current_user.is_anonymous:
        return redirect(url_for('.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('.index'))
        if user.reset_password(token, form.password.data):
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change_email_request', methods=['GET', 'POST'])
@login_required
def change_email_request():
    """Request for Changing email address.
    """
    form = ChangeEmailForm()
    if form.validate_on_submit():
        new_email = form.email.data
        token = current_user.generate_email_change_token(new_email)
        send_email(new_email, 'Confirm your email address',
                   'auth/email/change_email',
                   user=current_user, token=token)
        flash('An email with instructions to confirm your new email '
                  'address has been sent to you.')
        return redirect(url_for('.profile'))
    return render_template("auth/change_email.html", form=form)


@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    """Change email address using token.
    """
    if current_user.change_email(token):
        flash('Your email address has been updated.')
    else:
        flash('Invalid request.')
    return redirect(url_for('.profile'))


@auth.route('/change_username', methods=['GET', 'POST'])
@login_required
def change_username():
    """Change username.
    """
    form = ChangeUsernameForm()
    if form.validate_on_submit():
        print 'pass'
        current_user.change_username(form.username.data)
        print 'change'
        flash('Your username has been updated.')
        return redirect(url_for('.profile'))
    return render_template("auth/change_username.html", form=form)