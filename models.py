from flask_login import LoginManager, login_required
from app import db

# Define the Book model

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    subtitle = db.Column(db.String(255))
    author = db.Column(db.String(255), nullable=False)
    published = db.Column(db.String(20))
    publisher = db.Column(db.String(255))
    pages = db.Column(db.Integer)
    description = db.Column(db.Text)
    website = db.Column(db.String(255))
    image = db.Column(db.String(255)) 

# Define the User model (for user authentication)
# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String(120), nullable=False)
