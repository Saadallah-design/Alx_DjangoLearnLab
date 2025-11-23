from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

router = DefaultRouter()

# 2. Register the ViewSet
# r'books_all': The URL prefix (e.g., /api/books_all/, /api/books_all/1/)
# BookViewSet: The class that provides the logic (list, create, retrieve, etc.)
# basename='book_all': Used for naming the URL patterns (e.g., 'book_all-list', 'book_all-detail')
router.register(r'books_all', BookViewSet, basename='book_all')


urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('', include(router.urls)),
]