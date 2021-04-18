from flask import render_template, request, Blueprint
from app.models import Post, Category

main = Blueprint('main', __name__)

# Home Page
@main.route("/")
@main.route("/home")
def home():
    # page = request.args.get('page', 1, type=int)
    latestPosts = Post.query.order_by(Post.date_posted.desc()).limit(5).all()
    categories = Category.query.all()
    
    finalCat = []
    for category in categories:
        posts = Post.query.filter_by(category=category).all()
        newCat = {
            'id':category.id,
            'category':category.category,
            'threads':len(posts)
        }
        finalCat.append(newCat)
    
    return render_template('home.html', posts=posts,categories=finalCat,latestPosts=latestPosts)

# About Me Page
@main.route("/about")
def about():
    return render_template('about.html', title='About')