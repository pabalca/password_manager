from flask import abort, flash, redirect, render_template, session, url_for
from sqlalchemy import or_

from password_manager import app
from password_manager.decorators import login_required
from password_manager.forms import (
    DeletePasswordForm,
    EditPasswordForm,
    LoginForm,
    NewPasswordForm,
    SearchForm,
    RegisterForm,
)
from password_manager.generator import eff
from password_manager.models import Password, User, db


@app.route("/register", methods=["GET", "POST"])
def register():
    secret, qr = None, None
    form = RegisterForm()
    if form.validate_on_submit():
        challenge = form.challenge.data
        u = User(challenge)
        db.session.add(u)
        db.session.commit()
        qr = u.qr
        secret = u.secret
    return render_template("register.html", form=form, qr=qr, secret=secret)


@app.route("/login", methods=["GET", "POST"])
@app.route("/login/", methods=["GET", "POST"])
def login():
    session["logged_in"] = False
    form = LoginForm()
    if form.validate_on_submit():
        challenge = form.challenge.data
        code = form.code.data
        users = User.query.all()
        for user in users:
            if user.verify_password(challenge) and user.verify_totp(code):
                session["logged_in"] = True
                session["user"] = user.id
                return redirect(url_for("index"))
    return render_template("login.html", form=form, session=session)


@app.route("/logout")
def logout():
    session["logged_in"] = False
    return redirect(url_for("login"))


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    passwords = Password.query.filter(
        Password.user_id == session.get("user")
    ).order_by(Password.created_at.desc())
    form = SearchForm()
    if form.validate_on_submit():
        search = form.search.data
        passwords = passwords.filter(
            or_(
                Password.website.contains(search),
                Password.user.contains(search),
            )
        )
    passwords = passwords.all()
    return render_template("index.html", passwords=passwords, form=form)


@app.route("/new", methods=["GET", "POST"])
@login_required
def new_password():
    form = NewPasswordForm()
    if form.validate_on_submit():
        website = form.website.data
        user = form.user.data
        user_id = session.get("user")
        passphrase = form.passphrase.data
        password = Password(
            user_id=user_id, website=website, user=user, passphrase=passphrase
        )
        db.session.add(password)
        db.session.commit()
        flash("Your password is saved.")
        return redirect(url_for("index"))
    form.passphrase.data = eff.create()
    return render_template("new_password.html", form=form)


@app.route("/edit/<password_id>", methods=["GET", "POST"])
@login_required
def edit_password(password_id):
    form = EditPasswordForm()
    password = Password.query.get(password_id)
    if form.validate_on_submit():
        password.website = form.website.data
        password.user = form.user.data
        password.passphrase = form.passphrase.data
        db.session.commit()
        flash("Your password is updated.")
        return redirect(url_for("index"))

    form2 = DeletePasswordForm()
    if form2.validate_on_submit():
        password = Password.query.get(password_id)
        db.session.delete(password)
        db.session.commit()
        flash("Your password is deleted.")
        return redirect(url_for("index"))

    form.website.data = password.website  # preset form input's value
    form.user.data = password.user
    form.passphrase.data = password.passphrase
    return render_template("edit_password.html", form=form, form2=form2)


@app.route("/delete/<password_id>", methods=["POST"])
@login_required
def delete_password(password_id):
    form = DeletePasswordForm()
    if form.validate_on_submit():
        password = Password.query.get(password_id)
        db.session.delete(password)
        db.session.commit()
        flash("Your password is deleted.")
    else:
        abort(400)
    return redirect(url_for("index"))
