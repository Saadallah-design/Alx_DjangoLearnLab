# Django Permissions and Groups Setup Guide

## Table of Contents
1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [How Permissions Work](#how-permissions-work)
4. [Implementation Approach](#implementation-approach)
5. [Best Practices](#best-practices)
6. [Usage Examples](#usage-examples)
7. [Testing](#testing)
8. [Troubleshooting](#troubleshooting)

---

## Overview

This project implements a robust permission and group-based access control system for managing books in a library application. The implementation follows Django best practices and provides a scalable, maintainable approach to authorization.

### Key Components

1. **Custom Permissions** - Defined in the Book model
2. **User Groups** - Viewers, Editors, and Admins
3. **Management Command** - Automated setup script
4. **Permission Enforcement** - In views, templates, and admin

---

## Project Structure

```
LibraryProject/
├── bookshelf/
│   ├── models.py                    # Book model with custom permissions
│   ├── admin.py                     # Admin configuration with CustomUser
│   ├── views.py                     # Views with permission checks
│   ├── management/
│   │   ├── __init__.py
│   │   └── commands/
│   │       ├── __init__.py
│   │       └── setup_groups.py      # Command to create groups and assign permissions
│   ├── migrations/
│   │   └── 0001_initial.py          # Includes custom permissions
│   └── templates/
│       └── bookshelf/
│           └── book_list.html       # Template with permission checks
├── LibraryProject/
│   └── settings.py                  # AUTH_USER_MODEL configuration
└── manage.py
```

---

## How Permissions Work

### 1. Permission Definition (models.py)

Permissions are declared in the model's `Meta` class:

```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    class Meta:
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]

    def __str__(self):
        return self.title
```

**Why in the Model?**
- ✅ Declarative and clear
- ✅ Version controlled with the model
- ✅ Automatically creates database entries during migrations
- ✅ Easy to discover what permissions exist

**Permission Naming Convention:**
- Format: `(codename, "Human readable description")`
- Codename: lowercase, underscore-separated (e.g., `can_view`)
- Description: Title case, clear action (e.g., "Can view book")

### 2. Database Storage

When you run migrations, Django creates entries in the `auth_permission` table:

```
| id | name             | content_type_id | codename   |
|----|------------------|-----------------|------------|
| 1  | Can view book    | 12              | can_view   |
| 2  | Can create book  | 12              | can_create |
| 3  | Can edit book    | 12              | can_edit   |
| 4  | Can delete book  | 12              | can_delete |
```

### 3. Groups and Permission Assignment

Groups are collections of permissions. Users inherit all permissions from their groups.

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   User      │─────▶│    Group     │─────▶│ Permissions │
└─────────────┘      └──────────────┘      └─────────────┘
      │                                             ▲
      └─────────────────────────────────────────────┘
           (Can also have direct permissions)
```

---

## Implementation Approach

### Why Use a Management Command?

We use a Django management command (`setup_groups.py`) instead of putting group creation in `models.py`. Here's why:

#### ❌ Wrong Approach: Module-Level Code in models.py

```python
# DON'T DO THIS!
from django.contrib.auth.models import Group, Permission

# This runs when the module is imported
editors_group = Group.objects.get_or_create(name='Editors')[0]  # ❌ CRASHES!
```

**Problems:**
1. **Import-time execution** - Runs when Python imports the file
2. **Database not ready** - ORM isn't available during imports
3. **Migration failures** - Breaks during `makemigrations` and `migrate`
4. **Cannot be undone** - No way to rollback or clean up
5. **Not idempotent** - Can't safely run multiple times

#### ✅ Correct Approach: Management Command

```python
# bookshelf/management/commands/setup_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Create user groups and assign permissions'

    def handle(self, *args, **kwargs):
        # This runs ONLY when you explicitly call the command
        editors, created = Group.objects.get_or_create(name='Editors')
        # ... permission assignment
```

**Benefits:**
1. ✅ **Explicit execution** - Runs only when you want it
2. ✅ **Database is ready** - ORM fully initialized
3. ✅ **Idempotent** - Safe to run multiple times
4. ✅ **Testable** - Can be tested independently
5. ✅ **Reusable** - Can be run in different environments
6. ✅ **Manageable** - Easy to update and maintain

### Our Management Command Structure

```python
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book


class Command(BaseCommand):
    help = 'Create user groups and assign permissions'

    def handle(self, *args, **kwargs):
        # Step 1: Get the Book content type
        book_content_type = ContentType.objects.get_for_model(Book)

        # Step 2: Retrieve custom permissions
        can_view = Permission.objects.get(
            codename='can_view', 
            content_type=book_content_type
        )
        can_create = Permission.objects.get(
            codename='can_create', 
            content_type=book_content_type
        )
        can_edit = Permission.objects.get(
            codename='can_edit', 
            content_type=book_content_type
        )
        can_delete = Permission.objects.get(
            codename='can_delete', 
            content_type=book_content_type
        )

        # Step 3: Create groups (idempotent)
        viewers, created = Group.objects.get_or_create(name='Viewers')
        editors, created = Group.objects.get_or_create(name='Editors')
        admins, created = Group.objects.get_or_create(name='Admins')

        # Step 4: Assign permissions to groups
        viewers.permissions.set([can_view])
        editors.permissions.set([can_view, can_create, can_edit])
        admins.permissions.set([can_view, can_create, can_edit, can_delete])

        # Step 5: Provide feedback
        self.stdout.write(self.style.SUCCESS('✅ Groups and permissions set up!'))
```

### Permission Matrix

| Group   | can_view | can_create | can_edit | can_delete |
|---------|----------|------------|----------|------------|
| Viewers | ✓        | ✗          | ✗        | ✗          |
| Editors | ✓        | ✓          | ✓        | ✗          |
| Admins  | ✓        | ✓          | ✓        | ✓          |

---

## Best Practices

### 1. **Define Permissions in Models**

✅ **DO**: Declare permissions in the model's Meta class
```python
class Book(models.Model):
    # fields...
    
    class Meta:
        permissions = [
            ("can_publish", "Can publish book"),
        ]
```

❌ **DON'T**: Create permissions at module level
```python
# models.py
permission = Permission.objects.create(...)  # ❌ Will crash!
```

### 2. **Use Groups Instead of Direct User Permissions**

✅ **DO**: Assign permissions to groups, users to groups
```python
# Create group with permissions
editors = Group.objects.get(name='Editors')

# Add user to group
user.groups.add(editors)
```

❌ **DON'T**: Assign permissions directly to users
```python
# Avoid unless user needs unique permission
user.user_permissions.add(permission)  # ❌ Not scalable
```

### 3. **Use Descriptive Permission Names**

✅ **DO**: Clear, action-oriented names
```python
permissions = [
    ("can_publish_book", "Can publish book to website"),
    ("can_approve_review", "Can approve book reviews"),
]
```

❌ **DON'T**: Vague or generic names
```python
permissions = [
    ("special", "Special access"),  # ❌ What does this do?
    ("extra", "Extra permission"),   # ❌ Too generic
]
```

### 4. **Make Commands Idempotent**

✅ **DO**: Use `get_or_create()` for safe reruns
```python
group, created = Group.objects.get_or_create(name='Editors')
if created:
    print("Created new group")
else:
    print("Group already exists")
```

❌ **DON'T**: Use `create()` which fails if exists
```python
group = Group.objects.create(name='Editors')  # ❌ Crashes if exists
```

### 5. **Follow the Principle of Least Privilege**

✅ **DO**: Give users minimum permissions needed
```python
# Viewers can only read
viewers.permissions.set([can_view])

# Editors can read and write
editors.permissions.set([can_view, can_create, can_edit])
```

❌ **DON'T**: Give everyone admin access
```python
# Everyone gets all permissions ❌
all_users_group.permissions.set(Permission.objects.all())
```

### 6. **Check Permissions Early**

✅ **DO**: Check permissions at view entry
```python
from django.contrib.auth.decorators import permission_required

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    # User has permission, proceed
    pass
```

❌ **DON'T**: Check permissions after processing
```python
def edit_book(request, book_id):
    # Do lots of work...
    if not request.user.has_perm('bookshelf.can_edit'):  # ❌ Too late!
        return HttpResponseForbidden()
```

### 7. **Document Your Permission System**

✅ **DO**: Create a permission matrix
```markdown
| Role    | View | Create | Edit | Delete | Publish |
|---------|------|--------|------|--------|---------|
| Viewer  | ✓    | ✗      | ✗    | ✗      | ✗       |
| Editor  | ✓    | ✓      | ✓    | ✗      | ✗       |
| Admin   | ✓    | ✓      | ✓    | ✓      | ✓       |
```

### 8. **Use Permission Mixins for Class-Based Views**

✅ **DO**: Use Django's permission mixins
```python
from django.contrib.auth.mixins import PermissionRequiredMixin

class BookEditView(PermissionRequiredMixin, UpdateView):
    permission_required = 'bookshelf.can_edit'
    model = Book
```

### 9. **Test Your Permissions**

✅ **DO**: Write tests for permission checks
```python
def test_viewer_cannot_delete(self):
    viewer = User.objects.create_user('viewer')
    viewer.groups.add(Group.objects.get(name='Viewers'))
    self.assertFalse(viewer.has_perm('bookshelf.can_delete'))
```

### 10. **Version Control Your Setup Command**

✅ **DO**: Keep setup command in version control
```bash
git add bookshelf/management/commands/setup_groups.py
git commit -m "Add groups and permissions setup command"
```

---

## Usage Examples

### Setting Up Permissions (Initial Setup)

```bash
# 1. Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# 2. Run the setup command to create groups
python manage.py setup_groups

# Output:
# Created group: Viewers
# Assigned permissions to Viewers: can_view
# Created group: Editors
# Assigned permissions to Editors: can_view, can_create, can_edit
# Created group: Admins
# Assigned permissions to Admins: all book permissions
# ✅ Successfully set up groups and permissions!
```

### Creating Users and Assigning to Groups

```python
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

# Create users
viewer_user = User.objects.create_user(username='john', password='pass123')
editor_user = User.objects.create_user(username='jane', password='pass456')
admin_user = User.objects.create_user(username='admin', password='admin789')

# Get groups
viewers = Group.objects.get(name='Viewers')
editors = Group.objects.get(name='Editors')
admins = Group.objects.get(name='Admins')

# Assign users to groups
viewer_user.groups.add(viewers)
editor_user.groups.add(editors)
admin_user.groups.add(admins)
```

### Checking Permissions in Views

#### Function-Based Views

```python
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .models import Book

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    if request.method == 'POST':
        # Handle form submission
        pass
    return render(request, 'bookshelf/book_form.html')

@login_required
def edit_book(request, book_id):
    # Manual permission check
    if not request.user.has_perm('bookshelf.can_edit'):
        return HttpResponseForbidden("You don't have permission to edit books")
    
    book = get_object_or_404(Book, id=book_id)
    # Handle editing
    return render(request, 'bookshelf/book_form.html', {'book': book})
```

#### Class-Based Views

```python
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Book

class BookListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Book
    permission_required = 'bookshelf.can_view'
    template_name = 'bookshelf/book_list.html'
    context_object_name = 'books'

class BookCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Book
    permission_required = 'bookshelf.can_create'
    fields = ['title', 'author', 'publication_year']
    success_url = reverse_lazy('book_list')

class BookUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Book
    permission_required = 'bookshelf.can_edit'
    fields = ['title', 'author', 'publication_year']
    success_url = reverse_lazy('book_list')

class BookDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Book
    permission_required = 'bookshelf.can_delete'
    success_url = reverse_lazy('book_list')
```

### Checking Permissions in Templates

```django
{% if user.is_authenticated %}
    <h2>Books</h2>
    
    {% if perms.bookshelf.can_view %}
        <ul>
            {% for book in books %}
                <li>
                    {{ book.title }} by {{ book.author }}
                    
                    {% if perms.bookshelf.can_edit %}
                        <a href="{% url 'book_edit' book.id %}">Edit</a>
                    {% endif %}
                    
                    {% if perms.bookshelf.can_delete %}
                        <a href="{% url 'book_delete' book.id %}">Delete</a>
                    {% endif %}
                </li>
            {% endfor %}
        </ul>
    {% endif %}
    
    {% if perms.bookshelf.can_create %}
        <a href="{% url 'book_create' %}" class="btn">Add New Book</a>
    {% endif %}
{% else %}
    <p>Please <a href="{% url 'login' %}">login</a> to view books.</p>
{% endif %}
```

### Checking Group Membership

```python
# In views
if request.user.groups.filter(name='Editors').exists():
    # User is an editor
    pass

# In Python shell or scripts
from django.contrib.auth import get_user_model
User = get_user_model()

user = User.objects.get(username='john')

# Check if user is in a group
is_editor = user.groups.filter(name='Editors').exists()

# Get all user's groups
user_groups = user.groups.all()

# Get all users in a group
editors = Group.objects.get(name='Editors')
editor_users = editors.user_set.all()
```

---

## Testing

### Testing Permissions in Django

```python
# bookshelf/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from .models import Book

User = get_user_model()

class PermissionTests(TestCase):
    
    def setUp(self):
        # Create test users
        self.viewer = User.objects.create_user(username='viewer', password='pass')
        self.editor = User.objects.create_user(username='editor', password='pass')
        self.admin = User.objects.create_user(username='admin', password='pass')
        
        # Create groups and assign permissions
        from django.core.management import call_command
        call_command('setup_groups')
        
        # Assign users to groups
        self.viewer.groups.add(Group.objects.get(name='Viewers'))
        self.editor.groups.add(Group.objects.get(name='Editors'))
        self.admin.groups.add(Group.objects.get(name='Admins'))
    
    def test_viewer_can_view_only(self):
        self.assertTrue(self.viewer.has_perm('bookshelf.can_view'))
        self.assertFalse(self.viewer.has_perm('bookshelf.can_create'))
        self.assertFalse(self.viewer.has_perm('bookshelf.can_edit'))
        self.assertFalse(self.viewer.has_perm('bookshelf.can_delete'))
    
    def test_editor_permissions(self):
        self.assertTrue(self.editor.has_perm('bookshelf.can_view'))
        self.assertTrue(self.editor.has_perm('bookshelf.can_create'))
        self.assertTrue(self.editor.has_perm('bookshelf.can_edit'))
        self.assertFalse(self.editor.has_perm('bookshelf.can_delete'))
    
    def test_admin_has_all_permissions(self):
        self.assertTrue(self.admin.has_perm('bookshelf.can_view'))
        self.assertTrue(self.admin.has_perm('bookshelf.can_create'))
        self.assertTrue(self.admin.has_perm('bookshelf.can_edit'))
        self.assertTrue(self.admin.has_perm('bookshelf.can_delete'))
    
    def test_view_requires_permission(self):
        # Test that view access is restricted
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # Login as viewer
        self.client.login(username='viewer', password='pass')
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, 200)  # Access granted
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: Permissions Not Found

**Error:** `Permission matching query does not exist.`

**Solution:**
```bash
# Ensure migrations are applied
python manage.py migrate

# If still missing, check if migrations include custom permissions
python manage.py makemigrations bookshelf --dry-run

# Force recreate permissions
python manage.py migrate --run-syncdb
```

#### Issue 2: Groups Already Exist

**Error:** `IntegrityError: UNIQUE constraint failed: auth_group.name`

**Solution:**
Already handled in our command with `get_or_create()`. If you used `create()`, update to:
```python
group, created = Group.objects.get_or_create(name='Editors')
```

#### Issue 3: Permission Check Always Returns False

**Problem:** User should have permission but `has_perm()` returns False

**Debugging:**
```python
# Check user's permissions
user = User.objects.get(username='john')

# Get all permissions
all_perms = user.get_all_permissions()
print(all_perms)

# Check groups
groups = user.groups.all()
print(groups)

# Check if permission exists
from django.contrib.auth.models import Permission
perm = Permission.objects.get(codename='can_view')
print(f"Permission: {perm.content_type.app_label}.{perm.codename}")

# Check if user has it
has_perm = user.has_perm('bookshelf.can_view')
print(f"Has permission: {has_perm}")
```

#### Issue 4: Module Import Errors

**Error:** `AttributeError: module 'bookshelf.models' has no attribute 'Group'`

**Cause:** Trying to import Group from models.py

**Solution:**
```python
# Correct import
from django.contrib.auth.models import Group, Permission

# Not from your app's models
# from bookshelf.models import Group  # ❌ Wrong
```

---

## Summary

### Key Takeaways

1. ✅ **Define permissions in model Meta class** for version control and clarity
2. ✅ **Use management commands** for group/permission setup, not module-level code
3. ✅ **Assign permissions to groups**, not individual users
4. ✅ **Check permissions early** in views with decorators or mixins
5. ✅ **Make commands idempotent** with `get_or_create()`
6. ✅ **Follow least privilege** principle
7. ✅ **Test your permissions** thoroughly
8. ✅ **Document your permission matrix**

### Quick Command Reference

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations (creates permissions)
python manage.py migrate

# Set up groups and assign permissions
python manage.py setup_groups

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test bookshelf

# Django shell to inspect permissions
python manage.py shell
>>> from django.contrib.auth.models import Permission
>>> Permission.objects.all()
```

### Permission Format

- **In code:** `appname.permission_codename` (e.g., `bookshelf.can_view`)
- **In database:** Stored as separate app_label and codename
- **In templates:** `{% if perms.bookshelf.can_view %}`

This approach provides a scalable, maintainable, and Django-idiomatic way to manage permissions in your application!
