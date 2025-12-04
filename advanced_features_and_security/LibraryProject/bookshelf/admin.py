from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Book
# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')

    list_filter = ('publication_year', 'author')

    search_fields = ('title', 'author')

    list_display_links = ('title', 'author')



# Register your model with the custom ModelAdmin class
admin.site.register(Book, BookAdmin)
admin.site.site_header = "Library Project Admin"
admin.site.site_title = "Library Project Admin Portal"
admin.site.index_title = "Welcome to the Library Project Admin Portal"


# Custom UserAdmin to display custom fields
class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for User model.
    Extends Django's UserAdmin to include custom fields (date_of_birth, profile_photo).
    Provides comprehensive user management capabilities for administrators.
    """
    model = User
    
    # Add custom fields to the user detail/edit page
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('date_of_birth', 'profile_photo'),
            'description': 'Custom fields for extended user profile'
        }),
    )
    
    # Add custom fields to the 'add new user' page
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('date_of_birth', 'profile_photo'),
        }),
    )
    
    # Display these fields in the user list view
    list_display = [
        'username', 
        'email', 
        'first_name', 
        'last_name', 
        'date_of_birth', 
        'is_staff',
        'is_active',
        'date_joined'
    ]
    
    # Add sidebar filters for easy user filtering
    list_filter = [
        'is_staff', 
        'is_superuser', 
        'is_active', 
        'date_joined',
        'last_login'
    ]
    
    # Enable search on these fields
    search_fields = [
        'username', 
        'email', 
        'first_name', 
        'last_name'
    ]
    
    # Order users by date joined (newest first)
    ordering = ['-date_joined']
    
    # Enable these fields to be edited directly from the list view
    list_editable = ['is_active']
    
    # Add pagination - show 25 users per page
    list_per_page = 25
    
    # Show user count at the top
    show_full_result_count = True


# Register User model with CustomUserAdmin
admin.site.register(User, CustomUserAdmin)