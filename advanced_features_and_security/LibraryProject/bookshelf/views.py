from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Book
from .forms import BookForm
from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='5/m', block=True)
def user_login(request):
    """Login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'book_list'
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
        response = render(request, 'login.html')
        response["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self';"
        return response
    else:
        response = render(request, 'login.html')
        response["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self';"
        return response


def user_logout(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """Display list of all books - requires can_view permission"""
    books = Book.objects.all().order_by('-publication_year', 'title')
    # even though the html files are under bookshelf/templates we only need to specify 'bookshelf/book_list.html'
    return render(request, 'book_list.html', {'books': books})


@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """Create a new book - requires can_create permission"""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" has been added successfully!')
            return redirect('book_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm()
    
    return render(request, 'add_book.html', {'form': form})


@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    """Edit an existing book - requires can_edit permission"""
    # getting the book object with specified primary key (pk) or return 404 if not found
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" has been updated successfully!')
            return redirect('book_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'add_book.html', {'form': form, 'book': book})


@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """Delete a book - requires can_delete permission"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'Book "{title}" has been deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'delete_book.html', {'book': book})
