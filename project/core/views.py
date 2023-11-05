from flask import render_template, Blueprint, request
from project.models import BlogPost

core = Blueprint("core", __name__)


@core.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    blog_post = BlogPost.query.order_by(BlogPost.date.desc()).paginate(
        page=page, per_page=10
    )
    return render_template("index.html", blog_post=blog_post)


@core.route("/info")
def info():
    return render_template("info.html")
