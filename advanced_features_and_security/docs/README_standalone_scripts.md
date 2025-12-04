# How to Write Standalone Django Scripts (e.g., add_sample_books.py)

Standalone Django scripts are Python files you run directly (not via `manage.py`) to interact with your Django project's models, database, or settings. They are useful for tasks like data import/export, batch updates, or one-off admin jobs.

## Key Steps for a Standalone Django Script

1. **Set the Django Settings Module**
   - Django needs to know which settings to use. Set the environment variable `DJANGO_SETTINGS_MODULE` to your project's settings module (e.g., `LibraryProject.settings`).
   ```python
   import os
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
   ```

2. **Initialize Django**
   - Before importing any models, call `django.setup()` to initialize the Django application registry and settings.
   ```python
   import django
   django.setup()
   ```

3. **Import Your Models**
   - Now you can safely import models and use Django ORM as usual.
   ```python
   from bookshelf.models import Book
   ```

4. **Write Your Logic**
   - Use the ORM to create, update, or query objects. For example, to add books:
   ```python
   Book.objects.create(title="Example", author="Someone", publication_year=2020)
   ```

5. **Run the Script**
   - From your project root, run:
   ```sh
   python3 add_sample_books.py
   ```

## What Happens Behind the Scenes?
- Setting `DJANGO_SETTINGS_MODULE` tells Django where to find your settings (database config, installed apps, etc).
- `django.setup()` loads the settings, configures the app registry, and prepares the ORM.
- After setup, you can use all Django features (models, queries, etc) just like in views or management commands.

## When to Use Standalone Scripts
- Data migration or seeding (like adding sample books)
- Batch processing or cleanup
- Exporting/importing data
- One-off admin tasks

## Tips
- Always set up Django before importing models.
- Use `get_or_create` to avoid duplicate entries.
- For more complex scripts, consider writing a [custom management command](https://docs.djangoproject.com/en/5.2/howto/custom-management-commands/) (invoked via `python manage.py mycommand`).

---

**Example: Minimal Standalone Script**
```python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()
from bookshelf.models import Book
Book.objects.create(title="Minimal Example", author="A. Author", publication_year=2025)
```

---

For more info, see the [Django docs on standalone scripts](https://docs.djangoproject.com/en/5.2/topics/settings/#calling-django-setup-is-required-for-standalone-django-usage).
