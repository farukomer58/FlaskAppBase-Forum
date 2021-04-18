from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField,SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User, Category
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed


# Form for Creating and Updating Posts
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    
    allCategories = Category.query.all()
    valueLabelPair = [(category.id,category.category) for category in allCategories]
    category = SelectField('Category', choices = valueLabelPair)

    submit = SubmitField('Post')

# Form for Creating and Updating Posts
class CommentForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Comment')