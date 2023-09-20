from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# Create an instance of Flask-Admin
admin = Admin(app, name='My Admin', template_mode='bootstrap3')

# Create a view to manage your Book model
class BookView(ModelView):
    column_list = ('title', 'author', 'published', 'pages')  # List of columns to display
    column_searchable_list = ('title', 'author')  # Add columns you want to search
    column_filters = ('published', 'pages')  # Add filters for columns
    form_columns = ('title', 'subtitle', 'author', 'published', 'publisher', 'pages', 'description', 'website', 'image')  # Form fields for adding/editing
    can_export = True  # Allow exporting to CSV/Excel

# Add the view to the admin interface
admin.add_view(BookView(Book, db.session))
