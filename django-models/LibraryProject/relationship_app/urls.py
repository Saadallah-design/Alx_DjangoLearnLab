from django.urls import path
from . import views
from .views import LibraryDetailView
from .views import BookListView
from .views import list_books

app_name = 'relationship_app'

urlpatterns = [
	# Function-based view that renders a simple list of books
	path('books/', views.list_books, name='list_books'),

	# Class-based ListView for books
	path('books/class/', views.BookListView.as_view(), name='book_list_cbv'),

	# Detail view for a library (expects library_id in URL)
	path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]