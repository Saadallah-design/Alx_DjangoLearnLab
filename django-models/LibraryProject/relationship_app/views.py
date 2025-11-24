from django.views import View
from django.shortcuts import render, get_object_or_404
from .models import Library, Librarian, Book 
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

# Create your views here.

# Create a function-based view in relationship_app/views.py that lists all books stored in the database.
# This view should render a simple text list of book titles and their authors.

def list_books(request):
    from .models import Book  # Importing here to avoid circular imports
    books = Book.objects.all()
    output = ', '.join([f"{book.title} by {book.author.name}" for book in books])
    return render(request, 'relationship_app/list_books.html', {'output': output})

# create a class-based view in relationship_app/views.py that displays details of a specific library, listing all books available in that library along with the librarian's name.




class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        library = self.get_object()
        context['books_list'] = library.books.all()
        return context
    
# Task1. Django Views and URL Configuration

class BookListView(ListView):
    model = Book 
    template_name = 'relationship_app/list_books.html'
    context_object_name = 'all_books'

# Task2. Django Forms and Templates
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login




def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('relationship_app:login')
    else: 
        form = UserCreationForm()
    return render(request, 'relationship_app/registration.html', {'form': form})