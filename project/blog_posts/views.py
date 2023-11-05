from flask import render_template, url_for, request, redirect, Blueprint, abort
from flask_login import current_user, login_required
from project import db
from project.models import BlogPost
from project.blog_posts.forms import BlogPostForm

blog_post = Blueprint("blog_post", __name__)


# creating post
@blog_post.route("/create", methods=["POST", "GET"])
@login_required
def create():
    form = BlogPostForm()

    if form.validate_on_submit():
        blog = BlogPost(
            title=form.title.data, text=form.text.data, user_id=current_user.id
        )
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for("core.index"))

    return render_template("create_post.html", form=form, title="Create new blog")


@blog_post.route("/<int:blog_post_id>")
def blog_posts(blog_post_id):
    blog = BlogPost.query.get_or_404(blog_post_id)
    return render_template(
        "view_blog.html", title=blog.title, date=blog.date, text=blog.text, post=blog
    )


@blog_post.route("/<int:blog_post_id>/update", methods=["POST", "GET"])
@login_required
def blog_update(blog_post_id):
    blog = BlogPost.query.get_or_404(blog_post_id)
    if current_user != blog.author:
        abort(403)

    form = BlogPostForm()
    if form.validate_on_submit():
        blog.title = form.title.data
        blog.text = form.text.data
        db.session.commit()
        return redirect(url_for("blog_post.blog_posts", blog_post_id=blog.id))

    elif request.method == "GET":
        form.title.data = blog.title
        form.text.data = blog.text

    return render_template("create_post.html", form=form, title="Edit your blog")


@blog_post.route("/<int:blog_post_id>/delete", methods=["POST", "GET"])
@login_required
def blog_delete(blog_post_id):
    blog = BlogPost.query.get_or_404(blog_post_id)
    if current_user != blog.author:
        abort(403)

    db.session.delete(blog)
    db.session.commit()

    return redirect(url_for("core.index"))
