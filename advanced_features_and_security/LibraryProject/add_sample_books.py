
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()
from bookshelf.models import Book

sample_books = [
    {"title": "The Pragmatic Programmer", "author": "Andrew Hunt", "publication_year": 1999},
    {"title": "Clean Code", "author": "Robert C. Martin", "publication_year": 2008},
    {"title": "Django for APIs", "author": "William S. Vincent", "publication_year": 2020},
    {"title": "Python Crash Course", "author": "Eric Matthes", "publication_year": 2015},
    {"title": "Atomic Habits", "author": "James Clear", "publication_year": 2018},
    {"title": "Deep Work", "author": "Cal Newport", "publication_year": 2016},
    {"title": "Refactoring", "author": "Martin Fowler", "publication_year": 1999},
    {"title": "Introduction to Algorithms", "author": "Thomas H. Cormen", "publication_year": 2009},
    {"title": "Fluent Python", "author": "Luciano Ramalho", "publication_year": 2015},
    {"title": "Effective Java", "author": "Joshua Bloch", "publication_year": 2008},
    {"title": "Design Patterns", "author": "Erich Gamma", "publication_year": 1994},
    {"title": "You Don't Know JS", "author": "Kyle Simpson", "publication_year": 2015},
    {"title": "The Clean Coder", "author": "Robert C. Martin", "publication_year": 2011},
    {"title": "Zero to One", "author": "Peter Thiel", "publication_year": 2014},
    {"title": "Start With Why", "author": "Simon Sinek", "publication_year": 2009},
    {"title": "Algorithms to Live By", "author": "Brian Christian", "publication_year": 2016},
    {"title": "Grit", "author": "Angela Duckworth", "publication_year": 2016},
    {"title": "Thinking, Fast and Slow", "author": "Daniel Kahneman", "publication_year": 2011},
    {"title": "Drive", "author": "Daniel H. Pink", "publication_year": 2009},
    {"title": "The Art of Computer Programming", "author": "Donald Knuth", "publication_year": 1968},
]

for book in sample_books:
    Book.objects.get_or_create(
        title=book["title"],
        author=book["author"],
        publication_year=book["publication_year"]
    )
print("Sample books added.")
