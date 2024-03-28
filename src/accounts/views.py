from flask import Blueprint, flash, redirect, render_template, request, url_for, current_app
from flask_login import login_user, current_user, logout_user, login_required
from src.token import generate_confirmation_token, confirm_token
from src import db, bcrypt
from src.email import send_email
from src.accounts.models import User
from .forms import LoginForm, RegisterForm
from .forms import RegisterForm

accounts_bp = Blueprint("accounts", __name__)

@accounts_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("You are already registered.", "info")
        return redirect(url_for("core.home"))
    form = RegisterForm(request.form)
    if form.validate():
        user = User(email=form.email.data, password=form.password.data, confirmed=False)
        db.session.add(user)
        db.session.commit()

        token = generate_confirmation_token(user.email)

        confirm_url = url_for('core.home', token=token, _external=True)
        html = render_template('accounts/active.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(user.email, subject, html)
        login_user(user)
        flash("You registered and are now logged in. Welcome!", "success")

        return redirect(url_for("accounts.unconfirmed"))

    return render_template("accounts/register.html", form=form)

@accounts_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for("core.home"))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect(url_for("accounts.unconfirmed"))
        else:
            flash("Invalid email and/or password.", "danger")
            return render_template("accounts/login.html", form=form)
    return render_template("accounts/login.html", form=form)

@accounts_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "success")
    return redirect(url_for("accounts.login"))

@accounts_bp.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('the confirmation link has expired')
    user = User.query.filter_by(email=email).first()
    if user.confirmed:
        flask('Account already confirmed, please login.', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('core.home'))

@accounts_bp.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect('core.home')
    flash('Please confirm your account', 'warning')
    return render_template('accounts/unconfirmed.html')

@accounts_bp.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('accounts.confirm_email', token=token, _external=True)
    html = render_template('accounts/active.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('accounts.unconfirmed'))
