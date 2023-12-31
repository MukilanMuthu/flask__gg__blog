from flask import render_template, url_for, redirect, request, Blueprint, flash
from flask_login import login_user, current_user, login_required, logout_user
from project import db
from project.models import User, BlogPost
from project.users.forms import RegForm, LoginForm, UpdateUserForm
from project.users.picture_handler import add_profile_pic

users = Blueprint("users", __name__)


# register user
@users.route("/register", methods=["GET", "POST"])
def register():
    form = RegForm()

    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            roll=form.roll.data,
            password=form.password.data,
        )

        db.session.add(user)
        db.session.commit()

        flash("Thanks for registering")

        return redirect(url_for("users.login"))

    return render_template("register.html", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash("Login successful")

            next = request.args.get("next")

            if next == None or not next[0] == "/":
                next = url_for("core.index")

            return redirect(next)

    return render_template("login.html", form=form)


# logout user
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))


# update account
@users.route("/account", methods=["GET", "POST"])
@login_required
def update():
    form = UpdateUserForm()
    if request.method == "POST":
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username=username)
            current_user.profile_picture = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for("users.update"))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.roll.data = current_user.roll

    profile_image = url_for(
        "static", filename="/profile_pics" + current_user.profile_picture
    )
    return render_template("account.html", profile_image=profile_image, form=form)


@users.route("/<username>")
def user_posts(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_post = (
        BlogPost.query.filter_by(author=user)
        .order_by(BlogPost.date.desc())
        .paginate(page=page, per_page=5)
    )
    return render_template("user_blog_posts.html", blog_post=blog_post, user=user)
