
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from blog import views


urlpatterns = [
    path('admin/', admin.site.urls),
    # Blog post management URLs
    path('', include('blog.urls')),
]