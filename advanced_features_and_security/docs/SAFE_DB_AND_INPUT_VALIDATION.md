# Safe Database Usage and Input Validation in Django

This guide explains how to safely interact with the database using Django’s ORM and how to validate and sanitize user input to prevent security vulnerabilities like SQL injection and XSS.

---

## 1. Use Django’s ORM to Parameterize Queries

**Never** use string formatting or concatenation to build SQL queries. Always use Django’s ORM methods, which automatically parameterize queries and prevent SQL injection.

### Example: Safe Query
```python
# BAD (vulnerable to SQL injection!)
Book.objects.raw(f"SELECT * FROM bookshelf_book WHERE title = '{user_input}'")

# GOOD (safe, parameterized)
Book.objects.filter(title=user_input)
```

- The ORM escapes and parameterizes all values, so user input cannot break out of the query.
- For custom SQL, use parameter substitution:
```python
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM bookshelf_book WHERE title = %s", [user_input])
    rows = cursor.fetchall()
```

---

## 2. Validate and Sanitize All User Inputs

Always use Django forms or model validation to ensure user data is correct and safe.

### Example: Using Django Forms
```python
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

    def clean_title(self):
        title = self.cleaned_data['title']
        # Add custom validation if needed
        return title
```

- Forms automatically validate types, required fields, and can be extended with custom validation.
- Forms also escape output in templates, preventing XSS.

### Example: Using Model Validation
```python
class Book(models.Model):
    # ... fields ...
    def clean(self):
        if self.publication_year < 0:
            raise ValidationError('Year must be positive')
```

---

## 3. Never Trust User Input
- Always validate and clean data from forms, query parameters, and file uploads.
- Use `form.is_valid()` before saving or using form data.
- Escape output in templates (Django does this by default).

---

## 4. References
- [Django ORM Security](https://docs.djangoproject.com/en/5.2/topics/security/#sql-injection-protection)
- [Django Forms](https://docs.djangoproject.com/en/5.2/topics/forms/)
- [Model Validation](https://docs.djangoproject.com/en/5.2/ref/models/instances/#validating-objects)

---

**Summary:**
- Use Django ORM/filter methods, not raw SQL or string formatting.
- Always validate and sanitize user input with forms or model validation.
- Never trust user input—validate, clean, and escape everything.
