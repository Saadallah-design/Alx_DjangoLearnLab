from django.views import View
from django.shortcuts import render, get_object_or_404
from .models import Library, Librarian, Book 
from django.views.generic import ListView

# Create your views here.

# Create a function-based view in relationship_app/views.py that lists all books stored in the database.
# This view should render a simple text list of book titles and their authors.

def book_list(request):
    from .models import Book  # Importing here to avoid circular imports
    books = Book.objects.all()
    output = ', '.join([f"{book.title} by {book.author.name}" for book in books])
    return render(request, 'relationship_app/list_books.html', {'output': output})

# create a class-based view in relationship_app/views.py that displays details of a specific library, listing all books available in that library along with the librarian's name.




class LibraryDetailView(View):
    """
    A Class-Based View for displaying library details, 
    manually implemented to fetch all related data.
    """
    
    # This method handles all GET requests to this view.
    # It takes 'request' and 'library_id' (from the URL) as arguments.
    def get(self, request, library_id):
        
        # 1. Fetch the main Library object (The exact same FBV logic)
        library = get_object_or_404(Library, id=library_id)
        
        # 2. Fetch the related books using the ManyToMany relationship
        books = library.books.all()
        
        # 3. Fetch the related Librarian using the OneToOne relationship
        try:
            librarian_info = library.librarian
        except Librarian.DoesNotExist:
            librarian_info = None
            
        # 4. Put all the data into the context dictionary
        context = {
            'library': library, 
            'books_list': books, 
            'librarian_info': librarian_info, 
        }
        
        # 5. Tell Django to render the template with the context
        return render(request, 'relationship_app/library_detail.html', context)
    
# Task1. Django Views and URL Configuration

class BookListView(ListView):
    model = Book 
    template_name = 'relationship_app/list_books.html'
    context_object_name = 'all_books'
