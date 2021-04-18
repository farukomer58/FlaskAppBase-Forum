from app.extensions import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from flask import current_app

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    
    # Define Relationship
    posts=  db.relationship('Post', backref='author', lazy=True)
    # Define Relationship
    comments=  db.relationship('Comment', backref='authorCom', lazy=True)

    # Generate and Return User Token 
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    # Static method For verifyng User Token 
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f'User({self.id}, {self.username}, {self.email}, {self.image_file})'

# Post Model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    # The the other side of the relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Define Relationship -> POST-COMMENT
    comments=  db.relationship('Comment', backref='thread', lazy=True)

    # The the other side of the category relationship
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
  
    def __repr__(self):
        return f'Post({self.id}, {self.title}, {self.date_posted})'

# Comment Model
class Comment(db.Model):
    # __tablename__ = '...' optional
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # The the other side of the relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # The the other side of the relationship
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f'Comment({self.id}, {self.comment}, {self.date_posted})'

# Category Model
class Category(db.Model):
    # __tablename__ = '...' optional
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)

    # Define Relationship -> POST-Category
    post= db.relationship('Post', backref='category', lazy=True)

    def __repr__(self):
        return f'Category({self.id}, {self.category})'

