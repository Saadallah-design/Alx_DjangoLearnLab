from django.urls import path
from . import views

app_name = 'relationship_app'

urlpatterns = [
	# Function-based view that renders a simple list of books
	path('books/', views.book_list, name='book_list'),

	# Class-based ListView for books
	path('books/class/', views.BookListView.as_view(), name='book_list_cbv'),

	# Detail view for a library (expects library_id in URL)
	path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]