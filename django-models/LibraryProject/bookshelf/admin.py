from django.contrib import admin

from .models import Book
# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')

    list_filter = ('publication_year', 'author')

    search_fields = ('title', 'author')

    list_display_links = ('title', 'author')



# Register your model with the custom ModelAdmin class
admin.site.register(Book, BookAdmin)

