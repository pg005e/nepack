from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, current_user, logout_user
from flaskr import db
from flaskr.forms import RegistrationForm, LoginForm
from flaskr.models import load_user, User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
                    password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash(message=f'Account created for { form.username.data }!', category='success')
        return redirect(url_for('index'))
    return render_template('/auth/register.html', title='Register', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(message=f'You are already logged in {current_user.username}', category='success')
        return redirect(url_for('tradinguser.landing'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(pwhash=user.password, password=form.password.data):
            login_user(user=user, remember=form.remember.data)
            flash(message='Login Successful', category='success')
            return redirect(url_for('tradinguser.landing'))
        else:
            flash(message='Login Unsuccessful. Please check email and password.', category='error')
    return render_template('auth/login.html', title='Login', form=form)


@bp.route('/logout')
def logout():
    # display a logout page
    logout_user()
    return redirect(url_for('index'))
