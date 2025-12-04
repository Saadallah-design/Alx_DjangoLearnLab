from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.forms import ValidationError


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def clean(self):
        # Custom validation logic can be added here
        if self.publication_year < 0 or self.publication_year > 2100:
            raise ValidationError('Publication year must be between 0 and 2100.')

    class Meta:
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]

    def __str__(self):
        return self.title
    
# to create a custom user manager
class CustomUserManager(BaseUserManager):
    # Manager methods - CREATE or QUERY multiple users
    def create_user(self, username, email=None, password=None, **extra_fields):
        """Factory method to CREATE a new user"""
        if not username:
            raise ValueError('The Username must be set')
        
        # Normalize email (lowercase the domain part) or set to empty string if None
        if email:
            email = self.normalize_email(email)
        else:
            email = ''  # Set empty string instead of None to avoid NOT NULL constraint
        
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        """the self._db is used in manager methods to specify which database to use when saving or querying objects.
        This is particularly useful in scenarios where one has multiple databases configured in their Django project."""
        user.save(using=self._db)  # Support for multiple databases
        return user
    
    
    # method to create superuser
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """Factory method to CREATE a superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)
    
    def get_active_users(self):
        """Query method to GET multiple users"""
        return self.filter(is_active=True)


# this is Model Layer for Custom User Model
class CustomUser(AbstractUser):
    # here we have extended the default User model with custom fields
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    
    # Override email field to make it optional (blank=True allows empty string)
    email = models.EmailField(blank=True, default='')

    # Attach the custom manager (CRITICAL!)
    objects = CustomUserManager()

    # can create instance methods which operate on a SINGLE user instance
    def get_age(self):
        from datetime import date
        if self.date_of_birth:
            today = date.today()
            # age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
            
            return (date.today() - self.date_of_birth).days // 365
        return None
    
    # instance method 
    def update_profile_photo(self, new_photo):
        """Update this user's profile photo"""
        self.profile_photo = new_photo
        self.save()

    def get_full_display_name(self):
        """Return the user's full name in a display format"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name} (@{self.username})"
        return self.username
    
    # this is a string representation method
    def __str__(self):
        return self.username