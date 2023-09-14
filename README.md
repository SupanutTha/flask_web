# Flask Web Application

This is a simple Flask web application that allows users to register, log in, and view a list of books. It also includes a feature to import books from a JSON file into a SQLite database.

## Features

- **User Registration:** Users can create an account with a unique username and email.
- **User Login:** Registered users can log in to their accounts.
- **Book List:** Users can view a list of books stored in the database.
- **Book Import:** Books can be imported from a JSON file into the database.
- **Database:** Uses SQLite for data storage.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python (>=3.6)
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Werkzeug

## Getting Started

1. **Clone this repository** to your local machine:

   ```bash
   git clone https://github.com/yourusername/flask-web-app.git
2. **Change into the project directory**:
   ```bash
   cd flask-web-app
3. **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
4. **Activate the virtual environment**:
      ```bash
       venv\Scripts\activate

  5. **Install the required dependencies**:

      ```bash
      Copy code
      pip install -r requirements.txt
  6. **Initialize the SQLite database**:

      ```bash
      python
      >>> from app import db
      >>> db.create_all()
      >>> exit()
  7. **Run the application**:

      ```bash
      Copy code
      python app.py
