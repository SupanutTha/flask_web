import json
from flask import Flask, flash, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_login import logout_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import flash


secret_key = os.urandom(24)
print(secret_key)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.db'
db = SQLAlchemy(app)
admin = Admin(app, name='My Admin', template_mode='bootstrap3')

# login instance
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


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

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  # Assuming this is the email column
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f'<User {self.username}>'
class UserView(ModelView):
    column_list = ('username', 'email')  # List of columns to display
    column_searchable_list = ('username', 'email')  # Add columns you want to search
    column_filters = ('username', 'email')  # Add filters for columns
    form_columns = ('username', 'email', 'password')  # Form fields for adding/editing

admin.add_view(UserView(User, db.session))

class BookView(ModelView):
    column_list = ('title', 'author', 'published', 'pages','image')  # List of columns to display
    column_searchable_list = ('title', 'author')  # Add columns you want to search
    column_filters = ('published', 'pages')  # Add filters for columns
    form_columns = ('title', 'subtitle', 'author', 'published', 'publisher', 'pages', 'description', 'website', 'image')  # Form fields for adding/editing
    can_export = True  # Allow exporting to CSV/Excel

admin.add_view(BookView(Book, db.session))

def import_books_from_json(json_filename):
    print(json_filename)
    with open(json_filename, 'r') as json_file:
        books_data = json.load(json_file)
        print("load success")
        for book_data in books_data['books']:
            isbn = book_data['isbn']
            
            # Check if a book with the same ISBN already exists in the database
            existing_book = Book.query.filter_by(isbn=isbn).first()
            
            if existing_book:
                # Handle the duplicate (e.g., update the existing record or skip)
                print(f"Book with ISBN {isbn} already exists. Skipping...")
                continue

            image = book_data.get('image', None)
            new_book = Book(
                isbn=isbn,
                title=book_data['title'],
                subtitle=book_data['subtitle'],
                author=book_data['author'],
                published=book_data['published'],
                publisher=book_data['publisher'],
                pages=book_data['pages'],
                description=book_data['description'],
                website=book_data['website'],
                image=image
            )
            print(new_book.title)
            # Add the Book object to the session
            try:
                # Add the Book object to the session
                db.session.add(new_book)

                # Commit the transaction to save the new book to the database
                db.session.commit()
            except Exception as e:
                # Handle the exception here
                db.session.rollback()  # Rollback the transaction in case of an error
                print(f"Error adding book: {str(e)}")
                # You can choose to log the error or perform any other necessary actions

        # Commit the transaction to save the new books to the database
        db.session.commit()

@app.before_first_request
def before_first_request():
    db.create_all()
    print("check")
    import_books_from_json('static/json/database.json')

@app.route('/', methods=['GET', 'POST'])
def home():
    # import_books_from_json('static/json/database.json')
    if request.method == 'POST' and 'register' in request.form:
        # Handle user registration form submission
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if the email or username already exists in the database
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists. Please choose a different email.', 'danger')
        else:
            new_user = User(username=username, email=email, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash('Registration successful. You can now log in.', 'success')

    elif request.method == 'POST' and 'login' in request.form:
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful.', 'success')
        else:
            flash('Login failed. Please check your username and password.', 'danger')

    elif request.method == 'POST':
        logout_user()

    books = Book.query.all()
    return render_template("index.html", books=books)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create the database tables before the first request
# @app.before_request
# def create_tables():
#     db.create_all()

if __name__ == "__main__":
    app.secret_key = 'your_secret_key'
    app.run(debug=True)
