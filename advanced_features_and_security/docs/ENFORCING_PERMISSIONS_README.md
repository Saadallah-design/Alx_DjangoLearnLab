git # Enforcing Permissions in Views - Implementation Guide

## Overview

This guide covers implementing and testing permission-based access control in Django views. We'll enforce the custom permissions (`can_view`, `can_create`, `can_edit`, `can_delete`) defined in the Book model across all views.

---

## Table of Contents

1. [Permission Decorators](#permission-decorators)
2. [Function-Based Views (FBV)](#function-based-views-fbv)
3. [Class-Based Views (CBV)](#class-based-views-cbv)
4. [Testing Permissions](#testing-permissions)
5. [Verification Checklist](#verification-checklist)

---

## Permission Decorators

Django provides built-in decorators and mixins to enforce permissions:

### For Function-Based Views
- `@login_required` - Requires user authentication
- `@permission_required('app.permission')` - Requires specific permission
- `@user_passes_test(test_func)` - Custom test function

### For Class-Based Views
- `LoginRequiredMixin` - Requires authentication
- `PermissionRequiredMixin` - Requires specific permission
- `UserPassesTestMixin` - Custom test function

---

## Function-Based Views (FBV)

### Example Implementation

Create or modify `bookshelf/views.py`:

```python
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Book


# View all books - requires can_view permission
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    Display list of all books.
    Only users with can_view permission can access.
    """
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


# View single book - requires can_view permission
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_detail(request, pk):
    """
    Display details of a single book.
    Only users with can_view permission can access.
    """
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_detail.html', {'book': book})


# Create new book - requires can_create permission
@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """
    Create a new book.
    Only users with can_create permission can access.
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_year = request.POST.get('publication_year')
        
        book = Book.objects.create(
            title=title,
            author=author,
            publication_year=publication_year
        )
        messages.success(request, f'Book "{book.title}" created successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_form.html')


# Edit existing book - requires can_edit permission
@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    """
    Edit an existing book.
    Only users with can_edit permission can access.
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.publication_year = request.POST.get('publication_year')
        book.save()
        
        messages.success(request, f'Book "{book.title}" updated successfully!')
        return redirect('book_detail', pk=book.pk)
    
    return render(request, 'bookshelf/book_form.html', {'book': book})


# Delete book - requires can_delete permission
@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """
    Delete a book.
    Only users with can_delete permission can access.
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'Book "{title}" deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})


# Alternative: Manual permission checking
@login_required
def book_edit_manual(request, pk):
    """
    Example of manual permission checking.
    Use this approach when you need custom logic.
    """
    # Check permission manually
    if not request.user.has_perm('bookshelf.can_edit'):
        messages.error(request, "You don't have permission to edit books.")
        return HttpResponseForbidden("You don't have permission to edit books.")
    
    book = get_object_or_404(Book, pk=pk)
    # ... rest of the view logic
    return render(request, 'bookshelf/book_form.html', {'book': book})
```

### Key Points for FBV

1. **Decorator Order Matters:**
   ```python
   @login_required          # First: Check if user is logged in
   @permission_required('bookshelf.can_edit', raise_exception=True)  # Then: Check permission
   def my_view(request):
       pass
   ```

2. **raise_exception=True:**
   - Raises `PermissionDenied` (403 error)
   - Without it, redirects to login page

3. **Multiple Permissions:**
   ```python
   @permission_required(['bookshelf.can_edit', 'bookshelf.can_delete'])
   def my_view(request):
       # User must have BOTH permissions
       pass
   ```

---

## Class-Based Views (CBV)

### Example Implementation

Add to `bookshelf/views.py`:

```python
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .models import Book


# List all books - requires can_view permission
class BookListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Display list of all books.
    Only users with can_view permission can access.
    """
    model = Book
    template_name = 'bookshelf/book_list.html'
    context_object_name = 'books'
    permission_required = 'bookshelf.can_view'
    
    # Optional: Custom behavior when permission is denied
    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to view books.")
        return redirect('home')


# View single book - requires can_view permission
class BookDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
    Display details of a single book.
    Only users with can_view permission can access.
    """
    model = Book
    template_name = 'bookshelf/book_detail.html'
    context_object_name = 'book'
    permission_required = 'bookshelf.can_view'


# Create new book - requires can_create permission
class BookCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create a new book.
    Only users with can_create permission can access.
    """
    model = Book
    template_name = 'bookshelf/book_form.html'
    fields = ['title', 'author', 'publication_year']
    permission_required = 'bookshelf.can_create'
    success_url = reverse_lazy('book_list')
    success_message = "Book '%(title)s' created successfully!"


# Edit existing book - requires can_edit permission
class BookUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Edit an existing book.
    Only users with can_edit permission can access.
    """
    model = Book
    template_name = 'bookshelf/book_form.html'
    fields = ['title', 'author', 'publication_year']
    permission_required = 'bookshelf.can_edit'
    success_url = reverse_lazy('book_list')
    success_message = "Book '%(title)s' updated successfully!"


# Delete book - requires can_delete permission
class BookDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Delete a book.
    Only users with can_delete permission can access.
    """
    model = Book
    template_name = 'bookshelf/book_confirm_delete.html'
    permission_required = 'bookshelf.can_delete'
    success_url = reverse_lazy('book_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f"Book '{self.get_object().title}' deleted successfully!")
        return super().delete(request, *args, **kwargs)


# Alternative: Custom permission logic with UserPassesTestMixin
class BookUpdateCustomView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Example with custom permission logic.
    """
    model = Book
    fields = ['title', 'author', 'publication_year']
    
    def test_func(self):
        # Custom logic: user must be in Editors group OR have can_edit permission
        user = self.request.user
        return (
            user.groups.filter(name='Editors').exists() or
            user.has_perm('bookshelf.can_edit')
        )
    
    def handle_no_permission(self):
        messages.error(self.request, "You need to be an Editor to modify books.")
        return redirect('book_list')
```

### Key Points for CBV

1. **Mixin Order Matters:**
   ```python
   # Correct order
   class MyView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
       pass
   ```

2. **Multiple Permissions:**
   ```python
   class MyView(PermissionRequiredMixin, UpdateView):
       permission_required = ['bookshelf.can_edit', 'bookshelf.can_delete']
       # User must have BOTH permissions
   ```

3. **Permission for ANY (not all):**
   ```python
   class MyView(UserPassesTestMixin, UpdateView):
       def test_func(self):
           return (
               self.request.user.has_perm('bookshelf.can_edit') or
               self.request.user.has_perm('bookshelf.can_delete')
           )
   ```

---

## URL Configuration

Update `bookshelf/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    # Function-Based Views
    path('books/', views.book_list, name='book_list'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/create/', views.book_create, name='book_create'),
    path('books/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    
    # Or Class-Based Views (comment out FBV if using these)
    # path('books/', views.BookListView.as_view(), name='book_list'),
    # path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    # path('books/create/', views.BookCreateView.as_view(), name='book_create'),
    # path('books/<int:pk>/edit/', views.BookUpdateView.as_view(), name='book_edit'),
    # path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete'),
]
```

Include in main `urls.py`:

```python
# LibraryProject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bookshelf.urls')),
]
```

---

## Testing Permissions

### Step 1: Create Test Users

Use Django shell or create a management command:

```bash
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

# Create test users
viewer = User.objects.create_user(username='viewer_user', password='testpass123')
editor = User.objects.create_user(username='editor_user', password='testpass123')
admin = User.objects.create_user(username='admin_user', password='testpass123')

# Assign to groups
viewers_group = Group.objects.get(name='Viewers')
editors_group = Group.objects.get(name='Editors')
admins_group = Group.objects.get(name='Admins')

viewer.groups.add(viewers_group)
editor.groups.add(editors_group)
admin.groups.add(admins_group)

print("Test users created successfully!")
```

### Step 2: Manual Testing Checklist

#### Test as Viewer (can_view only)

| Action | Expected Result | URL | Status |
|--------|----------------|-----|--------|
| View book list | ✅ Success (200) | `/books/` | |
| View book detail | ✅ Success (200) | `/books/1/` | |
| Create book | ❌ Forbidden (403) | `/books/create/` | |
| Edit book | ❌ Forbidden (403) | `/books/1/edit/` | |
| Delete book | ❌ Forbidden (403) | `/books/1/delete/` | |

#### Test as Editor (can_view, can_create, can_edit)

| Action | Expected Result | URL | Status |
|--------|----------------|-----|--------|
| View book list | ✅ Success (200) | `/books/` | |
| View book detail | ✅ Success (200) | `/books/1/` | |
| Create book | ✅ Success (200) | `/books/create/` | |
| Edit book | ✅ Success (200) | `/books/1/edit/` | |
| Delete book | ❌ Forbidden (403) | `/books/1/delete/` | |

#### Test as Admin (all permissions)

| Action | Expected Result | URL | Status |
|--------|----------------|-----|--------|
| View book list | ✅ Success (200) | `/books/` | |
| View book detail | ✅ Success (200) | `/books/1/` | |
| Create book | ✅ Success (200) | `/books/create/` | |
| Edit book | ✅ Success (200) | `/books/1/edit/` | |
| Delete book | ✅ Success (200) | `/books/1/delete/` | |

### Step 3: Automated Testing

Create `bookshelf/tests.py`:

```python
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from .models import Book

User = get_user_model()


class PermissionEnforcementTests(TestCase):
    """Test that permissions are enforced correctly in views"""
    
    def setUp(self):
        """Set up test users, groups, and books"""
        # Create test book
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            publication_year=2024
        )
        
        # Create groups and assign permissions
        from django.core.management import call_command
        call_command('setup_groups')
        
        # Create test users
        self.viewer = User.objects.create_user('viewer', password='pass123')
        self.editor = User.objects.create_user('editor', password='pass123')
        self.admin = User.objects.create_user('admin', password='pass123')
        
        # Assign to groups
        self.viewer.groups.add(Group.objects.get(name='Viewers'))
        self.editor.groups.add(Group.objects.get(name='Editors'))
        self.admin.groups.add(Group.objects.get(name='Admins'))
        
        self.client = Client()
    
    def test_viewer_can_view_only(self):
        """Test that viewers can only view, not create/edit/delete"""
        self.client.login(username='viewer', password='pass123')
        
        # Can view list
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        
        # Can view detail
        response = self.client.get(reverse('book_detail', args=[self.book.pk]))
        self.assertEqual(response.status_code, 200)
        
        # Cannot create
        response = self.client.get(reverse('book_create'))
        self.assertEqual(response.status_code, 403)
        
        # Cannot edit
        response = self.client.get(reverse('book_edit', args=[self.book.pk]))
        self.assertEqual(response.status_code, 403)
        
        # Cannot delete
        response = self.client.get(reverse('book_delete', args=[self.book.pk]))
        self.assertEqual(response.status_code, 403)
    
    def test_editor_cannot_delete(self):
        """Test that editors can create/edit but not delete"""
        self.client.login(username='editor', password='pass123')
        
        # Can view
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        
        # Can create
        response = self.client.get(reverse('book_create'))
        self.assertEqual(response.status_code, 200)
        
        # Can edit
        response = self.client.get(reverse('book_edit', args=[self.book.pk]))
        self.assertEqual(response.status_code, 200)
        
        # Cannot delete
        response = self.client.get(reverse('book_delete', args=[self.book.pk]))
        self.assertEqual(response.status_code, 403)
    
    def test_admin_has_all_permissions(self):
        """Test that admins can perform all actions"""
        self.client.login(username='admin', password='pass123')
        
        # Can view
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        
        # Can create
        response = self.client.get(reverse('book_create'))
        self.assertEqual(response.status_code, 200)
        
        # Can edit
        response = self.client.get(reverse('book_edit', args=[self.book.pk]))
        self.assertEqual(response.status_code, 200)
        
        # Can delete
        response = self.client.get(reverse('book_delete', args=[self.book.pk]))
        self.assertEqual(response.status_code, 200)
    
    def test_unauthenticated_user_redirected(self):
        """Test that unauthenticated users are redirected to login"""
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertIn('/login/', response.url)


# Run tests with:
# python manage.py test bookshelf
```

---

## Verification Checklist

### Pre-Testing Setup
- [ ] Migrations created and applied
- [ ] Groups created via `python manage.py setup_groups`
- [ ] Test users created and assigned to groups
- [ ] At least one book exists in database

### View Protection
- [ ] All views have `@login_required` or `LoginRequiredMixin`
- [ ] All views have appropriate `@permission_required` or `PermissionRequiredMixin`
- [ ] URLs are correctly configured

### Manual Testing
- [ ] Logged out user cannot access any view (redirected to login)
- [ ] Viewer can access list and detail views
- [ ] Viewer cannot access create, edit, or delete views
- [ ] Editor can access create and edit views
- [ ] Editor cannot access delete views
- [ ] Admin can access all views

### Automated Testing
- [ ] All tests pass with `python manage.py test bookshelf`
- [ ] Test coverage includes all permission scenarios

### User Experience
- [ ] Appropriate error messages displayed when permission denied
- [ ] Success messages shown after successful operations
- [ ] User redirected appropriately after actions

---

## Quick Commands

```bash
# Create and set up groups
python manage.py setup_groups

# Create test data
python manage.py shell < create_test_users.py

# Run tests
python manage.py test bookshelf

# Run specific test
python manage.py test bookshelf.tests.PermissionEnforcementTests.test_viewer_can_view_only

# Check coverage (if installed)
coverage run --source='.' manage.py test bookshelf
coverage report
```

---

## Common Issues & Solutions

### Issue: Permission denied but user is in correct group
**Solution:** User might need to log out and log back in for group changes to take effect.

### Issue: Tests fail with "Permission does not exist"
**Solution:** Run migrations first: `python manage.py migrate`

### Issue: All users get 403
**Solution:** Check that `raise_exception=True` is set and CSRF token is included in forms.

### Issue: Redirect loop on permission denied
**Solution:** Ensure `LOGIN_URL` is set correctly in settings and login page doesn't require permissions.

---

## Summary

✅ **Implemented:**
- Permission-based view protection using decorators and mixins
- Function-based and class-based view examples
- Comprehensive testing approach
- Manual and automated testing procedures

✅ **Key Takeaways:**
- Always use `@login_required` before `@permission_required`
- Set `raise_exception=True` to get proper 403 errors
- Test with actual users in different groups
- Write automated tests for all permission scenarios

✅ **Security Best Practices:**
- Never trust client-side permission checks alone
- Always validate permissions server-side in views
- Use Django's built-in decorators/mixins
- Test thoroughly before deploying to production
