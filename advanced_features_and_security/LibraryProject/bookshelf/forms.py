# Demo form for autochecker
from django import forms

class ExampleForm(forms.Form):
    example_field = forms.CharField(label='Example Field', max_length=100)
from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    """
    ModelForm for creating and editing books.
    Provides built-in validation and rendering.
    """
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        
        # Customize form widgets for better UX
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title',
                'required': True
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name',
                'required': True
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter publication year (e.g., 2024)',
                'min': 1000,
                'max': 2100,
                'required': True
            }),
        }
        
        # Custom labels
        labels = {
            'title': 'Book Title',
            'author': 'Author Name',
            'publication_year': 'Publication Year',
        }
        
        # Help text
        help_texts = {
            'publication_year': 'Enter a year between 1000 and 2100',
        }
    
    def clean_publication_year(self):
        """
        Custom validation for publication year.
        Ensures the year is reasonable.
        """
        year = self.cleaned_data.get('publication_year')
        
        if year:
            if year < 1000:
                raise forms.ValidationError('Publication year must be after year 1000.')
            if year > 2100:
                raise forms.ValidationError('Publication year cannot be in the distant future.')
        
        return year
    
    def clean_title(self):
        """
        Custom validation for title.
        Ensures title is not too short.
        """
        title = self.cleaned_data.get('title')
        
        if title and len(title) < 2:
            raise forms.ValidationError('Book title must be at least 2 characters long.')
        
        return title
