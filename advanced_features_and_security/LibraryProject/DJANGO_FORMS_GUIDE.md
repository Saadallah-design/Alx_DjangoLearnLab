# Django Forms - Comprehensive Guide

## Table of Contents
1. [Introduction to Django Forms](#introduction-to-django-forms)
2. [Types of Forms](#types-of-forms)
3. [Form vs ModelForm](#form-vs-modelform)
4. [Creating Forms](#creating-forms)
5. [Form Fields and Widgets](#form-fields-and-widgets)
6. [Form Validation](#form-validation)
7. [Rendering Forms in Templates](#rendering-forms-in-templates)
8. [Handling Forms in Views](#handling-forms-in-views)
9. [Best Practices](#best-practices)
10. [Advanced Topics](#advanced-topics)

---

## Introduction to Django Forms

Django forms handle three distinct parts of working with forms:
1. **Rendering** - Generating HTML form elements
2. **Validation** - Ensuring data meets requirements
3. **Data Cleaning** - Converting submitted data to Python types

### Why Use Django Forms?

**Without Django Forms (Raw HTML):**
```html
<!-- ❌ Manual approach - error-prone -->
<form method="post">
    <input type="text" name="title">
    <input type="text" name="author">
    <input type="number" name="year">
</form>
```
Problems: No validation, no CSRF protection, manual error handling, no data cleaning.

**With Django Forms:**
```python
# ✅ Django approach - automatic handling
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
```
Benefits: Automatic validation, CSRF protection, error handling, HTML generation, data cleaning.

---

## Types of Forms

### 1. **forms.Form** - Generic Form
Used when you need a form NOT directly tied to a model.

**Use Cases:**
- Contact forms
- Search forms
- Login forms
- Custom calculations
- Multi-model forms

**Example:**
```python
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)
    
    def send_email(self):
        # Custom logic to send email
        pass
```

### 2. **forms.ModelForm** - Model-Based Form
Used when you need a form to create or update a model instance.

**Use Cases:**
- Creating/editing database records
- User registration
- CRUD operations
- Any form that maps to a model

**Example:**
```python
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book  # The model to use
        fields = ['title', 'author', 'publication_year']  # Which fields to include
```

---

## Form vs ModelForm

### Comparison Table

| Feature | forms.Form | forms.ModelForm |
|---------|-----------|-----------------|
| **Purpose** | Generic forms | Create/update model instances |
| **Model Binding** | ❌ No | ✅ Yes |
| **Field Definition** | Manual | Automatic from model |
| **save() Method** | ❌ No | ✅ Yes |
| **Validation** | Custom | Model + Custom |
| **Use Case** | Contact, search, login | CRUD operations |

### When to Use Each

**Use `forms.Form` when:**
```python
# Example 1: Search form (no database interaction)
class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)
    category = forms.ChoiceField(choices=[...])

# Example 2: Calculation form
class BMICalculatorForm(forms.Form):
    weight = forms.DecimalField()
    height = forms.DecimalField()
    
    def calculate_bmi(self):
        return self.cleaned_data['weight'] / (self.cleaned_data['height'] ** 2)
```

**Use `forms.ModelForm` when:**
```python
# Example: Creating/editing a database record
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
```

---

## Creating Forms

### Basic ModelForm Structure

```python
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    """
    Step 1: Define the form class inheriting from ModelForm
    """
    
    class Meta:
        """
        Step 2: Configure the Meta class
        This tells Django which model to use and which fields to include
        """
        model = Book  # Which model this form is for
        
        # Option 1: Include specific fields
        fields = ['title', 'author', 'publication_year']
        
        # Option 2: Include all fields
        # fields = '__all__'
        
        # Option 3: Exclude specific fields
        # exclude = ['created_at', 'updated_at']
```

### Field Selection Options

```python
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        
        # ✅ RECOMMENDED: Explicit field list (most secure)
        fields = ['title', 'author', 'publication_year']
        # Pros: Clear, secure, maintainable
        # Cons: Must update when adding new fields
        
        # ⚠️ USE CAREFULLY: All fields
        # fields = '__all__'
        # Pros: Automatic inclusion of new fields
        # Cons: May expose sensitive fields, security risk
        
        # ⚠️ USE CAREFULLY: Exclude specific fields
        # exclude = ['created_at', 'updated_at']
        # Pros: Easy to maintain
        # Cons: May accidentally expose new fields
```

---

## Form Fields and Widgets

### Understanding Fields vs Widgets

**Field** = Data type + validation rules
**Widget** = HTML representation (how it looks)

```python
from django import forms

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        
        # Customize widgets (HTML rendering)
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',          # CSS class
                'placeholder': 'Enter book title', # Placeholder text
                'maxlength': 200,                  # HTML attribute
                'required': True                   # HTML5 validation
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name'
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1000,
                'max': 2100
            })
        }
```

### Common Form Fields

```python
from django import forms

class ExampleForm(forms.Form):
    # Text inputs
    char_field = forms.CharField(max_length=100)
    email_field = forms.EmailField()
    url_field = forms.URLField()
    
    # Numbers
    integer_field = forms.IntegerField(min_value=0, max_value=100)
    decimal_field = forms.DecimalField(max_digits=5, decimal_places=2)
    
    # Dates and times
    date_field = forms.DateField()
    datetime_field = forms.DateTimeField()
    time_field = forms.TimeField()
    
    # Choices
    choice_field = forms.ChoiceField(choices=[
        ('option1', 'Option 1'),
        ('option2', 'Option 2')
    ])
    multiple_choice = forms.MultipleChoiceField(choices=[...])
    
    # Boolean
    boolean_field = forms.BooleanField(required=False)
    
    # Files
    file_field = forms.FileField()
    image_field = forms.ImageField()
    
    # Text areas
    text_area = forms.CharField(widget=forms.Textarea)
```

### Common Widgets

```python
from django import forms

class ExampleForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = '__all__'
        widgets = {
            # Text inputs
            'field1': forms.TextInput(),      # <input type="text">
            'field2': forms.PasswordInput(),  # <input type="password">
            'field3': forms.EmailInput(),     # <input type="email">
            'field4': forms.NumberInput(),    # <input type="number">
            'field5': forms.URLInput(),       # <input type="url">
            
            # Text areas
            'field6': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
            
            # Selects
            'field7': forms.Select(),         # <select>
            'field8': forms.SelectMultiple(), # <select multiple>
            
            # Checkboxes and radios
            'field9': forms.CheckboxInput(),  # <input type="checkbox">
            'field10': forms.RadioSelect(),   # Radio buttons
            
            # Dates
            'field11': forms.DateInput(attrs={'type': 'date'}),  # HTML5 date picker
            
            # Files
            'field12': forms.FileInput(),     # <input type="file">
            'field13': forms.ClearableFileInput(),  # File with clear option
        }
```

---

## Form Validation

Django provides three levels of validation:

### 1. **Field-Level Validation** (Automatic)

Built-in validation from field types:

```python
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        
    # Automatic validations:
    # - title: CharField validates max_length
    # - author: CharField validates max_length
    # - publication_year: IntegerField validates it's an integer
```

### 2. **Custom Field Validation** (clean_<fieldname>)

Validate individual fields with custom logic:

```python
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
    
    def clean_title(self):
        """
        Custom validation for title field.
        Method naming: clean_<field_name>
        """
        title = self.cleaned_data.get('title')
        
        # Validation 1: Minimum length
        if len(title) < 2:
            raise forms.ValidationError('Title must be at least 2 characters long.')
        
        # Validation 2: No numbers in title
        if any(char.isdigit() for char in title):
            raise forms.ValidationError('Title cannot contain numbers.')
        
        # Validation 3: Check for duplicates
        if Book.objects.filter(title__iexact=title).exists():
            raise forms.ValidationError('A book with this title already exists.')
        
        # Must return the cleaned value
        return title
    
    def clean_publication_year(self):
        """Custom validation for publication year"""
        year = self.cleaned_data.get('publication_year')
        
        if year < 1000:
            raise forms.ValidationError('Year must be after 1000.')
        
        if year > 2100:
            raise forms.ValidationError('Year cannot be in the distant future.')
        
        return year
    
    def clean_author(self):
        """Custom validation for author"""
        author = self.cleaned_data.get('author')
        
        # Capitalize each word
        author = author.title()
        
        # Remove extra spaces
        author = ' '.join(author.split())
        
        return author
```

### 3. **Form-Level Validation** (clean)

Validate multiple fields together:

```python
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
    
    def clean(self):
        """
        Form-level validation - validates multiple fields together.
        Called after all field-level validation passes.
        """
        cleaned_data = super().clean()
        
        title = cleaned_data.get('title')
        author = cleaned_data.get('author')
        year = cleaned_data.get('publication_year')
        
        # Example: Check if this exact combination exists
        if title and author and year:
            if Book.objects.filter(
                title=title,
                author=author,
                publication_year=year
            ).exists():
                raise forms.ValidationError(
                    'This book already exists in the database.'
                )
        
        # Example: Business logic validation
        if year and year < 1950 and 'Modern' in title:
            raise forms.ValidationError(
                'Books published before 1950 cannot be labeled as "Modern".'
            )
        
        return cleaned_data
```

### Validation Flow

```
User submits form
       ↓
1. Field type validation (automatic)
   - CharField max_length
   - IntegerField is integer
   - EmailField is valid email
       ↓
2. Field-level clean_<fieldname>() methods
   - clean_title()
   - clean_author()
   - clean_publication_year()
       ↓
3. Form-level clean() method
   - Cross-field validation
       ↓
Form is valid ✅ or has errors ❌
```

---

## Rendering Forms in Templates

### Method 1: Automatic Rendering (Quickest)

```django
<form method="post">
    {% csrf_token %}
    
    <!-- Render all fields as paragraphs -->
    {{ form.as_p }}
    
    <!-- OR as table rows -->
    {{ form.as_table }}
    
    <!-- OR as list items -->
    {{ form.as_ul }}
    
    <button type="submit">Submit</button>
</form>
```

### Method 2: Manual Field Rendering (Most Control)

```django
<form method="post" novalidate>
    {% csrf_token %}
    
    {% if form.non_field_errors %}
        <div class="alert alert-danger">
            {{ form.non_field_errors }}
        </div>
    {% endif %}
    
    {% for field in form %}
        <div class="form-group">
            <label for="{{ field.id_for_label }}">
                {{ field.label }}
                {% if field.field.required %}
                    <span class="required">*</span>
                {% endif %}
            </label>
            
            {{ field }}
            
            {% if field.help_text %}
                <small class="form-text">{{ field.help_text }}</small>
            {% endif %}
            
            {% if field.errors %}
                <div class="error-messages">
                    {% for error in field.errors %}
                        <p class="error">{{ error }}</p>
                    {% endfor %}
                </div>
            {% endif %}
        </div>
    {% endfor %}
    
    <button type="submit">Submit</button>
</form>
```

### Method 3: Individual Field Rendering (Maximum Control)

```django
<form method="post">
    {% csrf_token %}
    
    <div class="form-group">
        <label for="{{ form.title.id_for_label }}">Title</label>
        {{ form.title }}
        {{ form.title.errors }}
    </div>
    
    <div class="form-group">
        <label for="{{ form.author.id_for_label }}">Author</label>
        {{ form.author }}
        {{ form.author.errors }}
    </div>
    
    <div class="form-group">
        <label for="{{ form.publication_year.id_for_label }}">Year</label>
        {{ form.publication_year }}
        {{ form.publication_year.errors }}
    </div>
    
    <button type="submit">Submit</button>
</form>
```

---

## Handling Forms in Views

### Function-Based View Pattern

```python
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BookForm

def book_create(request):
    """Standard form handling pattern"""
    
    if request.method == 'POST':
        # POST request - process form data
        form = BookForm(request.POST, request.FILES)  # Include FILES for file uploads
        
        if form.is_valid():
            # Form is valid - save and redirect
            book = form.save()
            messages.success(request, f'Book "{book.title}" created successfully!')
            return redirect('book_list')
        else:
            # Form has errors - re-render with errors
            messages.error(request, 'Please correct the errors below.')
    else:
        # GET request - show empty form
        form = BookForm()
    
    return render(request, 'bookshelf/book_form.html', {'form': form})
```

### Editing Existing Objects

```python
from django.shortcuts import render, redirect, get_object_or_404

def book_edit(request, pk):
    """Edit existing book"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        # Pass instance to update existing object
        form = BookForm(request.POST, instance=book)
        
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" updated!')
            return redirect('book_list')
    else:
        # Pre-populate form with existing data
        form = BookForm(instance=book)
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form,
        'book': book  # Pass book for template context
    })
```

### Class-Based View Pattern

```python
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages

class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'bookshelf/book_form.html'
    success_url = reverse_lazy('book_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Book created successfully!')
        return super().form_valid(form)

class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'bookshelf/book_form.html'
    success_url = reverse_lazy('book_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Book updated successfully!')
        return super().form_valid(form)
```

---

## Best Practices

### 1. **Always Use CSRF Protection**

```django
<!-- ✅ CORRECT -->
<form method="post">
    {% csrf_token %}  <!-- ALWAYS include this -->
    {{ form.as_p }}
    <button type="submit">Submit</button>
</form>

<!-- ❌ WRONG - Missing CSRF token -->
<form method="post">
    {{ form.as_p }}
    <button type="submit">Submit</button>
</form>
```

### 2. **Explicit Field Lists**

```python
# ✅ RECOMMENDED - Explicit and secure
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

# ❌ AVOID - Can expose sensitive fields
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'  # Dangerous if model has sensitive fields
```

### 3. **Custom Validation**

```python
# ✅ GOOD - Clear validation with helpful messages
def clean_publication_year(self):
    year = self.cleaned_data.get('publication_year')
    
    if year < 1000:
        raise forms.ValidationError(
            'Publication year must be after 1000. Please enter a valid year.'
        )
    
    return year

# ❌ BAD - Vague error message
def clean_publication_year(self):
    year = self.cleaned_data.get('publication_year')
    if year < 1000:
        raise forms.ValidationError('Invalid year')
    return year
```

### 4. **Form Organization**

```python
# ✅ GOOD - Well-organized form
class BookForm(forms.ModelForm):
    """
    Form for creating and editing books.
    Includes custom validation for title and publication year.
    """
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'publication_year': 'Year Published',
        }
    
    def clean_title(self):
        # Field validation
        pass
    
    def clean(self):
        # Form validation
        pass
```

### 5. **User Feedback**

```python
# ✅ GOOD - Clear user feedback
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'✅ Book "{book.title}" created successfully!')
            return redirect('book_list')
        else:
            messages.error(request, '❌ Please correct the errors below.')
    else:
        form = BookForm()
    
    return render(request, 'book_form.html', {'form': form})
```

### 6. **DRY Principle - Reusable Forms**

```python
# ✅ GOOD - One form for create and edit
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

# Use in create view
def book_create(request):
    form = BookForm(request.POST or None)
    # ...

# Use in edit view
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    # ...
```

### 7. **Security Considerations**

```python
# ✅ SECURE - Validate all inputs
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']  # Only safe fields
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        # Sanitize input
        title = title.strip()
        # Validate
        if len(title) < 2:
            raise forms.ValidationError('Title too short')
        return title

# ❌ INSECURE - No validation
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'  # May expose sensitive fields
    # No validation methods
```

---

## Advanced Topics

### 1. **Formsets - Multiple Forms**

```python
from django.forms import modelformset_factory

# Create a formset for editing multiple books at once
BookFormSet = modelformset_factory(
    Book,
    fields=['title', 'author', 'publication_year'],
    extra=3  # Number of empty forms to display
)

def edit_multiple_books(request):
    if request.method == 'POST':
        formset = BookFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('book_list')
    else:
        formset = BookFormSet(queryset=Book.objects.all())
    
    return render(request, 'edit_books.html', {'formset': formset})
```

### 2. **Inline Formsets - Related Objects**

```python
from django.forms import inlineformset_factory

# Edit a publisher and all their books in one form
BookInlineFormSet = inlineformset_factory(
    Publisher,  # Parent model
    Book,       # Child model
    fields=['title', 'author', 'publication_year'],
    extra=2,
    can_delete=True
)
```

### 3. **Dynamic Field Choices**

```python
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'category']
    
    def __init__(self, *args, **kwargs):
        # Get user from kwargs
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Customize based on user
        if user and not user.is_staff:
            # Limit choices for non-staff
            self.fields['category'].queryset = Category.objects.filter(public=True)
```

### 4. **Form Mixins**

```python
class TimestampedFormMixin:
    """Mixin to add created_by and modified_by tracking"""
    
    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        
        if user:
            if not instance.pk:
                instance.created_by = user
            instance.modified_by = user
        
        if commit:
            instance.save()
        
        return instance

class BookForm(TimestampedFormMixin, forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']
```

---

## Quick Reference

### Form Creation Checklist

- [ ] Choose between `forms.Form` and `forms.ModelForm`
- [ ] Define Meta class with model and fields
- [ ] Customize widgets if needed
- [ ] Add custom labels and help text
- [ ] Implement field-level validation (`clean_<field>`)
- [ ] Implement form-level validation (`clean`)
- [ ] Test validation logic
- [ ] Create template with CSRF token
- [ ] Handle form in view (GET and POST)
- [ ] Add user feedback messages
- [ ] Test with valid and invalid data

### Common Patterns

```python
# Pattern 1: Simple ModelForm
class MyForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ['field1', 'field2']

# Pattern 2: Custom validation
def clean_field1(self):
    value = self.cleaned_data.get('field1')
    # Validate
    return value

# Pattern 3: Widget customization
widgets = {
    'field1': forms.TextInput(attrs={'class': 'form-control'})
}

# Pattern 4: View handling
if request.method == 'POST':
    form = MyForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('success')
else:
    form = MyForm()
```

---

## Summary

✅ **Key Takeaways:**
1. Use `ModelForm` for database models, `Form` for other cases
2. Always include CSRF token in templates
3. Implement custom validation for business rules
4. Provide clear error messages to users
5. Use explicit field lists for security
6. Follow Django's validation flow: field → clean_<field> → clean
7. Keep forms DRY - reuse for create and edit
8. Test validation thoroughly

✅ **Security:**
- Always validate on the server side
- Never trust client-side validation alone
- Use explicit field lists
- Sanitize user input
- Include CSRF protection

✅ **User Experience:**
- Provide helpful error messages
- Use appropriate widgets
- Add placeholders and help text
- Show success/error feedback
- Pre-populate forms when editing
