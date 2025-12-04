"""
SIMPLE DJANGO FORMS - EDUCATIONAL EXAMPLE
==========================================

This file demonstrates Django forms from the absolute basics.
We'll build up from the simplest possible form to more complex examples.

KEY CONCEPT: What is a Django Form?
- A Python class that represents an HTML form
- Handles rendering HTML, validation, and data cleaning
- Makes form handling safer and easier than raw HTML
"""

from django import forms
from .models import Book


# =============================================================================
# EXAMPLE 1: THE SIMPLEST POSSIBLE FORM
# =============================================================================

class SimpleContactForm(forms.Form):
    """
    The most basic form possible - just one text field.
    
    This demonstrates:
    - How to create a form class (inherit from forms.Form)
    - How to define a single field
    - Basic field properties (max_length)
    
    Usage in view:
        form = SimpleContactForm()
    
    In template:
        {{ form.as_p }}
    """
    # Field definition: field_name = forms.FieldType(options)
    name = forms.CharField(max_length=100)
    
    # That's it! This creates:
    # - HTML: <input type="text" name="name" maxlength="100">
    # - Validation: Ensures name is provided and <= 100 characters
    # - Cleaning: Converts form data to Python string


# =============================================================================
# EXAMPLE 2: FORM WITH MULTIPLE FIELDS
# =============================================================================

class ContactForm(forms.Form):
    """
    A slightly more complex form with multiple field types.
    
    This demonstrates:
    - Different field types (CharField, EmailField, etc.)
    - Field arguments (required, initial, help_text)
    - How Django creates different HTML elements
    """
    
    # Text input - required by default
    name = forms.CharField(
        max_length=100,
        help_text="Enter your full name"  # Shows under the field
    )
    
    # Email input - automatically validates email format
    email = forms.EmailField(
        help_text="We'll never share your email"
    )
    
    # Text area - for longer text
    message = forms.CharField(
        widget=forms.Textarea,  # Changes HTML to <textarea>
        help_text="Enter your message (max 500 characters)",
        max_length=500
    )
    
    # Optional field - not required
    phone = forms.CharField(
        required=False,  # User can leave this blank
        max_length=20,
        help_text="Optional: Your phone number"
    )
    
    # Boolean field - checkbox
    subscribe = forms.BooleanField(
        required=False,  # Checkboxes should usually be optional
        initial=True,    # Checked by default
        help_text="Send me updates"
    )


# =============================================================================
# EXAMPLE 3: FORM WITH CHOICES (DROPDOWNS)
# =============================================================================

class FeedbackForm(forms.Form):
    """
    Form demonstrating choice fields (dropdowns, radio buttons).
    
    This demonstrates:
    - How to create dropdown menus
    - Radio buttons
    - Choice field formats
    """
    
    # Text input
    name = forms.CharField(max_length=100)
    
    # Dropdown menu - single selection
    rating = forms.ChoiceField(
        choices=[
            # Format: (value_stored_in_database, label_shown_to_user)
            ('1', '⭐ Poor'),
            ('2', '⭐⭐ Fair'),
            ('3', '⭐⭐⭐ Good'),
            ('4', '⭐⭐⭐⭐ Very Good'),
            ('5', '⭐⭐⭐⭐⭐ Excellent'),
        ],
        help_text="How would you rate our service?"
    )
    
    # Radio buttons - same as ChoiceField but different widget
    recommendation = forms.ChoiceField(
        choices=[
            ('yes', 'Yes, definitely'),
            ('maybe', 'Maybe'),
            ('no', 'No'),
        ],
        widget=forms.RadioSelect,  # Renders as radio buttons instead of dropdown
        help_text="Would you recommend us to a friend?"
    )
    
    # Multiple choice - allows selecting multiple options
    interests = forms.MultipleChoiceField(
        choices=[
            ('books', 'Books'),
            ('music', 'Music'),
            ('movies', 'Movies'),
            ('sports', 'Sports'),
        ],
        required=False,
        widget=forms.CheckboxSelectMultiple,  # Renders as checkboxes
        help_text="Select all that apply"
    )
    
    # Text area for comments
    comments = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        required=False,
        help_text="Any additional comments?"
    )


# =============================================================================
# EXAMPLE 4: FORM WITH CUSTOM VALIDATION
# =============================================================================

