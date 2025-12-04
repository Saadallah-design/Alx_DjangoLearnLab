from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Book management
    path('books/', views.book_list, name='book_list'),
    path('books/create/', views.book_create, name='book_create'),
    path('books/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
]
