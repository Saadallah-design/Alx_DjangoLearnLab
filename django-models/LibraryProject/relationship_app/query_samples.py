# Prepare a Python script query_samples.py in the relationship_app directory. This script should contain the query for each of the following of relationship:
# Query all books by a specific author.
# List all books in a library.
# Retrieve the librarian for a library.

from relationship_app.models import Author, Book, Library, Librarian
def get_books_by_author(author_username):
    try:
        author = Author.objects.get(username=author_username)
        books = author.books.all()
        return books
    except Author.DoesNotExist:
        return None
def get_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        return books
    except Library.DoesNotExist:
        return None
def get_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = library.librarian
        return librarian
    except Library.DoesNotExist:
        return None
    except Librarian.DoesNotExist:
        return None