class RegistrationForm(forms.Form):
    """
    Form demonstrating custom validation.
    
    This demonstrates:
    - How to add custom validation to individual fields
    - The clean_<fieldname>() pattern
    - How to raise validation errors
    """
    
    username = forms.CharField(
        max_length=50,
        help_text="Choose a unique username (3-50 characters)"
    )
    
    email = forms.EmailField()
    
    age = forms.IntegerField(
        min_value=1,
        max_value=120,
        help_text="You must be at least 13 years old"
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput,  # Hides text as you type
        help_text="Minimum 8 characters"
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        help_text="Re-enter your password"
    )
    
    # CUSTOM VALIDATION METHODS
    # -------------------------
    # Pattern: def clean_<fieldname>(self):
    # These methods run automatically when form.is_valid() is called
    
    def clean_username(self):
        """
        Custom validation for username field.
        
        This method is automatically called when validating the form.
        It runs AFTER the field's built-in validation (max_length, etc.)
        
        Must return the cleaned value!
        """
        # Get the submitted value (after basic validation)
        username = self.cleaned_data.get('username')
        
        # Rule 1: Minimum length
        if len(username) < 3:
            raise forms.ValidationError(
                "Username must be at least 3 characters long."
            )
        
        # Rule 2: Only alphanumeric and underscores
        if not username.replace('_', '').isalnum():
            raise forms.ValidationError(
                "Username can only contain letters, numbers, and underscores."
            )
        
        # Rule 3: Check if username already exists (example)
        # if User.objects.filter(username=username).exists():
        #     raise forms.ValidationError(
        #         "This username is already taken."
        #     )
        
        # IMPORTANT: Always return the cleaned value
        return username
    
    def clean_age(self):
        """
        Custom validation for age field.
        
        Ensures user is at least 13 years old.
        """
        age = self.cleaned_data.get('age')
        
        if age and age < 13:
            raise forms.ValidationError(
                "You must be at least 13 years old to register."
            )
        
        return age
    
    def clean_password(self):
        """
        Custom validation for password strength.
        """
        password = self.cleaned_data.get('password')
        
        # Minimum length
        if len(password) < 8:
            raise forms.ValidationError(
                "Password must be at least 8 characters long."
            )
        
        # Must contain at least one number
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError(
                "Password must contain at least one number."
            )
        
        return password
    
    def clean(self):
        """
        Form-level validation - validates multiple fields together.
        
        This method runs AFTER all field-level clean_<fieldname>() methods.
        Use it when you need to validate relationships between fields.
        """
        # Get all cleaned data
        cleaned_data = super().clean()
        
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        # Check if passwords match
        if password and confirm_password:
            if password != confirm_password:
                # This is a form-level error, not specific to one field
                raise forms.ValidationError(
                    "The two password fields must match."
                )
        
        # Always return cleaned_data
        return cleaned_data


# =============================================================================
# EXAMPLE 5: SIMPLE MODEL FORM (CONNECTED TO DATABASE)
# =============================================================================

class SimpleBookForm(forms.ModelForm):
    """
    A ModelForm - automatically creates form from a database model.
    
    This demonstrates:
    - The difference between forms.Form and forms.ModelForm
    - How Django automatically creates fields from model
    - The Meta class configuration
    - Why ModelForm is easier for database operations
    
    KEY DIFFERENCE from forms.Form:
    - forms.Form: Generic form, not connected to database
    - forms.ModelForm: Connected to a model, has save() method
    """
    
    class Meta:
        """
        Meta class tells Django:
        - Which model to use
        - Which fields to include
        - How to customize them
        """
        
        # 1. WHICH MODEL?
        model = Book  # This is our Book model from models.py
        
        # 2. WHICH FIELDS?
        # Django will automatically create form fields for these
        fields = ['title', 'author', 'publication_year']
        
        # Django automatically knows:
        # - title is CharField → creates text input
        # - author is CharField → creates text input
        # - publication_year is IntegerField → creates number input
    
    # That's it! This automatically creates a form with:
    # - All the specified fields
    # - Proper field types
    # - Model-level validation
    # - A save() method to save to database


# =============================================================================
# EXAMPLE 6: CUSTOMIZED MODEL FORM
# =============================================================================

class CustomBookForm(forms.ModelForm):
    """
    A more advanced ModelForm with customizations.
    
    This demonstrates:
    - How to customize auto-generated fields
    - Adding custom labels and help text
    - Customizing widgets (HTML elements)
    - Adding custom validation to ModelForm
    """
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        
        # CUSTOMIZE LABELS (what users see)
        labels = {
            'title': 'Book Title',
            'author': 'Author Name',
            'publication_year': 'Year Published',
        }
        
        # CUSTOMIZE HELP TEXT (hints under fields)
        help_texts = {
            'title': 'Enter the full title of the book',
            'author': 'Enter the author\'s full name',
            'publication_year': 'Enter a year between 1000 and 2100',
        }
        
        # CUSTOMIZE WIDGETS (HTML rendering)
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',  # Add CSS class
                'placeholder': 'e.g., To Kill a Mockingbird',  # Placeholder text
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Harper Lee',
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1000,  # HTML5 min attribute
                'max': 2100,  # HTML5 max attribute
                'placeholder': 'e.g., 1960',
            }),
        }
    
    # CUSTOM VALIDATION (same as regular Form)
    def clean_title(self):
        """Validate that title is not too short"""
        title = self.cleaned_data.get('title')
        
        if title and len(title) < 2:
            raise forms.ValidationError(
                'Title must be at least 2 characters long.'
            )
        
        return title
    
    def clean_publication_year(self):
        """Validate that publication year is reasonable"""
        year = self.cleaned_data.get('publication_year')
        
        if year:
            if year < 1000:
                raise forms.ValidationError(
                    'Publication year must be after 1000.'
                )
            if year > 2100:
                raise forms.ValidationError(
                    'Publication year cannot be in the distant future.'
                )
        
        return year


