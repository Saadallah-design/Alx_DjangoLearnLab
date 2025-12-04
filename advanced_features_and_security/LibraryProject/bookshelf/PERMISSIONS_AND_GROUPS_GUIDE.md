# Django Permissions and Groups Guide

## Table of Contents
1. [Understanding Django's Permission System](#understanding-djangos-permission-system)
2. [Types of Permissions](#types-of-permissions)
3. [Working with Groups](#working-with-groups)
4. [Implementing Custom Permissions](#implementing-custom-permissions)
5. [Permission Checking Methods](#permission-checking-methods)
6. [View-Level Permission Control](#view-level-permission-control)
7. [Template-Level Permission Checking](#template-level-permission-checking)
8. [Practical Examples](#practical-examples)
9. [Best Practices](#best-practices)

---

## Understanding Django's Permission System

Django's permission system provides a way to assign permissions to specific users and groups of users. It's built on top of Django's authentication framework and allows you to control who can do what in your application.

### Core Concepts

**Permission**: A flag that determines whether a user can perform a specific action.

**Group**: A collection of permissions that can be assigned to multiple users at once.

**User**: Can have permissions assigned directly or inherited from groups they belong to.

### Permission Flow

```
User → Groups → Permissions
  ↓
Direct Permissions
```

A user's final permissions are the combination of:
1. Permissions assigned directly to the user
2. Permissions from all groups the user belongs to

---

## Types of Permissions

### 1. Default Model Permissions

Django automatically creates four permissions for each model:

```python
# For a model named 'Book', Django creates:
- add_book      # Can add book
- change_book   # Can edit book
- delete_book   # Can delete book
- view_book     # Can view book (Django 2.1+)
```

**Format**: `<app_label>.<action>_<model_name>`

Example:
```python
bookshelf.add_book
bookshelf.change_book
bookshelf.delete_book
bookshelf.view_book
```

### 2. Custom Permissions

You can define custom permissions in your model's `Meta` class:

```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    
    class Meta:
        permissions = [
            ("can_publish_book", "Can publish book"),
            ("can_archive_book", "Can archive book"),
            ("can_feature_book", "Can feature book on homepage"),
        ]
    
    def __str__(self):
        return self.title
```

**Important**: Run `python manage.py makemigrations` and `migrate` after adding custom permissions.

### 3. Programmatically Created Permissions

Create permissions on-the-fly:

```python
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book

# Get the content type for Book model
content_type = ContentType.objects.get_for_model(Book)

# Create a new permission
permission = Permission.objects.create(
    codename='can_borrow_book',
    name='Can Borrow Book',
    content_type=content_type,
)
```

---

## Working with Groups

### What Are Groups?

Groups are a way to categorize users and apply permissions to multiple users at once. Instead of assigning permissions to each user individually, you assign them to a group, then add users to that group.

### Creating Groups

#### Method 1: Django Admin Interface

1. Go to Admin → Authentication and Authorization → Groups
2. Click "Add Group"
3. Enter group name (e.g., "Editors", "Librarians", "Viewers")
4. Select permissions for the group
5. Save

#### Method 2: Programmatically

```python
from django.contrib.auth.models import Group, Permission

# Create a group
editors_group = Group.objects.create(name='Editors')

# Get specific permissions
add_book = Permission.objects.get(codename='add_book')
change_book = Permission.objects.get(codename='change_book')
view_book = Permission.objects.get(codename='view_book')

# Add permissions to group
editors_group.permissions.add(add_book, change_book, view_book)

# Or use set() to replace all permissions at once
editors_group.permissions.set([add_book, change_book, view_book])
```

#### Method 3: Management Command (Recommended for Initial Setup)

Create a custom management command:

```python
# bookshelf/management/commands/setup_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Create user groups with permissions'
    
    def handle(self, *args, **kwargs):
        # Define groups and their permissions
        groups_permissions = {
            'Viewers': [
                'view_book',
            ],
            'Editors': [
                'view_book',
                'add_book',
                'change_book',
            ],
            'Admins': [
                'view_book',
                'add_book',
                'change_book',
                'delete_book',
                'can_publish_book',
                'can_archive_book',
            ],
        }
        
        for group_name, permissions in groups_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            
            for perm_codename in permissions:
                try:
                    permission = Permission.objects.get(codename=perm_codename)
                    group.permissions.add(permission)
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f'Permission {perm_codename} not found')
                    )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created group: {group_name}')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'Updated group: {group_name}')
                )

# Run with: python manage.py setup_groups
```

### Adding Users to Groups

```python
from django.contrib.auth import get_user_model

User = get_user_model()

# Get user and group
user = User.objects.get(username='john_doe')
editors_group = Group.objects.get(name='Editors')

# Add user to group
user.groups.add(editors_group)

# Remove user from group
user.groups.remove(editors_group)

# Clear all groups
user.groups.clear()

# Set groups (replaces all existing groups)
user.groups.set([editors_group, viewers_group])

# Check if user is in a group
if user.groups.filter(name='Editors').exists():
    print("User is an editor")
```

---

## Implementing Custom Permissions

### In Models

```python
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    is_published = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    
    class Meta:
        permissions = [
            ("can_publish_book", "Can publish book to public"),
            ("can_archive_book", "Can archive old books"),
            ("can_feature_book", "Can feature book on homepage"),
            ("can_set_premium", "Can mark book as premium content"),
        ]
        
        # Default ordering
        ordering = ['-publication_year', 'title']
        
        # Plural name
        verbose_name = "Book"
        verbose_name_plural = "Books"
    
    def __str__(self):
        return f"{self.title} by {self.author}"
```

### Assigning Permissions to Users

```python
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

User = get_user_model()

user = User.objects.get(username='jane_doe')

# Get permission
publish_perm = Permission.objects.get(codename='can_publish_book')

# Assign permission to user
user.user_permissions.add(publish_perm)

# Remove permission
user.user_permissions.remove(publish_perm)

# Clear all user permissions
user.user_permissions.clear()

# Assign multiple permissions
perms = Permission.objects.filter(codename__in=['can_publish_book', 'can_archive_book'])
user.user_permissions.set(perms)
```

---

## Permission Checking Methods

### 1. In Python Code

```python
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.get(username='john')

# Check single permission
if user.has_perm('bookshelf.add_book'):
    print("User can add books")

# Check multiple permissions (user must have ALL)
if user.has_perms(['bookshelf.add_book', 'bookshelf.change_book']):
    print("User can add and change books")

# Check if user is in a group
if user.groups.filter(name='Editors').exists():
    print("User is an editor")

# Check module-level permissions (any permission in the app)
if user.has_module_perms('bookshelf'):
    print("User has some bookshelf permissions")

# Superusers always return True
if user.is_superuser:
    print("Superuser has all permissions")

# Check if user is staff
if user.is_staff:
    print("User can access admin site")
```

### 2. In Views (Function-Based Views)

#### Using Decorators

```python
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden

# Require login
@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/list.html', {'books': books})

# Require specific permission
@permission_required('bookshelf.add_book')
def add_book(request):
    # Only users with add_book permission can access
    if request.method == 'POST':
        # Handle form submission
        pass
    return render(request, 'books/add.html')

# Require permission with custom redirect
@permission_required('bookshelf.delete_book', raise_exception=True)
def delete_book(request, book_id):
    # If user lacks permission, raises PermissionDenied (403)
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect('book_list')

# Multiple decorators
@login_required
@permission_required(['bookshelf.change_book', 'bookshelf.can_publish_book'])
def publish_book(request, book_id):
    book = Book.objects.get(id=book_id)
    book.is_published = True
    book.save()
    return redirect('book_detail', book_id=book_id)

# Manual permission checking
@login_required
def feature_book(request, book_id):
    if not request.user.has_perm('bookshelf.can_feature_book'):
        return HttpResponseForbidden("You don't have permission to feature books")
    
    book = Book.objects.get(id=book_id)
    # Feature the book logic here
    return redirect('book_detail', book_id=book_id)
```

### 3. In Views (Class-Based Views)

```python
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Require login
class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'books/list.html'
    context_object_name = 'books'
    login_url = '/login/'  # Where to redirect if not logged in

# Require specific permission
class BookCreateView(PermissionRequiredMixin, CreateView):
    model = Book
    template_name = 'books/form.html'
    fields = ['title', 'author', 'publication_year']
    permission_required = 'bookshelf.add_book'
    success_url = reverse_lazy('book_list')

# Multiple permissions (user must have ALL)
class BookUpdateView(PermissionRequiredMixin, UpdateView):
    model = Book
    template_name = 'books/form.html'
    fields = ['title', 'author', 'publication_year', 'is_published']
    permission_required = ['bookshelf.change_book', 'bookshelf.can_publish_book']
    
    def handle_no_permission(self):
        # Custom behavior when user lacks permission
        return redirect('book_list')

# Delete with permission
class BookDeleteView(PermissionRequiredMixin, DeleteView):
    model = Book
    template_name = 'books/confirm_delete.html'
    permission_required = 'bookshelf.delete_book'
    success_url = reverse_lazy('book_list')
    raise_exception = True  # Raise 403 instead of redirect

# Custom permission checking
class BookPublishView(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ['is_published']
    
    def dispatch(self, request, *args, **kwargs):
        # Check permission before processing request
        if not request.user.has_perm('bookshelf.can_publish_book'):
            return HttpResponseForbidden("You cannot publish books")
        return super().dispatch(request, *args, **kwargs)
```

---

## View-Level Permission Control

### Custom Permission Mixins

Create reusable mixins for common permission patterns:

```python
# bookshelf/mixins.py
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class GroupRequiredMixin(UserPassesTestMixin):
    """Mixin to require user to be in specific group(s)"""
    group_required = None
    
    def test_func(self):
        user = self.request.user
        if user.is_superuser:
            return True
        
        if isinstance(self.group_required, str):
            groups = [self.group_required]
        else:
            groups = self.group_required
        
        return user.groups.filter(name__in=groups).exists()
    
    def handle_no_permission(self):
        raise PermissionDenied("You must be in the required group")

# Usage
class EditorOnlyView(GroupRequiredMixin, ListView):
    model = Book
    group_required = 'Editors'
    template_name = 'books/editor_list.html'

class AdminOrEditorView(GroupRequiredMixin, UpdateView):
    model = Book
    group_required = ['Admins', 'Editors']  # User must be in at least one
    fields = ['title', 'author']
```

### Permission Checks in View Methods

```python
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404

class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'books/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add permission flags to context
        context['can_edit'] = self.request.user.has_perm('bookshelf.change_book')
        context['can_delete'] = self.request.user.has_perm('bookshelf.delete_book')
        context['can_publish'] = self.request.user.has_perm('bookshelf.can_publish_book')
        context['is_editor'] = self.request.user.groups.filter(name='Editors').exists()
        
        return context
```

---

## Template-Level Permission Checking

### Checking Permissions in Templates

```django
{% load static %}

<h1>Book Details</h1>

<!-- Check if user is authenticated -->
{% if user.is_authenticated %}
    <p>Welcome, {{ user.username }}!</p>
    
    <!-- Check specific permission -->
    {% if perms.bookshelf.change_book %}
        <a href="{% url 'book_edit' book.id %}" class="btn btn-primary">Edit Book</a>
    {% endif %}
    
    <!-- Check multiple permissions -->
    {% if perms.bookshelf.delete_book %}
        <a href="{% url 'book_delete' book.id %}" class="btn btn-danger">Delete Book</a>
    {% endif %}
    
    <!-- Check custom permission -->
    {% if perms.bookshelf.can_publish_book %}
        <form method="post" action="{% url 'book_publish' book.id %}">
            {% csrf_token %}
            <button type="submit" class="btn btn-success">Publish Book</button>
        </form>
    {% endif %}
    
    <!-- Check if user is superuser -->
    {% if user.is_superuser %}
        <p class="alert alert-info">You have admin access to all features</p>
    {% endif %}
    
    <!-- Check if user is staff -->
    {% if user.is_staff %}
        <a href="{% url 'admin:bookshelf_book_change' book.id %}">Edit in Admin</a>
    {% endif %}
    
{% else %}
    <p><a href="{% url 'login' %}">Login</a> to access more features</p>
{% endif %}

<!-- Check group membership (requires passing in context) -->
{% if is_editor %}
    <div class="editor-tools">
        <h3>Editor Tools</h3>
        <!-- Editor-specific features -->
    </div>
{% endif %}
```

### Template Filters for Permissions

```python
# bookshelf/templatetags/permission_tags.py
from django import template

register = template.Library()

@register.filter
def has_group(user, group_name):
    """Check if user belongs to a specific group"""
    return user.groups.filter(name=group_name).exists()

@register.filter
def has_any_group(user, group_names):
    """Check if user belongs to any of the specified groups (comma-separated)"""
    groups = [g.strip() for g in group_names.split(',')]
    return user.groups.filter(name__in=groups).exists()

# Usage in template:
# {% load permission_tags %}
# {% if user|has_group:"Editors" %}
#     <!-- Show editor content -->
# {% endif %}
#
# {% if user|has_any_group:"Editors,Admins" %}
#     <!-- Show content for editors or admins -->
# {% endif %}
```

---

## Practical Examples

### Example 1: Library Management System

```python
# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    copies_available = models.IntegerField(default=1)
    is_published = models.BooleanField(default=False)
    
    class Meta:
        permissions = [
            ("can_borrow_book", "Can borrow books"),
            ("can_return_book", "Can return books"),
            ("can_publish_book", "Can publish books"),
            ("can_manage_inventory", "Can manage book inventory"),
        ]

# management/commands/setup_library_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Member group
        members, _ = Group.objects.get_or_create(name='Library Members')
        member_perms = Permission.objects.filter(
            codename__in=['view_book', 'can_borrow_book', 'can_return_book']
        )
        members.permissions.set(member_perms)
        
        # Librarian group
        librarians, _ = Group.objects.get_or_create(name='Librarians')
        librarian_perms = Permission.objects.filter(
            codename__in=[
                'view_book', 'add_book', 'change_book',
                'can_borrow_book', 'can_return_book',
                'can_manage_inventory'
            ]
        )
        librarians.permissions.set(librarian_perms)
        
        # Administrator group
        admins, _ = Group.objects.get_or_create(name='Library Admins')
        admin_perms = Permission.objects.filter(
            content_type__app_label='bookshelf'
        )
        admins.permissions.set(admin_perms)
        
        self.stdout.write(self.style.SUCCESS('Library groups created'))

# views.py
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect, get_object_or_404

@login_required
@permission_required('bookshelf.can_borrow_book', raise_exception=True)
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if book.copies_available > 0:
        book.copies_available -= 1
        book.save()
        # Create borrow record
        return redirect('book_detail', book_id=book_id)
    else:
        return render(request, 'books/not_available.html', {'book': book})

@login_required
@permission_required('bookshelf.can_manage_inventory', raise_exception=True)
def manage_inventory(request):
    books = Book.objects.all()
    return render(request, 'books/inventory.html', {'books': books})
```

### Example 2: Content Management System

```python
# models.py
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('draft', 'Draft'),
        ('review', 'In Review'),
        ('published', 'Published'),
    ])
    
    class Meta:
        permissions = [
            ("can_publish_article", "Can publish articles"),
            ("can_feature_article", "Can feature articles on homepage"),
            ("can_approve_article", "Can approve articles for publication"),
        ]

# views.py
from django.views.generic import UpdateView

class ArticlePublishView(PermissionRequiredMixin, UpdateView):
    model = Article
    fields = ['status']
    permission_required = 'articles.can_publish_article'
    
    def form_valid(self, form):
        # Only allow changing to 'published' status
        if form.instance.status == 'published':
            if not self.request.user.has_perm('articles.can_publish_article'):
                return HttpResponseForbidden("You cannot publish articles")
        return super().form_valid(form)
```

---

## Best Practices

### 1. Group-Based Permissions

✅ **DO**: Assign permissions to groups, not individual users
```python
# Good
editors_group = Group.objects.get(name='Editors')
user.groups.add(editors_group)
```

❌ **DON'T**: Assign permissions directly to users unless necessary
```python
# Avoid this unless truly user-specific
user.user_permissions.add(permission)
```

### 2. Principle of Least Privilege

Grant users only the permissions they need to perform their job:

```python
# Good: Specific, minimal permissions
viewers_permissions = ['view_book']
editors_permissions = ['view_book', 'add_book', 'change_book']
admins_permissions = ['view_book', 'add_book', 'change_book', 'delete_book']
```

### 3. Use Descriptive Permission Names

```python
# Good: Clear and descriptive
class Meta:
    permissions = [
        ("can_publish_to_website", "Can publish content to public website"),
        ("can_approve_user_comments", "Can moderate and approve user comments"),
    ]

# Bad: Vague
class Meta:
    permissions = [
        ("special", "Special permission"),
        ("extra", "Extra access"),
    ]
```

### 4. Check Permissions Early

```python
# Good: Check permission at the start
def publish_book(request, book_id):
    if not request.user.has_perm('bookshelf.can_publish_book'):
        return HttpResponseForbidden()
    
    # Rest of the logic
    book = Book.objects.get(id=book_id)
    book.is_published = True
    book.save()
```

### 5. Use Mixins for Reusability

```python
# Good: Reusable permission logic
class EditorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Editors').exists()

class BookEditView(EditorRequiredMixin, UpdateView):
    model = Book
```

### 6. Document Your Permission System

Create a permissions matrix:

```markdown
| Role           | View Books | Add Books | Edit Books | Delete Books | Publish Books |
|----------------|------------|-----------|------------|--------------|---------------|
| Anonymous      | ✓          | ✗         | ✗          | ✗            | ✗             |
| Member         | ✓          | ✗         | ✗          | ✗            | ✗             |
| Editor         | ✓          | ✓         | ✓          | ✗            | ✗             |
| Publisher      | ✓          | ✓         | ✓          | ✗            | ✓             |
| Admin          | ✓          | ✓         | ✓          | ✓            | ✓             |
```

### 7. Test Permissions

```python
# tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

User = get_user_model()

class PermissionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.editor_group = Group.objects.create(name='Editors')
        
    def test_user_can_be_added_to_group(self):
        self.user.groups.add(self.editor_group)
        self.assertTrue(self.user.groups.filter(name='Editors').exists())
    
    def test_user_has_group_permissions(self):
        perm = Permission.objects.get(codename='add_book')
        self.editor_group.permissions.add(perm)
        self.user.groups.add(self.editor_group)
        
        self.assertTrue(self.user.has_perm('bookshelf.add_book'))
```

### 8. Handle Permission Denials Gracefully

```python
# Good: User-friendly error messages
from django.core.exceptions import PermissionDenied

@permission_required('bookshelf.delete_book')
def delete_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        book.delete()
        messages.success(request, 'Book deleted successfully')
    except PermissionDenied:
        messages.error(request, 'You do not have permission to delete books')
    return redirect('book_list')
```

### 9. Use Django's Built-in Admin Permissions

Leverage Django admin's automatic permission handling:

```python
# admin.py
from django.contrib import admin

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published']
    
    def has_add_permission(self, request):
        # Custom logic for add permission
        return request.user.groups.filter(name='Editors').exists()
    
    def has_change_permission(self, request, obj=None):
        # Custom logic for change permission
        return request.user.has_perm('bookshelf.change_book')
    
    def has_delete_permission(self, request, obj=None):
        # Only admins can delete
        return request.user.groups.filter(name='Admins').exists()
```

### 10. Secure Your URLs

```python
# urls.py
from django.urls import path
from .views import (
    BookListView, BookCreateView, BookUpdateView, 
    BookDeleteView, publish_book
)

urlpatterns = [
    path('books/', BookListView.as_view(), name='book_list'),
    path('books/add/', BookCreateView.as_view(), name='book_add'),  # Requires permission
    path('books/<int:pk>/edit/', BookUpdateView.as_view(), name='book_edit'),  # Requires permission
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),  # Requires permission
    path('books/<int:book_id>/publish/', publish_book, name='book_publish'),  # Requires permission
]
```

---

## Quick Reference

### Common Permission Checks

```python
# Check if user is authenticated
if request.user.is_authenticated:
    pass

# Check if user is superuser
if request.user.is_superuser:
    pass

# Check if user is staff
if request.user.is_staff:
    pass

# Check specific permission
if request.user.has_perm('app_label.permission_codename'):
    pass

# Check multiple permissions (AND)
if request.user.has_perms(['app.perm1', 'app.perm2']):
    pass

# Check if user is in a group
if request.user.groups.filter(name='GroupName').exists():
    pass

# Get all user permissions
all_perms = request.user.get_all_permissions()

# Get group permissions
group_perms = request.user.get_group_permissions()
```

### Management Commands

```bash
# Create groups and permissions
python manage.py setup_groups

# Create superuser
python manage.py createsuperuser

# Show all permissions
python manage.py shell
>>> from django.contrib.auth.models import Permission
>>> for p in Permission.objects.all():
...     print(f"{p.content_type.app_label}.{p.codename} - {p.name}")
```

---

## Summary

Django's permission and group system provides:

1. ✅ **Fine-grained access control** - Control exactly who can do what
2. ✅ **Scalability** - Easy to manage permissions for many users via groups
3. ✅ **Flexibility** - Custom permissions for business-specific needs
4. ✅ **Security** - Built-in protection against unauthorized access
5. ✅ **Integration** - Works seamlessly with views, templates, and admin

**Key Takeaways:**
- Use **groups** to manage permissions for multiple users
- Define **custom permissions** for domain-specific actions
- Check permissions in **views**, **templates**, and **models**
- Follow the **principle of least privilege**
- **Test** your permission logic thoroughly

By properly implementing permissions and groups, you create a secure, maintainable, and user-friendly access control system for your Django application.
