from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, current_user, logout_user
from flaskr.forms import ShareHolderCredentialsForm
from flaskr.models import ShareHolderCredentials
from flaskr import db

bp = Blueprint('tradinguser', __name__, url_prefix='/tradinguser')


@bp.route('/', methods=['GET', 'POST'])
def landing():
    form = ShareHolderCredentialsForm()
    if form.validate_on_submit():
        creds = ShareHolderCredentials(client_Id=form.client_Id.data, username=form.username.data,
                                       password=generate_password_hash(form.password.data))
        db.session.add(creds)
        db.session.commit()
        flash(message=f'Credentials for account added for the user!',
              category='success')
        return redirect(url_for(url_for('tradinguser.landing')))

    return render_template('tradinguser/landing.html', title='Portfolio Tracker', form=form)