# =============================================================================
# EXAMPLE 7: HOW TO USE FORMS IN VIEWS (REFERENCE)
# =============================================================================

"""
VIEW USAGE EXAMPLES:
--------------------

# Example 1: Basic Form in View
def contact_view(request):
    if request.method == 'POST':
        # User submitted the form
        form = ContactForm(request.POST)
        
        if form.is_valid():
            # Form is valid - access cleaned data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Do something with the data (send email, save to DB, etc.)
            # ...
            
            return redirect('success')
    else:
        # User is viewing the form (GET request)
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})


# Example 2: ModelForm in View (Create)
def book_create_view(request):
    if request.method == 'POST':
        form = SimpleBookForm(request.POST)
        
        if form.is_valid():
            # Save directly to database!
            book = form.save()
            return redirect('book_list')
    else:
        form = SimpleBookForm()
    
    return render(request, 'book_form.html', {'form': form})


# Example 3: ModelForm in View (Edit)
def book_edit_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        # Pass instance to update existing book
        form = SimpleBookForm(request.POST, instance=book)
        
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        # Pre-populate form with existing data
        form = SimpleBookForm(instance=book)
    
    return render(request, 'book_form.html', {'form': form})
"""


# =============================================================================
# EXAMPLE 8: HOW TO USE FORMS IN TEMPLATES (REFERENCE)
# =============================================================================

"""
TEMPLATE USAGE EXAMPLES:
------------------------

<!-- Example 1: Automatic rendering (quickest) -->
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}  <!-- Renders all fields as paragraphs -->
    <button type="submit">Submit</button>
</form>


<!-- Example 2: Loop through fields (more control) -->
<form method="post">
    {% csrf_token %}
    
    {% for field in form %}
        <div class="form-group">
            <label>{{ field.label }}</label>
            {{ field }}
            
            {% if field.help_text %}
                <small>{{ field.help_text }}</small>
            {% endif %}
            
            {% if field.errors %}
                <div class="errors">
                    {{ field.errors }}
                </div>
            {% endif %}
        </div>
    {% endfor %}
    
    <button type="submit">Submit</button>
</form>


<!-- Example 3: Individual field rendering (maximum control) -->
<form method="post">
    {% csrf_token %}
    
    <div>
        <label>{{ form.name.label }}</label>
        {{ form.name }}
        {{ form.name.errors }}
    </div>
    
    <div>
        <label>{{ form.email.label }}</label>
        {{ form.email }}
        {{ form.email.errors }}
    </div>
    
    <button type="submit">Submit</button>
</form>
"""


# =============================================================================
# KEY CONCEPTS SUMMARY
# =============================================================================

"""
FORMS VS MODELFORMS - WHEN TO USE WHAT?
---------------------------------------

Use forms.Form when:
✓ Form is not connected to a database model
✓ Contact forms, search forms, login forms
✓ Calculations or processing that don't save to DB
✓ Multi-model forms (combining data from multiple models)

Use forms.ModelForm when:
✓ Form creates or edits a database record
✓ You want automatic field generation from model
✓ You need the save() method
✓ Most CRUD (Create, Read, Update, Delete) operations


VALIDATION FLOW:
---------------
1. User submits form
2. Field-level validation (automatic: max_length, email format, etc.)
3. Field-level clean_<fieldname>() methods (custom validation)
4. Form-level clean() method (cross-field validation)
5. form.is_valid() returns True or False


IMPORTANT METHODS:
-----------------
- form.is_valid() → Returns True if form passes all validation
- form.cleaned_data → Dictionary of validated, cleaned data
- form.save() → (ModelForm only) Saves to database
- form.errors → Dictionary of validation errors


BEST PRACTICES:
--------------
1. Always include {% csrf_token %} in form templates
2. Use explicit field lists in ModelForm (not fields = '__all__')
3. Provide helpful error messages in validation
4. Always return cleaned data from clean_* methods
5. Use ModelForm when working with database models
6. Add help_text to guide users
7. Test validation thoroughly
"""
