from flask import render_template, request, Blueprint
from app.models import Post, Category

main = Blueprint('main', __name__)

# Home Page
@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    categories = Category.query.limit(6).all()
    return render_template('home.html', posts=posts,categories=categories)

# About Me Page
@main.route("/about")
def about():
    return render_template('about.html', title='About')