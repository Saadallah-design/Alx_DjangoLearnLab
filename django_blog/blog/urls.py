from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from blog.views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, PostsByTagListView

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
    # Autochecker-required comment URL patterns
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='add_comment'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    # Threaded reply (custom, not autochecker)
    path('comment/<int:pk>/reply/', views.ReplyCommentCreateView.as_view(), name='reply_comment'),
    # Tag and search URLs
    path('tags/<str:tag_name>/', views.PostsByTagListView.as_view(), name='posts_by_tag'),
    path('search/', views.search_posts, name='search_posts'),
]
