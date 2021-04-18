from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from app.extensions import db
from app.models import Post, Comment, Category
from app.posts.forms import PostForm, CommentForm

posts = Blueprint('posts',__name__)

#### ROUTES FOR CRUD operations Post ####
# CREATE new Post Route
@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()

    # print(dict(form.category.choices).get(form.category.data))
    if form.validate_on_submit():
        # labelOfSelectField = dict(form.category.choices).get(int(form.category.data))
        category = Category.query.get_or_404(form.category.data)   # Get the Post or return 404 if post not exist
        post = Post(title=form.title.data, content=form.content.data, author=current_user, category=category)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')

# READ Post
@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    form = CommentForm()                    # Form for posting a Comment
    post = Post.query.get_or_404(post_id)   # Get the Post or return 404 if post not exist

    #If Comment is pushed add the comment to the database
    if form.validate_on_submit():
        comment = Comment(comment=form.content.data,thread=post,user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('posts.post',post_id=post.id))

    return render_template('post.html', title=post.title, post=post,commentForm=form)

# UPDATE Post
@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')

# DELETE Post
@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))

# Get All Posts for given category
@posts.route("/post/filter/<int:category>")
def filter_posts(category):
    page = request.args.get('page', 1, type=int)
    category = Category.query.get_or_404(category)   # Get the Post or return 404 if post not exist

    posts = Post.query.filter_by(category=category)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('filter_posts.html', posts=posts, category=category)