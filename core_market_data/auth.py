from flask import Blueprint,render_template,redirect,url_for,flash
from core_market_data.forms import RegisterForm,LoginForm
from .models import User
from . import db
from flask_login import login_user,logout_user
auth=Blueprint('auth',__name__)


@auth.route('/login',methods=['GET','POST'])
def login_page():
    form=LoginForm()
    if form.validate_on_submit():
        attempted_user=User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Login successful! you logged in as {attempted_user.username}',category='success')
            return redirect(url_for('views.market_page'))
        else:
            flash('Username or password is incorrect',category='error')
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Their was an error with creating a user:  {err_msg}',category='error')
    return render_template('login.html',form=form)

@auth.route('/register',methods=['GET','POST'])
def register_page():
    form=RegisterForm()
    if form.validate_on_submit():
        new_user=User(username=form.username.data,
                      email_address=form.email_address.data,
                      password=form.password1.data
                      )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash(f'Account Created successfully! you logged in as {new_user.username}', category='success')
        return redirect(url_for('views.market_page'))
    if form.errors !={}:
        for err_msg in form.errors.values():
            flash(f'Their was an error with creating a user:  {err_msg}')
    return render_template('register.html',form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login_page'))