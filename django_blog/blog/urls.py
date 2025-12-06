from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from blog.views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logged_out.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    # post management URLs 
    path('posts/', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('posts/<int:post_id>/comments/new/', views.CommentCreateView.as_view(), name='add_comment'),
    path('posts/<int:post_id>/comments/<int:comment_id>/edit/', views.CommentUpdateView.as_view(), name='comment_edit'),
    path('posts/<int:post_id>/comments/<int:comment_id>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('posts/<int:post_id>/comments/<int:comment_id>/reply/', views.ReplyCommentCreateView.as_view(), name='reply_comment'),
]
