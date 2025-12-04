# Django Custom User Model Guide: AbstractUser vs Managers

## Table of Contents
1. [Understanding Django's User Architecture](#understanding-djangos-user-architecture)
2. [Instance Methods vs Manager Methods](#instance-methods-vs-manager-methods)
3. [When to Use AbstractUser vs AbstractBaseUser](#when-to-use-abstractuser-vs-abstractbaseuser)
4. [Custom Manager Implementation](#custom-manager-implementation)
5. [Common Mistakes and Solutions](#common-mistakes-and-solutions)
6. [Complete Implementation Example](#complete-implementation-example)

---

## Understanding Django's User Architecture

Django's authentication system has three layers:

### 1. **Model Layer** (The User Model)
```python
class User(AbstractUser):
    # Custom fields
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    
    # Instance methods - operate on a SINGLE user instance
    def get_age(self):
        """Calculate user's age from date_of_birth"""
        if self.date_of_birth:
            return (date.today() - self.date_of_birth).days // 365
        return None
    
    def __str__(self):
        return self.username
```

### 2. **Manager Layer** (User.objects)
```python
class CustomUserManager(BaseUserManager):
    # Manager methods - CREATE or QUERY multiple users
    def create_user(self, username, email=None, password=None, **extra_fields):
        """Factory method to CREATE a new user"""
        pass
    
    def get_active_users(self):
        """Query method to GET multiple users"""
        return self.filter(is_active=True)
```

### 3. **QuerySet Layer** (Database Operations)
```python
# These use the manager
User.objects.all()           # Returns QuerySet
User.objects.filter(...)     # Returns QuerySet
User.objects.create_user()   # Returns single User instance
```

---

## Instance Methods vs Manager Methods

### Instance Methods
**Defined in:** The Model class  
**Called on:** A single user object  
**Purpose:** Operations on ONE existing user

```python
class User(AbstractUser):
    bio = models.TextField(blank=True)
    
    # ✅ INSTANCE METHOD - operates on self (one user)
    def update_bio(self, new_bio):
        """Update this user's bio"""
        self.bio = new_bio
        self.save()
    
    def is_adult(self):
        """Check if this user is over 18"""
        return self.get_age() >= 18
    
    def get_full_display_name(self):
        """Get formatted name for this user"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

# Usage:
user = User.objects.get(id=1)  # Get ONE user
user.update_bio("Hello world")  # Call instance method
print(user.is_adult())          # Call instance method
```

### Manager Methods
**Defined in:** A Manager class (inherits BaseUserManager)  
**Called on:** User.objects  
**Purpose:** CREATE users or QUERY multiple users

```python
class CustomUserManager(BaseUserManager):
    # ✅ MANAGER METHOD - creates new users
    def create_user(self, username, email=None, password=None, **extra_fields):
        """Factory method to CREATE a user"""
        if not username:
            raise ValueError('Username is required')
        
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # ✅ MANAGER METHOD - queries multiple users
    def get_adults(self):
        """Get all users over 18"""
        return self.filter(date_of_birth__lte=date.today() - timedelta(days=18*365))
    
    def get_with_photos(self):
        """Get all users who have profile photos"""
        return self.exclude(profile_photo='')

class User(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    
    objects = CustomUserManager()  # Attach manager

# Usage:
user = User.objects.create_user(username='john', password='pass123')  # Manager method
adults = User.objects.get_adults()  # Manager method returns QuerySet
users_with_photos = User.objects.get_with_photos()  # Manager method
```

---

## When to Use AbstractUser vs AbstractBaseUser

### AbstractUser (Recommended for Most Cases)
**Use when:** You want to keep Django's default user fields (username, email, first_name, last_name, etc.) and just add extra fields.

**Includes:**
- `username` (login identifier)
- `email`
- `first_name`, `last_name`
- `is_staff`, `is_active`, `is_superuser`
- `date_joined`, `last_login`
- Password hashing
- Permissions system

```python
# ✅ Good for adding extra fields
class User(AbstractUser):
    # Keep all default fields, add custom ones
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    bio = models.TextField(blank=True)
```

### AbstractBaseUser (Advanced)
**Use when:** You want to completely change the authentication identifier (e.g., use email instead of username).

**Requires:** More setup - you must define `USERNAME_FIELD`, `REQUIRED_FIELDS`, and implement all necessary fields yourself.

```python
# ⚠️ More complex - only if you need different login field
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)  # Login with email
    username = models.CharField(max_length=150, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'  # Login with email instead of username
    REQUIRED_FIELDS = ['username']
    
    objects = CustomUserManager()
```

---

## Custom Manager Implementation

### Why You Need a Custom Manager

Django's authentication commands and admin interface use these methods:

```bash
python manage.py createsuperuser  # Calls create_superuser()
```

```python
# Admin interface and your code use:
User.objects.create_user()       # Called internally
```

### Minimal Required Implementation

```python
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Custom manager for User model with custom create methods
    """
    
    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Create and save a regular User with the given username and password.
        
        Args:
            username (str): Required. The username for the user.
            email (str): Optional. The email address.
            password (str): Optional. Raw password (will be hashed).
            **extra_fields: Additional fields like date_of_birth, profile_photo, etc.
        
        Returns:
            User: The created user instance.
        
        Raises:
            ValueError: If username is not provided.
        """
        if not username:
            raise ValueError('The Username field must be set')
        
        # Normalize email (lowercase the domain part)
        if email:
            email = self.normalize_email(email)
        
        # Create user instance (self.model refers to the User class)
        user = self.model(username=username, email=email, **extra_fields)
        
        # Hash the password (NEVER store plain text passwords!)
        user.set_password(password)
        
        # Save to database (using=self._db supports multiple databases)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given username and password.
        
        Args:
            username (str): Required. The username for the superuser.
            email (str): Optional. The email address.
            password (str): Optional. Raw password (will be hashed).
            **extra_fields: Additional fields.
        
        Returns:
            User: The created superuser instance.
        
        Raises:
            ValueError: If is_staff or is_superuser are not True.
        """
        # Set superuser flags
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        # Validate flags
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        # Reuse create_user logic
        return self.create_user(username, email, password, **extra_fields)
```

### Extended Manager with Custom Queries

```python
class CustomUserManager(BaseUserManager):
    # ... create_user and create_superuser as above ...
    
    def active_users(self):
        """Get all active users"""
        return self.filter(is_active=True)
    
    def users_with_birthdays_this_month(self):
        """Get users with birthdays in current month"""
        current_month = date.today().month
        return self.filter(date_of_birth__month=current_month)
    
    def staff_users(self):
        """Get all staff members"""
        return self.filter(is_staff=True, is_active=True)

# Usage:
active = User.objects.active_users()
birthday_users = User.objects.users_with_birthdays_this_month()
```

---

## Common Mistakes and Solutions

### ❌ Mistake 1: Defining create_user as Instance Method

```python
# WRONG - This won't work with Django's auth system
class User(AbstractUser):
    def create_user(self, username, password):  # ❌ Instance method
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user
```

**Why it's wrong:**
- It's an instance method (requires an existing user object)
- `User.objects.create_user()` won't find it
- `manage.py createsuperuser` will fail

**✅ Correct:**
```python
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):  # ✅ Manager method
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractUser):
    objects = CustomUserManager()  # Attach the manager
```

### ❌ Mistake 2: Using *args Incorrectly

```python
# WRONG
def create_user(self, username, *args, **kwargs):
    user = User(username=username, *args, **kwargs)  # ❌ Can't pass *args here
```

**✅ Correct:**
```python
def create_user(self, username, email=None, password=None, **extra_fields):
    user = self.model(username=username, email=email, **extra_fields)  # ✅ Use **extra_fields
```

### ❌ Mistake 3: Not Using set_password()

```python
# WRONG - Password stored as plain text!
def create_user(self, username, password=None, **extra_fields):
    user = self.model(username=username, **extra_fields)
    user.password = password  # ❌ Plain text password!
    user.save()
```

**✅ Correct:**
```python
def create_user(self, username, password=None, **extra_fields):
    user = self.model(username=username, **extra_fields)
    user.set_password(password)  # ✅ Hashes the password
    user.save(using=self._db)
```

### ❌ Mistake 4: Forgetting to Attach Manager

```python
# WRONG - Manager not attached
class CustomUserManager(BaseUserManager):
    def create_user(self, ...):
        pass

class User(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    # ❌ Missing: objects = CustomUserManager()
```

**✅ Correct:**
```python
class User(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    
    objects = CustomUserManager()  # ✅ Attach the manager
```

### ❌ Mistake 5: Using User() Instead of self.model()

```python
# WRONG
class CustomUserManager(BaseUserManager):
    def create_user(self, username, **extra_fields):
        user = User(username=username, **extra_fields)  # ❌ Hardcoded class name
```

**Why it's wrong:**
- Breaks inheritance if someone extends your User class
- Doesn't work with Django's model system properly

**✅ Correct:**
```python
class CustomUserManager(BaseUserManager):
    def create_user(self, username, **extra_fields):
        user = self.model(username=username, **extra_fields)  # ✅ Uses manager's model
```

---

## Complete Implementation Example

Here's a full working example:

```python
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from datetime import date, timedelta


class CustomUserManager(BaseUserManager):
    """
    Custom manager for User model.
    Provides factory methods for creating users and superusers.
    """
    
    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Create and save a regular User.
        
        Usage:
            user = User.objects.create_user(
                username='john',
                email='john@example.com',
                password='securepass123',
                date_of_birth='1990-01-15'
            )
        """
        if not username:
            raise ValueError('The Username field must be set')
        
        # Normalize email
        if email:
            email = self.normalize_email(email)
        
        # Create user instance
        user = self.model(username=username, email=email, **extra_fields)
        
        # Hash password
        user.set_password(password)
        
        # Save to database
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Create and save a SuperUser.
        
        Usage:
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='adminpass123'
            )
        """
        # Set required superuser flags
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        # Validate
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(username, email, password, **extra_fields)
    
    # Custom query methods
    def active_users(self):
        """Return all active users"""
        return self.filter(is_active=True)
    
    def get_adults(self):
        """Return users over 18 years old"""
        eighteen_years_ago = date.today() - timedelta(days=18*365)
        return self.filter(date_of_birth__lte=eighteen_years_ago)


class User(AbstractUser):
    """
    Custom User model extending AbstractUser.
    Adds date_of_birth and profile_photo fields.
    """
    # Custom fields
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    
    # Attach custom manager
    objects = CustomUserManager()
    
    # Instance methods
    def __str__(self):
        return self.username
    
    def get_age(self):
        """Calculate and return user's age"""
        if not self.date_of_birth:
            return None
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    def has_profile_photo(self):
        """Check if user has uploaded a profile photo"""
        return bool(self.profile_photo)
    
    def get_display_name(self):
        """Return full name or username"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
```

### Usage Examples

```python
# Creating users (Manager methods)
user1 = User.objects.create_user(
    username='john_doe',
    email='john@example.com',
    password='secure_password_123',
    first_name='John',
    last_name='Doe',
    date_of_birth='1990-05-15'
)

# Creating superuser (Manager method)
admin = User.objects.create_superuser(
    username='admin',
    email='admin@example.com',
    password='admin_password_123'
)

# Using instance methods
print(user1.get_age())  # e.g., 34
print(user1.get_display_name())  # "John Doe"
print(user1.has_profile_photo())  # False

# Using custom manager query methods
active_users = User.objects.active_users()
adults = User.objects.get_adults()

# Standard Django ORM (uses manager)
all_users = User.objects.all()
johns = User.objects.filter(first_name='John')
```

---

## Configuration Steps

### 1. Update settings.py
```python
# Tell Django to use your custom user model
AUTH_USER_MODEL = 'bookshelf.User'
```

### 2. Create and apply migrations
```bash
# If this is a NEW project (before any migrations)
python manage.py makemigrations
python manage.py migrate

# If you already have migrations, you'll need to:
# 1. Delete db.sqlite3
# 2. Delete all migration files except __init__.py
# 3. Then run makemigrations and migrate
```

### 3. Update admin.py (optional but recommended)
```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('date_of_birth', 'profile_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('date_of_birth', 'profile_photo')}),
    )
```

### 4. Test your implementation
```bash
# Create a superuser
python manage.py createsuperuser

# Start the development server
python manage.py runserver

# Login to admin at http://127.0.0.1:8000/admin
```

---

## Key Takeaways

1. **Manager methods** = CREATE users or QUERY multiple users → Defined in `CustomUserManager`
2. **Instance methods** = Operations on ONE existing user → Defined in `User` model
3. **Always use `set_password()`** to hash passwords
4. **Use `self.model()`** in managers, not hardcoded class names
5. **Attach manager** with `objects = CustomUserManager()`
6. **Set `AUTH_USER_MODEL`** in settings.py
7. **`**extra_fields`** automatically handles your custom fields
8. **Both `create_user` and `create_superuser`** are required for Django's auth system

---

## Quick Reference

| Need to... | Use... | Example |
|------------|--------|---------|
| Create a user | Manager method | `User.objects.create_user(...)` |
| Get one user | Manager query | `User.objects.get(id=1)` |
| Get multiple users | Manager query | `User.objects.filter(...)` |
| Update a user's field | Instance method | `user.update_bio(...)` or `user.bio = '...'` |
| Check user property | Instance method | `user.get_age()` |
| Custom creation logic | Manager method | Define in `CustomUserManager` |
| Custom user behavior | Instance method | Define in `User` model |

---

## Additional Resources

- [Django Official Docs: Customizing Authentication](https://docs.djangoproject.com/en/stable/topics/auth/customizing/)
- [Django Official Docs: User Model](https://docs.djangoproject.com/en/stable/ref/contrib/auth/)
- [Django Best Practices: Custom User Model](https://learndjango.com/tutorials/django-custom-user-model)
