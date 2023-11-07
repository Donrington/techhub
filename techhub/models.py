from flask import Flask
from datetime import datetime,time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import TEXT
db =SQLAlchemy()



# User entity
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)  # Store hashed password
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    profile_picture = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    join_date = db.Column(db.DateTime, server_default=db.func.now())

# Category entity
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

# Tag entity
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Comment(db.Model):
    __tablename__ = 'comment'
    comment_id = db.Column(db.Integer, primary_key=True)
    userpostid = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    response_text = db.Column(db.String(500), nullable=False)
    date_posted = db.Column(db.DateTime(), default=datetime.utcnow)
    
    # Define the relationship to the User model
    user = db.relationship('User', backref='comments')

    # Define the relationship to the Post model
   

# Post entity
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    subcontent = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=True)
    post_date = db.Column(db.DateTime, server_default=db.func.now())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('posts', lazy=True))
    categories = db.relationship('Category', secondary='post_category', backref=db.backref('posts', lazy=True))
    tags = db.relationship('Tag', secondary='post_tag', backref=db.backref('posts', lazy=True))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

# Association table for Post-Category (Many-to-Many)
post_category = db.Table('post_category',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

# Association table for Post-Tag (Many-to-Many)
post_tag = db.Table('post_tag',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class Contact(db.Model):
    __tablename__ = 'contactus' 
    contact_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    contact_name=db.Column(db.String(100),nullable=True)
    contact_email = db.Column(db.String(100),nullable=True)
    contact_no=db.Column(db.String(100),nullable=True)
    contact_message = db.Column(db.String(100),nullable=True)

if __name__ == '__main__':
    db.create_all()
