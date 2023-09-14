import json
from models import db, Book


# Define a function to import books from a JSON file
def import_books_from_json(json_filename):
    with open(json_filename, 'r') as json_file:
        books_data = json.load(json_file)

        for book_data in books_data['books']:
            new_book = Book(
                isbn=book_data['isbn'],
                title=book_data['title'],
                subtitle=book_data['subtitle'],
                author=book_data['author'],
                published=book_data['published'],
                publisher=book_data['publisher'],
                pages=book_data['pages'],
                description=book_data['description'],
                website=book_data['website']
            )

            # Add the Book object to the session
            db.session.add(new_book)

        # Commit the transaction to save the new books to the database
        db.session.commit()

if __name__ == "__main__":
    json_filename = "books.json"  # Replace with the path to your JSON file
    import_books_from_json(json_filename)